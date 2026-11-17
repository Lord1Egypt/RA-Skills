#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
window_prune.py —— 以 top10%/bottom10% 分位窗口为优化对象的去相关筛选
================================================================================
在 window_opt.py 的离线「分侧有效率门限 + 联合评分」基础上, 接上 QuantAll 逐对去相关:
  * 排序指标 score = |top10%_IR_eff| + |bottom10%_IR_eff| (放弃侧已置 0)
  * 每轮取 score 最高的因子作 benchmark, 用 batch_factor_corr 与其余候选算"因子值"相关
  * 移除 |corr| > corr_threshold 的候选, 直到选中数达 max_selected 或池清空
  * 输出 scripts/factor-pure-topbottom.xlsx (不覆盖 factor-pure.xlsx / factor-window-opt.xlsx)

分侧门限: 某侧 coverage < 0.07 -> 该侧有效性置 0 (放弃该侧), 但整行保留不删;
          只有两侧都 <0.07 才整因子无贡献, 自然排在池尾、进不了入选区。
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
    print("ERROR: pandas/numpy required"); sys.exit(1)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(SCRIPT_DIR, "state")
INPUT_DIR = os.path.join(SCRIPT_DIR, "output")
WIN_LS1 = os.path.join(STATE_DIR, "win_ls1.xlsx")
WIN_RESULT = os.path.join(STATE_DIR, "win_result.xlsx")
WIN_LS2 = os.path.join(STATE_DIR, "win_ls2.xlsx")
FINAL_FILE = os.path.join(SCRIPT_DIR, "factor-pure-topbottom.xlsx")

COV_FLOOR = 0.07  # 分侧有效率门限


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
                except Exception:
                    continue
                if "result" in obj or "error" in obj:
                    return obj
        return None

    def connect(self):
        self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "win-prune", "version": "1.0"}},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"},
                   expect_response=False)
        return self.session_id

    def call_tool(self, name, arguments, retries=8):
        last = None
        for attempt in range(1, retries + 1):
            try:
                resp = self._post({
                    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
                })
                if resp is None:
                    raise RuntimeError("no resp")
                if "error" in resp:
                    raise RuntimeError(f"QuantAll error: {resp['error']}")
                result = resp.get("result")
                # 识别 "有其它任务在执行" / result="失败" 这类"软失败", 触发重试
                busy = False
                try:
                    if isinstance(result, dict):
                        if result.get("result") == "失败" or "有其它任务" in str(result.get("message", "")):
                            busy = True
                        rtxt = json.dumps(result, ensure_ascii=False)
                    else:
                        rtxt = str(result)
                    if "有其它任务" in rtxt or '"result": "失败"' in rtxt:
                        busy = True
                except Exception:
                    pass
                if busy:
                    raise RuntimeError(f"QuantAll busy/失败 (attempt {attempt})")
                return result
            except Exception as e:
                last = e
                if attempt < retries:
                    print(f"  [retry {attempt}/{retries}] {e}; sleep 20s",
                          file=sys.stderr, flush=True)
                    time.sleep(20)
                else:
                    print(f"  [retry {attempt}/{retries}] {e}", file=sys.stderr, flush=True)
        raise RuntimeError(f"call_tool failed: {last}")


def _fnum(v):
    try:
        return float(v) if pd.notna(v) else 0.0
    except Exception:
        return 0.0


