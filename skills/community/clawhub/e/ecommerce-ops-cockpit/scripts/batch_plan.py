#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量变更 dry-run 预演：只出预览报告，绝不执行任何平台操作。

借鉴 QM-CLAW `ecommerce` 技能的店铺操作守则：
  - 批量操作默认 dry-run，先出预览再让人确认
  - **不从缺失行推断删除**（缺失只跳过，绝不产生未声明的 delete）
  - 保留原件，输出带时间戳的变更文件
  - 每个变更都要能回滚：记录「变更前 / 变更后」

本脚本只做预演与风险标记。它不登录店铺、不调用任何平台 API、不写回原文件。

输入 JSON：
{
  "action": "price_update",        // price_update / publish / unpublish / update / delete
  "dry_run": true,                 // 默认 true
  "rows": [
    {"sku":"A1","title":"榨汁杯","field":"price","old":129,"new":99,"stock":50,"status":"active"},
    {"sku":"A2","title":"收纳箱","field":"price","old":89,"new":95,"stock":0}
  ]
}

风险规则：
  P0  降价幅度 >30%            P0  有库存却下架/删除    P0  重复 SKU
  P1  涨价幅度 >50%            P1  无标题（不便人工核对）
  跳过：缺 sku / 缺 old 与 new / old == new（无变化）

用法：
  python batch_plan.py --data plan.json
  python batch_plan.py --data plan.json --json
  python batch_plan.py --data plan.json --csv-out preview.csv
  python batch_plan.py --demo
  python batch_plan.py --self-test
退出码：0 无风险 / 1 存在 P0（必须人工确认后才可继续） / 2 输入错误
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime

P0_DROP = 0.30      # 降价超 30% → P0
P1_RISE = 0.50      # 涨价超 50% → P1


