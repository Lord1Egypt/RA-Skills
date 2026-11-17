"""模型名归一化原语（P2-1：从 leaderboard.py / leaderboard_sources.py 下沉为无依赖叶子模块）。

灭除 leaderboard↔model_meta、leaderboard↔leaderboard_checks 两处循环依赖：
原 canon_key 定义在 leaderboard.py，model_meta / leaderboard_checks 为避开循环依赖
只能「函数内延迟导入」；下沉到本叶子模块（仅依赖标准库 + 技能目录下的 model_aliases.json）
后，所有消费者改为「顶部导入」，循环依赖自然消除，延迟导入亦可删除。

设计约束：本模块**不 import 任何 aiweekly 子模块**，确保它自身不会成为循环依赖的一环。
"""
import json
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
ALIASES_PATH = SKILL_DIR / "model_aliases.json"


# ---------- 跨源模型名归一（与 leaderboard_sources 同源，避免后缀剥离撞键）----------
# 已知开发方前缀（用于从 LMArena 拼接 slug 中切分机构名；也供 _norm_model 剥离机构前缀）
ORG_PREFIXES = [
    "Anthropic", "OpenAI", "Google", "Meta", "Mistral AI", "DeepSeek", "Alibaba",
    "Qwen", "Moonshot", "xAI", "Zhipu", "Zai", "MiniMax", "NVIDIA", "IBM",
    "Microsoft", "Cohere", "01.AI", "Ai2", "AllenAI", "Databricks",
    "NousResearch", "Tencent", "Baidu", "StepFun", "Arcee", "Grok",
]

# leaderboard_sources 用的后缀剥离正则（无词边界，纯剥离）
_SUFFIX_RE = re.compile(r"(max|xhigh|high|thinking|withfallback|preview|pro|flash|sol|ultra)")


def _norm_model(name: str) -> str:
    """跨源模型名归一：小写、去分隔符、去前缀机构、去常见后缀词。

    注意：后缀词只去掉词本身，不吞掉前面的数字
    （否则 "1.1" 会被拆成 "11" 再误删版本位）。
    机构名内嵌的 max（如 MiniMax）已由 ORG_PREFIXES 前缀剥离先行处理，不受影响。
    """
    if not name:
        return ""
    s = name.lower()
    for ch in " ()[]-_./":
        s = s.replace(ch, "")
    for p in ORG_PREFIXES:
        pk = p.lower().replace(" ", "")
        if s.startswith(pk):
            s = s[len(pk):]
            break
    return _SUFFIX_RE.sub("", s)


# ---------- 别名表（L0#1）：canonical -> [variants] ----------
def _load_aliases() -> dict:
    """加载 model_aliases.json；文件缺失或损坏时返回空表（降级为 _norm_model 兜底）。"""
    try:
        if ALIASES_PATH.exists():
            return json.loads(ALIASES_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


_ALIASES = _load_aliases()
# 反向索引：variant(小写) / variant 归一形 -> canonical(小写键)
_ALIAS_REV: dict = {}
# canonical(小写) -> canonical 展示名（即 _ALIASES 的键本身）
_CANON_DISPLAY: dict = {}
for _c, _vs in _ALIASES.items():
    _CANON_DISPLAY[_c.lower()] = _c
    for _v in (list(_vs) if isinstance(_vs, list) else []):
        if not isinstance(_v, str):
            continue
        _ALIAS_REV.setdefault(_v.lower(), _c.lower())
        _ALIAS_REV.setdefault(_norm_model(_v), _c.lower())


# R5：后缀感知归一并发——避免 "Base" 与 "Base-Suffix" 被 _norm_model 剥后缀后撞键
# （如 GLM-5.3 与 GLM-5.3-Flash、未来 Qwen3 与 Qwen3-Max）。
_SUFFIX_TOKENS = {
    "flash": "flash", "preview": "preview", "max": "max", "pro": "pro",
    "ultra": "ultra", "mini": "mini", "lite": "lite", "turbo": "turbo",
    "air": "air", "sol": "sol", "high": "high", "xhigh": "xhigh",
    "thinking": "thinking", "withfallback": "withfallback",
}
_SUFFIX_TOKEN_RE = re.compile(
    r"[-_\s.]+(" + "|".join(_SUFFIX_TOKENS) + r")(?:[-_\s.]|$|\()"
)


def _suffix_token(name: str) -> str | None:
    if not name:
        return None
    m = _SUFFIX_TOKEN_RE.search(name.lower())
    return _SUFFIX_TOKENS[m.group(1)] if m else None


def canon_key(name: str) -> str:
    """返回模型名的跨榜归一键（小写）。先查别名表精确/归一匹配，否则回退 _norm_model。

    归一键用于跨源匹配（LMArena↔AA 回填、跨源差异、性价比象限、WoW 历史），
    保证同一模型的不同变体 / 大小写 / 日期戳写法被识别为同一实体。
    R5：归一并发时携带后缀标记（``glm53~flash``），避免 Base/Base-Suffix 撞键。
    """
    if not name:
        return ""
    low = name.strip().lower()
    if low in _ALIAS_REV:
        return _ALIAS_REV[low]
    norm = _norm_model(name)
    if norm in _ALIAS_REV:
        return _ALIAS_REV[norm]
    tok = _suffix_token(name)
    return f"{norm}~{tok}" if tok else norm


def canon_display(name: str) -> str:
    """返回模型名的规范展示名（优先别名表中的 canonical 写法，否则原样）。"""
    if not name:
        return name
    low = name.strip().lower()
    if low in _ALIAS_REV:
        return _CANON_DISPLAY.get(_ALIAS_REV[low], name)
    norm = _norm_model(name)
    if norm in _ALIAS_REV:
        return _CANON_DISPLAY.get(_ALIAS_REV[norm], name)
    return name


__all__ = [
    "ALIASES_PATH", "ORG_PREFIXES", "_norm_model", "canon_key", "canon_display",
    "_load_aliases", "_ALIASES", "_ALIAS_REV", "_CANON_DISPLAY",
    "_SUFFIX_RE", "_SUFFIX_TOKENS", "_SUFFIX_TOKEN_RE", "_suffix_token",
]
