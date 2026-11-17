#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
prune_flow.py —— 文件驱动的因子筛选流程（v2：coverage 感知 + 单文件预筛 + 聚合）
====================================================================================

设计目标：
  * 临时文件统一在 state/ 目录管理，尽量减少 AI 在筛选过程中的负担
  * 脚本直连 QuantAll（HTTP JSON-RPC），自己跑完整个循环，无需 AI 逐轮转发
  * 中间信息由脚本提供（status 命令），AI 只在需要时查看
  * 为因子数量持续扩展而设计：单文件先预筛，再聚合二次筛选

流程（v2 六步 ↔ 命令）：
  [0]   prescreen : 对 output/ 下「每个」xlsx 单独预筛（按阈值 + coverage 感知排序），
                    取每文件 top-N → state/prescreen/<source>.xlsx（可扩展：新家族只补预筛）
  [1-2] init      : 聚合所有 prescreen 文件 → 全局 coverage 感知排序（低覆盖置底）→
                    降序 → name 加 6 位编号 → 存 ls1.xlsx
  [3-5] run       : 循环：取 ls1 首行追加 ls_result → 生成 round_N.json(save_path=ls2.xlsx)
                    → QuantAll 执行 batch_factor_corr → 读 ls2 移除高相关 → 回写 ls1
                    直到选中数达到 --max-selected（默认 50）或 ls1 清空
  [6]   finalize  : 读 ls_result，去除 name 前 6 位编号 → 输出 scripts/factor-pure.xlsx

辅助命令：
  status : 查看当前 ls1 / ls_result / coverage 分布（AI 获取中间信息用）
  reset  : 清空 state 下所有临时文件（覆盖写，不删除）

coverage（有效数据比例）处理：
  * 优先读 xlsx 的 `coverage` 列（QuantAll 调整后新增），取值 0~1
  * 若该列缺失：用 start_date / end_date / stock_count 推算 proxy_coverage（明确标注来源=proxy），
    算法：proxy = clip( (因子活跃天数/全样本天数) * (stock_count/全市场股票数), 0, 1 )
    —— 停牌/上市晚/退市会缩短活跃天数、降低 stock_count，proxy 自然更低；财报类因 NaN 填充略高，符合预期
  * 排序：低覆盖因子（coverage < --coverage-floor）整体置底；其余按所选指标降序
    → 满足「top 和 bottom 的 coverage 偏低的置底；有效数据大的因子往前排」

文件布局（全部在 state/ 内）：
  state/prescreen/<source>.xlsx  单文件预筛结果（每文件 top-N）
  state/ls1.xlsx                 当前存活因子池（全局降序、name 带前缀）
  state/ls_result.xlsx           已选中因子累积表
  state/ls2.xlsx                 本轮相关性结果（每轮覆盖）
  state/round_NNN.json           本轮 batch_factor_corr 任务文件（含 save_path）
  state/flow_config.json         阈值 / 前缀长度 / coverage 来源等配置
  scripts/factor-pure.xlsx       最终输出（去前缀，含 coverage）

用法示例：
  python prune_flow.py prescreen --ir-threshold 0.3 --per-file 60
  python prune_flow.py init
  python prune_flow.py run --corr-threshold 0.5 --max-selected 50
  python prune_flow.py status
  python prune_flow.py finalize
  python prune_flow.py reset
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: pandas/numpy is required. Install: pip install pandas numpy openpyxl")
    sys.exit(1)


# ============================================================
# 路径常量（临时文件统一在 state/ 目录）
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(SCRIPT_DIR, "state")
PRESCREEN_DIR = os.path.join(STATE_DIR, "prescreen")
INPUT_DIR = os.path.join(SCRIPT_DIR, "output")      # 因子 xlsx 输入目录

LS1 = os.path.join(STATE_DIR, "ls1.xlsx")            # 当前存活池
LS_RESULT = os.path.join(STATE_DIR, "ls_result.xlsx")  # 已选累积
LS2 = os.path.join(STATE_DIR, "ls2.xlsx")            # 本轮相关性结果
CONFIG_FILE = os.path.join(STATE_DIR, "flow_config.json")
FINAL_FILE = os.path.join(SCRIPT_DIR, "factor-pure.xlsx")  # 最终输出

