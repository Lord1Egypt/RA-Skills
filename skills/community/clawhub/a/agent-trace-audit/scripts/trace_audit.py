# -*- coding: utf-8 -*-
"""行为留痕审计：读 JSONL 动作日志，建账本，标出未过闸越界项。零依赖。"""
import argparse, json, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    a = ap.parse_args()
    rows = []
    for line in pathlib.Path(a.log).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    if not rows:
        print("无动作记录")
        return
    rows.sort(key=lambda r: r.get("ts", ""))
    violations = []
    print(f"行为账本（{len(rows)} 条）：\n" + "=" * 50)
    for r in rows:
        gate = r.get("gate", "无闸")
        flag = "🔒越界" if gate in ("无闸", "ungated", None) and r.get("action", "").find("写") >= 0 else ""
        if flag:
            violations.append(r)
        print(f"  {r.get('ts','?')} | {r.get('actor','?')} | {r.get('action','?')} → {r.get('target','?')} | gate={gate} {flag}")
    print("=" * 50)
    print(f"违规（未过闸写操作）：{len(violations)} 条" if violations else "✅ 无越界写操作")

if __name__ == "__main__":
    main()
