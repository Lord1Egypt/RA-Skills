"""
ClawSoul 本地 AI 人格分析（无 LLM）
当无 LLM 时，用本地 MBTI 数据库对「AI 默认特征」做匹配，得到最接近的 MBTI。
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# 默认认为 AI 常见特征（用于与 base.json 的 traits/communication 匹配）
AI_DEFAULT_FEATURES = [
    "逻辑", "系统", "简洁", "直接", "效率", "分析", "理性",
    "有条理", "结论", "框架", "精确",
]

MBTI_DATABASE_DIR = Path(__file__).resolve().parent.parent / "prompts" / "mbti_database"
VALID_MBTI = {
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
}


def _load_base() -> Dict:
    """加载 base.json"""
    path = MBTI_DATABASE_DIR / "base.json"
    if not path.is_file():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def local_analyze_ai_personality() -> Optional[str]:
    """
    本地分析 AI 人格：用 AI 默认特征与 base.json 中每种 MBTI 的 traits + communication 做匹配，
    返回得分最高的 MBTI；失败则返回 None。
    """
    base = _load_base()
    if not base:
        return None
    best_mbti = None
    best_score = 0
    for mbti, data in base.items():
        if mbti not in VALID_MBTI:
            continue
        traits = data.get("traits") or []
        comm = data.get("communication") or []
        keywords = set(traits) | set(comm)
        score = sum(1 for f in AI_DEFAULT_FEATURES if any(f in k or k in f for k in keywords))
        if score > best_score:
            best_score = score
            best_mbti = mbti
    return best_mbti if best_mbti else None
