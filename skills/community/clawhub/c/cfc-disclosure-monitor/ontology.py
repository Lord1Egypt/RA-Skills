#!/usr/bin/env python3
"""
ontology.py — Phase 5: 消金信披知识图谱
═══════════════════════════════════════════════════════════════
使用 SQLite 存储知识图谱，支持实体、关系查询和增量监控。

Schema:
    entities(id, type, name, props JSON, created_at)
    relations(id, from_id, to_id, relation_type, props JSON, created_at)

用法：
    python3 ontology.py --init                      # 初始化数据库
    python3 ontology.py --add "蚂蚁消费金融"          # 添加公司实体
    python3 ontology.py --query "蚂蚁消费金融"        # 查询公司所有信息
    python3 ontology.py --query "蚂蚁消费金融" --relation PARTNERS_WITH
    python3 ontology.py --date-range 2026-01-01 2026-04-11
    python3 ontology.py --changes-since 2026-04-01    # 增量变化
    python3 ontology.py --export-cypher > neo4j.cypher  # 导出 Neo4j
    python3 ontology.py --stats                       # 统计信息

集成（与 Phase 4 parser.py）：
    from ontology import OntologyGraph, parse_and_index
    parse_and_index("蚂蚁消费金融", "2026-04-11")
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Any

# ── 路径设置 ─────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
DB_PATH = SKILL_DIR / "ontology.db"
PARSER_PATH = SKILL_DIR / "parser.py"

# ── Schema SQL ────────────────────────────────────────────────────────────────
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entities (
    id          TEXT PRIMARY KEY,
    type        TEXT NOT NULL,         -- Company|Regulation|Announcement|Metric|PartnerRelation
    name        TEXT NOT NULL,
    props       TEXT DEFAULT '{}',     -- JSON
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);

CREATE TABLE IF NOT EXISTS relations (
    id              TEXT PRIMARY KEY,
    from_id         TEXT NOT NULL,
    to_id           TEXT NOT NULL,
    relation_type   TEXT NOT NULL,
    props           TEXT DEFAULT '{}', -- JSON
    created_at      TEXT NOT NULL,
    FOREIGN KEY (from_id) REFERENCES entities(id),
    FOREIGN KEY (to_id)   REFERENCES entities(id)
);
CREATE INDEX IF NOT EXISTS idx_relations_from  ON relations(from_id);
CREATE INDEX IF NOT EXISTS idx_relations_to    ON relations(to_id);
CREATE INDEX IF NOT EXISTS idx_relations_type  ON relations(relation_type);
"""

# ── 关系类型常量 ─────────────────────────────────────────────────────────────
REL_ISSUED_BY     = "ISSUED_BY"       # 监管文件 → 发布机构
REL_CITES         = "CITES"           # 公告引用监管文件
REL_ANNOUNCES     = "ANNOUNCES"       # 公司发布公告
REL_HAS_METRIC    = "HAS_METRIC"      # 公司有指标
REL_PARTNERS_WITH = "PARTNERS_WITH"   # 公司间合作
REL_SUBSIDIARY_OF = "SUBSIDIARY_OF"   # 子公司关系
REL_COMPETES_WITH = "COMPETES_WITH"   # 竞争关系
REL_REGULATES     = "REGULATES"       # 监管文件监管公司
REL_REPORTS_TO    = "REPORTS_TO"      # 下属机构


# ─────────────────────────────────────────────────────────────────────────────
#  OntologyGraph
# ─────────────────────────────────────────────────────────────────────────────

