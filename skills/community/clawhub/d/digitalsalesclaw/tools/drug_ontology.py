#!/usr/bin/env python3
"""
药品统一本体

将 drug_products 和 pharmacy_inventory 统一为单一药品本体：

目标:
  1. 建立统一药品 ID 体系（drug_id）
  2. 关联品牌名 ↔ 通用名
  3. 标准化药品分类（ATC分类、疾病领域）
  4. 合并库存 + 商业数据于一身
  5. 支持跨表查询

本体模型:
  drug_unified: drug_id, drug_name(通用名), brand_name, dosage,规格,
                manufacturer, drug_category, atc_code, disease_areas[],
                inventory: {quantity, reorder_point, pharmacy, status}
                commercial: {price, cost, sales_trend, profit_margin}

工具:
  query_drug()      - 统一查询（支持多种ID格式）
  get_drug_profile()- 获取完整药品档案
  search_by_disease()- 按疾病领域搜索
  analyze_category() - 品类分析
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 药品名称标准化映射（种子数据）
# ─────────────────────────────────────────

BRAND_TO_GENERIC = {
    "拜糖平":      "阿卡波糖片 50mg*30",
    "格华止":      "二甲双胍片 0.5g*30",
    "拜新同":      "硝苯地平控释片 30mg*7",
    "络活喜":      "氨氯地平片 5mg*28",
    "代文":        "缬沙坦胶囊 80mg*7",
    "立普妥":      "阿托伐他汀钙片 20mg*7",
    "可特":        "瑞舒伐他汀钙片 10mg*7",
    "耐信":        "泮托拉唑钠肠溶片 40mg*14",
    "顺尔宁":      "孟鲁司特钠片 10mg*5",
    "普米克":      "布地奈德吸入剂 0.5mg*30",
    "波立维":      "硫酸氢氯吡格雷片 75mg*7",
    "诺和龙":      "格列美脲片 2mg*30",
    "艾塞那肽":    "艾塞那肽注射液",
}

GENERIC_NAME_MAP = {
    "阿卡波糖片":      {"category": "糖尿病", "atc": "A10BF", "disease": ["2型糖尿病"]},
    "二甲双胍片":      {"category": "糖尿病", "atc": "A10BA", "disease": ["2型糖尿病"]},
    "硝苯地平控释片":  {"category": "高血压", "atc": "C08CA", "disease": ["高血压", "冠心病"]},
    "氨氯地平片":      {"category": "高血压", "atc": "C08CA", "disease": ["高血压"]},
    "缬沙坦胶囊":      {"category": "高血压", "atc": "C09CA", "disease": ["高血压", "心衰"]},
    "阿托伐他汀钙片":  {"category": "高血脂", "atc": "C10AA", "disease": ["高血脂", "动脉粥样硬化"]},
    "瑞舒伐他汀钙片":  {"category": "高血脂", "atc": "C10AA", "disease": ["高血脂"]},
    "泮托拉唑钠肠溶片":{"category": "胃肠道", "atc": "A02BC", "disease": ["胃溃疡", "胃食管反流"]},
    "孟鲁司特钠片":    {"category": "呼吸系统", "atc": "R03DC", "disease": ["哮喘", "过敏性鼻炎"]},
    "布地奈德吸入剂":  {"category": "呼吸系统", "atc": "R03BA", "disease": ["哮喘", "COPD"]},
    "硫酸氢氯吡格雷片":{"category": "心血管", "atc": "B01AC", "disease": ["冠心病", "脑卒中二级预防"]},
    "格列美脲片":      {"category": "糖尿病", "atc": "A10BB", "disease": ["2型糖尿病"]},
    "胰岛素注射液":    {"category": "糖尿病", "atc": "A10A", "disease": ["1型糖尿病", "2型糖尿病"]},
    "奥司他韦胶囊":    {"category": "抗病毒", "atc": "J05AH", "disease": ["流感"]},
    "蒙脱石散":        {"category": "胃肠道", "atc": "A07BC", "disease": ["腹泻"]},
    "连花清瘟胶囊":    {"category": "中成药", "atc": "J05", "disease": ["流感", "感冒"]},
    "布洛芬混悬液":    {"category": "解热镇痛", "atc": "M01AE", "disease": ["发热", "疼痛"]},
}


# ─────────────────────────────────────────
# 数据库初始化
# ─────────────────────────────────────────

def ensure_tables(conn):
    """创建统一药品本体表"""
    # 药品统一本体（主表）
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drug_unified (
            drug_id          TEXT PRIMARY KEY,
            generic_name     TEXT NOT NULL,
            brand_name       TEXT,
            dosage           TEXT,
            specification    TEXT,
            manufacturer     TEXT,
            drug_category    TEXT,
            atc_code         TEXT,
            disease_areas    TEXT DEFAULT '[]',
            drug_form        TEXT,
            unit             TEXT,
            price            REAL,
            cost             REAL,
            profit_margin    REAL,
            status           TEXT DEFAULT 'active',
            source_ids       TEXT DEFAULT '{}',
            created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 药品关联映射
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drug_mapping (
            mapping_id    TEXT PRIMARY KEY,
            drug_id       TEXT NOT NULL,
            source_type   TEXT NOT NULL,
            source_id     TEXT NOT NULL,
            source_name   TEXT,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (drug_id) REFERENCES drug_unified(drug_id)
        )
    """)

    # 库存快照
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drug_inventory_snapshots (
            snapshot_id  TEXT PRIMARY KEY,
            drug_id      TEXT NOT NULL,
            quantity     INTEGER,
            reorder_point INTEGER,
            pharmacy     TEXT,
            status       TEXT,
            stock_ratio  REAL,
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_unified_category ON drug_unified(drug_category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_unified_atc ON drug_unified(atc_code)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_mapping_source ON drug_mapping(source_type, source_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inv_drug ON drug_inventory_snapshots(drug_id)")


def build_unified_ontology(conn, dry_run=False) -> dict:
    """
    从 drug_products + pharmacy_inventory 构建统一本体
    运行一次即可（幂等）
    """
    ensure_tables(conn)

    # 1. 从 pharmacy_inventory 构建基础本体
    inv_rows = conn.execute("SELECT * FROM pharmacy_inventory").fetchall()
    inv_cols = [d[1] for d in conn.execute("PRAGMA table_info(pharmacy_inventory)").fetchall()]

    mapped = 0
    for r in inv_rows:
        row = dict(zip(inv_cols, r))
        pid = row["product_id"]
        name = row["product_name"]

        # 解析通用名
        generic_name = name
        for brand, generic in BRAND_TO_GENERIC.items():
            if brand in name:
                generic_name = generic
                break

        # 查找分类信息
        cat_info = {"category": "其他", "atc": "", "disease": []}
        for key, info in GENERIC_NAME_MAP.items():
            if key in generic_name:
                cat_info = info
                break

        # 解析规格
        dosage, spec = _parse_dosage_spec(name)

        drug_id = f"DRG-{pid}"

        source_ids = json.dumps({"pharmacy": pid}, ensure_ascii=False)

        drug_data = (
            drug_id,
            generic_name,
            None,  # brand_name
            dosage,
            spec,
            None,  # manufacturer
            cat_info["category"],
            cat_info["atc"],
            json.dumps(cat_info["disease"], ensure_ascii=False),
            None,  # drug_form
            None,  # unit
            None,  # price
            None,  # cost
            None,  # profit_margin
            "active",
            source_ids,
        )

        if not dry_run:
            conn.execute("""
                INSERT OR IGNORE INTO drug_unified
                (drug_id, generic_name, brand_name, dosage, specification,
                 manufacturer, drug_category, atc_code, disease_areas,
                 drug_form, unit, price, cost, profit_margin, status, source_ids)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, drug_data)

            # 映射
            conn.execute("""
                INSERT OR IGNORE INTO drug_mapping
                (mapping_id, drug_id, source_type, source_id, source_name)
                VALUES (?, ?, ?, ?, ?)
            """, (f"MAP-{pid}", drug_id, "pharmacy_inventory", pid, name))

            # 库存快照
            snap_id = f"SNAP-{pid}-{row['last_restocked'][:10].replace('-','')}" if row['last_restocked'] else f"SNAP-{pid}"
            ratio = row["quantity"] / row["reorder_point"] if row["reorder_point"] else 999
            conn.execute("""
                INSERT OR IGNORE INTO drug_inventory_snapshots
                (snapshot_id, drug_id, quantity, reorder_point, pharmacy, status, stock_ratio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (snap_id, drug_id, row["quantity"], row["reorder_point"],
                  row["pharmacy"], row["status"], round(ratio, 2)))

        mapped += 1

    # 2. 从 drug_products 丰富本体（价格、成本、销售趋势）
    comm_rows = conn.execute("SELECT * FROM drug_products").fetchall()
    comm_cols = [d[1] for d in conn.execute("PRAGMA table_info(drug_products)").fetchall()]

    enriched = 0
    for r in comm_rows:
        row = dict(zip(comm_cols, r))
        sid = row["product_id"]
        name = row["name"]
        category = row["category"]

        # 查找对应 pharmacy_inventory ID
        mapped_pid = None
        for brand, generic in BRAND_TO_GENERIC.items():
            if brand in name:
                # 找对应的 pharmacy product
                inv_match = conn.execute(
                    "SELECT product_id FROM pharmacy_inventory WHERE product_name LIKE ?",
                    (f"%{generic.split()[0]}%",)
                ).fetchone()
                if inv_match:
                    mapped_pid = inv_match[0]
                break

        drug_id = f"DRG-{mapped_pid}" if mapped_pid else f"DRG-COM-{sid}"

        # 找通用名
        generic_name = name
        for brand, generic in BRAND_TO_GENERIC.items():
            if brand in name:
                generic_name = generic
                break

        if not mapped_pid:
            # 没有 pharmacy 对应，创建独立条目
            cat_info = GENERIC_NAME_MAP.get(generic_name.split()[0], {"category": category, "atc": "", "disease": []})
            drug_data = (
                drug_id,
                generic_name,
                name,
                None, None, None,
                category,
                cat_info["atc"],
                json.dumps(cat_info["disease"], ensure_ascii=False),
                None, None,
                row["price"],
                row["cost"],
                row["profit_margin"],
                "active",
                json.dumps({"commercial": sid}, ensure_ascii=False),
            )
            if not dry_run:
                conn.execute("""
                    INSERT OR IGNORE INTO drug_unified
                    (drug_id, generic_name, brand_name, dosage, specification,
                     manufacturer, drug_category, atc_code, disease_areas,
                     drug_form, unit, price, cost, profit_margin, status, source_ids)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, drug_data)

                conn.execute("""
                    INSERT OR IGNORE INTO drug_mapping
                    (mapping_id, drug_id, source_type, source_id, source_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (f"MAP-C{sid}", drug_id, "drug_products", sid, name))

        else:
            # 更新已有条目
            if not dry_run:
                conn.execute("""
                    UPDATE drug_unified
                    SET brand_name = ?, price = ?, cost = ?, profit_margin = ?,
                        source_ids = ?
                    WHERE drug_id = ?
                """, (
                    name, row["price"], row["cost"], row["profit_margin"],
                    json.dumps({"pharmacy": mapped_pid, "commercial": sid}, ensure_ascii=False),
                    drug_id
                ))

                # 也建一条 commercial 映射
                conn.execute("""
                    INSERT OR IGNORE INTO drug_mapping
                    (mapping_id, drug_id, source_type, source_id, source_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (f"MAP-C{sid}", drug_id, "drug_products", sid, name))

        enriched += 1

    if not dry_run:
        conn.commit()

    return {
        "mapped_from_inventory": mapped,
        "enriched_from_commercial": enriched,
        "message": f"✅ 药品本体构建完成: {mapped} 条库存记录 + {enriched} 条商业记录已统一",
    }


def _parse_dosage_spec(name: str) -> tuple:
    """从药品名解析剂量和规格"""
    # 匹配 0.5g, 50mg, 300IU 等
    dose_pattern = r"(\d+\.?\d*)\s*(g|mgs?|IU|ml|mg|%)"
    m = re.search(dose_pattern, name, re.IGNORECASE)
    dosage = m.group(1) + m.group(2) if m else None

    # 匹配 *30, *7 等包装规格
    spec_pattern = r"\*(\d+)"
    s = re.search(spec_pattern, name)
    spec = f"*{s.group(1)}" if s else None

    return dosage, spec


# ─────────────────────────────────────────
# 查询接口
# ─────────────────────────────────────────

def query_drug(
    query: str = None,
    drug_id: str = None,
    source_id: str = None,
    source_type: str = None,
    category: str = None,
    disease: str = None,
    conn=None,
) -> dict:
    """
    统一药品查询入口
    支持: drug_id / source_id / 通用名/品牌名关键词 / category / disease
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        sql = "SELECT DISTINCT d.* FROM drug_unified d WHERE 1=1"
        params = []

        if drug_id:
            sql += " AND d.drug_id = ?"
            params.append(drug_id)
        elif source_id:
            sql += """
                AND d.drug_id IN (
                    SELECT drug_id FROM drug_mapping
                    WHERE source_id = ? AND source_type = ?
                )
            """
            params.extend([source_id, source_type or "pharmacy_inventory"])
        elif query:
            sql += " AND (d.generic_name LIKE ? OR d.brand_name LIKE ? OR d.drug_id LIKE ?)"
            q = f"%{query}%"
            params.extend([q, q, q])
        elif category:
            sql += " AND d.drug_category = ?"
            params.append(category)
        elif disease:
            sql += " AND d.disease_areas LIKE ?"
            params.append(f"%{disease}%")

        sql += " ORDER BY d.drug_category, d.generic_name"
        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM drug_unified LIMIT 0").description]
        drugs = [dict(zip(cols, r)) for r in rows]

        result = []
        for drug in drugs:
            # 补充库存信息
            inv_rows = conn.execute("""
                SELECT * FROM drug_inventory_snapshots
                WHERE drug_id = ? ORDER BY created_at DESC LIMIT 1
            """, (drug["drug_id"],)).fetchall()
            if inv_rows:
                inv_cols = [d[0] for d in conn.execute("SELECT * FROM drug_inventory_snapshots LIMIT 0").description]
                drug["inventory"] = dict(zip(inv_cols, inv_rows[0]))

            # 补充映射
            maps = conn.execute("""
                SELECT * FROM drug_mapping WHERE drug_id = ?
            """, (drug["drug_id"],)).fetchall()
            drug["mappings"] = [dict(m) for m in maps]

            result.append(drug)

        return {
            "query": query or drug_id or source_id or category or disease or "all",
            "count": len(result),
            "drugs": result,
        }

    finally:
        if own_conn:
            conn.close()


def get_drug_profile(drug_id: str = None, source_id: str = None, source_type: str = None, conn=None) -> dict:
    """获取完整药品档案"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        if drug_id:
            d = conn.execute("SELECT * FROM drug_unified WHERE drug_id = ?", (drug_id,)).fetchone()
        elif source_id:
            d = conn.execute("""
                SELECT d.* FROM drug_unified d
                JOIN drug_mapping m ON d.drug_id = m.drug_id
                WHERE m.source_id = ? AND m.source_type = ?
            """, (source_id, source_type or "pharmacy_inventory")).fetchone()
        else:
            return {"error": "drug_id or source_id required"}

        if not d:
            return {"error": "Drug not found"}

        cols = [c[0] for c in conn.execute("SELECT * FROM drug_unified LIMIT 0").description]
        drug = dict(zip(cols, d))
        drug["disease_areas"] = json.loads(drug.get("disease_areas") or "[]")
        drug["source_ids"] = json.loads(drug.get("source_ids") or "{}")

        # 库存历史
        inv_rows = conn.execute("""
            SELECT * FROM drug_inventory_snapshots
            WHERE drug_id = ? ORDER BY created_at DESC LIMIT 30
        """, (drug["drug_id"],)).fetchall()
        inv_cols = [c[0] for c in conn.execute("SELECT * FROM drug_inventory_snapshots LIMIT 0").description]
        drug["inventory_history"] = [dict(zip(inv_cols, r)) for r in inv_rows]

        # 映射
        maps = conn.execute("""
            SELECT * FROM drug_mapping WHERE drug_id = ?
        """, (drug["drug_id"],)).fetchall()
        drug["mappings"] = [dict(m) for m in maps]

        # 关联内容数据
        content_count = conn.execute("""
            SELECT COUNT(*) FROM content_metrics m
            JOIN content_campaigns c ON m.campaign_id = c.campaign_id
            WHERE c.platform = ?
        """, (drug.get("brand_name", ""),)).fetchone()[0] or 0

        drug["content_associations"] = content_count

        # 建议
        suggestions = []
        if drug.get("inventory"):
            qty = drug["inventory"].get("quantity", 0)
            rop = drug["inventory"].get("reorder_point", 1)
            ratio = qty / rop if rop else 999
            if ratio < 0.5:
                suggestions.append(f"⚠️ 库存严重不足（{qty}/{rop}），需立即补货")
            elif ratio < 1.0:
                suggestions.append(f"⚠️ 库存偏低（{qty}/{rop}），建议补货")

        if drug.get("profit_margin"):
            margin = drug["profit_margin"]
            if margin < 0.3:
                suggestions.append(f"⚠️ 利润率较低（{margin:.0%}），考虑优化供应链")
            elif margin > 0.6:
                suggestions.append(f"✅ 利润率优秀（{margin:.0%}）")

        drug["suggestions"] = suggestions

        return drug

    finally:
        if own_conn:
            conn.close()


def search_by_disease(disease: str, conn=None) -> dict:
    """按疾病领域搜索药品"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        rows = conn.execute("""
            SELECT * FROM drug_unified
            WHERE disease_areas LIKE ?
            ORDER BY drug_category, generic_name
        """, (f"%{disease}%",)).fetchall()

        cols = [c[0] for c in conn.execute("SELECT * FROM drug_unified LIMIT 0").description]
        drugs = [dict(zip(cols, r)) for r in rows]

        for drug in drugs:
            drug["disease_areas"] = json.loads(drug.get("disease_areas") or "[]")

        by_category = defaultdict(list)
        for d in drugs:
            by_category[d["drug_category"]].append(d)

        return {
            "disease": disease,
            "total_drugs": len(drugs),
            "by_category": {k: len(v) for k, v in by_category.items()},
            "drugs": drugs,
            "suggestions": [
                f"疾病「{disease}」涉及 {len(by_category)} 个品类，共 {len(drugs)} 个药品",
                f"主要品类: {', '.join(by_category.keys())}",
            ]
        }

    finally:
        if own_conn:
            conn.close()


def analyze_category(conn=None) -> dict:
    """品类分析"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        categories = conn.execute("""
            SELECT drug_category, COUNT(*) as drug_count,
                   AVG(price) as avg_price, AVG(profit_margin) as avg_margin
            FROM drug_unified
            WHERE drug_category IS NOT NULL
            GROUP BY drug_category
        """).fetchall()

        # 库存状态汇总
        inv_stats = conn.execute("""
            SELECT du.drug_category,
                   SUM(CAST(di.quantity AS FLOAT)) as total_stock,
                   SUM(CAST(di.reorder_point AS FLOAT)) as total_rop,
                   COUNT(CASE WHEN di.quantity < di.reorder_point THEN 1 END) as low_stock_count
            FROM drug_unified du
            JOIN drug_inventory_snapshots di ON du.drug_id = di.drug_id
            GROUP BY du.drug_category
        """).fetchall()

        cat_stats = {}
        for r in categories:
            cat_stats[r["drug_category"]] = {
                "drug_count": r["drug_count"],
                "avg_price": round(r["avg_price"] or 0, 2),
                "avg_margin": round(r["avg_margin"] or 0, 3),
            }
        for r in inv_stats:
            if r["drug_category"] in cat_stats:
                total_rop = r["total_rop"] or 1
                cat_stats[r["drug_category"]].update({
                    "total_stock": r["total_stock"] or 0,
                    "low_stock_count": r["low_stock_count"] or 0,
                    "stock_ratio": round((r["total_stock"] or 0) / total_rop, 2),
                })

        return {
            "categories": cat_stats,
            "total_categories": len(cat_stats),
            "suggestions": _generate_category_suggestions(cat_stats),
        }

    finally:
        if own_conn:
            conn.close()


def _generate_category_suggestions(cat_stats: dict) -> list[str]:
    suggestions = []
    for cat, stats in cat_stats.items():
        if stats.get("low_stock_count", 0) > 0:
            suggestions.append(f"⚠️ {cat}: {stats['low_stock_count']} 个产品库存不足")
        if stats.get("avg_margin", 0) < 0.3:
            suggestions.append(f"💰 {cat} 平均利润率较低（{stats['avg_margin']:.0%}），有优化空间")

    if not suggestions:
        suggestions.append("所有品类库存和利润状况正常")

    return suggestions


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "query")

    conn = get_conn()

    try:
        ensure_tables(conn)
        conn.commit()

        if action == "build":
            result = build_unified_ontology(conn, dry_run=args.get("dry_run", False))

        elif action == "query":
            result = query_drug(
                query=args.get("query"),
                drug_id=args.get("drug_id"),
                source_id=args.get("source_id"),
                source_type=args.get("source_type"),
                category=args.get("category"),
                disease=args.get("disease"),
            )

        elif action == "profile":
            result = get_drug_profile(
                drug_id=args.get("drug_id"),
                source_id=args.get("source_id"),
                source_type=args.get("source_type"),
            )

        elif action == "search_disease":
            result = search_by_disease(args.get("disease", "糖尿病"))

        elif action == "analyze_category":
            result = analyze_category()

        else:
            result = {"error": f"Unknown action: {action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        close_conn(conn)
