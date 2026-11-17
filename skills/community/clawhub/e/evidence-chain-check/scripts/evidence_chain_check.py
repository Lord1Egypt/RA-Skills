#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""evidence-chain-check — 法律证据链完整性校验纵深工具（零依赖）。
校验证据链: 时间单调 / 主体一致 / 哈希链不断(prev==上一项hash)。
理论真源：LGD 凡自治之物三律（SynomosAI）。"""
import argparse, json, sys
NAME = "evidence-chain-check"
def check(chain):
    breaks = []
    subjects = set()
    prev_hash = None
    last_t = None
    for i, e in enumerate(chain):
        subj = e.get("subject")
        if subj: subjects.add(subj)
        t = e.get("time")
        if last_t is not None and t is not None and t < last_t:
            breaks.append("时间倒序 @" + str(i))
        last_t = t
        h = e.get("hash")
        if prev_hash is not None and e.get("prev") != prev_hash:
            breaks.append("哈希链断裂 @" + str(i))
        prev_hash = h
    if len(subjects) > 1:
        breaks.append("主体不一致:" + "/".join(sorted(subjects)))
    return {"breaks": breaks, "complete": len(breaks) == 0, "subjects": sorted(subjects)}
def main():
    ap = argparse.ArgumentParser(description=NAME + " · 证据链校验")
    ap.add_argument("--chain", help="证据列表 JSON: [{id,time,subject,hash,prev}]")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.chain: print("用法: --chain <JSON>", file=sys.stderr); sys.exit(2)
    try: chain = json.loads(a.chain)
    except Exception as e: print("chain JSON 解析失败: " + str(e), file=sys.stderr); sys.exit(2)
    r = check(chain)
    if a.json: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 证据链校验 ===")
        print("  断裂点: " + (",".join(r["breaks"]) or "无"))
        print("  结论: " + ("链完整 ✅" if r["complete"] else "链断裂 ⛔"))
    sys.exit(0 if r["complete"] else 1)
if __name__ == "__main__":
    main()
