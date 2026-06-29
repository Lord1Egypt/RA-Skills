"""
🛠️ axiom-css-specificity — CSS Specificity Calculator
======================================================

⚠️ LIMITATIONS CONNUES :
- Ne gère pas @scope (trop récent)
- :is() / :not() : on prend la spécificité max des arguments
- Pas de résolution !important (CSS Cascade layer)

CALCULE LA SPÉCIFICITÉ D'UN SÉLECTEUR CSS (a, b, c)

Usage CLI:
    python3 axiom_css_specificity.py "#header .nav a:hover"
    python3 axiom_css_specificity.py "div.container > p.error" --compare ".error"
"""

import re
import sys


def _split_outside_parens(selector: str) -> list:
    """
    Split a selector into [outside-paren, (paren-content, paren-content, ...)]
    using depth tracking. Yields ('outer', text) and ('inner', text) tuples.
    The outer keeps the opening '(' so we can detect functional pseudos.
    """
    segments = []
    current_outer = []
    current_inner = []
    depth = 0
    in_paren = False

    for ch in selector:
        if ch == "(":
            depth += 1
            if depth == 1:
                # Keep the '(' in the outer
                current_outer.append(ch)
                in_paren = True
                current_inner = []
            else:
                current_inner.append(ch)
        elif ch == ")":
            depth -= 1
            if depth == 0:
                segments.append(("outer", "".join(current_outer)))
                current_outer = []
                segments.append(("inner", "".join(current_inner)))
                current_inner = []
                in_paren = False
            else:
                current_inner.append(ch)
        else:
            if in_paren:
                current_inner.append(ch)
            else:
                current_outer.append(ch)

    if current_outer:
        segments.append(("outer", "".join(current_outer)))
    if current_inner:
        segments.append(("inner", "".join(current_inner)))

    return segments


def _spec_outer(text: str) -> tuple:
    """
    Compute specificity of a flat string (no parens).
    Returns (a, b, c).
    """
    a, b, c = 0, 0, 0
    s = text

    if not s.strip():
        return (0, 0, 0)

    # Universal selector alone
    if s.strip() == "*":
        return (0, 0, 0)

    # IDs: #foo
    a = len(re.findall(r"#[a-zA-Z][\w-]*", s))

    # Classes: .foo
    b += len(re.findall(r"\.[a-zA-Z][\w-]*", s))

    # Attribute selectors: [foo=bar]
    b += len(re.findall(r"\[[^\]]+\]", s))

    # Pseudo-elements (::foo) — count as c
    c += len(re.findall(r"::[a-zA-Z-]+", s))

    # Strip pseudo-elements
    s = re.sub(r"::[a-zA-Z-]+(?:\([^)]*\))?", "", s)

    # Pseudo-classes (:foo) — count as b
    # Find all :name patterns
    pc_matches = re.findall(r":[a-zA-Z-]+", s)
    for pc in pc_matches:
        # Strip the leading ":"
        name = pc[1:]
        # :is/:not/:has/:where are handled at higher level
        # Here we just count as b for plain pseudo-classes
        b += 1

    # Strip all pseudo-classes
    s = re.sub(r":[a-zA-Z-]+(?:\([^)]*\))?", "", s)
    # Strip IDs, classes, attributes
    s = re.sub(r"#[a-zA-Z][\w-]*", "", s)
    s = re.sub(r"\[[^\]]+\]", "", s)
    s = re.sub(r"\.[a-zA-Z][\w-]*", "", s)

    # Elements: alphanumeric tokens (excluding combinators)
    elements = re.findall(r"[a-zA-Z][\w-]*", s)
    c += len(elements)

    return (a, b, c)


def _spec_inner(text: str, pseudo_name: str) -> tuple:
    """
    Compute specificity contributed by a :pseudo(arg) inner content.
    For :is/:not/:has: returns max of args.
    For :where: returns (0, 0, 0) always.
    """
    if pseudo_name == "where":
        return (0, 0, 0)

    # :is/:not/:has : return max specificity of comma-separated args
    args = [a.strip() for a in text.split(",") if a.strip()]
    if not args:
        return (0, 0, 0)

    specs = []
    for arg in args:
        # Process the arg as if it were a top-level selector
        spec = _calculate_single(arg)
        specs.append(spec)

    if not specs:
        return (0, 0, 0)

    return max(specs, key=lambda t: (t[0] * 100 + t[1] * 10 + t[2]))


def _calculate_single(selector: str) -> tuple:
    """Specificity of a single compound/complex selector (no top-level commas)."""
    global pending_pseudo
    pending_pseudo = None

    # Split by top-level combinators (>, +, ~, ||) and whitespace
    # But we also need to handle :is/:not/:has/:where content
    segments = _split_outside_parens(selector)

    total_a, total_b, total_c = 0, 0, 0

    for kind, text in segments:
        if kind == "outer":
            # Split by combinators
            parts = re.split(r"\s*[>+~]\s*|\s+", text)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                # Process this part
                spec = _process_outer_with_pending(part)
                total_a += spec[0]
                total_b += spec[1]
                total_c += spec[2]
        elif kind == "inner":
            # Find which pseudo this belongs to
            if pending_pseudo:
                pseudo_name = pending_pseudo
                spec = _spec_inner(text, pseudo_name)
                total_a += spec[0]
                total_b += spec[1]
                total_c += spec[2]
                pending_pseudo = None

    return (total_a, total_b, total_c)


