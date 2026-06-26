---
name: calculator
description: |
  Accurate mathematical calculations. Use when user needs to compute: (1) Basic arithmetic (+, -, *, /), 
  (2) Powers and roots (^, sqrt), (3) Percentages, (4) Trigonometry (sin, cos, tan), 
  (5) Logarithms (log, ln), (6) Complex expressions, (7) Unit conversions.
---

# Calculator Skill

Perform accurate mathematical calculations using the `calc.py` script.

## Usage

Run calculations directly with Python:

```bash
python3 <skill-path>/scripts/calc.py "<expression>"
```

## Supported Operations

### Basic Arithmetic
- `+` Addition: `2 + 3` → 5
- `-` Subtraction: `10 - 4` → 6
- `*` Multiplication: `6 * 7` → 42
- `/` Division: `15 / 3` → 5

### Powers & Roots
- `^` or `**` Power: `2^10` → 1024
- `sqrt()` Square root: `sqrt(16)` → 4

### Percentages
- `100 * 15%` → 15 (15% of 100)
- `50 + 50 * 10%` → 55 (add 10%)

### Trigonometry (radians)
- `sin(pi/2)` → 1
- `cos(pi)` → -1
- `tan(pi/4)` → 1

### Logarithms
- `log(100)` → 2 (base 10)
- `ln(e)` → 1 (natural log)

### Constants
- `pi` → 3.141592653589793
- `e` → 2.718281828459045

### Other Functions
- `abs(-5)` → 5
- `round(3.7)` → 4
- `floor(3.9)` → 3
- `ceil(3.1)` → 4
- `pow(2, 8)` → 256

## Examples

```bash
python3 scripts/calc.py "2 + 3 * 4"        # 14
python3 scripts/calc.py "(2 + 3) * 4"       # 20
python3 scripts/calc.py "sqrt(144)"         # 12
python3 scripts/calc.py "2^8"               # 256
python3 scripts/calc.py "1000 * 5%"         # 50
python3 scripts/calc.py "sin(0)"            # 0
python3 scripts/calc.py "log(1000)"         # 3
```

## Notes

- Implicit multiplication supported: `2(3)` = `2*3`
- Use parentheses for grouping
- Float results are rounded to 10 decimal places to avoid precision issues
