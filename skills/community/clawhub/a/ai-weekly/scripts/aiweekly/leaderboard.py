"""排行榜编排层：多源池调度 / 区域优先级 / 快照与缓存兜底 / 周变化 / 选型结论。

单榜源解析器见 `leaderboard_sources.py`，成本与资料卡富化见 `model_meta.py`
（P1#1 Phase 3 拆分，本文件只负责「怎么组合、怎么兜底」）。

设计原则：
① 每源独立容错，单源失败不影响其他榜；
② 抓取失败不脑补、不空白，回退本地缓存快照并标注数据截止日；
③ 基于本地缓存计算「周变化 ↑↓」；
④ 排行榜描述字段以 model_profiles.json（资料卡）为唯一权威源。
"""
import json
import logging
import time
import concurrent.futures
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

from aiweekly.utils import (
    _http_get, _probe, _detect_region, _retry_fetch, _resolved_proxy,
    _parse_date_arg, _parse_snapshot_date,
)
from aiweekly.news import LEADERBOARD_STALE_DAYS
from aiweekly.model_meta import (
    COST_PATH, DEFAULT_PROFILES, PENDING_PROFILES,
    _load_cost_table, _COST_TABLE, _match_cost, _enrich_cost, _apply_profile_as_truth,
)
from aiweekly.leaderboard_sources import (
    _norm_model,
)
from aiweekly.leaderboard_fetch import (
    LB_CRITERIA, SOURCES, _collect_source_results, _record_health,
    inject_open_source_ranks,
)
# P2-1：模型名归一原语已下沉到 aiweekly.canon（叶子模块）；榜源 schema 校验在
# aiweekly.leaderboard_checks（顶部导入即可，循环依赖已消除）。
from aiweekly.canon import canon_key, canon_display, ALIASES_PATH
from aiweekly.leaderboard_checks import validate_leaderboard_data, LB_ROW_FIELDS

# P2-4：快照 / 缓存子系统已抽到 aiweekly.leaderboard_snapshot（降体量、收敛 IO 边界）；
# 本文件经顶部 re-export，对外 API（含 CACHE_PATH 等路径常量）不变。
from aiweekly.leaderboard_snapshot import (  # noqa: F401
    CACHE_PATH, CN_SNAPSHOT_PATH, SNAPSHOTS_DIR,
    _load_snapshots, _save_snapshot, _seed_bootstrap, _build_history,
    _normalize_snapshot_orgs, _load_cn_snapshot,
    _load_cache, _save_cache, _fill_from_cache,
)

SKILL_DIR = Path(__file__).resolve().parents[2]

__all__ = [
    "CACHE_PATH", "CN_SNAPSHOT_PATH", "SNAPSHOTS_DIR", "ALIASES_PATH",
    "_load_cn_snapshot", "_leaderboard_freshness",
    "LB_CRITERIA", "SOURCES", "_load_cache", "_save_cache",
    "_apply_deltas", "fetch_all_leaderboards", "_fill_from_cache", "_collect_leaderboard_models",
    "sync_model_profiles", "canon_key", "canon_display",
    "_load_snapshots", "_save_snapshot", "_build_history",
    "validate_leaderboard_data", "LB_ROW_FIELDS",
]


# L0#1 / R5：模型名归一（canon_key / canon_display / 别名反向索引 / 后缀令牌）已下沉到
# aiweekly.canon（P2-1：叶子模块，灭 leaderboard↔model_meta↔leaderboard_checks 循环依赖）。
# 本文件只保留编排逻辑：区域优先级 / 快照兜底 / 周变化 / 选型结论。


def _dedupe_by_alias(rows: list) -> list:
    """同一榜内按归一键去重（L0#4）：合并 "(max)" / "(pro)" 等变体双胞胎。

    当两个变体归一为同一键时，保留信息更完整的那行（价格/上下文/分数更全），
    其余丢弃；返回保序后的去重列表。
    """
    if not rows:
        return rows
    seen, out = {}, []
    for r in rows:
        k = canon_key(r.get("model", ""))
        if not k:
            out.append(r)
            continue
        prev = seen.get(k)
        if prev is None:
            seen[k] = r
            out.append(r)
        else:
            # 选信息更完整者：非 None 字段数更多者胜出
            def _info(x):
                return sum(1 for v in x.values() if v not in (None, "", "—"))
            if _info(r) > _info(prev):
                seen[k] = r
                out[out.index(prev)] = r
    return out


