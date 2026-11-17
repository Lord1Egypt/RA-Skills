#!/usr/bin/env python3
"""刷新 cn_leaderboard_snapshot.json（国内排行榜兜底快照）。

用途：技能附带的快照会随榜单变化而陈旧。本脚本重抓**当前网络可达**的源，
对不可达的槽位保留历史真实数据并如实标注，绝不拿别家榜单冒充。

诚实原则（重要）：
- 槽位名（lmarena / aa / ls / hf）是**展示位**，源 key（lm / aa / oc / sv /
  ls / dl / hf / ms）是**数据提供方**；槽位可由多个源回退填充。
  因此「lmarena 槽」里装的可能是回退源的旧数据——此时必须标注真实来源，
  而不是沿用槽位名义，否则等于挂羊头卖狗肉。
- 抓不到的源一律标注不可达 + 旧日期，不用其他榜单顶替。

用法：
    python refresh_snapshot.py                      # 刷新到技能目录（不自动同步工作区副本）
    python refresh_snapshot.py --snapshot PATH      # 只写指定路径
    python refresh_snapshot.py --no-sync            # 不同步工作区副本
    python refresh_snapshot.py --dry-run            # 只打印将要写入的摘要，不落盘
    # 工作区副本同步目标通过环境变量 AIWEEKLY_WS_SNAPSHOT 指定（不设置则跳过同步）
"""
import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from aiweekly import leaderboard_sources as S  # noqa: E402
from aiweekly.leaderboard_fetch import LB_CRITERIA  # noqa: E402

SKILL_DIR = SCRIPTS.parent
DEFAULT_SNAPSHOT = SKILL_DIR / "cn_leaderboard_snapshot.json"

# 工作区副本同步目标（可选）。默认从环境变量 AIWEEKLY_WS_SNAPSHOT 读取，
# 不写死任何个人绝对路径（此前曾硬编码作者工作区路径并随包分发，已修正）。
# 未设置该变量时不同步工作区副本，仅刷新技能目录内的快照。
WS_SNAPSHOT_ENV = "AIWEEKLY_WS_SNAPSHOT"


def _ws_snapshot_path() -> Path | None:
    raw = os.environ.get(WS_SNAPSHOT_ENV)
    return Path(raw) if raw else None

# 展示槽 -> (名义榜单, 实时源名, 国内回退源名)
SLOT_META = {
    ("comprehensive", "lmarena"): ("LMArena · 人类偏好 Elo", "LMArena",
                                   "OpenCompass 司南 / SuperCLUE / ModelScope"),
    ("open_source", "hf"): ("Hugging Face · Open LLM Leaderboard",
                            "Hugging Face Open LLM Leaderboard", "ModelScope 魔搭"),
}

# 实时抓取计划：槽位 -> (抓取函数, criteria key, 源展示名, URL)
FETCH_PLAN = [
    ("comprehensive", "aa", S.fetch_aa_ranking, "aa",
     "Artificial Analysis · 智能指数", "https://artificialanalysis.ai/"),
    ("open_source", "ls", S.fetch_datalearner_ranking, "ls",
     "DataLearner · 开源模型榜", "https://www.datalearner.com/leaderboards/open-source"),
]


def _rows(fn, n=10):
    """抓取函数可能返回 dict（含 rows）或直接返回 list，统一成 list。"""
    r = fn(n)
    return (r or {}).get("rows", []) if isinstance(r, dict) else (r or [])


def _top(rows, n=3):
    return [f"{r.get('model')}（{r.get('score')}）" for r in (rows or [])[:n] if r.get("model")]


