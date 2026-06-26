"""Breaking-change extractor from changelog markdown for /depradar."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from schema import BreakingChange
from semver import parse as _parse_semver


# ── Keyword patterns ──────────────────────────────────────────────────────────

# Patterns that strongly indicate a breaking change line
_BREAKING_KEYWORDS_RE = re.compile(
    r"\b(removes?|removed|renamed?|drops?|dropped|deleted?|"
    r"no longer supports?|deprecated and removed|"
    r"breaking changes?|\bbreaking\b|incompatible|"
    r"not backward[- ]compatible|drop support|"
    r"migration required|must (?:now |be )?(?:use|update|upgrade)|"
    r"previously.*?now|signature changed?|return(?:s)? type changed?|"
    r"replaced? by|replaced? with|use .+ instead|"
    r"no longer available|has been removed)\b",
    re.IGNORECASE,
)

# Subset of keywords that are unambiguous even without a code symbol.
# Used by the relaxed Pass 3 gate to accept plain-English breaking lines.
_STRONG_PLAIN_BREAKING_RE = re.compile(
    r"\b(not backward[- ]compatible|drop support|breaking change|"
    r"migration required|incompatible change|removed and replaced|"
    r"no longer supported|will no longer work|"
    r"has been removed|is no longer available)\b",
    re.IGNORECASE,
)

# Section headers that indicate a breaking changes block
_BREAKING_SECTION_RE = re.compile(
    r"^#{1,4}\s*(?:breaking\s*changes?|⚠.*?breaking|migration|"
    r"incompatible\s*changes?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Conventional commit BREAKING CHANGE footer
_CC_FOOTER_RE = re.compile(
    r"BREAKING[- ]CHANGE\s*[:\!]?\s*(.+?)(?=\n\n|\Z)",
    re.DOTALL,
)

# feat!: or fix!: syntax
_CC_BANG_RE = re.compile(
    r"^(?:feat|fix|refactor|chore|perf|build|ci|docs|style|test)!:\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)

# Version section header patterns
_VERSION_HEADER_RE = re.compile(
    r"^#{1,3}\s*\[?v?(\d+\.\d+(?:\.\d+)?(?:[.\-][a-zA-Z0-9]+)*)\]?\s*"
    r"(?:[-–]\s*\d{4}-\d{2}-\d{2})?",
    re.MULTILINE,
)

# Bullet point pattern
_BULLET_RE = re.compile(r"^[\s]*[-\*\+]\s+(.+)$", re.MULTILINE)

# Qualifier: line must contain a code symbol to pass keyword scan
# (prevents false positives like "removed a typo in the README")
_CODE_SYMBOL_RE = re.compile(
    r"`[^`]+`"                      # backtick-wrapped `foo()`
    r"|[A-Za-z][a-z]+[A-Z]\w*"      # CamelCase or lowerCamelCase (createCustomer, PaymentProcessor)
    r"|\b\w+\.\w+[\(\.]"            # dot-method: obj.method( or obj.prop.
    r"|\b\w+\([^)]{0,60}\)"         # function call: foo(args)
    r"|v\d+\.\d+"                   # version ref: v2.0
    r"|\d+\.\d+\.\d+"               # semver: 1.2.3
)

# Migration note patterns
# Capture groups allow @scope/package names (e.g. @noble/hashes/sha256):
#   @?   — optional leading @ for scoped packages
#   [\w] — word char after optional @
#   [\w\.\-\/\(\)@]* — rest: allows . - / ( ) @ for paths like @noble/hashes/sha256
_MIGRATION_RE = re.compile(
    r"(?:use\s+[`'\"]?(@?[\w][\w\.\-\/\(\)@]*)[`'\"]?\s+instead"
    r"|replace(?:d)?\s+with\s+[`'\"]?(@?[\w][\w\.\-\/\(\)@]*)[`'\"]?"
    r"|migrate(?:d)?\s+to\s+[`'\"]?(@?[\w][\w\.\-\/\(\)@]*)[`'\"]?"
    r"|now\s+(?:use|using)\s+[`'\"]?(@?[\w][\w\.\-\/\(\)@]*)[`'\"]?"
    r"|instead\s+use\s+[`'\"]?(@?[\w][\w\.\-\/\(\)@]*)[`'\"]?)",
    re.IGNORECASE,
)

# Symbol extraction patterns
_BACKTICK_RE    = re.compile(r"`(@?[A-Za-z_][\w\.\-\/\(\)@]*)`")
_QUOTED_RE      = re.compile(r"""['"]([A-Za-z_][\w\.\-]+)['"]""")
_CAMEL_CASE_RE  = re.compile(r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b")
_SNAKE_CASE_RE  = re.compile(r"\b([a-z][a-z0-9]+(?:_[a-z0-9]+)+)\b")
_METHOD_CALL_RE = re.compile(r"\b([a-zA-Z_][\w\.]+\()")


# ── Public API ────────────────────────────────────────────────────────────────

def extract_breaking_changes(
    text: str,
    source: str = "release_notes",
) -> List[BreakingChange]:
    """Multi-pass extraction of breaking changes from changelog/release markdown.

    Pass 1: Find ## Breaking Changes section headers, extract bullet points
    Pass 2: Scan for Conventional Commits BREAKING CHANGE footer and feat!: syntax
    Pass 3: Keyword scanning — lines with a code symbol (medium confidence)
    Pass 3b: Keyword scanning — plain-English breaking lines without code symbol (low confidence)
    Pass 4: Classify and extract symbol for each candidate
    Deduplicate before returning.

    Candidates are (description, excerpt) or (description, excerpt, confidence_hint) tuples.
    """
    candidates: List = []

    # Pass 1: Breaking section headers
    candidates.extend(_pass1_section_headers(text))

    # Pass 2: Conventional commits
    candidates.extend(_pass2_conventional_commits(text))

    # Pass 3: Keyword scanning (filtered to avoid housekeeping prose)
    candidates.extend(_pass3_keyword_scan(text))

    # Pass 4: Classify each candidate
    breaking_changes: List[BreakingChange] = []
    for item in candidates:
        if isinstance(item, tuple) and len(item) == 3:
            desc, excerpt, confidence_hint = item
        elif isinstance(item, tuple):
            desc, excerpt = item
            confidence_hint = None
        else:
            desc, excerpt = item, item
            confidence_hint = None
        desc = desc.strip()
        if not desc:
            continue
        change_type   = classify_change_type(desc)
        symbol        = extract_symbol(desc)
        migration     = extract_migration_note(desc)
        if confidence_hint:
            confidence = confidence_hint
        else:
            confidence = "high" if _is_explicit_breaking(desc) else "med"
        breaking_changes.append(BreakingChange(
            symbol=symbol,
            change_type=change_type,
            description=desc,
            migration_note=migration,
            source=source,
            confidence=confidence,
            source_excerpt=excerpt[:300] if excerpt else None,
        ))

    return _deduplicate(breaking_changes)


def classify_change_type(text: str) -> str:
    """Classify breaking change type from description text.

    Returns: removed|renamed|signature_changed|behavior_changed|deprecated|
             type_changed|other
    """
    t = text.lower()
    if re.search(r"\b(removed?|deleted?|dropped?|no longer (?:available|supported?))\b", t):
        return "removed"
    if re.search(r"\b(renamed?|moved? to|now called)\b", t):
        return "renamed"
    if re.search(r"\b(signature|parameter|argument|return type|overload)\b", t):
        return "signature_changed"
    if re.search(r"\b(type changed?|return(?:s)? type|typed? as)\b", t):
        return "type_changed"
    if re.search(r"\b(deprecated)\b", t):
        return "deprecated"
    if re.search(r"\b(behavior|behaviour|semantic|now (?:throws?|raises?|returns?)|"
                 r"default(?:s)? (?:changed?|is now))\b", t):
        return "behavior_changed"
    return "other"


def extract_symbol(text: str) -> str:
    """Extract function/class/method name from breaking change text.

    Tries backtick-quoted identifiers, quoted identifiers, method calls,
    CamelCase, snake_case patterns.  Returns best guess or empty string.
    """
    # 1. Backtick-quoted — highest confidence
    m = _BACKTICK_RE.search(text)
    if m:
        return _base_symbol(m.group(1))

    # 2. Method call pattern: foo.bar(
    m = _METHOD_CALL_RE.search(text)
    if m:
        sym = m.group(1).rstrip("(")
        return _base_symbol(sym)

    # 3. Quoted identifier
    m = _QUOTED_RE.search(text)
    if m:
        return _base_symbol(m.group(1))

    # 4. CamelCase class name
    m = _CAMEL_CASE_RE.search(text)
    if m:
        return m.group(1)

    # 5. Long snake_case name (at least 3 components)
    m = _SNAKE_CASE_RE.search(text)
    if m:
        return m.group(1)

    return ""


def extract_migration_note(text: str) -> Optional[str]:
    """Extract 'use X instead' or 'replace with Y' patterns from text."""
    m = _MIGRATION_RE.search(text)
    if not m:
        return None
    # Return first non-None capturing group
    for group in m.groups():
        if group:
            return f"Use `{group}` instead."
    return None


def parse_version_section(changelog_text: str, version: str) -> Optional[str]:
    """Extract the changelog section for a specific version (e.g., ## [8.0.0]).

    Strategy:
    1. Exact match: ## [8.0.0] or ## 8.0.0
    2. Normalized match: strip leading 'v', normalize '8.0' → '8.0.0'
    3. Nearest preceding version: find closest version <= target
    """
    headers = list(_VERSION_HEADER_RE.finditer(changelog_text))
    if not headers:
        return None

    def _section(idx: int) -> str:
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(changelog_text)
        return changelog_text[headers[idx].start():end].strip()

    # Step 1: Exact match
    for idx, m in enumerate(headers):
        if m.group(1) == version:
            return _section(idx)

    # Step 2: Normalized match (strip leading 'v', pad to 3 parts)
    def _norm(v: str) -> str:
        v = v.lstrip("v")
        parts = v.split(".")
        while len(parts) < 3:
            parts.append("0")
        return ".".join(parts[:3])

    norm_target = _norm(version)
    for idx, m in enumerate(headers):
        if _norm(m.group(1)) == norm_target:
            return _section(idx)

    # Step 3: Nearest preceding version (e.g. looking for 8.0.1 → use 8.0.0)
    target_ver = _parse_semver(version)
    if target_ver is None:
        return None

    best_idx: Optional[int] = None
    best_ver = None
    for idx, m in enumerate(headers):
        hdr_ver = _parse_semver(m.group(1))
        if hdr_ver is None:
            continue
        if hdr_ver <= target_ver:
            if best_ver is None or hdr_ver > best_ver:
                best_ver = hdr_ver
                best_idx = idx

    if best_idx is not None:
        return _section(best_idx)

    return None


def parse_all_version_sections(
    changelog_text: str,
    from_version: str,
    to_version: str,
) -> Optional[str]:
    """Extract and concatenate ALL CHANGELOG sections for versions strictly
    newer than *from_version* up to and including *to_version*.

    Used for multi-major jumps (e.g. starknet 7→9) to collect v8.0.0 and
    v9.0.0 sections from CHANGELOG.md rather than only the latest version.
    Returns None if no relevant sections are found.
    """
    headers = list(_VERSION_HEADER_RE.finditer(changelog_text))
    if not headers:
        return None

    from_v = _parse_semver(from_version)
    to_v   = _parse_semver(to_version)

    def _section_text(idx: int) -> str:
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(changelog_text)
        return changelog_text[headers[idx].start():end].strip()

    sections: List[str] = []
    for idx, m in enumerate(headers):
        hdr_ver = _parse_semver(m.group(1))
        if hdr_ver is None:
            continue
        # Include sections strictly newer than from_version, up to to_version
        if from_v is not None and hdr_ver <= from_v:
            continue
        if to_v is not None and hdr_ver > to_v:
            continue
        sections.append(_section_text(idx))

    if not sections:
        return None
    return "\n\n---\n\n".join(sections)


def has_breaking_changes_flag(text: str) -> bool:
    """Quick check: does this text contain any breaking change markers?"""
    if _BREAKING_SECTION_RE.search(text):
        return True
    if _CC_FOOTER_RE.search(text):
        return True
    if _CC_BANG_RE.search(text):
        return True
    if _BREAKING_KEYWORDS_RE.search(text):
        return True
    return False


# ── Internal passes ───────────────────────────────────────────────────────────

def _pass1_section_headers(text: str) -> List[Tuple[str, str]]:
    """Find ## Breaking Changes sections and extract their bullet points.

    Returns list of (description, source_excerpt) tuples.
    """
    results: List[Tuple[str, str]] = []
    lines = text.splitlines()
    in_breaking_section = False
    section_depth = 0

    for line in lines:
        # Check for a breaking section header
        if _BREAKING_SECTION_RE.match(line.strip()):
            in_breaking_section = True
            # Capture header depth (number of # chars)
            section_depth = len(line) - len(line.lstrip("#"))
            continue

        if in_breaking_section:
            # End section on a new header of same or lesser depth
            header_m = re.match(r"^(#{1,4})\s+", line)
            if header_m:
                depth = len(header_m.group(1))
                if depth <= section_depth:
                    in_breaking_section = False
                    continue

            # Collect bullet points
            bullet_m = re.match(r"^[\s]*[-\*\+]\s+(.+)$", line)
            if bullet_m:
                desc = bullet_m.group(1).strip()
                results.append((desc, line.strip()))
            elif line.strip() and not line.startswith("#"):
                # Plain paragraph text in the breaking section
                results.append((line.strip(), line.strip()))

    return results


def _pass2_conventional_commits(text: str) -> List[Tuple[str, str]]:
    """Scan for BREAKING CHANGE footers and feat!: syntax.

    Returns list of (description, source_excerpt) tuples.
    """
    results: List[Tuple[str, str]] = []

    for m in _CC_FOOTER_RE.finditer(text):
        body = m.group(1).strip()
        # Could be multi-sentence; split on newlines
        for line in body.splitlines():
            line = line.strip()
            if line:
                results.append((line, f"BREAKING CHANGE: {line}"))

    for m in _CC_BANG_RE.finditer(text):
        desc = m.group(1).strip()
        results.append((desc, m.group(0).strip()))

    return results


def _pass3_keyword_scan(text: str) -> List[Tuple]:
    """Scan every line for breaking-change keywords.

    Tier 1 (medium confidence, 2-tuple): line has a code symbol (backtick,
    CamelCase, dot-method, function call, version reference), OR is inside a
    code/indented block.

    Tier 2 (low confidence, 3-tuple with "low" hint): line has no code symbol
    but contains an unambiguous strong plain-English breaking phrase such as
    "not backward compatible", "drop support", "breaking change", etc.
    These cannot be housekeeping noise but lack a specific symbol to scan for.

    Returns list of (description, excerpt) or (description, excerpt, "low") tuples.
    """
    results: List[Tuple] = []
    in_code_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        # Skip section headers and empty lines
        if not stripped or stripped.startswith("#"):
            continue
        if not _BREAKING_KEYWORDS_RE.search(stripped):
            continue
        # Strip bullet prefix for description
        clean = re.sub(r"^[-\*\+]\s+", "", stripped)
        indent = len(line) - len(line.lstrip())
        if in_code_block or indent >= 4:
            results.append((clean, stripped))
        elif _CODE_SYMBOL_RE.search(stripped):
            # Has a code symbol — medium confidence
            results.append((clean, stripped))
        elif _STRONG_PLAIN_BREAKING_RE.search(stripped):
            # Unambiguous plain-English breaking phrase; no specific symbol —
            # accept at low confidence so the user still sees the signal.
            results.append((clean, stripped, "low"))
        # else: too ambiguous (e.g. "removed a typo in the README") — skip
    return results


def _is_explicit_breaking(text: str) -> bool:
    """Return True if text contains an explicit 'breaking change' marker."""
    return bool(re.search(r"\b(breaking change|BREAKING CHANGE|breaking:)\b",
                           text, re.IGNORECASE))


def _deduplicate(items: List[BreakingChange]) -> List[BreakingChange]:
    """Remove near-duplicate breaking changes by description similarity."""
    if not items:
        return items

    unique: List[BreakingChange] = []
    seen_sigs: List[str] = []

    for item in items:
        sig = _normalize_sig(item.description)
        if _is_too_similar(sig, seen_sigs):
            continue
        seen_sigs.append(sig)
        unique.append(item)

    return unique


def _normalize_sig(text: str) -> str:
    """Normalise a description to a lowercase word-set signature."""
    words = re.findall(r"[a-z0-9_]+", text.lower())
    # Remove stop words
    stop = {"the", "a", "an", "is", "was", "has", "been", "to", "of",
             "in", "and", "or", "that", "this", "it", "for", "with"}
    meaningful = [w for w in words if w not in stop and len(w) > 1]
    return " ".join(sorted(set(meaningful)))


def _is_too_similar(sig: str, seen: List[str], threshold: float = 0.7) -> bool:
    """Return True if sig is too similar to any existing signature (Jaccard)."""
    if not sig:
        return False
    a_set = set(sig.split())
    for existing in seen:
        b_set = set(existing.split())
        if not a_set and not b_set:
            continue
        union = a_set | b_set
        intersection = a_set & b_set
        if union and len(intersection) / len(union) >= threshold:
            return True
    return False


def _base_symbol(sym: str) -> str:
    """Delegate to module-level _extract_base_symbol equivalent."""
    parts = re.split(r"[.\:]", sym)
    return parts[-1].rstrip("()") if parts else sym
