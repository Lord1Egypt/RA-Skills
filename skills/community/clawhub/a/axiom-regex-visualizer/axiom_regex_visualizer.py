"""
🛠️ axiom-regex-visualizer — Regex Pattern Visualizer
======================================================

⚠️ LIMITATIONS CONNUES :
- Pas de support des lookbehind complexes
- Pas de backref visualization
- Pas de Unicode property visualization

VISUALISE UN PATTERN REGEX EN STRUCTURE LISIBLE
"""

import re
import sys


# Tokenize regex into components
TOKEN_TYPES = {
    "literal": "Lit",
    "char_class": "Class",
    "predefined": "Pre",
    "group_capture": "Group",
    "group_noncapture": "NCGroup",
    "group_named": "NGroup",
    "quantifier_star": "*",
    "quantifier_plus": "+",
    "quantifier_question": "?",
    "quantifier_exact": "{n}",
    "quantifier_range": "{n,m}",
    "anchor_start": "^",
    "anchor_end": "$",
    "anchor_word_boundary": r"\b",
    "alternation": "|",
    "dot": ".",
    "escape": r"\x",
}


def tokenize(pattern: str) -> list:
    """
    Tokenize a regex pattern into a list of (type, value) tuples.

    Returns a list of tokens for visualization.
    """
    tokens = []
    i = 0
    n = len(pattern)

    while i < n:
        ch = pattern[i]

        if ch == "\\":
            # Escape sequence
            if i + 1 < n:
                next_ch = pattern[i+1]
                if next_ch in "dDsSwWbB":
                    # Predefined class
                    name = {
                        "d": r"\d (digit)",
                        "D": r"\D (non-digit)",
                        "s": r"\s (whitespace)",
                        "S": r"\S (non-whitespace)",
                        "w": r"\w (word char)",
                        "W": r"\W (non-word char)",
                        "b": r"\b (word boundary)",
                        "B": r"\B (non-word boundary)",
                    }[next_ch]
                    tokens.append(("predefined", name))
                    i += 2
                    continue
                elif next_ch in "0123456789":
                    # Backref
                    j = i + 1
                    while j < n and pattern[j].isdigit():
                        j += 1
                    tokens.append(("escape", f"\\{pattern[i+1:j]} (backref)"))
                    i = j
                    continue
                else:
                    # Escaped literal
                    tokens.append(("literal", next_ch))
                    i += 2
                    continue
            else:
                i += 1
                continue

        elif ch == "[":
            # Character class
            j = i + 1
            if j < n and pattern[j] == "^":
                j += 1
            while j < n and pattern[j] != "]":
                j += 1
            tokens.append(("char_class", pattern[i:j+1]))
            i = j + 1
            continue

        elif ch == "(":
            # Group
            j = i + 1
            group_type = "group_capture"
            if j < n and pattern[j] == "?":
                if j + 1 < n and pattern[j+1] == ":":
                    group_type = "group_noncapture"
                    j += 2
                elif j + 1 < n and pattern[j+1] == "<":
                    # Named group
                    k = j + 2
                    while k < n and pattern[k] != ">":
                        k += 1
                    group_type = "group_named"
                    j = k + 1
                else:
                    j += 1
            tokens.append((group_type, "("))
            i = j
            continue

        elif ch in "*+?":
            tokens.append((f"quantifier_{ {'*':'star','+':'plus','?':'question'}[ch] }", ch))
            i += 1
            continue

        elif ch == "{":
            j = i + 1
            while j < n and pattern[j] != "}":
                j += 1
            content = pattern[i+1:j]
            if "," in content:
                tokens.append(("quantifier_range", f"{{{content}}}"))
            else:
                tokens.append(("quantifier_exact", f"{{{content}}}"))
            i = j + 1
            continue

        elif ch == "^":
            tokens.append(("anchor_start", "^ (start)"))
            i += 1
            continue

        elif ch == "$":
            tokens.append(("anchor_end", "$ (end)"))
            i += 1
            continue

        elif ch == "|":
            tokens.append(("alternation", "| (OR)"))
            i += 1
            continue

        elif ch == ".":
            tokens.append(("dot", ". (any)"))
            i += 1
            continue

        elif ch == ")":
            tokens.append(("group_close", ")"))
            i += 1
            continue

        else:
            # Literal
            tokens.append(("literal", ch))
            i += 1
            continue

    return tokens


