#!/usr/bin/env python3
import sys

def estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / 3.6))

if __name__ == '__main__':
    text = sys.stdin.read()
    print(estimate_tokens(text))
