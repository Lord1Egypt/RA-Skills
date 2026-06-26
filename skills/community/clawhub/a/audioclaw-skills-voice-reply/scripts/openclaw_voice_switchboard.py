#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def _bootstrap_shared_senseaudio_env() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "_shared" / "senseaudio_env.py"
        if candidate.exists():
            candidate_dir = str(candidate.parent)
            if candidate_dir not in sys.path:
                sys.path.insert(0, candidate_dir)
            from senseaudio_env import ensure_senseaudio_env
            ensure_senseaudio_env()
            return


_bootstrap_shared_senseaudio_env()

from audioclaw_paths import get_clone_voices_path
from senseaudio_api_guard import ensure_runtime_api_key
from senseaudio_tts_client import SenseAudioError, synthesize


DEFAULT_PREFERENCES_FILE = Path.home() / ".codex" / "senseaudio_openclaw_voice_preferences.json"
DEFAULT_CLONE_VOICES_FILE = get_clone_voices_path()


OFFICIAL_VOICES = [
    {
        "voice_id": "child_0001_a",
        "family": "child_0001",
        "name": "可爱萌娃",
        "tier": "free",
        "official_emotion": "开心",
        "tags": ["cheerful", "playful", "fun", "welcome"],
        "validated_access": True,
    },
    {
        "voice_id": "child_0001_b",
        "family": "child_0001",
        "name": "可爱萌娃",
        "tier": "free",
        "official_emotion": "平稳",
        "tags": ["gentle", "education", "neutral"],
        "validated_access": True,
    },
    {
        "voice_id": "male_0004_a",
        "family": "male_0004",
        "name": "儒雅道长",
        "tier": "free",
        "official_emotion": "平稳",
        "tags": ["assistant", "briefing", "knowledge", "serious", "neutral"],
        "validated_access": True,
    },
    {
        "voice_id": "male_0018_a",
        "family": "male_0018",
        "name": "沙哑青年",
        "tier": "free",
        "official_emotion": "深情",
        "tags": ["warm", "story", "gentle", "narration"],
        "validated_access": True,
    },
    {
        "voice_id": "male_0027_a",
        "family": "male_0027",
        "name": "亢奋主播",
        "tier": "trial",
        "official_emotion": "热情介绍",
        "tags": ["promo", "marketing", "launch"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0027_b",
        "family": "male_0027",
        "name": "亢奋主播",
        "tier": "trial",
        "official_emotion": "卖点解读",
        "tags": ["promo", "sales", "analysis"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0027_c",
        "family": "male_0027",
        "name": "亢奋主播",
        "tier": "trial",
        "official_emotion": "促销逼单",
        "tags": ["promo", "sales", "conversion"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0023_a",
        "family": "male_0023",
        "name": "撒娇青年",
        "tier": "trial",
        "official_emotion": "平稳",
        "tags": ["light", "playful", "neutral"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0019_a",
        "family": "male_0019",
        "name": "孔武青年",
        "tier": "paid",
        "official_emotion": "平稳",
        "tags": ["heroic", "strong", "gaming"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_a",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "平稳",
        "tags": ["lively", "neutral"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_b",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "开心",
        "tags": ["cheerful", "promo"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_c",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "撒娇",
        "tags": ["playful", "flirty"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_d",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "低落",
        "tags": ["sad"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_e",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "委屈",
        "tags": ["sad", "soft"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0033_f",
        "family": "female_0033",
        "name": "嗲嗲台妹",
        "tier": "paid",
        "official_emotion": "生气",
        "tags": ["angry"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0026_a",
        "family": "male_0026",
        "name": "乐观少年",
        "tier": "paid",
        "official_emotion": "平稳",
        "tags": ["neutral"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0026_b",
        "family": "male_0026",
        "name": "乐观少年",
        "tier": "paid",
        "official_emotion": "开心",
        "tags": ["cheerful"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0026_c",
        "family": "male_0026",
        "name": "乐观少年",
        "tier": "paid",
        "official_emotion": "深情",
        "tags": ["warm"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0006_a",
        "family": "female_0006",
        "name": "温柔御姐",
        "tier": "paid",
        "official_emotion": "深情",
        "tags": ["warm", "narration"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_a",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "内容剖析",
        "tags": ["analytical", "briefing"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_b",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "开场介绍",
        "tags": ["promo", "marketing"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_c",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "广告中插",
        "tags": ["promo", "sales"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_d",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "轻松铺陈",
        "tags": ["warm", "narration"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_e",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "细心提问",
        "tags": ["warm", "customer_support"],
        "validated_access": False,
    },
    {
        "voice_id": "male_0028_f",
        "family": "male_0028",
        "name": "可靠青叔",
        "tier": "paid",
        "official_emotion": "主题升华",
        "tags": ["analytical", "serious"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_a",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "平稳",
        "tags": ["neutral"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_b",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "撒娇",
        "tags": ["playful"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_c",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "病娇",
        "tags": ["gaming", "playful"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_d",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "低落",
        "tags": ["sad"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_e",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "妩媚",
        "tags": ["playful", "promo"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0027_f",
        "family": "female_0027",
        "name": "魅力姐姐",
        "tier": "paid",
        "official_emotion": "傲娇",
        "tags": ["gaming", "playful"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0008_a",
        "family": "female_0008",
        "name": "气质学姐",
        "tier": "paid",
        "official_emotion": "生气",
        "tags": ["angry", "warning"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0008_b",
        "family": "female_0008",
        "name": "气质学姐",
        "tier": "paid",
        "official_emotion": "开心",
        "tags": ["cheerful"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0008_c",
        "family": "female_0008",
        "name": "气质学姐",
        "tier": "paid",
        "official_emotion": "平稳",
        "tags": ["neutral"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_a",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "内容剖析",
        "tags": ["analytical", "briefing"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_b",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "开场介绍",
        "tags": ["promo", "marketing"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_c",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "广告中插",
        "tags": ["promo", "sales"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_d",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "轻松铺陈",
        "tags": ["warm", "narration"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_e",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "细心提问",
        "tags": ["warm", "customer_support"],
        "validated_access": False,
    },
    {
        "voice_id": "female_0035_f",
        "family": "female_0035",
        "name": "知心少女",
        "tier": "paid",
        "official_emotion": "主题升华",
        "tags": ["analytical", "serious"],
        "validated_access": False,
    },
]


EMOTION_PRESETS = {
    "neutral": {
        "official_emotions": ["平稳"],
        "tags": ["neutral", "assistant"],
        "speed": 1.0,
        "pitch": 0,
        "volume": 1.0,
    },
    "calm": {
        "official_emotions": ["平稳", "主题升华", "内容剖析"],
        "tags": ["assistant", "briefing", "knowledge", "serious"],
        "speed": 0.96,
        "pitch": -1,
        "volume": 1.0,
    },
    "warm": {
        "official_emotions": ["深情", "轻松铺陈", "细心提问"],
        "tags": ["warm", "narration", "customer_support", "story"],
        "speed": 0.94,
        "pitch": -1,
        "volume": 1.02,
    },
    "cheerful": {
        "official_emotions": ["开心", "热情介绍", "开场介绍"],
        "tags": ["cheerful", "playful", "welcome", "marketing"],
        "speed": 1.08,
        "pitch": 2,
        "volume": 1.04,
    },
    "serious": {
        "official_emotions": ["平稳", "内容剖析", "主题升华"],
        "tags": ["serious", "briefing", "warning"],
        "speed": 0.92,
        "pitch": -2,
        "volume": 1.0,
    },
    "promo": {
        "official_emotions": ["卖点解读", "促销逼单", "广告中插", "热情介绍"],
        "tags": ["promo", "sales", "marketing", "launch"],
        "speed": 1.1,
        "pitch": 1,
        "volume": 1.08,
    },
    "sad": {
        "official_emotions": ["低落", "委屈"],
        "tags": ["sad"],
        "speed": 0.9,
        "pitch": -2,
        "volume": 0.95,
    },
    "angry": {
        "official_emotions": ["生气"],
        "tags": ["angry", "warning"],
        "speed": 1.02,
        "pitch": 1,
        "volume": 1.08,
    },
    "analytical": {
        "official_emotions": ["内容剖析", "主题升华"],
        "tags": ["analytical", "briefing", "knowledge"],
        "speed": 0.97,
        "pitch": 0,
        "volume": 1.0,
    },
}


SCENE_HINTS = {
    "assistant": ["male_0004_a", "male_0018_a", "child_0001_b"],
    "customer_support": ["male_0004_a", "male_0018_a", "child_0001_b"],
    "briefing": ["male_0004_a", "male_0018_a"],
    "sales": ["male_0027_b", "male_0027_c", "male_0018_a", "child_0001_a"],
    "marketing": ["male_0027_a", "female_0033_b", "child_0001_a", "male_0018_a"],
    "narration": ["male_0018_a", "female_0006_a", "male_0004_a"],
    "education": ["child_0001_b", "male_0004_a"],
    "gaming": ["male_0019_a", "female_0027_f", "male_0018_a"],
    "warning": ["female_0008_a", "male_0004_a"],
}


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def get_voice(voice_id: str) -> Optional[Dict[str, object]]:
    for voice in OFFICIAL_VOICES:
        if voice["voice_id"] == voice_id:
            return voice
    return None


def load_clone_voices(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"voices": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"voices": {}}
    if not isinstance(data, dict):
        return {"voices": {}}
    voices = data.get("voices")
    if not isinstance(voices, dict):
        data["voices"] = {}
    return data


def save_clone_voices(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_custom_voice_entry(
    voice_id: str,
    *,
    name: str = "",
    validated_access: bool = False,
    source: str = "custom",
) -> Dict[str, object]:
    family = voice_id.split("_", 1)[0] if "_" in voice_id else voice_id.split("-", 1)[0]
    if voice_id.startswith("vc-"):
        family = "clone_voice"
    return {
        "voice_id": voice_id,
        "family": family or "custom",
        "name": name or ("Cloned Voice" if voice_id.startswith("vc-") else "Custom Voice"),
        "tier": "clone" if voice_id.startswith("vc-") else "custom",
        "official_emotion": "自定义",
        "tags": ["custom", "clone"] if voice_id.startswith("vc-") else ["custom"],
        "validated_access": validated_access,
        "source": source,
    }


def get_clone_voice_entry(clone_data: Dict[str, object], voice_id: str) -> Optional[Dict[str, object]]:
    voices = clone_data.get("voices")
    if not isinstance(voices, dict):
        return None
    raw = voices.get(voice_id)
    if not isinstance(raw, dict):
        return None
    return build_custom_voice_entry(
        voice_id,
        name=str(raw.get("name") or ""),
        validated_access=bool(raw.get("validated_access", False)),
        source=str(raw.get("source") or "registered_clone"),
    )


def upsert_clone_voice(
    clone_data: Dict[str, object],
    *,
    voice_id: str,
    name: str = "",
    validated_access: Optional[bool] = None,
    source: str = "registered_clone",
) -> Dict[str, object]:
    voices = clone_data.setdefault("voices", {})
    if not isinstance(voices, dict):
        clone_data["voices"] = {}
        voices = clone_data["voices"]
    entry = voices.get(voice_id)
    if not isinstance(entry, dict):
        entry = {}
    entry["voice_id"] = voice_id
    if name:
        entry["name"] = name
    elif "name" not in entry:
        entry["name"] = "Cloned Voice" if voice_id.startswith("vc-") else "Custom Voice"
    if validated_access is not None:
        entry["validated_access"] = bool(validated_access)
    elif "validated_access" not in entry:
        entry["validated_access"] = False
    entry["source"] = source
    voices[voice_id] = entry
    return entry


def all_voices(clone_data: Dict[str, object]) -> List[Dict[str, object]]:
    voices: List[Dict[str, object]] = list(OFFICIAL_VOICES)
    raw = clone_data.get("voices")
    if isinstance(raw, dict):
        for voice_id, payload in raw.items():
            if any(item["voice_id"] == voice_id for item in voices):
                continue
            if not isinstance(payload, dict):
                payload = {}
            voices.append(
                build_custom_voice_entry(
                    voice_id,
                    name=str(payload.get("name") or ""),
                    validated_access=bool(payload.get("validated_access", False)),
                    source=str(payload.get("source") or "registered_clone"),
                )
            )
    return voices


def load_preferences(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"users": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"users": {}}
    if not isinstance(data, dict):
        return {"users": {}}
    users = data.get("users")
    if not isinstance(users, dict):
        data["users"] = {}
    return data


def save_preferences(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_reply_mode(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"voice", "text", "auto"}:
        return normalized
    raise SystemExit("reply_mode must be one of: voice, text, auto")


def get_preference(data: Dict[str, object], key: str) -> Dict[str, object]:
    users = data.setdefault("users", {})
    entry = users.get(key)
    return entry if isinstance(entry, dict) else {}


def update_preference(
    data: Dict[str, object],
    key: str,
    *,
    reply_mode: Optional[str] = None,
    default_voice_id: Optional[str] = None,
    default_emotion: Optional[str] = None,
    default_scene: Optional[str] = None,
) -> Dict[str, object]:
    users = data.setdefault("users", {})
    entry = users.get(key)
    if not isinstance(entry, dict):
        entry = {}

    if reply_mode is not None:
        entry["reply_mode"] = normalize_reply_mode(reply_mode)
    if default_voice_id is not None:
        entry["default_voice_id"] = default_voice_id
    if default_emotion is not None:
        entry["default_emotion"] = str(default_emotion).strip().lower()
    if default_scene is not None:
        entry["default_scene"] = default_scene

    users[key] = entry
    return entry


def apply_preference_defaults(request: Dict[str, object], preference: Dict[str, object]) -> None:
    if not preference:
        return
    if request.get("reply_mode") is None and preference.get("reply_mode") is not None:
        request["reply_mode"] = preference["reply_mode"]
    if request.get("voice_id") is None and preference.get("default_voice_id") is not None:
        request["voice_id"] = preference["default_voice_id"]
    if request.get("emotion") is None and preference.get("default_emotion") is not None:
        request["emotion"] = preference["default_emotion"]
    if request.get("scene") is None and preference.get("default_scene") is not None:
        request["scene"] = preference["default_scene"]


def load_request(args: argparse.Namespace) -> Dict[str, object]:
    if args.request_file and args.request_json:
        raise SystemExit("Use either --request-file or --request-json, not both.")

    request: Dict[str, object] = {}
    if args.request_file:
        request = json.loads(Path(args.request_file).read_text(encoding="utf-8"))
    elif args.request_json:
        request = json.loads(args.request_json)

    direct = {
        "text": args.text,
        "scene": args.scene,
        "voice_id": args.voice_id,
        "voice_family": args.voice_family,
        "emotion": args.emotion,
        "speed": args.speed,
        "pitch": args.pitch,
        "volume": args.volume,
        "audio_format": args.format,
        "sample_rate": args.sample_rate,
        "delivery_profile": args.delivery_profile,
        "ffmpeg_exe": args.ffmpeg_exe,
        "allow_fallback": args.allow_fallback,
        "strict_voice": args.strict_voice,
        "cache_dir": args.cache_dir,
        "validated_only": args.validated_only,
        "preference_key": args.preference_key,
        "reply_mode": args.reply_mode,
    }
    for key, value in direct.items():
        if value is not None:
            request[key] = value

    if "text" not in request or not str(request["text"]).strip():
        raise SystemExit("Request must contain non-empty text.")
    return request


def score_voice(
    voice: Dict[str, object],
    *,
    preset: Dict[str, object],
    scene: str,
    validated_only: bool,
) -> int:
    if validated_only and not bool(voice.get("validated_access")):
        return -10_000

    score = 0
    if bool(voice.get("validated_access")):
        score += 20

    official_emotion = str(voice.get("official_emotion") or "")
    if official_emotion in preset["official_emotions"]:
        score += 50
    tags = set(voice.get("tags") or [])
    if scene in tags:
        score += 25

    for tag in preset["tags"]:
        if tag in tags:
            score += 8

    scene_hints = SCENE_HINTS.get(scene, [])
    if str(voice.get("voice_id") or "") in scene_hints:
        score += max(15 - scene_hints.index(str(voice.get("voice_id") or "")) * 3, 1)

    return score


def resolve_voice(request: Dict[str, object], validated_only: bool, clone_data: Dict[str, object]) -> Dict[str, object]:
    emotion = str(request.get("emotion") or "neutral").strip().lower()
    scene = str(request.get("scene") or "assistant").strip()
    preset = EMOTION_PRESETS.get(emotion, EMOTION_PRESETS["neutral"])
    voices = all_voices(clone_data)

    requested_voice_id = request.get("voice_id")
    if requested_voice_id:
        voice = get_voice(str(requested_voice_id))
        if not voice:
            voice = get_clone_voice_entry(clone_data, str(requested_voice_id))
        if voice:
            return {
                "voice": voice,
                "resolution_mode": "exact_voice_id",
                "emotion_strategy": "parameter_shaping",
                "preset": preset,
            }
        return {
            "voice": build_custom_voice_entry(str(requested_voice_id), source="explicit_voice_id"),
            "resolution_mode": "exact_voice_id",
            "emotion_strategy": "parameter_shaping",
            "preset": preset,
        }

    requested_family = request.get("voice_family")
    if requested_family:
        family_candidates = [
            voice
            for voice in voices
            if voice["family"] == requested_family
            and (bool(voice.get("validated_access")) or not validated_only)
        ]
        family_candidates.sort(
            key=lambda voice: score_voice(voice, preset=preset, scene=scene, validated_only=validated_only),
            reverse=True,
        )
        if family_candidates:
            best = family_candidates[0]
            emotion_strategy = "voice_variant"
            if str(best["official_emotion"]) not in preset["official_emotions"]:
                emotion_strategy = "parameter_shaping"
            return {
                "voice": best,
                "resolution_mode": "family_emotion_variant",
                "emotion_strategy": emotion_strategy,
                "preset": preset,
            }

    candidates = sorted(
        voices,
        key=lambda voice: score_voice(voice, preset=preset, scene=scene, validated_only=validated_only),
        reverse=True,
    )
    best = next(
        (
            voice
            for voice in candidates
            if score_voice(voice, preset=preset, scene=scene, validated_only=validated_only) > -1_000
        ),
        None,
    )
    if not best and validated_only:
        return resolve_voice(request, validated_only=False, clone_data=clone_data)
    if not best:
        raise SystemExit("No compatible voice candidate found.")

    emotion_strategy = "voice_variant"
    if str(best["official_emotion"]) not in preset["official_emotions"]:
        emotion_strategy = "parameter_shaping"
    return {
        "voice": best,
        "resolution_mode": "scene_emotion_match",
        "emotion_strategy": emotion_strategy,
        "preset": preset,
    }


def build_effective_settings(request: Dict[str, object], resolved: Dict[str, object]) -> Dict[str, object]:
    preset = resolved["preset"]
    speed = float(request.get("speed") if request.get("speed") is not None else preset["speed"])
    pitch = int(request.get("pitch") if request.get("pitch") is not None else preset["pitch"])
    volume = float(request.get("volume") if request.get("volume") is not None else preset["volume"])

    return {
        "speed": round(clamp(speed, 0.5, 2.0), 3),
        "pitch": int(clamp(pitch, -12, 12)),
        "volume": round(clamp(volume, 0.0, 10.0), 3),
        "audio_format": str(request.get("audio_format") or "mp3"),
        "sample_rate": int(request.get("sample_rate") or 32000),
    }


def is_access_error(exc: SenseAudioError) -> bool:
    haystack = f"{exc} {exc.raw_body or ''}".lower()
    return "no access" in haystack or "permission" in haystack or "403" in haystack


def cache_path_for(cache_dir: Path, text: str, voice_id: str, settings: Dict[str, object]) -> Path:
    digest = hashlib.sha256(
        json.dumps(
            {
                "text": text,
                "voice_id": voice_id,
                "settings": settings,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    extension = settings["audio_format"]
    return cache_dir / f"{digest}.{extension}"


def delivery_cache_path_for(
    cache_dir: Path,
    source_cache_file: Path,
    delivery_profile: str,
    extension: str,
) -> Path:
    digest = hashlib.sha256(
        json.dumps(
            {
                "source_cache_file": str(source_cache_file),
                "delivery_profile": delivery_profile,
                "extension": extension,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return cache_dir / f"{digest}.{extension}"


def default_workspace_output_path(
    workspace_root: Path,
    *,
    text: str,
    voice_id: str,
    emotion: str,
    delivery_profile: str,
    settings: Dict[str, object],
) -> Path:
    extension = "ogg" if delivery_profile == "feishu_voice" else str(settings["audio_format"])
    digest = hashlib.sha256(
        json.dumps(
            {
                "text": text,
                "voice_id": voice_id,
                "emotion": emotion,
                "delivery_profile": delivery_profile,
                "extension": extension,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:12]
    safe_voice = voice_id.replace("/", "_")
    safe_emotion = (emotion or "neutral").replace("/", "_")
    outdir = workspace_root / "state" / "audio"
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir / f"{safe_voice}_{safe_emotion}_{digest}.{extension}"


def output_from_cache(cache_file: Path, out_path: Optional[Path]) -> Path:
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cache_file, out_path)
        return out_path
    return cache_file


def parse_file_mode(value: str) -> int:
    try:
        return int(str(value), 8)
    except ValueError as exc:
        raise SystemExit("--chmod must be an octal mode such as 644 or 640.") from exc


def ensure_file_mode(path: Path, mode: int) -> None:
    try:
        path.chmod(mode)
    except OSError:
        return


def build_openclaw_media_reference(final_path: Path, workspace_root: Optional[Path]) -> str:
    if workspace_root is None:
        return ""
    try:
        relative = final_path.resolve().relative_to(workspace_root.resolve())
    except ValueError:
        return ""
    return f"MEDIA:./{relative.as_posix()}"


def normalize_delivery_profile(value: object) -> str:
    profile = str(value or "default").strip().lower()
    if profile not in {"default", "feishu_voice"}:
        raise SystemExit("delivery_profile must be one of: default, feishu_voice")
    return profile


def delivery_extension_for(profile: str, out_path: Optional[Path]) -> str:
    if profile != "feishu_voice":
        return out_path.suffix.lstrip(".").lower() if out_path and out_path.suffix else ""
    if out_path and out_path.suffix.lower() in {".ogg", ".opus"}:
        return out_path.suffix.lstrip(".").lower()
    return "ogg"


def resolve_ffmpeg_exe(explicit: Optional[str]) -> str:
    if explicit:
        return str(Path(explicit).expanduser())
    bundled = Path(__file__).resolve().parent.parent / "assets" / "ffmpeg-macos-aarch64-v7.1"
    if bundled.exists():
        return str(bundled)
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:  # pragma: no cover - fallback path
        raise SystemExit(
            "Feishu voice delivery needs ffmpeg. Install ffmpeg or `python3 -m pip install imageio-ffmpeg`."
        ) from exc


def transcode_for_delivery(source_path: Path, target_path: Path, *, profile: str, ffmpeg_exe: str) -> None:
    if profile != "feishu_voice":
        if source_path != target_path:
            shutil.copyfile(source_path, target_path)
        return

    if target_path.suffix.lower() not in {".ogg", ".opus"}:
        raise SystemExit("feishu_voice delivery requires an output suffix of .ogg or .opus")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg_exe,
        "-y",
        "-i",
        str(source_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "24000",
        "-c:a",
        "libopus",
        "-b:a",
        "48k",
        str(target_path),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise SystemExit(f"ffmpeg transcoding failed: {stderr or exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenClaw voice router for SenseAudio.")
    parser.add_argument("--request-file")
    parser.add_argument("--request-json")
    parser.add_argument("--text")
    parser.add_argument("--scene")
    parser.add_argument("--voice-id")
    parser.add_argument("--voice-family")
    parser.add_argument("--emotion")
    parser.add_argument("--speed", type=float)
    parser.add_argument("--pitch", type=int)
    parser.add_argument("--volume", type=float)
    parser.add_argument("--format", choices=["mp3", "wav", "pcm", "flac"])
    parser.add_argument("--sample-rate", type=int)
    parser.add_argument("--delivery-profile", choices=["default", "feishu_voice"])
    parser.add_argument("--ffmpeg-exe")
    parser.add_argument("--out")
    parser.add_argument("--cache-dir")
    parser.add_argument("--chmod", default="644")
    parser.add_argument("--openclaw-workspace-root")
    parser.add_argument("--preferences-file")
    parser.add_argument("--clone-voices-file")
    parser.add_argument("--preference-key")
    parser.add_argument("--reply-mode", choices=["voice", "text", "auto"])
    parser.add_argument("--set-reply-mode", choices=["voice", "text", "auto"])
    parser.add_argument("--set-default-voice-id")
    parser.add_argument("--set-default-emotion")
    parser.add_argument("--set-default-scene")
    parser.add_argument("--show-preference", action="store_true")
    parser.add_argument("--show-clone-voices", action="store_true")
    parser.add_argument("--register-clone-voice-id")
    parser.add_argument("--register-clone-name")
    parser.add_argument("--remove-clone-voice-id")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    parser.add_argument("--list-voices", action="store_true")
    parser.add_argument("--list-emotions", action="store_true")
    parser.add_argument("--list-scenes", action="store_true")
    parser.add_argument("--allow-fallback", dest="allow_fallback", action="store_true")
    parser.add_argument("--no-fallback", dest="allow_fallback", action="store_false")
    parser.add_argument("--strict-voice", dest="strict_voice", action="store_true")
    parser.add_argument("--no-strict-voice", dest="strict_voice", action="store_false")
    parser.add_argument("--validated-only", dest="validated_only", action="store_true")
    parser.add_argument("--no-validated-only", dest="validated_only", action="store_false")
    parser.set_defaults(allow_fallback=None, strict_voice=None, validated_only=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    clone_voices_path = Path(
        args.clone_voices_file
        or os.getenv("SENSEAUDIO_CLONE_VOICES_FILE")
        or DEFAULT_CLONE_VOICES_FILE
    )
    clone_data = load_clone_voices(clone_voices_path)

    if args.list_voices:
        json.dump(all_voices(clone_data), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.list_emotions:
        json.dump(EMOTION_PRESETS, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.list_scenes:
        json.dump(SCENE_HINTS, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    preferences_path = Path(
        args.preferences_file
        or os.getenv("SENSEAUDIO_VOICE_PREFERENCES_FILE")
        or DEFAULT_PREFERENCES_FILE
    )
    file_mode = parse_file_mode(args.chmod)
    workspace_root = Path(args.openclaw_workspace_root).expanduser() if args.openclaw_workspace_root else None
    preferences_data = load_preferences(preferences_path)

    if args.register_clone_voice_id:
        entry = upsert_clone_voice(
            clone_data,
            voice_id=str(args.register_clone_voice_id).strip(),
            name=str(args.register_clone_name or "").strip(),
            source="manual_registration",
        )
        save_clone_voices(clone_voices_path, clone_data)
        json.dump(
            {
                "clone_voices_file": str(clone_voices_path),
                "registered": entry,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    if args.remove_clone_voice_id:
        voices = clone_data.get("voices")
        removed = None
        if isinstance(voices, dict):
            removed = voices.pop(str(args.remove_clone_voice_id).strip(), None)
        save_clone_voices(clone_voices_path, clone_data)
        json.dump(
            {
                "clone_voices_file": str(clone_voices_path),
                "removed": removed,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    if args.show_clone_voices:
        json.dump(
            {
                "clone_voices_file": str(clone_voices_path),
                "voices": clone_data.get("voices", {}),
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    wants_preference_op = any(
        [
            args.show_preference,
            args.set_reply_mode is not None,
            args.set_default_voice_id is not None,
            args.set_default_emotion is not None,
            args.set_default_scene is not None,
        ]
    )
    if wants_preference_op:
        if not args.preference_key:
            raise SystemExit("--preference-key is required for preference operations.")
        if (
            args.set_reply_mode is not None
            or args.set_default_voice_id is not None
            or args.set_default_emotion is not None
            or args.set_default_scene is not None
        ):
            preference = update_preference(
                preferences_data,
                args.preference_key,
                reply_mode=args.set_reply_mode,
                default_voice_id=args.set_default_voice_id,
                default_emotion=args.set_default_emotion,
                default_scene=args.set_default_scene,
            )
            save_preferences(preferences_path, preferences_data)
            if args.set_default_voice_id and str(args.set_default_voice_id).startswith("vc-"):
                upsert_clone_voice(
                    clone_data,
                    voice_id=str(args.set_default_voice_id),
                    source="preference_default",
                )
                save_clone_voices(clone_voices_path, clone_data)
        else:
            preference = get_preference(preferences_data, args.preference_key)

        if not any([args.request_file, args.request_json, args.text]):
            result = {
                "preference_key": args.preference_key,
                "preferences_file": str(preferences_path),
                "preference": preference,
            }
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return 0

    api_key = ensure_runtime_api_key(os.getenv(args.api_key_env), args.api_key_env, purpose="tts")

    request = load_request(args)
    preference_key = request.get("preference_key")
    preference = {}
    if preference_key:
        preference = get_preference(preferences_data, str(preference_key))
        apply_preference_defaults(request, preference)
    effective_reply_mode = normalize_reply_mode(request.get("reply_mode")) or "voice"
    request["reply_mode"] = effective_reply_mode
    delivery_profile = normalize_delivery_profile(request.get("delivery_profile"))
    request["delivery_profile"] = delivery_profile

    if effective_reply_mode != "voice":
        manifest = {
            "request": request,
            "delivery": {
                "reply_mode": effective_reply_mode,
                "voice_enabled": False,
                "mode_source": "preference" if preference_key and preference.get("reply_mode") else "request",
                "preference_key": preference_key or "",
                "preferences_file": str(preferences_path),
                "delivery_profile": delivery_profile,
                "file_mode": oct(file_mode),
                "openclaw_media_reference": "",
            },
            "audio": None,
        }
        json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    text = str(request["text"]).strip()
    resolved = resolve_voice(request, validated_only=bool(request.get("validated_only", False)), clone_data=clone_data)
    settings = build_effective_settings(request, resolved)
    selected_voice = resolved["voice"]

    cache_dir = Path(str(request.get("cache_dir") or args.cache_dir or "/tmp/openclaw_voice_switchboard_cache"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    requested_out_path = Path(args.out).expanduser() if args.out else None
    out_path = requested_out_path
    if out_path is None and workspace_root is not None:
        out_path = default_workspace_output_path(
            workspace_root,
            text=text,
            voice_id=str(selected_voice["voice_id"]),
            emotion=str(request.get("emotion") or "neutral"),
            delivery_profile=delivery_profile,
            settings=settings,
        )
    delivery_extension = delivery_extension_for(delivery_profile, out_path)
    if delivery_profile == "feishu_voice" and out_path and out_path.suffix.lower() not in {".ogg", ".opus"}:
        raise SystemExit("Use an .ogg or .opus output path when delivery_profile is feishu_voice.")
    ffmpeg_exe = resolve_ffmpeg_exe(str(request.get("ffmpeg_exe") or args.ffmpeg_exe or "")) if delivery_profile == "feishu_voice" else ""
    primary_cache_file = cache_path_for(cache_dir, text, str(selected_voice["voice_id"]), settings)
    primary_delivery_cache_file = (
        delivery_cache_path_for(cache_dir, primary_cache_file, delivery_profile, delivery_extension or settings["audio_format"])
        if delivery_profile != "default"
        else primary_cache_file
    )

    if primary_delivery_cache_file.exists():
        final_path = output_from_cache(primary_delivery_cache_file, out_path)
        ensure_file_mode(primary_delivery_cache_file, file_mode)
        if primary_cache_file.exists():
            ensure_file_mode(primary_cache_file, file_mode)
        ensure_file_mode(primary_cache_file, file_mode)
        ensure_file_mode(final_path, file_mode)
        manifest = {
            "request": request,
            "delivery": {
                "reply_mode": effective_reply_mode,
                "voice_enabled": True,
                "mode_source": "preference" if preference_key and preference.get("reply_mode") else "request",
                "preference_key": preference_key or "",
                "preferences_file": str(preferences_path),
                "delivery_profile": delivery_profile,
                "file_mode": oct(file_mode),
                "openclaw_media_reference": build_openclaw_media_reference(final_path, workspace_root),
            },
            "resolved": {
                "voice_id": selected_voice["voice_id"],
                "family": selected_voice["family"],
                "voice_name": selected_voice["name"],
                "official_emotion": selected_voice["official_emotion"],
                "resolution_mode": resolved["resolution_mode"],
                "emotion_strategy": resolved["emotion_strategy"],
                "validated_access": selected_voice["validated_access"],
                "settings": settings,
            },
            "audio": {
                "path": str(final_path),
                "cache_path": str(primary_delivery_cache_file),
                "source_cache_path": str(primary_cache_file),
                "cache_hit": True,
                "bytes": primary_delivery_cache_file.stat().st_size,
                "trace_id": None,
            },
        }
        json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    attempt_voices: List[Dict[str, object]] = [selected_voice]
    if request.get("allow_fallback", args.allow_fallback):
        fallback = resolve_voice(
            {
                **request,
                "voice_id": None,
                "voice_family": None,
            },
            validated_only=True,
            clone_data=clone_data,
        )["voice"]
        if fallback["voice_id"] != selected_voice["voice_id"]:
            attempt_voices.append(fallback)

    last_exc: Optional[SenseAudioError] = None
    final_trace_id = None
    final_voice = None
    extra_info = None
    model_used = None
    final_source_cache_file = None
    final_delivery_cache_file = None
    final_cache_hit = False

    for index, voice in enumerate(attempt_voices):
        attempt_cache_file = cache_path_for(cache_dir, text, str(voice["voice_id"]), settings)
        attempt_delivery_cache_file = (
            delivery_cache_path_for(
                cache_dir,
                attempt_cache_file,
                delivery_profile,
                delivery_extension or settings["audio_format"],
            )
            if delivery_profile != "default"
            else attempt_cache_file
        )
        if attempt_delivery_cache_file.exists():
            final_voice = voice
            final_source_cache_file = attempt_cache_file
            final_delivery_cache_file = attempt_delivery_cache_file
            final_cache_hit = True
            break
        try:
            if not attempt_cache_file.exists():
                result = synthesize(
                    api_key=api_key,
                    text=text,
                    voice_id=str(voice["voice_id"]),
                    audio_format=str(settings["audio_format"]),
                    sample_rate=int(settings["sample_rate"]),
                    speed=float(settings["speed"]),
                    volume=float(settings["volume"]),
                    pitch=int(settings["pitch"]),
                )
                attempt_cache_file.write_bytes(result.audio_bytes)
                final_trace_id = result.trace_id
                extra_info = result.extra_info
                model_used = result.model_used
            else:
                result = None
            ensure_file_mode(attempt_cache_file, file_mode)
            if delivery_profile == "default":
                attempt_delivery_cache_file = attempt_cache_file
            else:
                transcode_for_delivery(
                    attempt_cache_file,
                    attempt_delivery_cache_file,
                    profile=delivery_profile,
                    ffmpeg_exe=ffmpeg_exe,
                )
                ensure_file_mode(attempt_delivery_cache_file, file_mode)
            final_voice = voice
            final_source_cache_file = attempt_cache_file
            final_delivery_cache_file = attempt_delivery_cache_file
            final_cache_hit = False
            if str(voice.get("voice_id") or "").startswith("vc-"):
                upsert_clone_voice(
                    clone_data,
                    voice_id=str(voice["voice_id"]),
                    name=str(voice.get("name") or ""),
                    validated_access=True,
                    source=str(voice.get("source") or "runtime_success"),
                )
                save_clone_voices(clone_voices_path, clone_data)
            break
        except SenseAudioError as exc:
            last_exc = exc
            should_try_next = index < len(attempt_voices) - 1 and not request.get("strict_voice", args.strict_voice)
            if should_try_next and not voice["validated_access"]:
                continue
            if should_try_next and is_access_error(exc):
                continue
            if index == len(attempt_voices) - 1 or request.get("strict_voice", args.strict_voice) or not is_access_error(exc):
                raise

    if final_voice is None:
        raise last_exc or SystemExit("Failed to synthesize audio.")

    if final_source_cache_file is None or final_delivery_cache_file is None:
        raise SystemExit("Missing cache path for resolved voice.")

    final_path = output_from_cache(final_delivery_cache_file, out_path)
    ensure_file_mode(final_source_cache_file, file_mode)
    ensure_file_mode(final_delivery_cache_file, file_mode)
    ensure_file_mode(final_path, file_mode)
    resolution_mode = resolved["resolution_mode"]
    emotion_strategy = resolved["emotion_strategy"]
    if final_voice["voice_id"] != selected_voice["voice_id"]:
        resolution_mode = "validated_fallback"
        emotion_strategy = "validated_fallback"
    manifest = {
        "request": request,
        "delivery": {
            "reply_mode": effective_reply_mode,
            "voice_enabled": True,
            "mode_source": "preference" if preference_key and preference.get("reply_mode") else "request",
            "preference_key": preference_key or "",
            "preferences_file": str(preferences_path),
            "delivery_profile": delivery_profile,
            "file_mode": oct(file_mode),
            "openclaw_media_reference": build_openclaw_media_reference(final_path, workspace_root),
        },
        "resolved": {
            "voice_id": final_voice["voice_id"],
            "family": final_voice["family"],
            "voice_name": final_voice["name"],
            "official_emotion": final_voice["official_emotion"],
            "resolution_mode": resolution_mode,
            "emotion_strategy": emotion_strategy,
            "validated_access": final_voice["validated_access"],
            "settings": settings,
        },
        "audio": {
            "path": str(final_path),
            "cache_path": str(final_delivery_cache_file),
            "source_cache_path": str(final_source_cache_file),
            "cache_hit": final_cache_hit,
            "bytes": final_delivery_cache_file.stat().st_size,
            "trace_id": final_trace_id,
            "extra_info": extra_info,
            "model_used": model_used,
        },
    }
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
