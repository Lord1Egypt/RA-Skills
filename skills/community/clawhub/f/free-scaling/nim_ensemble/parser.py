"""Answer extraction from model responses — handles thinking models, word boundaries."""

import re

# Negation prefix detector — rejects "NOT SAFE" matching as SAFE
_NEGATION_RE = re.compile(
    r'\b(?:NOT|NO|ISN\'T|AREN\'T|DOESN\'T|DON\'T|NEVER|NEITHER|NOR)'
    r'(?:\s+\w+){0,3}\s*$'  # up to 3 intervening words before the match
)


def strip_thinking(content: str) -> str:
    """Strip <think>...</think> blocks from content (MiniMax M2.5 style)."""
    if not content or "<think>" not in content:
        return content or ""
    after = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()
    return after if after else content


def extract_content(message: dict) -> str:
    """Extract answer text from a chat completion message.
    
    Handles:
    - Normal models: content field
    - MiniMax M2.5: <think>...</think>answer in content
    - Kimi K2.5/Qwen3: content=null, answer in reasoning_content
    """
    content = message.get("content", "") or ""
    
    # Strip inline thinking blocks
    content = strip_thinking(content)
    
    # Fallback to reasoning_content for thinking models with null content
    if not content and message.get("reasoning_content"):
        content = message["reasoning_content"]
    
    return content


# Answer patterns sorted longest-first to avoid substring matches
# e.g., "NOT_PATCHED" must match before "NO", "INCONSISTENT" before "CONSISTENT"
DEFAULT_PATTERNS = [
    # Compound
    "SIGNIFICANT_DRIFT", "MINOR_DRIFT", "NOT_PATCHED", "TIMEOUT_PATTERN",
    "OVER_CAPACITY", "HAS_ISSUES", "NEEDS_OVERHAUL", "GHOSTS_FOUND",
    "PATTERN_DETECTED", "COULD_DOWNGRADE", "NEEDS_UPGRADE",
    "GHOST_IDS", "UNABLE_TO_PARSE", "SHOULD_CLEAN", "TOO_SHORT", "TOO_WEAK",
    "MINOR_GAPS", "MAJOR_GAPS", "NEEDS_REVIEW",
    # Long single words
    "INCONSISTENT", "COMPLIANT", "VIOLATIONS", "VIOLATED",
    "PARTIALLY", "HALLUCINATED", "EMBELLISHED",
    "WASTEFUL", "EFFICIENT",
    "REPEATING", "IMPROVING", "DEGRADING", "DEGRADED",
    "DRIFTING",
    "FOLLOWED", "ACCURATE",
    "CONSISTENT", "PATCHED",
    "RELIABLE", "FAILING", "FLAKY",
    "HEALTHY", "PRESSURE",
    "CONTINUOUS", "ACCEPTABLE", "APPROPRIATE", "BORDERLINE",
    "ADEQUATE", "EXPLICIT", "IMPLICIT",
    "CRITICAL", "ANOMALIES", "CONTRADICTIONS", "SOMETIMES",
    "BROKEN", "STABLE", "FRESH", "STALE", "CLEAN",
    "UNSAFE", "SAFE",
    "GOOD", "BAD",
    # Short last
    "YES", "NO",
    "UNCLEAR",
]


def parse_answer(raw_response: str, patterns: list[str] = None) -> str:
    """Extract structured answer from model response.
    
    Looks for recognized answer keywords at the START of the first line,
    checking longer patterns first to avoid substring false matches.
    
    Args:
        raw_response: Full model response text
        patterns: Custom answer patterns (default: DEFAULT_PATTERNS)
    
    Returns:
        Matched pattern string, or "UNCLEAR" if no match
    """
    if not raw_response:
        return "UNCLEAR"
    
    search_patterns = patterns or DEFAULT_PATTERNS
    # Sort longest-first to avoid substring false matches
    search_patterns = sorted(search_patterns, key=len, reverse=True)
    
    first_line = raw_response.strip().split("\n")[0].strip()
    first_line_clean = first_line.replace("**", "").strip().upper()
    
    # First pass: match at start of line (escape patterns to prevent regex injection)
    for pattern in search_patterns:
        escaped = re.escape(pattern)
        if re.match(rf'^{escaped}\b', first_line_clean):
            return pattern
    
    # Second pass: match anywhere as whole word, but reject negated matches
    # Catches: "NOT SAFE", "not at all SAFE", "not really COMPLIANT", "ISN'T SAFE"
    for pattern in search_patterns:
        escaped = re.escape(pattern)
        match = re.search(rf'\b{escaped}\b', first_line_clean)
        if match:
            # Check if preceded by a negation (with up to 3 words gap)
            prefix = first_line_clean[:match.start()].rstrip()
            if not _NEGATION_RE.search(prefix):
                return pattern
    
    return "UNCLEAR"
