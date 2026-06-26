#!/usr/bin/env python3
"""Authentication manager for ChatGPT Web."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict

from patchright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))

from browser_utils import BrowserFactory, classify_page, ensure_chat_ready, goto_and_classify, wait_for_app_ready
from config import AUTH_INFO_FILE, BROWSER_STATE_DIR, DATA_DIR, LOGIN_TIMEOUT_MINUTES, STATE_FILE, UI_LONG_TIMEOUT_MS
from errors import ChatGPTSkillError, result_from_exception
from storage import AuthInfoStore, utcnow_iso


class AuthManager:
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        BROWSER_STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.auth_store = AuthInfoStore()

    def is_authenticated(self) -> bool:
        return STATE_FILE.exists()

    def get_status(self) -> Dict[str, Any]:
        info = self.auth_store.load()
        state_exists = STATE_FILE.exists()
        status = {
            "status": "success",
            "state_exists": state_exists,
            "state_file": str(STATE_FILE),
            "auth_info_file": str(AUTH_INFO_FILE),
            "last_auth": info.get("authenticated_at"),
            "last_validation": info.get("last_validation"),
            "last_validation_status": info.get("last_validation_status"),
            "last_url": info.get("last_url"),
        }
        return status

    def _save_browser_state(self, context):
        context.storage_state(path=str(STATE_FILE))

    def _save_auth_info(self, **extra: Any):
        payload = self.auth_store.load()
        payload.update(extra)
        self.auth_store.save(payload)

    def validate_auth(self, *, headless: bool = True) -> Dict[str, Any]:
        playwright = None
        context = None
        page = None
        try:
            playwright = sync_playwright().start()
            context = BrowserFactory.launch_persistent_context(
                playwright,
                headless=headless,
            )
            page = context.new_page()
            classification = goto_and_classify(page, "https://chatgpt.com")
            if classification["status"] == "page_structure_changed":
                classification = wait_for_app_ready(page, timeout_ms=UI_LONG_TIMEOUT_MS)
            result = {
                "status": "success" if classification["status"] == "chat_ready" else "error",
                "authenticated": classification["status"] == "chat_ready",
                "validation_status": classification["status"],
                "final_url": classification.get("final_url"),
            }
            if classification["status"] == "chat_ready":
                self._save_browser_state(context)
            self._save_auth_info(
                last_validation=utcnow_iso(),
                last_validation_status=classification["status"],
                last_url=classification.get("final_url"),
            )
            return result
        except Exception as error:
            return result_from_exception(error)
        finally:
            if page:
                try:
                    page.close()
                except Exception:
                    pass
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

    def setup_auth(self, timeout_minutes: float = LOGIN_TIMEOUT_MINUTES) -> Dict[str, Any]:
        playwright = None
        context = None
        page = None
        try:
            playwright = sync_playwright().start()
            context = BrowserFactory.launch_persistent_context(playwright, headless=False)
            page = context.new_page()
            last_classification = goto_and_classify(page, "https://chatgpt.com")

            deadline = time.time() + timeout_minutes * 60
            while time.time() < deadline:
                last_classification = classify_page(page)
                if last_classification["status"] == "chat_ready":
                    ensure_chat_ready(page, timeout_ms=UI_LONG_TIMEOUT_MS)
                    self._save_browser_state(context)
                    self._save_auth_info(
                        authenticated_at=utcnow_iso(),
                        last_validation=utcnow_iso(),
                        last_validation_status="chat_ready",
                        last_url=page.url,
                    )
                    return {
                        "status": "success",
                        "authenticated": True,
                        "validation_status": "chat_ready",
                        "final_url": page.url,
                    }
                time.sleep(2)

            raise ChatGPTSkillError(
                "auth_timeout",
                "Timed out waiting for manual ChatGPT login to complete",
                details={
                    "last_seen_status": last_classification.get("status"),
                    "final_url": last_classification.get("final_url"),
                },
            )
        except Exception as error:
            return result_from_exception(error)
        finally:
            if page:
                try:
                    page.close()
                except Exception:
                    pass
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

    def logout(self) -> Dict[str, Any]:
        try:
            if STATE_FILE.exists():
                STATE_FILE.unlink()
            if AUTH_INFO_FILE.exists():
                AUTH_INFO_FILE.unlink()
            if BROWSER_STATE_DIR.exists():
                shutil.rmtree(BROWSER_STATE_DIR)
            BROWSER_STATE_DIR.mkdir(parents=True, exist_ok=True)
            self.auth_store.save({})
            return {"status": "success", "logged_out": True}
        except Exception as error:
            return result_from_exception(error)


def print_json(payload: Dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") == "success" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage ChatGPT authentication")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status")
    subparsers.add_parser("validate")
    setup_parser = subparsers.add_parser("setup")
    setup_parser.add_argument("--timeout", type=float, default=LOGIN_TIMEOUT_MINUTES)
    subparsers.add_parser("logout")

    args = parser.parse_args()
    manager = AuthManager()

    if args.command == "status":
        return print_json(manager.get_status())
    if args.command == "validate":
        return print_json(manager.validate_auth(headless=BrowserFactory.recommended_headless(default=True)))
    if args.command == "setup":
        return print_json(manager.setup_auth(timeout_minutes=args.timeout))
    if args.command == "logout":
        return print_json(manager.logout())

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