DEFAULT_IR = 0.3          # v2：初步筛选放宽，多保留候选
DEFAULT_CORR = 0.5        # v2：降低相关性要求（容忍更高相关 → 少移除）
DEFAULT_MAX_SELECTED = 50 # v2：最终输出控制在 50 个
DEFAULT_COV_FLOOR = 0.4   # 低于此 coverage 的因子置底
DEFAULT_PER_FILE = 60     # 单文件预筛保留 top-N
DEFAULT_AGG_KEEP = 200    # 聚合后保留 top-M 进入去相关（控制轮次上限）

UNIVERSE_REF = 5588       # 全市场股票数参考（用于 proxy 截面覆盖率）

# 持久化/传递的列
COLS = ["name", "orig_name", "code", "IR", "IC", "time_potential",
        "coverage", "coverage_source", "source_file", "abs_IR",
        "sort_metric", "feature_days"]


# ============================================================
# 输入读取 + coverage 解析
# ============================================================
def _fnum(v):
    try:
        return float(v) if pd.notna(v) else 0.0
    except (ValueError, TypeError):
        return 0.0


def _proxy_coverage(row, gmin, gmax):
    """coverage 缺失时用 活跃天数×截面占比 推算（0~1）"""
    try:
        sd = pd.to_datetime(row.get("start_date"), errors="coerce")
        ed = pd.to_datetime(row.get("end_date"), errors="coerce")
    except Exception:
        sd = ed = pd.NaT
    if pd.isna(sd) or pd.isna(ed) or pd.isna(gmin) or pd.isna(gmax) or gmax <= gmin:
        span_frac = 0.5
    else:
        span_frac = max(0.0, min(1.0, (ed - sd).days / max(1, (gmax - gmin).days)))
    sc = _fnum(row.get("stock_count"))
    cross_frac = max(0.0, min(1.0, sc / UNIVERSE_REF))
    return max(0.0, min(1.0, span_frac * cross_frac))


def records_from_dataframe(df, source_file, gmin, gmax):
    """从 xlsx DataFrame 解析出因子记录列表（含 coverage 解析）"""
    recs = []
    for _, row in df.iterrows():
        if "name" not in df.columns or "code" not in df.columns:
            continue
        cov_raw = row.get("coverage")
        if cov_raw is not None and pd.notna(cov_raw):
            coverage = _fnum(cov_raw)
            cov_src = "real"
        else:
            coverage = _proxy_coverage(row, gmin, gmax)
            cov_src = "proxy"
        ir = _fnum(row.get("IR"))
        recs.append({
            "name": str(row["name"]),
            "code": str(row["code"]),
            "IR": ir,
            "IC": _fnum(row.get("IC")),
            "time_potential": _fnum(row.get("time_potential")),
            "coverage": coverage,
            "coverage_source": cov_src,
            "source_file": source_file,
            "abs_IR": abs(ir),
            "feature_days": int(row["feature_days"]) if pd.notna(row.get("feature_days")) else 5,
        })
    return recs


def _global_date_bounds():
    """扫描 output/ 所有文件，得到全局最早 start / 最晚 end（供 proxy 用）"""
    gmin = gmax = pd.NaT
    for fname in sorted(os.listdir(INPUT_DIR)):
        if not fname.endswith(".xlsx"):
            continue
        if fname.startswith("pruned") or fname.startswith("factor-pure"):
            continue
        try:
            df = pd.read_excel(os.path.join(INPUT_DIR, fname),
                               usecols=["start_date", "end_date"])
            s = pd.to_datetime(df["start_date"], errors="coerce").min()
            e = pd.to_datetime(df["end_date"], errors="coerce").max()
            if pd.notna(s) and (pd.isna(gmin) or s < gmin):
                gmin = s
            if pd.notna(e) and (pd.isna(gmax) or e > gmax):
                gmax = e
        except Exception:
            pass
    return gmin, gmax


