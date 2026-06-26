#!/usr/bin/env python3
"""Run a Chinese voice detective mystery game with LLM, ASR, and TTS."""

from __future__ import annotations

import argparse
import json
import os
import sys
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

# --- Runtime settings ---
LLM_BASE_URL = ""
LLM_MODEL = ""
LLM_API_KEY = ""
LLM_TIMEOUT = 120.0
LLM_TEMPERATURE = 0.5

ASR_URL = ""
ASR_MODEL = ""
ASR_API_KEY = ""
ASR_TIMEOUT = 300.0

TTS_URL = ""
TTS_MODEL = ""
TTS_API_KEY = ""
TTS_TIMEOUT = 60.0

# Voice configuration per character role
VOICE_CONFIG: dict[str, dict[str, Any]] = {
    "narrator": {"voice_id": "child_0001_a", "speed": 0.85, "pitch": -1},
    "suspect_a": {"voice_id": "male_0004_a", "speed": 1.0, "pitch": 0},
    "suspect_b": {"voice_id": "male_0018_a", "speed": 1.1, "pitch": 0},
    "suspect_c": {"voice_id": "child_0001_b", "speed": 1.0, "pitch": 2},
}

MAX_INTERROGATION_ROUNDS = 5
COMPRESS_AFTER_ROUNDS = 4

# --- System prompts ---
CASE_SYSTEM_PROMPT = (
    "你是一位推理小说作家，擅长创建逻辑严密的中文侦探推理案件。"
    "只输出 JSON，不要输出 Markdown。"
)

INTERROGATION_SYSTEM_PROMPT = (
    "你正在扮演一个嫌疑人接受审讯。"
    "完全以角色身份回答，符合性格特点。"
    "只输出 JSON，不要输出 Markdown。"
)

EXAMINE_SYSTEM_PROMPT = (
    "你是案件的旁白，需要描述侦探勘察现场的发现。"
    "描述要有画面感和氛围。"
    "只输出 JSON，不要输出 Markdown。"
)

ACCUSE_SYSTEM_PROMPT = (
    "你是公正的案件评审官，需要评估侦探的指控并给出评分。"
    "只输出 JSON，不要输出 Markdown。"
)

