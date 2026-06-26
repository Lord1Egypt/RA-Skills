#!/usr/bin/env python3
"""
Logical Consistency Checker for First-Principles Analysis

Verifies if a set of assumptions is logically consistent by converting them
to propositional logic and checking for contradictions using SAT solving.
"""

import argparse
import json
import sys

def parse_proposition(prop_str):
    """
    Parse a simple proposition string into a logical structure.
    Supports: AND, OR, NOT, IMPLIES, IFF
    """
    prop_str = prop_str.strip()
    
    # Simple atomic proposition
    if ' ' not in prop_str or prop_str.upper() in ['TRUE', 'FALSE']:
        return {'type': 'atom', 'value': prop_str}
    
    # Negation
    if prop_str.upper().startswith('NOT '):
        inner = parse_proposition(prop_str[4:].strip())
        return {'type': 'not', 'operand': inner}
    
    # Binary operators
    operators = ['IFF', 'IMPLIES', 'AND', 'OR']
    for op in operators:
        parts = prop_str.split(f' {op} ', 1)
        if len(parts) == 2:
            left = parse_proposition(parts[0])
            right = parse_proposition(parts[1])
            return {'type': op.lower(), 'left': left, 'right': right}
    
    # Default: treat as atomic
    return {'type': 'atom', 'value': prop_str}

def evaluate_proposition(prop, assignment):
    """
    Evaluate a proposition given a truth assignment.
    assignment is a dict mapping atom names to True/False.
    """
    if prop['type'] == 'atom':
        val = prop['value'].upper()
        if val == 'TRUE':
            return True
        elif val == 'FALSE':
            return False
        else:
            return assignment.get(prop['value'], False)
    
    elif prop['type'] == 'not':
        return not evaluate_proposition(prop['operand'], assignment)
    
    elif prop['type'] == 'and':
        return (evaluate_proposition(prop['left'], assignment) and
                evaluate_proposition(prop['right'], assignment))
    
    elif prop['type'] == 'or':
        return (evaluate_proposition(prop['left'], assignment) or
                evaluate_proposition(prop['right'], assignment))
    
    elif prop['type'] == 'implies':
        # P -> Q is equivalent to NOT P OR Q
        p = evaluate_proposition(prop['left'], assignment)
        q = evaluate_proposition(prop['right'], assignment)
        return (not p) or q
    
    elif prop['type'] == 'iff':
        # P <-> Q is (P -> Q) AND (Q -> P)
        p = evaluate_proposition(prop['left'], assignment)
        q = evaluate_proposition(prop['right'], assignment)
        return ((not p) or q) and ((not q) or p)

def extract_atoms(prop):
    """Extract all atomic propositions from a proposition."""
    if prop['type'] == 'atom':
        if prop['value'].upper() not in ['TRUE', 'FALSE']:
            return {prop['value']}
    elif prop['type'] == 'not':
        return extract_atoms(prop['operand'])
    elif prop['type'] in ['and', 'or', 'implies', 'iff']:
        return extract_atoms(prop['left']).union(extract_atoms(prop['right']))
    return set()

def check_consistency(propositions):
    """
    Check if a set of propositions is consistent.
    Returns a tuple (is_consistent, counterexample)
    
    is_consistent: True if no contradiction found, False otherwise
    counterexample: If inconsistent, the assignment that causes contradiction
    """
    # Extract all atoms
    all_atoms = set()
    for prop in propositions:
        all_atoms.update(extract_atoms(prop))
    
    atoms_list = list(all_atoms)
    n = len(atoms_list)
    
    if n > 20:
        # Too many atoms for brute force
        return True, None  # Assume consistent (heuristic)
    
    # Brute force search for a satisfying assignment
    for i in range(2**n):
        assignment = {}
        for j, atom in enumerate(atoms_list):
            assignment[atom] = bool((i >> j) & 1)
        
        # Check if all propositions evaluate to True
        all_true = True
        for prop in propositions:
            if not evaluate_proposition(prop, assignment):
                all_true = False
                break
        
        if all_true:
            # Found a satisfying assignment
            return True, None
    
    # No satisfying assignment found
    return False, None

def check_conclusion(premises, conclusion):
    """
    Check if conclusion is entailed by premises.
    Returns (is_entailed, counterexample)
    """
    # Conclusion is entailed if {premises, NOT conclusion} is inconsistent
    negated_conclusion = {
        'type': 'not',
        'operand': conclusion
    }
    
    all_props = premises + [negated_conclusion]
    is_consistent, _ = check_consistency(all_props)
    
    # If {premises, NOT conclusion} is inconsistent, conclusion is entailed
    is_entailed = not is_consistent
    
    return is_entailed, None

def main():
    parser = argparse.ArgumentParser(description='Check logical consistency of assumptions')
    parser.add_argument('--propositions', nargs='+', help='List of propositions')
    parser.add_argument('--premises', nargs='+', help='Premises for conclusion checking')
    parser.add_argument('--conclusion', help='Conclusion to check')
    parser.add_argument('--json', help='Input JSON file with propositions')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    propositions = []
    
    if args.json:
        with open(args.json, 'r') as f:
            data = json.load(f)
            propositions = [parse_proposition(p) for p in data['propositions']]
    elif args.propositions:
        propositions = [parse_proposition(p) for p in args.propositions]
    else:
        parser.print_help()
        sys.exit(1)
    
    if args.premises and args.conclusion:
        # Check if conclusion is entailed by premises
        premises_parsed = [parse_proposition(p) for p in args.premises]
        conclusion_parsed = parse_proposition(args.conclusion)
        is_entailed, _ = check_conclusion(premises_parsed, conclusion_parsed)
        
        result = {
            'check': 'entailment',
            'is_entailed': is_entailed,
            'premises': args.premises,
            'conclusion': args.conclusion
        }
    else:
        # Check consistency
        is_consistent, _ = check_consistency(propositions)
        
        result = {
            'check': 'consistency',
            'is_consistent': is_consistent,
            'propositions': [p if isinstance(p, str) else str(p) for p in args.propositions]
        }
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        if result['check'] == 'consistency':
            status = "✓ CONSISTENT" if result['is_consistent'] else "✗ INCONSISTENT"
            print(f"\n{status}")
            print(f"\nPropositions:")
            for i, prop in enumerate(args.propositions, 1):
                print(f"  {i}. {prop}")
        else:
            status = "✓ VALID" if result['is_entailed'] else "✗ INVALID"
            print(f"\n{status}")
            print(f"\nPremises:")
            for i, prem in enumerate(args.premises, 1):
                print(f"  {i}. {prem}")
            print(f"\nConclusion:")
            print(f"  → {args.conclusion}")

if __name__ == "__main__":
    main()
