"""WHO ICTRP 切片累积检索（A 层优化，2026-09-06）。

背景：统一网关 WHO search 模式单次仅回 ~10 条（total>400 时早退 + escalate 信号），
combined 需真筛选且 ~165s/次。本适配器把宽查询切成 N 个窄子查询逐片拉取，
按注册号（Main ID）客户端合并去重，用多次 10 条的小响应换总量。

切片策略（可组合）：
  --by-registry  按注册库后缀切片（EUCTR/JPRN/CTRI/NTR/…），WHO 自由词可命中 Main ID
  --by-year      按注册年份切片（keyword + 年份词）
  自定义 --slices "osimertinib EUCTR,osimertinib JPRN,…"

实现方式：子进程调用既有 search_ictrp.py --source who --q <slice>（复用其
降级守卫/超时重试/探针逻辑，零侵入），读取各自输出 JSON 合并。

用法：
  python search_who_sliced.py --drug osimertinib --cond "non-small cell lung cancer" \
      --by-registry --by-year --out merged.json
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICTRP = os.path.join(HERE, "search_ictrp.py")
PY = sys.executable

# WHO ICTRP 一级注册库 Main ID 前缀（自由词可命中）
REGISTRY_SUFFIXES = ["EUCTR", "JPRN", "CTRI", "NTR", "SLCTR", "KCT", "RPCEC", "TCTR", "ACTRN"]
# 年份切片（近年为主；更早年份量小，首页 10 条已基本覆盖）
YEAR_SLICES = ["2023", "2024", "2025", "2026"]


def _run_slice(query: str, out_path: str, timeout: int = 120) -> dict:
    """跑一个切片（子进程复用 search_ictrp.py 全部既有守卫）。"""
    cmd = [PY, ICTRP, "--run", "--no-stream", "--source", "who",
           "--q", query, "--out", out_path, "--timeout", str(timeout)]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 90)
    except subprocess.TimeoutExpired:
        pass
    try:
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"records": [], "total_available": 0, "error_msg": "slice run failed"}


def _norm_id(rec: dict) -> str:
    """取记录的唯一注册号（优先 Main ID，回退 project_id/登记号）。"""
    for k in ("Main ID", "project_id", "登记号"):
        v = rec.get(k)
        if v:
            return str(v).strip().upper()
    return ""


def merge_slices(slice_results: list, keyword_stats: dict) -> dict:
    """按注册号合并去重（保持首现顺序）。"""
    merged, seen, dup = [], set(), 0
    for res in slice_results:
        for rec in res.get("records") or []:
            rid = _norm_id(rec)
            if not rid:
                rid = f"IDX::{len(merged)}"
            if rid in seen:
                dup += 1
                continue
            seen.add(rid)
            rec = dict(rec)
            rec["_slice"] = rec.get("_slice", "")
            merged.append(rec)
    total_fields = [r.get("total_available") for r in slice_results]
    return {
        "source": "WHO ICTRP",
        "mode": "sliced",
        "records": merged,
        "total": len(merged),
        "duplicates_removed": dup,
        "total_available_per_slice": total_fields,
        "keyword_stats": keyword_stats,
        "is_partial": True,
        "note": "切片累积=样本合并，非全量；全量需网关真翻页（C 层）或 combined+真筛选",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="WHO ICTRP sliced accumulation search")
    ap.add_argument("--drug", default="", help="药物英文名（如 osimertinib）")
    ap.add_argument("--cond", default="", help="疾病英文名（如 non-small cell lung cancer）")
    ap.add_argument("--slices", default="", help="逗号分隔的自定义切片查询（优先）")
    ap.add_argument("--by-registry", action="store_true", help="按注册库前缀切片")
    ap.add_argument("--by-year", action="store_true", help="按年份切片")
    ap.add_argument("--max-slices", type=int, default=5, help="最多切片数（默认 5，控制配额）")
    ap.add_argument("--timeout", type=int, default=240, help="单片 WHO 等待秒数（网关慢时 120s 会误判超时，默认 240）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", default="", help="切片中间文件目录（默认与 out 同目录）")
    args = ap.parse_args()

    base = " ".join(x for x in (args.drug, args.cond) if x).strip()
    if args.slices:
        queries = [s.strip() for s in args.slices.split(",") if s.strip()]
    else:
        queries = []
        if args.by_registry:
            queries += [f"{base} {sfx}" for sfx in REGISTRY_SUFFIXES]
        if args.by_year:
            queries += [f"{base} {y}" for y in YEAR_SLICES]
        if not queries:
            queries = [base]
    queries = queries[: max(1, args.max_slices)]

    workdir = args.workdir or os.path.dirname(os.path.abspath(args.out))
    os.makedirs(workdir, exist_ok=True)
    print(f"[who-sliced] {len(queries)} slices: {queries}")

    slice_results, kstats = [], {}
    for i, q in enumerate(queries, 1):
        out_i = os.path.join(workdir, f"_who_slice_{i}.json")
        print(f"[who-sliced] slice {i}/{len(queries)}: {q!r}")
        res = _run_slice(q, out_i, args.timeout)
        n = len(res.get("records") or [])
        print(f"[who-sliced]   -> {n} records (total_available={res.get('total_available')})")
        kstats[q] = {"fetched": n, "total_available": res.get("total_available"),
                     "error_msg": res.get("error_msg") or ""}
        for r in (res.get("records") or []):
            r["_slice"] = q
        slice_results.append(res)

    merged = merge_slices(slice_results, kstats)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"[who-sliced] merged {merged['total']} unique records "
          f"(dup removed {merged['duplicates_removed']}) -> {args.out}")


if __name__ == "__main__":
    main()
