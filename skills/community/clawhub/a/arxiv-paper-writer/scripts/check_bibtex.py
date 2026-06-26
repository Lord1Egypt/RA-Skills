import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,]+),", re.MULTILINE)
REQUIRED_FIELDS = ["title", "author", "year"]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python check_bibtex.py <references.bib>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"BibTeX file not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    entries = ENTRY_RE.findall(text)
    if not entries:
        print("No BibTeX entries found")
        return 1

    duplicate_keys = sorted({key for key in entries if entries.count(key) > 1})
    if duplicate_keys:
        print("Duplicate BibTeX keys:")
        for key in duplicate_keys:
            print(f"- {key}")
        return 1

    lower_text = text.lower()
    missing_fields = [field for field in REQUIRED_FIELDS if f"{field}={{" not in lower_text and f"{field} = {{" not in lower_text]
    if missing_fields:
        print(f"Missing common required fields somewhere in file: {missing_fields}")
        return 1

    print(f"BibTeX sanity check ok: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