def _num(v):
    """安全转数字；非数字返回 None（不硬转 0，避免把缺失伪装成 0）。"""
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def plan(data):
    action = data.get("action") or "update"
    dry = data.get("dry_run", True)
    rows = data.get("rows") or []
    if not rows:
        raise ValueError("缺少 rows（至少一行）")

    seen = {}
    out = []
    for idx, r in enumerate(rows):
        sku = r.get("sku")
        item = {"row": idx + 1, "sku": sku, "title": r.get("title") or "",
                "field": r.get("field"), "old": r.get("old"), "new": r.get("new"),
                "stock": _num(r.get("stock")), "status": r.get("status"),
                "risks": [], "skip": None}

        # ── 跳过判定（缺失 / 无变化）──
        if not sku:
            item["skip"] = "缺 SKU"
            out.append(item)
            continue
        if item["field"] is None and action in ("price_update", "update"):
            item["skip"] = "缺变更字段"
            out.append(item)
            continue
        if item["old"] is None and item["new"] is None:
            item["skip"] = "缺变更前/后值"
            out.append(item)
            continue
        if item["old"] is not None and item["new"] is not None and item["old"] == item["new"]:
            item["skip"] = "变更前=变更后（无变化）"
            out.append(item)
            continue

        # ── 重复 SKU ──
        if sku in seen:
            item["risks"].append(("P0", "SKU 重复（第 %d 行已出现）" % seen[sku]))
        else:
            seen[sku] = idx + 1

        # ── 价格风险 ──
        o, n = _num(item["old"]), _num(item["new"])
        if o is not None and n is not None and o > 0:
            chg = (o - n) / o
            if chg > P0_DROP:
                item["risks"].append(("P0", "降价 %.0f%%，超过 30%% 阈值" % (chg * 100)))
            elif -chg > P1_RISE:
                item["risks"].append(("P1", "涨价 %.0f%%，超过 50%% 阈值" % (-chg * 100)))
            if n is not None and n <= 0:
                item["risks"].append(("P0", "变更后价格 <= 0"))

        # ── 有库存却下架/删除 ──
        if action in ("unpublish", "delete") and (item["stock"] or 0) > 0:
            item["risks"].append(("P0", "有库存 %d 件却要 %s" % (int(item["stock"]), action)))

        if not item["title"]:
            item["risks"].append(("P1", "无标题，不便人工核对"))

        out.append(item)

    will = [x for x in out if not x["skip"]]
    skipped = [x for x in out if x["skip"]]
    p0 = [x for x in will if any(lv == "P0" for lv, _ in x["risks"])]
    p1 = [x for x in will if any(lv == "P1" for lv, _ in x["risks"])]

    # 绝不推断删除：只有 action=delete 才产生删除语义
    delete_rows = [x for x in will] if action == "delete" else []

    return {"action": action, "dry_run": dry, "rows": out,
            "total": len(out), "will_change": len(will), "skipped": len(skipped),
            "p0": len(p0), "p1": len(p1), "delete_rows": len(delete_rows),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


def render(r):
    o = []
    o.append("【批量变更预演】action=%s  dry_run=%s" % (r["action"], r["dry_run"]))
    o.append("总行数 %d ｜ 将变更 %d ｜ 跳过 %d ｜ 风险 P0 %d / P1 %d"
             % (r["total"], r["will_change"], r["skipped"], r["p0"], r["p1"]))
    o.append("")
    o.append("【变更预览】")
    for x in r["rows"]:
        if x["skip"]:
            o.append("  [跳过] 第%d行 %s：%s" % (x["row"], x["sku"] or "(无SKU)", x["skip"]))
            continue
        old_s = "" if x["old"] is None else str(x["old"])
        new_s = "" if x["new"] is None else str(x["new"])
        tag = ""
        if x["risks"]:
            tag = "  ⚠ " + "；".join("%s %s" % (lv, m) for lv, m in x["risks"])
        o.append("  [%s] %s ｜ %s：%s → %s%s"
                 % ("P0" if any(lv == "P0" for lv, _ in x["risks"]) else "OK",
                    x["sku"], x["field"] or "-", old_s, new_s, tag))
    o.append("")
    if r["p0"]:
        o.append("【结论】存在 %d 条 P0 风险，**确认前不得执行**。" % r["p0"])
    else:
        o.append("【结论】无 P0 风险，可交由人工在后台执行（本脚本不执行）。")
    o.append("")
    o.append("【守则】")
    o.append("  · 本脚本只出预览，不登录店铺、不调 API、不改原文件")
    o.append("  · 不从缺失行推断删除：action=%s，删除语义行数=%d" % (r["action"], r["delete_rows"]))
    o.append("  · 执行前请保留原始导出文件，另存带时间戳的变更文件（%s）" % r["generated_at"])
    o.append("  · 每个变更记录变更前/后值，保证可回滚")
    return "\n".join(o)


def make_spec(r, title=None, subtitle=None):
    """产出可直接喂给 report_pdf.build 的 spec（只描述预演结果，不含任何执行动作）。"""
    blocks = [
        {"type": "h1", "text": "一、预演结论"},
        {"type": "callout", "tone": "warn" if r["p0"] else "ok",
         "text": "动作 %s ｜ 总行 %d、将变更 %d、跳过 %d ｜ 风险 P0 %d / P1 %d。%s"
                 % (r["action"], r["total"], r["will_change"], r["skipped"],
                    r["p0"], r["p1"],
                    "存在 P0，**确认前不得执行**。" if r["p0"] else "无 P0 风险，可交人工在后台执行。")},
        {"type": "kv", "per_row": 4, "items": [
            ["总行数", str(r["total"])], ["将变更", str(r["will_change"])],
            ["跳过", str(r["skipped"])], ["P0 风险", str(r["p0"])]]},
        {"type": "h1", "text": "二、变更分布"},
        {"type": "bar", "title": "预演结果分布（行）",
         "labels": ["将变更", "跳过", "P0 风险", "P1 提示"],
         "values": [r["will_change"], r["skipped"], r["p0"], r["p1"]], "unit": "行"},
        {"type": "h1", "text": "三、变更预览（变更前 → 变更后）"},
        {"type": "table", "header": ["SKU", "字段", "变更前", "变更后", "状态/风险"],
         "rows": [[x["sku"] or "(无)", x["field"] or "-",
                   "" if x["old"] is None else str(x["old"]),
                   "" if x["new"] is None else str(x["new"]),
                   x["skip"] or ("；".join("%s %s" % (lv, m) for lv, m in x["risks"]) or "OK")]
                  for x in r["rows"]]},
        {"type": "bullets", "items": [
            "本预览只做呈现，不登录店铺、不调 API、不改原文件",
            "绝不从缺失行推断删除：动作=%s，删除语义行数=%d" % (r["action"], r["delete_rows"]),
            "执行前保留原始导出文件，另存带时间戳的变更文件（%s）" % r["generated_at"],
            "每行记录变更前/后值，保证可回滚"]},
    ]
    spec = {"blocks": blocks}
    if title:
        spec["title"] = title
    if subtitle:
        spec["subtitle"] = subtitle
    return spec


DEMO = {
    "action": "price_update",
    "dry_run": True,
    "rows": [
        {"sku": "A1", "title": "便携榨汁杯", "field": "price", "old": 129, "new": 99, "stock": 320},
        {"sku": "A2", "title": "大容量收纳箱", "field": "price", "old": 89, "new": 95, "stock": 0},
        {"sku": "A3", "title": "无线充电底座", "field": "price", "old": 199, "new": 119, "stock": 88},
        {"sku": "A1", "title": "便携榨汁杯", "field": "price", "old": 129, "new": 109, "stock": 320},
        {"sku": "A4", "field": "price", "old": 59, "new": 49},
        {"sku": "A5", "title": "玻璃保鲜盒", "field": "price", "old": 79, "new": 79, "stock": 12},
        {"sku": "", "title": "缺SKU样例", "field": "price", "old": 39, "new": 35},
    ],
}


def main():
    ap = argparse.ArgumentParser(description="批量变更 dry-run 预演（只出预览不执行）")
    ap.add_argument("--data")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--csv-out", help="导出预览 CSV")
    ap.add_argument("--spec-out", help="输出 report_pdf 可用的图表 spec JSON")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if a.demo:
        data = DEMO
    elif a.data:
        if not os.path.isfile(a.data):
            sys.stderr.write("输入文件不存在: %s\n" % a.data)
            return 2
        with open(a.data, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                sys.stderr.write("JSON 解析失败: %s\n" % e)
                return 2
    else:
        sys.stderr.write("需要 --data / --demo / --self-test 之一\n")
        return 2

    try:
        r = plan(data)
    except ValueError as e:
        sys.stderr.write("输入错误: %s\n" % e)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render(r))

    if a.csv_out:
        with open(a.csv_out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["row", "sku", "title", "field", "old", "new", "stock", "status", "risk"])
            for x in r["rows"]:
                w.writerow([x["row"], x["sku"] or "", x["title"], x["field"] or "",
                            "" if x["old"] is None else x["old"],
                            "" if x["new"] is None else x["new"],
                            "" if x["stock"] is None else x["stock"], x["status"] or "",
                            x["skip"] or ("；".join("%s:%s" % (lv, m) for lv, m in x["risks"]))])
        sys.stderr.write("预览 CSV 已写入 %s\n" % a.csv_out)

    if a.spec_out:
        with open(a.spec_out, "w", encoding="utf-8") as f:
            json.dump(make_spec(r, title="批量变更预演报告（%s）" % r["action"]), f,
                      ensure_ascii=False, indent=2)
        sys.stderr.write("spec 已写入 %s\n" % a.spec_out)

    return 1 if r["p0"] else 0


def self_test():
    ok = True

    def chk(name, got, exp, tol=1e-9):
        nonlocal ok
        good = (abs(got - exp) < tol) if isinstance(exp, float) else (got == exp)
        print("[%s] %s (got=%s exp=%s)" % ("PASS" if good else "FAIL", name, got, exp))
        if not good:
            ok = False

    base = lambda **kw: dict({"action": "price_update", "rows": []}, **kw)  # noqa: E731

    # 1) 降价 40% → P0；无变化 → 跳过；缺 SKU → 跳过；重复 SKU → P0
    r = plan({"action": "price_update", "rows": [
        {"sku": "A1", "title": "t", "field": "price", "old": 100, "new": 60},   # -40% P0
        {"sku": "A2", "title": "t", "field": "price", "old": 50, "new": 50},    # 无变化 跳过
        {"sku": "", "title": "t", "field": "price", "old": 30, "new": 25},      # 缺 SKU 跳过
        {"sku": "A1", "title": "t", "field": "price", "old": 100, "new": 90},   # 重复 P0
    ]})
    chk("总数=4", r["total"], 4)
    chk("跳过=2（无变化+缺SKU）", r["skipped"], 2)
    chk("P0>=1（降价40%）", r["p0"] >= 1, True)
    chk("重复SKU被标记P0",
        any(lv == "P0" and "重复" in m for lv, m in r["rows"][3]["risks"]), True)

    # 2) 有库存却下架 → P0
    r2 = plan({"action": "unpublish", "rows": [
        {"sku": "B1", "title": "t", "field": "status", "old": "active", "new": "inactive", "stock": 40},
    ]})
    chk("有库存下架→P0",
        any(lv == "P0" and "有库存" in m for lv, m in r2["rows"][0]["risks"]), True)

    # 3) 绝不推断删除：action=price_update 时删除语义行数为 0
    r3 = plan({"action": "price_update", "rows": [
        {"sku": "C1", "title": "t", "field": "price", "old": 10, "new": 9},
    ]})
    chk("非delete动作不产生删除语义", r3["delete_rows"], 0)
    r3b = plan({"action": "delete", "rows": [
        {"sku": "C2", "title": "t", "field": "status", "old": "active", "new": "deleted"},
    ]})
    chk("delete动作才产生删除语义", r3b["delete_rows"], 1)

    # 4) 涨价 60% → P1
    r4 = plan({"action": "price_update", "rows": [
        {"sku": "D1", "title": "t", "field": "price", "old": 50, "new": 80},
    ]})
    chk("涨价60%→P1",
        any(lv == "P1" and "涨价" in m for lv, m in r4["rows"][0]["risks"]), True)

    # 5) 缺 rows 应报错；dry_run 默认 True
    try:
        plan({"action": "price_update"})
        chk("缺 rows 应抛错", False, True)
    except ValueError:
        chk("缺 rows 应抛错", True, True)
    r5 = plan({"action": "price_update", "rows": [
        {"sku": "E1", "title": "t", "field": "price", "old": 10, "new": 9}]})
    chk("dry_run 默认 True", r5["dry_run"], True)

    print("\n自测：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
