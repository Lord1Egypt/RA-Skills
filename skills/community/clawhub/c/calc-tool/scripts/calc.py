#!/usr/bin/env python3
"""Calc Tool - Calculator."""

import argparse
import math
import sys
import re


def evaluate(expr: str, precision: int = 6) -> float:
    """Evaluate mathematical expression."""
    # Replace constants
    expr = expr.replace('pi', str(math.pi))
    expr = expr.replace('e', str(math.e))
    
    # Replace functions
    expr = re.sub(r'sqrt\(', 'math.sqrt(', expr)
    expr = re.sub(r'sin\(', 'math.sin(', expr)
    expr = re.sub(r'cos\(', 'math.cos(', expr)
    expr = re.sub(r'tan\(', 'math.tan(', expr)
    expr = re.sub(r'log\(', 'math.log10(', expr)
    expr = re.sub(r'ln\(', 'math.log(', expr)
    expr = re.sub(r'abs\(', 'math.fabs(', expr)
    expr = re.sub(r'round\(', 'round(', expr)
    expr = re.sub(r'floor\(', 'math.floor(', expr)
    expr = re.sub(r'ceil\(', 'math.ceil(', expr)
    expr = re.sub(r'pow\(', 'math.pow(', expr)
    
    # Replace ^ with **
    expr = expr.replace('^', '**')
    
    try:
        result = eval(expr)
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


def main():
    parser = argparse.ArgumentParser(description='Calculator')
    parser.add_argument('expression', help='Mathematical expression')
    parser.add_argument('-p', '--precision', type=int, default=6, help='Decimal precision')
    
    args = parser.parse_args()
    
    try:
        result = evaluate(args.expression, args.precision)
        
        # Format output
        if isinstance(result, float):
            if result == int(result):
                print(int(result))
            else:
                print(f"{result:.{args.precision}f}".rstrip('0').rstrip('.'))
        else:
            print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
