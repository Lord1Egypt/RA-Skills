---
slug: cn-math-expression
name: Cn Math Expression
version: "1.0.0"
description: "cn math expression"
keywords: tool, utility
license: MIT-0
tags:
  - tools
---


# Math Expression Evaluator

Safely evaluate mathematical expressions with support for common functions.

## Features

- Safe evaluation (no arbitrary code execution)
- Common mathematical functions: sqrt, sin, cos, tan, log
- Constants: pi, e
- Basic arithmetic: +, -, *, /, **, %
- Pure Python, no external dependencies

## Supported Functions

| Function | Description | Example |
|----------|-------------|---------|
| sqrt(x) | Square root | sqrt(144) = 12 |
| sin(x) | Sine (radians) | sin(pi/2) = 1 |
| cos(x) | Cosine (radians) | cos(0) = 1 |
| tan(x) | Tangent (radians) | tan(pi/4) = 1 |
| log(x) | Natural log | log(e) = 1 |
| log10(x) | Base 10 log | log10(100) = 2 |
| abs(x) | Absolute value | abs(-5) = 5 |
| pow(x,y) | Power | pow(2,8) = 256 |

## Supported Constants

- `pi` = 3.141592653589793
- `e` = 2.718281828459045

## Usage Examples

```bash
# Basic arithmetic
python3 scripts/math_eval.py --expr "2 + 3 * 4"
# Result: 14

# Using functions
python3 scripts/math_eval.py --expr "sqrt(144) + pow(2, 10)"
# Result: 1028.0

# Constants
python3 scripts/math_eval.py --expr "2 * pi * 10"
# Result: 62.8318...

# Complex expression
python3 scripts/math_eval.py --expr "log(pow(e, 5)) + sqrt(81)"
# Result: 14.0
```

## Safety

The evaluator uses Python's `eval()` with a restricted namespace. Only mathematical functions and constants are available. No imports, no file access, no system commands.

## Error Handling

If the expression is invalid or contains unsafe operations:
```json
{"error": "name 'os' is not defined"}
```

Exit code 1 on error.

## Technical Details

- Language: Python 3
- Dependencies: None (standard library only)
- License: MIT-0

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