def load_all_factors():
    """读取 output/ 下所有因子 xlsx（排除已产出/中间文件），汇总为记录列表"""
    all_factors = []
    gmin, gmax = _global_date_bounds()
    xlsx_files = sorted([
        f for f in os.listdir(INPUT_DIR)
        if f.endswith(".xlsx")
        and not f.startswith("pruned")
        and not f.startswith("factor-pure")
    ])
    for fname in xlsx_files:
        fpath = os.path.join(INPUT_DIR, fname)
        try:
            df = pd.read_excel(fpath)
            if df.empty or "name" not in df.columns or "code" not in df.columns:
                continue
            all_factors.extend(records_from_dataframe(df, fname, gmin, gmax))
        except Exception as e:
            print(f"WARN: Failed to read {fname}: {e}", file=sys.stderr)
    return all_factors


# ============================================================
# 筛选 + coverage 感知排序
# ============================================================
def apply_filters(pool, ir_t, ic_t, tp_t, top_frac, metric):
    """按阈值过滤（AND）。top_frac 在已过滤集合上按 |IR| 取前 N%。"""
    applied = []
    if ir_t is not None:
        pool = [f for f in pool if f["abs_IR"] > ir_t]
        applied.append(f"|IR|>{ir_t}")
    if ic_t is not None:
        pool = [f for f in pool if abs(f["IC"]) > ic_t]
        applied.append(f"|IC|>{ic_t}")
    if tp_t is not None:
        pool = [f for f in pool if f["time_potential"] > tp_t]
        applied.append(f"time_potential>{tp_t}")
    if top_frac is not None:
        ps = sorted(pool, key=lambda x: x["abs_IR"], reverse=True)
        k = max(1, int(round(top_frac * len(ps))))
        pool = ps[:k]
        applied.append(f"top{top_frac * 100:.0f}%IR(k={k})")
    return pool, applied


def coverage_aware_sort(pool, metric, cov_floor):
    """coverage 感知排序：低覆盖置底；其余按 metric 降序。
    metric: 'abs_IR' | 'IC' | 'time_potential'
    """
    for f in pool:
        if metric == "IC":
            f["sort_metric"] = abs(f["IC"])
        elif metric == "time_potential":
            f["sort_metric"] = f["time_potential"]
        else:
            f["sort_metric"] = f["abs_IR"]
    # 排序键：先按是否低覆盖（False 在前），再按 sort_metric 降序
    pool.sort(key=lambda x: (x["coverage"] < cov_floor, -x["sort_metric"]))
    return pool


def _prefix_rows(pool, width):
    rows = []
    for i, f in enumerate(pool, start=1):
        r = dict(f)
        r["orig_name"] = f["name"]
        r["name"] = f"{i:0{width}d}-" + f["name"]
        rows.append(r)
    return rows


# ============================================================
# QuantAll MCP 直连（HTTP JSON-RPC，全自动模式脚本自己调用）
# ============================================================
class QuantAllClient:
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
                "clientInfo": {"name": "factor-prune-flow", "version": "2.0"},
            },
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"},
                   expect_response=False)
        return self.session_id

    def call_tool(self, name, arguments, retries=4):
        last_err = None
        for attempt in range(1, retries + 1):
            try:
                resp = self._post({
                    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
                })
                if resp is None:
                    raise RuntimeError("No response from QuantAll MCP")
                if "error" in resp:
                    raise RuntimeError(f"QuantAll error: {resp['error']}")
                return resp.get("result")
            except Exception as e:
                last_err = e
                if attempt < retries:
                    print(f"  [retry {attempt}/{retries}] QuantAll call failed: {e}; "
                          f"sleep 15s then retry", file=sys.stderr, flush=True)
                    time.sleep(15)
                else:
                    print(f"  [retry {attempt}/{retries}] QuantAll call failed: {e}",
                          file=sys.stderr, flush=True)
        raise RuntimeError(f"QuantAll call_tool failed after {retries} tries: {last_err}")


