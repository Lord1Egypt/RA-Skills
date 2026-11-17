"""模型元数据富化：成本参考表 + 资料卡（model_profiles.json）权威覆盖。

从 leaderboard.py 抽出（P1#1 Phase 3），无榜源依赖，可独立单测。

核心规则（项目数据治理约定）：
**排行榜以资料卡为准** —— `model_profiles.json` 是排行榜描述字段（成本/上下文/许可证/
商用/模态/币种）的唯一权威源；`models_cost.json` 仅作「榜上有、卡上无」的兜底。
排名与分数来自基准榜，不被资料卡覆盖。
"""
import json
import re
from pathlib import Path

from aiweekly.canon import canon_key as _ck  # P2-1：叶子模块，无循环依赖

SKILL_DIR = Path(__file__).resolve().parents[2]

COST_PATH = SKILL_DIR / "models_cost.json"
# 模型资料卡 canonical 档案（按模型名索引，联网核实的机构/许可证/成本等）；
# 每次生成自动加载，新模型研究后合并写回，实现档案实时累积更新。
DEFAULT_PROFILES = SKILL_DIR / "model_profiles.json"
# 新上榜但档案缺失的模型清单（供后续联网核实），检测为空时自动删除。
PENDING_PROFILES = SKILL_DIR / "model_profiles.pending.json"

__all__ = [
    "COST_PATH", "DEFAULT_PROFILES", "PENDING_PROFILES", "_load_cost_table",
    "_COST_TABLE", "_match_cost", "_enrich_cost", "_apply_profile_as_truth",
]


# 选型决策所需的「成本/上下文/可用性」参考表（公开资料整理，维护者周更；非实时）
# P0/P1 使用：每行模型按家族匹配后注入 price/context/commercial/cn_access 等字段；
# 未匹配到的家族一律返回 None（页面显示 —，绝不编造）。
def _load_cost_table() -> list:
    try:
        if COST_PATH.exists():
            return json.loads(COST_PATH.read_text(encoding="utf-8")).get("models", [])
    except Exception:
        pass
    return []


_COST_TABLE = _load_cost_table()


def _match_cost(model: str):
    """按模型名匹配家族，返回成本参考条目或 None。"""
    if not model:
        return None
    t = model.lower()
    for entry in _COST_TABLE:
        for k in entry.get("keys", []):
            if k.lower() in t:
                return entry
    return None


def _enrich_cost(row: dict) -> dict:
    """给排行行注入选型字段（成本/上下文/可用性）。无匹配则留 None。"""
    c = _match_cost(row.get("model", ""))
    if not c:
        row.setdefault("price_in", None)
        row.setdefault("price_out", None)
        row.setdefault("context", None)
        row.setdefault("multimodal", None)
        row.setdefault("cn_access", None)
        row.setdefault("best_for", None)
        row.setdefault("commercial", None)
        row.setdefault("currency", "USD")
        return row
    row["price_in"] = c.get("price_in")
    row["price_out"] = c.get("price_out")
    row["context"] = c.get("context")
    row["multimodal"] = c.get("multimodal")
    row["cn_access"] = c.get("cn_access")
    row["best_for"] = c.get("best_for")
    row["commercial"] = c.get("commercial")
    row["currency"] = c.get("currency", "USD")
    return row


def _apply_profile_as_truth(leaderboard: dict, profiles: dict):
    """以资料卡(model_profiles.json)为准：用卡片的权威值覆盖排行榜行里的描述性字段
    （成本/上下文/许可证/商用/模态/币种）。排名字段(rank/score/model/org)来自基准榜，
    不覆盖。卡片缺字段时保留榜单原值（成本表/实时抓取兜底）。

    这是用户确立的硬性规则：排行榜上展示的模型「资料」必须与资料卡一致，
    资料卡是唯一权威源；成本表(models_cost.json)仅作无卡片时的兜底。
    """
    # 归一键匹配：profile 键（如 "DeepSeek-V4-Pro"）与排行榜模型名（如 "deepseek v4 pro"）
    # 格式不一，必须归一（去大小写/空白/符号）才能匹配上，否则行内描述字段无法回填 → 资料缺失
    def _canon(name):
        return re.sub(r'[^a-z0-9]', '', (name or '').strip().lower())
    _MAP = [("cost_in", "price_in"), ("cost_out", "price_out"),
            ("context", "context"), ("license", "license"),
            ("commercial", "commercial"), ("multimodal", "multimodal"),
            ("currency", "currency")]
    # 双索引：轻量 canon（最宽容，去所有非字母数字）+ 可选别名 canon_key，提高命中率
    profiles_canon = {}
    for k, v in (profiles or {}).items():
        # P0-2 守护：未核实条目（verified=false，来自 model_profiles_unverified.json
        # 或历史遗留）不参与排行榜排名，绝不把无来源锚点的推测数据回填到榜单行。
        if v.get("verified") is False:
            continue
        profiles_canon[_canon(k)] = v
        if _ck:
            profiles_canon.setdefault(_ck(k), v)
    boards = []
    for b in (list((leaderboard.get("comprehensive") or {}).values())
              + list((leaderboard.get("open_source") or {}).values())):
        if isinstance(b, dict) and "rows" in b:
            boards.append(b)
    for b in boards:
        for r in b.get("rows", []):
            model = r.get("model") or ""
            p = profiles_canon.get(_canon(model)) or (_ck and profiles_canon.get(_ck(model)))
            if not p:
                continue
            for cf, rf in _MAP:
                v = p.get(cf)
                if v in (None, "", "—"):
                    continue
                r[rf] = v