# ---------- L0#2: 时序快照（snapshots/{date}.json）----------
# 以下快照 / 缓存子系统已抽到 aiweekly.leaderboard_snapshot（P2-4），本文件经顶部 re-export。


# _parse_snapshot_date 已迁移到 aiweekly.utils（顶部已 re-export）。


def _leaderboard_freshness(leaderboard: dict, report_date) -> dict:
    """计算排行榜各源快照距报告日的时效，判断是否需要「非本周抓取」告警。

    返回 dict：{max_age, stale, per_source, per_source_age, worst_source, worst_age}
    - max_age: 所有源中最大天数（无快照则为 -1）
    - stale: 是否存在超龄（> LEADERBOARD_STALE_DAYS）源
    - per_source: {key: ISO 8601 快照串 or None}（P1#21：语义明确、可对比、可排序）
    - per_source_age: {key: 距报告日天数 or None}（兼容模板渲染，向前端提供现成天数差）
    """
    # report_date 可能是 str（CLI --date）或 datetime 或 None，统一解析为 datetime
    if isinstance(report_date, str):
        report_date = _parse_date_arg(report_date)
    elif report_date is None:
        report_date = datetime.now()
    per_source, per_source_age = {}, {}
    worst_key, worst_age = None, -1
    groups = [
        ("comprehensive.lmarena", leaderboard.get("comprehensive", {}).get("lmarena", {})),
        ("comprehensive.aa", leaderboard.get("comprehensive", {}).get("aa", {})),
        ("open_source.ls", leaderboard.get("open_source", {}).get("ls", {})),
        ("open_source.hf", leaderboard.get("open_source", {}).get("hf", {})),
    ]
    for key, sub in groups:
        snap = (sub or {}).get("snapshot", "")
        d = _parse_snapshot_date(snap)
        if d is None:
            per_source[key] = None
            per_source_age[key] = None
            continue
        age = (report_date.date() - d).days
        per_source[key] = str(snap).strip()  # P1#21：保留原始 ISO 8601 快照串
        per_source_age[key] = age
        if age > worst_age:
            worst_key, worst_age = key, age
    max_age = max((a for a in per_source_age.values() if a is not None), default=-1)
    stale = any((a is not None and a > LEADERBOARD_STALE_DAYS) for a in per_source_age.values())
    return {
        "max_age": max_age,
        "stale": stale,
        "per_source": per_source,
        "per_source_age": per_source_age,
        "worst_source": worst_key,
        "worst_age": worst_age if worst_age >= 0 else None,
    }



# ---------- 国内可直连榜源解析器（尽力而为）----------
# 说明：OpenCompass / SuperCLUE / ModelScope 官网均为 JS 渲染 SPA，其数据 API
# 无法用简单 HTTP 稳定抓取（返回 SPA 兜底 HTML 或需鉴权）。下列解析器按「尽力而为」
# 实现——若抓到的是 SPA 兜底页（无 <table>）或解析失败，一律返回 None，
# 由多源池优雅降级到国内快照（cn_leaderboard_snapshot.json）或本地缓存。
# 一旦某源开放稳定 JSON API，只需在对应解析器里补全字段提取即可自动生效。





# LB_CRITERIA / SOURCES 已迁移到 aiweekly.leaderboard_fetch（L2 模块拆分，见该文件）。
# 本文件仅保留编排逻辑：区域优先级 / 快照兜底 / 周变化 / 选型结论。