class OntologyGraph:
    """
    SQLite-backed 知识图谱。

    支持的实体类型：
        Company, Regulation, Announcement, Metric, PartnerRelation
    支持的关系类型：
        ISSUED_BY, CITES, ANNOUNCES, HAS_METRIC, PARTNERS_WITH,
        SUBSIDIARY_OF, COMPETES_WITH, REGULATES, REPORTS_TO
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """初始化表结构"""
        with self._conn() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # ── 实体操作 ─────────────────────────────────────────────────────────────

    def add_entity(self, entity_type: str, name: str, props: dict = None) -> str:
        """
        添加实体，返回 entity_id。
        如果同名同类型已存在，返回已有 ID（upsert）。
        """
        props = props or {}
        props_json = json.dumps(props, ensure_ascii=False)

        with self._conn() as conn:
            # 检查是否存在
            row = conn.execute(
                "SELECT id FROM entities WHERE type=? AND name=?",
                (entity_type, name)
            ).fetchone()
            if row:
                # 更新 props
                conn.execute(
                    "UPDATE entities SET props=? WHERE id=?",
                    (props_json, row[0])
                )
                conn.commit()
                return row[0]

            entity_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO entities (id, type, name, props, created_at) VALUES (?,?,?,?,?)",
                (entity_id, entity_type, name, props_json, self._now())
            )
            conn.commit()
            return entity_id

    def get_entity(self, entity_id: str) -> Optional[dict]:
        """按 ID 查询实体"""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id, type, name, props, created_at FROM entities WHERE id=?",
                (entity_id,)
            ).fetchone()
            if not row:
                return None
            return {
                "id": row[0], "type": row[1], "name": row[2],
                "props": json.loads(row[3]), "created_at": row[4]
            }

    def find_entities(self, entity_type: str = None, name_pattern: str = None) -> list[dict]:
        """按类型和名称模式查询实体"""
        q = "SELECT id, type, name, props, created_at FROM entities WHERE 1=1"
        params = []
        if entity_type:
            q += " AND type=?"
            params.append(entity_type)
        if name_pattern:
            q += " AND name LIKE ?"
            params.append(f"%{name_pattern}%")
        with self._conn() as conn:
            rows = conn.execute(q, params).fetchall()
            return [
                {"id": r[0], "type": r[1], "name": r[2],
                 "props": json.loads(r[3]), "created_at": r[4]}
                for r in rows
            ]

    # ── 关系操作 ─────────────────────────────────────────────────────────────

    def add_relation(self, from_id: str, to_id: str, relation_type: str,
                     props: dict = None) -> str:
        """
        添加关系，返回 relation_id。
        重复关系不会创建（from_id + to_id + relation_type 唯一）。
        """
        props = props or {}

        with self._conn() as conn:
            # 检查重复
            existing = conn.execute(
                "SELECT id FROM relations WHERE from_id=? AND to_id=? AND relation_type=?",
                (from_id, to_id, relation_type)
            ).fetchone()
            if existing:
                return existing[0]

            rel_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO relations (id, from_id, to_id, relation_type, props, created_at) "
                "VALUES (?,?,?,?,?,?)",
                (rel_id, from_id, to_id, relation_type,
                 json.dumps(props, ensure_ascii=False), self._now())
            )
            conn.commit()
            return rel_id

    def get_relations(self, entity_id: str = None, direction: str = "both",
                      relation_type: str = None) -> list[dict]:
        """
        查询关系。
        direction: "out" (from_id=entity_id), "in" (to_id=entity_id), "both"
        """
        q = ("SELECT r.id, r.from_id, r.to_id, r.relation_type, r.props, r.created_at, "
             "e_from.name, e_to.name "
             "FROM relations r "
             "JOIN entities e_from ON r.from_id=e_from.id "
             "JOIN entities e_to   ON r.to_id=e_to.id "
             "WHERE 1=1")
        params = []
        if entity_id:
            if direction == "out":
                q += " AND r.from_id=?"
                params.append(entity_id)
            elif direction == "in":
                q += " AND r.to_id=?"
                params.append(entity_id)
            else:  # both
                q += " AND (r.from_id=? OR r.to_id=?)"
                params.extend([entity_id, entity_id])
        if relation_type:
            q += " AND r.relation_type=?"
            params.append(relation_type)
        q += " ORDER BY r.created_at DESC"

        with self._conn() as conn:
            rows = conn.execute(q, params).fetchall()
            return [
                {"id": r[0], "from_id": r[1], "to_id": r[2],
                 "relation_type": r[3], "props": json.loads(r[4]),
                 "created_at": r[5],
                 "from_name": r[6], "to_name": r[7]}
                for r in rows
            ]

    # ── 快捷查询 ─────────────────────────────────────────────────────────────

    def query_company(self, name: str) -> dict:
        """
        查询公司所有信息：基本信息 + 所有关系 + 所有公告。
        """
        # 找公司实体
        companies = self.find_entities(entity_type="Company",
                                        name_pattern=name)
        if not companies:
            return {"error": f"未找到公司: {name}"}

        company = companies[0]
        cid = company["id"]

        # 所有关系
        relations = self.get_relations(cid, direction="both")

        # 所有公告（ANNOUNCES 关系）
        announcements = []
        for rel in relations:
            if rel["relation_type"] == REL_ANNOUNCES:
                ann = self.get_entity(rel["to_id"])
                if ann:
                    announcements.append(ann)

        # 所有指标（HAS_METRIC）
        metrics = []
        for rel in relations:
            if rel["relation_type"] == REL_HAS_METRIC:
                m = self.get_entity(rel["to_id"])
                if m:
                    metrics.append(m)

        return {
            "company": company,
            "relations": relations,
            "announcements": sorted(announcements, key=lambda x: x.get("props", {}).get("date", ""), reverse=True),
            "metrics": metrics,
        }

    def query_related(self, company: str, relation_type: str = None) -> list[dict]:
        """
        按关系类型查询公司关联信息。
        例如：query_related("蚂蚁消费金融", "PARTNERS_WITH")
        返回关联公司列表。
        """
        companies = self.find_entities(entity_type="Company", name_pattern=company)
        if not companies:
            return []

        cid = companies[0]["id"]
        relations = self.get_relations(cid, direction="both", relation_type=relation_type)

        results = []
        for rel in relations:
            # 找对方实体
            other_id = rel["from_id"] if rel["to_id"] == cid else rel["to_id"]
            other = self.get_entity(other_id)
            if other:
                results.append({
                    "relation_type": rel["relation_type"],
                    "related": other,
                    "props": rel["props"],
                })
        return results

    def query_by_date_range(self, start: str, end: str) -> list[dict]:
        """
        按日期范围查询公告。
        返回 Announcement 实体列表。
        日期通过 props.date 字段过滤。
        """
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT e.id, e.type, e.name, e.props, e.created_at
                   FROM entities e
                   WHERE e.type='Announcement'
                   ORDER BY e.props DESC"""
            ).fetchall()
            results = []
            for r in rows:
                props = json.loads(r[3])
                ann_date = props.get("date", "")[:10]  # YYYY-MM-DD
                if ann_date and start <= ann_date <= end:
                    results.append({
                        "id": r[0], "type": r[1], "name": r[2],
                        "props": props, "created_at": r[4]
                    })
            return results

    def get_changes_since(self, since_date: str) -> list[dict]:
        """
        获取增量变化（用于监控）。
        返回 since_date 之后新添加或更新的公告。
        """
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT e.id, e.type, e.name, e.props, e.created_at
                   FROM entities e
                   WHERE e.type='Announcement'
                   ORDER BY e.created_at DESC
                   LIMIT 200"""
            ).fetchall()
            changes = []
            for r in rows:
                props = json.loads(r[3])
                ann_date = props.get("date", "")
                if ann_date and ann_date[:10] >= since_date:
                    changes.append({
                        "id": r[0], "type": r[1], "name": r[2],
                        "props": props, "created_at": r[4],
                        "change_type": "new" if ann_date[:10] >= since_date else "updated"
                    })
            return changes

    # ── 公告写入 ─────────────────────────────────────────────────────────────

    def add_announcement(self, parsed: dict) -> str:
        """
        将解析后的 AnnouncementSchema 写入图谱。

        自动创建：
        1. Company 实体（如果不存在）
        2. Announcement 实体
        3. ANNOUNCES 关系（Company → Announcement）
        4. CITES 关系（Announcement → Regulation）
        5. Metric 实体 + HAS_METRIC 关系
        6. PartnerRelation 实体 + PARTNERS_WITH 关系
        7. related_companies → 提取为 CITES 或 COMPETES_WITH
        """
        company_name = parsed.get("company", "")
        title = parsed.get("title", "")
        ann_date = parsed.get("date", "")
        category = parsed.get("category", "重要公告")
        importance = parsed.get("importance", "medium")
        url = parsed.get("url", "")
        content_hash = hashlib.md5((title + ann_date + url).encode()).hexdigest()[:16]

        if not company_name or not title:
            raise ValueError("parsed 必须包含 company 和 title 字段")

        # ── 创建/获取 Company ────────────────────────────────────────────────
        company_id = self.add_entity("Company", company_name, {
            "source": "announcement_parser"
        })

        # ── 创建 Announcement ───────────────────────────────────────────────
        ann_props = {
            "title": title,
            "date": ann_date,
            "category": category,
            "importance": importance,
            "content_hash": content_hash,
            "url": url,
            "sentiment": parsed.get("sentiment", "neutral"),
            "summary": parsed.get("summary", ""),
            "highlights": parsed.get("highlights", []),
        }
        ann_id = self.add_entity("Announcement", title, ann_props)

        # ── ANNOUNCES 关系 ────────────────────────────────────────────────────
        self.add_relation(company_id, ann_id, REL_ANNOUNCES, {
            "date": ann_date, "category": category
        })

        # ── 监管文件 CITES ────────────────────────────────────────────────────
        for reg_name in parsed.get("regulations", []):
            reg_id = self.add_entity("Regulation", reg_name, {"source": "auto_extracted"})
            self.add_relation(ann_id, reg_id, REL_CITES)

        # ── 指标 HAS_METRIC ──────────────────────────────────────────────────
        for metric_type, metric_value in parsed.get("metrics", {}).items():
            metric_id = self.add_entity("Metric", f"{company_name}_{metric_type}", {
                "metric_type": metric_type,
                "value": str(metric_value),
                "unit": self._extract_unit(str(metric_value)),
                "report_date": ann_date,
                "source_announcement_id": ann_id,
            })
            self.add_relation(company_id, metric_id, REL_HAS_METRIC, {
                "report_date": ann_date
            })

        # ── 合作机构 PARTNERS_WITH ───────────────────────────────────────────
        for partner_name in parsed.get("partners", []):
            partner_id = self.add_entity("Company", partner_name, {
                "source": "partner_extracted", "type_detail": "partner"
            })
            self.add_relation(company_id, partner_id, REL_PARTNERS_WITH, {
                "start_date": ann_date,
                "source_announcement_id": ann_id,
            })

        # ── 相关消金公司 ─────────────────────────────────────────────────────
        for other_name in parsed.get("related_companies", []):
            other_id = self.add_entity("Company", other_name, {
                "source": "related_company"
            })
            # 如果是同一类消金公司，记录为关联（竞争/合作均可能）
            self.add_relation(company_id, other_id, REL_COMPETES_WITH, {
                "source_announcement_id": ann_id
            })

        return ann_id

    def _extract_unit(self, value_str: str) -> str:
        """从值字符串中提取单位"""
        if "亿" in value_str:
            return "亿元"
        if "万" in value_str:
            return "万元"
        if "%" in value_str:
            return "%"
        if "元" in value_str:
            return "元"
        return ""

    # ── 导出 ─────────────────────────────────────────────────────────────────

    def export_cypher(self) -> str:
        """
        导出为 Cypher 查询格式（可导入 Neo4j）。
        """
        lines = ["// Neo4j Cypher Export from cfc-disclosure-monitor ontology",
                 "// Generated: " + datetime.now().isoformat(),
                 ""]

        with self._conn() as conn:
            # 导出节点
            entities = conn.execute("SELECT id, type, name, props FROM entities").fetchall()
            for eid, etype, ename, eprops in entities:
                props = json.loads(eprops)
                props_str = ", ".join(
                    f"{k}: {repr(str(v))}" for k, v in props.items()
                )
                props_str = f" {{{props_str}}}" if props_str else ""
                label = etype.capitalize()
                cypher = f"CREATE (n:{label} {{id: {repr(eid)}, name: {repr(ename)}{props_str}}})"
                lines.append(cypher)

            lines.append("")
            # 导出关系
            rels = conn.execute(
                "SELECT from_id, to_id, relation_type, props FROM relations"
            ).fetchall()
            for rid_from, rid_to, rtype, rprops in rels:
                props = json.loads(rprops)
                props_str = ", ".join(
                    f"{k}: {repr(str(v))}" for k, v in props.items()
                )
                props_str = f" {{{props_str}}}" if props_str else ""
                lines.append(
                    f"MATCH (a), (b) WHERE a.id={repr(rid_from)} AND b.id={repr(rid_to)} "
                    f"CREATE (a)-[r:{rtype}{props_str}]->(b)"
                )

        return "\n".join(lines)

    def export_json(self) -> str:
        """导出完整图谱为 JSON"""
        with self._conn() as conn:
            entities = conn.execute("SELECT id, type, name, props, created_at FROM entities").fetchall()
            relations = conn.execute(
                "SELECT id, from_id, to_id, relation_type, props, created_at FROM relations"
            ).fetchall()
        return json.dumps({
            "entities": [
                {"id": r[0], "type": r[1], "name": r[2],
                 "props": json.loads(r[3]), "created_at": r[4]}
                for r in entities
            ],
            "relations": [
                {"id": r[0], "from_id": r[1], "to_id": r[2],
                 "relation_type": r[3], "props": json.loads(r[4]), "created_at": r[5]}
                for r in relations
            ],
        }, ensure_ascii=False, indent=2)

    def stats(self) -> dict:
        """图谱统计"""
        with self._conn() as conn:
            entity_counts = conn.execute(
                "SELECT type, COUNT(*) FROM entities GROUP BY type"
            ).fetchall()
            rel_counts = conn.execute(
                "SELECT relation_type, COUNT(*) FROM relations GROUP BY relation_type"
            ).fetchall()
            total_e = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            total_r = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
        return {
            "total_entities": total_e,
            "total_relations": total_r,
            "by_entity_type": {r[0]: r[1] for r in entity_counts},
            "by_relation_type": {r[0]: r[1] for r in rel_counts},
        }

    def clear(self):
        """清空图谱（慎用）"""
        with self._conn() as conn:
            conn.execute("DELETE FROM relations")
            conn.execute("DELETE FROM entities")
            conn.commit()
        print("🗑️ 图谱已清空")


# ─────────────────────────────────────────────────────────────────────────────
#  与 Phase 4 集成
# ─────────────────────────────────────────────────────────────────────────────

def parse_and_index(company: str, date_str: str = None,
                    use_llm: bool = False, dry_run: bool = False) -> list:
    """
    解析 + 索引一站式完成。

    流程：
    1. 加载 announcements.json
    2. 尝试加载每条的 fulltext.txt
    3. 调用 parser.parse_announcement
    4. 调用 ontology.add_announcement

    Args:
        company: 公司名称
        date_str: 采集日期
        use_llm: 是否使用 LLM（默认 False，避免 API 不可用时报错）
        dry_run: True=只解析不写入图谱

    Returns:
        list[dict] 解析结果
    """
    sys.path.insert(0, str(SKILL_DIR))

    try:
        from parser import (
            load_announcements, load_content, parse_announcement,
            ROOT_DIR, TODAY_STR
        )
    except ImportError as e:
        print(f"❌ 无法导入 parser.py: {e}")
        raise

    date_str = date_str or TODAY_STR
    announcements = load_announcements(company, date_str)
    if not announcements:
        print(f"⚠️ 无公告数据: {company} @ {date_str}")
        return []

    print(f"▶ {company}: {len(announcements)} 条公告待解析")

    if dry_run:
        from parser import parse_batch
        items = []
        for ann in announcements:
            meta = {
                "company": company,
                "title": ann.get("title", ""),
                "date": ann.get("date", ""),
                "category": ann.get("category", "重要公告"),
                "url": ann.get("url", ""),
            }
            text = load_content(company, ann.get("url", ""), date_str)
            items.append({"meta": meta, "text": text})
        return parse_batch(items, company, use_llm=use_llm)

    # 解析
    parsed_results = []
    for ann in announcements:
        meta = {
            "company": company,
            "title": ann.get("title", ""),
            "date": ann.get("date", ""),
            "category": ann.get("category", "重要公告"),
            "url": ann.get("url", ""),
        }
        text = load_content(company, ann.get("url", ""), date_str)
        try:
            result = parse_announcement(text, meta, use_llm=use_llm)
            parsed_results.append(result)
        except Exception as e:
            print(f"  ❌ 解析失败: {meta.get('title','')}: {e}")

    # 写入图谱
    graph = OntologyGraph()
    indexed_count = 0
    for parsed in parsed_results:
        try:
            graph.add_announcement(parsed)
            indexed_count += 1
        except Exception as e:
            print(f"  ❌ 索引失败: {parsed.get('title','')}: {e}")

    print(f"✅ {company}: {indexed_count}/{len(parsed_results)} 条已索引")
    return parsed_results


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="消金信披知识图谱 — Phase 5")
    p.add_argument("--init", action="store_true", help="初始化数据库")
    p.add_argument("--add", metavar="NAME", help="添加公司实体")
    p.add_argument("--query", metavar="NAME", help="查询公司所有信息")
    p.add_argument("--relation", metavar="TYPE",
                   help="按关系类型过滤（配合 --query）")
    p.add_argument("--date-range", nargs=2, metavar=("START", "END"),
                   help="按日期范围查询")
    p.add_argument("--changes-since", metavar="DATE",
                   help="获取增量变化")
    p.add_argument("--export-cypher", action="store_true",
                   help="导出 Cypher 格式")
    p.add_argument("--export-json", action="store_true",
                   help="导出 JSON 格式")
    p.add_argument("--stats", action="store_true", help="图谱统计")
    p.add_argument("--clear", action="store_true", help="清空图谱（慎用）")
    p.add_argument("--parse-and-index", action="store_true",
                   help="解析+索引（需配合 --company --date）")
    p.add_argument("--company", help="公司名称")
    p.add_argument("--date", default=None, help="采集日期")
    p.add_argument("--llm", action="store_true", default=False, help="使用 LLM 模式")
    p.add_argument("--output", help="输出文件路径")
    return p.parse_args()


def main():
    args = parse_args()
    graph = OntologyGraph()

    # 初始化
    if args.init:
        print("🔧 初始化数据库...")
        graph._init_db()
        print(f"✅ 数据库已初始化: {graph.db_path}")
        return

    # 清空
    if args.clear:
        confirm = input("⚠️ 确定清空图谱？(yes/no): ")
        if confirm.lower() == "yes":
            graph.clear()
        return

    # 统计
    if args.stats:
        stats = graph.stats()
        print("╔══ 图谱统计 ══╗")
        print(f"  实体总数: {stats['total_entities']}")
        print(f"  关系总数: {stats['total_relations']}")
        print("  按类型：")
        for k, v in stats["by_entity_type"].items():
            print(f"    {k}: {v}")
        print("  关系类型：")
        for k, v in stats["by_relation_type"].items():
            print(f"    {k}: {v}")
        return

    # 导出 Cypher
    if args.export_cypher:
        cypher = graph.export_cypher()
        if args.output:
            Path(args.output).write_text(cypher, encoding="utf-8")
            print(f"💾 已导出 Cypher: {args.output}")
        else:
            print(cypher)
        return

    # 导出 JSON
    if args.export_json:
        j = graph.export_json()
        if args.output:
            Path(args.output).write_text(j, encoding="utf-8")
            print(f"💾 已导出 JSON: {args.output}")
        else:
            print(j)
        return

    # 简单添加实体
    if args.add:
        eid = graph.add_entity("Company", args.add, {"source": "cli"})
        print(f"✅ 添加实体: {args.add} (id={eid})")
        return

    # 查询公司
    if args.query:
        if args.relation:
            # 查指定关系类型
            related = graph.query_related(args.query, args.relation)
            print(f"╔══ {args.query} 的 {args.relation} 关系 ══╗")
            if not related:
                print("  （无数据）")
            for r in related:
                print(f"  [{r['relation_type']}] {r['related']['name']} | {r['props']}")
        else:
            # 完整查询
            info = graph.query_company(args.query)
            print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    # 日期范围查询
    if args.date_range:
        start, end = args.date_range
        results = graph.query_by_date_range(start, end)
        print(f"╔══ {start} ~ {end} 公告 ({len(results)} 条) ══╗")
        for r in results:
            props = r.get("props", {})
            print(f"  [{props.get('date','?')}] {props.get('category','?')} | {r['name'][:60]}")
        return

    # 增量变化
    if args.changes_since:
        changes = graph.get_changes_since(args.changes_since)
        print(f"╔══ {args.changes_since} 后的变化 ({len(changes)} 条) ══╗")
        for c in changes:
            props = c.get("props", {})
            print(f"  [{props.get('date','?')}] [{c.get('change_type','?')}] {props.get('category','?')} | {c['name'][:60]}")
        return

    # 解析 + 索引
    if args.parse_and_index:
        if not args.company:
            print("❌ --parse-and-index 需要 --company")
            sys.exit(1)
        parse_and_index(args.company, args.date, use_llm=args.llm)
        return

    # 无参数
    if len(sys.argv) == 1:
        stats = graph.stats()
        print(f"""╔══ 消金信披知识图谱 ══╗
  数据库: {graph.db_path}
  实体: {stats['total_entities']} | 关系: {stats['total_relations']}
╠══════════════════════════════╣
用法:
  --init                  初始化
  --add NAME              添加公司实体
  --query NAME            查询公司完整信息
  --query NAME --relation TYPE   按关系类型查询
  --date-range YYYY-MM-DD YYYY-MM-DD  日期范围查询
  --changes-since DATE    增量监控
  --export-cypher         导出 Neo4j 格式
  --export-json            导出 JSON
  --stats                 图谱统计
  --parse-and-index --company NAME --date DATE  解析+索引
╚══════════════════════════════╝""")
        return

    print("❌ 未知参数组合")
    sys.exit(1)


if __name__ == "__main__":
    main()
