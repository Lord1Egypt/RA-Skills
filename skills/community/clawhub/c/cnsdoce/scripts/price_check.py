#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
price_check.py - cnsdoce1 增强2：AI 价格自检与询比价（借鉴广联达 AI 质控 + AI 询比价）

功能：
  1. 报价结果 ↔ 历史项目同类型价格区间对标（±30% 黄标 / ±50% 红标 + 溯源）
  2. AI 询比价推荐：inquiry_inquiry.db 供应商价格区间 + 采购建议价
  3. 三库缺口标注（询价库/信息价/价目表均无 → ⚠️估算，严禁编造）
  4. 输出结构化检查报告 JSON

用法：
  python price_check.py check "AZ-8-3-27" 412.44        # 单条定额价格自检
  python price_check.py check-material "法兰阀门" "DN200" 350.0   # 材料询比价+对标
  python price_check.py report '<组价JSON>'              # 对 ai_quota_engine 输出整体检查
  python price_check.py --json '{"quota_no":"AZ-8-3-27","unit_price":412.44,"specs":"DN200"}'
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path

ASSETS = Path(__file__).parent.parent / "assets"

YELLOW_THRESHOLD = 0.30   # ±30% 黄标（提示复核）
RED_THRESHOLD = 0.50      # ±50% 红标（预警溯源）


def _connect(db_name):
    path = ASSETS / db_name
    if not path.exists():
        return None
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────── 1. 历史价格对标 ───────────────────────────

def check_against_history(quota_no, unit_price, specs=""):
    """
    报价 vs 历史项目同类型价格区间对标
    返回 {level, deviation, history_count, history_avg, history_min, history_max, note}
    """
    result = {"level": "info", "deviation": 0, "history_count": 0,
              "history_avg": None, "history_min": None, "history_max": None,
              "note": "历史库无同定额记录，跳过对标"}
    conn = _connect("project_history.db")
    if not conn:
        return result
    try:
        sql = "SELECT unit_price FROM quota_items WHERE quota_no = ? AND unit_price > 0"
        params = [quota_no]
        if specs:
            sql += " AND specs LIKE ?"
            params.append(f"%{specs}%")
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        if not rows:
            return result
        prices = [r["unit_price"] for r in rows]
        avg = sum(prices) / len(prices)
        mn, mx = min(prices), max(prices)
        deviation = (unit_price - avg) / avg if avg else 0
        if abs(deviation) >= RED_THRESHOLD:
            level = "red"
            note = (f"🔴 超历史均价 ±50%：偏差 {deviation:+.1%}（历史均价 {avg:.2f}，"
                    f"区间 {mn:.2f}~{mx:.2f}，样本 {len(prices)}）。检查：定额套错/单位换算漏/主材价异常")
        elif abs(deviation) >= YELLOW_THRESHOLD:
            level = "yellow"
            note = (f"🟡 超历史均价 ±30%：偏差 {deviation:+.1%}（历史均价 {avg:.2f}，"
                    f"区间 {mn:.2f}~{mx:.2f}，样本 {len(prices)}）。建议复核价格或主材")
        else:
            level = "green"
            note = f"✅ 在历史价格区间内（偏差 {deviation:+.1%}，历史均价 {avg:.2f}，样本 {len(prices)}）"
        return {"level": level, "deviation": round(deviation, 4), "history_count": len(prices),
                "history_avg": round(avg, 2), "history_min": round(mn, 2), "history_max": round(mx, 2),
                "note": note}
    except Exception as e:
        conn.close()
        return {**result, "note": f"对标异常: {e}"}


# ─────────────────────────── 2. AI 询比价推荐 ───────────────────────────

def ai_price_recommend(material_name, spec="", target_price=None):
    """
    AI 询比价：从公司询价库给出供应商价格区间 + 采购建议价
    返回 {found, vendor_count, min_price, max_price, avg_price, recommend_price,
          vendors[], note}
    """
    result = {"found": False, "vendor_count": 0, "min_price": None, "max_price": None,
              "avg_price": None, "recommend_price": None, "vendors": [], "note": ""}
    conn = _connect("inquiry_inquiry.db")
    if not conn:
        return result
    try:
        # 汇总区间（inquiry_materials）
        sql = """SELECT min_price, max_price, avg_price, vendor_count, inquiry_count
                 FROM inquiry_materials WHERE 1=1"""
        params = []
        if material_name:
            sql += " AND material_name LIKE ?"
            params.append(f"%{material_name}%")
        if spec:
            sql += " AND (spec LIKE ? OR material_name LIKE ?)"
            params.extend([f"%{spec}%", f"%{spec}%"])
        sql += " ORDER BY inquiry_count DESC, last_inquiry_date DESC LIMIT 5"
        mats = conn.execute(sql, params).fetchall()
        if mats:
            m = mats[0]
            result.update({
                "found": True,
                "vendor_count": m["vendor_count"],
                "min_price": m["min_price"],
                "max_price": m["max_price"],
                "avg_price": m["avg_price"],
                "recommend_price": m["avg_price"],   # 采购建议价 = 历史成交均价
                "note": f"公司询价库 {m['inquiry_count']} 次询价",
            })
        # 供应商明细（inquiry_records join）
        sql2 = """SELECT ir.vendor, ir.unit_price_tax, ir.inquiry_date, ir.doc_no
                  FROM inquiry_records ir
                  JOIN inquiry_materials im ON ir.material_id = im.id
                  WHERE im.material_name LIKE ?"""
        params2 = [f"%{material_name}%"]
        if spec:
            sql2 += " AND (im.spec LIKE ? OR im.material_name LIKE ?)"
            params2.extend([f"%{spec}%", f"%{spec}%"])
        sql2 += " ORDER BY ir.inquiry_date DESC LIMIT 5"
        vendors = [dict(r) for r in conn.execute(sql2, params2).fetchall()]
        if vendors:
            result["vendors"] = vendors
            if not result["found"]:
                prices = [v["unit_price_tax"] for v in vendors if v["unit_price_tax"]]
                if prices:
                    result.update({"found": True, "min_price": min(prices), "max_price": max(prices),
                                   "avg_price": sum(prices) / len(prices),
                                   "recommend_price": sum(prices) / len(prices),
                                   "vendor_count": len(set(v["vendor"] for v in vendors)),
                                   "note": "公司询价库（明细级）"})
        conn.close()
    except Exception as e:
        conn.close()
        result["note"] = f"询比价异常: {e}"

    # 与目标价对标（如果传入）
    if result["found"] and target_price and result["avg_price"]:
        dev = (target_price - result["avg_price"]) / result["avg_price"]
        if abs(dev) >= RED_THRESHOLD:
            result["target_level"] = "red"
            result["target_note"] = f"🔴 与公司采购均价偏差 {dev:+.1%}，价格异常需溯源"
        elif abs(dev) >= YELLOW_THRESHOLD:
            result["target_level"] = "yellow"
            result["target_note"] = f"🟡 与公司采购均价偏差 {dev:+.1%}，建议复核"
        else:
            result["target_level"] = "green"
            result["target_note"] = f"✅ 与公司采购均价基本一致（偏差 {dev:+.1%}）"
    elif result["found"] and not result["avg_price"]:
        result["target_note"] = "⚠️ 询价库无有效均价"
    return result