def visualize(pattern: str, indent: int = 0) -> str:
    """
    Return a human-readable visualization of a regex pattern.
    """
    tokens = tokenize(pattern)
    lines = []
    depth = 0
    prefix = "  " * indent

    lines.append(f"{prefix}Pattern: {pattern}")
    lines.append(f"{prefix}{'─' * 50}")

    for tok_type, tok_value in tokens:
        if tok_type in ("group_capture", "group_noncapture", "group_named"):
            lines.append(f"{prefix}  {'  ' * depth}┌─ [{tok_type.replace('group_', '')}]")
            depth += 1
        elif tok_type == "group_close":
            depth = max(0, depth - 1)
            lines.append(f"{prefix}  {'  ' * depth}└─")
        elif tok_type == "alternation":
            lines.append(f"{prefix}  {'  ' * depth}│  OR")
        elif tok_type.startswith("quantifier_"):
            lines.append(f"{prefix}  {'  ' * depth}└─ {tok_value} (repeat)")
        elif tok_type.startswith("anchor_"):
            lines.append(f"{prefix}  {'  ' * depth}📍 {tok_value}")
        elif tok_type == "dot":
            lines.append(f"{prefix}  {'  ' * depth}• (any char)")
        elif tok_type == "predefined":
            lines.append(f"{prefix}  {'  ' * depth}{tok_value}")
        elif tok_type == "char_class":
            lines.append(f"{prefix}  {'  ' * depth}📋 {tok_value}")
        else:
            lines.append(f"{prefix}  {'  ' * depth}'{tok_value}'")

    lines.append(f"{prefix}{'─' * 50}")
    return "\n".join(lines)


def explain(pattern: str) -> str:
    """Plain-English explanation of the pattern."""
    tokens = tokenize(pattern)
    parts = []
    for tok_type, tok_value in tokens:
        if tok_type == "literal":
            parts.append(f"the character '{tok_value}'")
        elif tok_type == "predefined":
            parts.append(f"a {tok_value.replace('\\\\', '')}")
        elif tok_type == "char_class":
            parts.append(f"any character in `{tok_value}`")
        elif tok_type == "dot":
            parts.append("any character")
        elif tok_type == "group_capture":
            parts.append("a group capturing")
        elif tok_type == "group_noncapture":
            parts.append("a non-capturing group of")
        elif tok_type == "quantifier_star":
            parts.append("(zero or more times)")
        elif tok_type == "quantifier_plus":
            parts.append("(one or more times)")
        elif tok_type == "quantifier_question":
            parts.append("(zero or one time)")
        elif tok_type == "anchor_start":
            parts.append("start of string")
        elif tok_type == "anchor_end":
            parts.append("end of string")
        elif tok_type == "alternation":
            parts.append("OR")
    return " ".join(parts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-regex-visualizer ")
    parser.add_argument("pattern", nargs="?", help="Regex pattern to visualize")
    parser.add_argument("--explain", action="store_true", help="Plain English explanation")
    parser.add_argument("--tokens", action="store_true", help="Just show tokens")
    args = parser.parse_args()

    if not args.pattern:
        # Demo
        examples = [
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            r"(\d{3})-(\d{3})-(\d{4})",
            r"https?://[^\s]+",
        ]
        for ex in examples:
            print(visualize(ex))
            print(explain(ex))
            print()
        return 0

    if args.tokens:
        for tok in tokenize(args.pattern):
            print(tok)
    elif args.explain:
        print(explain(args.pattern))
    else:
        print(visualize(args.pattern))
        print()
        print(explain(args.pattern))
    return 0


if __name__ == "__main__":
    sys.exit(main())
