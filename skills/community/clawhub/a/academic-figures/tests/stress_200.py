#!/usr/bin/env python3
"""A3(v2.7): 200 图连跑压测（发布电池用；不进默认测试套件）。
用法: python3 tests/stress_200.py   （约 5-8 分钟，全部成功输出 ALL 200 OK）"""
import json
import os
import random
import subprocess
import sys
import tempfile
import time

GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "gen_figure.py")
TYPES = ["bar", "grouped_bar", "hbar", "stacked_bar", "line", "scatter", "box", "violin",
         "heatmap", "forest", "roc", "pca", "cluster_heatmap", "bland_altman", "funnel"]


def make(t, rng):
    if t in ("bar", "grouped_bar", "hbar", "stacked_bar"):
        return {"labels": [f"g{j}" for j in range(6)],
                "series": {f"s{k}": [rng.random() * 5 for _ in range(6)] for k in range(3)}}
    if t == "line":
        return {"x": list(range(40)), "series": {f"a{k}": [rng.random() for _ in range(40)]
                                                for k in range(2)}}
    if t == "scatter":
        return {"x": [rng.random() for _ in range(120)],
                "y": [rng.random() for _ in range(120)]}
    if t in ("box", "violin"):
        return {"labels": ["A", "B", "C"],
                "series": {g: [rng.gauss(0, 1) for _ in range(25)] for g in "ABC"}}
    if t in ("heatmap", "cluster_heatmap"):
        return {"matrix": [[rng.random() for _ in range(10)] for _ in range(14)],
                "rows": [f"r{j}" for j in range(14)], "cols": [f"c{j}" for j in range(10)]}
    if t == "forest":
        n = 7
        es = [1 + rng.uniform(-.4, .4) for _ in range(n)]
        return {"labels": [f"study{j}" for j in range(n)], "estimates": es,
                "ci_low": [v - rng.random() * .3 for v in es],
                "ci_high": [v + rng.random() * .3 for v in es], "measure": "RR"}
    if t == "roc":
        return {"curves": [{"name": f"m{k}", "fpr": [0, .3, .6, 1], "tpr": [0, .6+k*.1, .85+k*.05, 1]}
                           for k in range(2)]}
    if t == "pca":
        return {"matrix": [[rng.gauss(0, 1) for _ in range(6)] for _ in range(20)]}
    if t == "bland_altman":
        a = [rng.gauss(100, 5) for _ in range(30)]
        return {"a": a, "b": [v + rng.gauss(0, 2) for v in a]}
    if t == "funnel":
        return {"effects": [rng.gauss(-.7, .2) for _ in range(10)],
                "ses": [rng.uniform(.05, .2) for _ in range(10)]}
    raise ValueError(t)


def main():
    rng = random.Random(2027)
    fails = []
    t0 = time.time()
    with tempfile.TemporaryDirectory() as td:
        for i in range(200):
            t = TYPES[i % len(TYPES)]
            p = os.path.join(td, f"d{i}.json")
            json.dump(make(t, rng), open(p, "w", encoding="utf-8"), ensure_ascii=False)
            r = subprocess.run([sys.executable, GEN, "-t", t, "--data", p,
                                "-o", os.path.join(td, f"o{i}"), "--dpi", "70"],
                               capture_output=True, text=True, timeout=180)
            if r.returncode != 0:
                fails.append((i, t, r.stderr[-200:]))
                print(f"FAIL #{i} {t}: {r.stderr[-150:]}")
            if (i + 1) % 50 == 0:
                print(f"  ... {i + 1}/200 ({time.time() - t0:.0f}s)")
    if fails:
        print(f"FAILED {len(fails)}/200")
        sys.exit(1)
    print(f"ALL 200 OK ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
