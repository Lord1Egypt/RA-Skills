#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indicator_engine.py - cnsdoce1 增强3：AI 指标引擎（借鉴广联达指标网/指标神器）

功能：
  1. indicators 表（project_history.db 内）：沉淀单方造价/含量/综合单价指标
  2. 指标计算：从项目报价自动提取（单方造价=总价/面积、含量=主材量/面积、综合单价）
  3. 动态调价：历史指标 × (当前信息价/历史信息价) → 生成"当前价格下"的指标
  4. 对标推荐：新报价自动匹配最相似历史项目/定额，输出对标结论
  5. 数据闭环：报价 → 入库 → 指标 → ML → 对标（贯穿三大增强）

用法：
  python indicator_engine.py init                      # 建 indicators 表
  python indicator_engine.py calc '<项目JSON>'          # 计算并存储指标
  python indicator_engine.py query <工程类型>           # 查询指标
  python indicator_engine.py benchmark '<规格>'         # 对标推荐（同规格历史指标）
  python indicator_engine.py adjust <indicator_id> <当前信息价> <历史信息价>   # 动态调价
  python indicator_engine.py list                       # 列出全部指标
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

ASSETS = Path(__file__).parent.parent / "assets"
DB_PATH = ASSETS / "project_history.db"


def _connect(write=False):
    if not DB_PATH.exists() and write:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """创建 indicators 指标表"""
    conn = _connect(write=True)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,              -- 关联 projects.id（可为空=行业参考指标）
            engineering_type TEXT,           -- 工程类型（工业管道/给排水等）
            quota_no TEXT,                   -- 定额编号（如 AZ-8-3-27）
            item_name TEXT,                  -- 指标名称（如 法兰阀门安装）
            specs TEXT,                      -- 规格（DN200）
            quantity REAL,                   -- 工程量
            unit TEXT,                       -- 单位
            total_cost REAL,                 -- 合价（元）
            cost_per_unit REAL,              -- 单方造价/单价指标（元/单位量）
            content_index REAL,              -- 含量指标（主材量/工程量）
            main_material TEXT,              -- 主材名称
            info_price REAL,                 -- 计算时点信息价（用于动态调价）
            price_date TEXT,                 -- 价格期数（如 2026-06）
            district TEXT DEFAULT '济南',     -- 地区
            source TEXT DEFAULT 'project',   -- 来源（project/import/manual）
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_ind_quota ON indicators(quota_no)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_ind_type ON indicators(engineering_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_ind_spec ON indicators(specs)")
    conn.commit()
    conn.close()
    print(f"✅ indicators 表就绪: {DB_PATH}")


# ─────────────────────────── 指标计算 ───────────────────────────

def calc_indicator(project_data, main_material_price=0, info_price=None, price_date="2026-06"):
    """
    计算单条指标（借鉴指标神器公式）：
      单方造价(cost_per_unit) = 总价 / 工程量
      含量指标(content_index) = 主材量 / 工程量
    project_data: {quota_no, item_name, specs, quantity, unit, total_cost,
                   main_material, main_material_qty, engineering_type, district}
    """
    qty = float(project_data.get("quantity") or 1)
    total = float(project_data.get("total_cost") or 0)
    mm_qty = float(project_data.get("main_material_qty") or 0)
    cpu = round(total / qty, 4) if qty else None
    ci = round(mm_qty / qty, 6) if qty else None

    conn = _connect(write=True)
    c = conn.cursor()
    c.execute("""
        INSERT INTO indicators (
            project_id, engineering_type, quota_no, item_name, specs,
            quantity, unit, total_cost, cost_per_unit, content_index,
            main_material, info_price, price_date, district, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        project_data.get("project_id"),
        project_data.get("engineering_type", "工业管道"),
        project_data.get("quota_no"),
        project_data.get("item_name"),
        project_data.get("specs"),
        qty,
        project_data.get("unit", "个"),
        total,
        cpu,
        ci,
        project_data.get("main_material"),
        info_price,
        price_date,
        project_data.get("district", "济南"),
        project_data.get("source", "project"),
    ))
    ind_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"✅ 指标已存储 (ID={ind_id}): {project_data.get('item_name')} "
          f"单方造价={cpu} 含量={ci}")
    return {"id": ind_id, "cost_per_unit": cpu, "content_index": ci}


# ─────────────────────────── 动态调价 ───────────────────────────

def dynamic_adjust(indicator_id, current_price, history_price):
    """
    动态调价（借鉴指标网动态调价）：
      当前指标 = 历史指标 × (当前信息价 / 历史信息价)
    返回 {original, adjusted, ratio}
    """
    conn = _connect(write=True)
    c = conn.cursor()
    row = c.execute("SELECT id, cost_per_unit, info_price FROM indicators WHERE id=?",
                    (indicator_id,)).fetchone()
    if not row:
        conn.close()
        return {"error": f"指标 {indicator_id} 不存在"}
    if not history_price:
        conn.close()
        return {"error": "缺少历史信息价，无法调价"}
    ratio = current_price / history_price
    adjusted = round((row[1] or 0) * ratio, 4)
    c.execute("UPDATE indicators SET info_price=? WHERE id=?", (current_price, indicator_id))
    conn.commit()
    conn.close()
    return {"id": indicator_id, "original": row[1], "ratio": round(ratio, 4),
            "adjusted": adjusted, "current_price": current_price,
            "history_price": history_price}


# ─────────────────────────── 对标推荐 ───────────────────────────

def benchmark(specs="", engineering_type=None, quota_no=None, limit=5):
    """
    对标推荐：匹配最相似历史指标（规格/工程类型/定额）
    返回 [{item_name, specs, cost_per_unit, content_index, engineering_type, price_date}]
    """
    conn = _connect()
    sql = "SELECT * FROM indicators WHERE 1=1"
    params = []
    if specs:
        sql += " AND specs LIKE ?"
        params.append(f"%{specs}%")
    if engineering_type:
        sql += " AND engineering_type LIKE ?"
        params.append(f"%{engineering_type}%")
    if quota_no:
        sql += " AND quota_no = ?"
        params.append(quota_no)
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    cur = conn.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    conn.close()
    return rows


def benchmark_report(new_indicator):
    """
    新报价对标报告：计算新指标 vs 历史同规格指标
    new_indicator: {specs, cost_per_unit, engineering_type}
    返回 {benchmarks[], level, note}
    """
    specs = new_indicator.get("specs", "")
    cpu = new_indicator.get("cost_per_unit", 0)
    et = new_indicator.get("engineering_type")
    rows = benchmark(specs=specs, engineering_type=et)
    if not rows:
        return {"benchmarks": [], "level": "info",
                "note": f"历史库无同规格({specs})指标，暂无对标样本"}
    result = []
    for r in rows:
        dev = (cpu - r["cost_per_unit"]) / r["cost_per_unit"] if r["cost_per_unit"] else 0
        level = "red" if abs(dev) >= 0.5 else ("yellow" if abs(dev) >= 0.3 else "green")
        result.append({"id": r["id"], "item_name": r["item_name"], "specs": r["specs"],
                       "engineering_type": r["engineering_type"],
                       "cost_per_unit": r["cost_per_unit"],
                       "content_index": r["content_index"], "price_date": r["price_date"],
                       "deviation": round(dev, 4), "level": level})
    level = "red" if any(x["level"] == "red" for x in result) else \
            ("yellow" if any(x["level"] == "yellow" for x in result) else "green")
    note = {"red": "🔴 存在超出历史 ±50% 的指标项，建议溯源",
            "yellow": "🟡 存在超出历史 ±30% 的指标项，建议复核",
            "green": "✅ 与历史同规格指标基本一致"}[level]
    return {"benchmarks": result, "level": level, "note": note}


# ─────────────────────────── 查询 / CLI ───────────────────────────

def list_indicators(limit=20):
    conn = _connect()
    rows = [dict(zip([d[0] for d in conn.execute("SELECT * FROM indicators LIMIT 1").description], r))
            for r in conn.execute("SELECT * FROM indicators ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
    conn.close()
    return rows


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd = args[0]
    if cmd == "init":
        init_db()
    elif cmd == "calc" and len(args) >= 2:
        calc_indicator(json.loads(args[1]))
    elif cmd == "query" and len(args) >= 2:
        rows = benchmark(engineering_type=args[1])
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif cmd == "benchmark" and len(args) >= 2:
        report = benchmark_report({"specs": args[1], "cost_per_unit": float(args[2]) if len(args) > 2 else 0,
                                   "engineering_type": args[3] if len(args) > 3 else None})
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif cmd == "adjust" and len(args) >= 4:
        print(json.dumps(dynamic_adjust(int(args[1]), float(args[2]), float(args[3])),
                         ensure_ascii=False, indent=2))
    elif cmd == "list":
        print(json.dumps(list_indicators(), ensure_ascii=False, indent=2))
    else:
        print("参数不足或格式错误")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
