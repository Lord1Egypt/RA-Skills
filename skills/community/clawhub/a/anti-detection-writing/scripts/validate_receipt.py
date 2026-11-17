#!/usr/bin/env python3
"""Check a local GPTZero Basic receipt; never authenticate or authorize it."""

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_artifact(root, item):
    """Read only a named artifact inside the receipt's directory."""
    require(isinstance(item, dict), "Artifact must be an object")
    name = item.get("path")
    require(isinstance(name, str) and bool(name), "Missing artifact path")
    relative = Path(name)
    require(not relative.is_absolute() and ".." not in relative.parts,
            "Artifact paths must be relative and cannot traverse parents")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "Artifact escapes receipt directory")
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == item.get("sha256"),
            f"Artifact hash mismatch: {name}")
    return data


def normalize_line_endings(data):
    """Preserve spaces, punctuation, code, and the number of line breaks."""
    return data.decode("utf-8").replace("\r\n", "\n")


def finite_percent(value):
    return (type(value) in (int, float) and math.isfinite(value)
            and 0 <= value <= 100)


def validate(answer, receipt_path, max_ai_exclusive=None):
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(isinstance(receipt, dict), "Receipt must be an object")
    require(receipt.get("schema_version") == 1, "Unsupported receipt schema")
    require(receipt.get("service") == "GPTZero", "Unsupported service")
    require(receipt.get("mode") == "Basic Scan", "Expected Basic Scan")
    require(receipt.get("status") == "complete", "Scan is not complete")
    require(receipt.get("text_up_to_date") is True, "Scan is not current")
    require(receipt.get("entry_mode") == "verbatim", "Only verbatim entry is supported")
    model = receipt.get("model")
    require(isinstance(model, str) and re.fullmatch(r"[A-Za-z0-9._-]+", model),
            "Missing or invalid model")
    observed = datetime.fromisoformat(receipt["observed_at"].replace("Z", "+00:00"))
    require(observed.utcoffset() is not None, "Observation time needs a timezone")

    scores = [receipt.get(f"{label}_percent") for label in ("ai", "mixed", "human")]
    require(all(finite_percent(score) for score in scores), "Invalid confidence values")
    require(abs(sum(scores) - 100) <= 1, "Confidence values must sum to approximately 100")
    require(type(receipt.get("short_text_warning")) is bool, "Record the short-text warning")

    root = receipt_path.parent
    original = read_artifact(root, receipt["answer"])
    submitted = read_artifact(root, receipt["submitted"])
    editor = read_artifact(root, receipt["editor"])
    ui = read_artifact(root, receipt["visible_result"]).decode("utf-8")
    require(answer.read_bytes() == original, "Final answer differs from the recorded answer")
    require(original.strip(), "Answer cannot be empty")
    require(normalize_line_endings(original) == normalize_line_endings(submitted),
            "Submitted text differs from the final answer")
    require(normalize_line_endings(submitted) == normalize_line_endings(editor),
            "Editor text differs from submitted text")

    # Match result controls in a saved accessibility snapshot, not answer prose.
    require(re.search(r'^\s*- heading "Basic Scan" \[level=1\]\s*$', ui, re.M),
            "Visible Basic Scan result heading is missing")
    require(re.search(r'^\s*- generic: Text up-to-date\s*$', ui, re.M),
            "Visible fresh-result indicator is missing")
    require(not re.search(r'^\s*- (?:generic|button|paragraph|text).*'
                          r'(?:Text changed|Scan to update)', ui, re.M),
            "Visible result is stale")
    models = re.findall(r'^\s*- generic: Model (\S+)\s*$', ui, re.M)
    require(models == [model], "Visible model does not match the receipt uniquely")
    for label, score in zip(("AI", "Mixed", "Human"), scores):
        found = re.findall(r'^\s*- button "' + label + r' (\d+(?:\.\d+)?)%":?\s*$',
                           ui, re.M)
        require(len(found) == 1 and float(found[0]) == score,
                f"Visible {label} confidence does not match uniquely")
    warning = bool(re.search(r'^\s*- paragraph: This text is under 100 words\s*$', ui, re.M))
    require(warning == receipt["short_text_warning"], "Short-text warning mismatch")
    if max_ai_exclusive is not None:
        require(finite_percent(max_ai_exclusive) and max_ai_exclusive > 0,
                "Threshold must be greater than zero and at most 100")
        require(scores[0] < max_ai_exclusive, "Recorded AI confidence fails requested threshold")
    return {"result": "consistent_local_receipt", "ai_percent": scores[0],
            "threshold_checked": max_ai_exclusive,
            "limit": "Does not authenticate the detector, assess quality, or authorize posting."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("answer", type=Path)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--max-ai-exclusive", type=float,
                        help="Optional user-requested condition, for example 100")
    args = parser.parse_args()
    try:
        result = validate(args.answer, args.receipt, args.max_ai_exclusive)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        parser.exit(1, f"Receipt rejected: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
