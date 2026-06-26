"""
ClawSoul 交互学习引擎 - V3 升级
用户消息 → 本地关键词匹配（加载 mbti_database/keywords.json）→ 提取偏好 → 更新 Soul
无需 LLM。
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

from .memory_manager import get_memory_manager

# 本地 MBTI 数据库目录
MBTI_DB_DIR = Path(__file__).resolve().parent.parent / "prompts" / "mbti_database"
KEYWORDS_FILE = MBTI_DB_DIR / "keywords.json"

# 内置兜底关键词（与 keywords.json 对齐；文件缺失时使用）
BUILTIN_KEYWORDS: Dict[str, List[str]] = {
    "喜欢简洁": ["短", "简单", "说重点", "直接", "简洁", "简短", "精简", "别啰嗦", "少废话"],
    "技术控": ["代码", "API", "技术", "开发", "编程", "实现", "debug", "函数", "架构"],
    "喜欢例子": ["比如", "例如", "举个例", "举个例子", "举例", "例子", "像这样"],
    "慢性子": ["不急", "慢慢", "等一下", "稍等"],
    "要详细": ["详细", "展开", "具体", "深入", "完整", "全面", "多说点"],
    "重逻辑": ["逻辑", "推理", "因果", "前提", "论证", "所以"],
    "重数据": ["数据", "数字", "统计", "证据", "依据", "量化"],
    "随意": ["随便", "都行", "可以", "没事", "嗯", "哈哈"],
    "礼貌": ["谢谢", "请", "麻烦", "感谢", "辛苦了"],
    "专业": ["专业", "正式", "报告", "文档", "规范"],
}


def _load_keywords() -> Dict[str, List[str]]:
    """加载用户偏好关键词：优先 keywords.json，失败则用内置"""
    if KEYWORDS_FILE.is_file():
        try:
            with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return {k: v if isinstance(v, list) else [v] for k, v in data.items()}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(BUILTIN_KEYWORDS)


def analyze_user_message(user_message: str) -> Dict[str, Any]:
    """
    本地关键词匹配分析用户消息（无需 LLM）。
    Returns:
        dict: length, word_count, tone_hints, preference_keys（偏好名列表，如 ["喜欢简洁", "技术控"]）
    """
    if not user_message or not isinstance(user_message, str):
        return {"length": "medium", "word_count": 0, "tone_hints": [], "preference_keys": []}
    text = user_message.strip()
    word_count = len(re.findall(r"[\u4e00-\u9fff\w]+", text)) or len(text)
    length = "short" if word_count <= 5 else ("long" if word_count > 30 else "medium")
    tone_hints = []
    if any(k in text for k in ("谢谢", "请", "麻烦")):
        tone_hints.append("polite")
    if any(k in text for k in ("随便", "没事", "哈哈", "嗯")):
        tone_hints.append("casual")
    if any(k in text for k in ("专业", "正式", "报告")):
        tone_hints.append("formal")
    keywords_map = _load_keywords()
    preference_keys = []
    for pref_name, kws in keywords_map.items():
        if any(kw in text for kw in kws) and pref_name not in preference_keys:
            preference_keys.append(pref_name)
    return {
        "length": length,
        "word_count": word_count,
        "tone_hints": tone_hints,
        "preference_keys": preference_keys,
    }


def detect_preferences(user_message: str) -> List[str]:
    """
    从用户消息中检测偏好（人类可读的「学到的内容」）。
    Returns:
        list: 如 ["用户偏好：喜欢简洁", "用户偏好：技术控"]
    """
    if not user_message or not isinstance(user_message, str):
        return []
    analysis = analyze_user_message(user_message)
    return [f"用户偏好：{p}" for p in analysis.get("preference_keys", [])]


def update_soul(analysis: Dict[str, Any], preferences: List[str]) -> None:
    """
    根据本次分析更新 Soul：
    - preference_keys → interaction_patterns 计数
    - preferences → learnings 去重追加
    - 有匹配则 adaptation_level +1
    """
    mm = get_memory_manager()
    for key in analysis.get("preference_keys") or []:
        mm.update_interaction_pattern(key, 1)
    for pref in preferences:
        mm.add_learning(pref)
    if analysis.get("preference_keys") or preferences:
        mm.add_adaptation(1)


def process_user_message(user_message: str) -> Dict[str, Any]:
    """
    一站式：关键词匹配 → 提取偏好 → 更新 Soul。
    上层在每轮人类消息后调用一次即可。
    """
    analysis = analyze_user_message(user_message)
    preferences = detect_preferences(user_message)
    update_soul(analysis, preferences)
    return {
        "analysis": analysis,
        "preferences": preferences,
        "adaptation_level": get_memory_manager().get_adaptation_level(),
    }


_learner = None


def get_interaction_learner() -> "InteractionLearner":
    """获取交互学习引擎单例"""
    global _learner
    if _learner is None:
        _learner = InteractionLearner()
    return _learner


class InteractionLearner:
    """交互学习引擎封装（V3：基于本地关键词库）"""

    def __init__(self) -> None:
        self._mm = get_memory_manager()

    def analyze_user_message(self, user_message: str) -> Dict[str, Any]:
        return analyze_user_message(user_message)

    def detect_preferences(self, user_message: str) -> List[str]:
        return detect_preferences(user_message)

    def update_soul(self, analysis: Dict[str, Any], preferences: List[str]) -> None:
        update_soul(analysis, preferences)

    def process_user_message(self, user_message: str) -> Dict[str, Any]:
        return process_user_message(user_message)
