#!/usr/bin/env python3
"""Validate a chat-format JSONL dataset for Crusoe Serverless Fine-Tuning.

Checks the format rules from docs.crusoe.ai (serverless-fine-tuning):
messages-array chat rows, assistant-only loss targets, model-specific quirks,
and sequence-length limits. Exits non-zero when errors are found.

Usage:
    python3 validate_dataset.py train.jsonl [--model qwen/Qwen3.5-9B]
                                           [--holdout 0.1 --train-out tr.jsonl --val-out va.jsonl]
                                           [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_FILE_BYTES = 3 * 1024**3
SIZE_WARN_BYTES = int(2.5 * 1024**3)
CHARS_PER_TOKEN = 3.5
VALID_ROLES = {"system", "user", "assistant", "tool"}
SPLIT_SEED = 42
DEFAULT_CONTEXT_TOKENS = 32_768

# Context windows (tokens) from docs.crusoe.ai available-models, matched by
# substring against the --model argument.
MODEL_CONTEXT_TOKENS = {
    "deepseek-v4-flash": 1_000_000,
    "gemma-4": 262_000,
    "llama-3.3-70b": 131_000,
    "nemotron-3.5": 1_000_000,
    "gpt-oss-120b": 131_000,
    "qwen3-235b": 262_000,
    "qwen3.8-27b": 262_000,
    "glm-5.2": 1_000_000,
}


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    row: int | None
    message: str


@dataclass
class Args:
    path: Path
    model: str | None
    context_length: int
    holdout: float | None
    train_out: Path | None
    val_out: Path | None
    as_json: bool


@dataclass
class SplitPaths:
    train_out: Path
    val_out: Path


def parse_args(argv: list[str]) -> Args:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to the .jsonl or .parquet dataset")
    parser.add_argument("--model", help="Base model id, for model-specific checks")
    parser.add_argument(
        "--context-length",
        type=int,
        default=DEFAULT_CONTEXT_TOKENS,
        help="Context window used for length checks when the model is unknown",
    )
    parser.add_argument("--holdout", type=float, help="Validation fraction, e.g. 0.1")
    parser.add_argument("--train-out", type=Path, help="Split output: training rows")
    parser.add_argument("--val-out", type=Path, help="Split output: validation rows")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    ns = parser.parse_args(argv)
    args = Args(
        path=ns.path,
        model=ns.model,
        context_length=ns.context_length,
        holdout=ns.holdout,
        train_out=ns.train_out,
        val_out=ns.val_out,
        as_json=ns.json,
    )
    require_valid_split_args(args)
    return args


def require_valid_split_args(args: Args) -> None:
    split_requested = args.holdout is not None
    split_complete = args.train_out is not None and args.val_out is not None
    if split_requested and not split_complete:
        sys.exit("--holdout requires both --train-out and --val-out")
    if not split_requested and (args.train_out or args.val_out):
        sys.exit("--train-out/--val-out require --holdout")
    if args.holdout is not None and not 0.0 < args.holdout < 1.0:
        sys.exit("--holdout must be between 0 and 1 (exclusive)")


def model_context(model: str) -> int | None:
    lowered = model.lower()
    for fragment, window in MODEL_CONTEXT_TOKENS.items():
        if fragment in lowered:
            return window
    return None


def context_window(args: Args) -> int:
    if args.model:
        known = model_context(args.model)
        if known is not None:
            return known
    return args.context_length


def estimate_tokens(text: str) -> int:
    return int(len(text) / CHARS_PER_TOKEN) + 1


def row_tokens(row: dict) -> int:
    total = 0
    for message in row.get("messages", []):
        total += estimate_tokens(message.get("content") or "")
        thinking = message.get("thinking") or ""
        total += estimate_tokens(thinking) if isinstance(thinking, str) else 0
    return total


def load_rows(path: Path) -> tuple[list[tuple[int, dict]], list[Issue]]:
    """Return (line_number, row) pairs preserving original line numbers."""
    issues: list[Issue] = []
    if path.suffix.lower() not in {".jsonl", ".parquet"}:
        issues.append(Issue("error", None, f"unsupported extension {path.suffix!r}: use .jsonl or .parquet"))
        return [], issues
    size = os.path.getsize(path)
    if size > MAX_FILE_BYTES:
        issues.append(Issue("error", None, f"file is {size / 1e9:.2f} GB; the limit is 3 GB"))
    elif size > SIZE_WARN_BYTES:
        issues.append(Issue("warning", None, f"file is {size / 1e9:.2f} GB, close to the 3 GB limit"))
    if path.suffix.lower() == ".parquet":
        return load_parquet_rows(path, issues)
    return load_jsonl_rows(path, issues)


def load_jsonl_rows(path: Path, issues: list[Issue]) -> tuple[list[tuple[int, dict]], list[Issue]]:
    parsed: list[tuple[int, dict]] = []
    with path.open() as handle:
        for row_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append(Issue("error", row_number, f"invalid JSON: {exc}"))
                continue
            if not isinstance(row, dict):
                issues.append(Issue("error", row_number, "row is not a JSON object"))
                continue
            parsed.append((row_number, row))
    if not parsed and not any(i.severity == "error" for i in issues):
        issues.append(Issue("error", None, "file contains no rows"))
    return parsed, issues


def load_parquet_rows(path: Path, issues: list[Issue]) -> tuple[list[tuple[int, dict]], list[Issue]]:
    try:
        import pandas as pd
    except ImportError:
        issues.append(Issue("error", None, "parquet input requires pandas (pip install pandas pyarrow)"))
        return [], issues
    frame = pd.read_parquet(path)
    if "messages" not in frame.columns:
        issues.append(Issue("error", None, 'parquet file has no "messages" column'))
        return [], issues
    return list(enumerate(frame.to_dict("records"), start=1)), issues


def check_tool_calls(message: dict, row_number: int, issues: list[Issue]) -> None:
    tool_calls = message.get("tool_calls")
    if tool_calls is None:
        return
    if not isinstance(tool_calls, list) or not tool_calls:
        issues.append(Issue("error", row_number, "tool_calls must be a non-empty list"))
        return
    for call in tool_calls:
        function = call.get("function") if isinstance(call, dict) else None
        if not isinstance(function, dict) or not isinstance(function.get("name"), str):
            issues.append(Issue("error", row_number, "tool call is missing function.name"))
            continue
        arguments = function.get("arguments")
        if not isinstance(arguments, str):
            issues.append(
                Issue("error", row_number, 'tool call "arguments" must be a JSON-encoded string, not an object')
            )


def check_row(row: dict, row_number: int, context: int) -> list[Issue]:
    issues: list[Issue] = []
    messages = row.get("messages")
    if not isinstance(messages, list) or not messages:
        issues.append(Issue("error", row_number, 'row has no non-empty "messages" array'))
        return issues
    has_assistant = False
    for message in messages:
        if not isinstance(message, dict):
            issues.append(Issue("error", row_number, "message is not an object"))
            continue
        role = message.get("role")
        if role not in VALID_ROLES:
            issues.append(Issue("error", row_number, f"unknown role {role!r}"))
            continue
        content = message.get("content")
        if content is not None and not isinstance(content, str):
            issues.append(Issue("error", row_number, f"{role} content must be a string (multimodal rows unsupported)"))
        check_tool_calls(message, row_number, issues)
        if role == "assistant":
            has_assistant = True
            tool_calls = message.get("tool_calls")
            if not content and not tool_calls:
                issues.append(Issue("error", row_number, "assistant turn is empty (no content, no tool calls)"))
        if role == "tool" and not content:
            issues.append(Issue("error", row_number, "tool turn has no result content"))
    if not has_assistant:
        issues.append(Issue("error", row_number, "row has no assistant turn; loss would be computed on nothing"))
    tokens = row_tokens(row)
    if tokens > context:
        issues.append(
            Issue(
                "error",
                row_number,
                f"row is ~{tokens} tokens, over the {context}-token context window "
                "(trim it, or set overlong_row_behavior=drop)",
            )
        )
    return issues


def model_fit_issues(rows: list[dict], model: str) -> list[Issue]:
    issues: list[Issue] = []
    name = model.lower()
    gpt_oss_missing_thinking = 0
    llama_mixed_turn = 0
    gemma_mixed_turn = 0
    for row in rows:
        for message in row.get("messages", []):
            if message.get("role") != "assistant":
                continue
            has_content = bool(message.get("content"))
            has_tools = bool(message.get("tool_calls"))
            if "gpt-oss" in name and has_content and "thinking" not in message:
                gpt_oss_missing_thinking += 1
            if has_content and has_tools:
                if "llama-3" in name:
                    llama_mixed_turn += 1
                if "gemma" in name:
                    gemma_mixed_turn += 1
    if gpt_oss_missing_thinking:
        issues.append(
            Issue(
                "warning",
                None,
                f"gpt-oss: {gpt_oss_missing_thinking} assistant turn(s) lack a 'thinking' field; "
                'add "thinking": "" so the model keeps its analysis-before-final format',
            )
        )
    if llama_mixed_turn:
        issues.append(
            Issue(
                "warning",
                None,
                f"llama-3-instruct: {llama_mixed_turn} assistant turn(s) mix content and tool_calls; "
                "the template drops the content, so train them as separate turns",
            )
        )
    if gemma_mixed_turn:
        issues.append(
            Issue(
                "warning",
                None,
                f"gemma-4: {gemma_mixed_turn} assistant turn(s) mix content and tool_calls; "
                "content renders before the tool call, so move post-tool content into its own turn",
            )
        )
    return issues


def summarize(rows: list[dict], context: int) -> dict:
    role_counts: dict[str, int] = {}
    system_prompts: set[str] = set()
    seen_rows: set[str] = set()
    duplicate_rows = 0
    tool_call_rows = 0
    max_row_tokens = 0
    total_row_tokens = 0
    for row in rows:
        canonical = json.dumps(row, sort_keys=True)
        if canonical in seen_rows:
            duplicate_rows += 1
        seen_rows.add(canonical)
        row_token_total = 0
        for message in row.get("messages", []):
            if not isinstance(message, dict):
                continue
            role_counts[message.get("role", "?")] = role_counts.get(message.get("role", "?"), 0) + 1
            content = message.get("content") or ""
            row_token_total += estimate_tokens(content)
            if message.get("role") == "system":
                system_prompts.add(content)
            if message.get("role") == "assistant" and message.get("tool_calls"):
                tool_call_rows += 1
        max_row_tokens = max(max_row_tokens, row_token_total)
        total_row_tokens += row_token_total
    over_context = sum(1 for row in rows if row_tokens(row) > context)
    return {
        "rows": len(rows),
        "role_turn_counts": role_counts,
        "distinct_system_prompts": len(system_prompts),
        "rows_with_tool_calls": tool_call_rows,
        "duplicate_rows": duplicate_rows,
        "estimated_max_row_tokens": max_row_tokens,
        "estimated_total_tokens": total_row_tokens,
        "rows_over_context": over_context,
    }


def split_holdout(rows: list[dict], holdout: float, paths: SplitPaths) -> tuple[int, int]:
    shuffled = list(rows)
    random.Random(SPLIT_SEED).shuffle(shuffled)
    validation_count = max(1, round(len(shuffled) * holdout))
    validation, training = shuffled[:validation_count], shuffled[validation_count:]
    for destination, subset in ((paths.val_out, validation), (paths.train_out, training)):
        with destination.open("w") as handle:
            for row in subset:
                handle.write(json.dumps(row) + "\n")
    return len(training), len(validation)


def render_report(issues: list[Issue], stats: dict, args: Args) -> str:
    lines = [f"Dataset: {args.path}", f"Rows parsed: {stats['rows']}"]
    lines.append(f"Role turns: {stats['role_turn_counts']}")
    lines.append(f"Distinct system prompts: {stats['distinct_system_prompts']}")
    lines.append(f"Rows with tool calls: {stats['rows_with_tool_calls']}")
    lines.append(f"Exact duplicate rows: {stats['duplicate_rows']}")
    lines.append(f"Estimated max row tokens: {stats['estimated_max_row_tokens']}")
    lines.append(f"Estimated total tokens: {stats['estimated_total_tokens']}")
    lines.append(f"Rows over context window: {stats['rows_over_context']}")
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    lines.append(f"\nErrors: {len(errors)} | Warnings: {len(warnings)}")
    file_level = [i for i in issues if i.row is None]
    row_level = sorted((i for i in issues if i.row is not None), key=lambda i: i.row)
    for issue in file_level + row_level:
        location = f"row {issue.row}" if issue.row is not None else "file"
        lines.append(f"  [{issue.severity.upper()}] {location}: {issue.message}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    parsed, issues = load_rows(args.path)
    rows = [row for _, row in parsed]
    context = context_window(args)
    if args.model and model_context(args.model) is None:
        issues.append(
            Issue(
                "warning",
                None,
                f"unknown context window for {args.model}; assuming {context} tokens "
                "(pass --context-length to override)",
            )
        )
    for row_number, row in parsed:
        issues.extend(check_row(row, row_number, context))
    if args.model:
        issues.extend(model_fit_issues(rows, args.model))
    stats = summarize(rows, context)
    split_summary = None
    if args.holdout is not None and args.train_out and args.val_out:
        training_count, validation_count = split_holdout(rows, args.holdout, SplitPaths(args.train_out, args.val_out))
        split_summary = f"split: {training_count} train -> {args.train_out}, {validation_count} val -> {args.val_out}"
    if args.as_json:
        print(
            json.dumps(
                {
                    "errors": [vars(i) for i in issues if i.severity == "error"],
                    "warnings": [vars(i) for i in issues if i.severity == "warning"],
                    "stats": stats,
                    "split": split_summary,
                },
                indent=2,
            )
        )
    else:
        print(render_report(issues, stats, args))
        if split_summary:
            print(split_summary)
    return 1 if any(i.severity == "error" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
