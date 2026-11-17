#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 方向记录/*.md 同步到飞书「02_方向研究」文件夹。

为什么单独一个脚本：`sync_ledgers_to_feishu.py` 只覆盖
候选台账 + 流程状态表 + 待办与时点，**不含 方向记录/**，
于是这类方向研究报告一直不在云端。
本脚本补这个缺口，复用前者的 token/api/write_doc（同一套凭证与写法）。

用法：
  python3 sync_direction_docs_to_feishu.py                    # 全部 *.md
  python3 sync_direction_docs_to_feishu.py 方向甲_....md ...  # 只同步指定几份
"""
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_ledgers_to_feishu import (BASE, INDEX, api, guard, load_index,  # noqa: E402
                                    token, write_doc)

DIR = BASE.parent / "方向记录"
FOLDER = os.environ.get("FEISHU_FOLDER_DIRECTION", "").strip()   # 02_方向研究（自建后填环境变量）

# 🔴 隐私：与持仓台账同口径。命中即**不同步该文件**（不是读了再过滤）。
#    持仓数量/成本/盈亏一律不出本机。
PRIVACY = (
    (r"\d{3,6}\s*股", "疑似持股数"),
    (r"加权成本\s*[|｜]\s*\d", "疑似加权成本"),
    (r"(已实现|未实现)盈亏\s*[|｜]\s*[-−\d]", "疑似盈亏金额"),
)


def main() -> None:
    if not FOLDER:
        print("ℹ️ 未配置 FEISHU_FOLDER_DIRECTION（02_方向研究 文件夹 token）"
              "→ 跳过方向文档同步。配置方法见 README。", file=sys.stderr)
        return
    idx = load_index()
    T = token()
    d = idx.setdefault("direction", {})

    args = sys.argv[1:]
    if args:
        files = []
        for a in args:
            p = pathlib.Path(a)
            files.append(p if p.is_absolute() else DIR / a)
    else:
        files = sorted(DIR.glob("*.md"))

    ok = bad = 0
    errors, skipped = [], []
    for f in files:
        if not f.exists():
            errors.append(f"{f.name}：文件不存在")
            bad += 1
            continue
        guard(f)
        text = f.read_text(encoding="utf-8")
        hit = next((why for rx, why in PRIVACY if re.search(rx, text)), None)
        if hit:
            skipped.append(f"{f.name}（{hit}）")
            print(f"  🔒 跳过 {f.name}：{hit}")
            continue
        name = f.stem
        doc = d.get(name, "")
        if not doc:
            r = api("POST", T, "/docx/v1/documents",
                    {"folder_token": FOLDER, "title": name})
            doc = (r.get("data") or {}).get("document", {}).get("document_id", "")
            if not doc:
                msg = f"{name}：建文档失败 {r.get('msg')}"
                print(f"  ❌ {msg}")
                errors.append(msg)
                bad += 1
                continue
            # 🔴 建完立刻落盘，避免被超时中断后下次重跑再建一份（重名）
            d[name] = doc
            INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
        good, msg = write_doc(f, doc)
        if good:
            d[name] = doc
        else:
            errors.append(f"{name} 写入失败：{msg}")
        print(f"  {'✅' if good else '❌'} {name}  {msg[:56]}")
        ok += good
        bad += (not good)

    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📊 成功 {ok}｜失败 {bad}｜隐私跳过 {len(skipped)}")
    print(f"📁 目标：02_方向研究 {FOLDER}")
    if skipped:
        print("🔒 未同步（隐私边界）：")
        for s in skipped:
            print(f"   · {s}")
    if errors:
        print("\n🔴🔴 失败明细（云端与本地不一致）：")
        for e in errors:
            print(f"   · {e}")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
