#!/usr/bin/env python3
"""Generate Fibonacci sequences."""

def fibonacci(n):
    """Generate the first n numbers of the Fibonacci sequence."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    return sequence

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    result = fibonacci(n)
    print(f"First {n} Fibonacci numbers:")
    print(", ".join(map(str, result)))
