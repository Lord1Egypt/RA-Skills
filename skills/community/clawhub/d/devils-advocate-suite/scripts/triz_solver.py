"""
TRIZ Contradiction Solver for Business Trade-offs.
Resolves technical and business contradictions using inventive principles.
"""

TRIZ_PRINCIPLES = {
    1: "Segmentation: Divide the organization into product centers or autonomous units.",
    2: "Taking Out: Separate interfering parts (e.g., separate people from the problem).",
    10: "Preliminary Action: Perform the change fully or partially before it is needed.",
    13: "The Other Way Round: Invert actions (e.g., expansion instead of contraction).",
    23: "Feedback: Introduce cross-checking (e.g., enlist customers in the design process).",
    24: "Intermediary: Use a third party (e.g., mediator or consultant).",
    25: "Self-service: Make the object serve itself by performing auxiliary and repair functions.",
    35: "Parameter Changes: Change the system's physical state, concentration, flexibility, or temperature.",
}

# Contradiction matrix: maps (param_a, param_b) -> list of principle IDs
CONTRADICTION_MATRIX = {
    ("Speed", "Quality"): [1, 10, 23],
    ("Quality", "Speed"): [1, 10, 23],
    ("Capacity", "Complexity"): [1, 2, 24],
    ("Complexity", "Capacity"): [1, 2, 24],
    ("Profitability", "Sustainability"): [13, 23, 2],
    ("Sustainability", "Profitability"): [13, 23, 2],
    ("Speed", "Cost"): [1, 10, 25],
    ("Cost", "Speed"): [1, 10, 25],
    ("Customization", "Scalability"): [1, 2, 35],
    ("Scalability", "Customization"): [1, 2, 35],
    ("Innovation", "Stability"): [13, 10, 23],
    ("Stability", "Innovation"): [13, 10, 23],
}


def resolve_contradiction(param_a, param_b):
    """
    Look up TRIZ principles for a given business contradiction.
    Returns a list of applicable principle descriptions.
    """
    key = (param_a.strip().title(), param_b.strip().title())
    reverse_key = (param_b.strip().title(), param_a.strip().title())

    principle_ids = CONTRADICTION_MATRIX.get(key) or CONTRADICTION_MATRIX.get(reverse_key)

    if principle_ids:
        return [f"Principle {p}: {TRIZ_PRINCIPLES[p]}" for p in principle_ids]
    else:
        # Generic fallback using most versatile principles
        generic = [1, 2, 10, 13, 23, 24]
        results = [f"Principle {p}: {TRIZ_PRINCIPLES[p]}" for p in generic]
        results.append(
            "\nNote: No exact match found. Consult references/methodology_summary.md "
            "for the full 40-principle TRIZ matrix."
        )
        return results


def list_known_contradictions():
    """Print all pre-mapped contradiction pairs."""
    seen = set()
    pairs = []
    for a, b in CONTRADICTION_MATRIX.keys():
        pair = tuple(sorted([a, b]))
        if pair not in seen:
            seen.add(pair)
            pairs.append(f"  {pair[0]} vs {pair[1]}")
    return pairs


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        p_a, p_b = sys.argv[1], sys.argv[2]
        print(f"\nResolving contradiction: {p_a} vs {p_b}\n")
        print("Recommended TRIZ Principles:")
        for principle in resolve_contradiction(p_a, p_b):
            print(f"  - {principle}")
    elif len(sys.argv) == 2 and sys.argv[1] == "--list":
        print("\nKnown contradiction pairs:")
        for pair in list_known_contradictions():
            print(pair)
        print("\nUsage: python triz_solver.py [Param A] [Param B]")
        print("Example: python triz_solver.py Speed Quality")
    else:
        print("Usage: python triz_solver.py [Param A] [Param B]")
        print("       python triz_solver.py --list")
        print("\nExample: python triz_solver.py Customization Scalability")
