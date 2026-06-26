#!/usr/bin/env python3
"""
Phase 1.4 - 医生-KOL 统一身份模型

问题: 同一个医生可能既是线下专家（doctor_profiles）又是新媒体KOL（kol_profiles），
      但两张表独立，没有关联。

解决方案:
  1. 创建 unified_identity 表，统一管理所有 KOL 和医生身份
  2. 创建 identity_mapping 表，关联 kol_id ↔ doctor_id
  3. 匹配合并规则（同名、医院相同 → 可能是同一人）
  4. 提供统一查询接口

本体模型:
  unified_identity: identity_id (主键), identity_type (kol|doctor|both),
    name, gender, specialty, hospital, title, department,
    influence_level (S/A/B/C), influence_score, platform[], tags[],
    kol_data: {kol_id, platform, fans_count, level}
    doctor_data: {doctor_id, hospital, region, city}
"""

import sys
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from collections import defaultdict

SKILL_DIR = Path(__file__).parent.parent


def ensure_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS unified_identity (
            identity_id  TEXT PRIMARY KEY,
            identity_type TEXT NOT NULL,
            name         TEXT NOT NULL,
            gender       TEXT,
            specialty    TEXT,
            hospital     TEXT,
            title        TEXT,
            department   TEXT,
            region       TEXT,
            city         TEXT,
            influence_level TEXT,
            influence_score REAL,
            tags         TEXT DEFAULT '[]',
            platform     TEXT DEFAULT '[]',
            kol_id       TEXT,
            doctor_id    TEXT,
            kol_data     TEXT DEFAULT '{}',
            doctor_data  TEXT DEFAULT '{}',
            merge_status TEXT DEFAULT 'manual',
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS identity_mapping (
            mapping_id   TEXT PRIMARY KEY,
            identity_id TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_id   TEXT NOT NULL,
            source_name TEXT,
            confidence  REAL DEFAULT 1.0,
            match_method TEXT DEFAULT 'manual',
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (identity_id) REFERENCES unified_identity(identity_id)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_identity_name ON unified_identity(name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_identity_hospital ON unified_identity(hospital)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_identity_kolid ON unified_identity(kol_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_identity_docid ON unified_identity(doctor_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_mapping_source ON identity_mapping(source_type, source_id)")


def build_unified_identity(conn, dry_run=False) -> dict:
    """
    构建统一身份库
    策略:
      1. 精确匹配: kol.username == doctor.name AND kol.tags 包含 hospital → same person
      2. 模糊匹配: name 相似度 > 0.85 AND hospital 相同 → high confidence
      3. 单表收录: 无法匹配的分别收录
    """
    ensure_tables(conn)

    # 读取所有 KOL
    kol_rows = conn.execute("SELECT * FROM kol_profiles").fetchall()
    kol_cols = [d[1] for d in conn.execute("PRAGMA table_info(kol_profiles)").fetchall()]
    kols = [dict(zip(kol_cols, r)) for r in kol_rows]

    # 读取所有医生
    doc_rows = conn.execute("SELECT * FROM doctor_profiles").fetchall()
    doc_cols = [d[1] for d in conn.execute("PRAGMA table_info(doctor_profiles)").fetchall()]
    docs = [dict(zip(doc_cols, r)) for r in doc_rows]

    # 建立姓名→医生列表的索引
    doc_by_name = defaultdict(list)
    for d in docs:
        doc_by_name[d["name"]].append(d)

    identity_count = 0
    mapping_count = 0

    for kol in kols:
        kol_id   = kol["kol_id"]
        kol_name = kol["username"]
        kol_tags = kol.get("tags") or ""
        kol_platform = kol.get("platform")
        kol_fans = kol.get("fans_count", 0)
        kol_level = kol.get("level", "C")

        # 尝试在医生表中找匹配
        matched_doc = None
        match_method = None
        confidence = 0.0

        # 精确匹配: 医生姓名 == kol.username，且标签包含医院
        if kol_name in doc_by_name:
            for doc in doc_by_name[kol_name]:
                doc_hosp = doc.get("hospital", "")
                if doc_hosp and doc_hosp in kol_tags:
                    matched_doc = doc
                    match_method = "exact_name_plus_hospital"
                    confidence = 1.0
                    break

        # 模糊匹配: 名字相似度高
        if not matched_doc:
            best_sim = 0
            best_doc = None
            for d in docs:
                sim = SequenceMatcher(None, kol_name, d['name']).ratio()
                if sim > best_sim and sim >= 85:
                    best_sim = sim
                    best_doc = d
            if best_doc:
                matched_doc = best_doc
                match_method = "fuzzy_name"
                confidence = best_sim / 100.0

        # 构建 identity
        if matched_doc:
            identity_id = f"ID-{matched_doc['doctor_id']}"
            identity_type = "both"
            doc_id = matched_doc["doctor_id"]
            kol_id_out = kol_id
            merge_status = "auto_merged"
            kol_data = json.dumps({
                "kol_id": kol_id, "platform": kol_platform,
                "fans_count": kol_fans, "level": kol_level,
                "tags": kol_tags,
            }, ensure_ascii=False)
            doc_data = json.dumps(dict(matched_doc), ensure_ascii=False)
            influence_score = matched_doc.get("influence_score", 0) or 80
        else:
            identity_id = f"ID-KOL-{kol_id}"
            identity_type = "kol"
            doc_id = None
            kol_id_out = kol_id
            merge_status = "kol_only"
            kol_data = json.dumps({
                "kol_id": kol_id, "platform": kol_platform,
                "fans_count": kol_fans, "level": kol_level,
                "tags": kol_tags,
            }, ensure_ascii=False)
            doc_data = "{}"
            influence_score = _kol_influence_score(kol_fans, kol_level)

        # 解析 specialty
        specialty = _extract_specialty(kol_tags, matched_doc.get("specialty") if matched_doc else None)

        # 解析 influence_level
        influence_level = kol_level if not matched_doc else (
            _doc_influence_to_level(matched_doc.get("influence_score"))
        )

        tags = _parse_tags(kol_tags, matched_doc.get("tags") if matched_doc else None)

        if not dry_run:
            conn.execute("""
                INSERT OR IGNORE INTO unified_identity
                (identity_id, identity_type, name, specialty, hospital, title,
                 department, region, city, influence_level, influence_score,
                 tags, platform, kol_id, doctor_id,
                 kol_data, doctor_data, merge_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                identity_id, identity_type,
                kol_name,
                specialty,
                matched_doc.get("hospital") if matched_doc else None,
                matched_doc.get("title") if matched_doc else None,
                matched_doc.get("department") if matched_doc else None,
                matched_doc.get("region") if matched_doc else None,
                matched_doc.get("city") if matched_doc else None,
                influence_level,
                influence_score,
                json.dumps(tags, ensure_ascii=False),
                json.dumps([kol_platform], ensure_ascii=False) if kol_platform else "[]",
                kol_id_out, doc_id,
                kol_data, doc_data,
                merge_status,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            ))

            # 记录映射
            conn.execute("""
                INSERT OR IGNORE INTO identity_mapping
                (mapping_id, identity_id, source_type, source_id, source_name, confidence, match_method)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"MAP-KOL-{kol_id}", identity_id, "kol", kol_id, kol_name, confidence, match_method or "kol_only"
            ))
            if matched_doc:
                conn.execute("""
                    INSERT OR IGNORE INTO identity_mapping
                    (mapping_id, identity_id, source_type, source_id, source_name, confidence, match_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"MAP-DOC-{matched_doc['doctor_id']}", identity_id, "doctor",
                    matched_doc["doctor_id"], matched_doc["name"], confidence, match_method
                ))

        identity_count += 1
        if matched_doc:
            mapping_count += 2  # both kol and doc mappings

    # 收录未匹配的医生
    for doc in docs:
        doc_id = doc["doctor_id"]
        # 检查是否已被收录
        existing = conn.execute(
            "SELECT identity_id FROM unified_identity WHERE doctor_id = ?", (doc_id,)
        ).fetchone()
        if existing:
            continue

        identity_id = f"ID-DOC-{doc_id}"
        tags = _parse_tags(None, doc.get("tags"))
        influence_level = _doc_influence_to_level(doc.get("influence_score"))
        platform = _detect_platform_from_tags(doc.get("tags"))

        if not dry_run:
            conn.execute("""
                INSERT OR IGNORE INTO unified_identity
                (identity_id, identity_type, name, specialty, hospital, title,
                 department, region, city, influence_level, influence_score,
                 tags, platform, kol_id, doctor_id,
                 kol_data, doctor_data, merge_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                identity_id, "doctor",
                doc["name"],
                doc.get("specialty"),
                doc.get("hospital"),
                doc.get("title"),
                doc.get("department"),
                doc.get("region"),
                doc.get("city"),
                influence_level,
                doc.get("influence_score", 80),
                json.dumps(tags, ensure_ascii=False),
                json.dumps(platform, ensure_ascii=False),
                None, doc_id,
                "{}", json.dumps(dict(doc), ensure_ascii=False),
                "doctor_only",
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            ))

            conn.execute("""
                INSERT OR IGNORE INTO identity_mapping
                (mapping_id, identity_id, source_type, source_id, source_name, confidence, match_method)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"MAP-DOC-{doc_id}", identity_id, "doctor", doc_id, doc["name"], 1.0, "doctor_only"
            ))

        identity_count += 1
        mapping_count += 1

    if not dry_run:
        conn.commit()

    return {
        "identities_created": identity_count,
        "mappings_created": mapping_count,
        "message": f"✅ 统一身份库构建完成: {identity_count} 个身份，{mapping_count} 条映射",
    }


def _kol_influence_score(fans: int, level: str) -> float:
    level_boost = {"S": 1.5, "A": 1.3, "B": 1.0, "C": 0.8}.get(level, 1.0)
    base = min(fans / 100000, 100) * 10  # 10-1000
    return round(base * level_boost, 1)


def _doc_influence_to_level(score: float) -> str:
    if score is None:
        return "B"
    if score >= 90:
        return "S"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    return "C"


def _extract_specialty(kol_tags: str, doc_specialty: str) -> str:
    if doc_specialty:
        return doc_specialty
    if kol_tags:
        parts = kol_tags.split("|")
        for p in parts:
            if any(x in p for x in ["科", "内科", "外科", "科"]):
                return p.strip()
    return "综合"


def _parse_tags(kol_tags: str, doc_tags: str) -> list[str]:
    tags = set()
    if kol_tags:
        for t in kol_tags.split("|"):
            if t.strip():
                tags.add(t.strip())
    if doc_tags:
        for t in doc_tags.split("|"):
            if t.strip():
                tags.add(t.strip())
    return list(tags)


def _detect_platform_from_tags(tags_str: str) -> list[str]:
    if not tags_str:
        return ["线下"]
    return ["线下"]


# ─────────────────────────────────────────
# 查询接口
# ─────────────────────────────────────────

def query_identity(
    query: str = None,
    identity_id: str = None,
    kol_id: str = None,
    doctor_id: str = None,
    level: str = None,
    specialty: str = None,
    conn=None,
) -> dict:
    """统一身份查询"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        sql = "SELECT * FROM unified_identity WHERE 1=1"
        params = []

        if identity_id:
            sql += " AND identity_id = ?"
            params.append(identity_id)
        elif kol_id:
            sql += " AND kol_id = ?"
            params.append(kol_id)
        elif doctor_id:
            sql += " AND doctor_id = ?"
            params.append(doctor_id)
        elif query:
            sql += " AND (name LIKE ? OR specialty LIKE ? OR hospital LIKE ?)"
            q = f"%{query}%"
            params.extend([q, q, q])
        elif level:
            sql += " AND influence_level = ?"
            params.append(level)
        elif specialty:
            sql += " AND specialty LIKE ?"
            params.append(f"%{specialty}%")

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM unified_identity LIMIT 0").description]
        identities = [dict(zip(cols, r)) for r in rows]

        for ident in identities:
            ident["tags"] = json.loads(ident.get("tags") or "[]")
            ident["platform"] = json.loads(ident.get("platform") or "[]")
            ident["kol_data"] = json.loads(ident.get("kol_data") or "{}")
            ident["doctor_data"] = json.loads(ident.get("doctor_data") or "{}")

            # 映射
            maps = conn.execute("""
                SELECT * FROM identity_mapping WHERE identity_id = ?
            """, (ident["identity_id"],)).fetchall()
            ident["mappings"] = [dict(m) for m in maps]

        # 统计
        type_counts = defaultdict(int)
        level_counts = defaultdict(int)
        for i in identities:
            type_counts[i["identity_type"]] += 1
            level_counts[i.get("influence_level", "C")] += 1

        return {
            "query": query or identity_id or kol_id or doctor_id or level or specialty or "all",
            "count": len(identities),
            "type_counts": dict(type_counts),
            "level_counts": dict(level_counts),
            "identities": identities,
        }

    finally:
        if own_conn:
            conn.close()


def get_identity_profile(identity_id: str = None, kol_id: str = None, doctor_id: str = None, conn=None) -> dict:
    """获取完整身份档案"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)

        if identity_id:
            row = conn.execute("SELECT * FROM unified_identity WHERE identity_id = ?", (identity_id,)).fetchone()
        elif kol_id:
            row = conn.execute("SELECT * FROM unified_identity WHERE kol_id = ?", (kol_id,)).fetchone()
        elif doctor_id:
            row = conn.execute("SELECT * FROM unified_identity WHERE doctor_id = ?", (doctor_id,)).fetchone()
        else:
            return {"error": "identity_id, kol_id, or doctor_id required"}

        if not row:
            return {"error": "Identity not found"}

        cols = [d[0] for d in conn.execute("SELECT * FROM unified_identity LIMIT 0").description]
        profile = dict(zip(cols, row))
        profile["tags"] = json.loads(profile.get("tags") or "[]")
        profile["platform"] = json.loads(profile.get("platform") or "[]")
        profile["kol_data"] = json.loads(profile.get("kol_data") or "{}")
        profile["doctor_data"] = json.loads(profile.get("doctor_data") or "{}")

        # 获取映射
        maps = conn.execute("""
            SELECT * FROM identity_mapping WHERE identity_id = ?
        """, (profile["identity_id"],)).fetchall()
        profile["mappings"] = [dict(m) for m in maps]

        # 关联内容数据
        if kol_id or profile.get("kol_id"):
            kid = kol_id or profile["kol_id"]
            content_rows = conn.execute("""
                SELECT COUNT(*) as cnt, SUM(impressions) as impr, SUM(conversions) as conv
                FROM content_metrics m
                JOIN content_campaigns c ON m.campaign_id = c.campaign_id
                WHERE c.platform = ?
            """, (profile.get("kol_data", {}).get("platform"),)).fetchone()
            if content_rows:
                profile["content_stats"] = dict(content_rows)

        # 建议
        suggestions = []
        if profile["identity_type"] == "both":
            suggestions.append("✅ 此身份已关联医生和KOL双身份")
        if profile.get("influence_score", 0) >= 90:
            suggestions.append(f"影响力得分 {profile['influence_score']}，建议重点维护")
        if profile.get("kol_data", {}).get("fans_count", 0) > 1000000:
            suggestions.append(f"粉丝 {profile['kol_data']['fans_count']}，建议开展合作")

        profile["suggestions"] = suggestions

        return profile

    finally:
        if own_conn:
            conn.close()


from datetime import datetime
from db import get_conn, close_conn

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
            result = build_unified_identity(conn, dry_run=args.get("dry_run", False))

        elif action == "query":
            result = query_identity(
                query=args.get("query"),
                identity_id=args.get("identity_id"),
                kol_id=args.get("kol_id"),
                doctor_id=args.get("doctor_id"),
                level=args.get("level"),
                specialty=args.get("specialty"),
            )

        elif action == "profile":
            result = get_identity_profile(
                identity_id=args.get("identity_id"),
                kol_id=args.get("kol_id"),
                doctor_id=args.get("doctor_id"),
            )

        else:
            result = {"error": f"Unknown action: {action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        close_conn(conn)