# ============================================================
# 状态读写
# ============================================================
def save_config(cfg):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ls1():
    if not os.path.exists(LS1):
        return pd.DataFrame(columns=COLS)
    return pd.read_excel(LS1)


def load_ls_result():
    if not os.path.exists(LS_RESULT):
        return pd.DataFrame(columns=COLS)
    return pd.read_excel(LS_RESULT)


def append_to_result(row):
    """把已选中因子（一行）追加到 ls_result 末尾；按 name 去重防止中断续跑重复"""
    res = load_ls_result()
    name = row["name"]
    if not res.empty and name in set(res["name"].tolist()):
        return  # 已存在，跳过（续跑保护）
    new_row = pd.DataFrame([{c: row[c] for c in COLS}])
    out = pd.concat([res, new_row], ignore_index=True)
    out.to_excel(LS_RESULT, index=False)


# ============================================================
# 命令实现
# ============================================================
def cmd_prescreen(args):
    """步骤 0：对 output/ 下「每个」xlsx 单独预筛（支持因子家族持续扩展）"""
    os.makedirs(PRESCREEN_DIR, exist_ok=True)
    gmin, gmax = _global_date_bounds()
    per_file = args.per_file
    cov_floor = args.coverage_floor
    metric = args.metric

    # 解析全局筛选阈值（prescreen 用宽松口径，保留更多）
    ir_t = args.ir_threshold if args.ir_threshold is not None else None
    ic_t = args.ic_threshold
    tp_t = args.time_potential_threshold
    top_frac = args.top_ir_frac

    files = sorted([
        f for f in os.listdir(INPUT_DIR)
        if f.endswith(".xlsx")
        and not f.startswith("pruned")
        and not f.startswith("factor-pure")
    ])
    summary = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        try:
            df = pd.read_excel(fpath)
        except Exception as e:
            print(f"WARN skip {fname}: {e}", file=sys.stderr)
            continue
        if df.empty or "name" not in df.columns or "code" not in df.columns:
            continue
        recs = records_from_dataframe(df, fname, gmin, gmax)
        pool, applied = apply_filters(recs, ir_t, ic_t, tp_t, top_frac, metric)
        pool = coverage_aware_sort(pool, metric, cov_floor)
        pool = pool[:per_file]
        width = max(5, len(str(len(pool))))
        rows = _prefix_rows(pool, width)
        out_df = pd.DataFrame(rows)[COLS]
        out_path = os.path.join(PRESCREEN_DIR, fname)
        out_df.to_excel(out_path, index=False)
        n_low = sum(1 for f in pool if f["coverage"] < cov_floor)
        summary.append({
            "source": fname, "total": len(recs), "kept": len(pool),
            "low_cov_demoted": n_low, "filters": applied,
            "coverage_source": pool[0]["coverage_source"] if pool else "n/a",
        })
        print(json.dumps({"prescreen": fname, "kept": len(pool),
                          "low_cov_demoted": n_low}, ensure_ascii=False))

    save_config(load_config() | {
        "prescreen_per_file": per_file,
        "coverage_floor": cov_floor,
        "metric": metric,
        "prescreen_filters": {
            "ir_threshold": ir_t, "ic_threshold": ic_t,
            "time_potential_threshold": tp_t, "top_ir_frac": top_frac,
        },
        "prescreen_time": datetime.now().isoformat(timespec="seconds"),
    })
    print(json.dumps({
        "step": "prescreen",
        "files": len(summary),
        "per_file": per_file,
        "metric": metric,
        "coverage_floor": cov_floor,
        "summary": summary,
    }, ensure_ascii=False, indent=2))


