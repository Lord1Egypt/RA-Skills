#!/usr/bin/env python3
"""
对话标准化脚本（ASR 友好版）

用途：统一 Excel/JSON/CSV 输入格式，做基础角色分离、ASR 清洗与结构增强，输出标准 JSON。
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from common import WORKSPACE_DIR

DISCOVERY_DIR = os.path.join(WORKSPACE_DIR, "discovery")
os.makedirs(DISCOVERY_DIR, exist_ok=True)

ROLE_PATTERNS = {
    "agent": [r"^(机器人|客服|坐席|销售|顾问|京东金融|AI)[:：]"],
    "user": [r"^(用户|客户)[:：]"],
}


COMMON_ASR_REPLACEMENTS = {
    "今条": "金条",
    "京东今条": "京东金条",
    "免西券": "免息券",
    "白条今条": "白条金条",
    "备用今": "备用金",
}


FILLER_WORDS = {"嗯", "啊", "哦", "呃", "诶", "额", "嗯嗯", "啊啊"}


def detect_content_field(headers: List[str]) -> str:
    for header in headers:
        if not header:
            continue
        h = str(header).strip().lower()
        if any(k in h for k in ["conversation", "dialog", "content", "transcription", "对话", "话术", "内容"]):
            return header
    return ""


def detect_session_field(headers: List[str]) -> str:
    for header in headers:
        if not header:
            continue
        h = str(header).strip().lower()
        if any(k in h for k in ["session", "sessionid", "会话", "通话id", "dialog_id"]):
            return header
    return ""


def split_segments(text: str) -> List[str]:
    if not text:
        return []
    parts = re.split(r"[\n；;]+", text)
    return [p.strip() for p in parts if p and p.strip()]


def detect_role(segment: str) -> str:
    s = segment.strip()
    for role, patterns in ROLE_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, s, flags=re.IGNORECASE):
                return role
    return "unknown"


def clean_role_prefix(segment: str) -> str:
    return re.sub(r"^(机器人|客服|坐席|销售|顾问|京东金融|AI|用户|客户)[:：]\s*", "", segment.strip(), flags=re.IGNORECASE)


def normalize_asr_text(text: str) -> str:
    """ASR 文本清洗，但保留换行符（换行是 turn 分割依据）"""
    if not text:
        return ""
    text = text.replace("\u3000", " ")
    # 不把换行合并为空格，保留 \n 作为 turn 分隔符
    text = re.sub(r"[^\S\n]+", " ", text).strip()
    text = re.sub(r"([，。！？,.!?；;]){2,}", r"\1", text)
    text = re.sub(r"([嗯啊哦呃诶额])\1{2,}", r"\1", text)
    for src, dst in COMMON_ASR_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text.strip()


def count_filler_tokens(text: str) -> int:
    if not text:
        return 0
    return sum(1 for token in re.split(r"[\s，。！？,.!?；;]+", text) if token in FILLER_WORDS)


def estimate_noise_score(text: str) -> float:
    if not text:
        return 1.0
    filler_count = count_filler_tokens(text)
    weird_symbol_count = len(re.findall(r"[^\w\s\u4e00-\u9fff，。！？,.!?；;:：()（）-]", text))
    repeated_fragments = len(re.findall(r"(.{1,4})\1{2,}", text))
    total_len = max(len(text), 1)
    score = (filler_count * 0.5 + weird_symbol_count * 1.0 + repeated_fragments * 1.5) / max(total_len / 20, 1)
    return round(min(score, 1.0), 3)


def parse_turns(text: str) -> Tuple[List[Dict[str, str]], str, str, bool]:
    turns: List[Dict[str, str]] = []
    agent_parts: List[str] = []
    user_parts: List[str] = []

    segments = split_segments(text)
    has_role_markers = False

    # 第一遍：尝试用显式角色标记
    for part in segments:
        role = detect_role(part)
        if role != "unknown":
            has_role_markers = True
        clean_text = normalize_asr_text(clean_role_prefix(part))
        turns.append({"role": role, "text": clean_text})
        if role == "agent":
            agent_parts.append(clean_text)
        elif role == "user":
            user_parts.append(clean_text)

    # 如果有显式角色标记，直接使用
    if has_role_markers:
        return turns, " ".join(agent_parts), " ".join(user_parts), has_role_markers

    # 第二遍（fallback）：ASR 无角色标记时，用交替启发式
    # 外呼场景假设：客服先说话，交替轮次
    # 客服特征：句子更长、包含产品/利益/引导词
    # 用户特征：句子更短、包含语气词/拒绝词/模糊应答
    agent_keywords = {"金条", "免息", "额度", "借款", "京东", "备用金", "福利", "优惠券",
                      "点击", "查看", "激活", "申请", "您好", "打扰", "回访", "工号"}
    user_keywords = {"嗯", "啊", "哦", "不用", "不了", "不需要", "别打了", "挂了",
                     "不方便", "忙", "在忙", "开车", "不用了", "行", "好", "可以"}

    turns = []
    agent_parts = []
    user_parts = []

    for idx, part in enumerate(segments):
        clean_text = normalize_asr_text(clean_role_prefix(part))
        if not clean_text:
            continue

        # 启发式打分：文本更像客服还是用户
        agent_score = sum(1 for kw in agent_keywords if kw in clean_text) * 2
        user_score = sum(1 for kw in user_keywords if kw in clean_text) * 2

        # 短句更可能是用户（<=4字倾向用户）
        if len(clean_text) <= 4:
            user_score += 1
        # 长句更可能是客服（>=20字倾向客服）
        if len(clean_text) >= 20:
            agent_score += 1

        # 如果打分不分伯仲，用交替规则：偶数轮=客服，奇数轮=用户（0-indexed）
        if agent_score == user_score:
            role = "agent" if idx % 2 == 0 else "user"
        elif agent_score > user_score:
            role = "agent"
        else:
            role = "user"

        turns.append({"role": role, "text": clean_text})
        if role == "agent":
            agent_parts.append(clean_text)
        else:
            user_parts.append(clean_text)

    return turns, " ".join(agent_parts), " ".join(user_parts), False


def infer_dialog_end_type(turns: List[Dict[str, str]]) -> str:
    if not turns:
        return "unknown"
    last_turn = turns[-1]
    last_text = last_turn.get("text", "")
    if any(k in last_text for k in ["挂了", "别打了", "不说了", "先这样"]):
        return "user_stop" if last_turn.get("role") == "user" else "possible_hangup"
    if any(k in last_text for k in ["祝您", "先这样", "您先忙"]):
        return "natural_end"
    if last_turn.get("role") == "agent":
        return "possible_hangup"
    return "unknown"


def build_meta(turns: List[Dict[str, str]], agent_text: str, user_text: str, raw_text: str, has_role_markers: bool = True) -> Dict[str, Any]:
    agent_turns = [t for t in turns if t.get("role") == "agent"]
    user_turns = [t for t in turns if t.get("role") == "user"]
    avg_agent_len = round(sum(len(t.get("text", "")) for t in agent_turns) / max(len(agent_turns), 1), 2)
    avg_user_len = round(sum(len(t.get("text", "")) for t in user_turns) / max(len(user_turns), 1), 2)
    noise_score = estimate_noise_score(raw_text)

    return {
        "turn_count": len(turns),
        "agent_turn_count": len(agent_turns),
        "user_turn_count": len(user_turns),
        "avg_agent_len": avg_agent_len,
        "avg_user_len": avg_user_len,
        "last_speaker": turns[-1].get("role") if turns else "unknown",
        "dialog_end_type": infer_dialog_end_type(turns),
        "has_role_markers": has_role_markers,
        "asr_noise_score": noise_score,
        "short_utterance_ratio": round(sum(1 for t in turns if len(t.get("text", "")) <= 2) / max(len(turns), 1), 3),
        "duplicate_span_ratio": round(len(re.findall(r"(.{1,4})\1{2,}", raw_text)) / max(len(raw_text) / 10, 1), 3),
        "speaker_switch_confidence": round(1.0 if has_role_markers else 0.6, 2),
    }


def load_xlsx(input_path: str) -> List[Dict[str, Any]]:
    import openpyxl

    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    headers = [ws.cell(1, col).value for col in range(1, ws.max_column + 1)]
    content_field = detect_content_field(headers)
    session_field = detect_session_field(headers)

    if not content_field:
        raise ValueError("未找到对话内容列")

    content_col = headers.index(content_field) + 1
    session_col = headers.index(session_field) + 1 if session_field else None

    dialogs = []
    for row in range(2, ws.max_row + 1):
        content = ws.cell(row, content_col).value
        if not content:
            continue
        session_id = ws.cell(row, session_col).value if session_col else None
        dialogs.append({
            "id": str(session_id or f"dialog_{row}"),
            "content": str(content),
            "row": row,
            "source_type": "xlsx",
        })
    return dialogs


def load_csv(input_path: str) -> List[Dict[str, Any]]:
    dialogs = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        content_field = detect_content_field(headers)
        session_field = detect_session_field(headers)
        if not content_field:
            raise ValueError("未找到对话内容列")
        for i, row in enumerate(reader, start=2):
            content = row.get(content_field)
            if not content:
                continue
            dialogs.append({
                "id": str(row.get(session_field) or f"dialog_{i}"),
                "content": str(content),
                "row": i,
                "source_type": "csv",
            })
    return dialogs


def load_json(input_path: str) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    dialogs = []
    items = data if isinstance(data, list) else data.get("dialogs", [])
    for i, item in enumerate(items, start=1):
        content = item.get("content") or item.get("dialog_content") or item.get("conversation_text")
        if not content:
            continue
        dialogs.append({
            "id": str(item.get("id") or item.get("session_id") or f"dialog_{i}"),
            "content": str(content),
            "row": i,
            "source_type": "json",
        })
    return dialogs


def load_dialogs(input_path: str) -> List[Dict[str, Any]]:
    if input_path.endswith(".xlsx"):
        return load_xlsx(input_path)
    if input_path.endswith(".csv"):
        return load_csv(input_path)
    if input_path.endswith(".json"):
        return load_json(input_path)
    raise ValueError(f"不支持的文件格式: {input_path}")


def normalize_dialogs(dialogs: List[Dict[str, Any]], scene: str, input_path: str) -> List[Dict[str, Any]]:
    normalized = []
    for d in dialogs:
        raw_text = d["content"]
        clean_text = normalize_asr_text(raw_text)
        turns, agent_text, user_text, has_role_markers = parse_turns(clean_text)
        meta = build_meta(turns, agent_text, user_text, raw_text, has_role_markers)
        normalized.append({
            "dialog_id": d["id"],
            "scene": scene,
            "source_file": os.path.basename(input_path),
            "source_type": d.get("source_type"),
            "source_row": d.get("row"),
            "raw_text": raw_text,
            "clean_text": clean_text,
            "normalized_text": clean_text,
            "turns": turns,
            "agent_text": agent_text,
            "user_text": user_text,
            "meta": meta,
        })
    return normalized


def save_results(normalized: List[Dict[str, Any]], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(normalized),
            "dialogs": normalized,
            "created_at": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="标准化对话数据（ASR 友好版）")
    parser.add_argument("--input", required=True, help="输入文件 xlsx/csv/json")
    parser.add_argument("--scene", required=True, help="场景")
    parser.add_argument("--output", required=True, help="输出标准化 json 文件")
    args = parser.parse_args()

    dialogs = load_dialogs(args.input)
    normalized = normalize_dialogs(dialogs, args.scene, args.input)
    save_results(normalized, args.output)
    print(f"✅ 标准化完成: {len(normalized)} 条 -> {args.output}")