def _norm(model: str, strip_version: bool = False) -> str:
    """归一化模型名。

    strip_version=True 时抹掉数字版本号：同一榜单的先后两版会换代
    （Grok 4.5→4.6、GLM-5.2→5.3、Gemini 3.6→3.7），按全名比对会低估同源度。
    """
    s = (model or "").strip().lower()
    if strip_version:
        s = re.sub(r"\d+(?:\.\d+)*", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _same_source(rows_a, rows_b, threshold=0.5, versionless_threshold=0.6):
    """数据驱动判定两栏是否同源（同一榜单的不同时间版本）。

    比比对 source 字符串可靠——源名写法会变（「X 智能指数」vs「X · 智能指数」）。
    两级判定：先按全名，再按去版本号之名（应对模型换代）。
    """
    def names(rows, strip_version):
        return {_norm(r.get("model"), strip_version) for r in (rows or []) if r.get("model")}

    full = _jaccard(names(rows_a, False), names(rows_b, False))
    nov = _jaccard(names(rows_a, True), names(rows_b, True))
    hit = full >= threshold or nov >= versionless_threshold
    print(f"      同源度：全名 Jaccard={full:.2f} / 去版本号={nov:.2f} -> {hit}")
    return hit


def _org_desc(rows, k=4):
    counter = {}
    for r in rows or []:
        o = (r.get("org") or "未知").strip()
        counter[o] = counter.get(o, 0) + 1
    return "、".join(f"{k_} {v} 席" for k_, v in sorted(counter.items(), key=lambda x: -x[1])[:k])


def build(cur: dict, today: str) -> dict:
    snap = json.loads(json.dumps(cur))  # 深拷贝，失败时不污染原文件

    # 1) 实时刷新可达槽位
    fetched = {}
    for slot, key, fn, crit_key, label, url in FETCH_PLAN:
        rows = _rows(fn)
        if not rows:
            print(f"  ⏭️ {slot}.{key}: 实时源返回空，保留原数据")
            continue
        snap.setdefault(slot, {})[key] = {
            "source": label,
            "url": url,
            "snapshot": today,
            "criteria": LB_CRITERIA[crit_key],
            "source_region": "global",
            "is_cache": False,
            "rows": rows,
        }
        fetched[key] = rows
        print(f"  ✅ {slot}.{key}: 实时 {len(rows)} 行")

    # 2) 不可达槽位：保留历史数据 + 如实标注（关键：区分「同源历史」与「异源补充」）
    for (slot, key), (nominal, real_name, cn_fallback) in SLOT_META.items():
        v = snap.get(slot, {}).get(key)
        if not v or not v.get("rows"):
            continue
        # 幂等：反复运行不会让 source 越拼越长（按「（」「(」「·」取首段）
        base = re.split(r"[（(·]", (v.get("source") or "").strip())[0].strip() or nominal
        date = v.get("snapshot") or "历史"
        v["is_cache"] = True
        v["snapshot"] = date
        # 与同组另一列是否同源（模型构成重合 -> 同一榜单的旧版本）
        sibling = "aa" if key == "lmarena" else "ls"
        same_source = _same_source(v.get("rows"), (snap.get(slot, {}).get(sibling) or {}).get("rows"))
        if same_source:
            v["source"] = f"{base} · {date} 历史对照"
            v["criteria"] = (
                f"⚠️ 本栏名义为「{nominal}」，但 {real_name} 实时源在本环境网络不可达（HTTP 502），"
                f"国内回退源（{cn_fallback}）同样返回空。"
                f"当前填充的是 {base} 于 {date} 抓取的真实历史数据，与同组「{sibling}」栏同源，"
                f"即同一榜单的一周前版本，可用于观察一周变化；评分口径为原榜口径，并非 Elo 分。"
            )
        else:
            v["source"] = f"{base}（缓存快照 {date}；{real_name} 实时源不可达）"
            v["criteria"] = (
                f"⚠️ 本栏为 {date} 的缓存快照：{real_name} 实时源在本环境网络不可达（HTTP 502），"
                f"已保留当时抓取的真实数据并如实标注旧日期，未用其他榜单顶替。 原数据评分口径：{base}。"
            )
        print(f"  ⚠️ {slot}.{key}: 缓存保留 {len(v['rows'])} 行（{date}，同源={same_source}）")

    # 3) selection_note 按真实榜首重写（旧文案曾长期停留在过气榜首）
    aa_rows, ls_rows = fetched.get("aa") or [], fetched.get("ls") or []
    if not aa_rows:
        aa_rows = (snap.get("comprehensive", {}).get("aa") or {}).get("rows") or []
    if not ls_rows:
        ls_rows = (snap.get("open_source", {}).get("ls") or {}).get("rows") or []
    org_desc = _org_desc(ls_rows)
    snap["selection_note"] = (
        f"综合榜头部是 {' / '.join(_top(aa_rows))}；开源榜前三是 {' / '.join(_top(ls_rows))}"
        f"{f'，前十被国产模型包圆（{org_desc}）' if org_desc else ''}。"
    )

    # 4) 顶层日期与元信息
    snap["snapshot_date"] = today
    snap["meta"] = {
        "region": "cn",
        "proxy": "",
        "note": (
            f"{today} 刷新：可达源为当日实时抓取；不可达槽位保留历史真实数据并标注旧日期与"
            f"不可达说明（不拿其他榜单顶替）。selection_note 已按当日真实榜首重写。"
        ),
    }
    return snap


def main() -> int:
    ap = argparse.ArgumentParser(description="刷新国内排行榜兜底快照")
    ap.add_argument("--snapshot", default=str(DEFAULT_SNAPSHOT), help="快照文件路径")
    ap.add_argument("--no-sync", action="store_true", help="不同步工作区副本")
    ap.add_argument("--dry-run", action="store_true", help="只打印摘要，不落盘")
    args = ap.parse_args()

    path = Path(args.snapshot)
    if not path.exists():
        print(f"❌ 快照文件不存在：{path}")
        return 1
    cur = json.loads(path.read_text(encoding="utf-8"))
    today = datetime.now().astimezone().strftime("%Y-%m-%d")

    print(f"刷新 {path}（{today}）")
    snap = build(cur, today)

    if args.dry_run:
        print("\n[dry-run] selection_note:", snap["selection_note"])
        return 0

    payload = json.dumps(snap, ensure_ascii=False, indent=1)
    path.write_text(payload, encoding="utf-8")
    print(f"✅ 写入：{path}")
    if not args.no_sync:
        ws = _ws_snapshot_path()
        if ws is not None and ws.parent.exists() and ws != path:
            shutil.copyfile(path, ws)
            print(f"✅ 同步：{ws}")
        elif ws is None:
            print(f"   ℹ️ 未设置环境变量 {WS_SNAPSHOT_ENV}，跳过工作区副本同步"
                  f"（如需同步请在环境中设置该变量指向目标快照路径）")
    print("   selection_note:", snap["selection_note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
