#!/usr/bin/env python3
"""解游客通道的 PoW 挑战，输出可直接使用的 nonce。

用法:
    python3 pow_solve.py <challenge> <difficulty> [--max-seconds N] [--max-difficulty N] [--max-iterations N]

说明:
    找最小的十进制 nonce，使 sha256(f"{challenge}{nonce}") 的前 difficulty 个 bit 全为 0。
    difficulty 一般为 16，耗时通常 <1 秒。

安全护栏（challenge / difficulty 来自远端响应，一律按不可信输入校验）:
    - difficulty 必须是整数且落在 0 ~ --max-difficulty（默认 20）之间：
      超出上限即非 0 退出 —— 被篡改或异常的难度值不会把本机拖成无限占用 CPU；
    - challenge 只接受 1~512 个 [A-Za-z0-9._~+/=-] 字符，其余一律拒绝；
    - 求解带**时间上限**（--max-seconds，默认 30 秒）与**迭代上限**（--max-iterations，
      默认按难度推算），任一触顶即非 0 退出且不输出 nonce —— 调用方据此报错，
      而不是让本进程一直跑下去（curl 的 --max-time 只约束 HTTP，不约束求解）。

退出码:
    0 成功（stdout 只有 nonce）
    2 参数或难度非法
    3 触达时间 / 迭代上限（未解出）
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time

MAX_DIFFICULTY = 20
MAX_CHALLENGE_LEN = 512
DEFAULT_MAX_SECONDS = 30.0
# 时间检查的间隔（每 N 次哈希查一次表，避免把开销压在循环里）
CHECK_EVERY = 4096
CHALLENGE_OK = re.compile(r"^[A-Za-z0-9._~+/=-]{1,%d}$" % MAX_CHALLENGE_LEN)


class PowLimitExceeded(RuntimeError):
    """触达时间或迭代上限（未能解出）。"""


def default_max_iterations(difficulty: int) -> int:
    """按难度推算迭代上限：期望工作量 2**difficulty 的 256 倍（再兜 2**31）。"""
    return min(1 << (difficulty + 8), 1 << 31)


def solve(
    challenge: str,
    difficulty: int,
    *,
    max_iterations: int,
    max_seconds: float = DEFAULT_MAX_SECONDS,
    clock=time.monotonic,
) -> int:
    """返回最小 nonce；触顶抛 PowLimitExceeded。"""
    deadline = clock() + max_seconds
    full_bytes, remainder = divmod(difficulty, 8)
    nonce = 0
    while True:
        digest = hashlib.sha256(f"{challenge}{nonce}".encode()).digest()
        if all(byte == 0 for byte in digest[:full_bytes]) and (
            remainder == 0 or digest[full_bytes] >> (8 - remainder) == 0
        ):
            return nonce
        if nonce >= max_iterations:
            raise PowLimitExceeded(f"迭代达上限 {max_iterations}")
        nonce += 1
        if nonce % CHECK_EVERY == 0 and clock() >= deadline:
            raise PowLimitExceeded(f"运行时间达上限 {max_seconds:g}s")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pow_solve.py",
        description="解游客通道 PoW 挑战（challenge / difficulty 来自远端响应，按不可信输入校验）",
    )
    parser.add_argument("challenge", help="一次性挑战串（取自 challenge 接口）")
    parser.add_argument("difficulty", help="前导 0 bit 数（取自 challenge 接口）")
    parser.add_argument(
        "--max-difficulty",
        type=int,
        default=MAX_DIFFICULTY,
        help=f"允许的最大难度 bit（默认 {MAX_DIFFICULTY}；超出即拒绝，不做求解）",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=DEFAULT_MAX_SECONDS,
        help=f"求解时间上限（秒，默认 {DEFAULT_MAX_SECONDS:g}）",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="迭代上限（默认 0 = 按难度推算）",
    )
    args = parser.parse_args(argv)

    if not CHALLENGE_OK.match(args.challenge):
        print(
            f"挑战串不合法（只接受 1~{MAX_CHALLENGE_LEN} 个 [A-Za-z0-9._~+/=-] 字符）",
            file=sys.stderr,
        )
        return 2

    try:
        difficulty = int(args.difficulty)
    except ValueError:
        print(f"难度值不是整数: {args.difficulty!r}", file=sys.stderr)
        return 2
    if args.max_difficulty < 0 or difficulty < 0 or difficulty > args.max_difficulty:
        print(
            f"难度值 {difficulty} bit 超出允许范围 0~{args.max_difficulty} bit，"
            "已中止（不给异常难度值留出长时间占用 CPU 的机会）",
            file=sys.stderr,
        )
        return 2

    max_iterations = args.max_iterations or default_max_iterations(difficulty)
    if max_iterations <= 0 or args.max_seconds <= 0:
        print("时间 / 迭代上限必须为正数", file=sys.stderr)
        return 2

    try:
        nonce = solve(
            args.challenge,
            difficulty,
            max_iterations=max_iterations,
            max_seconds=args.max_seconds,
        )
    except PowLimitExceeded as exc:
        print(
            f"未在限制内解出挑战（{exc}）；请核对 challenge 接口返回的难度是否异常",
            file=sys.stderr,
        )
        return 3
    print(nonce)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
