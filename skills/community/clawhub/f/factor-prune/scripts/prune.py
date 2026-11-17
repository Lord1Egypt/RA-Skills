#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因子筛选脚本 (Factor Prune Script)
==================================
贪心前向选择 + 去相关 的因子筛选流程。

算法:
  1. 从 input 目录加载所有因子 xlsx，汇总为一张总表
  2. 按 |IR| > ir_threshold 筛选有效因子
  3. 按 |IR| 降序排列
  4. 提取排名第一的因子（有效性最高）
  5. 用 QuantAll batch_factor_corr 计算已选因子与所有剩余因子的相关性
  6. 移除 |IC| > corr_threshold 的因子（冗余）
  7. 从存活因子中提取下一个（|IR| 最高的）
  8. 重复 5-7 直到无候选
  9. 输出最终精选因子清单

命令:
  init      初始化：读取 xlsx → 筛选 → 排序 → 选第一个 → 输出基准+候选
  update    接收相关性结果 → 移除冗余 → 选下一个 → 输出基准+候选
  status    查看当前状态
  finalize  生成最终输出 xlsx
  reset     重置状态（删除 state 文件）
  config    查看/修改配置参数

使用示例:
  python prune.py init --ir-threshold 0.3 --corr-threshold 0.8
  python prune.py update --results corr_results.json
  python prune.py status
  python prune.py finalize
  python prune.py reset
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas is required. Install: pip install pandas openpyxl")
    sys.exit(1)


# ============================================================
# 路径常量
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(SCRIPT_DIR, "state")
STATE_FILE = os.path.join(STATE_DIR, "prune_state.json")
INPUT_DIR = os.path.join(SCRIPT_DIR, "output")     # xlsx 输入目录
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output", "pruned_factors.xlsx")

# QuantAll 任务文件 / 结果文件（走磁盘，避免大 payload 进入对话上下文）
TASK_FILE = os.path.join(STATE_DIR, "task_corr.json")
RESULT_FILE = os.path.join(STATE_DIR, "corr_result.xlsx")

# 相关性矩阵缓存目录：每个基准因子一行，持久化后可重放不同阈值
CORR_CACHE_DIR = os.path.join(STATE_DIR, "corr_cache")
CORR_MATRIX_FILE = os.path.join(STATE_DIR, "corr_matrix.json")
INGEST_MARK = os.path.join(STATE_DIR, "ingested.json")

# 默认配置
DEFAULT_CONFIG = {
    "ir_threshold": 0.3,      # |IR| 阈值，保留有效因子
    "corr_threshold": 0.8,    # |IC| 阈值，移除冗余因子
    "feature_days": 5,        # 因子评估的未来收益天数
}


# ============================================================
# 状态管理
# ============================================================
def load_state():
    """加载状态文件"""
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    # 空字典视为已重置
    return state if state else None


def save_state(state):
    """保存状态文件"""
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def make_factor_record(row, source_file):
    """从 xlsx 行构造因子记录"""
    return {
        "name": str(row["name"]),
        "code": str(row["code"]),
        "IR": float(row["IR"]) if pd.notna(row.get("IR")) else 0.0,
        "IC": float(row["IC"]) if pd.notna(row.get("IC")) else 0.0,
        "time_potential": float(row["time_potential"]) if pd.notna(row.get("time_potential")) else 0.0,
        "feature_days": int(row["feature_days"]) if pd.notna(row.get("feature_days")) else 5,
        "source_file": source_file,
        "abs_IR": abs(float(row["IR"])) if pd.notna(row.get("IR")) else 0.0,
    }


def write_task_file(benchmark_name, benchmark_code, factor_dict):
    """
    生成 QuantAll run_task_file 用的任务文件。

    因子代码体积很大（数百个因子），通过磁盘传递给 QuantAll，
    避免大 payload 进入对话上下文。
    """
    os.makedirs(STATE_DIR, exist_ok=True)
    task = {
        "tool_name": "batch_factor_corr",
        "benchmark_name": benchmark_name,
        "benchmark_code": benchmark_code,
        "factor_dict": factor_dict,
        "save_path": RESULT_FILE,
    }
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    return TASK_FILE


