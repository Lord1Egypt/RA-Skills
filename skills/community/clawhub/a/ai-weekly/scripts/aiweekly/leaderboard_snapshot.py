"""排行榜快照与缓存子系统（P2-4：从 leaderboard.py 抽出，降低其体量、收敛 IO 边界）。

本模块只负责「排行榜时序快照 / 本地缓存 / 国内权威榜兜底快照」的读写与清洗：
- ``CACHE_PATH`` / ``CN_SNAPSHOT_PATH`` / ``SNAPSHOTS_DIR``：三类持久化路径（相对技能根）。
- ``_load_snapshots`` / ``_save_snapshot`` / ``_seed_bootstrap`` / ``_build_history``：
  时序快照（L0#2）的读取 / 写入 / 首跑基线播种 / 历史名次序列构建（供 sparkline）。
- ``_normalize_snapshot_orgs``：历史快照行的机构名防御清洗。
- ``_load_cn_snapshot``：国内可直连榜兜底快照（实时抓取不可达时）。
- ``_load_cache`` / ``_save_cache`` / ``_fill_from_cache``：本地缓存快照读写与回退填充。

这些函数原散落在 leaderboard.py 的编排逻辑中；抽出后 leaderboard.py 只保留「怎么组合、
怎么兜底」的编排，并经由顶部 re-export 保持对外 API 不变（含 CACHE_PATH 等路径常量）。
依赖均为叶子模块，无循环依赖：aiweekly.canon（归一）/ aiweekly.leaderboard_sources（机构拆分）
/ aiweekly.utils（日期解析）。
"""
import json
import logging
from datetime import datetime
from pathlib import Path

from aiweekly.canon import canon_key
from aiweekly.cli_utils import load_json_soft
from aiweekly.leaderboard_sources import _split_dl_org
from aiweekly.utils import _parse_snapshot_date

logger = logging.getLogger(__name__)

SKILL_DIR = Path(__file__).resolve().parents[2]

# ---------- 持久化路径（相对技能根）----------
CACHE_PATH = SKILL_DIR / "leaderboard_cache.json"
# 国内可直连权威榜快照（OpenCompass 司南；实时抓取不可达时的兜底；非实时，标注截止日）
CN_SNAPSHOT_PATH = SKILL_DIR / "cn_leaderboard_snapshot.json"
# 时序快照目录（L0#2）：每次生成写一份 snapshots/{date}.json，供 WoW 趋势线 / 跨周 diff
SNAPSHOTS_DIR = SKILL_DIR / "snapshots"


# ---------- L0#2: 时序快照（snapshots/{date}.json）----------
def _load_snapshots() -> dict:
    """读取 snapshots/ 下全部 {date}.json，返回 {date: snapshot_dict}（date 升序拼装）。"""
    out = {}
    try:
        if SNAPSHOTS_DIR.exists():
            for p in sorted(SNAPSHOTS_DIR.glob("*.json")):
                try:
                    d = json.loads(p.read_text(encoding="utf-8"))
                    out[p.stem] = d
                except Exception:
                    continue
    except Exception:
        pass
    return out


