"""Check a retrieved guide for the versioned production contract, without I/O to hosts."""

import json
from pathlib import Path
import re
import sys

CONTRACT = "dcc-mcp-production-reuse/v1"


def has_contract(text):
    """Accept source Markdown or the gateway's decoded resource payload."""
    try:
        payload = json.loads(text)
    except ValueError:
        document = text
    else:
        if not isinstance(payload, dict) or payload.get("production_reuse_contract") != CONTRACT:
            return False
        document = payload.get("document", "")
    if not isinstance(document, str):
        return False
    match = re.search(r"^## Production reuse gate\s*\n(.*?)(?=^## |\Z)", document, re.M | re.S)
    if not match:
        return False
    section = match.group(1)
    marker = "**Contract:** `" + CONTRACT + "`"
    # A marker-only placeholder is not the contract's substantive instructions.
    return marker in section and bool(section.replace(marker, "").strip())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: check_production_guide.py <retrieved-guide-file>", file=sys.stderr)
        return 2
    try:
        accepted = has_contract(Path(argv[0]).read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError):
        accepted = False
    print(json.dumps({"contract": CONTRACT, "guide_available": accepted,
                      "next_step": "read_and_execute_gate" if accepted else "try_core_source_or_report_rollout_dependency"}))
    return 0 if accepted else 2


if __name__ == "__main__":
    sys.exit(main())
