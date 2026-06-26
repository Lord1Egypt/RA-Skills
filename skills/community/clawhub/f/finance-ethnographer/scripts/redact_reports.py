#!/usr/bin/env python3
"""
redact_reports.py
PII Redactor – strips personally identifiable information from report files.

Usage:
    python3 redact_reports.py <file.md>          # redact single file
    python3 redact_reports.py <directory/>       # redact all *.md in dir
    python3 redact_reports.py --validate-only    # scan REDACTED files for residual PII
    python3 redact_reports.py --validate-only --verbose

Outputs: for each input.md → input.REDACTED.md
Placeholders are consistent within a file: [EMAIL_1] always refers to the same original value.
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── PII patterns (order matters — specific before catch-all) ───────────────────
RAW_PATTERNS: List[Tuple[str, str, str]] = [
    # SSN / Individual Tax ID
    ("SSN",      r"\b\d{3}[-\u2013]\d{2}[-\u2013]\d{4}\b",                      "TAX_ID"),
    # EIN  XX-XXXXXXX
    ("EIN",      r"\b\d{2}[-\u2013]\d{7}\b",                                     "EIN"),
    # Credit / debit card  (4×4 blocks)
    ("CC",       r"\b(?:\d{4}[\s\-]){3}\d{4}\b",                                 "CC"),
    # Routing number in context
    ("ROUTING",  r"(?i)\b(?:routing(?:\s+number)?|aba)[:\s#]*(\d{9})\b",         "ROUTING"),
    # Bank account in context
    ("ACCOUNT",  r"(?i)\b(?:acct|account|acc(?:ount)?)[:\s#\.]*([\d\-]{6,20})\b","ACCOUNT"),
    # Long standalone digit strings (≥10 digits)
    ("LONG_NUM", r"\b\d{10,}\b",                                                  "ACCOUNT"),
    # US phone numbers
    ("PHONE",    r"(?:\+?1[\s.\-]?)?\(?[2-9]\d{2}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}","PHONE"),
    # Email
    ("EMAIL",    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",       "EMAIL"),
    # Bearer / OAuth tokens
    ("BEARER",   r"(?i)Bearer\s+[A-Za-z0-9._\-/+]{20,}",                         "TOKEN"),
    # Generic API keys (≥32 chars, no spaces)
    ("API_KEY",  r"\b[A-Za-z0-9_\-]{32,}\b",                                     "TOKEN"),
    # Street addresses
    ("ADDRESS",
     r"\b\d{1,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4}"
     r"(?:\s+(?:St|Ave|Rd|Blvd|Dr|Ln|Ct|Way|Pl|Pkwy|Hwy|Cir|Ter|Sq)\.?\b)",    "ADDRESS"),
    # Name introductions
    ("NAME_IS",
     r"(?i)(?:my name is|i am|i['\u2019]m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",
     "PERSON"),
    # US ZIP codes (only when near a state abbreviation or comma)
    ("ZIP",      r"(?i)\b(?:[A-Z]{2}\s+|,\s*)\d{5}(?:-\d{4})?\b",               "ZIP"),
]

# Used for validation scans of REDACTED files
VALIDATION_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("email",       re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("phone",       re.compile(r"(?:\+?1[\s.\-]?)?\(?[2-9]\d{2}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}")),
    ("ssn",         re.compile(r"\b\d{3}[-\u2013]\d{2}[-\u2013]\d{4}\b")),
    ("credit_card", re.compile(r"\b(?:\d{4}[\s\-]){3}\d{4}\b")),
    ("bearer",      re.compile(r"(?i)Bearer\s+[A-Za-z0-9._\-/+]{20,}")),
]


class Redactor:
    """
    Stateful PII redactor. Counters and seen-values reset between files so
    [EMAIL_1] consistently refers to the same original within one document.
    """

    def __init__(self) -> None:
        self._counters: Dict[str, int] = {}
        self._seen:     Dict[str, str] = {}
        self._compiled = [
            (label, re.compile(pattern, re.MULTILINE), prefix)
            for label, pattern, prefix in RAW_PATTERNS
        ]

    def reset(self) -> None:
        self._counters.clear()
        self._seen.clear()

    def _placeholder(self, prefix: str, original: str) -> str:
        key = f"{prefix}:{original.strip()}"
        if key not in self._seen:
            n = self._counters.get(prefix, 0) + 1
            self._counters[prefix] = n
            self._seen[key] = f"[{prefix}_{n}]"
        return self._seen[key]

    def redact(self, text: str) -> str:
        for _label, pattern, prefix in self._compiled:
            def _sub(m: re.Match, p: str = prefix) -> str:
                return self._placeholder(p, m.group(0))
            text = pattern.sub(_sub, text)
        return text

    def redact_file(self, input_path: Path) -> Tuple[Path, str]:
        self.reset()
        raw      = input_path.read_text(encoding="utf-8", errors="replace")
        redacted = self.redact(raw)
        ts       = datetime.now(tz=timezone.utc).isoformat()
        header   = (
            f"<!-- REDACTED VERSION — Generated {ts} -->\n"
            f"<!-- Source: {input_path.name} -->\n"
            f"<!-- PII substitutions: {len(self._seen)} -->\n\n"
        )
        content = header + redacted
        stem    = input_path.stem
        out     = (
            input_path
            if stem.endswith(".REDACTED")
            else input_path.with_name(stem + ".REDACTED" + input_path.suffix)
        )
        return out, content

    @property
    def substitution_count(self) -> int:
        return len(self._seen)


# ── Validation ─────────────────────────────────────────────────────────────────

def validate_file(path: Path, verbose: bool = False) -> List[str]:
    issues: List[str] = []
    if not path.exists():
        issues.append(f"MISSING: {path}")
        return issues
    content = path.read_text(encoding="utf-8", errors="replace")
    for name, pattern in VALIDATION_PATTERNS:
        matches = pattern.findall(content)
        if matches:
            issues.append(f"POSSIBLE_PII ({name}): {len(matches)} instance(s) in {path.name}")
            if verbose:
                for m in matches[:3]:
                    issues.append(f"    → {m!r}")
    return issues


def validate_reports_dir(reports_base: Path, verbose: bool = False) -> bool:
    """Scan all date subdirectories under reports_base. Returns True if clean."""
    if not reports_base.exists():
        print("No reports directory found — nothing to validate.")
        return True

    all_clean = True
    for date_dir in sorted(reports_base.iterdir()):
        if not date_dir.is_dir():
            continue
        md_files      = sorted(date_dir.glob("*.md"))
        source_files  = [f for f in md_files if ".REDACTED." not in f.name]
        redacted_files = [f for f in md_files if ".REDACTED." in f.name]

        # Check every source file has a REDACTED counterpart
        for f in source_files:
            expected = f.with_name(f.stem + ".REDACTED" + f.suffix)
            if not expected.exists():
                print(f"  ❌ MISSING_REDACTED: {date_dir.name}/{expected.name}")
                all_clean = False

        # Scan REDACTED files for residual PII
        for f in redacted_files:
            issues = validate_file(f, verbose=verbose)
            if issues:
                all_clean = False
                print(f"  ⚠️  {date_dir.name}/{f.name}")
                for issue in issues:
                    print(f"     • {issue}")

    return all_clean


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Finance UX Observer — PII Redactor")
    parser.add_argument("target", nargs="?", help="File or directory to redact")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        reports_base = Path(__file__).resolve().parent.parent / "reports"
        clean = validate_reports_dir(reports_base, verbose=args.verbose)
        if clean:
            print("✅ Redaction validation passed — no residual PII detected.")
            sys.exit(0)
        else:
            sys.exit(1)

    if not args.target:
        parser.print_help()
        sys.exit(1)

    target   = Path(args.target)
    redactor = Redactor()

    if target.is_file():
        out_path, content = redactor.redact_file(target)
        out_path.write_text(content, encoding="utf-8")
        print(f"✅ {target.name} → {out_path.name} ({redactor.substitution_count} substitution(s))")

    elif target.is_dir():
        sources = sorted(f for f in target.glob("*.md") if ".REDACTED." not in f.name)
        if not sources:
            print(f"No source .md files in {target}")
            sys.exit(0)
        for f in sources:
            redactor = Redactor()
            out_path, content = redactor.redact_file(f)
            out_path.write_text(content, encoding="utf-8")
            print(f"  ✅ {f.name} → {out_path.name} ({redactor.substitution_count} substitution(s))")

    else:
        print(f"Error: '{target}' is not a file or directory.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
