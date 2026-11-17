# -*- coding: utf-8 -*-
"""失控循环护栏：读动作轨迹，监测 步数超限/重复动作/无进展，给熔断建议+诊断。零依赖。"""
import argparse, json, pathlib, re

def parse_trace(p):
    rows = []
    for line in pathlib.Path(p).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"(\d+)\s+(\S+)\s*(.*)", line)
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True)
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows = parse_trace(a.trace)
    n = len(rows)
    risk = "低"
    advice = "继续运行"
    diag = ""
    if n > a.max_steps:
        risk = "高"; advice = "熔断：超过最大步数"; diag = f"已执行 {n} 步 > 上限 {a.max_steps}"
    # 重复动作检测
    last = rows[-a.repeat:] if len(rows) >= a.repeat else rows
    if len(last) == a.repeat and len(set((t[1], t[2]) for t in last)) == 1:
        risk = "高"; advice = "熔断：连续重复相同动作"; diag = f"第 {last[0][0]} 步起重复 {last[0][1]}({last[0][2]})"
    # 无进展（状态hash 相似，简化为 step 差值无新 tool）
    if n >= 6 and len(set(t[1] for t in rows[-6:])) == 1:
        if risk != "高":
            risk = "中"
        advice = "建议熔断：近 6 步无新动作，疑似原地打转"
        diag = diag or f"近 6 步均为 {rows[-1][1]}"
    if a.json:
        print(json.dumps({"steps": n, "risk": risk, "advice": advice, "diagnosis": diag}, ensure_ascii=False, indent=2))
    else:
        print(f"轨迹步数：{n}  风险：{risk}  建议：{advice}")
        if diag:
            print(f"  诊断：{diag}")

if __name__ == "__main__":
    main()