COMPRESS_SYSTEM_PROMPT = (
    "你需要将审讯对话历史压缩为摘要，保留关键信息和矛盾点。"
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
    global ASR_URL, ASR_MODEL, ASR_API_KEY, ASR_TIMEOUT
    global TTS_URL, TTS_MODEL, TTS_API_KEY, TTS_TIMEOUT

    LLM_BASE_URL = os.environ.get("MYSTERY_LLM_BASE_URL", "https://models.audiozen.cn/v1")
    LLM_MODEL = os.environ.get("MYSTERY_LLM_MODEL", "doubao-seed-2-0-lite-260215")
    LLM_API_KEY = os.environ.get("MYSTERY_LLM_API_KEY", os.environ.get("IME_MODEL_API_KEY", ""))
    LLM_TIMEOUT = float(os.environ.get("MYSTERY_LLM_TIMEOUT", "120"))
    LLM_TEMPERATURE = float(os.environ.get("MYSTERY_LLM_TEMPERATURE", "0.5"))

    ASR_URL = os.environ.get("MYSTERY_ASR_URL", "https://api.senseaudio.cn/v1/audio/transcriptions")
    ASR_MODEL = os.environ.get("MYSTERY_ASR_MODEL", "sense-asr-pro")
    ASR_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
    ASR_TIMEOUT = float(os.environ.get("MYSTERY_ASR_TIMEOUT", "300"))

    TTS_URL = os.environ.get("MYSTERY_TTS_URL", "https://api.senseaudio.cn/v1/t2a_v2")
    TTS_MODEL = os.environ.get("MYSTERY_TTS_MODEL", "SenseAudio-TTS-1.0")
    TTS_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
    TTS_TIMEOUT = float(os.environ.get("MYSTERY_TTS_TIMEOUT", "60"))


def require_env(name: str, value: str) -> str:
    if value:
        return value
    raise SystemExit(f"缺少必要配置: {name}")


def build_client() -> OpenAI:
    api_key = require_env("MYSTERY_LLM_API_KEY / IME_MODEL_API_KEY", LLM_API_KEY)
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
    """Synthesize TTS and return raw MP3 bytes."""
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


def play_tts(text: str, role: str, tag: str, no_tts: bool) -> str | None:
    """Synthesize TTS, save to file, return path."""
    if no_tts or not text:
        return None
    voice_cfg = VOICE_CONFIG.get(role, VOICE_CONFIG["narrator"])
    try:
        audio_bytes = synthesize_tts(text, voice_cfg, tag)
        if audio_bytes:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = OUTPUT_DIR / f"{tag}.mp3"
            out_path.write_bytes(audio_bytes)
            return str(out_path)
    except Exception as exc:
        print(f"  TTS 合成失败 ({tag}): {exc}", file=sys.stderr)
    return None


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe audio via ASR and return text."""
    api_key = require_env("SENSEAUDIO_API_KEY", ASR_API_KEY)
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"model": ASR_MODEL, "response_format": "verbose_json"}
    with audio_path.open("rb") as handle:
        files = {"file": (audio_path.name, handle)}
        response = requests.post(ASR_URL, headers=headers, data=data, files=files, timeout=ASR_TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    text = payload.get("text", "").strip()
    if not text and payload.get("segments"):
        text = " ".join(seg.get("text", "").strip() for seg in payload["segments"]).strip()
    if not text:
        raise ValueError("ASR 未返回可用文本")
    return text


def validate_case(case: dict[str, Any]) -> bool:
    """Validate case has exactly 1 culprit and evidence links are consistent."""
    suspects = case.get("suspects", [])
    culprits = [s for s in suspects if s.get("is_culprit")]
    if len(culprits) != 1:
        print(f"  验证失败：真凶数量为 {len(culprits)}，应为 1", file=sys.stderr)
        return False

    evidence = case.get("evidence", [])
    if len(evidence) < 3:
        print(f"  验证失败：线索数量为 {len(evidence)}，应至少 3 条", file=sys.stderr)
        return False

    suspect_ids = {s["id"] for s in suspects}
    for e in evidence:
        related = e.get("related_suspect")
        if not related:
            continue
        # Handle both string and list formats
        if isinstance(related, list):
            for r in related:
                if r not in suspect_ids:
                    print(f"  验证失败：线索 {e['id']} 关联了不存在的嫌疑人 {r}", file=sys.stderr)
                    return False
        elif related not in suspect_ids:
            print(f"  验证失败：线索 {e['id']} 关联了不存在的嫌疑人 {related}", file=sys.stderr)
            return False

    locations = case.get("locations", [])
    if len(locations) < 2:
        print(f"  验证失败：地点数量为 {len(locations)}，应至少 2 个", file=sys.stderr)
        return False

    return True


def generate_case(
    difficulty: str,
    theme: str | None = None,
    custom_suspects: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate and validate a mystery case. Retry up to 3 times."""
    difficulty_desc = {"easy": "简单", "medium": "中等", "hard": "困难"}.get(difficulty, "中等")

    # Build theme constraint
    theme_line = ""
    if theme:
        theme_line = f"\n- 案件主题/类型：{theme}（请围绕此主题构建案件背景和犯罪事实）"

    # Build suspect constraint
    suspect_count = len(custom_suspects) if custom_suspects else 3
    if custom_suspects:
        suspect_desc = json.dumps(custom_suspects, ensure_ascii=False)
        suspect_ids = " / ".join(s["id"] for s in custom_suspects)
        suspect_section = f"""- suspects: 数组，包含{suspect_count}个嫌疑人（必须使用以下预设角色信息，补全缺失字段），每个有：
  - id: {suspect_ids}
  - name/occupation/personality: 使用预设值
  - motive: 作案动机（根据角色背景合理设定）
  - alibi: 不在场证明（真凶的应该有破绽）
  - is_culprit: true/false（恰好1个为true）
  - secret: 隐藏信息（审讯深入才会暴露）

预设角色信息：
{suspect_desc}"""
    else:
        suspect_ids = "suspect_a / suspect_b / suspect_c"
        suspect_section = f"""- suspects: 数组，包含{suspect_count}个嫌疑人，每个有：
  - id: {suspect_ids}
  - name: 中文姓名
  - occupation: 职业
  - motive: 作案动机
  - alibi: 不在场证明（真凶的应该有破绽）
  - personality: 性格特点
  - is_culprit: true/false（恰好1个为true）
  - secret: 隐藏信息（审讯深入才会暴露）"""

    user_prompt = f"""输入信息：
- 难度：{difficulty}（{difficulty_desc}：{"线索明显容易推理" if difficulty == "easy" else "需要仔细推理" if difficulty == "medium" else "有误导线索，需要排除干扰"}）{theme_line}

请输出 JSON，字段包括：
- case_name: 案件名称
- background: 案件背景描述（3-5句话）
- crime: 犯罪事实描述（2-3句话）
{suspect_section}
- evidence: 数组，包含4-6条证据线索，每条有：
  - id: E1/E2/E3 等编号
  - description: 线索描述
  - location: 发现位置
  - related_suspect: 关联嫌疑人ID
  - importance: high/medium/low
- locations: 数组，可勘察的地点（3-4个），每个有：
  - name: 地点名称
  - description: 地点描述
  - clues: 该地点可发现的证据ID列表
- solution: 完整的破案推理过程（3-5句话）

要求：
- 恰好1个真凶
- 每条线索至少关联1个嫌疑人
- 真凶的不在场证明必须有可验证的破绽
- 非真凶也应有可疑之处
- 案件逻辑自洽，根据证据可以唯一确定真凶"""

    for attempt in range(3):
        print(f"  生成案件（第 {attempt + 1} 次尝试）...")
        case = llm_json(CASE_SYSTEM_PROMPT, user_prompt)
        if validate_case(case):
            return case
        print("  案件验证未通过，重新生成...")
    raise RuntimeError("3次尝试后仍无法生成有效案件")


def interrogate_suspect(
    case: dict[str, Any],
    suspect: dict[str, Any],
    question: str,
    history: list[dict[str, Any]],
    compressed_summary: str | None,
) -> dict[str, Any]:
    """Run one interrogation round with a suspect."""
    history_text = ""
    if compressed_summary:
        history_text = f"[之前的审讯摘要] {compressed_summary}\n\n"
    for entry in history:
        history_text += f"侦探：{entry['question']}\n{suspect['name']}：{entry['response']}\n\n"

    user_prompt = f"""角色信息：
- 姓名：{suspect['name']}
- 职业：{suspect['occupation']}
- 性格：{suspect['personality']}
- 动机：{suspect['motive']}
- 不在场证明：{suspect['alibi']}
- 是否为真凶：{suspect['is_culprit']}
- 隐藏信息：{suspect['secret']}

审讯历史：
{history_text if history_text else "无"}

侦探的问题：{question}

请输出 JSON，字段包括：
- response: 嫌疑人的回答
- emotion: 当前情绪（calm/nervous/angry/evasive/cooperative）
- revealed_info: 本次回答暴露的新信息（无则为空字符串）

要求：
- 完全以该角色身份回答，符合性格特点
- 如果是真凶，在前几轮保持镇定，但面对关键证据时会出现破绽
- 如果不是真凶，可能会紧张但不会在关键事实上说谎
- 回答自然，像真实审讯对话
- 每次回答 2-4 句话"""
    return llm_json(INTERROGATION_SYSTEM_PROMPT, user_prompt)


def examine_location(case: dict[str, Any], location: dict[str, Any], collected: list[str]) -> dict[str, Any]:
    """Examine a location and discover new clues."""
    evidence_map = {e["id"]: e for e in case.get("evidence", [])}
    new_clues = [evidence_map[cid] for cid in location.get("clues", []) if cid not in collected and cid in evidence_map]

    if not new_clues:
        return {
            "narration": f"你仔细搜索了{location['name']}的每个角落，但没有发现新的线索。",
            "clues_found": [],
        }

    evidence_text = json.dumps(
        [{"id": c["id"], "description": c["description"]} for c in new_clues],
        ensure_ascii=False,
    )
    user_prompt = f"""案件背景：{case['background']}
勘察地点：{location['name']} — {location['description']}
本次发现的证据：{evidence_text}

请输出 JSON，字段包括：
- narration: 旁白描述（描述侦探如何发现这些线索，2-4句话）
- clues_found: 数组，每条包含：
  - id: 证据编号
  - discovery_text: 发现过程的具体描述

要求：
- 描述要有画面感和氛围
- 让玩家感受到探案的紧张感"""
    result = llm_json(EXAMINE_SYSTEM_PROMPT, user_prompt)
    # Ensure clue IDs match
    valid_ids = {c["id"] for c in new_clues}
    result["clues_found"] = [c for c in result.get("clues_found", []) if c.get("id") in valid_ids]
    if not result["clues_found"]:
        result["clues_found"] = [{"id": c["id"], "discovery_text": c["description"]} for c in new_clues]
    return result


def evaluate_accusation(
    case: dict[str, Any],
    accused_id: str,
    reasoning: str,
    collected_evidence: list[str],
    total_interrogations: int,
    total_examinations: int,
) -> dict[str, Any]:
    """Evaluate the player's accusation and score it."""
    culprit = next((s for s in case["suspects"] if s.get("is_culprit")), None)
    accused = next((s for s in case["suspects"] if s["id"] == accused_id), None)
    evidence_map = {e["id"]: e for e in case.get("evidence", [])}
    collected_details = [evidence_map[eid] for eid in collected_evidence if eid in evidence_map]

    user_prompt = f"""案件真相：
- 真凶：{culprit['name']}（{culprit['id']}）
- 完整推理：{case['solution']}
- 全部证据：{json.dumps(case['evidence'], ensure_ascii=False)}

侦探的指控：
- 指控对象：{accused['name']}（{accused_id}）
- 推理过程：{reasoning}
- 引用证据：{json.dumps(collected_details, ensure_ascii=False)}

已收集的证据数：{len(collected_evidence)}/{len(case['evidence'])}
使用的审讯轮数：{total_interrogations}
使用的勘察次数：{total_examinations}
总操作数：{total_interrogations + total_examinations}

请输出 JSON，字段包括：
- correct: {"true" if accused_id == culprit['id'] else "false"}（指控对象{"正确" if accused_id == culprit['id'] else "错误"}）
- scores:
  - logic: 0-30（推理逻辑是否严密）
  - evidence: 0-30（证据引用是否充分）
  - completeness: 0-20（是否涵盖关键线索）
  - efficiency: 0-20（步骤效率）
  - total: 0-100（各项之和）
- feedback: 详细评语（3-5句话）
- truth_reveal: 揭示完整真相的叙述（3-5句话）

要求：
- 即使指控正确，推理不严密也应扣分
- efficiency 按总操作数评估"""
    return llm_json(ACCUSE_SYSTEM_PROMPT, user_prompt)


def compress_history(suspect_name: str, history: list[dict[str, Any]]) -> dict[str, Any]:
    """Compress interrogation history to a summary."""
    history_text = ""
    for entry in history:
        history_text += f"侦探：{entry['question']}\n{suspect_name}：{entry['response']}\n\n"

    user_prompt = f"""审讯对象：{suspect_name}
对话历史：
{history_text}

请输出 JSON，字段包括：
- summary: 压缩后的摘要（3-5句话）
- key_facts: 数组，关键事实点
- contradictions: 数组，发现的矛盾点

要求：
- 保留所有可能影响破案的关键信息
- 特别标注矛盾和可疑之处"""
    return llm_json(COMPRESS_SYSTEM_PROMPT, user_prompt)


def get_player_input(prompt_text: str, no_asr: bool) -> str:
    """Get player input via text or ASR."""
    if no_asr:
        return input(prompt_text).strip()

    print(f"{prompt_text}")
    print("  输入方式：1) 文本输入  2) 音频文件路径")
    choice = input("  选择 [1/2]: ").strip() or "1"
    if choice == "2":
        path = input("  音频文件路径：").strip()
        audio_path = Path(path).expanduser()
        if not audio_path.exists():
            print("  文件不存在，请使用文本输入。", file=sys.stderr)
            return input("  请输入文本：").strip()
        try:
            text = transcribe_audio(audio_path)
            print(f"  ASR 识别：{text}")
            return text
        except Exception as exc:
            print(f"  ASR 失败：{exc}，请使用文本输入。", file=sys.stderr)
            return input("  请输入文本：").strip()
    return input("  请输入：").strip()


def load_game_state() -> dict[str, Any] | None:
    state_path = OUTPUT_DIR / "game_save.json"
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return None


def save_game_state(state: dict[str, Any]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    save_path = OUTPUT_DIR / "game_save.json"
    save_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(save_path)


def print_case_intro(case: dict[str, Any]) -> str:
    """Print case introduction and return narration text."""
    print(f"\n{'=' * 50}")
    print(f"案件：{case['case_name']}")
    print(f"{'=' * 50}")
    print(f"\n{case['background']}")
    print(f"\n{case['crime']}")
    print(f"\n嫌疑人：")
    for s in case["suspects"]:
        print(f"  - {s['name']}（{s['occupation']}）— {s['id']}")
    print(f"\n可勘察地点：")
    for loc in case["locations"]:
        print(f"  - {loc['name']}：{loc['description']}")
    return f"{case['case_name']}。{case['background']}。{case['crime']}。共有三名嫌疑人等待你的审讯。"


def print_status(state: dict[str, Any]) -> None:
    """Print current game status."""
    print(f"\n--- 当前状态 ---")
    print(f"回合：{state['current_turn']}/{state['max_turns']}")
    print(f"已收集证据：{len(state['collected_evidence'])} 条")
    print(f"已勘察地点：{', '.join(state['examined_locations']) or '无'}")
    for sid, log in state["interrogation_logs"].items():
        if log["rounds"] > 0:
            print(f"  {sid} 已审讯 {log['rounds']} 轮")


def load_custom_voices(path: str | None) -> None:
    """Load custom voice config from JSON file, merging into VOICE_CONFIG."""
    if not path:
        return
    p = Path(path).expanduser()
    if not p.exists():
        print(f"警告：音色配置文件不存在: {path}", file=sys.stderr)
        return
    custom = json.loads(p.read_text(encoding="utf-8"))
    for role, cfg in custom.items():
        VOICE_CONFIG[role] = {
            "voice_id": cfg.get("voice_id", VOICE_CONFIG.get(role, {}).get("voice_id", "male_0004_a")),
            "speed": cfg.get("speed", 1.0),
            "pitch": cfg.get("pitch", 0),
        }
    print(f"已加载自定义音色配置：{list(custom.keys())}")


def load_custom_suspects(path: str | None) -> list[dict[str, Any]] | None:
    """Load custom suspect definitions from JSON file.

    Expected format: array of objects with fields:
      name, occupation, personality
    Optional fields (LLM will fill if missing):
      motive, alibi, secret, is_culprit
    """
    if not path:
        return None
    p = Path(path).expanduser()
    if not p.exists():
        print(f"警告：角色配置文件不存在: {path}", file=sys.stderr)
        return None
    suspects = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(suspects, list) or len(suspects) < 2:
        print("警告：角色配置至少需要 2 个嫌疑人", file=sys.stderr)
        return None
    # Assign IDs if missing
    id_labels = [f"suspect_{chr(ord('a') + i)}" for i in range(len(suspects))]
    for i, s in enumerate(suspects):
        s.setdefault("id", id_labels[i])
    print(f"已加载自定义角色：{[s.get('name', s['id']) for s in suspects]}")
    return suspects


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="中文语音侦探推理游戏")
    parser.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"], help="难度")
    parser.add_argument("--max-turns", type=int, default=30, help="最大回合数")
    parser.add_argument("--load", action="store_true", help="加载存档继续游戏")
    parser.add_argument("--no-tts", action="store_true", help="不调用 TTS")
    parser.add_argument("--no-asr", action="store_true", help="不调用 ASR，使用文本输入")
    parser.add_argument("--theme", default=None,
                        help="案件主题/背景，如「密室杀人」「博物馆盗窃」「校园悬疑」")
    parser.add_argument("--suspects", default=None,
                        help="自定义嫌疑人 JSON 文件路径，格式见 references/state_schema_cn.md")
    parser.add_argument("--voices", default=None,
                        help="自定义音色 JSON 文件路径，键为角色ID，值含 voice_id/speed/pitch")
    return parser.parse_args()


def main() -> None:
    load_env()
    refresh_runtime_settings()
    args = parse_args()

    game_state: dict[str, Any] | None = None
    case: dict[str, Any] | None = None

    if args.load:
        game_state = load_game_state()
        if game_state is None:
            print("未找到存档，将开始新游戏。")
        else:
            case = game_state["case"]
            print("存档加载成功！")

    # Load custom voices and suspects
    load_custom_voices(args.voices)
    custom_suspects = load_custom_suspects(args.suspects)

    if case is None:
        theme_msg = f"「{args.theme}」主题 " if args.theme else ""
        print(f"\n正在生成{theme_msg}{args.difficulty}难度案件...")
        case = generate_case(args.difficulty, theme=args.theme, custom_suspects=custom_suspects)

        # Build interrogation_logs dynamically from actual suspect IDs
        suspect_ids = [s["id"] for s in case["suspects"]]
        interrogation_logs = {sid: {"rounds": 0, "history": [], "compressed_summary": None} for sid in suspect_ids}

        game_state = {
            "case": case,
            "difficulty": args.difficulty,
            "max_turns": args.max_turns,
            "current_turn": 0,
            "collected_evidence": [],
            "examined_locations": [],
            "interrogation_logs": interrogation_logs,
            "actions_log": [],
        }

    # Print intro
    intro_text = print_case_intro(case)
    play_tts(intro_text, "narrator", "intro", args.no_tts)

    # Main game loop
    suspect_map = {s["id"]: s for s in case["suspects"]}
    location_map = {loc["name"]: loc for loc in case["locations"]}
    total_interrogations = sum(log["rounds"] for log in game_state["interrogation_logs"].values())
    total_examinations = len(game_state["examined_locations"])

    while game_state["current_turn"] < game_state["max_turns"]:
        print_status(game_state)
        print(f"\n可选动作：")
        print(f"  1) interrogate — 审讯嫌疑人")
        print(f"  2) examine     — 勘察现场")
        print(f"  3) review      — 回顾证据")
        print(f"  4) accuse      — 提出指控")
        print(f"  5) save        — 保存进度")
        print(f"  6) quit        — 退出游戏")

        action = input("\n选择动作 [1-6]: ").strip()
        action_map = {"1": "interrogate", "2": "examine", "3": "review", "4": "accuse", "5": "save", "6": "quit"}
        action = action_map.get(action, action)

        if action == "quit":
            print("退出游戏。")
            break

        if action == "save":
            path = save_game_state(game_state)
            print(f"游戏已保存：{path}")
            continue

        if action == "review":
            evidence_map = {e["id"]: e for e in case.get("evidence", [])}
            if not game_state["collected_evidence"]:
                print("\n你还没有收集到任何证据。")
            else:
                print(f"\n--- 已收集证据 ({len(game_state['collected_evidence'])} 条) ---")
                for eid in game_state["collected_evidence"]:
                    e = evidence_map.get(eid, {})
                    print(f"  [{eid}] {e.get('description', '未知')}（关联：{e.get('related_suspect', '未知')}，重要性：{e.get('importance', '未知')}）")
            continue

        game_state["current_turn"] += 1

        if action == "examine":
            print("\n可勘察地点：")
            for i, loc in enumerate(case["locations"]):
                visited = "已勘察" if loc["name"] in game_state["examined_locations"] else "未勘察"
                print(f"  {i + 1}) {loc['name']} [{visited}]")
            choice = input("选择地点编号：").strip()
            try:
                loc_idx = int(choice) - 1
                location = case["locations"][loc_idx]
            except (ValueError, IndexError):
                print("无效选择。")
                continue

            print(f"\n正在勘察 {location['name']}...")
            result = examine_location(case, location, game_state["collected_evidence"])
            print(f"\n{result['narration']}")

            new_ids = []
            for clue in result.get("clues_found", []):
                cid = clue["id"]
                if cid not in game_state["collected_evidence"]:
                    game_state["collected_evidence"].append(cid)
                    new_ids.append(cid)
                    print(f"  发现证据 [{cid}]：{clue.get('discovery_text', '')}")

            if not new_ids:
                print("  没有发现新线索。")

            if location["name"] not in game_state["examined_locations"]:
                game_state["examined_locations"].append(location["name"])
            total_examinations += 1

            play_tts(result["narration"], "narrator", f"examine_{game_state['current_turn']}", args.no_tts)
            game_state["actions_log"].append({
                "turn": game_state["current_turn"],
                "action": "examine",
                "target": location["name"],
                "new_evidence": new_ids,
            })

        elif action == "interrogate":
            print("\n选择审讯对象：")
            for i, s in enumerate(case["suspects"]):
                log = game_state["interrogation_logs"][s["id"]]
                remaining = MAX_INTERROGATION_ROUNDS - log["rounds"]
                status = f"剩余 {remaining} 轮" if remaining > 0 else "已用完"
                print(f"  {i + 1}) {s['name']}（{s['occupation']}）[{status}]")
            choice = input("选择编号：").strip()
            try:
                s_idx = int(choice) - 1
                suspect = case["suspects"][s_idx]
            except (ValueError, IndexError):
                print("无效选择。")
                continue

            sid = suspect["id"]
            log = game_state["interrogation_logs"][sid]

            if log["rounds"] >= MAX_INTERROGATION_ROUNDS:
                print(f"\n{suspect['name']}的审讯轮数已用完。")
                continue

            print(f"\n--- 审讯 {suspect['name']} ---")
            print("（输入 'done' 结束审讯）")

            while log["rounds"] < MAX_INTERROGATION_ROUNDS:
                remaining = MAX_INTERROGATION_ROUNDS - log["rounds"]
                question = get_player_input(f"\n[剩余{remaining}轮] 你的问题：", args.no_asr)
                if not question or question.lower() == "done":
                    print("结束审讯。")
                    break

                # Compress history if needed
                if len(log["history"]) >= COMPRESS_AFTER_ROUNDS and log["compressed_summary"] is None:
                    print("  正在压缩审讯历史...")
                    compress_result = compress_history(suspect["name"], log["history"])
                    log["compressed_summary"] = compress_result.get("summary", "")
                    old_history = log["history"]
                    log["history"] = old_history[-1:]  # Keep last entry

                result = interrogate_suspect(
                    case, suspect, question, log["history"], log["compressed_summary"]
                )
                response_text = result.get("response", "...")
                emotion = result.get("emotion", "calm")
                revealed = result.get("revealed_info", "")

                print(f"\n{suspect['name']} [{emotion}]：{response_text}")
                if revealed:
                    print(f"  （你注意到：{revealed}）")

                log["history"].append({
                    "round": log["rounds"] + 1,
                    "question": question,
                    "response": response_text,
                    "emotion": emotion,
                    "revealed_info": revealed,
                })
                log["rounds"] += 1
                total_interrogations += 1

                play_tts(response_text, sid, f"interrogate_{sid}_{log['rounds']}", args.no_tts)

            game_state["actions_log"].append({
                "turn": game_state["current_turn"],
                "action": "interrogate",
                "target": sid,
            })

        elif action == "accuse":
            print("\n--- 提出指控 ---")
            print("选择你认为的真凶：")
            for i, s in enumerate(case["suspects"]):
                print(f"  {i + 1}) {s['name']}（{s['occupation']}）— {s['id']}")
            choice = input("选择编号：").strip()
            try:
                a_idx = int(choice) - 1
                accused = case["suspects"][a_idx]
            except (ValueError, IndexError):
                print("无效选择。")
                continue

            reasoning = get_player_input("请陈述你的推理过程：", args.no_asr)
            if not reasoning:
                print("推理过程不能为空。")
                continue

            print(f"\n正在评估你的指控...")
            result = evaluate_accusation(
                case,
                accused["id"],
                reasoning,
                game_state["collected_evidence"],
                total_interrogations,
                total_examinations,
            )

            correct = result.get("correct", False)
            scores = result.get("scores", {})
            feedback = result.get("feedback", "")
            truth = result.get("truth_reveal", "")

            print(f"\n{'=' * 50}")
            if correct:
                print("恭喜！你的指控正确！")
            else:
                culprit = next(s for s in case["suspects"] if s.get("is_culprit"))
                print(f"很遗憾，你指控了错误的人。真凶是 {culprit['name']}。")

            print(f"\n评分：")
            print(f"  逻辑推理：{scores.get('logic', 0)}/30")
            print(f"  证据引用：{scores.get('evidence', 0)}/30")
            print(f"  完整性：  {scores.get('completeness', 0)}/20")
            print(f"  效率：    {scores.get('efficiency', 0)}/20")
            print(f"  总分：    {scores.get('total', 0)}/100")
            print(f"\n评语：{feedback}")
            print(f"\n真相：{truth}")

            play_tts(truth, "narrator", "truth_reveal", args.no_tts)

            # Save final report
            report = {
                "case": case,
                "game_state": game_state,
                "accusation": {
                    "accused": accused["id"],
                    "accused_name": accused["name"],
                    "reasoning": reasoning,
                },
                "result": result,
            }
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            report_path = OUTPUT_DIR / "case_report.json"
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\n案件报告已保存：{report_path}")

            game_state["actions_log"].append({
                "turn": game_state["current_turn"],
                "action": "accuse",
                "target": accused["id"],
                "correct": correct,
                "score": scores.get("total", 0),
            })
            break
        else:
            print("无效动作，请重新选择。")
            game_state["current_turn"] -= 1

    else:
        print(f"\n已达到最大回合数 {game_state['max_turns']}，游戏结束！")
        print("你未能在限定回合内破案。")

    print("\n游戏结束！")


if __name__ == "__main__":
    main()