def cmd_init(args):
    """步骤 1-2：聚合所有 prescreen 文件 → 全局 coverage 感知排序 → 加编号 → ls1.xlsx
    若没有 prescreen 目录（未运行 prescreen），则直接读 output/ 聚合，等价于旧 init。
    """
    os.makedirs(STATE_DIR, exist_ok=True)
    cfg = load_config()
    cov_floor = args.coverage_floor if args.coverage_floor is not None \
        else cfg.get("coverage_floor", DEFAULT_COV_FLOOR)
    metric = args.metric if args.metric is not None else cfg.get("metric", "abs_IR")
    agg_keep = args.aggregate_keep

    # 来源：优先 prescreen 目录
    pool = []
    if os.path.isdir(PRESCREEN_DIR) and any(f.endswith(".xlsx")
                                            for f in os.listdir(PRESCREEN_DIR)):
        src_dir, src_label = PRESCREEN_DIR, "prescreen"
        gmin = gmax = pd.NaT
    else:
        src_dir, src_label = INPUT_DIR, "output"
        gmin, gmax = _global_date_bounds()

    files = sorted([f for f in os.listdir(src_dir)
                    if f.endswith(".xlsx")
                    and not f.startswith("pruned")
                    and not f.startswith("factor-pure")])
    for fname in files:
        fpath = os.path.join(src_dir, fname)
        df = pd.read_excel(fpath)
        if df.empty or "name" not in df.columns or "code" not in df.columns:
            continue
        if src_label == "prescreen":
            # prescreen 已含 coverage，直接读（不重算）
            for _, row in df.iterrows():
                pool.append({
                    "name": str(row["name"]),
                    "code": str(row["code"]),
                    "IR": _fnum(row.get("IR")),
                    "IC": _fnum(row.get("IC")),
                    "time_potential": _fnum(row.get("time_potential")),
                    "coverage": _fnum(row.get("coverage")),
                    "coverage_source": str(row.get("coverage_source", "real")),
                    "source_file": str(row.get("source_file", fname)),
                    "abs_IR": _fnum(row.get("abs_IR")),
                    "feature_days": int(row["feature_days"]) if pd.notna(row.get("feature_days")) else 5,
                })
        else:
            pool.extend(records_from_dataframe(df, fname, gmin, gmax))

    # 全局可再施加一次阈值（可选）
    ir_t = args.ir_threshold
    ic_t = args.ic_threshold
    tp_t = args.time_potential_threshold
    top_frac = args.top_ir_frac
    applied = []
    if ir_t is not None:
        pool = [f for f in pool if f["abs_IR"] > ir_t]; applied.append(f"|IR|>{ir_t}")
    if ic_t is not None:
        pool = [f for f in pool if abs(f["IC"]) > ic_t]; applied.append(f"|IC|>{ic_t}")
    if tp_t is not None:
        pool = [f for f in pool if f["time_potential"] > tp_t]; applied.append(f"tp>{tp_t}")
    if top_frac is not None:
        ps = sorted(pool, key=lambda x: x["abs_IR"], reverse=True)
        k = max(1, int(round(top_frac * len(ps))))
        pool = ps[:k]; applied.append(f"top{top_frac*100:.0f}%IR(k={k})")

    pool = coverage_aware_sort(pool, metric, cov_floor)
    # 聚合后保留 top-M（控制去相关轮次上限，但最终不超过 max_selected）
    if agg_keep is not None and len(pool) > agg_keep:
        pool = pool[:agg_keep]

    width = max(5, len(str(len(pool))))
    rows = _prefix_rows(pool, width)
    df = pd.DataFrame(rows)[COLS]
    df.to_excel(LS1, index=False)
    pd.DataFrame(columns=COLS).to_excel(LS_RESULT, index=False)

    n_low = sum(1 for f in pool if f["coverage"] < cov_floor)
    covs = [f["coverage"] for f in pool]
    save_config(cfg | {
        "ir_threshold": ir_t, "ic_threshold": ic_t,
        "time_potential_threshold": tp_t, "top_ir_frac": top_frac,
        "filters_applied": applied,
        "coverage_floor": cov_floor, "metric": metric,
        "corr_threshold": args.corr_threshold if args.corr_threshold is not None
        else cfg.get("corr_threshold", DEFAULT_CORR),
        "max_selected": args.max_selected if args.max_selected is not None
        else cfg.get("max_selected", DEFAULT_MAX_SELECTED),
        "prefix_len": width + 1,
        "valid_count": len(pool),
        "low_cov_demoted": n_low,
        "coverage_source": pool[0]["coverage_source"] if pool else "n/a",
        "init_time": datetime.now().isoformat(timespec="seconds"),
    })
    print(json.dumps({
        "step": "init",
        "source": src_label,
        "pool_size": len(pool),
        "low_cov_demoted": n_low,
        "coverage_min": round(min(covs), 3) if covs else None,
        "coverage_median": round(float(np.median(covs)), 3) if covs else None,
        "coverage_max": round(max(covs), 3) if covs else None,
        "coverage_source": pool[0]["coverage_source"] if pool else "n/a",
        "filters_applied": applied,
        "ls1": LS1,
    }, ensure_ascii=False, indent=2))


