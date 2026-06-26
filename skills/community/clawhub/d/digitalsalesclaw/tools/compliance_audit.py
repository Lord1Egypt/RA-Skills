#!/usr/bin/env python3
"""
合规审核状态机

创建 compliance_audits 表 + 状态流转引擎：
  状态: draft → pending_review → approved/published
                     ↓
              non_compliant → pending_review → ...

支持:
  - 创建审核单（自动触发合规扫描）
  - 状态流转（带校验）
  - 审核历史追溯
  - 批量审核
  - 自动合规评分
"""

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 状态机定义
# ─────────────────────────────────────────

class AuditState:
    DRAFT             = "draft"              # 草稿
    PENDING_REVIEW    = "pending_review"      # 待审核
    COMPLIANT         = "compliant"           # 合规通过
    NON_COMPLIANT     = "non_compliant"       # 不合规
    APPROVED          = "approved"             # 审批通过
    PUBLISHED         = "published"           # 已发布
    REJECTED          = "rejected"            # 驳回


# 允许的流转路径
STATE_TRANSITIONS = {
    AuditState.DRAFT:            {AuditState.PENDING_REVIEW, AuditState.NON_COMPLIANT},
    AuditState.PENDING_REVIEW:   {AuditState.COMPLIANT, AuditState.NON_COMPLIANT, AuditState.APPROVED},
    AuditState.NON_COMPLIANT:    {AuditState.PENDING_REVIEW, AuditState.REJECTED},
    AuditState.COMPLIANT:        {AuditState.APPROVED, AuditState.PUBLISHED},
    AuditState.APPROVED:         {AuditState.PUBLISHED},
    AuditState.PUBLISHED:        set(),   # 终态
    AuditState.REJECTED:          set(),   # 终态
}

STATE_LABELS = {
    AuditState.DRAFT:           "📝 草稿",
    AuditState.PENDING_REVIEW:  "⏳ 待审核",
    AuditState.COMPLIANT:        "✅ 合规通过",
    AuditState.NON_COMPLIANT:    "❌ 不合规",
    AuditState.APPROVED:         "👍 审批通过",
    AuditState.PUBLISHED:        "🚀 已发布",
    AuditState.REJECTED:         "🚫 驳回",
}


def get_available_transitions(current_state: str) -> list[str]:
    return list(STATE_TRANSITIONS.get(current_state, set()))


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in STATE_TRANSITIONS.get(from_state, set())


# ─────────────────────────────────────────
# 数据库操作
# ─────────────────────────────────────────

