#!/usr/bin/env python3
"""Search the web with EmpirioLabs AI: results, an answer with sources, or a research report.

Examples:
  python3 search.py "latest stable release of Python"
  python3 search.py "who maintains the Model Context Protocol" --answer
  python3 search.py "state of solid-state batteries in 2026" --research --out ./battery-report.md
  python3 search.py "rust async runtimes compared" --model MODEL_ID --param num_results=5
  python3 search.py "open source vector databases" --json
  python3 search.py --list-models            # add --answer or --research for those models

Prints the results as text (or JSON with --json) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

SEARCH = "POST /v1/search"
ANSWER = "POST /v1/answer"
RESEARCH = "POST /v1/research"
PATHS = {SEARCH: "/search", ANSWER: "/answer", RESEARCH: "/research"}
# A research report can take several minutes; the request stays open until it is ready.
TIMEOUTS = {SEARCH: 120.0, ANSWER: 180.0, RESEARCH: 900.0}
SNIPPET_KEYS = ("content", "snippet", "text", "description", "summary")
SNIPPET_LENGTH = 320


def build_parser():
    parser = argparse.ArgumentParser(
        prog="search.py",
        description="Search the web, get an answer with sources, or run a research report with EmpirioLabs AI.",
        epilog=(
            "When --model is omitted, a model from the live catalog is used.\n"
            "Search is billed per request at the model's listed price, and a research report costs\n"
            "more than a search; check --list-models first.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="?", help="What to search for, or the question to answer.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--answer", action="store_true", help="Return one answer with its sources.")
    mode.add_argument("--research", action="store_true",
                      help="Run a research report with citations. This can take several minutes.")
    parser.add_argument("--model", help="Model id. See --list-models.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param num_results=5. Repeatable.")
    parser.add_argument("--out", help="Save the output here (.json saves the full result).")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing --out file.")
    parser.add_argument("--json", action="store_true", help="Print the full result as JSON.")
    parser.add_argument("--list-models", action="store_true",
                        help="List the models of the chosen mode with prices, then exit.")
    return parser


def endpoint_of(args):
    if args.answer:
        return ANSWER
    if args.research:
        return RESEARCH
    return SEARCH


def search_models(models):
    """Models that only search, in catalog order: the ones a plain search should default to."""
    return [m for m in api.candidates(models, SEARCH) if (m.get("supported_endpoints") or []) == [SEARCH]]


def resolve(args, endpoint):
    if args.model or endpoint != SEARCH:
        return api.resolve_model(args.model, endpoint)
    models = api.list_models()
    pool = search_models(models)
    if pool:
        return pool[0]["id"], pool[0]
    entry = api.pick_default(models, SEARCH)
    return entry["id"], entry


def list_models(endpoint):
    models = api.list_models()
    if endpoint != SEARCH:
        api.print_model_list(models, endpoint)
        return
    pool = api.candidates(models, SEARCH)
    only_search = search_models(models)
    default = (only_search or pool or [{}])[0].get("id")
    for model in pool:
        mark = "*" if model["id"] == default else " "
        print(mark + " " + model["id"].ljust(32) + " " + api.price_summary(model))
    api.log(str(len(pool)) + " models support " + SEARCH + ". * marks the default when --model is omitted.")


def answer_text(result):
    for key in ("answer", "report", "output", "content"):
        value = result.get(key) if isinstance(result, dict) else None
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def sources_of(result):
    rows = result.get("results") if isinstance(result, dict) else None
    out = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        url = row.get("url") or row.get("link")
        if not isinstance(url, str) or not url:
            continue
        snippet = ""
        for key in SNIPPET_KEYS:
            if isinstance(row.get(key), str) and row[key].strip():
                snippet = " ".join(row[key].split())
                break
        out.append({"title": str(row.get("title") or "").strip() or url, "url": url, "snippet": snippet})
    return out


def render(result, endpoint):
    """Plain text for an agent to read: the answer first, then the numbered sources."""
    lines = []
    text = answer_text(result)
    if text:
        lines.append(text)
        lines.append("")
    sources = sources_of(result)
    if sources and text:
        lines.append("Sources:")
    for index, row in enumerate(sources, 1):
        lines.append(str(index) + ". " + row["title"])
        lines.append("   " + row["url"])
        if row["snippet"] and endpoint == SEARCH:
            snippet = row["snippet"]
            if len(snippet) > SNIPPET_LENGTH:
                snippet = snippet[:SNIPPET_LENGTH].rstrip() + "..."
            lines.append("   " + snippet)
    if not lines:
        return None
    return "\n".join(lines).rstrip()


def finish(args, result, endpoint, model_id):
    text = None if args.json else render(result, endpoint)
    if text is None and not args.json:
        api.log("No readable results in the response; printing the full result.")
    if args.out:
        out = os.path.expanduser(args.out)
        if api.is_dir_target(out):
            path = api.target_path(out, api.default_stem("search"), ".json" if text is None else ".md", 1, 1,
                                   args.overwrite)
        else:
            path = os.path.abspath(out)
            if not args.overwrite:
                path = api.free_path(path)
        if path.lower().endswith(".json") or text is None:
            content = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            content = text
        api.write_bytes(path, (content.rstrip("\n") + "\n").encode("utf-8"))
        api.log("Saved " + path)
        api.print_json({"model": model_id, "file": path, "sources": len(sources_of(result)),
                        "characters": len(answer_text(result) or "")})
    elif text is None:
        api.print_json(result)
    else:
        print(text, flush=True)
    return api.EXIT_OK


def run(args, parser):
    endpoint = endpoint_of(args)
    if args.list_models:
        list_models(endpoint)
        return api.EXIT_OK
    if not args.query:
        parser.error("a query is required (or pass --list-models)")
    api.api_key()
    model_id, _entry = resolve(args, endpoint)
    body = {"model": model_id, "query": args.query}
    if endpoint == RESEARCH:
        body["stream"] = False
        api.log("Researching with " + model_id + ". This can take several minutes ...")
    else:
        api.log(("Answering" if endpoint == ANSWER else "Searching") + " with " + model_id + " ...")
    body.update(api.parse_params(args.param))
    result = api.post_json(PATHS[endpoint], body, timeout=TIMEOUTS[endpoint]).json()
    job_id = api.job_id_of(result)
    if job_id:
        job = api.wait_for_job(job_id, timeout=TIMEOUTS[RESEARCH], label="Search job")
        result = job.get("result") if isinstance(job.get("result"), dict) else job
    return finish(args, result, endpoint, model_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.ApiError as exc:
        return api.fail(exc)
    except OSError as exc:
        return api.fail(api.ApiError("Could not read or write a file: " + str(exc)))
    except KeyboardInterrupt:
        api.log("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
