# -*- coding: utf-8 -*-

import json
import os
import sys
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from src.ecommerce_voice_cs import EcommerceVoiceCSSkill, VoiceCloneService


def _u(text: str) -> str:
    return text.encode("ascii").decode("unicode_escape")


STATE_DIR = SKILL_ROOT / ".session_state"
STATE_DIR.mkdir(exist_ok=True)

CONFIRMED_VOICE_IDS = ["child_0001_b", "male_0004_a", "male_0018_a"]
DEFAULT_VOICE_ID = CONFIRMED_VOICE_IDS[0]
SENSEAUDIO_API_KEY_ENV = "SENSEAUDIO_API_KEY"

AFTER_SALES_TRIGGER = _u(
    "\\u6211\\u9700\\u8981\\u4f60\\u73b0\\u5728\\u5f53\\u4e00\\u4e2a\\u5ba2\\u670d\\u673a\\u5668\\u4eba"
)
SALES_TRIGGER = _u(
    "\\u6211\\u9700\\u8981\\u4f60\\u73b0\\u5728\\u5f53\\u4e00\\u4e2a\\u63a8\\u9500\\u5458"
)
CONFIRM_ENTER_PHRASES = {
    _u("\\u786e\\u8ba4\\u8fdb\\u5165"),
    _u("\\u786e\\u8ba4"),
    _u("\\u8fdb\\u5165"),
    _u("\\u5f00\\u59cb"),
    _u("\\u5f00\\u59cb\\u5427"),
}
CANCEL_ENTER_PHRASES = {
    _u("\\u53d6\\u6d88"),
    _u("\\u5148\\u4e0d\\u8fdb\\u5165"),
    _u("\\u6682\\u4e0d\\u8fdb\\u5165"),
}

AFTER_SALES_DEFAULTS = {
    "api_key": "",
    "voice_id": DEFAULT_VOICE_ID,
    "refund_policy": "",
    "unboxing_allowed": None,
    "shipping_fee_by": "",
    "audio_output_path": "",
}
SALES_DEFAULTS = {
    "api_key": "",
    "voice_id": DEFAULT_VOICE_ID,
    "audio_output_path": "",
    "product_name": "",
    "product_features": "",
    "product_advantages": "",
    "discount_range": "",
}


def _env_api_key() -> str:
    return os.getenv(SENSEAUDIO_API_KEY_ENV, "").strip()


def _resolved_api_key(cfg: dict[str, Any]) -> str:
    return str(cfg.get("api_key", "")).strip() or _env_api_key()


def _normalize_audio_format(value: Any) -> str:
    normalized = str(value or ".mp3").strip().lower() or ".mp3"
    return normalized if normalized.startswith(".") else f".{normalized}"


def _mime_type_for_ext(file_ext: str) -> str:
    return {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
    }.get(file_ext.lower(), "application/octet-stream")


def _build_playback(audio_file: str | None) -> dict[str, Any] | None:
    if not audio_file:
        return None
    path = Path(audio_file)
    file_ext = path.suffix.lower() or ".mp3"
    return {
        "action": "play_audio",
        "auto_play": True,
        "source_type": "local_file",
        "path": str(path),
        "format": file_ext.lstrip("."),
        "mime_type": _mime_type_for_ext(file_ext),
        "retain_file": True,
    }


def _state_file(session_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in session_id)
    return STATE_DIR / f"{safe}.json"


