---
name: integer-calculator
description: Calculate addition, subtraction, multiplication and division of two integers via a Python script.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🧮"
---

# Integer Calculator

This skill calculates the addition, subtraction, multiplication or division of two integers by calling a local Python script.

## Usage

When the user asks to perform arithmetic on two integers, run the following command:

```bash
python3 scripts/calculator.py   
```

### Parameters

| Parameter   | Type   | Required | Description                          |
|-------------|--------|----------|--------------------------------------|
| num1        | int    | Yes      | First integer                        |
| num2        | int    | Yes      | Second integer                       |
| operation   | string | Yes      | `add`, `sub`, `mul`, `div`           |

### Examples

**Addition:**
```bash
python3 scripts/calculator.py 3 5 add
# Output: 8
```

**Subtraction:**
```bash
python3 scripts/calculator.py 10 4 sub
# Output: 6
```

**Multiplication:**
```bash
python3 scripts/calculator.py 3 5 mul
# Output: 15
```

**Division:**
```bash
python3 scripts/calculator.py 10 4 div
# Output: 2.5
```

## Notes

- Supported operations: `add`, `sub`, `mul`, `div`.
- Both inputs must be valid integers.
- Division returns a float result; dividing by zero will return an error message to stderr and exit with code 1.
- The script prints only the numeric result to stdout for easy parsing.