def _apply_deltas(rows, cache_rows, score_key=None):
    """rows 含 rank/model；cache_rows 为上期 {model: value}（按展示名）。

    返回每行的 delta 字典（L0#2）：
      {"wow": +2, "wow_score": -0.5, "new_entry": false}
    - wow: 名次变化（正数=名次前进，基于 rank）；
    - wow_score: 分数变化（基于 score）；
    - new_entry: 上期无该模型记录（跨榜按归一键匹配，兼容变体漂移）。
    score_key 为 None 时按行自动判定（优先 score，否则 rank）。
    无上期数据时所有行标记 new_entry=True（首跑基线周，模板据此抑制 🆕 噪声）。
    """
    if not cache_rows:
        for r in rows:
            r["delta"] = {"wow": None, "wow_score": None, "new_entry": True}
        return rows
    if score_key is None:
        score_key = "score" if any(r.get("score") is not None for r in rows) else "rank"
    cache_map = {canon_key(k): v for k, v in cache_rows.items()}
    for r in rows:
        ck = canon_key(r["model"])
        prev = cache_map.get(ck)
        cur = r.get(score_key)
        if prev is None:
            r["delta"] = {"wow": None, "wow_score": None, "new_entry": True}
            continue
        if cur is None:
            r["delta"] = {"wow": None, "wow_score": None, "new_entry": False}
            continue
        if score_key == "rank":
            r["delta"] = {"wow": prev - cur, "wow_score": None, "new_entry": False}
        else:
            r["delta"] = {"wow": None, "wow_score": round(cur - prev, 1), "new_entry": False}
    return rows


# L2#14 / L2#15（_collect_source_results / _record_health）已迁移到 aiweekly.leaderboard_fetch。
# 本文件经顶部 `from aiweekly.leaderboard_fetch import ...` 复用，不再本地定义。


def _build_selection_notes(top_name, cheap, new_entries, risers):
    """L0#3 / L2#13：根据综合榜首、低成本可直连模型、新上榜、跃升模型，
    生成「总览一句 + 三受众（开发者/PM/自媒体）选型结论」。纯函数，便于单测。

    cheap: 低成本可直连模型行(dict，含 model/price_out) 或 None
    new_entries / risers: 模型名列表（可为空）
    """
    if top_name:
        selection_note = (f"本周综合最强为 {top_name}；开源/自部署可关注 Qwen、Llama、DeepSeek 等家族"
                          f"（详见开源榜）。")
    else:
        selection_note = "本期源数据缺失，排名与结论仅供参考。"
    selection_notes = {
        "开发者": (f"选型先看成本与可直连：{cheap['model']}（{cheap['price_out']}$/1M·out，国内可直连）"
                   f"适合低成本接入；闭源头部 {top_name or '模型'} 能力强但需评估 API 合规与计费。"
                   if cheap else
                   f"闭源头部 {top_name or '模型'} 能力强；自部署优先 Qwen / DeepSeek 家族（开源榜可查许可证与单价）。"),
        "PM": (f"本周综合最强 {top_name or '头部闭源模型'}"
               f"{('；' + '、'.join(risers) + ' 名次大幅上升') if risers else ''}"
               f"——产品路线图可据此评估供应商集中度与替换风险。"),
        "自媒体": (f"本周看点：{top_name or '头部模型'} 居综合榜首"
                   f"{('；新上榜 ' + '、'.join(new_entries[:3])) if new_entries else ''}"
                   f"{('；' + '、'.join(risers) + ' 名次跃升') if risers else ''}。"),
    }
    return selection_note, selection_notes