# ─────────────────────────── 3. 三库缺口检查 ───────────────────────────

def check_3tier_gap(material_name, spec=""):
    """三库缺口检查：询价库/信息价/价目表 是否覆盖"""
    from ai_quota_engine import lookup_price_3tier
    info = lookup_price_3tier(material_name, spec)
    return {
        "material": material_name,
        "spec": spec,
        "found": info["price"] is not None,
        "price": info["price"],
        "source": info["source"],
        "note": info["note"],
    }


# ─────────────────────────── 4. 整体检查报告 ───────────────────────────

def check_quota_report(quota_no, unit_price, specs="", material_name=""):
    """对单条定额做完整检查：历史对标 + 询比价 + 缺口"""
    report = {
        "quota_no": quota_no,
        "unit_price": unit_price,
        "specs": specs,
        "history_check": check_against_history(quota_no, unit_price, specs),
    }
    if material_name:
        report["price_recommend"] = ai_price_recommend(material_name, specs, unit_price)
        report["3tier_gap"] = check_3tier_gap(material_name, specs)
    else:
        report["price_recommend"] = {"found": False, "note": "未指定材料名，跳过询比价"}
    return report


def check_engine_report(engine_json):
    """对 ai_quota_engine.py 输出做整体检查"""
    data = engine_json if isinstance(engine_json, dict) else json.loads(engine_json)
    if not data.get("ok"):
        return {"ok": False, "error": data.get("error")}
    report = {
        "ok": True,
        "quota_no": data["quota"]["quota_no"],
        "quota_name": data["quota"]["name"],
        "specs": data["parsed"]["spec"],
        "ad_unit": data["pricing"]["ad_unit"],
        "checks": [],
        "summary": {"green": 0, "yellow": 0, "red": 0},
    }
    # 主定额 AD 历史对标
    hc = check_against_history(data["quota"]["quota_no"], data["pricing"]["ad_unit"])
    report["checks"].append({"type": "主定额AD历史对标", **hc})
    report["summary"][hc["level"] if hc["level"] in ("green", "yellow", "red") else "green"] += 1

    # 主材询比价 + 缺口
    for m in data.get("main_materials", []):
        if not m.get("price"):
            report["checks"].append({
                "type": "主材缺口",
                "material": m["resource_name"],
                "spec": m.get("resource_spec", ""),
                "level": "red",
                "note": m.get("price_note", "⚠️ 无价格，须询价/估算标注"),
            })
            report["summary"]["red"] += 1
            continue
        rec = ai_price_recommend(m["resource_name"], m.get("resource_spec", ""), m["price"])
        level = rec.get("target_level", "green")
        report["checks"].append({
            "type": "主材询比价",
            "material": m["resource_name"],
            "spec": m.get("resource_spec", ""),
            "level": level,
            "price": m["price"],
            "recommend": rec.get("recommend_price"),
            "vendor_count": rec.get("vendor_count"),
            "note": rec.get("target_note") or rec.get("note", ""),
        })
        report["summary"][level if level in ("green", "yellow", "red") else "green"] += 1
    return report


# ─────────────────────────── CLI ───────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "check" and len(args) >= 3:
        report = check_quota_report(args[1], float(args[2]),
                                    specs=args[3] if len(args) > 3 else "",
                                    material_name=args[4] if len(args) > 4 else "")
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args[0] == "check-material" and len(args) >= 3:
        rec = ai_price_recommend(args[1], args[2] if len(args) > 2 else "",
                                 float(args[3]) if len(args) > 3 else None)
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    elif args[0] == "report" and len(args) >= 2:
        report = check_engine_report(json.loads(args[1]))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args[0] == "--json" and len(args) >= 2:
        report = check_quota_report(**json.loads(args[1]))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("参数不足或格式错误")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
