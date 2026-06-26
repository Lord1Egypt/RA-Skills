#!/usr/bin/env python3
"""Generate multi-character Chinese bedtime stories with TTS synthesis."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SKILL_DIR / "outputs"

# --- Runtime settings (populated by refresh_runtime_settings) ---
LLM_BASE_URL = ""
LLM_MODEL = ""
LLM_API_KEY = ""
LLM_TIMEOUT = 90.0
LLM_TEMPERATURE = 0.7

TTS_URL = ""
TTS_MODEL = ""
TTS_API_KEY = ""
TTS_TIMEOUT = 60.0

# Voice configuration per character role
VOICE_CONFIG: dict[str, dict[str, Any]] = {
    "narrator": {"voice_id": "male_0004_a", "speed": 0.9, "pitch": 0},
    "protagonist": {"voice_id": "child_0001_a", "speed": 1.0, "pitch": 0},
    "sidekick": {"voice_id": "child_0001_b", "speed": 1.0, "pitch": 0},
    "elder": {"voice_id": "male_0018_a", "speed": 0.85, "pitch": -2},
}

# --- System prompts ---
WORLD_SYSTEM_PROMPT = (
    "你是一位专业的中文儿童故事作家，擅长创建奇幻温馨的故事世界观和角色。"
    "只输出 JSON，不要输出 Markdown。"
)

STORY_SYSTEM_PROMPT = (
    "你是一位专业的中文儿童故事作家，擅长编写适合睡前讲述的温馨故事。"
    "只输出 JSON，不要输出 Markdown。"
)

CONTINUE_SYSTEM_PROMPT = (
    "你是一位专业的中文儿童故事作家，需要根据上集摘要续写新一集故事。"
    "保持角色性格一致，情节自然衔接。"
    "只输出 JSON，不要输出 Markdown。"
)


def load_env() -> None:
    if load_dotenv is None:
        return
    for path in (SKILL_DIR / ".env", Path.cwd() / ".env"):
        if path.exists():
            load_dotenv(path)


def refresh_runtime_settings() -> None:
    global LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_TIMEOUT, LLM_TEMPERATURE
    global TTS_URL, TTS_MODEL, TTS_API_KEY, TTS_TIMEOUT

    LLM_BASE_URL = os.environ.get("STORY_LLM_BASE_URL", "https://models.audiozen.cn/v1")
    LLM_MODEL = os.environ.get("STORY_LLM_MODEL", "doubao-seed-2-0-lite-260215")
    LLM_API_KEY = os.environ.get("STORY_LLM_API_KEY", os.environ.get("IME_MODEL_API_KEY", ""))
    LLM_TIMEOUT = float(os.environ.get("STORY_LLM_TIMEOUT", "90"))
    LLM_TEMPERATURE = float(os.environ.get("STORY_LLM_TEMPERATURE", "0.7"))

    TTS_URL = os.environ.get("STORY_TTS_URL", "https://api.senseaudio.cn/v1/t2a_v2")
    TTS_MODEL = os.environ.get("STORY_TTS_MODEL", "SenseAudio-TTS-1.0")
    TTS_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
    TTS_TIMEOUT = float(os.environ.get("STORY_TTS_TIMEOUT", "60"))


def require_env(name: str, value: str) -> str:
    if value:
        return value
    raise SystemExit(f"缺少必要配置: {name}")


def build_client() -> OpenAI:
    api_key = require_env("STORY_LLM_API_KEY / IME_MODEL_API_KEY", LLM_API_KEY)
    return OpenAI(api_key=api_key, base_url=LLM_BASE_URL, timeout=LLM_TIMEOUT)


def extract_message_content(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_parts = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                text_parts.append(text)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                text_parts.append(item["text"])
        return "".join(text_parts).strip()
    raise ValueError("模型响应缺少文本内容")


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"模型未返回 JSON: {text}")
    return json.loads(text[start : end + 1])


def llm_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    client = build_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return extract_json(extract_message_content(response))


def synthesize_tts(text: str, voice_cfg: dict[str, Any], tag: str) -> bytes | None:
    """Synthesize a single TTS segment and return raw MP3 bytes."""
    if not text:
        return None
    api_key = require_env("SENSEAUDIO_API_KEY", TTS_API_KEY)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    voice_setting: dict[str, Any] = {"voice_id": voice_cfg["voice_id"]}
    if voice_cfg.get("speed") is not None and voice_cfg["speed"] != 1.0:
        voice_setting["speed"] = voice_cfg["speed"]
    if voice_cfg.get("pitch") is not None and voice_cfg["pitch"] != 0:
        voice_setting["pitch"] = voice_cfg["pitch"]

    payload = {
        "model": TTS_MODEL,
        "text": text,
        "stream": False,
        "voice_setting": voice_setting,
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    response = requests.post(TTS_URL, headers=headers, json=payload, timeout=TTS_TIMEOUT)
    response.raise_for_status()
    result = response.json()
    if result.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(result.get("base_resp", {}).get("status_msg", "TTS 调用失败"))
    audio_hex = result.get("data", {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError("TTS 响应缺少音频数据")
    return bytes.fromhex(audio_hex)


def generate_world(child_name: str, age: int, interests: str) -> dict[str, Any]:
    """Generate story world and characters via LLM."""
    user_prompt = f"""输入信息：