def cmd_run(args):
    """步骤 3-5：循环直到选中数达 max_selected 或 ls1 清空；结束后自动 finalize（步骤 6）"""
    cfg = load_config()
    corr_threshold = args.corr_threshold if args.corr_threshold is not None \
        else cfg.get("corr_threshold", DEFAULT_CORR)
    max_selected = args.max_selected if args.max_selected is not None \
        else cfg.get("max_selected", DEFAULT_MAX_SELECTED)
    prefix_len = cfg.get("prefix_len", 6)

    client = QuantAllClient(url=args.mcp_url, timeout=args.timeout)
    try:
        sid = client.connect()
        print(f"[connect] QuantAll session {sid}", flush=True)
    except Exception as e:
        print(json.dumps({"error": f"Cannot connect QuantAll at {args.mcp_url}: {e}"},
                         ensure_ascii=False))
        return

    started = datetime.now()
    round_no = 0
    while True:
        ls1 = load_ls1()
        if ls1.empty:
            break
        round_no += 1
        benchmark = ls1.iloc[0]

        # 步骤 3：首行追加到 ls_result（末尾）
        append_to_result(benchmark)

        # 达到目标选中数 → 结束并 finalize
        if len(load_ls_result()) >= max_selected:
            pd.DataFrame(columns=COLS).to_excel(LS1, index=False)
            print(f"[round {round_no}] reached max_selected={max_selected}; stop",
                  flush=True)
            break

        remainder = ls1.iloc[1:].reset_index(drop=True)

        # ---- IC 邻近窗口优化（可选）：只与 benchmark IC 邻近的候选算相关 ----
        # 高 IC 与低 IC 因子高相关在理论上近乎不可能（高相关 ⇒ 两者 |IC| 量级接近），
        # 故可跳过 IC 远低于 benchmark 的尾部，显著减少 QuantAll 调用。默认关闭（None=全量）。
        win_desc = "full"
        if args.window is not None and args.window > 0:
            remainder = remainder.iloc[:args.window].reset_index(drop=True)
            win_desc = f"top{args.window}"
        elif args.window_ratio is not None and args.window_ratio > 0:
            b_ic = abs(float(benchmark["IC"])) if pd.notna(benchmark.get("IC")) else 0.0
            if b_ic > 0:
                thr = args.window_ratio * b_ic
                remainder = remainder[remainder["IC"].abs() >= thr].reset_index(drop=True)
                win_desc = f"IC>={args.window_ratio:.2f}*bench"

        if remainder.empty:
            pd.DataFrame(columns=COLS).to_excel(LS1, index=False)
            print(f"[round {round_no}] last factor {benchmark['orig_name']} selected; ls1 cleared",
                  flush=True)
            break

        # 步骤 3：生成 round_N.json（含 save_path=ls2.xlsx）
        factor_dict = {row["name"]: row["code"] for _, row in remainder.iterrows()}
        task = {
            "tool_name": "batch_factor_corr",
            "benchmark_name": benchmark["name"],
            "benchmark_code": benchmark["code"],
            "factor_dict": factor_dict,
            "save_path": LS2,
        }
        round_json = os.path.join(STATE_DIR, f"round_{round_no:03d}.json")
        with open(round_json, "w", encoding="utf-8") as f:
            json.dump(task, f, ensure_ascii=False, indent=2)

        # 步骤 4：QuantAll 执行 json
        t0 = datetime.now()
        try:
            client.call_tool("batch_factor_corr", task)
        except Exception as e:
            print(json.dumps({"error": f"round {round_no} failed: {e}"}, ensure_ascii=False))
            return
        dt = (datetime.now() - t0).total_seconds()

        # 步骤 4：脚本加载 ls2 与 ls1，提取高相关清单，从 ls1 去除
        res = pd.read_excel(LS2)
        ic_col = "IC" if "IC" in res.columns else ("ic" if "ic" in res.columns else None)
        if ic_col is None:
            print(json.dumps({"error": f"ls2 has no IC column; cols={list(res.columns)}"},
                             ensure_ascii=False))
            return
        over = set(res.loc[res[ic_col].abs() > corr_threshold, "name"].tolist())
        kept = remainder[~remainder["name"].isin(over)].reset_index(drop=True)
        kept.to_excel(LS1, index=False)

        print(json.dumps({
            "round": round_no,
            "benchmark": benchmark["orig_name"],
            "benchmark_IR": round(benchmark["IR"], 4),
            "candidates": int(len(remainder)),
            "window": win_desc,
            "removed": int(len(over)),
            "ls1_left": int(len(kept)),
            "secs": round(dt, 1),
        }, ensure_ascii=False), flush=True)

    print(f"[done] {round_no} rounds, "
          f"elapsed {(datetime.now() - started).total_seconds():.0f}s", flush=True)
    cmd_finalize(args)


