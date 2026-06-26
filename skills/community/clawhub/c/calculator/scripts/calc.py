#!/usr/bin/env python3
"""
Calculator script for accurate mathematical operations.
Supports: basic arithmetic, percentages, powers, roots, trigonometry, logarithms, etc.
"""

import math
import sys
import re

def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result."""
    # Clean up the expression
    expr = expression.strip()
    
    # Define safe operations
    safe_dict = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'pow': pow,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'log': math.log10,
        'ln': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
        'floor': math.floor,
        'ceil': math.ceil,
    }
    
    # Replace common operators
    expr = expr.replace('^', '**')
    expr = expr.replace('×', '*')
    expr = expr.replace('÷', '/')
    expr = expr.replace('％', '%')
    
    # Handle percentages: "100 * 15%" -> "100 * 0.15"
    # Match patterns like "100 * 15%" or "100*15%"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)\s*%', r'(\1 * \2 / 100)', expr)
    
    # Handle implicit multiplication: 2(3) -> 2*(3)
    expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
    expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
    expr = re.sub(r'(\))(\()', r'\1*\2', expr)
    
    try:
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        
        # Format result nicely
        if isinstance(result, float):
            # Avoid floating point precision issues
            if result.is_integer():
                return str(int(result))
            # Round to reasonable precision
            rounded = round(result, 10)
            return str(rounded).rstrip('0').rstrip('.')
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: calculator.py '<expression>'")
        print("Examples:")
        print("  calculator.py '2 + 3'           # 5")
        print("  calculator.py '10 * 5'          # 50")
        print("  calculator.py '2^10'             # 1024")
        print("  calculator.py 'sqrt(16)'         # 4")
        print("  calculator.py 'sin(pi/2)'        # 1")
        print("  calculator.py '100 * 15%'         # 15")
        sys.exit(1)
    
    expression = ' '.join(sys.argv[1:])
    result = calculate(expression)
    print(result)


if __name__ == "__main__":
    main()
