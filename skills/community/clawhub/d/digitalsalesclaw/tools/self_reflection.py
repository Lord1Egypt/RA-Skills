"""
Phase 2.2 - Self-Reflection 机制

让 AI Agent 在执行后批判性审视自身输出，自动检测并修正错误：

核心流程:
  执行 → 记录 → 自审 → 检测失败 → 修正 → 记录反思

工具:
  - record_execution(): 记录一次执行（含输入、输出、上下文）
  - self_review():       批判性审视执行结果，发现问题
  - detect_failure():    判断是否失败 + 失败类型
  - self_correct():      生成修正方案
  - get_reflection():    从历史反思中学习

使用场景:
  - ask/tool 执行后自动调用 self_review
  - 归因分析结果可疑时调用 self_review
  - 内容合规审核后调用 self_review
"""

import sys
import json
import uuid
import re
from pathlib import Path
from datetime import datetime
from enum import Enum
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 失败类型定义
# ─────────────────────────────────────────

class FailureType(Enum):
    NONE                = "none"
    EMPTY_RESULT        = "empty_result"
    SYNTAX_ERROR        = "syntax_error"
    SEMANTIC_ERROR      = "semantic_error"
    DATA_MISSING        = "data_missing"
    QUALITY_LOW         = "quality_low"
    CONTRADICTION       = "contradiction"
    COVERAGE_LOW        = "coverage_low"
    TIMEOUT             = "timeout"


class ConfidenceLevel(Enum):
    HIGH    = "high"
    MEDIUM  = "medium"
    LOW     = "low"


# ─────────────────────────────────────────
# 数据库
# ─────────────────────────────────────────