def load_factors():
    recs = []
    for fname in sorted(os.listdir(INPUT_DIR)):
        if not fname.endswith(".xlsx"):
            continue
        if fname.startswith(("pruned", "factor-pure", "factor-window")):
            continue
        fpath = os.path.join(INPUT_DIR, fname)
        df = pd.read_excel(fpath)
        if df.empty or "name" not in df.columns or "code" not in df.columns:
            continue
        src = fname.replace("factor-", "").replace("facotr-", "").replace(".xlsx", "")
        for _, r in df.iterrows():
            top_cov = _fnum(r.get("top10%_coverage"))
            bot_cov = _fnum(r.get("bottom10%_coverage"))
            top_ir = _fnum(r.get("top10%_IR"))
            bot_ir = _fnum(r.get("bottom10%_IR"))
            top_keep = 1 if top_cov >= COV_FLOOR else 0
            bot_keep = 1 if bot_cov >= COV_FLOOR else 0
            top_ir_eff = top_ir if top_keep else 0.0
            bot_ir_eff = bot_ir if bot_keep else 0.0
            score = abs(top_ir_eff) + abs(bot_ir_eff)
            recs.append({
                "name": str(r["name"]), "code": str(r["code"]), "source": src,
                "feature_days": int(r["feature_days"]) if pd.notna(r.get("feature_days")) else 5,
                "top_IR": top_ir, "top_IR_eff": top_ir_eff,
                "top_cov": top_cov, "top_keep": top_keep,
                "bot_IR": bot_ir, "bot_IR_eff": bot_ir_eff,
                "bot_cov": bot_cov, "bot_keep": bot_keep,
                "score": score,
                "IR": _fnum(r.get("IR")), "IC": _fnum(r.get("IC")),
                "coverage": _fnum(r.get("coverage")),
                "time_potential": _fnum(r.get("time_potential")),
            })
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", type=int, default=120,
                    help="进入去相关的候选数(按 score 取前 N)")
    ap.add_argument("--corr-threshold", type=float, default=0.5)
    ap.add_argument("--max-selected", type=int, default=50)
    ap.add_argument("--mcp-url", default="http://127.0.0.1:8686/mcp")
    ap.add_argument("--timeout", type=int, default=3600)
    args = ap.parse_args()

    recs = load_factors()
    # 至少保留一侧(两侧都<0.07 的整因子无贡献, 直接排除出池)
    recs = [r for r in recs if r["top_keep"] + r["bot_keep"] >= 1]
    recs.sort(key=lambda x: -x["score"])
    pool = recs[:args.pool]
    pool_df = pd.DataFrame(pool)
    os.makedirs(STATE_DIR, exist_ok=True)
    pool_df.to_excel(WIN_LS1, index=False)
    pd.DataFrame(columns=pool_df.columns).to_excel(WIN_RESULT, index=False)
    print(json.dumps({
        "step": "init", "pool_size": len(pool),
        "score_min": round(pool[-1]["score"], 4) if pool else None,
        "cov_floor": COV_FLOOR,
        "corr_threshold": args.corr_threshold, "max_selected": args.max_selected,
    }, ensure_ascii=False))

    client = QuantAllClient(url=args.mcp_url, timeout=args.timeout)
    try:
        sid = client.connect()
        print(f"[connect] {sid}", flush=True)
    except Exception as e:
        print(json.dumps({"error": f"connect fail: {e}"}, ensure_ascii=False))
        return

    started = datetime.now()
    round_no = 0
    while True:
        ls1 = pd.read_excel(WIN_LS1)
        if ls1.empty:
            break
        round_no += 1
        bench = ls1.iloc[0]

        # 选中 benchmark, 追加到结果
        res = pd.read_excel(WIN_RESULT)
        res = pd.concat([res, bench.to_frame().T], ignore_index=True)
        res.to_excel(WIN_RESULT, index=False)

        if len(res) >= args.max_selected:
            pd.DataFrame(columns=ls1.columns).to_excel(WIN_LS1, index=False)
            print(f"[round {round_no}] reached max_selected={args.max_selected}; stop",
                  flush=True)
            break

        remainder = ls1.iloc[1:].reset_index(drop=True)
        if remainder.empty:
            pd.DataFrame(columns=ls1.columns).to_excel(WIN_LS1, index=False)
            print(f"[round {round_no}] last factor {bench['name']} selected; clear",
                  flush=True)
            break

        factor_dict = {row["name"]: row["code"] for _, row in remainder.iterrows()}
        task = {
            "tool_name": "batch_factor_corr",
            "benchmark_name": bench["name"],
            "benchmark_code": bench["code"],
            "factor_dict": factor_dict,
            "save_path": WIN_LS2,
        }
        t0 = datetime.now()
        try:
            client.call_tool("batch_factor_corr", task)
        except Exception as e:
            print(json.dumps({"error": f"round {round_no} fail: {e}"}, ensure_ascii=False))
            return
        dt = (datetime.now() - t0).total_seconds()

        r2 = pd.read_excel(WIN_LS2)
        ic_col = "IC" if "IC" in r2.columns else ("ic" if "ic" in r2.columns else None)
        if ic_col is None:
            print(json.dumps({"error": f"ls2 no IC; cols={list(r2.columns)}"},
                             ensure_ascii=False))
            return
        over = set(r2.loc[r2[ic_col].abs() > args.corr_threshold, "name"].tolist())
        kept = remainder[~remainder["name"].isin(over)].reset_index(drop=True)
        kept.to_excel(WIN_LS1, index=False)
        print(json.dumps({
            "round": round_no, "bench": bench["name"],
            "bench_score": round(bench["score"], 4),
            "candidates": int(len(remainder)), "removed": int(len(over)),
            "ls1_left": int(len(kept)), "secs": round(dt, 1),
        }, ensure_ascii=False), flush=True)

    print(f"[done] {round_no} rounds, elapsed "
          f"{(datetime.now() - started).total_seconds():.0f}s", flush=True)

    # finalize
    res = pd.read_excel(WIN_RESULT)
    cols = ["name", "code", "source", "feature_days", "score",
            "top_IR", "top_keep", "top_cov", "bot_IR", "bot_keep", "bot_cov",
            "IR", "IC", "coverage", "time_potential"]
    out = res[[c for c in cols if c in res.columns]].copy()
    out.to_excel(FINAL_FILE, index=False)
    print(json.dumps({"step": "finalize", "selected": int(len(out)),
                      "output": FINAL_FILE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
