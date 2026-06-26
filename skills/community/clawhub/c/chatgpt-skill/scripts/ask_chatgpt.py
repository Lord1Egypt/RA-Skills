#!/usr/bin/env python3
"""One-shot ChatGPT ask flow."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from patchright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_session import ChatGPTBrowserSession
from browser_utils import BrowserFactory
from errors import ChatGPTSkillError, result_from_exception
from session_manager import SessionManagerClient, SessionManagerError


def ask_once(
    question: str,
    *,
    conversation_id: str | None = None,
    show_browser: bool = False,
    model: str | None = None,
    extended_thinking: bool = False,
    new_chat: bool = False,
    proof_screenshot: bool = False,
):
    auth = AuthManager()
    validation = auth.validate_auth(headless=not show_browser and BrowserFactory.recommended_headless(default=True))
    if not validation.get("authenticated"):
        raise ChatGPTSkillError(
            "not_logged_in",
            "ChatGPT is not authenticated. Run auth_manager.py setup first.",
            details={"validation": validation},
        )

    playwright = None
    context = None
    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=not show_browser and BrowserFactory.recommended_headless(default=True),
        )
        session = ChatGPTBrowserSession("oneshot", context, conversation_id=conversation_id)
        return session.ask(
            question,
            model=model,
            extended_thinking=extended_thinking,
            new_chat=new_chat,
            proof_screenshot=proof_screenshot,
        )
    finally:
        if context:
            try:
                context.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask ChatGPT through the web UI")
    parser.add_argument("--question", required=True)
    parser.add_argument("--conversation-id")
    parser.add_argument("--session-id")
    parser.add_argument("--show-browser", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--extended-thinking", action="store_true")
    parser.add_argument("--new-chat", action="store_true")
    parser.add_argument("--proof-screenshot", action="store_true")
    args = parser.parse_args()

    try:
        if args.session_id:
            client = SessionManagerClient()
            payload = client.request(
                "ask",
                session_id=args.session_id,
                question=args.question,
                model=args.model,
                extended_thinking=args.extended_thinking,
                new_chat=args.new_chat,
                proof_screenshot=args.proof_screenshot,
            )
        else:
            payload = ask_once(
                args.question,
                conversation_id=args.conversation_id,
                show_browser=args.show_browser,
                model=args.model,
                extended_thinking=args.extended_thinking,
                new_chat=args.new_chat,
                proof_screenshot=args.proof_screenshot,
            )
    except SessionManagerError as error:
        payload = error.to_result()
    except Exception as error:
        payload = result_from_exception(error)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
