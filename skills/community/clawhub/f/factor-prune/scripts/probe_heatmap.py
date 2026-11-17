#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe2: 用精确因子代码跑管道，dump 完整 heat_map / move 结果看矩阵字段。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prune_flow import QuantAllClient
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(SCRIPT_DIR, "state")

df = pd.read_excel(os.path.join(SCRIPT_DIR, "factor-pure.xlsx"))
FACTOR0 = str(df.iloc[0]["code"]).strip()
print("FACTOR0 len:", len(FACTOR0))

RET5 = "out = (d['close']*d['adj_factor']).shift(-5)/(d['close']*d['adj_factor']) - 1"


def text_of(res):
    try:
        return res["content"][0]["text"]
    except Exception:
        return str(res)


def main():
    client = QuantAllClient(timeout=3600)
    client.connect()

    client.call_tool("new_layer_from_code", {"name": "probe", "code": "out = d['close'] > 0"})
    mx = client.call_tool("move_by_code",
                          {"code": FACTOR0, "name": "factor", "direction": "x",
                           "to_percentile": True})
    my = client.call_tool("move_by_code",
                          {"code": RET5, "name": "5日收益", "direction": "y",
                           "to_percentile": True})
    w = client.call_tool("weight_by_code",
                         {"code": RET5, "name": "5日收益", "to_percentile": False})
    hm = client.call_tool("heat_map", {"mode": "auto"})

    out = {
        "move_x": json.loads(text_of(mx))["result"],
        "move_y": json.loads(text_of(my))["result"],
        "weight": json.loads(text_of(w))["result"],
        "heat_map": json.loads(text_of(hm))["result"],
    }
    with open(os.path.join(STATE, "probe_full.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    # 打印关键字段
    h = out["heat_map"]
    print("heat_map keys:", list(h.keys()))
    for key in h.keys():
        v = h[key]
        if isinstance(v, list) and v and isinstance(v[0], list):
            print(f"  {key}: matrix {len(v)}x{len(v[0])}")
        else:
            print(f"  {key}: {str(v)[:120]}")
    print("move_x keys:", list(out["move_x"].keys()))
    print("move_x summary:", out["move_x"].get("summary"))
    print("move_x X轴统计:", out["move_x"].get("X轴统计"))


if __name__ == "__main__":
    main()
