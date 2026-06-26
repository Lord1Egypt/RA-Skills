---
name: fibonacci-generator
description: Generate and work with Fibonacci sequences and related number sequences. Use when users need Fibonacci numbers, calculate Fibonacci sequences, find nth Fibonacci numbers, check Fibonacci properties, or work with golden ratios and related mathematical sequences.
---

# Fibonacci Sequence Generator

Generate Fibonacci sequences and work with Fibonacci numbers, golden ratios, and related mathematical concepts.

## Quick Start

### Basic Usage

The Fibonacci sequence starts with 0, 1, and each subsequent number is the sum of the two preceding ones.

**First 10 Fibonacci numbers:** 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

### Generate First N Numbers

```python
def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq
```

## Common Operations

### Nth Fibonacci Number (0-indexed)
```python
def nth_fibonacci(n):
    """Get the nth Fibonacci number (0-indexed)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### Check if Number is Fibonacci
```python
import math

def is_fibonacci(x):
    """Check if x is a Fibonacci number."""
    def is_perfect_square(n):
        s = int(math.sqrt(n))
        return s * s == n
    return is_perfect_square(5 * x * x + 4) or is_perfect_square(5 * x * x - 4)
```

### Golden Ratio Approximation
As n increases, the ratio F(n+1)/F(n) approaches the golden ratio φ ≈ 1.618033988749895

## Related Sequences

### Lucas Numbers
Similar to Fibonacci but starts with 2, 1

### Tribonacci
Each number is sum of previous three

### Fibonacci Sum
Sum of first n Fibonacci numbers = F(n+2) - 1
