#!/usr/bin/env python3
"""Assert that every document states the same Skill slug, display name, and version.

Before this check existed the bundle carried four disagreeing identities: the
SKILL.md frontmatter slug, the marketing display name, the archive filename, and
the engine version. Installation, discovery, and version conversation all depend
on those agreeing, so they are now derived from two files:

  * `VERSION`                 - the engine version, one line;
  * `packaging/identity.json` - slug, display name, aliases, owner, licence, and
                                which document asserts which field.

Run `python3 scripts/check_identity.py` (exit 0 = consistent). The bundled
release-identity tests call the same functions, so a drifting document fails
the suite rather than shipping.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_FILE = ROOT / "packaging" / "identity.json"
VERSION_FILE = ROOT / "VERSION"


def load_identity(root: Path = ROOT) -> dict[str, Any]:
    """Return the identity document with `version` resolved from VERSION."""
    identity = json.loads((root / "packaging" / "identity.json").read_text(encoding="utf-8"))
    identity["version"] = (root / "VERSION").read_text(encoding="utf-8").strip()
    return identity


def expected_values(identity: dict[str, Any], field: str) -> list[str]:
    """Return the literal strings a document must contain for one asserted field."""
    if field == "brand_aliases":
        return list(identity.get("brand_aliases", []))
    value = identity.get(field)
    return [str(value)] if value else []


def check(root: Path = ROOT) -> list[str]:
    """Return a list of human-readable problems; empty means consistent."""
    problems: list[str] = []
    identity = load_identity(root)
    version = identity["version"]

    for consumer in identity.get("consumers", []) or []:
        relative = consumer.get("path")
        if not relative:
            continue
        path = root / relative
        if not path.exists():
            problems.append(f"{relative}: declared in packaging/identity.json but missing from the bundle")
            continue
        text = path.read_text(encoding="utf-8")
        for field in consumer.get("asserts", []) or []:
            for expected in expected_values(identity, field):
                if expected not in text:
                    problems.append(f"{relative}: missing {field} value {expected!r}")

    # A stale version left behind by an incomplete bump is the failure mode this
    # check exists for, so scan the same documents for any other x.y.z that looks
    # like an engine version claim.
    for consumer in identity.get("consumers", []) or []:
        relative = consumer.get("path")
        if not relative or "version" not in (consumer.get("asserts") or []):
            continue
        path = root / relative
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            lowered = line.lower()
            if "version" not in lowered and "当前版本" not in line:
                continue
            for token in ("2.0.", "1.5.", "1.2."):
                if token in line and version not in line and _looks_like_current_claim(line):
                    problems.append(f"{relative}:{line_number}: version claim does not use {version}: {line.strip()[:110]}")
                    break

    return problems


def _looks_like_current_claim(line: str) -> bool:
    """Distinguish a current-version claim from a historical changelog entry.

    Release-note headings and migration references legitimately name older
    versions; a sentence that says "current version" or sits in frontmatter does not.
    """
    lowered = line.lower()
    historical_markers = ("preserve", "preserves", "remain", "remains", "unchanged", "migration", "changelog", "→", "->", "previous")
    if any(marker in lowered for marker in historical_markers):
        return False
    if lowered.lstrip().startswith("#"):
        return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Assert that every document states the same Skill slug, display name, and version.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)

    identity = load_identity(args.root)
    problems = check(args.root)

    print(f"slug={identity['registry_slug']} display_name={identity['display_name']!r} version={identity['version']}")
    print(f"archive={identity['archive_name_template'].format(version=identity['version'])}")
    if problems:
        for problem in problems:
            print(f"  IDENTITY_DRIFT {problem}", file=sys.stderr)
        print(f"identity check failed: {len(problems)} problem(s)")
        return 1
    print("identity check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