def cmd_finalize(args):
    """步骤 6：读 ls_result，去除 name 前 prefix_len 位编号 → factor-pure.xlsx（保留 coverage）"""
    cfg = load_config()
    prefix_len = cfg.get("prefix_len", 6)
    res = load_ls_result()
    if res.empty:
        print(json.dumps({"error": "ls_result is empty; run init+run first"}, ensure_ascii=False))
        return
    out = res.copy()
    out["name"] = out["name"].str.slice(start=prefix_len)
    if "orig_name" in out.columns:
        mask = (out["name"].str.len() == 0) | (out["name"] != out["orig_name"])
        out.loc[mask, "name"] = out.loc[mask, "orig_name"]
    out_cols = ["name", "code", "IR", "IC", "time_potential", "coverage",
                "source_file", "abs_IR"]
    out = out[out_cols]
    out.to_excel(FINAL_FILE, index=False)
    print(json.dumps({
        "step": "finalize",
        "selected": int(len(out)),
        "output": FINAL_FILE,
    }, ensure_ascii=False, indent=2))


def cmd_status(args):
    """查看中间状态（AI 获取信息用）"""
    ls1 = load_ls1()
    res = load_ls_result()
    cfg = load_config()
    info = {"step": "status", "config": cfg,
            "ls1_count": int(len(ls1)), "ls_result_count": int(len(res))}
    if not ls1.empty and "coverage" in ls1.columns:
        covs = ls1["coverage"].astype(float)
        info["coverage"] = {
            "min": round(float(covs.min()), 3),
            "median": round(float(covs.median()), 3),
            "max": round(float(covs.max()), 3),
            "source": cfg.get("coverage_source", "n/a"),
            "low_cov_demoted": int((covs < cfg.get("coverage_floor", DEFAULT_COV_FLOOR)).sum()),
        }
        info["ls1_top3"] = [{"name": r["orig_name"], "IR": round(r["IR"], 4),
                             "coverage": round(r["coverage"], 3)}
                            for _, r in ls1.head(3).iterrows()]
    if not res.empty:
        info["selected_top3"] = [{"name": r["orig_name"], "IR": round(r["IR"], 4)}
                                 for _, r in res.head(3).iterrows()]
    print(json.dumps(info, ensure_ascii=False, indent=2))