def _load_state(session_id: str) -> dict[str, Any]:
    path = _state_file(session_id)
    if not path.exists():
        return {
            "mode": "idle",
            "stage": "idle",
            "after_sales": dict(AFTER_SALES_DEFAULTS),
            "sales": dict(SALES_DEFAULTS),
        }
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(session_id: str, state: dict[str, Any]) -> None:
    _state_file(session_id).write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class VoiceMaster:
    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        session_id = str(payload.get("session_id", "default")).strip() or "default"
        message = str(payload.get("message", "")).strip()
        if not message:
            return {"ok": False, "error": "message is required", "session_id": session_id}

        state = _load_state(session_id)
        if message == AFTER_SALES_TRIGGER:
            state["mode"] = "after_sales"
            state["stage"] = "collecting"
            _save_state(session_id, state)
            return self._handle_after_sales(session_id, message, payload, state)
        if message == SALES_TRIGGER:
            state["mode"] = "sales"
            state["stage"] = "collecting"
            _save_state(session_id, state)
            return self._handle_sales(session_id, message, payload, state)
        if state["mode"] == "after_sales":
            return self._handle_after_sales(session_id, message, payload, state)
        if state["mode"] == "sales":
            return self._handle_sales(session_id, message, payload, state)
        return {
            "ok": True,
            "session_id": session_id,
            "text": (
                _u("\\u5f53\\u524d\\u672a\\u8fdb\\u5165\\u4efb\\u4f55\\u6a21\\u5f0f\\u3002")
                + _u("\\u5982\\u679c\\u8981\\u542f\\u7528\\u552e\\u540e\\u529f\\u80fd\\uff0c\\u8bf7\\u53d1\\u9001\\u201c")
                + AFTER_SALES_TRIGGER
                + _u("\\u201d\\uff1b")
                + _u("\\u5982\\u679c\\u8981\\u542f\\u7528\\u7535\\u8bdd\\u63a8\\u9500\\u529f\\u80fd\\uff0c\\u8bf7\\u53d1\\u9001\\u201c")
                + SALES_TRIGGER
                + _u("\\u201d\\u3002")
            ),
            "audio_file": None,
            "playback": None,
            "state_changed": False,
            "metadata": {"mode": "idle"},
        }

    def _handle_after_sales(self, session_id: str, message: str, payload: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
        cfg = dict(AFTER_SALES_DEFAULTS)
        cfg.update(state.get("after_sales") or {})
        effective_api_key = _resolved_api_key(cfg)
        self._merge_after_sales_payload(cfg, payload)
        effective_api_key = _resolved_api_key(cfg)
        if state["stage"] == "collecting":
            if message != AFTER_SALES_TRIGGER:
                self._parse_after_sales_message(cfg, message)
            state["after_sales"] = cfg
            missing = self._missing_after_sales(cfg)
            if missing:
                _save_state(session_id, state)
                return self._after_sales_collecting_prompt(session_id, state["stage"], cfg, missing)
            state["stage"] = "awaiting_confirmation"
            _save_state(session_id, state)
            return self._simple_response(
                session_id,
                self._build_after_sales_confirmation_text(cfg),
                {"mode": "after_sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]},
            )
        if state["stage"] == "awaiting_confirmation":
            self._parse_after_sales_message(cfg, message)
            state["after_sales"] = cfg
            if self._is_cancel_message(message, payload):
                state["stage"] = "collecting"
                _save_state(session_id, state)
                return self._simple_response(session_id, _u("\\u5df2\\u53d6\\u6d88\\u8fdb\\u5165\\u552e\\u540e\\u6a21\\u5f0f\\u3002\\u8bf7\\u91cd\\u65b0\\u8865\\u5145\\u6216\\u4fee\\u6539\\u914d\\u7f6e\\u9879\\u3002"), {"mode": "after_sales", "stage": state["stage"]})
            if self._contains_after_sales_update(message):
                _save_state(session_id, state)
                return self._simple_response(session_id, self._build_after_sales_confirmation_text(cfg), {"mode": "after_sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]})
            if not self._is_confirm_message(message, payload):
                _save_state(session_id, state)
                return self._simple_response(session_id, _u("\\u8bf7\\u56de\\u590d\\u201c\\u786e\\u8ba4\\u8fdb\\u5165\\u201d\\u6216\\u4f20 confirm_enter=true\\uff0c\\u4ee5\\u6b63\\u5f0f\\u8fdb\\u5165\\u552e\\u540e\\u6a21\\u5f0f\\uff1b\\u5982\\u9700\\u4fee\\u6539\\uff0c\\u7ee7\\u7eed\\u53d1\\u9001\\u5bf9\\u5e94\\u5b57\\u6bb5\\u3002"), {"mode": "after_sales", "stage": state["stage"]})
            state["stage"] = "active"
            _save_state(session_id, state)
            return self._simple_response(session_id, _u("\\u5df2\\u6b63\\u5f0f\\u8fdb\\u5165\\u552e\\u540e\\u5ba2\\u670d\\u6a21\\u5f0f\\u3002\\u540e\\u7eed\\u6bcf\\u6761\\u56de\\u590d\\u90fd\\u4f1a\\u5148\\u751f\\u6210\\u6587\\u672c\\uff0c\\u518d\\u751f\\u6210 TTS \\u97f3\\u9891\\uff0c\\u5e76\\u8f93\\u51fa\\u5230\\uff1a") + cfg["audio_output_path"], {"mode": "after_sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]}, state_changed=True)

        skill = EcommerceVoiceCSSkill()
        skill.set_api_key(effective_api_key)
        skill.configure(
            refund_policy=cfg["refund_policy"],
            unboxing_allowed=bool(cfg["unboxing_allowed"]),
            shipping_fee_by=cfg["shipping_fee_by"],
            audio_output_path=cfg["audio_output_path"],
        )
        skill.handle_message(AFTER_SALES_TRIGGER, voice_handle=cfg["voice_id"])
        response = skill.handle_message(
            message,
            voice_handle=cfg["voice_id"],
            api_key=effective_api_key,
            audio_output_path=cfg["audio_output_path"],
            refund_policy=cfg["refund_policy"],
            unboxing_allowed=cfg["unboxing_allowed"],
            shipping_fee_by=cfg["shipping_fee_by"],
            audio_format=_normalize_audio_format(payload.get("audio_format", ".mp3")),
            sample_rate=int(payload.get("sample_rate", 32000)),
            bitrate=int(payload.get("bitrate", 128000)),
            channel=int(payload.get("channel", 1)),
            speed=float(payload.get("speed", 1)),
            volume=float(payload.get("volume", 1)),
            pitch=int(payload.get("pitch", 0)),
        )
        text = response.text
        audio_file = str(response.audio_file) if response.audio_file else None
        playback = _build_playback(audio_file)
        if response.audio_file:
            text += "\n\n" + _u("\\u0054\\u0054\\u0053\\u0020\\u5df2\\u751f\\u6210\\u6210\\u529f\\uff0c\\u6587\\u4ef6\\u5df2\\u4fdd\\u5b58\\u5230\\uff1a") + str(Path(response.audio_file))
        return {
            "ok": True,
            "session_id": session_id,
            "text": text,
            "audio_file": audio_file,
            "playback": playback,
            "state_changed": response.state_changed,
            "metadata": {"mode": "after_sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"], "playback": playback, **response.metadata},
        }

    def _handle_sales(self, session_id: str, message: str, payload: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
        cfg = dict(SALES_DEFAULTS)
        cfg.update(state.get("sales") or {})
        effective_api_key = _resolved_api_key(cfg)
        self._merge_sales_payload(cfg, payload)
        effective_api_key = _resolved_api_key(cfg)
        if state["stage"] == "collecting":
            if message != SALES_TRIGGER:
                self._parse_sales_message(cfg, message)
            state["sales"] = cfg
            missing = self._missing_sales(cfg)
            if missing:
                _save_state(session_id, state)
                return self._sales_collecting_prompt(session_id, state["stage"], cfg, missing)
            state["stage"] = "awaiting_confirmation"
            _save_state(session_id, state)
            return self._simple_response(session_id, self._build_sales_confirmation_text(cfg), {"mode": "sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]})
        if state["stage"] == "awaiting_confirmation":
            self._parse_sales_message(cfg, message)
            state["sales"] = cfg
            if self._is_cancel_message(message, payload):
                state["stage"] = "collecting"
                _save_state(session_id, state)
                return self._simple_response(session_id, _u("\\u5df2\\u53d6\\u6d88\\u8fdb\\u5165\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\u3002\\u8bf7\\u91cd\\u65b0\\u8865\\u5145\\u6216\\u4fee\\u6539\\u914d\\u7f6e\\u9879\\u3002"), {"mode": "sales", "stage": state["stage"]})
            if self._contains_sales_update(message):
                _save_state(session_id, state)
                return self._simple_response(session_id, self._build_sales_confirmation_text(cfg), {"mode": "sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]})
            if not self._is_confirm_message(message, payload):
                # In some hosts, Chinese confirmation text may be transcoded poorly.
                # For sales mode, treat any non-update, non-cancel reply here as confirmation.
                if message.strip():
                    state["stage"] = "active"
                    _save_state(session_id, state)
                    return self._simple_response(session_id, _u("\\u5df2\\u6b63\\u5f0f\\u8fdb\\u5165\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\u3002\\u540e\\u7eed\\u63a8\\u9500\\u8bdd\\u672f\\u4f1a\\u5148\\u751f\\u6210\\u6587\\u672c\\uff0c\\u518d\\u751f\\u6210 TTS \\u97f3\\u9891\\uff0c\\u5e76\\u8f93\\u51fa\\u5230\\uff1a") + cfg["audio_output_path"], {"mode": "sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]}, state_changed=True)
                _save_state(session_id, state)
                return self._simple_response(session_id, _u("\\u8bf7\\u56de\\u590d\\u201c\\u5f00\\u59cb\\u201d\\u6216\\u4f20 confirm_enter=true\\uff0c\\u4ee5\\u6b63\\u5f0f\\u8fdb\\u5165\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\uff1b\\u5982\\u9700\\u4fee\\u6539\\uff0c\\u7ee7\\u7eed\\u53d1\\u9001\\u5bf9\\u5e94\\u5b57\\u6bb5\\u3002"), {"mode": "sales", "stage": state["stage"]})
            state["stage"] = "active"
            _save_state(session_id, state)
            return self._simple_response(session_id, _u("\\u5df2\\u6b63\\u5f0f\\u8fdb\\u5165\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\u3002\\u540e\\u7eed\\u63a8\\u9500\\u8bdd\\u672f\\u4f1a\\u5148\\u751f\\u6210\\u6587\\u672c\\uff0c\\u518d\\u751f\\u6210 TTS \\u97f3\\u9891\\uff0c\\u5e76\\u8f93\\u51fa\\u5230\\uff1a") + cfg["audio_output_path"], {"mode": "sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"]}, state_changed=True)

        voice_service = VoiceCloneService(api_key=effective_api_key)
        sales_text = self._generate_sales_text(message, cfg)
        audio_file = voice_service.synthesize_to_file(
            text=sales_text,
            voice_handle=cfg["voice_id"],
            output_dir=cfg["audio_output_path"],
            file_ext=_normalize_audio_format(payload.get("audio_format", ".mp3")),
            sample_rate=int(payload.get("sample_rate", 32000)),
            bitrate=int(payload.get("bitrate", 128000)),
            channel=int(payload.get("channel", 1)),
            speed=float(payload.get("speed", 1)),
            volume=float(payload.get("volume", 1)),
            pitch=int(payload.get("pitch", 0)),
        )
        audio_file_str = str(audio_file)
        playback = _build_playback(audio_file_str)
        return {
            "ok": True,
            "session_id": session_id,
            "text": sales_text + "\n\n" + _u("\\u0054\\u0054\\u0053\\u0020\\u5df2\\u751f\\u6210\\u6210\\u529f\\uff0c\\u6587\\u4ef6\\u5df2\\u4fdd\\u5b58\\u5230\\uff1a") + str(Path(audio_file)),
            "audio_file": audio_file_str,
            "playback": playback,
            "state_changed": False,
            "metadata": {"mode": "sales", "stage": state["stage"], "voice_id": cfg["voice_id"], "audio_output_path": cfg["audio_output_path"], "playback": playback},
        }

    @staticmethod
    def _simple_response(session_id: str, text: str, metadata: dict[str, Any], state_changed: bool = False) -> dict[str, Any]:
        return {"ok": True, "session_id": session_id, "text": text, "audio_file": None, "playback": None, "state_changed": state_changed, "metadata": metadata}

    @staticmethod
    def _missing_after_sales(cfg: dict[str, Any]) -> list[str]:
        missing = []
        if not _resolved_api_key(cfg):
            missing.append("api_key")
        for key in ("refund_policy", "shipping_fee_by", "audio_output_path"):
            if not cfg.get(key):
                missing.append(key)
        if cfg.get("unboxing_allowed") is None:
            missing.append("unboxing_allowed")
        return missing

    @staticmethod
    def _missing_sales(cfg: dict[str, Any]) -> list[str]:
        missing = []
        if not _resolved_api_key(cfg):
            missing.append("api_key")
        missing.extend(
            key
            for key in (
                "audio_output_path",
                "product_name",
                "product_features",
                "product_advantages",
                "discount_range",
            )
            if not cfg.get(key)
        )
        return missing

    @staticmethod
    def _merge_after_sales_payload(cfg: dict[str, Any], payload: dict[str, Any]) -> None:
        for key in ("api_key", "refund_policy", "shipping_fee_by", "audio_output_path"):
            value = str(payload.get(key, "")).strip()
            if value:
                cfg[key] = value
        voice_id = str(payload.get("voice_id", "")).strip()
        if voice_id in CONFIRMED_VOICE_IDS:
            cfg["voice_id"] = voice_id
        if payload.get("unboxing_allowed") is not None:
            cfg["unboxing_allowed"] = bool(payload.get("unboxing_allowed"))

    @staticmethod
    def _merge_sales_payload(cfg: dict[str, Any], payload: dict[str, Any]) -> None:
        for key in ("api_key", "audio_output_path", "product_name", "product_features", "product_advantages", "discount_range"):
            value = str(payload.get(key, "")).strip()
            if value:
                cfg[key] = value
        voice_id = str(payload.get("voice_id", "")).strip()
        if voice_id in CONFIRMED_VOICE_IDS:
            cfg["voice_id"] = voice_id

    @staticmethod
    def _parse_after_sales_message(cfg: dict[str, Any], message: str) -> None:
        normalized = message.strip()
        if normalized in CONFIRMED_VOICE_IDS:
            cfg["voice_id"] = normalized
        for key in ("api_key", "audio_output_path", "refund_policy", "shipping_fee_by"):
            prefix = f"{key}="
            if normalized.startswith(prefix):
                cfg[key] = normalized.split("=", 1)[1].strip()
                return
        if normalized.startswith("unboxing_allowed="):
            value = normalized.split("=", 1)[1].strip().lower()
            if value in {"true", "yes", "1"}:
                cfg["unboxing_allowed"] = True
            elif value in {"false", "no", "0"}:
                cfg["unboxing_allowed"] = False

    @staticmethod
    def _parse_sales_message(cfg: dict[str, Any], message: str) -> None:
        normalized = message.strip()
        if normalized in CONFIRMED_VOICE_IDS:
            cfg["voice_id"] = normalized
        for key in ("api_key", "audio_output_path", "product_name", "product_features", "product_advantages", "discount_range"):
            prefix = f"{key}="
            if normalized.startswith(prefix):
                cfg[key] = normalized.split("=", 1)[1].strip()
                return

    @staticmethod
    def _after_sales_collecting_prompt(session_id: str, stage: str, cfg: dict[str, Any], missing: list[str]) -> dict[str, Any]:
        prompts = {
            "api_key": _u("\\u672a\\u68c0\\u6d4b\\u5230\\u73af\\u5883\\u53d8\\u91cf SENSEAUDIO_API_KEY\\uff0c\\u8bf7\\u63d0\\u4f9b SenseAudio API Key\\u3002"),
            "refund_policy": _u("\\u8bf7\\u63d0\\u4f9b refund_policy\\uff0c\\u4f8b\\u5982\\uff1a\\u5546\\u54c1\\u7b7e\\u6536\\u540e 7 \\u5929\\u5185\\u53ef\\u9000\\u6362\\uff0c\\u8d28\\u91cf\\u95ee\\u9898\\u4f18\\u5148\\u5904\\u7406\\u3002"),
            "unboxing_allowed": _u("\\u8bf7\\u8bf4\\u660e unboxing_allowed\\uff0c\\u586b true/false\\u3002"),
            "shipping_fee_by": _u("\\u8bf7\\u8bf4\\u660e shipping_fee_by\\uff0c\\u4f8b\\u5982\\uff1a\\u5546\\u5bb6 \\u6216 \\u4e70\\u5bb6\\u3002"),
            "audio_output_path": _u("\\u8bf7\\u63d0\\u4f9b audio_output_path\\uff0c\\u4e5f\\u5c31\\u662f\\u97f3\\u9891\\u6587\\u4ef6\\u8f93\\u51fa\\u76ee\\u5f55\\u3002"),
        }
        return {"ok": True, "session_id": session_id, "text": _u("\\u8fdb\\u5165\\u552e\\u540e\\u6a21\\u5f0f\\u524d\\uff0c\\u9700\\u8981\\u5148\\u786e\\u8ba4\\u914d\\u7f6e\\u3002\\u8bf7\\u5148\\u8865\\u5145\\u4ee5\\u4e0b\\u4fe1\\u606f\\u540e\\uff0c\\u6211\\u518d\\u7ed9\\u4f60\\u505a\\u6700\\u7ec8\\u786e\\u8ba4\\uff1a\\n") + "\n".join(prompts[item] for item in missing) + _u("\\n\\u53ef\\u9009 voice_id\\uff1achild_0001_b / male_0004_a / male_0018_a\\u3002\\n\\u5f53\\u524d\\u9ed8\\u8ba4 voice_id\\uff1a") + cfg["voice_id"], "audio_file": None, "playback": None, "state_changed": False, "metadata": {"mode": "after_sales", "stage": stage, "missing_configuration": missing, "voice_id": cfg["voice_id"]}}

    @staticmethod
    def _sales_collecting_prompt(session_id: str, stage: str, cfg: dict[str, Any], missing: list[str]) -> dict[str, Any]:
        prompts = {
            "api_key": _u("\\u672a\\u68c0\\u6d4b\\u5230\\u73af\\u5883\\u53d8\\u91cf SENSEAUDIO_API_KEY\\uff0c\\u8bf7\\u63d0\\u4f9b SenseAudio API Key\\u3002"),
            "audio_output_path": _u("\\u8bf7\\u63d0\\u4f9b audio_output_path\\uff0c\\u4e5f\\u5c31\\u662f\\u97f3\\u9891\\u6587\\u4ef6\\u8f93\\u51fa\\u76ee\\u5f55\\u3002"),
            "product_name": _u("\\u8bf7\\u63d0\\u4f9b product_name\\uff0c\\u4e5f\\u5c31\\u662f\\u4ea7\\u54c1\\u540d\\u79f0\\u3002"),
            "product_features": _u("\\u8bf7\\u63d0\\u4f9b product_features\\uff0c\\u4e5f\\u5c31\\u662f\\u4ea7\\u54c1\\u529f\\u80fd\\u3002"),
            "product_advantages": _u("\\u8bf7\\u63d0\\u4f9b product_advantages\\uff0c\\u4e5f\\u5c31\\u662f\\u4ea7\\u54c1\\u4f18\\u52bf\\u3002"),
            "discount_range": _u("\\u8bf7\\u63d0\\u4f9b discount_range\\uff0c\\u4e5f\\u5c31\\u662f\\u53ef\\u4f18\\u60e0\\u8303\\u56f4\\u3002"),
        }
        return {"ok": True, "session_id": session_id, "text": _u("\\u8fdb\\u5165\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\u524d\\uff0c\\u9700\\u8981\\u5148\\u786e\\u8ba4\\u914d\\u7f6e\\u3002\\u8bf7\\u5148\\u8865\\u5145\\u4ee5\\u4e0b\\u4fe1\\u606f\\u540e\\uff0c\\u6211\\u518d\\u7ed9\\u4f60\\u505a\\u6700\\u7ec8\\u786e\\u8ba4\\uff1a\\n") + "\n".join(prompts[item] for item in missing) + _u("\\n\\u53ef\\u9009 voice_id\\uff1achild_0001_b / male_0004_a / male_0018_a\\u3002\\n\\u5f53\\u524d\\u9ed8\\u8ba4 voice_id\\uff1a") + cfg["voice_id"], "audio_file": None, "playback": None, "state_changed": False, "metadata": {"mode": "sales", "stage": stage, "missing_configuration": missing, "voice_id": cfg["voice_id"]}}

    @staticmethod
    def _build_after_sales_confirmation_text(cfg: dict[str, Any]) -> str:
        unpacked = _u("\\u652f\\u6301") if cfg["unboxing_allowed"] else _u("\\u4e0d\\u652f\\u6301")
        return _u("\\u8bf7\\u786e\\u8ba4\\u4ee5\\u4e0b\\u552e\\u540e\\u6a21\\u5f0f\\u914d\\u7f6e\\uff1a\\n\\u9000\\u6b3e\\u653f\\u7b56\\uff1a") + cfg["refund_policy"] + "\n" + _u("\\u62c6\\u5c01\\u9000\\u8d27\\uff1a") + unpacked + "\n" + _u("\\u8fd0\\u8d39\\u627f\\u62c5\\u65b9\\uff1a") + cfg["shipping_fee_by"] + "\nvoice_id: " + cfg["voice_id"] + "\n" + _u("\\u97f3\\u9891\\u8f93\\u51fa\\u76ee\\u5f55\\uff1a") + cfg["audio_output_path"] + "\n" + _u("\\u5982\\u679c\\u786e\\u8ba4\\u65e0\\u8bef\\uff0c\\u8bf7\\u56de\\u590d\\u201c\\u786e\\u8ba4\\u8fdb\\u5165\\u201d\\u6216\\u4f20 confirm_enter=true\\uff1b\\u5982\\u679c\\u8981\\u4fee\\u6539\\uff0c\\u8bf7\\u7ee7\\u7eed\\u53d1\\u9001\\u5bf9\\u5e94\\u5b57\\u6bb5\\u3002")

    @staticmethod
    def _build_sales_confirmation_text(cfg: dict[str, Any]) -> str:
        return _u("\\u8bf7\\u786e\\u8ba4\\u4ee5\\u4e0b\\u7535\\u8bdd\\u63a8\\u9500\\u6a21\\u5f0f\\u914d\\u7f6e\\uff1a\\n\\u4ea7\\u54c1\\u540d\\u79f0\\uff1a") + cfg["product_name"] + "\n" + _u("\\u4ea7\\u54c1\\u529f\\u80fd\\uff1a") + cfg["product_features"] + "\n" + _u("\\u4ea7\\u54c1\\u4f18\\u52bf\\uff1a") + cfg["product_advantages"] + "\n" + _u("\\u4f18\\u60e0\\u8303\\u56f4\\uff1a") + cfg["discount_range"] + "\nvoice_id: " + cfg["voice_id"] + "\n" + _u("\\u97f3\\u9891\\u8f93\\u51fa\\u76ee\\u5f55\\uff1a") + cfg["audio_output_path"] + "\n" + _u("\\u5982\\u679c\\u786e\\u8ba4\\u65e0\\u8bef\\uff0c\\u8bf7\\u56de\\u590d\\u201c\\u5f00\\u59cb\\u201d\\u6216\\u4f20 confirm_enter=true\\uff1b\\u5982\\u679c\\u8981\\u4fee\\u6539\\uff0c\\u8bf7\\u7ee7\\u7eed\\u53d1\\u9001\\u5bf9\\u5e94\\u5b57\\u6bb5\\u3002")

    @staticmethod
    def _generate_sales_text(user_input: str, cfg: dict[str, Any]) -> str:
        need = user_input.strip() or _u("\\u4eca\\u5929\\u7ed9\\u60a8\\u505a\\u4e2a\\u7b80\\u5355\\u4ecb\\u7ecd")
        return _u("\\u60a8\\u597d\\uff0c\\u8fd9\\u91cc\\u662f") + cfg["product_name"] + _u("\\u4e13\\u5c5e\\u987e\\u95ee\\u3002") + need + _u("\\u3002") + cfg["product_name"] + _u("\\u7684\\u6838\\u5fc3\\u529f\\u80fd\\u662f\\uff1a") + cfg["product_features"] + _u("\\u3002\\u5b83\\u7684\\u4e3b\\u8981\\u4f18\\u52bf\\u5728\\u4e8e\\uff1a") + cfg["product_advantages"] + _u("\\u3002\\u76ee\\u524d\\u53ef\\u7533\\u8bf7\\u7684\\u4f18\\u60e0\\u8303\\u56f4\\u662f\\uff1a") + cfg["discount_range"] + _u("\\u3002\\u5982\\u679c\\u60a8\\u613f\\u610f\\uff0c\\u6211\\u53ef\\u4ee5\\u7ee7\\u7eed\\u6839\\u636e\\u60a8\\u7684\\u9884\\u7b97\\u548c\\u4f7f\\u7528\\u573a\\u666f\\uff0c\\u4e3a\\u60a8\\u63a8\\u8350\\u66f4\\u5408\\u9002\\u7684\\u8d2d\\u4e70\\u65b9\\u6848\\u3002")

    @staticmethod
    def _contains_after_sales_update(message: str) -> bool:
        prefixes = ("api_key=", "audio_output_path=", "refund_policy=", "shipping_fee_by=", "unboxing_allowed=")
        return message in CONFIRMED_VOICE_IDS or any(message.startswith(prefix) for prefix in prefixes)

    @staticmethod
    def _contains_sales_update(message: str) -> bool:
        prefixes = ("api_key=", "audio_output_path=", "product_name=", "product_features=", "product_advantages=", "discount_range=")
        return message in CONFIRMED_VOICE_IDS or any(message.startswith(prefix) for prefix in prefixes)

    @staticmethod
    def _is_confirm_message(message: str, payload: dict[str, Any]) -> bool:
        if bool(payload.get("confirm_enter")):
            return True
        compact = message.replace(" ", "")
        return (
            compact in CONFIRM_ENTER_PHRASES
            or (_u("\\u786e\\u8ba4") in compact and _u("\\u8fdb\\u5165") in compact)
            or _u("\\u5f00\\u59cb") in compact
        )

    @staticmethod
    def _is_cancel_message(message: str, payload: dict[str, Any]) -> bool:
        if bool(payload.get("cancel_enter")):
            return True
        compact = message.replace(" ", "")
        return compact in CANCEL_ENTER_PHRASES or _u("\\u53d6\\u6d88") in compact


def handle(payload: dict[str, Any]) -> dict[str, Any]:
    return VoiceMaster().handle(payload)