def ensure_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reflection_executions (
            execution_id TEXT PRIMARY KEY,
            tool_name   TEXT,
            action      TEXT,
            input_text  TEXT,
            output_text TEXT,
            context     TEXT DEFAULT '{}',
            result_info TEXT DEFAULT '{}',
            is_failure  INTEGER DEFAULT 0,
            failure_type TEXT,
            confidence  TEXT DEFAULT 'high',
            review_notes TEXT DEFAULT '',
            corrected_output TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reflection_lessons (
            lesson_id   TEXT PRIMARY KEY,
            pattern     TEXT NOT NULL,
            root_cause  TEXT,
            fix_method  TEXT,
            tool_name   TEXT,
            frequency   INTEGER DEFAULT 1,
            last_seen   DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reflection_self_corrections (
            correction_id  TEXT PRIMARY KEY,
            execution_id   TEXT NOT NULL,
            failure_type  TEXT NOT NULL,
            diagnosis     TEXT NOT NULL,
            fix_suggestion TEXT,
            fix_applied   INTEGER DEFAULT 0,
            fix_result    TEXT,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_exec_failure ON reflection_executions(is_failure)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lessons_pattern ON reflection_lessons(pattern)")


# ─────────────────────────────────────────
# 记录执行
# ─────────────────────────────────────────

def record_execution(
    tool_name: str,
    action: str,
    input_text: str,
    output_text: str,
    context: dict = None,
    result_info: dict = None,
    conn=None,
) -> str:
    """记录一次执行，生成 execution_id"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        execution_id = f"EXEC-{uuid.uuid4().hex[:12].upper()}"
        conn.execute("""
            INSERT INTO reflection_executions
            (execution_id, tool_name, action, input_text, output_text,
             context, result_info, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            execution_id, tool_name, action, input_text, output_text,
            json.dumps(context or {}, ensure_ascii=False),
            json.dumps(result_info or {}, ensure_ascii=False),
            datetime.now().isoformat(),
        ))
        conn.commit()
        return execution_id

    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 自审核心
# ─────────────────────────────────────────

def self_review(
    execution_id: str = None,
    tool_name: str = None,
    action: str = None,
    input_text: str = None,
    output_text: str = None,
    context: dict = None,
    expected_fields: list[str] = None,
    min_results: int = 0,
    conn=None,
) -> dict:
    """
    批判性审视执行结果，返回审阅报告

    检查维度:
      1. 结构完整性：必要字段是否存在
      2. 结果有效性：是否为空、数据量是否足够
      3. 语义合理性：数值是否合理、是否有矛盾
      4. 质量评估：输出是否完整、有深度
      5. 历史对比：与同类执行相比是否异常
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        # 如果没有 execution_id，先记录
        if not execution_id:
            execution_id = record_execution(
                tool_name or "unknown", action or "", input_text or "", output_text or "",
                context=context, conn=conn
            )

        # 获取原始执行记录
        row = conn.execute(
            "SELECT * FROM reflection_executions WHERE execution_id = ?",
            (execution_id,)
        ).fetchone()

        if row:
            orig_context = json.loads(row["context"] or "{}")
            orig_result_info = json.loads(row["result_info"] or "{}")
        else:
            orig_context = context or {}
            orig_result_info = result_info or {}

        # 解析输出
        try:
            output = json.loads(output_text) if isinstance(output_text, str) else output_text
        except Exception:
            output = {"raw": output_text}

        # 执行各项检查
        checks = []

        # 1. 结构检查
        if expected_fields:
            missing = _check_missing_fields(output, expected_fields)
            if missing:
                checks.append({
                    "check": "structure",
                    "passed": False,
                    "issue": f"缺少字段: {missing}",
                    "severity": "high",
                })
            else:
                checks.append({"check": "structure", "passed": True, "issue": ""})

        # 2. 空结果检查
        empty_issue = _check_empty_result(output)
        if empty_issue:
            checks.append({
                "check": "empty",
                "passed": False,
                "issue": empty_issue,
                "severity": "high",
            })
        else:
            checks.append({"check": "empty", "passed": True, "issue": ""})

        # 3. 数量检查
        if min_results > 0:
            count = _count_results(output)
            if count < min_results:
                checks.append({
                    "check": "quantity",
                    "passed": False,
                    "issue": f"结果数量 {count} < 要求 {min_results}",
                    "severity": "medium",
                })
            else:
                checks.append({"check": "quantity", "passed": True, "issue": ""})

        # 4. 数值合理性检查
        semantic_issues = _check_semantic_validity(output)
        if semantic_issues:
            checks.append({
                "check": "semantic",
                "passed": False,
                "issue": semantic_issues,
                "severity": "medium",
            })
        else:
            checks.append({"check": "semantic", "passed": True, "issue": ""})

        # 5. 错误检测
        error_issues = _check_errors(output_text, output)
        if error_issues:
            checks.append({
                "check": "errors",
                "passed": False,
                "issue": error_issues,
                "severity": "high",
            })
        else:
            checks.append({"check": "errors", "passed": True, "issue": ""})

        # 综合判断
        failed_checks = [c for c in checks if not c["passed"]]
        failure_types = [FailureType.SYNTAX_ERROR, FailureType.EMPTY_RESULT,
                        FailureType.DATA_MISSING, FailureType.QUALITY_LOW,
                        FailureType.SEMANTIC_ERROR]

        if any(c["severity"] == "high" for c in failed_checks):
            confidence = ConfidenceLevel.LOW
        elif any(c["severity"] == "medium" for c in failed_checks):
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.HIGH

        is_failure = len([c for c in checks if not c["passed"]]) > 0

        # 识别失败类型
        detected_failures = []
        for c in failed_checks:
            if c["check"] == "empty":
                detected_failures.append(FailureType.EMPTY_RESULT)
            elif c["check"] == "errors":
                detected_failures.append(FailureType.SYNTAX_ERROR)
            elif c["check"] == "semantic":
                detected_failures.append(FailureType.SEMANTIC_ERROR)
            elif c["check"] == "structure":
                detected_failures.append(FailureType.DATA_MISSING)
            elif c["check"] == "quantity":
                detected_failures.append(FailureType.COVERAGE_LOW)

        # 生成审阅笔记
        review_notes = _generate_review_notes(checks, output, detected_failures)

        # 更新执行记录
        conn.execute("""
            UPDATE reflection_executions
            SET is_failure = ?, failure_type = ?, confidence = ?, review_notes = ?
            WHERE execution_id = ?
        """, (
            int(is_failure),
            ",".join(f.value for f in detected_failures) if detected_failures else "none",
            confidence.value,
            review_notes,
            execution_id,
        ))
        conn.commit()

        return {
            "execution_id": execution_id,
            "is_failure": is_failure,
            "confidence": confidence.value,
            "failure_types": [f.value for f in detected_failures],
            "checks": checks,
            "review_notes": review_notes,
            "suggestions": _generate_fix_suggestions(checks, detected_failures, tool_name, output),
        }

    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 检查函数
# ─────────────────────────────────────────

def _check_missing_fields(output: dict, expected: list[str]) -> list[str]:
    missing = []
    for f in expected:
        if f not in output or output[f] is None or output[f] == "":
            missing.append(f)
    return missing


def _check_empty_result(output: dict) -> str:
    """检查结果是否为空"""
    if isinstance(output, dict):
        # 检查常见的结果字段
        result_fields = ["results", "data", "items", "records", "audits", "journeys"]
        for field in result_fields:
            if field in output:
                val = output[field]
                if isinstance(val, list) and len(val) == 0:
                    return f"字段 '{field}' 结果列表为空"
                if isinstance(val, dict) and len(val) == 0:
                    return f"字段 '{field}' 结果字典为空"
        # 检查 error 字段
        if "error" in output and output["error"]:
            return f"执行返回错误: {output['error']}"
    if isinstance(output, list) and len(output) == 0:
        return "结果列表为空"
    return ""


def _count_results(output: dict) -> int:
    """计算结果数量"""
    if isinstance(output, dict):
        for field in ["results", "data", "items", "records", "audits", "journeys", "metrics"]:
            if field in output and isinstance(output[field], list):
                return len(output[field])
    if isinstance(output, list):
        return len(output)
    return 1


def _check_semantic_validity(output: dict) -> list[str]:
    """检查语义合理性"""
    issues = []

    if isinstance(output, dict):
        # 检查负数
        for key in ["score", "confidence", "rate", "ratio", "pct", "percentage"]:
            if key in output:
                val = output[key]
                if isinstance(val, (int, float)) and val < 0:
                    issues.append(f"{key} 为负数: {val}")
                if isinstance(val, (int, float)) and val > 1 and key in ["score", "confidence"]:
                    issues.append(f"{key} 超过1: {val}")

        # 检查百分比
        for key in ["score", "cvr", "ctr", "ctr_pct", "conversion_rate"]:
            if key in output:
                val = output[key]
                if isinstance(val, (int, float)) and (val < 0 or val > 100):
                    issues.append(f"{key} 超出百分比范围: {val}")

        # 检查金额
        for key in ["total_amount", "value", "revenue", "cost", "spend"]:
            if key in output:
                val = output[key]
                if isinstance(val, (int, float)) and val < 0:
                    issues.append(f"{key} 为负数（金额不应为负）: {val}")

        # 检查列表数量悬殊（矛盾检测）
        if "total" in output and "results" in output:
            total = output["total"]
            results_len = len(output["results"]) if isinstance(output["results"], list) else 0
            if isinstance(total, int) and results_len > 0 and total == 0:
                issues.append(f"矛盾: total=0 但 results 非空")

    return issues


def _check_errors(output_text: str, output: dict) -> list[str]:
    """检测错误信息"""
    issues = []
    if isinstance(output_text, str):
        error_patterns = [
            r"error",
            r"exception",
            r"traceback",
            r"OperationalError",
            r"SyntaxError",
            r"Traceback \(most recent call last\)",
        ]
        text_lower = output_text.lower()
        for pattern in error_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                issues.append(f"发现错误标识: {pattern}")
                break

    if isinstance(output, dict) and "error" in output:
        err = output["error"]
        if err and str(err).lower() not in ["null", "none", ""]:
            issues.append(f"error 字段: {err}")

    return issues


def _generate_review_notes(
    checks: list[dict],
    output: dict,
    failures: list[FailureType],
) -> str:
    """生成审阅笔记摘要"""
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    notes = [f"审查完成: {passed}/{total} 项通过"]

    for c in checks:
        if not c["passed"]:
            notes.append(f"  ❌ [{c['check']}] {c['issue']}")

    if failures:
        notes.append(f"失败类型: {', '.join(f.value for f in failures)}")

    return "\n".join(notes)


def _generate_fix_suggestions(
    checks: list[dict],
    failures: list[FailureType],
    tool_name: str,
    output: dict,
) -> list[str]:
    """生成修正建议"""
    suggestions = []

    for f in failures:
        if f == FailureType.EMPTY_RESULT:
            suggestions.append("结果为空，建议检查输入条件或数据源是否正确")
            suggestions.append("可尝试扩大查询范围或调整过滤条件")
        elif f == FailureType.DATA_MISSING:
            suggestions.append("缺少必要字段，建议检查数据库 schema 是否匹配")
        elif f == FailureType.SYNTAX_ERROR:
            suggestions.append("执行出错，建议检查 SQL 或参数是否正确")
        elif f == FailureType.SEMANTIC_ERROR:
            suggestions.append("结果语义异常，建议人工复核计算逻辑")
        elif f == FailureType.COVERAGE_LOW:
            suggestions.append("结果数量不足，建议扩大时间范围或放宽筛选条件")

    # 通用建议
    if not suggestions:
        suggestions.append("输出质量合格，无需修正")

    return suggestions


# ─────────────────────────────────────────
# 自修正
# ─────────────────────────────────────────

def self_correct(
    execution_id: str,
    tool_name: str = None,
    conn=None,
) -> dict:
    """根据自审结果生成修正方案"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        # 获取执行记录
        row = conn.execute(
            "SELECT * FROM reflection_executions WHERE execution_id = ?",
            (execution_id,)
        ).fetchone()

        if not row:
            return {"error": f"Execution not found: {execution_id}"}

        execution = dict(row)
        output = json.loads(execution["output_text"]) if execution["output_text"] else {}

        failures = execution["failure_type"].split(",") if execution["failure_type"] else []
        failure_enum = [FailureType(f) for f in failures if f != "none"]

        # 生成诊断
        diagnosis = _diagnose_failure(execution, failure_enum, output)

        # 生成修正建议
        fix_suggestion = _generate_fix_suggestions(
            [], failure_enum, tool_name or execution["tool_name"], output
        )

        # 记录修正
        correction_id = f"CORR-{uuid.uuid4().hex[:10].upper()}"
        conn.execute("""
            INSERT INTO reflection_self_corrections
            (correction_id, execution_id, failure_type, diagnosis, fix_suggestion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            correction_id,
            execution_id,
            ",".join(f.value for f in failure_enum),
            diagnosis,
            json.dumps(fix_suggestion, ensure_ascii=False),
        ))
        conn.commit()

        return {
            "correction_id": correction_id,
            "execution_id": execution_id,
            "diagnosis": diagnosis,
            "failure_types": [f.value for f in failure_enum],
            "fix_suggestion": fix_suggestion,
        }

    finally:
        if own_conn:
            conn.close()


def _diagnose_failure(execution: dict, failures: list[FailureType], output: dict) -> str:
    """诊断失败根因"""
    tool = execution.get("tool_name", "unknown")
    action = execution.get("action", "")
    ctx = json.loads(execution.get("context") or "{}")

    diagnoses = []

    for f in failures:
        if f == FailureType.EMPTY_RESULT:
            diagnoses.append(
                f"结果为空可能原因: (1) 数据库中无符合条件的数据 "
                f"(2) 查询条件过于严格 (3) 数据表尚未初始化"
            )
        elif f == FailureType.DATA_MISSING:
            diagnoses.append(
                f"缺少字段可能是由于数据库 schema 与代码不匹配，"
                f"建议检查 {tool} 工具的 SQL 查询是否使用了正确的列名"
            )
        elif f == FailureType.SYNTAX_ERROR:
            diagnoses.append("执行错误可能是 SQL 语法有误或参数传递不正确")
        elif f == FailureType.SEMANTIC_ERROR:
            diagnoses.append("结果语义异常可能是计算逻辑有误或数据源质量问题")
        elif f == FailureType.COVERAGE_LOW:
            diagnoses.append("覆盖率低可能是查询时间范围过窄或分类标准过细")

    return " | ".join(diagnoses) if diagnoses else "未发现明显问题"


# ─────────────────────────────────────────
# 反思学习
# ─────────────────────────────────────────

def learn_from_execution(
    execution_id: str,
    conn=None,
) -> dict:
    """从一次执行中提取教训，更新 lessons 表"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        row = conn.execute(
            "SELECT * FROM reflection_executions WHERE execution_id = ?",
            (execution_id,)
        ).fetchone()

        if not row:
            return {"error": f"Execution not found: {execution_id}"}

        exec_dict = dict(row)
        failures = exec_dict["failure_type"].split(",") if exec_dict["failure_type"] else []

        if "none" in failures or not failures:
            return {"message": "成功执行，无需记录教训"}

        tool = exec_dict["tool_name"]
        pattern = f"{tool}:{','.join(failures)}"

        # 检查是否已存在
        existing = conn.execute(
            "SELECT * FROM reflection_lessons WHERE pattern = ?", (pattern,)
        ).fetchone()

        if existing:
            conn.execute("""
                UPDATE reflection_lessons
                SET frequency = frequency + 1, last_seen = ?
                WHERE pattern = ?
            """, (datetime.now().isoformat(), pattern))
            lesson_id = existing["lesson_id"]
        else:
            lesson_id = f"LESSON-{uuid.uuid4().hex[:8].upper()}"
            conn.execute("""
                INSERT INTO reflection_lessons
                (lesson_id, pattern, tool_name, frequency, last_seen)
                VALUES (?, ?, ?, 1, ?)
            """, (lesson_id, pattern, tool, datetime.now().isoformat()))

        conn.commit()
        return {
            "lesson_id": lesson_id,
            "pattern": pattern,
            "learned": True,
        }

    finally:
        if own_conn:
            conn.close()


def get_frequent_failures(limit: int = 10, conn=None) -> dict:
    """获取高频失败模式（用于预防）"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        rows = conn.execute("""
            SELECT * FROM reflection_lessons
            ORDER BY frequency DESC LIMIT ?
        """, (limit,)).fetchall()
        return {
            "frequent_failures": [dict(r) for r in rows],
            "suggestions": [
                f"高频问题: {r['pattern']} (出现 {r['frequency']} 次)"
                for r in rows if r['frequency'] > 1
            ]
        }
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
    action = args.get("action", "review")

    conn = get_conn()

    try:
        ensure_tables(conn)
        conn.commit()

        if action == "record":
            result = {
                "execution_id": record_execution(
                    tool_name=args.get("tool_name", "unknown"),
                    action=args.get("action", ""),
                    input_text=args.get("input_text", ""),
                    output_text=args.get("output_text", ""),
                    context=args.get("context"),
                    result_info=args.get("result_info"),
                )
            }

        elif action == "review":
            result = self_review(
                execution_id=args.get("execution_id"),
                tool_name=args.get("tool_name"),
                action=args.get("action"),
                input_text=args.get("input_text"),
                output_text=args.get("output_text"),
                context=args.get("context"),
                expected_fields=args.get("expected_fields"),
                min_results=args.get("min_results", 0),
            )

        elif action == "correct":
            result = self_correct(
                execution_id=args["execution_id"],
                tool_name=args.get("tool_name"),
            )

        elif action == "learn":
            result = learn_from_execution(args["execution_id"])

        elif action == "frequent_failures":
            result = get_frequent_failures(limit=args.get("limit", 10))

        else:
            result = {"error": f"Unknown action: {action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        close_conn(conn)