def read_corr_results(path):
    """
    读取相关性结果，支持 xlsx（QuantAll save_path 输出）和 json。
    返回 list[dict]，每项含 name / IC / IR / error_code。
    """
    ext = os.path.splitext(path)[1].lower()

    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
        records = []
        for _, row in df.iterrows():
            rec = {c: row[c] for c in df.columns}
            records.append(rec)
        return records

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "results" in raw:
            return raw["results"]
        if "name" in raw:
            return [raw]
        vals = list(raw.values())
        if vals and isinstance(vals[0], dict):
            return vals
    return []


# ============================================================
# 相关性矩阵缓存
# ============================================================
def load_corr_matrix():
    """加载已缓存的相关性矩阵 {benchmark: {factor: IC}}"""
    if not os.path.exists(CORR_MATRIX_FILE):
        return {}
    with open(CORR_MATRIX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_corr_matrix(matrix):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(CORR_MATRIX_FILE, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False)


def cache_corr_row(benchmark_name, ic_by_name):
    """
    把一轮的相关性结果写入矩阵缓存。

    相关性近似对称，同时反向填充 corr[factor][benchmark]，
    后续若该 factor 成为基准，可直接复用而无需重算。
    """
    matrix = load_corr_matrix()
    row = matrix.setdefault(benchmark_name, {})
    for name, ic in ic_by_name.items():
        row[name] = ic
        matrix.setdefault(name, {})[benchmark_name] = ic
    save_corr_matrix(matrix)
    return len(row)


def ingest_result(path=RESULT_FILE):
    """
    把 QuantAll 输出的相关性结果 xlsx 灌入矩阵缓存。

    基准因子名从结果表的 benchmark_name 列自动识别。
    用 mtime 标记去重，重复调用不会重复写入。
    返回 (benchmark, 条数) 或 None。
    """
    if not os.path.exists(path):
        return None
    mtime = os.path.getmtime(path)

    mark = {}
    if os.path.exists(INGEST_MARK):
        try:
            with open(INGEST_MARK, "r", encoding="utf-8") as f:
                mark = json.load(f)
        except Exception:
            mark = {}
    if mark.get("mtime") == mtime:
        return None  # 已处理过

    df = pd.read_excel(path)
    if "benchmark_name" not in df.columns or df.empty:
        return None
    bench = str(df["benchmark_name"].iloc[0]).strip()

    ic_by_name = {}
    for _, row in df.iterrows():
        n = str(row.get("name", "")).strip()
        if not n:
            continue
        try:
            fv = float(row.get("IC"))
        except (TypeError, ValueError):
            continue
        if fv == fv:  # 排除 NaN
            ic_by_name[n] = fv

    cache_corr_row(bench, ic_by_name)
    with open(INGEST_MARK, "w", encoding="utf-8") as f:
        json.dump({"mtime": mtime, "benchmark": bench}, f)
    return bench, len(ic_by_name)


def greedy_prune(valid_sorted, matrix, corr_threshold):
    """
    基于已缓存的相关性矩阵，执行贪心前向选择 + 去相关。

    返回 (selected, removed, pool_left, missing_benchmark, uncovered)
    missing_benchmark 非 None 表示该基准与部分候选的相关性尚未计算，
    uncovered 即这些待补算的候选（只需算这一部分，已算过的配对复用缓存）。
    """
    pool = list(valid_sorted)
    selected, removed = [], []
    rnd = 0

    while pool:
        rnd += 1
        bench = dict(pool.pop(0))
        bench["round"] = rnd
        selected.append(bench)

        if not pool:
            break

        row = matrix.get(bench["name"], {})

        # 该基准是否已覆盖当前全部候选？未覆盖的需要补算
        uncovered = [f for f in pool if f["name"] not in row]
        if uncovered:
            return selected, removed, pool, bench, uncovered

        survivors = []
        for f in pool:
            ic = row[f["name"]]
            if abs(ic) > corr_threshold:
                r = dict(f)
                r["removed_by"] = bench["name"]
                r["corr_IC"] = ic
                r["round"] = rnd
                removed.append(r)
            else:
                survivors.append(f)
        pool = survivors

    return selected, removed, [], None, []


# ============================================================
# 命令实现
# ============================================================
def load_all_factors():
    """读取 input 目录下所有因子 xlsx，汇总为记录列表"""
    all_factors = []
    xlsx_files = sorted([f for f in os.listdir(INPUT_DIR)
                         if f.endswith(".xlsx") and not f.startswith("pruned")])
    for fname in xlsx_files:
        fpath = os.path.join(INPUT_DIR, fname)
        try:
            df = pd.read_excel(fpath)
            if df.empty or "name" not in df.columns:
                continue
            for _, row in df.iterrows():
                all_factors.append(make_factor_record(row, fname))
        except Exception as e:
            print(f"WARN: Failed to read {fname}: {e}", file=sys.stderr)
    return all_factors


# ============================================================
# QuantAll MCP 直连（HTTP JSON-RPC，供全自动模式使用）
# ============================================================
class QuantAllClient:
    """
    直连 QuantAll 的 HTTP MCP 服务（默认 localhost:8686）。

    全自动模式下由脚本自己发起相关性计算，无需人工/AI 逐轮转发，
    也避免大体积返回值在对话中反复传递。
    """

    def __init__(self, url="http://127.0.0.1:8686/mcp", timeout=3600):
        self.url = url
        self.timeout = timeout
        self.session_id = None

    def _post(self, payload, expect_response=True):
        import urllib.request
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        if self.session_id:
            req.add_header("Mcp-Session-Id", self.session_id)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            sid = resp.headers.get("Mcp-Session-Id")
            if sid:
                self.session_id = sid
            if not expect_response:
                resp.read()
                return None
            body = resp.read().decode("utf-8", "replace")
        return self._parse(body)

    @staticmethod
    def _parse(body):
        """解析 SSE / 纯 JSON 响应"""
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                line = line[5:].strip()
            if line.startswith("{"):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "result" in obj or "error" in obj:
                    return obj
        return None

    def connect(self):
        self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "factor-prune", "version": "1.0"},
            },
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"},
                   expect_response=False)
        return self.session_id

    def call_tool(self, name, arguments):
        resp = self._post({
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        if resp is None:
            raise RuntimeError("No response from QuantAll MCP")
        if "error" in resp:
            raise RuntimeError(f"QuantAll error: {resp['error']}")
        return resp.get("result")


def cmd_run(args):
    """
    全自动模式：脚本直连 QuantAll，自己跑完整个贪心筛选流程。

    每轮只把"尚未算过的配对"发给 QuantAll，结果落盘后并入相关性矩阵，
    中断后重跑可从缓存续跑，不会重复计算。
    """
    client = QuantAllClient(url=args.mcp_url, timeout=args.timeout)
    try:
        sid = client.connect()
        print(f"[connect] QuantAll session {sid}", flush=True)
    except Exception as e:
        print(json.dumps({"error": f"Cannot connect QuantAll at {args.mcp_url}: {e}"},
                         ensure_ascii=False))
        return

    all_factors = load_all_factors()
    valid = [f for f in all_factors if f["abs_IR"] > args.ir_threshold]
    valid.sort(key=lambda x: x["abs_IR"], reverse=True)
    print(f"[init] {len(all_factors)} factors, {len(valid)} valid "
          f"(|IR|>{args.ir_threshold}), corr_threshold={args.corr_threshold}", flush=True)

    started = datetime.now()
    for it in range(1, args.max_rounds + 1):
        ingest_result()
        matrix = load_corr_matrix()
        selected, removed, pool_left, missing, uncovered = greedy_prune(
            valid, matrix, args.corr_threshold)

        if missing is None:
            _write_outputs(selected, removed,
                           {"ir_threshold": args.ir_threshold,
                            "corr_threshold": args.corr_threshold})
            elapsed = (datetime.now() - started).total_seconds()
            print(json.dumps({
                "action": "finished",
                "selected_count": len(selected),
                "removed_count": len(removed),
                "valid_factors": len(valid),
                "elapsed_sec": round(elapsed, 1),
                "output_file": OUTPUT_FILE,
                "selected_factors": [s["name"] for s in selected],
            }, ensure_ascii=False, indent=2), flush=True)
            return

        print(f"[round {len(selected)}] benchmark={missing['name']} "
              f"(IR={missing['IR']:.4f}) compute={len(uncovered)} "
              f"cached={len(pool_left) - len(uncovered)} "
              f"selected={len(selected)} removed={len(removed)}", flush=True)

        try:
            client.call_tool("batch_factor_corr", {
                "benchmark_name": missing["name"],
                "benchmark_code": missing["code"],
                "factor_dict": {f["name"]: f["code"] for f in uncovered},
                "save_path": RESULT_FILE,
            })
        except Exception as e:
            print(json.dumps({"error": f"Round failed: {e}",
                              "benchmark": missing["name"]}, ensure_ascii=False))
            return

    print(json.dumps({"action": "max_rounds_reached", "max_rounds": args.max_rounds},
                     ensure_ascii=False))


def cmd_step(args):
    """
    单步推进（缓存驱动的主循环）：
      1. 自动吸收上一轮 QuantAll 结果到相关性矩阵
      2. 用矩阵重放贪心筛选
      3. 若还缺某基准的相关性行 → 生成下一轮任务文件
         若已完整 → 直接写出最终结果

    每轮只需两步：prune.py step  →  QuantAll run_task_file  →  prune.py step ...
    """
    ing = ingest_result()

    matrix = load_corr_matrix()
    all_factors = load_all_factors()
    valid = [f for f in all_factors if f["abs_IR"] > args.ir_threshold]
    valid.sort(key=lambda x: x["abs_IR"], reverse=True)

    selected, removed, pool_left, missing, uncovered = greedy_prune(
        valid, matrix, args.corr_threshold)

    out = {
        "ingested": {"benchmark": ing[0], "rows": ing[1]} if ing else None,
        "ir_threshold": args.ir_threshold,
        "corr_threshold": args.corr_threshold,
        "total_factors": len(all_factors),
        "valid_factors": len(valid),
        "selected_count": len(selected),
        "removed_count": len(removed),
        "candidates_left": len(pool_left),
    }

    if missing is None:
        config = {"ir_threshold": args.ir_threshold, "corr_threshold": args.corr_threshold}
        _write_outputs(selected, removed, config)
        out["action"] = "finished"
        out["output_file"] = OUTPUT_FILE
        out["selected_factors"] = [s["name"] for s in selected]
        out["message"] = (f"DONE. {len(selected)} factors selected from {len(valid)} valid "
                          f"({len(removed)} removed as redundant).")
    else:
        # 只补算尚未覆盖的配对，已缓存的复用
        write_task_file(missing["name"], missing["code"],
                        {f["name"]: f["code"] for f in uncovered})
        out["action"] = "correlate"
        out["next_benchmark"] = missing["name"]
        out["next_benchmark_IR"] = round(missing["IR"], 4)
        out["to_compute"] = len(uncovered)
        out["reused_from_cache"] = len(pool_left) - len(uncovered)
        out["task_file"] = TASK_FILE
        out["message"] = (f"Round {len(selected)}: need corr for '{missing['name']}' "
                          f"vs {len(uncovered)} candidates "
                          f"({len(pool_left) - len(uncovered)} reused from cache). "
                          f"Run QuantAll run_task_file.")

    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_replay(args):
    """
    基于已缓存的相关性矩阵重放贪心筛选（不调用 QuantAll）。

    用途：调整 ir_threshold / corr_threshold 后立即看到新结果，
    只有当矩阵缺少某个基准的相关性行时才需要补算。
    """
    matrix = load_corr_matrix()
    if not matrix:
        print(json.dumps({"error": "No corr matrix cached. Run init + update first."},
                         ensure_ascii=False))
        return

    all_factors = load_all_factors()
    valid = [f for f in all_factors if f["abs_IR"] > args.ir_threshold]
    valid.sort(key=lambda x: x["abs_IR"], reverse=True)

    selected, removed, pool_left, missing, uncovered = greedy_prune(
        valid, matrix, args.corr_threshold)

    out = {
        "action": "replay",
        "ir_threshold": args.ir_threshold,
        "corr_threshold": args.corr_threshold,
        "total_factors": len(all_factors),
        "valid_factors": len(valid),
        "selected_count": len(selected),
        "removed_count": len(removed),
        "pool_left": len(pool_left),
        "cached_benchmarks": len(matrix),
        "complete": missing is None,
    }
    if missing is not None:
        out["missing_benchmark"] = missing["name"]
        out["message"] = (f"Replayed {len(selected)} rounds. Need correlation row for "
                          f"'{missing['name']}' to continue ({len(pool_left)} candidates left).")
    else:
        out["message"] = (f"Replay complete: {len(selected)} factors selected, "
                          f"{len(removed)} removed.")
    out["selected_factors"] = [s["name"] for s in selected]

    if args.save:
        _write_outputs(selected, removed,
                       {"ir_threshold": args.ir_threshold,
                        "corr_threshold": args.corr_threshold})
        out["output_file"] = OUTPUT_FILE
    print(json.dumps(out, ensure_ascii=False, indent=2))


def _write_outputs(selected, removed, config):
    """写出精选因子表和被移除因子表"""
    rows = []
    for i, f in enumerate(selected):
        rows.append({
            "rank": i + 1,
            "name": f["name"],
            "code": f["code"],
            "IR": f["IR"],
            "IC": f["IC"],
            "abs_IR": f["abs_IR"],
            "time_potential": f.get("time_potential", 0),
            "feature_days": f.get("feature_days", 5),
            "source_file": f.get("source_file", ""),
            "round": f.get("round", i + 1),
        })
    pd.DataFrame(rows).to_excel(OUTPUT_FILE, index=False)

    removed_file = os.path.join(SCRIPT_DIR, "output", "pruned_removed.xlsx")
    if removed:
        pd.DataFrame(removed).to_excel(removed_file, index=False)
    return OUTPUT_FILE, removed_file


def cmd_init(args):
    """初始化：读取 xlsx → 筛选 → 排序 → 选第一个因子"""
    config = {
        "ir_threshold": args.ir_threshold,
        "corr_threshold": args.corr_threshold,
        "feature_days": args.feature_days,
    }

    # 1. 读取所有 xlsx
    all_factors = []
    xlsx_files = sorted([f for f in os.listdir(INPUT_DIR)
                         if f.endswith(".xlsx") and not f.startswith("pruned")])

    if not xlsx_files:
        print(json.dumps({"error": "No xlsx files found in output directory"}, ensure_ascii=False))
        return

    for fname in xlsx_files:
        fpath = os.path.join(INPUT_DIR, fname)
        try:
            df = pd.read_excel(fpath)
            if df.empty or "name" not in df.columns:
                continue
            for _, row in df.iterrows():
                rec = make_factor_record(row, fname)
                all_factors.append(rec)
        except Exception as e:
            print(f"WARN: Failed to read {fname}: {e}", file=sys.stderr)

    total = len(all_factors)
    if total == 0:
        print(json.dumps({"error": "No factors loaded from xlsx files"}, ensure_ascii=False))
        return

    # 2. 筛选有效因子 |IR| > threshold
    valid = [f for f in all_factors if f["abs_IR"] > config["ir_threshold"]]
    valid_count = len(valid)

    if valid_count == 0:
        print(json.dumps({
            "error": f"No factors with |IR| > {config['ir_threshold']} found",
            "total_factors": total,
            "config": config
        }, ensure_ascii=False))
        return

    # 3. 按 |IR| 降序排列
    valid.sort(key=lambda x: x["abs_IR"], reverse=True)

    # 4. 选第一个因子
    selected = [valid[0]]
    remaining = valid[1:]

    # 5. 保存状态
    state = {
        "config": config,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "total_factors": total,
        "valid_count": valid_count,
        "selected": [],
        "removed": [],
        "remaining": remaining,
        "round": 0,
        "finished": False,
    }

    # 把第一个因子标记为已选
    first = valid[0].copy()
    first["round"] = 1
    first["selected_at"] = datetime.now().isoformat()
    state["selected"] = [first]
    state["round"] = 1
    save_state(state)

    # 6. 生成 QuantAll 任务文件（因子代码走磁盘，不进对话上下文）
    task_path = write_task_file(
        first["name"], first["code"],
        {f["name"]: f["code"] for f in remaining}
    )

    # 7. 输出给 AI 用的摘要（不含 factor_dict）
    output = {
        "action": "correlate",
        "round": 1,
        "benchmark_name": first["name"],
        "benchmark_IR": round(first["IR"], 4),
        "remaining_count": len(remaining),
        "selected_count": 1,
        "total_factors": total,
        "valid_factors": valid_count,
        "config": config,
        "task_file": task_path,
        "result_file": RESULT_FILE,
        "message": f"Round 1: selected '{first['name']}' (IR={first['IR']:.4f}). "
                   f"Run QuantAll run_task_file on task_file, then 'update'."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update(args):
    """接收相关性结果 → 移除冗余 → 选下一个因子"""
    state = load_state()
    if state is None:
        print(json.dumps({"error": "No state found. Run 'init' first."}, ensure_ascii=False))
        return

    if state["finished"]:
        print(json.dumps({"action": "finished", "message": "Already finished. Run 'finalize'."}, ensure_ascii=False))
        return

    if not state["remaining"]:
        print(json.dumps({"action": "finished", "message": "No remaining factors. Run 'finalize'."}, ensure_ascii=False))
        return

    # 读取相关性结果（默认读 QuantAll 输出的 xlsx）
    results_path = args.results or RESULT_FILE
    if not os.path.exists(results_path):
        print(json.dumps({"error": f"Results file not found: {results_path}"}, ensure_ascii=False))
        return

    corr_results = read_corr_results(results_path)
    if not corr_results:
        print(json.dumps({"error": f"No records parsed from: {results_path}"}, ensure_ascii=False))
        return

    # 构建因子名 → IC 映射
    def _num(v):
        """安全转 float，NaN/None/非数值 → None"""
        if v is None:
            return None
        try:
            fv = float(v)
        except (TypeError, ValueError):
            return None
        if fv != fv:  # NaN
            return None
        return fv

    corr_map = {}
    for item in corr_results:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        ic = _num(item.get("IC"))
        ir = _num(item.get("IR"))

        err = item.get("error_code", 0)
        if isinstance(err, dict):
            has_error = len(err.get("names", [])) > 0
        elif isinstance(err, str):
            s = err.strip()
            has_error = s not in ("", "0", "[]", "{'names': []}", '{"names": []}', "nan")
        else:
            has_error = bool(_num(err))

        # IC 缺失也视为计算失败（保守保留该因子）
        if ic is None:
            has_error = True

        corr_map[name] = {
            "IC": ic if ic is not None else 0.0,
            "IR": ir if ir is not None else 0.0,
            "has_error": has_error,
        }

    # 当前轮次信息
    current_round = state["round"]
    current_benchmark = state["selected"][-1]["name"] if state["selected"] else "unknown"
    threshold = state["config"]["corr_threshold"]

    # 持久化到相关性矩阵，供 replay 以不同阈值重放（避免重算）
    cache_corr_row(current_benchmark,
                   {n: v["IC"] for n, v in corr_map.items() if not v["has_error"]})

    # 遍历剩余因子，决定保留还是移除
    new_remaining = []
    newly_removed = []

    for factor in state["remaining"]:
        name = factor["name"]
        corr = corr_map.get(name)

        if corr is None:
            # 该因子不在相关性结果中（可能是 benchmark 自己），保留
            new_remaining.append(factor)
            continue

        if corr["has_error"]:
            # 计算出错的因子，保留（不因错误而移除）
            new_remaining.append(factor)
            continue

        abs_ic = abs(corr["IC"])
        if abs_ic > threshold:
            # 冗余因子，移除
            removed_rec = factor.copy()
            removed_rec["removed_by"] = current_benchmark
            removed_rec["corr_IC"] = corr["IC"]
            removed_rec["corr_IR"] = corr["IR"]
            removed_rec["round"] = current_round
            newly_removed.append(removed_rec)
        else:
            # 保留，并更新相关性信息
            factor["corr_with_last_selected"] = corr["IC"]
            new_remaining.append(factor)

    # 更新状态
    state["removed"].extend(newly_removed)
    state["remaining"] = new_remaining

    # 选下一个因子
    if new_remaining:
        # 按 |IR| 降序，选第一个
        new_remaining.sort(key=lambda x: x["abs_IR"], reverse=True)
        next_factor = new_remaining[0].copy()
        next_factor["round"] = current_round + 1
        next_factor["selected_at"] = datetime.now().isoformat()
        state["selected"].append(next_factor)
        state["remaining"] = new_remaining[1:]
        state["round"] = current_round + 1

        if state["remaining"]:
            # 还有候选：生成下一轮任务文件
            task_path = write_task_file(
                next_factor["name"], next_factor["code"],
                {f["name"]: f["code"] for f in state["remaining"]}
            )
            output = {
                "action": "correlate",
                "round": current_round + 1,
                "benchmark_name": next_factor["name"],
                "benchmark_IR": round(next_factor["IR"], 4),
                "remaining_count": len(state["remaining"]),
                "selected_count": len(state["selected"]),
                "removed_this_round": len(newly_removed),
                "removed_total": len(state["removed"]),
                "task_file": task_path,
                "result_file": RESULT_FILE,
                "message": f"Round {current_round + 1}: selected '{next_factor['name']}' "
                           f"(IR={next_factor['IR']:.4f}). Removed {len(newly_removed)} redundant. "
                           f"{len(state['remaining'])} remaining."
            }
        else:
            # 最后一个因子已选中，无候选可比
            state["finished"] = True
            output = {
                "action": "finished",
                "round": current_round + 1,
                "selected_count": len(state["selected"]),
                "removed_count": len(state["removed"]),
                "removed_this_round": len(newly_removed),
                "message": f"All done! Selected {len(state['selected'])} factors, "
                           f"removed {len(state['removed'])} redundant. Run 'finalize'."
            }
    else:
        # 没有剩余因子了
        state["finished"] = True
        output = {
            "action": "finished",
            "round": current_round,
            "selected_count": len(state["selected"]),
            "selected_so_far": [s["name"] for s in state["selected"]],
            "removed_count": len(state["removed"]),
            "message": f"All done! Selected {len(state['selected'])} factors, "
                       f"removed {len(state['removed'])} redundant. Run 'finalize'."
        }

    state["updated_at"] = datetime.now().isoformat()
    save_state(state)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_status(args):
    """查看当前状态"""
    state = load_state()
    if state is None:
        print(json.dumps({"status": "not_initialized", "message": "Run 'init' first."}, ensure_ascii=False))
        return

    selected_names = [s["name"] for s in state["selected"]]
    removed_count = len(state["removed"])
    remaining_count = len(state["remaining"])

    output = {
        "status": "finished" if state["finished"] else "in_progress",
        "round": state["round"],
        "total_factors": state["total_factors"],
        "valid_factors": state["valid_count"],
        "selected_count": len(state["selected"]),
        "remaining_count": remaining_count,
        "removed_count": removed_count,
        "selected_factors": selected_names,
        "config": state["config"],
        "created_at": state["created_at"],
        "updated_at": state["updated_at"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_finalize(args):
    """生成最终输出 xlsx"""
    state = load_state()
    if state is None:
        print(json.dumps({"error": "No state found. Run 'init' first."}, ensure_ascii=False))
        return

    selected = state["selected"]
    if not selected:
        print(json.dumps({"error": "No selected factors. Nothing to finalize."}, ensure_ascii=False))
        return

    # 构造输出 DataFrame
    rows = []
    for i, f in enumerate(selected):
        rows.append({
            "rank": i + 1,
            "name": f["name"],
            "code": f["code"],
            "IR": f["IR"],
            "IC": f["IC"],
            "abs_IR": f["abs_IR"],
            "time_potential": f.get("time_potential", 0),
            "feature_days": f.get("feature_days", 5),
            "source_file": f.get("source_file", ""),
            "round": f.get("round", i + 1),
            "selected_at": f.get("selected_at", ""),
        })

    df_out = pd.DataFrame(rows)
    df_out.to_excel(OUTPUT_FILE, index=False)

    # 同时输出被移除因子的详情
    removed_file = os.path.join(SCRIPT_DIR, "output", "pruned_removed.xlsx")
    if state["removed"]:
        df_removed = pd.DataFrame(state["removed"])
        df_removed.to_excel(removed_file, index=False)
    else:
        removed_file = None

    output = {
        "action": "finalized",
        "output_file": OUTPUT_FILE,
        "removed_file": removed_file,
        "selected_count": len(selected),
        "removed_count": len(state["removed"]),
        "selected_factors": [f["name"] for f in selected],
        "config": state["config"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_reset(args):
    """重置状态"""
    # 覆盖写空状态而非删除文件（沙箱环境下 os.remove 可能被拦截）
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)
    msg = "State cleared."
    if args.keep_matrix is False and os.path.exists(CORR_MATRIX_FILE):
        with open(CORR_MATRIX_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        msg += " Corr matrix also cleared."
    else:
        msg += " Corr matrix cache kept."
    print(json.dumps({"action": "reset", "message": msg}, ensure_ascii=False))


def cmd_config(args):
    """查看/修改配置"""
    state = load_state()
    if state is None:
        print(json.dumps({
            "status": "not_initialized",
            "default_config": DEFAULT_CONFIG,
            "message": "Run 'init' with --ir-threshold / --corr-threshold to set config."
        }, ensure_ascii=False))
        return

    if args.ir_threshold is not None:
        state["config"]["ir_threshold"] = args.ir_threshold
    if args.corr_threshold is not None:
        state["config"]["corr_threshold"] = args.corr_threshold
    save_state(state)

    print(json.dumps({"config": state["config"]}, ensure_ascii=False, indent=2))


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="因子筛选脚本 (Factor Prune Script) - Greedy forward selection with decorrelation"
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = sub.add_parser("init", help="Initialize: load xlsx, filter, sort, select first factor")
    p_init.add_argument("--ir-threshold", type=float, default=0.3, help="|IR| threshold for valid factors (default: 0.3)")
    p_init.add_argument("--corr-threshold", type=float, default=0.8, help="|IC| threshold for redundant factors (default: 0.8)")
    p_init.add_argument("--feature-days", type=int, default=5, help="Feature days (default: 5)")

    # update
    p_update = sub.add_parser("update", help="Apply correlation results, select next factor")
    p_update.add_argument("--results", type=str, default=None,
                          help="Correlation results file (.xlsx or .json). Default: state/corr_result.xlsx")

    # status
    sub.add_parser("status", help="Show current state")

    # finalize
    sub.add_parser("finalize", help="Generate final output xlsx")

    # reset
    p_reset = sub.add_parser("reset", help="Clear state (corr matrix cache kept by default)")
    p_reset.add_argument("--clear-matrix", dest="keep_matrix", action="store_false",
                         default=True, help="Also clear the cached correlation matrix")

    # step (推荐主循环)
    p_step = sub.add_parser("step", help="Cache-driven main loop: ingest -> replay -> emit next task")
    p_step.add_argument("--ir-threshold", type=float, default=0.5)
    p_step.add_argument("--corr-threshold", type=float, default=0.35)

    # replay
    p_replay = sub.add_parser("replay", help="Replay greedy prune from cached corr matrix (no QuantAll call)")
    p_replay.add_argument("--ir-threshold", type=float, default=0.3)
    p_replay.add_argument("--corr-threshold", type=float, default=0.8)
    p_replay.add_argument("--save", action="store_true", help="Write output xlsx")

    # config
    p_config = sub.add_parser("config", help="View/modify config")
    p_config.add_argument("--ir-threshold", type=float, default=None)
    p_config.add_argument("--corr-threshold", type=float, default=None)

    # run (全自动：直连 QuantAll 跑完整个筛选循环)
    p_run = sub.add_parser("run", help="Full-auto: connect QuantAll and run whole prune loop")
    p_run.add_argument("--ir-threshold", type=float, default=0.5, help="|IR| threshold for valid factors (default: 0.5)")
    p_run.add_argument("--corr-threshold", type=float, default=0.35, help="|IC| threshold for redundant factors (default: 0.35)")
    p_run.add_argument("--mcp-url", type=str, default="http://127.0.0.1:8686/mcp", help="QuantAll MCP URL")
    p_run.add_argument("--timeout", type=int, default=3600, help="HTTP timeout seconds per batch_factor_corr call (default: 3600)")
    p_run.add_argument("--max-rounds", type=int, default=200, help="Safety cap on rounds (default: 200)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "finalize":
        cmd_finalize(args)
    elif args.command == "step":
        cmd_step(args)
    elif args.command == "replay":
        cmd_replay(args)
    elif args.command == "reset":
        cmd_reset(args)
    elif args.command == "config":
        cmd_config(args)
    elif args.command == "run":
        cmd_run(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
