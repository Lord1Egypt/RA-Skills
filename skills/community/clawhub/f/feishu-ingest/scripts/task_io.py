import argparse
import json
import sys
from pathlib import Path


def read_payload(path=None):
    if path:
        raw = Path(path).read_bytes()
    else:
        raw = sys.stdin.buffer.read()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def envelope(result=None):
    base = {
        "success": True,
        "processedSources": [],
        "createdPages": [],
        "updatedPages": [],
        "archivedFiles": [],
        "skippedSources": [],
        "errors": [],
        "commitId": "",
    }
    base.update(result or {})
    return base


def write_result(path, result):
    data = envelope(result)
    if path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def print_json(data):
    text = json.dumps(data or {}, ensure_ascii=False, indent=2) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))


# Backward-compatible entry for the old single-shot fallback runner.
def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--task-json", dest="task_json")
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()
    return read_payload(args.input or args.task_json)


def emit(result):
    print_json(envelope(result))


def run(handler):
    try:
        emit(handler(read_input()))
    except Exception as exc:
        emit({"success": False, "errors": [str(exc)], "commitId": ""})