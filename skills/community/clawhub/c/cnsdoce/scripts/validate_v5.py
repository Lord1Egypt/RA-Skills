#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_v5.py - cnsdoce v2.0.0-alpha 回归验证
验证项：
  1. 两库搜索准确率（消耗量库 / 济南价目表）：≥20 术语，期望准确率 ≥95%
  2. AI 组价引擎关键场景回归（AZ-8-3 阀门 / AZ-8-4 法兰 / AZ-8-2 管件 / 副片换算）
  3. 公开版降级（无本地库）不崩溃
用法：python validate_v5.py
"""

import os
import re
import sys
import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS = SKILL_DIR / "scripts"
LOCAL_ASSETS = Path(os.path.expanduser("~/.workbuddy/skills/cnsdoce1/assets"))

sys.path.insert(0, str(SCRIPTS))

PASS = 0
FAIL = 0
REPORT = []


def record(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        REPORT.append(f"  ✅ {name} {detail}")
    else:
        FAIL += 1
        REPORT.append(f"  ❌ {name} {detail}")


def main():
    print("=" * 60)
    print("cnsdoce v2.0.0-alpha 回归验证")
    print("=" * 60)

    # ── 1. 两库搜索准确率 ──
    print("\n【1】两库搜索准确率（消耗量库 / 济南价目表）")
    # 术语 → 期望命中（正则，quota_no 或名称关键词）
    quota_cases = [
        ("低压法兰阀门 DN200", r"AZ-8-3-27", "消耗量库"),
        ("碳钢平焊法兰 DN200", r"AZ-8-4-21", "消耗量库"),
        ("不锈钢平焊法兰 DN300", r"AZ-8-4-146", "消耗量库"),
        ("低压碳钢管件 DN200 电弧焊", r"AZ-8-2-27", "消耗量库"),
        ("低压无缝钢管 DN200", r"AZ-8-1-27", "消耗量库"),
        ("中压法兰阀门 DN200", r"AZ-8-3-199", "消耗量库"),
        ("高压法兰阀门 DN200", r"AZ-8-3-330", "消耗量库"),
        ("调节阀门 DN350", r"AZ-8-3-91", "消耗量库"),
        ("电力电缆敷设 1kV", r"AZ-4-9-1(0[0-9]|1[0-9]|2[0-9])", "消耗量库"),  # 1kV 电缆敷设/埋地/穿管档
        ("金属软管敷设", r"AZ-4-12-168", "消耗量库"),
        ("离心式风机安装", r"AZ-1-7-", "消耗量库"),  # 第1册 风机安装节（离心式通引风机等）
        ("给排水法兰阀门 DN200", r"AZ-10-5-45", "消耗量库"),
        ("碳钢对焊法兰 DN200", r"AZ-8-4-87", "消耗量库"),
        ("低压碳钢管件 氩电联焊 DN200", r"AZ-8-2-48", "消耗量库"),
        ("镀锌钢管 DN50", r"AZ-10-[12]-", "消耗量库"),  # 给排水册镀锌钢管节（室内/室外螺纹连接）
        ("水喷淋钢管 DN25", r"AZ-9-1-1", "消耗量库"),
        ("低压阀门 DN250", r"AZ-8-3-28", "消耗量库"),
        ("手工除锈 管道", r"AZ-12-1-1", "消耗量库"),
        ("支架制作", r"AZ-13-1-1", "消耗量库"),
        ("交流发电机检查接线", r"4-6-1", "济南价目表"),
    ]

    has_local_db = (LOCAL_ASSETS / "quota_consumption.db").exists()
    if has_local_db:
        # 本地真实库回归（正式环境）——引擎 ASSETS 临时指向本地库
        import ai_quota_engine
        ai_quota_engine.ASSETS = LOCAL_ASSETS
        from ai_quota_engine import match_quota, compose_quota, unit_check
        for query, expect, db_name in quota_cases:
            if "消耗量库" in db_name:
                spec = re.search(r"DN(\d+)", query)
                spec = f"DN{spec.group(1)}" if spec else ""
                rows = match_quota(query, spec=spec, limit=10)
            else:
                rows = match_quota(query, spec="", limit=10)
            # ⚠️ 验收标准：期望值出现在 top5 候选（引擎设计为"候选+用户确认"工作流）
            top5 = rows[:5]
            hit = any(re.search(expect, str(r.get("quota_no", ""))) for r in top5)
            top = top5[0]["quota_no"] if top5 else "无"
            tops = [r["quota_no"] for r in top5]
            record(f"{query} → 期望{expect}", hit, f"(top5={tops})")
    else:
        for query, expect, db_name in quota_cases:
            record(f"{query}", False, "无本地库，跳过（公开版降级正常）")

    # ── 2. AI 组价引擎关键场景 ──
    print("\n【2】AI 组价引擎关键场景回归")
    if has_local_db:
        cases = [
            ("DN200 碳钢法兰蝶阀安装 10 个", "AZ-8-3-27", "个", 1.0),
            ("DN300 304不锈钢平焊法兰 2 副", "AZ-8-4-146", "副", 1.0),
            ("DN200 低压碳钢平焊法兰 4 片", "AZ-8-4-21", "副", 0.5),
            ("DN200 碳钢管件 电弧焊 10个", "AZ-8-2-27", "10个", 0.1),
            ("DN350 低压调节阀安装 5 个", "AZ-8-3-91", "个", 1.0),
        ]
        for text, expect_no, unit, factor in cases:
            r = compose_quota(text, use_llm=False)
            ok = r.get("ok") and r["quota"]["quota_no"] == expect_no
            detail = f"(命中 {r['quota']['quota_no'] if r.get('ok') else r.get('error')})"
            record(f"组价「{text}」→ {expect_no}", ok, detail)
            if r.get("ok"):
                # 单位换算检查
                f = r["pricing"]["unit_factor"]
                record(f"  单位比对 {r['quota']['unit']}→{unit} 系数={f}",
                       abs(f - factor) < 0.001 if f else False, f"(期望{factor})")
        # 副片换算专项
        fac, note = unit_check("片", "副")
        record("单位换算 片↔副", fac == 0.5, f"(系数={fac}, {note})")
    else:
        for text in ["DN200 碳钢法兰蝶阀安装 10 个"]:
            r = compose_quota(text, use_llm=False)
            record(f"缺库降级「{text}」", r.get("ok") is False, "(返回错误而非崩溃)")

    # ── 3. 公开版示例库检索 ──
    print("\n【3】公开版示例库检索（index/quota.db）")
    import sqlite3
    demo_db = SKILL_DIR / "index" / "quota.db"
    if demo_db.exists():
        conn = sqlite3.connect(demo_db)
        qn = conn.execute("SELECT COUNT(*) FROM quotas").fetchone()[0]
        mn = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        record(f"示例库 定额{qn}条/材料{mn}条", qn >= 25 and mn >= 15, f"(定额{qn}, 材料{mn})")
        conn.close()
    else:
        record("示例库存在", False, "index/quota.db 缺失")

    # ── 4. 敏感信息扫描 ──
    print("\n【4】敏感信息扫描（天瑞/东莞/临江/公司采购价）")
    sensitive_patterns = ["天瑞", "东莞", "临江", "公司采购价", "ERP应付"]
    found = []
    for root, dirs, files in os.walk(SKILL_DIR):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not (fn.endswith(".md") or fn.endswith(".py") or fn.endswith(".txt")):
                continue
            if fn == "validate_v5.py":   # 扫描器自身含关键词，排除
                continue
            p = Path(root) / fn
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                for pat in sensitive_patterns:
                    if pat in content:
                        found.append(f"{p.name}:{pat}")
            except Exception:
                pass
    record("无敏感信息", not found, f"({'; '.join(found[:5]) if found else '扫描通过'})")

    # ── 汇总 ──
    print("\n" + "=" * 60)
    print(f"验证汇总: 通过 {PASS} / 失败 {FAIL}")
    rate = PASS / (PASS + FAIL) * 100 if (PASS + FAIL) else 0
    print(f"通过率: {rate:.1f}%")
    print("=" * 60)
    for line in REPORT:
        print(line)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