def cmd_reset(args):
    """清空 state 下所有临时文件（覆盖写，不删除，兼容沙箱 safe-delete）"""
    os.makedirs(STATE_DIR, exist_ok=True)
    pd.DataFrame(columns=COLS).to_excel(LS1, index=False)
    pd.DataFrame(columns=COLS).to_excel(LS_RESULT, index=False)
    save_config({})
    print(json.dumps({"step": "reset", "state": STATE_DIR}, ensure_ascii=False))


# ============================================================
# CLI
# ============================================================
def main():
    p = argparse.ArgumentParser(description="文件驱动因子筛选流程 v2（coverage 感知 + 单文件预筛）")
    sub = p.add_subparsers(dest="command")

    p_pre = sub.add_parser("prescreen", help="步骤0: 对单 xlsx 预筛→state/prescreen/<src>.xlsx")
    p_pre.add_argument("--ir-threshold", type=float, default=None,
                       help="保留 |IR| > 此值 (默认不卡；聚合时再统一卡)")
    p_pre.add_argument("--ic-threshold", type=float, default=None)
    p_pre.add_argument("--time-potential-threshold", type=float, default=None)
    p_pre.add_argument("--top-ir-frac", type=float, default=None)
    p_pre.add_argument("--per-file", type=int, default=DEFAULT_PER_FILE,
                       help="每文件保留 top-N（控制聚合规模，支持家族扩展）")
    p_pre.add_argument("--coverage-floor", type=float, default=DEFAULT_COV_FLOOR)
    p_pre.add_argument("--metric", choices=["abs_IR", "IC", "time_potential"],
                       default="abs_IR", help="排序指标（coverage 低于 floor 者仍置底）")

    p_init = sub.add_parser("init", help="步骤1-2: 聚合 prescreen→全局排序→加编号→ls1.xlsx")
    p_init.add_argument("--ir-threshold", type=float, default=None)
    p_init.add_argument("--ic-threshold", type=float, default=None)
    p_init.add_argument("--time-potential-threshold", type=float, default=None)
    p_init.add_argument("--top-ir-frac", type=float, default=None)
    p_init.add_argument("--aggregate-keep", type=int, default=DEFAULT_AGG_KEEP,
                        help="聚合后保留 top-M 进入去相关（控制轮次上限）")
    p_init.add_argument("--coverage-floor", type=float, default=None)
    p_init.add_argument("--metric", choices=["abs_IR", "IC", "time_potential"], default=None)
    p_init.add_argument("--corr-threshold", type=float, default=None)
    p_init.add_argument("--max-selected", type=int, default=None)

    p_run = sub.add_parser("run", help="步骤3-5: 循环去相关直到选中达 max-selected，自动finalize")
    p_run.add_argument("--corr-threshold", type=float, default=None,
                      help="冗余阈值 |IC|；默认 0.5（降低相关性要求）")
    p_run.add_argument("--max-selected", type=int, default=None,
                      help="最终选中上限（默认 50）")
    p_run.add_argument("--mcp-url", default="http://127.0.0.1:8686/mcp")
    p_run.add_argument("--timeout", type=int, default=3600)
    p_run.add_argument("--max-rounds", type=int, default=100000)
    p_run.add_argument("--window", type=int, default=None,
                       help="IC 邻近窗口：benchmark 只与下方前 N 个高 IC 候选算相关（跳过低 IC 尾部）")
    p_run.add_argument("--window-ratio", type=float, default=None, dest="window_ratio",
                       help="IC 邻近窗口（比例）：只与 |IC|>=ratio*|IC(benchmark)| 的候选算相关")

    p_stat = sub.add_parser("status", help="查看中间状态（含 coverage 分布）")
    p_fin = sub.add_parser("finalize", help="步骤6: 去前缀→factor-pure.xlsx")
    p_reset = sub.add_parser("reset", help="清空 state 临时文件")

    args = p.parse_args()
    if args.command == "prescreen":
        cmd_prescreen(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "finalize":
        cmd_finalize(args)
    elif args.command == "reset":
        cmd_reset(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
