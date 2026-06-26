#!/usr/bin/env python3
"""Conversation metadata manager for ChatGPT Web."""

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
from storage import ConversationStore


class ChatManager:
    def __init__(self):
        self.store = ConversationStore()

    def list(self):
        return {
            "status": "success",
            "count": len(self.store.list()),
            "current": self.store.current(),
            "conversations": self.store.list(),
        }

    def current(self):
        current = self.store.current()
        if not current:
            return {"status": "success", "current": None}
        return {"status": "success", "current": current}

    def new(self, *, show_browser: bool = False):
        auth = AuthManager()
        validation = auth.validate_auth(headless=not show_browser and BrowserFactory.recommended_headless(default=True))
        if not validation.get("authenticated"):
            raise ChatGPTSkillError("not_logged_in", "ChatGPT is not authenticated", details={"validation": validation})

        playwright = None
        context = None
        try:
            playwright = sync_playwright().start()
            context = BrowserFactory.launch_persistent_context(
                playwright,
                headless=not show_browser and BrowserFactory.recommended_headless(default=True),
            )
            session = ChatGPTBrowserSession("chat-manager", context)
            payload = session.new_chat()
            return payload
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

    def open(self, conversation_id: str, *, show_browser: bool = False):
        auth = AuthManager()
        validation = auth.validate_auth(headless=not show_browser and BrowserFactory.recommended_headless(default=True))
        if not validation.get("authenticated"):
            raise ChatGPTSkillError("not_logged_in", "ChatGPT is not authenticated", details={"validation": validation})

        playwright = None
        context = None
        try:
            playwright = sync_playwright().start()
            context = BrowserFactory.launch_persistent_context(
                playwright,
                headless=not show_browser and BrowserFactory.recommended_headless(default=True),
            )
            session = ChatGPTBrowserSession("chat-manager", context, conversation_id=conversation_id)
            return {
                "status": "success",
                "conversation_id": session.conversation_id,
                "final_url": session.page.url if session.page else None,
            }
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

    def delete(self, conversation_id: str):
        raise ChatGPTSkillError(
            "not_implemented",
            "Conversation deletion is not implemented because the ChatGPT Web delete flow is not stable enough yet",
            details={"conversation_id": conversation_id},
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage ChatGPT conversations")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list")
    subparsers.add_parser("current")
    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("--show-browser", action="store_true")
    open_parser = subparsers.add_parser("open")
    open_parser.add_argument("--conversation-id", required=True)
    open_parser.add_argument("--show-browser", action="store_true")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--conversation-id", required=True)

    args = parser.parse_args()
    manager = ChatManager()

    try:
        if args.command == "list":
            payload = manager.list()
        elif args.command == "current":
            payload = manager.current()
        elif args.command == "new":
            payload = manager.new(show_browser=args.show_browser)
        elif args.command == "open":
            payload = manager.open(args.conversation_id, show_browser=args.show_browser)
        elif args.command == "delete":
            payload = manager.delete(args.conversation_id)
        else:
            parser.print_help()
            return 1
    except Exception as error:
        payload = result_from_exception(error)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