- 孩子姓名：{child_name}
- 孩子年龄：{age}
- 兴趣爱好：{interests}

请输出 JSON，字段包括：
- world_name: 故事世界的名称
- world_description: 世界背景描述（2-3句话）
- characters: 数组，包含4个角色，每个角色有：
  - role: narrator / protagonist / sidekick / elder
  - name: 角色名称（protagonist 默认使用孩子姓名 "{child_name}"）
  - personality: 性格描述（1句话）
  - catchphrase: 口头禅（1句话）

要求：
- 世界观要奇幻、温馨，适合{age}岁孩子
- 融入孩子的兴趣爱好元素：{interests}
- 角色性格鲜明但正面
- 语言温暖、有想象力"""
    return llm_json(WORLD_SYSTEM_PROMPT, user_prompt)


def generate_episode(world: dict[str, Any], age: int, episode: int) -> dict[str, Any]:
    """Generate a single story episode via LLM."""
    characters_text = json.dumps(world["characters"], ensure_ascii=False)
    user_prompt = f"""输入信息：
- 世界观：{world['world_name']} — {world['world_description']}
- 角色列表：{characters_text}
- 孩子年龄：{age}
- 集数：第{episode}集

请输出 JSON，字段包括：
- title: 本集标题
- segments: 数组，每个元素包含：
  - speaker: narrator / protagonist / sidekick / elder
  - text: 该角色说的话或旁白描述
- summary: 本集情节摘要（2-3句话，用于连载续写）
- cliffhanger: 悬念提示（1句话，可选）

要求：
- 生成 12-20 个 segments
- 以 narrator 开头和结尾
- 故事有起承转合，结尾温馨安宁，适合入睡
- 对话自然生动，符合角色性格
- 适合{age}岁孩子的语言水平
- 每段 text 控制在 1-3 句话"""
    return llm_json(STORY_SYSTEM_PROMPT, user_prompt)


def generate_continuation(
    world: dict[str, Any],
    age: int,
    episode: int,
    previous_summary: str,
    cliffhanger: str,
) -> dict[str, Any]:
    """Generate a continuation episode via LLM."""
    characters_text = json.dumps(world["characters"], ensure_ascii=False)
    user_prompt = f"""输入信息：
- 世界观：{world['world_name']} — {world['world_description']}
- 角色列表：{characters_text}
- 孩子年龄：{age}
- 集数：第{episode}集
- 上集摘要：{previous_summary}
- 上集悬念：{cliffhanger}

请输出 JSON，字段包括：
- title: 本集标题
- segments: 数组，每个元素包含：
  - speaker: narrator / protagonist / sidekick / elder
  - text: 该角色说的话或旁白描述
- summary: 本集情节摘要
- cliffhanger: 悬念提示（可选）

要求：
- 生成 12-20 个 segments
- 承接上集悬念自然展开
- 保持角色性格一致
- 结尾温馨安宁，适合入睡
- 每段 text 控制在 1-3 句话"""
    return llm_json(CONTINUE_SYSTEM_PROMPT, user_prompt)


def synthesize_episode(segments: list[dict[str, str]], episode: int, no_tts: bool) -> str | None:
    """Synthesize all segments to MP3 and concatenate. Returns output path or None."""
    if no_tts:
        return None

    all_audio = bytearray()
    total = len(segments)
    for i, seg in enumerate(segments):
        speaker = seg.get("speaker", "narrator")
        text = seg.get("text", "")
        voice_cfg = VOICE_CONFIG.get(speaker, VOICE_CONFIG["narrator"])

        print(f"  TTS [{i + 1}/{total}] {speaker}: {text[:30]}...")
        try:
            audio_bytes = synthesize_tts(text, voice_cfg, f"ep{episode}_seg{i}")
            if audio_bytes:
                all_audio.extend(audio_bytes)
        except Exception as exc:
            print(f"  TTS 段落 {i + 1} 合成失败: {exc}", file=sys.stderr)

    if not all_audio:
        print("所有 TTS 段落合成失败，跳过音频输出。", file=sys.stderr)
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"story_ep{episode}.mp3"
    out_path.write_bytes(bytes(all_audio))
    return str(out_path)


def save_story_text(segments: list[dict[str, str]], title: str, episode: int) -> str:
    """Save story text to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"story_ep{episode}.txt"
    lines = [f"第{episode}集：{title}\n", "=" * 40 + "\n\n"]
    for seg in segments:
        speaker = seg.get("speaker", "narrator")
        text = seg.get("text", "")
        if speaker == "narrator":
            lines.append(f"【旁白】{text}\n\n")
        else:
            name = seg.get("name", speaker)
            lines.append(f"【{name}】{text}\n\n")
    out_path.write_text("".join(lines), encoding="utf-8")
    return str(out_path)


