"""
Peer selector (v3).

Strategy:
  1. Get target's board memberships via eastmoney F10 ssbk
  2. Classify boards into industry / concept / theme, filter out technical/region tags
  3. Pick 1-2 industry + 1-2 concept + fillers → 3-5 peers total
  4. For each board, fetch constituents DIRECTLY from eastmoney (bypassing akshare rate limits)
     and pick the liquid representative (highest trading amount excluding target/ST)
"""
from __future__ import annotations
import re
import sys
import os
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sources import eastmoney  # noqa: E402


EXCLUDE_BOARD_PATTERNS = [
    r"昨日.*", r"最近.*", r"^\d{4}年.*", r".*板块$", r".*重仓$",
    r".*热股$", r".*龙头$", r".*一字$", r"融资融券", r"AH股",
    r"深股通", r"沪股通", r"MSCI.*", r"富时.*", r"证金持股",
    r"国企改革", r".*基金重仓$", r"^H股$", r"破净股",
    r"同花顺.*", r"次新股", r"小盘股", r"大盘股",
    r"预盈预增", r"预亏预减", r".*退市",
]

INDUSTRY_SUFFIX = re.compile(r"[Ⅰ-Ⅶ]$")

CONCEPT_KEYWORDS = [
    "新能源", "光伏", "锂电", "氢能", "储能", "5G", "半导体", "芯片",
    "机器人", "区块链", "元宇宙", "人工智能", "AI", "液冷", "算力",
    "数据中心", "服务器", "云计算", "军工", "航天", "航空",
    "特斯拉", "华为", "苹果", "宁德", "北斗", "光刻", "MCU", "GPU",
    "智能驾驶", "无人驾驶", "自动驾驶", "充电桩", "换电", "动力电池",
    "钠离子", "固态电池", "复合集流体", "一体化压铸", "CPO", "HBM",
    "电池", "汽车热管理", "石墨烯", "超级电容", "燃料电池",
]


def _should_exclude(name: str) -> bool:
    return any(re.match(pat, name) for pat in EXCLUDE_BOARD_PATTERNS)


def _is_industry_board(item: dict) -> bool:
    return bool(INDUSTRY_SUFFIX.search(item.get("board_name", "")))


def _is_concept_board(item: dict) -> bool:
    name = item.get("board_name", "")
    return any(k in name for k in CONCEPT_KEYWORDS) or name.endswith("概念")


def classify_boards(ssbk: list[dict]) -> dict:
    industry, concept, theme = [], [], []
    for item in ssbk:
        if _should_exclude(item.get("board_name", "")):
            continue
        if _is_industry_board(item):
            industry.append(item)
        elif _is_concept_board(item):
            concept.append(item)
        else:
            theme.append(item)
    for bucket in (industry, concept, theme):
        bucket.sort(key=lambda x: x.get("rank") or 999)
    return {"industry": industry, "concept": concept, "theme": theme}


def _pick_representative(board_code: str, target_code6: str,
                         exclude: set) -> Optional[dict]:
    df = eastmoney.get_board_members(board_code, limit=30)
    if df is None or len(df) == 0:
        return None

    def _ok(row):
        c = str(row["code"])
        n = str(row["name"])
        if c == target_code6 or c in exclude:
            return False
        if "ST" in n or "*" in n or "退" in n:
            return False
        if row.get("price") is None:
            return False
        return True

    filtered = df[df.apply(_ok, axis=1)]
    if len(filtered) == 0:
        return None

    # Rank by trading amount (元) — rewards liquidity + scale
    filtered = filtered.sort_values("amount", ascending=False, na_position="last")
    top = filtered.iloc[0]
    return {"code6": str(top["code"]), "name": str(top["name"])}


def select_peers(code6: str, max_peers: int = 4, verbose: bool = False) -> list[dict]:
    try:
        boards_info = eastmoney.get_boards_of(code6)
    except Exception as e:
        if verbose:
            print(f"[peer_selector] boards fetch failed: {e}", file=sys.stderr)
        return []

    classified = classify_boards(boards_info.get("ssbk", []))

    if verbose:
        print(f"[peer_selector] industry: {[b['board_name'] for b in classified['industry']]}", file=sys.stderr)
        print(f"[peer_selector] concept: {[b['board_name'] for b in classified['concept']]}", file=sys.stderr)
        print(f"[peer_selector] theme: {[b['board_name'] for b in classified['theme']]}", file=sys.stderr)

    picks, exclude = [], {code6}

    for board in classified["industry"][:3]:
        if sum(1 for p in picks if p["source"].startswith("industry")) >= 2:
            break
        rep = _pick_representative(board["board_code"], code6, exclude)
        if rep:
            picks.append({**rep, "source": f"industry:{board['board_name']}"})
            exclude.add(rep["code6"])

    for board in classified["concept"][:5]:
        if sum(1 for p in picks if p["source"].startswith("concept")) >= 2:
            break
        rep = _pick_representative(board["board_code"], code6, exclude)
        if rep:
            picks.append({**rep, "source": f"concept:{board['board_name']}"})
            exclude.add(rep["code6"])

    for board in classified["theme"][:6]:
        if len(picks) >= max_peers:
            break
        rep = _pick_representative(board["board_code"], code6, exclude)
        if rep:
            picks.append({**rep, "source": f"theme:{board['board_name']}"})
            exclude.add(rep["code6"])

    return picks[:max_peers]


if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print("usage: peer_selector.py <code6>")
        sys.exit(1)
    picks = select_peers(sys.argv[1], verbose=True)
    print(json.dumps(picks, ensure_ascii=False, indent=2))