pending_pseudo = None  # Global state for pseudo name tracking


def _process_outer_with_pending(part: str) -> tuple:
    """Process an outer segment, tracking pending pseudo for inner."""
    global pending_pseudo
    pending_pseudo = None

    # Find any :name( in this part (functional pseudo with parens)
    m = re.search(r":([a-zA-Z-]+)\s*\(", part)
    if m:
        pending_pseudo = m.group(1)

    # Remove ONLY :name followed by ( — the inner will handle the args
    # Other pseudo-classes (:hover, :focus, etc.) stay in outer and count as b
    part_stripped = re.sub(r":[a-zA-Z-]+\s*\(", "", part)

    return _spec_outer(part_stripped)


# Reset global at module load
def calculate(selector: str) -> tuple:
    """
    Calcule la spécificité d'un sélecteur CSS complet.

    Per W3C CSS Selectors Level 4:
    - a = ID selectors
    - b = class, attribute, pseudo-class
    - c = type, pseudo-element

    For comma-separated selector lists, returns the MAX of all selectors.

    Returns:
        tuple (a, b, c)
    """
    global pending_pseudo
    pending_pseudo = None

    if not selector or not selector.strip():
        raise ValueError("empty selector")

    # Handle selector list (comma-separated) — return max
    selectors = [s.strip() for s in selector.split(",") if s.strip()]

    if len(selectors) > 1:
        specs = [_calculate_single(s) for s in selectors]
        return max(specs, key=lambda t: (t[0] * 100 + t[1] * 10 + t[2]))

    return _calculate_single(selectors[0])


# ============================================================================
# Formatting & comparison
# ============================================================================

def format_specificity(spec: tuple) -> str:
    """Format specificity as (a, b, c) string."""
    return f"({spec[0]}, {spec[1]}, {spec[2]})"


def compare(selector_a: str, selector_b: str) -> dict:
    """Compare specificity of two selectors."""
    spec_a = calculate(selector_a)
    spec_b = calculate(selector_b)

    if spec_a > spec_b:
        winner = "a"
    elif spec_b > spec_a:
        winner = "b"
    else:
        winner = "tie"

    return {
        "selector_a": selector_a,
        "selector_b": selector_b,
        "specificity_a": spec_a,
        "specificity_b": spec_b,
        "winner": winner,
    }


# ============================================================================
# Common presets
# ============================================================================

EXAMPLES = [
    ("*", (0, 0, 0)),
    ("div", (0, 0, 1)),
    (".container", (0, 1, 0)),
    ("#header", (1, 0, 0)),
    ("div.container", (0, 1, 1)),
    ("#header .nav", (1, 1, 0)),
    ("#header .nav a:hover", (1, 2, 1)),
    ("div.container > p.error", (0, 2, 2)),
    ("a[href*='example']", (0, 1, 1)),
    (":not(.foo)", (0, 1, 0)),
    (":is(h1, h2, h3)", (0, 0, 1)),
    (":where(.foo)", (0, 0, 0)),
    ("::before", (0, 0, 1)),
    (".foo .bar, .baz", (0, 2, 0)),
]


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-css-specificity — CSS specificity calculator "
    )
    parser.add_argument("selector", nargs="?", help="CSS selector")
    parser.add_argument("--compare", help="Compare with another selector")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--examples", action="store_true", help="Show common examples")
    args = parser.parse_args()

    if args.examples:
        for sel, expected in EXAMPLES:
            actual = calculate(sel)
            icon = "✅" if actual == expected else "⚠️"
            print(f"{icon} {sel:<30} → {format_specificity(actual)}  (expected {format_specificity(expected)})")
        return 0

    if not args.selector:
        parser.print_help()
        return 1

    try:
        if args.compare:
            result = compare(args.selector, args.compare)
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            else:
                print(f"A: {result['selector_a']:<30} → {format_specificity(result['specificity_a'])}")
                print(f"B: {result['selector_b']:<30} → {format_specificity(result['specificity_b'])}")
                if result["winner"] == "tie":
                    print(f"\n🤝 Tie — same specificity")
                else:
                    print(f"\n🏆 Winner: {result['winner']}")
            return 0

        spec = calculate(args.selector)
        if args.json:
            import json
            print(json.dumps({"selector": args.selector, "specificity": list(spec)}, indent=2))
        else:
            print(f"Selector:    {args.selector}")
            print(f"Specificity: {format_specificity(spec)}  (a={spec[0]}, b={spec[1]}, c={spec[2]})")
        return 0

    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