def load_state() -> dict[str, Any] | None:
    """Load story state from file if exists."""
    state_path = OUTPUT_DIR / "story_state.json"
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return None


def save_state(state: dict[str, Any]) -> str:
    """Save story state to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    state_path = OUTPUT_DIR / "story_state.json"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(state_path)


def enrich_segments_with_names(
    segments: list[dict[str, str]], characters: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Add character names to segments for display."""
    name_map = {c["role"]: c["name"] for c in characters}
    for seg in segments:
        seg["name"] = name_map.get(seg.get("speaker", "narrator"), seg.get("speaker", "旁白"))
    return segments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成中文多角色睡前故事")
    parser.add_argument("--child-name", default="小朋友", help="孩子姓名")
    parser.add_argument("--age", type=int, default=5, help="孩子年龄")
    parser.add_argument("--interests", default="冒险,动物", help="兴趣爱好，逗号分隔")
    parser.add_argument("--continue", dest="continue_story", action="store_true",
                        help="连载模式，从上次状态续写")
    parser.add_argument("--episodes", type=int, default=1, help="生成集数")
    parser.add_argument("--no-tts", action="store_true", help="不调用 TTS，仅输出文本")
    return parser.parse_args()


def main() -> None:
    load_env()
    refresh_runtime_settings()
    args = parse_args()

    state: dict[str, Any] | None = None
    world: dict[str, Any] | None = None
    start_episode = 1

    if args.continue_story:
        state = load_state()
        if state is None:
            print("未找到 story_state.json，将创建新故事。")
        else:
            world = state["world"]
            start_episode = state["current_episode"] + 1
            args.child_name = state.get("child_name", args.child_name)
            args.age = state.get("age", args.age)
            args.interests = state.get("interests", args.interests)
            print(f"加载已有故事状态，从第 {start_episode} 集开始续写。")
            print(f"世界：{world['world_name']}")

    if world is None:
        print(f"\n正在为 {args.child_name}（{args.age}岁）创建故事世界...")
        print(f"兴趣爱好：{args.interests}")
        world = generate_world(args.child_name, args.age, args.interests)
        print(f"世界名称：{world['world_name']}")
        print(f"世界描述：{world['world_description']}")
        for char in world.get("characters", []):
            print(f"  角色 [{char['role']}] {char['name']}: {char['personality']}")

        state = {
            "child_name": args.child_name,
            "age": args.age,
            "interests": args.interests,
            "world": world,
            "episodes": [],
            "current_episode": 0,
        }

    for ep_offset in range(args.episodes):
        episode_num = start_episode + ep_offset
        print(f"\n{'=' * 50}")
        print(f"正在生成第 {episode_num} 集故事...")

        if episode_num == 1 or not state["episodes"]:
            episode_data = generate_episode(world, args.age, episode_num)
        else:
            last_ep = state["episodes"][-1]
            episode_data = generate_continuation(
                world,
                args.age,
                episode_num,
                last_ep.get("summary", ""),
                last_ep.get("cliffhanger", ""),
            )

        title = episode_data.get("title", f"第{episode_num}集")
        segments = episode_data.get("segments", [])
        summary = episode_data.get("summary", "")
        cliffhanger = episode_data.get("cliffhanger", "")

        print(f"标题：{title}")
        print(f"段落数：{len(segments)}")

        segments = enrich_segments_with_names(segments, world.get("characters", []))

        # Print story text
        print(f"\n--- 第{episode_num}集：{title} ---\n")
        for seg in segments:
            speaker = seg.get("speaker", "narrator")
            name = seg.get("name", speaker)
            text = seg.get("text", "")
            if speaker == "narrator":
                print(f"【旁白】{text}")
            else:
                print(f"【{name}】{text}")

        # Save story text
        text_path = save_story_text(segments, title, episode_num)
        print(f"\n故事文本已保存：{text_path}")

        # TTS synthesis
        audio_path = synthesize_episode(segments, episode_num, args.no_tts)
        if audio_path:
            print(f"故事音频已保存：{audio_path}")

        # Update state
        state["episodes"].append({
            "episode": episode_num,
            "title": title,
            "summary": summary,
            "cliffhanger": cliffhanger,
        })
        state["current_episode"] = episode_num
        state_path = save_state(state)

        if cliffhanger:
            print(f"悬念：{cliffhanger}")
        print(f"摘要：{summary}")

    print(f"\n故事状态已保存：{state_path}")
    print("完成！")


if __name__ == "__main__":
    main()
