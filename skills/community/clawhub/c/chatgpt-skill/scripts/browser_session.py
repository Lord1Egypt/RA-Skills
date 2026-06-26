#!/usr/bin/env python3
"""Persistent browser conversation page for ChatGPT Web."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from patchright.sync_api import BrowserContext, Locator

import sys

sys.path.insert(0, str(Path(__file__).parent))

from browser_utils import (
    StealthUtils,
    conversation_url,
    ensure_chat_ready,
    extract_conversation_state,
    is_url_addressable_conversation_id,
    normalize_chatgpt_url,
    read_page_text,
    take_debug_screenshot,
    wait_for_any,
)
from config import (
    ASSISTANT_MESSAGE_SELECTORS,
    CHATGPT_BASE_URL,
    COMPOSER_SELECTORS,
    EXTENDED_THINKING_SELECTORS,
    MODEL_MENU_ITEM_SELECTORS,
    MODEL_PICKER_SELECTORS,
    NEW_CHAT_SELECTORS,
    NON_CRITICAL_OVERLAY_SELECTORS,
    RESPONSE_ERROR_TEXT_HINTS,
    RESPONSE_TIMEOUT_SECONDS,
    RETRY_BUTTON_SELECTORS,
    SEND_BUTTON_SELECTORS,
    STOP_BUTTON_SELECTORS,
    UI_LONG_TIMEOUT_MS,
    UI_MEDIUM_TIMEOUT_MS,
    USER_MESSAGE_SELECTORS,
)
from errors import ChatGPTSkillError
from storage import ConversationStore


MODEL_PRESETS = {
    "gpt-5.3-instant": {
        "label": "ChatGPT 5.3 Instant",
        "match_terms": ("5.3", "instant"),
    },
    "gpt-5.4-thinking": {
        "label": "ChatGPT 5.4 Thinking",
        "match_terms": ("5.4", "thinking"),
    },
    "gpt-5.4-pro": {
        "label": "ChatGPT 5.4 Pro",
        "match_terms": ("5.4", "pro"),
    },
}


def normalize_ui_text(text: Optional[str]) -> str:
    return " ".join((text or "").split()).strip().lower()


class ChatGPTBrowserSession:
    def __init__(
        self,
        session_id: str,
        context: BrowserContext,
        conversation_id: Optional[str] = None,
    ):
        self.id = session_id
        self.context = context
        self.page = None
        self.created_at = time.time()
        self.created_at_iso = None
        self.last_activity = self.created_at
        self.message_count = 0
        self.conversation_id = conversation_id
        self.conversation_id_source: Optional[str] = None
        self.stealth = StealthUtils()
        self.conversations = ConversationStore()
        self._initialize(conversation_id)

    def _goto(self, target_url: str):
        normalized_url = normalize_chatgpt_url(target_url)
        last_error = None
        for attempt in range(1, 4):
            try:
                self.page.goto(normalized_url, wait_until="domcontentloaded")
                return
            except Exception as error:
                last_error = error
                if attempt < 3:
                    time.sleep(attempt)
                    continue
        raise ChatGPTSkillError(
            "network_error",
            "Failed to load ChatGPT page",
            details={"cause": str(last_error), "target_url": normalized_url, "attempts": 3},
        ) from last_error

    def _initialize(self, conversation_id: Optional[str]):
        self.page = self.context.new_page()
        target_url = conversation_url(conversation_id) if is_url_addressable_conversation_id(conversation_id) else CHATGPT_BASE_URL
        self._goto(target_url)
        self._ensure_ready()
        self._sync_current_conversation()

    def _dismiss_non_critical_overlays(self):
        if not self.page:
            return
        try:
            self.page.keyboard.press("Escape")
        except Exception:
            pass
        for selector in NON_CRITICAL_OVERLAY_SELECTORS:
            try:
                locator = self.page.locator(selector).first
                if locator.count() == 0 or not locator.is_visible(timeout=250):
                    continue
                locator.evaluate("el => el.remove()")
            except Exception:
                continue

    def _ensure_ready(self):
        self._dismiss_non_critical_overlays()
        try:
            ensure_chat_ready(self.page, timeout_ms=UI_LONG_TIMEOUT_MS)
        except ChatGPTSkillError as error:
            screenshot_path = take_debug_screenshot(self.page, f"session-{self.id}")
            if screenshot_path:
                error.details.setdefault("screenshot", screenshot_path)
            raise
        self._dismiss_non_critical_overlays()

    def _sync_current_conversation(self):
        state = extract_conversation_state(self.page)
        self.conversation_id = state.get("conversation_id")
        self.conversation_id_source = state.get("source")
        self.conversations.upsert(
            conversation_id=self.conversation_id,
            conversation_id_source=self.conversation_id_source,
            final_url=self.page.url,
            status="ready",
        )

    def _snapshot_latest_message(self, selectors) -> Optional[str]:
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count == 0:
                    continue
                text = locator.nth(count - 1).inner_text(timeout=1000).strip()
                if text:
                    return text
            except Exception:
                continue
        return None

    def _snapshot_latest_answer(self) -> Optional[str]:
        return self._snapshot_latest_message(ASSISTANT_MESSAGE_SELECTORS)

    def _snapshot_latest_user_message(self) -> Optional[str]:
        return self._snapshot_latest_message(USER_MESSAGE_SELECTORS)

    def _is_generating(self) -> bool:
        return wait_for_any(self.page, STOP_BUTTON_SELECTORS, timeout_ms=800) is not None

    def _detect_response_error(self) -> Optional[str]:
        latest_answer = self._snapshot_latest_answer()
        if latest_answer:
            lower_answer = latest_answer.lower()
            for hint in RESPONSE_ERROR_TEXT_HINTS:
                if hint in lower_answer:
                    return latest_answer
        body_text = read_page_text(self.page, max_chars=16000)
        for hint in RESPONSE_ERROR_TEXT_HINTS:
            if hint in body_text:
                return hint
        return None

    def _click_retry_button(self) -> bool:
        selector = wait_for_any(self.page, RETRY_BUTTON_SELECTORS, timeout_ms=1500)
        if not selector:
            return False
        button = self.page.locator(selector).first
        try:
            button.click(timeout=3000)
            return True
        except Exception:
            try:
                button.click(timeout=3000, force=True)
                return True
            except Exception:
                return False

    def _click_locator(self, locator: Locator) -> bool:
        try:
            locator.click(timeout=3000)
            return True
        except Exception:
            try:
                locator.click(timeout=3000, force=True)
                return True
            except Exception:
                try:
                    locator.evaluate("el => el.click()")
                    return True
                except Exception:
                    return False

    def _iter_visible_nodes(self, selectors: Iterable[str], *, max_count: int = 120):
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                count = min(locator.count(), max_count)
            except Exception:
                continue
            for index in range(count):
                node = locator.nth(index)
                try:
                    if not node.is_visible(timeout=100):
                        continue
                    text = node.inner_text(timeout=400).strip()
                    if not text:
                        continue
                    yield selector, node, " ".join(text.split())
                except Exception:
                    continue

    def _text_matches(self, text: Optional[str], terms: Iterable[str]) -> bool:
        normalized = normalize_ui_text(text)
        return all(term in normalized for term in terms)

    def _resolve_model_target(self, model: str) -> Dict[str, Any]:
        normalized = normalize_ui_text(model)
        for preset in MODEL_PRESETS.values():
            if self._text_matches(normalized, preset["match_terms"]):
                return preset
        if "instant" in normalized and "5.3" in normalized:
            return MODEL_PRESETS["gpt-5.3-instant"]
        if "thinking" in normalized and "5.4" in normalized:
            return MODEL_PRESETS["gpt-5.4-thinking"]
        if "pro" in normalized and "5.4" in normalized:
            return MODEL_PRESETS["gpt-5.4-pro"]
        raise ChatGPTSkillError(
            "unsupported_model",
            f"Unsupported model target: {model}",
            details={"model": model, "supported_models": [item["label"] for item in MODEL_PRESETS.values()]},
        )

    def current_model_label(self) -> Optional[str]:
        for _selector, _node, text in self._iter_visible_nodes(MODEL_PICKER_SELECTORS, max_count=20):
            normalized = normalize_ui_text(text)
            if any(term in normalized for term in ("5.3", "5.4", "instant", "thinking", "pro")):
                return text
        return None

    def select_model(self, model: str) -> Dict[str, Any]:
        target = self._resolve_model_target(model)
        current = self.current_model_label()
        if current and self._text_matches(current, target["match_terms"]):
            return {
                "selected_model": current,
                "requested_model": target["label"],
                "changed": False,
            }

        self._dismiss_non_critical_overlays()
        picker_text = None
        for _selector, node, text in self._iter_visible_nodes(MODEL_PICKER_SELECTORS, max_count=20):
            picker_text = text
            if self._click_locator(node):
                break
        else:
            raise ChatGPTSkillError("model_picker_missing", "Could not find the ChatGPT model picker", details={"final_url": self.page.url})

        self.page.wait_for_timeout(1200)
        selected_item = None
        for _selector, node, text in self._iter_visible_nodes(MODEL_MENU_ITEM_SELECTORS, max_count=200):
            if not self._text_matches(text, target["match_terms"]):
                continue
            if self._click_locator(node):
                selected_item = text
                break
        if not selected_item:
            raise ChatGPTSkillError(
                "model_option_missing",
                f"Could not find the requested model option: {target['label']}",
                details={"requested_model": target["label"], "final_url": self.page.url},
            )

        deadline = time.time() + 8
        while time.time() < deadline:
            current = self.current_model_label()
            if current and self._text_matches(current, target["match_terms"]):
                return {
                    "selected_model": current,
                    "requested_model": target["label"],
                    "changed": True,
                    "opened_from": picker_text,
                    "selected_item": selected_item,
                }
            time.sleep(0.5)

        raise ChatGPTSkillError(
            "model_switch_unconfirmed",
            f"Model switch did not settle on {target['label']}",
            details={
                "requested_model": target["label"],
                "selected_item": selected_item,
                "current_model": self.current_model_label(),
                "final_url": self.page.url,
            },
        )

    def enable_extended_thinking(self) -> Dict[str, Any]:
        self._dismiss_non_critical_overlays()
        for _selector, node, text in self._iter_visible_nodes(EXTENDED_THINKING_SELECTORS, max_count=120):
            if "extended thinking" not in normalize_ui_text(text):
                continue
            aria_pressed = node.get_attribute("aria-pressed")
            data_state = node.get_attribute("data-state")
            if aria_pressed == "true" or normalize_ui_text(data_state) in {"on", "active", "checked", "open"}:
                return {
                    "extended_thinking": True,
                    "changed": False,
                    "control_text": text,
                }
            if not self._click_locator(node):
                break
            self.page.wait_for_timeout(1000)
            return {
                "extended_thinking": True,
                "changed": True,
                "control_text": text,
            }
        raise ChatGPTSkillError(
            "extended_thinking_unavailable",
            "Could not find the Extended thinking control on the page",
            details={"current_model": self.current_model_label(), "final_url": self.page.url},
        )

    def prepare_chat(
        self,
        *,
        new_chat: bool = False,
        model: Optional[str] = None,
        extended_thinking: bool = False,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if new_chat:
            payload["new_chat"] = self.new_chat()
        if model:
            payload["model"] = self.select_model(model)
        if extended_thinking:
            payload["extended_thinking"] = self.enable_extended_thinking()
        payload["current_model"] = self.current_model_label()
        return payload

    def new_chat(self) -> Dict[str, Any]:
        self._dismiss_non_critical_overlays()
        selector = wait_for_any(self.page, NEW_CHAT_SELECTORS, timeout_ms=2000)
        if selector:
            button = self.page.locator(selector).first
            try:
                button.click(timeout=3000)
            except Exception:
                try:
                    button.click(timeout=3000, force=True)
                except Exception:
                    button.evaluate("el => el.click()")
            time.sleep(1)
        else:
            self._goto(CHATGPT_BASE_URL)
        self._ensure_ready()
        self._sync_current_conversation()
        return {
            "status": "success",
            "conversation_id": self.conversation_id,
            "conversation_id_source": self.conversation_id_source,
            "final_url": self.page.url,
        }

    def open_conversation(self, conversation_id: str) -> Dict[str, Any]:
        if not is_url_addressable_conversation_id(conversation_id):
            raise ChatGPTSkillError(
                "invalid_conversation_id",
                "This conversation id is not reopenable via ChatGPT URL",
                details={"conversation_id": conversation_id},
            )
        self._goto(conversation_url(conversation_id))
        self._ensure_ready()
        state = extract_conversation_state(self.page)
        current_id = state.get("conversation_id")
        if current_id != conversation_id:
            raise ChatGPTSkillError(
                "invalid_conversation_id",
                "Requested conversation id did not resolve to the expected ChatGPT conversation",
                details={
                    "requested_conversation_id": conversation_id,
                    "resolved_conversation_id": current_id,
                    "conversation_id_source": state.get("source"),
                    "final_url": self.page.url,
                },
            )
        self._sync_current_conversation()
        return {
            "status": "success",
            "conversation_id": self.conversation_id,
            "conversation_id_source": self.conversation_id_source,
            "final_url": self.page.url,
        }

    def _find_composer(self) -> str:
        self._dismiss_non_critical_overlays()
        selector = wait_for_any(self.page, COMPOSER_SELECTORS, timeout_ms=UI_MEDIUM_TIMEOUT_MS)
        if not selector:
            self._ensure_ready()
            selector = wait_for_any(self.page, COMPOSER_SELECTORS, timeout_ms=UI_MEDIUM_TIMEOUT_MS)
        if not selector:
            raise ChatGPTSkillError("input_box_missing", "ChatGPT message input box was not found", details={"final_url": self.page.url})
        return selector

    def _send_question(self, question: str):
        self._dismiss_non_critical_overlays()
        selector = self._find_composer()
        composer = self.page.locator(selector).first
        try:
            composer.click(timeout=3000)
        except Exception:
            try:
                composer.click(timeout=3000, force=True)
            except Exception:
                try:
                    composer.evaluate("el => el.focus()")
                except Exception:
                    pass
        self.stealth.random_delay(120, 260)

        try:
            composer.fill(question, timeout=3000)
        except Exception:
            try:
                composer.evaluate(
                    """(el, value) => {
                        el.focus();
                        if ('value' in el) {
                            el.value = value;
                        } else {
                            el.textContent = value;
                        }
                        el.dispatchEvent(new InputEvent('input', { bubbles: true, data: value }));
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }""",
                    question,
                )
            except Exception:
                self.page.keyboard.insert_text(question)

        self.stealth.random_delay(180, 320)
        self._dismiss_non_critical_overlays()

        send_selector = wait_for_any(self.page, SEND_BUTTON_SELECTORS, timeout_ms=1500)
        if send_selector:
            button = self.page.locator(send_selector).first
            try:
                if button.is_enabled(timeout=1000):
                    button.click(timeout=3000)
                    return
            except Exception:
                try:
                    button.click(timeout=3000, force=True)
                    return
                except Exception:
                    pass

        try:
            self.page.keyboard.press("Enter")
        except Exception as error:
            raise ChatGPTSkillError("send_button_unavailable", "Could not submit the message to ChatGPT", details={"cause": str(error)}) from error

    def _wait_for_send_ack(self, previous_user_message: Optional[str], question: str, timeout_seconds: int = 15) -> bool:
        deadline = time.time() + timeout_seconds
        normalized_question = " ".join(question.split())
        while time.time() < deadline:
            self._dismiss_non_critical_overlays()
            current_user_message = self._snapshot_latest_user_message()
            if self._is_generating():
                return True
            if current_user_message and current_user_message != previous_user_message:
                normalized_current = " ".join(current_user_message.split())
                if normalized_current == normalized_question:
                    return True
                if normalized_question and normalized_current and (
                    normalized_question in normalized_current or normalized_current in normalized_question
                ):
                    return True
                return True
            if self._detect_response_error():
                return True
            time.sleep(0.5)
        return False

    def _wait_for_answer(self, previous_answer: Optional[str], timeout_seconds: int = RESPONSE_TIMEOUT_SECONDS) -> str:
        deadline = time.time() + timeout_seconds
        last_text = None
        stable_count = 0
        saw_generation = False

        while time.time() < deadline:
            self._ensure_ready()
            current_text = self._snapshot_latest_answer()
            generating = self._is_generating()
            if generating:
                saw_generation = True

            error_text = self._detect_response_error()
            if error_text and not generating:
                raise ChatGPTSkillError(
                    "response_generation_failed",
                    "ChatGPT returned an internal generation error instead of a normal answer",
                    details={"final_url": self.page.url, "answer": error_text},
                )

            if current_text and current_text != previous_answer:
                if current_text == last_text:
                    stable_count += 1
                else:
                    last_text = current_text
                    stable_count = 1

                if not generating and stable_count >= 2 and (saw_generation or len(current_text) > 0):
                    return current_text

            time.sleep(1)

        raise ChatGPTSkillError(
            "response_timeout",
            f"Timed out waiting for ChatGPT response after {timeout_seconds} seconds",
            details={"final_url": self.page.url, "screenshot": take_debug_screenshot(self.page, f"timeout-{self.id}")},
        )

    def _recover_after_wait_error(
        self,
        previous_answer: Optional[str],
        error: ChatGPTSkillError,
        *,
        timeout_seconds: int = RESPONSE_TIMEOUT_SECONDS,
    ) -> Optional[str]:
        if error.code not in {"response_timeout", "response_generation_failed"}:
            return None

        if self._click_retry_button():
            return self._wait_for_answer(previous_answer, timeout_seconds=timeout_seconds)

        try:
            target_url = conversation_url(self.conversation_id) if is_url_addressable_conversation_id(self.conversation_id) else self.page.url
            self._goto(target_url)
            self._ensure_ready()
            refreshed_answer = self._snapshot_latest_answer()
            if refreshed_answer and refreshed_answer != previous_answer:
                lower_answer = refreshed_answer.lower()
                if not any(hint in lower_answer for hint in RESPONSE_ERROR_TEXT_HINTS):
                    return refreshed_answer
            if self._click_retry_button():
                return self._wait_for_answer(previous_answer, timeout_seconds=timeout_seconds)
        except Exception:
            return None
        return None

    def ask(
        self,
        question: str,
        *,
        new_chat: bool = False,
        model: Optional[str] = None,
        extended_thinking: bool = False,
        proof_screenshot: bool = False,
    ) -> Dict[str, Any]:
        if not question.strip():
            raise ChatGPTSkillError("empty_question", "Question must not be empty")

        workflow = self.prepare_chat(
            new_chat=new_chat,
            model=model,
            extended_thinking=extended_thinking,
        )
        answer_timeout_seconds = max(RESPONSE_TIMEOUT_SECONDS, 420) if extended_thinking else RESPONSE_TIMEOUT_SECONDS
        workflow["answer_timeout_seconds"] = answer_timeout_seconds

        self.last_activity = time.time()
        previous_answer = self._snapshot_latest_answer()
        previous_user_message = self._snapshot_latest_user_message()
        self._send_question(question)
        if not self._wait_for_send_ack(previous_user_message, question):
            self._dismiss_non_critical_overlays()
            self._send_question(question)
            if not self._wait_for_send_ack(previous_user_message, question):
                raise ChatGPTSkillError(
                    "message_submit_unconfirmed",
                    "The question could not be confirmed as submitted to ChatGPT",
                    details={
                        "final_url": self.page.url,
                        "screenshot": take_debug_screenshot(self.page, f"submit-{self.id}"),
                    },
                )
        try:
            answer = self._wait_for_answer(previous_answer, timeout_seconds=answer_timeout_seconds)
        except ChatGPTSkillError as error:
            recovered_answer = self._recover_after_wait_error(previous_answer, error, timeout_seconds=answer_timeout_seconds)
            if recovered_answer is None:
                raise
            answer = recovered_answer
        if not answer.strip():
            raise ChatGPTSkillError("empty_response", "ChatGPT returned an empty response", details={"final_url": self.page.url})
        lower_answer = answer.lower()
        if any(hint in lower_answer for hint in RESPONSE_ERROR_TEXT_HINTS):
            raise ChatGPTSkillError(
                "response_generation_failed",
                "ChatGPT returned an internal generation error instead of a normal answer",
                details={"final_url": self.page.url, "answer": answer},
            )

        self.message_count += 1
        self.last_activity = time.time()
        self._sync_current_conversation()
        screenshot = take_debug_screenshot(self.page, f"proof-{self.id}") if proof_screenshot else None
        return {
            "status": "success",
            "question": question,
            "answer": answer,
            "conversation_id": self.conversation_id,
            "conversation_id_source": self.conversation_id_source,
            "final_url": self.page.url,
            "session_id": self.id,
            "current_model": workflow.get("current_model") or self.current_model_label(),
            "selected_model": (workflow.get("model") or {}).get("selected_model"),
            "extended_thinking": bool(workflow.get("extended_thinking")),
            "screenshot": screenshot,
            "workflow": workflow,
        }

    def reset(self) -> Dict[str, Any]:
        target_conversation = self.conversation_id
        if self.page:
            self.page.close()
        self.page = self.context.new_page()
        target_url = conversation_url(target_conversation) if is_url_addressable_conversation_id(target_conversation) else CHATGPT_BASE_URL
        self._goto(target_url)
        self._ensure_ready()
        self._sync_current_conversation()
        self.message_count = 0
        self.last_activity = time.time()
        return {
            "status": "success",
            "conversation_id": self.conversation_id,
            "conversation_id_source": self.conversation_id_source,
            "final_url": self.page.url,
            "session_id": self.id,
        }

    def close(self):
        if self.page:
            try:
                self.page.close()
            except Exception:
                pass
            self.page = None

    def get_info(self) -> Dict[str, Any]:
        return {
            "session_id": self.id,
            "conversation_id": self.conversation_id,
            "conversation_id_source": self.conversation_id_source,
            "final_url": self.page.url if self.page else None,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "message_count": self.message_count,
        }

    def is_expired(self, timeout_seconds: int) -> bool:
        return (time.time() - self.last_activity) > timeout_seconds
