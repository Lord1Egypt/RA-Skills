#!/usr/bin/env python3
"""Text chat client supporting multi-turn conversation."""

import argparse
import html
from typing import Any, Dict

from client_common import has_error, load_env_file, load_session, post_json, print_json, require_env


def text_to_html_payload(text: str) -> str:
    """Convert plain text to safe paragraph-based HTML payload.

    功能:
        对文本做 HTML 转义，并将换行转换为 <br/>，外层包裹 <p> 标签。

    输入:
        text: 用户输入的纯文本。

    输出:
        可用于接口请求的 HTML 字符串。
    """
    escaped = html.escape(text)
    return f"<p>{escaped.replace(chr(10), '<br/>')}</p>"


def send_message(
    user_id: str,
    session_id: str,
    text: str,
    stream: bool = False,
    trace_id: str = "",
) -> Dict[str, Any]:
    """Send one message to the session message API.

    功能:
        构造消息请求并调用消息接口，支持可选流式与 trace 元数据。

    输入:
        user_id: 用户 ID。
        session_id: 会话 ID。
        text: 发送的文本内容。
        stream: 是否流式返回。
        trace_id: 可选链路追踪 ID。

    输出:
        消息接口响应字典；失败时通常包含 error 字段。
    """
    api_base_url = require_env("API_BASE_URL").rstrip("/")
    token = require_env("CLAWHUB_SKILL_TOKEN")

    payload: Dict[str, Any] = {
        "user_id": user_id,
        "session_id": session_id,
        "html_payload": text_to_html_payload(text),
        "stream": stream,
    }
    if trace_id:
        payload["metadata"] = {"trace_id": trace_id, "source": "clawhub_client"}

    url = f"{api_base_url}/session/message"
    return post_json(url, payload, token=token)


def run_multi_turn(user_id: str, session_id: str, stream: bool, trace_id: str) -> None:
    """Run an interactive multi-turn chat loop.

    功能:
        持续读取终端输入并调用 send_message，直到用户输入退出指令。

    输入:
        user_id: 用户 ID。
        session_id: 会话 ID。
        stream: 是否流式返回。
        trace_id: 可选追踪 ID。

    输出:
        无显式返回值；将对话结果打印到标准输出，接口错误时退出。
    """
    print("Multi-turn chat started. Type /exit to stop.")
    while True:
        text = input("You: ").strip()
        if not text:
            continue
        if text.lower() in {"/exit", "exit", "quit", "/quit"}:
            print("Chat ended.")
            break

        result = send_message(user_id, session_id, text, stream=stream, trace_id=trace_id)
        if has_error(result):
            print_json(result)
            raise SystemExit(1)
        answer = result.get("answer_text") or result.get("answer_html") or ""
        if answer:
            print(f"Bot: {answer}")
        else:
            print_json(result)


def main() -> None:
    """CLI entrypoint for single-turn or multi-turn chat.

    功能:
        解析参数，加载会话信息，并执行单轮或多轮消息发送。

    输入:
        命令行参数中的 env、text、stream、trace_id、session_file、user_id、session_id、multi_turn。

    输出:
        无显式返回值；打印聊天响应 JSON 或文本，失败时抛出 SystemExit。
    """
    parser = argparse.ArgumentParser(description="Send text message to skill and chat multi-turn")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--text", default="", help="Single-turn text input")
    parser.add_argument("--stream", action="store_true", help="Enable stream mode")
    parser.add_argument("--trace-id", default="")
    parser.add_argument(
        "--session-file",
        default=".session.json",
        help="Read user_id/session_id from this file, default: .session.json",
    )
    parser.add_argument("--user-id", default="", help="Optional override user id")
    parser.add_argument("--session-id", default="", help="Optional override session id")
    parser.add_argument("--multi-turn", action="store_true", help="Interactive multi-turn mode")
    args = parser.parse_args()

    load_env_file(args.env)

    session = load_session(args.session_file)
    user_id = args.user_id or session.get("user_id", "")
    session_id = args.session_id or session.get("session_id", "")

    if not user_id or not session_id:
        raise SystemExit("[ERROR] Missing user_id/session_id. Run login_client.py first or pass --user-id and --session-id.")

    if args.multi_turn or not args.text:
        run_multi_turn(user_id, session_id, args.stream, args.trace_id)
        return

    result = send_message(user_id, session_id, args.text, stream=args.stream, trace_id=args.trace_id)
    print_json(result)
    if has_error(result):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