def _save_snapshot(date: str, boards: dict):
    """写入 snapshots/{date}.json（本次完整排行，供后续 WoW / 趋势使用）。"""
    try:
        SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        SNAPSHOTS_DIR.joinpath(f"{date}.json").write_text(
            json.dumps(boards, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _seed_bootstrap(cache: dict):
    """首次引入时序快照时，用现有 leaderboard_cache.json 作为「上一周」基线播种，
    使 WoW 趋势线 / 跨周 diff 在首跑即有历史可对比（不伪造数据，仅复用既有缓存）。
    """
    if SNAPSHOTS_DIR.exists() and any(SNAPSHOTS_DIR.glob("*.json")):
        return
    prev = (cache or {}).get("snapshot")
    if not prev:
        return
    try:
        from datetime import date as _d, timedelta as _td
        _pd = _parse_snapshot_date(prev) or _d.today()
        seed_date = (_pd - _td(days=7)).isoformat()
        SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        boards = {k: cache[k] for k in ("lmarena", "aa", "ls", "hf") if k in cache}
        boards["snapshot"] = prev
        SNAPSHOTS_DIR.joinpath(f"{seed_date}.json").write_text(
            json.dumps(boards, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _build_history(snapshots: dict) -> dict:
    """从时序快照构建每个榜的「归一键 -> 历史名次序列」用于 sparkline。

    返回 {board: {canon: [rank, ...]}}（按日期升序，最近在前由模板控制）。
    仅取 rank 数值序列；缺失 rank 的快照位置留 None。
    """
    hist: dict = {"lmarena": {}, "aa": {}, "ls": {}, "hf": {}}
    for _date in sorted(snapshots.keys()):
        snap = snapshots[_date] or {}
        for board in ("lmarena", "aa", "ls", "hf"):
            m = snap.get(board, {}) or {}
            for model, val in m.items():
                ck = canon_key(model)
                if not ck:
                    continue
                rank = val if isinstance(val, int) else None
                hist[board].setdefault(ck, [])
                # 同日期多值（变体）取首个有效 rank
                if rank is not None and (not hist[board][ck] or hist[board][ck][-1] is None):
                    hist[board][ck].append(rank)
                elif rank is not None:
                    hist[board][ck].append(rank)
                else:
                    hist[board][ck].append(None)
    return hist


def _normalize_snapshot_orgs(data: dict):
    """快照行防御清洗：历史组装数据曾把中文机构名拼进 model 尾部
    （如「Qwen3.8-Max阿里巴巴」且 org 空），统一按 DL_ORG_SPLIT endswith 拆分。"""
    for board in ("comprehensive", "open_source"):
        for slot in (data.get(board) or {}).values():
            if not isinstance(slot, dict):
                continue
            for row in slot.get("rows") or []:
                if not isinstance(row, dict):
                    continue
                model = str(row.get("model") or "")
                if model and not str(row.get("org") or "").strip():
                    org, m = _split_dl_org(model)
                    if org and m:
                        row["org"], row["model"] = org, m


def _load_cn_snapshot() -> dict:
    """读取国内可直连榜快照（OpenCompass 司南；实时抓取不可达时的兜底）。"""
    data = load_json_soft(CN_SNAPSHOT_PATH, "国内可直连榜快照", default=None)
    if data is None:
        return {}
    _normalize_snapshot_orgs(data)
    return data


def _load_cache() -> dict:
    return load_json_soft(CACHE_PATH, "本地排行榜缓存", default={})


def _save_cache(cache: dict):
    try:
        CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _fill_from_cache(board: dict, cache: dict, snapshot: str):
    """实时源全失败时，用本地缓存快照填充（标注 is_cache）。board 为 {slot:{rows:[]}}。"""
    for slot, ckey in (("lmarena", "lmarena"), ("aa", "aa"),
                       ("ls", "ls"), ("ls", "hf"),
                       ("hf", "hf"), ("hf", "ls")):
        if slot in board and not board[slot]["rows"] and cache.get(ckey):
            cached_rows = [{"model": m, "rank": (v if isinstance(v, int) else None),
                            "score": (v if not isinstance(v, int) else None),
                            "org": "", "open_source": None}
                           for m, v in cache[ckey].items()]
            board[slot] = {
                "source": f"本地缓存快照（{cache.get('snapshot', '未知')}）", "url": "",
                "snapshot": cache.get("snapshot", ""), "criteria": "",
                "rows": cached_rows, "source_region": "cache", "is_cache": True,
            }
            break


__all__ = [
    "CACHE_PATH", "CN_SNAPSHOT_PATH", "SNAPSHOTS_DIR",
    "_load_snapshots", "_save_snapshot", "_seed_bootstrap", "_build_history",
    "_normalize_snapshot_orgs", "_load_cn_snapshot",
    "_load_cache", "_save_cache", "_fill_from_cache",
]
