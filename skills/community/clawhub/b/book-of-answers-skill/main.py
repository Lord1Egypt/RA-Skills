#!/usr/bin/env python3
from __future__ import annotations

import argparse

from service import WELCOME_MESSAGE, handle_request, normalize_text


def run_interactive_session(user_id: str) -> None:
    print(WELCOME_MESSAGE)
    while True:
        try:
            message = input("> ").strip()
        except EOFError:
            print()
            break
        if message.lower() in {"exit", "quit"}:
            break
        print(handle_request(user_id, message))
        print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="答案之书.skill 文本技能入口")
    parser.add_argument("message", nargs="*", help="要发送给答案之书.skill 的消息")
    parser.add_argument("--user-id", default="demo-user", help="用于持久化状态的用户标识")
    parser.add_argument("--interactive", action="store_true", help="进入本地 REPL 交互模式")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.interactive:
        run_interactive_session(args.user_id)
        return

    message = normalize_text(" ".join(args.message))
    print(handle_request(args.user_id, message))


if __name__ == "__main__":
    main()