def fetch_all_leaderboards(top_n: int = 15, region: str = "auto"):
    """抓取双排行榜，返回结构化数据；网络环境自适应。

    设计：
      - 多源池 SOURCES 每个榜源带 region 标签（cn/global）。
      - 按 detected region 排序优先级：国内环境优先国内源、国外环境优先国外源，
        依次 _retry_fetch 命中即用（每榜综合榜取 2 个源、开源榜取 1 个源）。
      - 国内环境且实时源全失败 -> 回退到国内快照 cn_leaderboard_snapshot.json（标注 is_cache）。
      - 国外环境或未知环境且实时源失败 -> 回退本地缓存 leaderboard_cache.json（标注 is_cache）。
      - 每个 slot 额外携带 source_region / is_cache，供前端来源区域徽章展示。
    """
    if region in ("auto", "cn", "global", "unknown"):
        detected = _detect_region() if region == "auto" else region
    else:
        detected = "global"
    proxy = _resolved_proxy()
    logger.info("网络环境判定: %s%s", detected, f"（代理：{proxy}）" if proxy else "")

    snapshot = datetime.now().astimezone().strftime("%Y-%m-%d")
    cache = _load_cache()
    cn_snap = _load_cn_snapshot()

    # L2#14：并行预抓取全部榜源（含健康元数据），后续按 region 优先级从结果挑选
    results = _collect_source_results(top_n, detected, proxy)
    # L2#15：追加健康监控记录
    _record_health(results, detected)

    def try_board(board: str, need: int):
        """按 region 优先级从已抓取结果中挑选该 board 的源池，返回 [(source_spec, rows), ...]。"""
        pool = [s for s in SOURCES.values() if s["board"] == board]
        pool.sort(key=lambda s: 0 if s["region"] == detected else 1)
        hit = []
        for s in pool:
            outcome = results.get(s["key"], {})
            if outcome.get("rows"):
                hit.append((s, outcome["rows"]))
                if len(hit) >= need:
                    break
        return hit

    def live_slot(s, rows):
        return {
            "source": s["label"], "url": s["url"], "snapshot": snapshot,
            "criteria": s["criteria"], "rows": rows[:top_n],
            "source_region": "cn" if s["region"] == "cn" else "global",
            "is_cache": False,
        }

    def snap_slot(src, snap_date):
        return {
            "source": src.get("source", ""), "url": src.get("url", ""),
            "snapshot": snap_date, "criteria": src.get("criteria", ""),
            "rows": src.get("rows", [])[:top_n],
            "source_region": "cn", "is_cache": True,
        }

    comp_hits = try_board("comprehensive", 2)

    # —— 综合榜（两列：lmarena / aa）——
    comp = {"lmarena": {"rows": []}, "aa": {"rows": []}}
    if comp_hits:
        # 按源 key 路由到正确槽位（避免 slot 名与承载数据相反）：
        # comp["lmarena"] 承载 LMArena 源，comp["aa"] 承载 Artificial Analysis 源。
        for s, rows in comp_hits:
            slot = "aa" if s.get("key") == "aa" else ("lmarena" if s.get("key") == "lm" else None)
            if slot:
                comp[slot] = live_slot(s, rows)
    # R2 修正（来源诚实化）：oc/sv 为 JS 渲染 SPA，国内简单 HTTP 抓取几乎必返回空
    # （leaderboard_health.jsonl 实测 0% 实时率），原「oc/sv 补综合榜双列」回退永不触发——
    # 删去死代码，不假装「cn 区域真出实时榜」。cn 综合榜实际依赖 aa(96%)/lm(35~67%)，
    # 二者皆失败才回退 cn_snap 静态快照（已标注 is_cache=True）。oc/sv/ms 仍留池作 best-effort。
    # 综合榜不足 / 全失败：回退到国内权威快照 cn_leaderboard_snapshot.json（标注 is_cache）。
    # 不区分区域——global 环境下国际源（aa/lm）不可达时，本地 cache 的 aa 常为空，
    # 必须借助快照才能补齐，否则校验会因某榜 0 行而不通过。
    if not comp["lmarena"]["rows"] or not comp["aa"]["rows"]:
        if cn_snap.get("comprehensive"):
            if not comp["lmarena"]["rows"] and "lmarena" in cn_snap["comprehensive"]:
                comp["lmarena"] = snap_slot(cn_snap["comprehensive"]["lmarena"], cn_snap.get("snapshot_date", ""))
            if not comp["aa"]["rows"] and "aa" in cn_snap["comprehensive"]:
                comp["aa"] = snap_slot(cn_snap["comprehensive"]["aa"], cn_snap.get("snapshot_date", ""))
        # 仍缺失的列再退本地 cache（原 global 环境设计路径）
        if not comp["lmarena"]["rows"] and (cache.get("lmarena") or cache.get("aa")):
            _fill_from_cache(comp, cache, snapshot)
        if not comp["aa"]["rows"] and (cache.get("aa") or cache.get("lmarena")):
            _fill_from_cache(comp, cache, snapshot)

    # —— 开源榜（双列：LLM-Stats + Hugging Face）——
    os_board = {"ls": {"rows": []}, "hf": {"rows": []}}
    # R1 修正（来源透明）：左列数据源随真实命中动态变化，杜绝「标 LLM-Stats、实为 DataLearner」误导。
    # 优先级 LLM-Stats(ls) → DataLearner(dl) → ModelScope(ms) 兜底；命中哪个就用哪个的
    # label/criteria/url 渲染，页面来源标注与数据严格一致（ls 源国内实测 0% 实时率，
    # 故多数情况下左列即显示 DataLearner · 开源模型榜，这是真实来源而非降级伪装）。
    ms_rows = (results.get("ms", {}) or {}).get("rows")  # 国内实时源回退（ModelScope 开源热度）
    _ls_spec, ls_rows = None, None
    for _key, _rows, _spec in (
        ("ls", results.get("ls", {}).get("rows"), SOURCES["ls"]),
        ("dl", results.get("dl", {}).get("rows"), SOURCES["dl"]),
    ):
        if _rows:
            _ls_spec, ls_rows = _spec, _rows
            break
    else:
        if ms_rows:
            _ls_spec, ls_rows = SOURCES["ms"], ms_rows
    if _ls_spec and ls_rows:
        os_board["ls"] = live_slot(_ls_spec, ls_rows)
    elif detected == "cn" and cn_snap.get("open_source"):
        for key in cn_snap["open_source"]:
            os_board["ls"] = snap_slot(cn_snap["open_source"][key], cn_snap.get("snapshot_date", ""))
            break
    # Hugging Face（独立源，与左列并排展示）；HF 不可达时回退 ModelScope 实时热度（诚实标注来源）
    hf_spec = SOURCES["hf"]
    hf_rows = results.get("hf", {}).get("rows")
    if not hf_rows and ms_rows:
        hf_spec, hf_rows = SOURCES["ms"], ms_rows
    if hf_rows:
        os_board["hf"] = live_slot(hf_spec, hf_rows)
    elif detected == "cn" and cn_snap.get("open_source"):
        for key in cn_snap["open_source"]:
            os_board["hf"] = snap_slot(cn_snap["open_source"][key], cn_snap.get("snapshot_date", ""))
            break
    # 兜底：本地缓存快照（标注 is_cache）
    _fill_from_cache(os_board, cache, snapshot)

    lm = _dedupe_by_alias(comp["lmarena"].get("rows") or [])
    aa = _dedupe_by_alias(comp["aa"].get("rows") or [])
    ls = _dedupe_by_alias(os_board["ls"].get("rows") or [])
    hf = _dedupe_by_alias(os_board["hf"].get("rows") or [])
    # 写回去重后的行到槽位（否则 data 里仍是原始未合并列表，校验会报重复）
    comp["lmarena"]["rows"] = lm
    comp["aa"]["rows"] = aa
    os_board["ls"]["rows"] = ls
    os_board["hf"]["rows"] = hf
    # L3#21：开源榜实时抓取行可能缺 rank，按当前顺序补 1..n（避免前端 undefined）
    inject_open_source_ranks(os_board)

    # L0#2: 写当前时序快照 + 构建历史序列（供 WoW 徽章 / sparkline）
    _seed_bootstrap(cache)
    _cur_snap = {
        "lmarena": {r["model"]: (r.get("rank") if r.get("rank") is not None else r.get("score"))
                    for r in lm if r.get("model")},
        "aa": {r["model"]: (r.get("score") if r.get("score") is not None else r.get("rank"))
               for r in aa if r.get("model")},
        "ls": {r["model"]: (r.get("rank") if r.get("rank") is not None else r.get("score"))
               for r in ls if r.get("model")},
        "hf": {r["model"]: (r.get("rank") if r.get("rank") is not None else r.get("score"))
               for r in hf if r.get("model")},
        "snapshot": snapshot,
    }
    _save_snapshot(snapshot, _cur_snap)
    _snaps = _load_snapshots()
    _hist = _build_history(_snaps)

    def _attach_delta_and_spark(rows, board, prev_map):
        _apply_deltas(rows, prev_map or {})
        for r in rows:
            ser = (_hist.get(board, {}) or {}).get(canon_key(r["model"]), []) or []
            r["spark"] = [x for x in ser if x is not None][-4:]
        return rows

    if lm:
        _attach_delta_and_spark(lm, "lmarena", cache.get("lmarena", {}))
    if aa:
        _attach_delta_and_spark(aa, "aa", cache.get("aa", {}))
    if ls:
        _attach_delta_and_spark(ls, "ls", cache.get("ls", {}) or cache.get("hf", {}))
    if hf:
        _attach_delta_and_spark(hf, "hf", cache.get("hf", {}) or cache.get("ls", {}))

    # —— LMArena 智能指数补全 ——
    # LMArena 公开页/API 仅暴露名次，无原始 Elo 分；用同模型在含真实
    # Intelligence Index 的列（Artificial Analysis）回填「智能指数」列。
    # 注意：comp["lmarena"] 实际承载 AA 数据（含分数），comp["aa"] 实际承载
    # LMArena 数据（仅名次）。两列模型名一致，故按模型名匹配回填。
    # 这里动态判定「含分列」为源、「缺分列」为目标，不依赖列名约定。
    _scored = next((rows for rows in (lm, aa)
                    if any(r.get("score") is not None for r in rows)), None)
    _unscored = next((rows for rows in (lm, aa) if rows is not _scored), None)
    if _scored and _unscored:
        _idx_map = {}
        for r in _scored:
            if r.get("score") is not None and r.get("model"):
                _idx_map[canon_key(r["model"])] = r["score"]
                _idx_map[r["model"].lower()] = r["score"]
        for r in _unscored:
            if r.get("score") is None and r.get("model"):
                v = _idx_map.get(canon_key(r["model"])) or _idx_map.get(r["model"].lower())
                if v is not None:
                    r["score"] = v

    # —— P1：选型支撑数据（性价比象限 / 跨源差异 / 本周结论）——
    def _ability(r):
        """能力近似分(0-100)：优先 score；否则以名次近似，仅供横向参考。"""
        if r.get("score") is not None:
            return float(r["score"])
        if r.get("rank") is not None:
            return round(max(0.0, 100 - (r["rank"] - 1) * 1.2), 1)
        return None

    import re as _re
    _paren = _re.compile(r'\s*\([^)]*\)$')
    def _vnorm(label):
        # 去掉末尾括号变体（如 “(max)” “(with fallback)”），避免同一模型的多个变体在象限里重复堆叠
        return _paren.sub('', label or '').strip().lower()

    value_chart, _seen = [], {}
    for src_rows in (lm, aa):
        for r in src_rows:
            price = r.get("price_out")
            ctx = r.get("context")
            ab = _ability(r)
            if price is None or ab is None:
                continue
            p = {
                "label": r.get("model", "?"), "price": price, "ability": ab,
                "context": (ctx // 1000) if isinstance(ctx, int) else None,
                "cn_access": r.get("cn_access"),
            }
            # L0#1: 按归一键去重，避免同一模型变体在象限重复堆叠
            k = canon_key(p["label"]) or _vnorm(p["label"])
            if k not in _seen or (_seen[k]["ability"] or 0) < (p["ability"] or 0):
                _seen[k] = p
    value_chart = list(_seen.values())

    # L1#10: 跨源差异（同模型在 LMArena 与 AA 的排名差）+ 维度差异上下文锚点
    cross_diff = []
    if lm and aa:
        aa_map = {canon_key(r["model"]): r["rank"] for r in aa if r.get("rank")}
        for r in lm:
            ar = aa_map.get(canon_key(r["model"]))
            if ar and r.get("rank"):
                cross_diff.append({
                    "model": r["model"], "lm_rank": r["rank"], "aa_rank": ar,
                    "diff": r["rank"] - ar,
                    # L1#10: 给差异一个解释锚点——两榜评测维度不同，名次差多源于侧重差异
                    "explanation": ("LMArena 偏「人类偏好 Elo」（真实使用体感），"
                                    "AA 偏「多项能力基准综合（智能指数）」——两榜维度不同，"
                                    "名次差多来自评测侧重差异，而非绝对强弱。"),
                })
        cross_diff.sort(key=lambda x: abs(x["diff"]), reverse=True)

    # L0#3: selection_note 受众化（开发者 / PM / 自媒体 三段，各 ≤ 1 句）
    top = (aa or lm or [{}])[0] if (aa or lm) else {}
    top_name = top.get("model") if top else None
    cheap = next((r for r in aa if r.get("cn_access")
                  and "国内可直连" in r["cn_access"] and r.get("price_out") is not None
                  and r["price_out"] <= 2), None)
    # 新上榜（new_entry）模型名，供自媒体/PM 视角点题
    new_entries = [r["model"] for r in (lm + aa) if isinstance(r.get("delta"), dict) and r["delta"].get("new_entry")]
    # 大幅上升（wow >= 5）模型名
    risers = [r["model"] for r in (lm + aa)
              if isinstance(r.get("delta"), dict) and isinstance(r["delta"].get("wow"), int)
              and r["delta"]["wow"] >= 5]
    selection_note, selection_notes = _build_selection_notes(top_name, cheap, new_entries, risers)

    data = {
        "meta": {"region": detected, "proxy": proxy or "",
                 "note": ("已按国内网络环境优先采用国内可直连榜源" if detected == "cn"
                          else "已按国外网络环境优先采用国际榜源")},
        "comprehensive": {
            "lmarena": comp["lmarena"],
            "aa": comp["aa"],
        },
        "open_source": {
            "ls": os_board["ls"],
            "hf": os_board["hf"],
        },
        "selection_note": selection_note,
        "selection_notes": selection_notes,
        "value_chart": value_chart,
        "cross_diff": cross_diff,
    }

    # 写回缓存供下次对比（按 slot 名 lmarena/aa/ls/hf 存模型->值）
    _save_cache({
        "lmarena": {r["model"]: r["rank"] if r.get("rank") is not None else r.get("score") for r in lm},
        "aa": {r["model"]: r["score"] if r.get("score") is not None else r.get("rank") for r in aa},
        "ls": {r["model"]: r["rank"] if r.get("rank") is not None else r.get("score") for r in ls},
        "hf": {r["model"]: r["rank"] if r.get("rank") is not None else r.get("score") for r in hf},
        "snapshot": snapshot,
    })
    return data


def _collect_leaderboard_models(leaderboard_data):
    """收集排行榜中出现的所有模型名（去重保序，按归一键去重）。

    L0#1: 用 canon_display 归一展示名，使 "(max)/(pro)" 变体与资料卡 canonical
    键（小写）稳定命中，避免把同一模型误判为「缺档案新模型」。
    """
    models = []
    if not leaderboard_data:
        return models
    for board in ("lmarena", "aa"):
        for r in leaderboard_data.get("comprehensive", {}).get(board, {}).get("rows", []):
            m = r.get("model")
            if m:
                models.append(m)
    for r in leaderboard_data.get("open_source", {}).get("hf", {}).get("rows", []):
        m = r.get("model")
        if m:
            models.append(m)
    seen, uniq = set(), []
    for m in models:
        ck = canon_key(m)
        if ck and ck not in seen:
            seen.add(ck)
            uniq.append(canon_display(m))
    return uniq


def sync_model_profiles(extra_profiles_path: str, leaderboard_data: dict):
    """模型档案同步（real-time archive update）：

    1. 自动加载技能目录下的 canonical 档案 model_profiles.json（无需手动 --profiles-json）；
    2. 若传入 --profiles-json，将其合并进 canonical 并写回，使档案随每次研究累积更新；
    3. 检测排行榜中出现、但档案缺失的模型，写入 model_profiles.pending.json 供后续联网核实；
    4. 返回合并后的档案 dict（注入 LEADERBOARD_DATA.model_profiles）。
    """
    base = {}
    if DEFAULT_PROFILES.exists():
        try:
            base = json.loads(DEFAULT_PROFILES.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("读取 canonical 模型档案失败: %s", e)

    # 合并本次传入的新档案并写回 canonical（实时更新）
    if extra_profiles_path:
        try:
            extra = json.loads(Path(extra_profiles_path).read_text(encoding="utf-8"))
            if isinstance(extra, dict) and extra:
                base.update(extra)
                DEFAULT_PROFILES.write_text(
                    json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
                logger.info("已合并 %d 条新模型档案 -> %s（canonical 已更新）",
                            len(extra), DEFAULT_PROFILES.name)
        except Exception as e:
            logger.warning("读取/合并 --profiles-json 失败: %s", e)

    # 检测新上榜却缺档案的模型
    if leaderboard_data:
        models = _collect_leaderboard_models(leaderboard_data)
        lower_keys = {k.lower() for k in base}
        missing = [m for m in models if m.lower() not in lower_keys]
        if missing:
            PENDING_PROFILES.write_text(
                json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.warning("发现 %d 个新模型未建档，已写入 %s: %s",
                           len(missing), PENDING_PROFILES.name, missing)
        else:
            if PENDING_PROFILES.exists():
                PENDING_PROFILES.unlink()
            logger.info("模型档案齐全：%d 条覆盖全部 %d 个上榜模型", len(base), len(models))
    else:
        logger.info("未提供排行榜数据，跳过新模型建档检测")

    return base

