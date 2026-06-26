"""Semantic versioning utilities for /depradar.

Handles: plain SemVer (1.2.3), npm ranges (^1.2.3, ~1.2, >=2),
PyPI specifiers (==1.2.3, >=1.0,<2.0, ~=1.4), Go pseudo-versions, etc.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple


# ── Version representation ───────────────────────────────────────────────────

class Version:
    """Parsed semantic version with major.minor.patch.pre components."""

    def __init__(self, major: int, minor: int = 0, patch: int = 0,
                 pre: str = "") -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre   = pre  # e.g. "alpha.1", "rc.2"

    def __lt__(self, other: "Version") -> bool:
        return self._tuple() < other._tuple()

    def __le__(self, other: "Version") -> bool:
        return self._tuple() <= other._tuple()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._tuple() == other._tuple()

    def __gt__(self, other: "Version") -> bool:
        return self._tuple() > other._tuple()

    def __ge__(self, other: "Version") -> bool:
        return self._tuple() >= other._tuple()

    def __repr__(self) -> str:
        pre = f"-{self.pre}" if self.pre else ""
        return f"{self.major}.{self.minor}.{self.patch}{pre}"

    def _tuple(self) -> Tuple[int, int, int, int]:
        # Per SemVer spec §9: pre-release versions have LOWER precedence than
        # the associated stable release.  Encode as a 4-tuple so that ordering
        # works correctly without custom __lt__/__gt__ logic:
        #   (major, minor, patch, 0)  →  pre-release
        #   (major, minor, patch, 1)  →  stable
        # Example: Version(1,0,0,"alpha") < Version(1,0,0,"") → True ✓
        return (self.major, self.minor, self.patch, 0 if self.pre else 1)


# ── Parsing ──────────────────────────────────────────────────────────────────

_SEMVER_RE = re.compile(
    r"[vV]?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[.\-+]([a-zA-Z0-9._+\-]+))?"
)

# Range prefix characters to strip before parsing the actual version
_RANGE_PREFIXES = re.compile(r"^[\^~>=<!\s]+")


def parse(version_str: str) -> Optional[Version]:
    """Parse a version string into a :class:`Version`.

    Accepts:
    - "1.2.3", "v1.2.3", "V1.2.3"
    - "^1.2.3", "~1.2", ">=2.0.0", "==1.4"
    - "1.2.3-alpha.1", "1.2.3+build.1"
    - Go pseudo: "v1.2.3-20230101120000-abcdef123456"

    Returns ``None`` if unparseable.
    """
    if not version_str:
        return None
    cleaned = _RANGE_PREFIXES.sub("", version_str.strip())
    # For ">=1.0,<2.0" style: take the first specifier
    cleaned = re.split(r"[,\s]", cleaned)[0]
    m = _SEMVER_RE.match(cleaned)
    if not m:
        return None
    major = int(m.group(1))
    minor = int(m.group(2) or 0)
    patch = int(m.group(3) or 0)
    pre   = m.group(4) or ""
    # Trim Go hash suffix from pre
    pre = re.sub(r"-[0-9a-f]{12}$", "", pre)
    return Version(major, minor, patch, pre)


def extract_numeric(version_str: str) -> Optional[str]:
    """Extract the plain X.Y.Z from a range specifier.

    "^4.17.0"  → "4.17.0"
    ">=1.0,<2" → "1.0.0"
    "~=1.4.2"  → "1.4.2"
    "1.2.3"    → "1.2.3"
    """
    v = parse(version_str)
    if v is None:
        return None
    return str(v)


# ── Comparison helpers ────────────────────────────────────────────────────────

def bump_type(current: str, latest: str) -> str:
    """Return "major", "minor", "patch", or "unknown" for the bump from
    *current* to *latest*.

    Pre-release → stable of the same version (e.g. "1.0.0-alpha" → "1.0.0")
    is classified as "patch" (a stabilisation release).
    """
    c = parse(current)
    l = parse(latest)
    if c is None or l is None:
        return "unknown"
    if l <= c:
        return "none"
    if l.major > c.major:
        return "major"
    if l.minor > c.minor:
        return "minor"
    if l.patch > c.patch:
        return "patch"
    # Pre-release → stable of the same numeric version
    if c.pre and not l.pre and (l.major, l.minor, l.patch) == (c.major, c.minor, c.patch):
        return "patch"
    return "none"


def is_breaking(current: str, latest: str) -> bool:
    """Return True if going from *current* to *latest* is a major bump."""
    return bump_type(current, latest) == "major"


def is_newer(candidate: str, baseline: str) -> bool:
    """Return True if *candidate* is strictly newer than *baseline*."""
    c = parse(candidate)
    b = parse(baseline)
    if c is None or b is None:
        return False
    return c > b


def newer_versions(all_versions: list[str], baseline: str) -> list[str]:
    """Return all versions from *all_versions* that are newer than *baseline*,
    sorted newest-first.
    """
    b = parse(baseline)
    if b is None:
        return []
    newer = [(v, parse(v)) for v in all_versions]
    newer = [(vs, vp) for vs, vp in newer if vp is not None and vp > b]
    newer.sort(key=lambda x: x[1], reverse=True)
    return [vs for vs, _ in newer]


def latest_stable(versions: list[str]) -> Optional[str]:
    """Return the highest stable (non-pre-release) version string."""
    parsed = [(v, parse(v)) for v in versions]
    stable = [(vs, vp) for vs, vp in parsed if vp is not None and not vp.pre]
    if not stable:
        return None
    stable.sort(key=lambda x: x[1], reverse=True)
    return stable[0][0]