def create_audits_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS compliance_audits (
            audit_id        TEXT PRIMARY KEY,
            content_id      TEXT,
            content_text    TEXT,
            content_hash    TEXT,
            title           TEXT,
            submitter       TEXT,
            reviewer        TEXT,
            current_state   TEXT DEFAULT 'draft',
            severity_score  REAL,
            hit_rules       TEXT DEFAULT '[]',
            hit_hierarchy   TEXT DEFAULT '[]',
            notes           TEXT DEFAULT '',
            submitted_at    DATETIME,
            reviewed_at     DATETIME,
            published_at    DATETIME,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS compliance_audit_history (
            history_id  TEXT PRIMARY KEY,
            audit_id    TEXT NOT NULL,
            from_state  TEXT,
            to_state    TEXT NOT NULL,
            actor       TEXT,
            reason      TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (audit_id) REFERENCES compliance_audits(audit_id)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_state ON compliance_audits(current_state)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_content ON compliance_audits(content_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_history ON compliance_audit_history(audit_id)")


# ─────────────────────────────────────────
# 核心业务逻辑
# ─────────────────────────────────────────

def auto_review_content(content_text: str) -> dict:
    """
    使用 compliance.py 的 check_banned() 自动扫描内容
    返回: {score, hit_rules, hit_hierarchy, is_compliant}
    """
    try:
        # 动态导入 compliance 模块
        sys.path.insert(0, str(SKILL_DIR / "tools"))
        from compliance import check_banned, check_hierarchy

        # 基础违禁词检测
        banned_result = check_banned(content_text, use_db_rules=True)
        # check_banned 返回 list[dict] 或 dict{"violations": list}
        if isinstance(banned_result, list):
            hit_rules = banned_result
        else:
            hit_rules = banned_result.get("hit_rules", banned_result.get("violations", []))

        # 层级编码检测
        rule_codes = [r["rule_code"] for r in hit_rules]
        hierarchy_result = check_hierarchy(rule_codes=rule_codes) if rule_codes else {
            "total_rules": 0, "rules": []}
        hit_hierarchy = hierarchy_result.get("rules", [])

        # 综合评分
        max_severity = 0
        for r in hit_rules:
            sev = r.get("severity_score", 5)
            if sev > max_severity:
                max_severity = sev

        # 分数 = 100 - sum(severity × 2)，最低0
        deductions = sum(r.get("severity_score", 5) * 2 for r in hit_rules)
        score = max(0, 100 - deductions)

        is_compliant = len(hit_rules) == 0

        return {
            "score": score,
            "is_compliant": is_compliant,
            "hit_rules": [
                {
                    "rule_code": r["rule_code"],
                    "rule_name": r["rule_name"],
                    "severity_score": r.get("severity_score", 5),
                    "rule_hierarchy": r.get("rule_hierarchy"),
                    "matched_keyword": r.get("matched_keyword"),
                }
                for r in hit_rules
            ],
            "hit_hierarchy": [
                {
                    "rule_hierarchy": h["rule_hierarchy"],
                    "law_reference": h.get("law_reference"),
                    "rule_name": h["rule_name"],
                }
                for h in hit_hierarchy
            ],
            "suggestions": _generate_suggestions(hit_rules, score),
        }

    except Exception as e:
        return {
            "score": 100,
            "is_compliant": False,
            "hit_rules": [],
            "hit_hierarchy": [],
            "error": str(e),
            "suggestions": ["自动审核失败，请人工审核"],
        }


def _generate_suggestions(hit_rules: list[dict], score: float) -> list[str]:
    if not hit_rules:
        return ["内容合规，建议提交审核"]

    suggestions = []
    by_category = {}
    for r in hit_rules:
        cat = r.get("rule_hierarchy", "unknown")
        by_category.setdefault(cat, []).append(r["rule_name"])

    for cat, names in by_category.items():
        suggestions.append(f"触及规则 {cat}: {', '.join(names)}")

    if score < 60:
        suggestions.append("⚠️ 严重违规，建议重新撰写后再提交")
    elif score < 80:
        suggestions.append("⚠️ 存在违规风险，建议修改后提交")
    else:
        suggestions.append("⚠️ 存在轻微问题，可修改后提交")

    return suggestions


# ─────────────────────────────────────────
# 状态机操作
# ─────────────────────────────────────────

def create_audit(
    content_text: str,
    content_id: str = None,
    title: str = None,
    submitter: str = "system",
    conn=None,
) -> dict:
    """创建审核单并自动触发合规扫描"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        create_audits_table(conn)
        conn.commit()

        audit_id = f"AUD-{uuid.uuid4().hex[:12].upper()}"
        content_hash = str(hash(content_text))[:16]

        # 自动审核
        review_result = auto_review_content(content_text)

        # 决定初始状态
        if review_result["is_compliant"]:
            current_state = AuditState.COMPLIANT
        else:
            current_state = AuditState.NON_COMPLIANT

        audit = (
            audit_id,
            content_id,
            content_text,
            content_hash,
            title,
            submitter,
            None,
            current_state,
            review_result["score"],
            json.dumps(review_result["hit_rules"], ensure_ascii=False),
            json.dumps(review_result["hit_hierarchy"], ensure_ascii=False),
            None,  # notes
            None,  # submitted_at
            None,  # reviewed_at
            None,  # published_at
            datetime.now().isoformat(),
            datetime.now().isoformat(),
        )

        conn.execute("""
            INSERT INTO compliance_audits
            (audit_id, content_id, content_text, content_hash, title, submitter,
             reviewer, current_state, severity_score, hit_rules, hit_hierarchy,
             notes, submitted_at, reviewed_at, published_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, audit)

        # 记录历史
        history_id = f"HIST-{uuid.uuid4().hex[:10].upper()}"
        conn.execute("""
            INSERT INTO compliance_audit_history
            (history_id, audit_id, from_state, to_state, actor, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (history_id, audit_id, None, current_state, submitter,
              "系统自动创建并审核", datetime.now().isoformat()))

        conn.commit()

        return {
            "audit_id": audit_id,
            "current_state": current_state,
            "state_label": STATE_LABELS[current_state],
            "score": review_result["score"],
            "is_compliant": review_result["is_compliant"],
            "hit_rules": review_result["hit_rules"],
            "hit_hierarchy": review_result["hit_hierarchy"],
            "suggestions": review_result["suggestions"],
            "available_transitions": get_available_transitions(current_state),
        }

    finally:
        if own_conn:
            conn.close()


def transition_audit(
    audit_id: str,
    to_state: str,
    actor: str = "system",
    reason: str = None,
    conn=None,
) -> dict:
    """状态流转"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        # 获取当前状态
        row = conn.execute(
            "SELECT * FROM compliance_audits WHERE audit_id = ?", (audit_id,)
        ).fetchone()
        if not row:
            return {"error": f"Audit not found: {audit_id}"}

        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_audits LIMIT 0").description]
        audit = dict(zip(cols, row))
        current_state = audit["current_state"]

        if not can_transition(current_state, to_state):
            return {
                "error": f"Invalid transition: {current_state} → {to_state}",
                "current_state": current_state,
                "available_transitions": get_available_transitions(current_state),
            }

        now = datetime.now().isoformat()
        update_fields = {"current_state": to_state, "updated_at": now}
        if to_state == AuditState.PENDING_REVIEW:
            update_fields["submitted_at"] = now
        if to_state in {AuditState.APPROVED, AuditState.PUBLISHED}:
            update_fields["reviewed_at"] = now
        if to_state == AuditState.PUBLISHED:
            update_fields["published_at"] = now

        set_clause = ", ".join(f"{k} = ?" for k in update_fields)
        conn.execute(
            f"UPDATE compliance_audits SET {set_clause} WHERE audit_id = ?",
            (*update_fields.values(), audit_id)
        )

        # 记录历史
        history_id = f"HIST-{uuid.uuid4().hex[:10].upper()}"
        conn.execute("""
            INSERT INTO compliance_audit_history
            (history_id, audit_id, from_state, to_state, actor, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (history_id, audit_id, current_state, to_state, actor,
              reason or f"状态流转 {current_state} → {to_state}", now))

        conn.commit()

        return {
            "audit_id": audit_id,
            "from_state": current_state,
            "to_state": to_state,
            "state_label": STATE_LABELS[to_state],
            "available_transitions": get_available_transitions(to_state),
            "message": f"✅ 状态已更新: {STATE_LABELS[current_state]} → {STATE_LABELS[to_state]}",
        }

    finally:
        if own_conn:
            conn.close()


def get_audit(audit_id: str, conn=None) -> dict:
    """获取审核单详情"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        row = conn.execute(
            "SELECT * FROM compliance_audits WHERE audit_id = ?", (audit_id,)
        ).fetchone()
        if not row:
            return {"error": f"Audit not found: {audit_id}"}

        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_audits LIMIT 0").description]
        audit = dict(zip(cols, row))

        # 获取历史
        history = conn.execute("""
            SELECT * FROM compliance_audit_history
            WHERE audit_id = ? ORDER BY created_at ASC
        """, (audit_id,)).fetchall()
        h_cols = [d[0] for d in conn.execute("SELECT * FROM compliance_audit_history LIMIT 0").description]
        history_list = [dict(zip(h_cols, r)) for r in history]

        return {
            **audit,
            "hit_rules": json.loads(audit.get("hit_rules") or "[]"),
            "hit_hierarchy": json.loads(audit.get("hit_hierarchy") or "[]"),
            "state_label": STATE_LABELS.get(audit["current_state"], audit["current_state"]),
            "available_transitions": get_available_transitions(audit["current_state"]),
            "history": history_list,
        }

    finally:
        if own_conn:
            conn.close()


def list_audits(
    state: str = None,
    limit: int = 50,
    conn=None,
) -> dict:
    """审核单列表"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        sql = "SELECT * FROM compliance_audits WHERE 1=1"
        params = []
        if state:
            sql += " AND current_state = ?"
            params.append(state)
        sql += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM compliance_audits LIMIT 0").description]
        audits = [dict(zip(cols, r)) for r in rows]

        state_counts = conn.execute("""
            SELECT current_state, COUNT(*) as cnt
            FROM compliance_audits GROUP BY current_state
        """).fetchall()

        return {
            "total": len(audits),
            "state_counts": dict(state_counts),
            "audits": [
                {
                    "audit_id": a["audit_id"],
                    "title": a.get("title") or a.get("content_id") or a["audit_id"],
                    "current_state": a["current_state"],
                    "state_label": STATE_LABELS.get(a["current_state"], a["current_state"]),
                    "score": a.get("severity_score"),
                    "submitter": a.get("submitter"),
                    "updated_at": a["updated_at"],
                }
                for a in audits
            ],
        }

    finally:
        if own_conn:
            conn.close()


def batch_review_audit(
    audit_ids: list[str],
    decision: str = "approve",
    actor: str = "system",
    conn=None,
) -> dict:
    """
    批量审核决策
    decision: 'approve' → compliant/approved
              'reject'  → non_compliant/rejected
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        results = []
        for audit_id in audit_ids:
            audit = get_audit(audit_id, conn)
            if "error" in audit:
                results.append({"audit_id": audit_id, "error": audit["error"]})
                continue

            current = audit["current_state"]

            if decision == "approve":
                if current == AuditState.NON_COMPLIANT:
                    to_state = AuditState.PENDING_REVIEW
                elif current == AuditState.PENDING_REVIEW:
                    to_state = AuditState.APPROVED
                else:
                    results.append({
                        "audit_id": audit_id,
                        "current_state": current,
                        "message": f"当前状态不支持审批操作",
                    })
                    continue
            else:  # reject
                if current == AuditState.NON_COMPLIANT:
                    to_state = AuditState.REJECTED
                elif current == AuditState.PENDING_REVIEW:
                    to_state = AuditState.NON_COMPLIANT
                else:
                    results.append({
                        "audit_id": audit_id,
                        "current_state": current,
                        "message": f"当前状态不支持驳回操作",
                    })
                    continue

            r = transition_audit(audit_id, to_state, actor, f"批量{dict(approve='批准', reject='驳回')[decision]}", conn)
            results.append(r)

        conn.commit()
        return {"batch_results": results}

    finally:
        if own_conn:
            conn.close()


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
    action = args.get("action", "list")

    conn = get_conn()

    try:
        create_audits_table(conn)
        conn.commit()

        if action == "create":
            result = create_audit(
                content_text=args["content_text"],
                content_id=args.get("content_id"),
                title=args.get("title"),
                submitter=args.get("submitter", "system"),
            )

        elif action == "transition":
            result = transition_audit(
                audit_id=args["audit_id"],
                to_state=args["to_state"],
                actor=args.get("actor", "system"),
                reason=args.get("reason"),
            )

        elif action == "get":
            result = get_audit(audit_id=args["audit_id"])

        elif action == "list":
            result = list_audits(
                state=args.get("state"),
                limit=args.get("limit", 50),
            )

        elif action == "batch_review":
            result = batch_review_audit(
                audit_ids=args["audit_ids"],
                decision=args.get("decision", "approve"),
                actor=args.get("actor", "system"),
            )

        elif action == "auto_review":
            result = auto_review_content(args["content_text"])

        elif action == "transitions":
            state = args.get("state")
            result = {
                "state": state,
                "available": get_available_transitions(state),
                "all_states": STATE_LABELS,
            }

        else:
            result = {"error": f"Unknown action: {action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        close_conn(conn)
