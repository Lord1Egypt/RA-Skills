#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eval_smoke.py — 类人数字员工配置 本地离线评测冒烟（D1 评测标准化）

不依赖任何外部 API / 网络 / 基准。对一份"已部署配置"或本技能自身方法论做
"接线检查"：是否真接了 类人四件套 + 认知内核四件套 的闭环接线。
输出评分卡（逐项 OK/FAIL + 总分 + 等级）。

用法：
  python tools/eval_smoke.py demo                 # 自检本技能自身八维覆盖
  python tools/eval_smoke.py <config_dir>         # 评测某部署配置包目录
  python tools/eval_smoke.py <config_dir> --json  # 机器可读输出

退出码：全 OK=0，有 FAIL=1，参数/目录错误=2。
"""
import os, re, sys, argparse, json

# 八维评测维度（D1 标准化维度表）：每维给一组"接线标记"，命中任一即视为已接。
DIMENSIONS = [
    ("memory",        "记忆持久", ["MEMORY.md", "记忆", "写回", "writeback", "分层", "持久化"]),
    ("proactive",     "主动执行", ["主动", "cron", "触发器", "trigger", "巡检", "提醒", "定时"]),
    ("tooluse",       "工具调用", ["工具", "tool", "API", "权限", "最小权限", "permission"]),
    ("persona",       "角色一致", ["SOUL.md", "IDENTITY.md", "USER.md", "人设", "角色一致", "persona"]),
    ("reflection",    "反思闭环", ["反思", "reflection", "复盘", "自省"]),
    ("planning",      "规划推理", ["规划", "planning", "System2", "ToT", "分解", "重规划"]),
    ("consolidation", "巩固遗忘", ["巩固", "遗忘", "consolidation", "遗忘曲线", "TTL", "代谢"]),
    ("evolution",     "持续进化", ["进化", "evolution", "飞轮", "训-战-省-化", "技能", "固化"]),
]

def grade(n, mx):
    if n >= mx: return "教授(类比非职称)"
    if n >= 6:  return "副教授"
    if n >= 4:  return "讲师"
    if n >= 1:  return "助教"
    return "未达标"

def check_dir(d):
    hits = {}
    for key, label, markers in DIMENSIONS:
        found = []
        for root, _, files in os.walk(d):
            for f in files:
                if f.startswith("_") or f in ("ATTESTATION.md", "manifest.json"):
                    continue
                if not f.lower().endswith((".md", ".yaml", ".yml", ".json", ".txt", ".py")):
                    continue
                p = os.path.join(root, f)
                try:
                    t = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for m in markers:
                    if re.search(m, t, re.I) and m not in found:
                        found.append(m)
        hits[key] = (label, found)
    return hits

def main():
    ap = argparse.ArgumentParser(description="类人数字员工配置 本地离线评测冒烟 (D1)")
    ap.add_argument("target", nargs="?", help="配置目录；省略或 'demo' = 自检本技能")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    if args.target in (None, "demo"):
        target = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mode = "demo(本技能自身)"
    else:
        target = args.target
        mode = "配置目录"

    if not os.path.isdir(target):
        print(f"错误：目录不存在 {target}", file=sys.stderr)
        sys.exit(2)

    hits = check_dir(target)
    rows = []
    total = 0
    for key, label, _ in DIMENSIONS:
        _, found = hits[key]
        ok = len(found) > 0
        if ok:
            total += 1
        rows.append((label, ok, found))

    if args.json:
        out = {
            "mode": mode, "target": target,
            "score": total, "max": len(DIMENSIONS), "grade": grade(total, len(DIMENSIONS)),
            "dimensions": {k: {"ok": len(h[1]) > 0, "markers": h[1]} for k, (_, h) in hits.items()},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"=== 类人数字员工配置 · 评测冒烟 ({mode}) ===")
        print(f"目标: {target}\n")
        for label, ok, found in rows:
            status = "OK " if ok else "FAIL"
            print(f"  [{status}] {label}  (命中: {', '.join(found) if found else '无'})")
        print(f"\n总分: {total}/{len(DIMENSIONS)}  等级: {grade(total, len(DIMENSIONS))}")
        print("说明: 本评测为本地离线'接线检查'，验证配置是否接齐八维；")
        print("      长程基准(LoCoMo/LongMemEval)真跑见 references/40 §D1 路线图。")

    sys.exit(0 if total == len(DIMENSIONS) else 1)

if __name__ == "__main__":
    main()
