#!/usr/bin/env python3
"""解游客通道的 PoW 挑战，输出可直接使用的 nonce。

用法:
    python3 pow_solve.py <challenge> <difficulty>

说明:
    找最小的十进制 nonce，使 sha256(f"{challenge}{nonce}") 的前 difficulty 个 bit 全为 0。
    difficulty 一般为 16，耗时通常 <1 秒。
"""
from __future__ import annotations

import hashlib
import sys


def solve(challenge: str, difficulty: int) -> int:
    nonce = 0
    while True:
        digest = hashlib.sha256(f"{challenge}{nonce}".encode()).digest()
        full_bytes, remainder = divmod(difficulty, 8)
        if all(byte == 0 for byte in digest[:full_bytes]) and (
            remainder == 0 or digest[full_bytes] >> (8 - remainder) == 0
        ):
            return nonce
        nonce += 1


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python3 pow_solve.py <challenge> <difficulty>", file=sys.stderr)
        return 2
    print(solve(sys.argv[1], int(sys.argv[2])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
