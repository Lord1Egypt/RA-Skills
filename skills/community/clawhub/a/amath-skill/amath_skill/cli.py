from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from .client import client


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="amath API CLI for OpenClaw skill usage")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("health")

    tree = sub.add_parser("curriculum-tree")
    tree.add_argument("--system-name", default="奥数探险课")

    topic = sub.add_parser("topic")
    topic.add_argument("topic_id", type=int)

    guide = sub.add_parser("curriculum-guide")

    problem = sub.add_parser("problem")
    problem.add_argument("problem_id")

    recommended = sub.add_parser("recommended")
    recommended.add_argument("--limit", type=int, default=10)
    recommended.add_argument("--difficulty", type=int)
    recommended.add_argument("--problem-type")
    recommended.add_argument("--lecture")
    recommended.add_argument("--topic-id")
    recommended.add_argument("--token")

    login = sub.add_parser("login")
    login.add_argument("username")
    login.add_argument("password")

    chat_start = sub.add_parser("chat-start")
    chat_start.add_argument("user_id")
    chat_start.add_argument("--problem-id")
    chat_start.add_argument("--mode", default="LECTURE")

    chat_send = sub.add_parser("chat-send")
    chat_send.add_argument("session_id")
    chat_send.add_argument("message")
    chat_send.add_argument("--direct-submit", action="store_true")

    chat_hint = sub.add_parser("chat-hint")
    chat_hint.add_argument("session_id")

    quiz_start = sub.add_parser("quiz-start")
    quiz_start.add_argument("mode")
    quiz_start.add_argument("--topic-id")
    quiz_start.add_argument("--lecture")
    quiz_start.add_argument("--difficulty-min", type=int, default=1)
    quiz_start.add_argument("--difficulty-max", type=int, default=5)
    quiz_start.add_argument("--limit", type=int, default=10)
    quiz_start.add_argument("--time-limit", type=int, default=900)
    quiz_start.add_argument("--token")

    quiz_answer = sub.add_parser("quiz-answer")
    quiz_answer.add_argument("session_id")
    quiz_answer.add_argument("question_id")
    quiz_answer.add_argument("selected_option")
    quiz_answer.add_argument("--time-spent", type=int)
    quiz_answer.add_argument("--token")

    quiz_submit = sub.add_parser("quiz-submit")
    quiz_submit.add_argument("session_id")
    quiz_submit.add_argument("--time-used", type=int)
    quiz_submit.add_argument("--token")

    return parser


async def dispatch(args: argparse.Namespace) -> Any:
    if args.command == "health":
        return await client.request("GET", "/health")
    if args.command == "curriculum-tree":
        return await client.request("GET", f"/curriculum/system/name/{args.system_name}/tree")
    if args.command == "topic":
        return await client.request("GET", f"/curriculum/topic/{args.topic_id}")
    if args.command == "curriculum-guide":
        return await client.request("GET", "/knowledge/curriculum-guide")
    if args.command == "problem":
        return await client.request("GET", f"/question-bank/problems/{args.problem_id}")
    if args.command == "recommended":
        return await client.request(
            "GET",
            "/question-bank/recommended",
            params={
                "limit": args.limit,
                "difficulty": args.difficulty,
                "problem_type": args.problem_type,
                "lecture": args.lecture,
                "topic_id": args.topic_id,
            },
            token=args.token,
        )
    if args.command == "login":
        return await client.request("POST", "/auth/login", json_body={"username": args.username, "password": args.password})
    if args.command == "chat-start":
        return await client.request(
            "POST",
            "/chat/start",
            json_body={"user_id": args.user_id, "problem_id": args.problem_id, "mode": args.mode},
        )
    if args.command == "chat-send":
        return await client.request(
            "POST",
            "/chat/interact",
            json_body={"session_id": args.session_id, "user_input": args.message, "direct_submit": args.direct_submit},
        )
    if args.command == "chat-hint":
        return await client.request("POST", "/chat/hint", json_body={"session_id": args.session_id})
    if args.command == "quiz-start":
        return await client.request(
            "POST",
            "/quiz/start",
            json_body={
                "mode": args.mode,
                "topic_id": args.topic_id,
                "lecture": args.lecture,
                "difficulty_min": args.difficulty_min,
                "difficulty_max": args.difficulty_max,
                "limit": args.limit,
                "time_limit": args.time_limit,
            },
            token=args.token,
        )
    if args.command == "quiz-answer":
        return await client.request(
            "PATCH",
            "/quiz/answer",
            json_body={
                "session_id": args.session_id,
                "question_id": args.question_id,
                "selected_option": args.selected_option,
                "time_spent": args.time_spent,
            },
            token=args.token,
        )
    if args.command == "quiz-submit":
        return await client.request(
            "POST",
            "/quiz/submit",
            json_body={"session_id": args.session_id, "time_used": args.time_used},
            token=args.token,
        )
    raise SystemExit(f"Unsupported command: {args.command}")


async def amain() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        data = await dispatch(args)
        try:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except BrokenPipeError:
            try:
                sys.stdout.close()
            except OSError:
                pass
        return 0
    finally:
        await client.close()


def main() -> None:
    raise SystemExit(asyncio.run(amain()))


if __name__ == "__main__":
    main()
