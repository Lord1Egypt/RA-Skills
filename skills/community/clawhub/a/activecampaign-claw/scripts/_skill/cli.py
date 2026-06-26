"""Common CLI driver for skill scripts.

Provides `cli_main()` — a template that handles the boilerplate every
analysis script needs: argparse with the standard `--format` and
`--output` flags, the `ACClient` instantiation, the
fetch → analyze → render → write flow, optional 403 handling for
plan-gated endpoints, optional `emit_files()` on output, and optional
history logging.

Scripts opt in by calling `cli_main(...)` from their `__main__` block
instead of writing a `main()`.

Status: opt-in. Existing scripts continue to work unchanged.
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

from _skill.client import ACClient, ACClientError
from _skill.history import log_outcome
from _skill.reports import emit_files, render_feature_unavailable


def cli_main(
    *,
    description: str,
    fetch_data: Callable[..., Any],
    analyze: Callable[..., dict],
    render_markdown: Callable[[dict], str],
    add_arguments: Callable[[argparse.ArgumentParser], None] | None = None,
    feature_unavailable: tuple[str, str, str] | None = None,
    history_recipe: str | None = None,
    history_metrics: Callable[[dict], dict] | None = None,
) -> None:
    """Drive a script through the common analysis lifecycle.

    Arguments:
        description: argparse description text.
        fetch_data: callable accepting `(client)` or `(client, args)`.
            Whichever signature is detected via `inspect.signature`.
        analyze: callable accepting `(data)` or `(data, args)`.
        render_markdown: callable accepting the analyze result; returns
            markdown.
        add_arguments: optional callback to add script-specific argparse
            arguments. Standard `--format` and `--output` are added by
            this function.
        feature_unavailable: optional `(feature, plan, what_this_does)`
            tuple. If `fetch_data` raises an `ACClientError` with status
            403, this function renders the friendly plan-tier markdown
            and exits 0. If omitted, the 403 is re-raised.
        history_recipe: if set, write a `history.jsonl` entry tagged with
            this recipe name after the run.
        history_metrics: optional callable that builds the metric dict
            for the history entry, given the analyze result.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None,
                        help="Write the report to this path instead of stdout")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress messages on stderr (default on for "
                             "TELEGRAM_QUIET=1 or when stderr isn't a tty)")
    if add_arguments is not None:
        add_arguments(parser)
    args = parser.parse_args()

    # Bind a progress callable onto the args namespace. Scripts that want to
    # emit per-step progress can call `args.progress("Pulling tags...")` and
    # the line goes to stderr (or nowhere, if --quiet). Scripts that don't
    # use it pay nothing.
    quiet = (
        args.quiet
        or os.environ.get("TELEGRAM_QUIET") == "1"
        or not sys.stderr.isatty()
    )
    if quiet:
        args.progress = lambda _msg: None
    else:
        def _emit(msg: str) -> None:
            sys.stderr.write(f"  → {msg}\n")
            sys.stderr.flush()
        args.progress = _emit

    client = ACClient()

    try:
        data = _call_with_optional_args(fetch_data, client, args)
    except ACClientError as e:
        if e.status_code == 403 and feature_unavailable is not None:
            feature, plan, what = feature_unavailable
            if args.format == "json":
                print(json.dumps({
                    "unavailable": True,
                    "feature": feature,
                    "plan_required": plan,
                    "reason": what,
                }, indent=2))
            else:
                print(render_feature_unavailable(feature, plan, what))
            return
        raise

    report = _call_with_optional_args(analyze, data, args, second_pos=True)

    if args.format == "json":
        out = json.dumps(report, indent=2, default=str)
    else:
        out = render_markdown(report)

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(out)
        print(f"Wrote {path}", file=sys.stderr)
        emit_files(path)
    else:
        print(out)

    if history_recipe is not None:
        metrics = history_metrics(report) if history_metrics is not None else {}
        log_outcome(f"{history_recipe}_executed",
                    recipe=history_recipe, **metrics)


def _call_with_optional_args(fn: Callable[..., Any], first_pos: Any,
                             args: argparse.Namespace,
                             second_pos: bool = False) -> Any:
    """Invoke `fn` passing args only if its signature has a param named `args`.

    The name check (rather than positional-count check) avoids accidentally
    passing the argparse Namespace into a parameter the script intended for
    something else (e.g. `analyze(data, now=None)` in tasks_audit).
    """
    sig = inspect.signature(fn)
    has_args_param = "args" in sig.parameters
    if has_args_param:
        return fn(first_pos, args)
    return fn(first_pos)
