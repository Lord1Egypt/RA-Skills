#!/usr/bin/env python3
"""
track_progress.py
接口四：追踪全员培训进度，生成状态报告供CHO归档与汇报

【安全标准 — v2.0】
- 输入验证：所有 ID 均经白名单校验
- 路径安全：读写路径锁定在 TRAINING_BASE
- 无外部网络：无任何 HTTP/网络调用
- 无敏感凭据：不访问任何凭据文件
- enrolled_list 仅接受显式传入，不自动扫描系统
- 版本标签：security_version = "v2.0"

版本：v2.0（安全加固版）
"""

import json
import os
import sys
import math
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

# ── 安全配置 ──────────────────────────────────────────────
WORKSPACE_BASE = os.environ.get(
    "TRAINING_WORKSPACE",
    os.path.join(os.path.expanduser("~"), ".qclaw", "workspace")
)
TRAINING_BASE = os.path.join(WORKSPACE_BASE, "knowledge-base", "training")
EXAMS_BASE = os.path.join(TRAINING_BASE, "exams")
CERTS_BASE = os.path.join(TRAINING_BASE, "certs")
REPORTS_BASE = os.path.join(TRAINING_BASE, "reports")

RE_SAFE_ID = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
RE_SAFE_ROLE = re.compile(r"^[A-Za-z0-9_\-]{1,32}$")
REPORT_TYPES = frozenset({"summary", "detail", "compliance", "all"})


# ── 安全工具函数 ────────────────────────────────────────────

def validate_id(value: str, name: str) -> str:
    """ID 白名单校验"""
    if not value or len(value) > 64:
        raise ValueError(f"{name} 为空或超长（最大64字符）")
    if not RE_SAFE_ID.match(value):
        raise ValueError(f"{name} 包含非法字符：{value!r}")
    return value


def validate_enrolled_list(raw_list: Any) -> List[Dict]:
    """校验 enrolled_list：每个条目格式正确，且仅来自显式传入"""
    if not isinstance(raw_list, list):
        raise TypeError("enrolled_list 必须为数组")
    result = []
    for entry in raw_list:
        if not isinstance(entry, dict):
            raise TypeError(f"enrolled_list 条目类型错误：{type(entry)}")
        eid = validate_id(entry.get("id", ""), "enrolled_list[].id")
        name = str(entry.get("name", eid))[:64]
        role = str(entry.get("role", ""))[:32]
        result.append({
            "id": eid,
            "name": name,
            "role": role,
            "plan_id": validate_id(entry.get("plan_id", ""), "enrolled_list[].plan_id")
                if entry.get("plan_id") else ""
        })
    return result


def safe_read_json(dir_base: str, sub_path: str) -> List[Dict]:
    """
    安全扫描目录并读取 JSON 文件
    仅扫描直接子目录，不递归，防止路径遍历
    """
    dir_base = os.path.normpath(dir_base)
    if not os.path.isdir(dir_base):
        return []

    results = []
    # os.listdir 限制在直接子目录
    for sub_name in os.listdir(dir_base):
        sub_path_full = os.path.normpath(os.path.join(dir_base, sub_name))
        # 确保是子目录而非文件
        if not os.path.isdir(sub_path_full):
            continue
        # 防路径遍历
        if not sub_path_full.startswith(dir_base):
            continue
        file_path = os.path.join(sub_path_full, sub_path)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    results.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                # 跳过损坏文件，不中断整个流程
                pass
    return results


def safe_write_json(path: str, data: Any) -> None:
    """安全写入 JSON 文件"""
    path = os.path.normpath(path)
    base = os.path.normpath(REPORTS_BASE)
    if not path.startswith(base):
        raise ValueError(f"路径越界：{path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 核心分析逻辑 ────────────────────────────────────────────

def load_all_exams(plan_id: str) -> List[Dict]:
    """扫描 exams 目录，读取所有学员成绩单"""
    plan_dir = os.path.normpath(os.path.join(EXAMS_BASE, plan_id))
    if not plan_dir.startswith(os.path.normpath(EXAMS_BASE)):
        return []
    return safe_read_json(plan_dir, "score_total.json")


def load_all_certs(plan_id: str = None) -> List[Dict]:
    """扫描 certs 目录，读取所有证书（可按 plan_id 过滤）"""
    certs = safe_read_json(CERTS_BASE, "certificate.json")
    if plan_id:
        return [c for c in certs
                if c.get("training", {}).get("plan_id") == plan_id]
    return certs


def calculate_batch_spd(exam_results: List[Dict]) -> float:
    """计算批次 SPD（Statistical Process Deviation）"""
    if not exam_results:
        return 0.0
    scores = [float(r.get("total_score", 0)) for r in exam_results]
    mean = sum(scores) / len(scores)
    if mean <= 0:
        return 0.0
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    return round(math.sqrt(variance) / mean, 4)


def check_batch_quality_gate(exam_results: List[Dict]) -> Dict:
    """批次质量门禁判定"""
    if not exam_results:
        return {
            "pass_gate": False, "pass_rate": 0.0, "avg_spd": 0.0,
            "action": "INSUFFICIENT_DATA"
        }
    passed = [r for r in exam_results if r.get("pass", False)]
    pass_rate = len(passed) / len(exam_results)
    avg_spd = calculate_batch_spd(exam_results)
    gate_passed = pass_rate >= 0.90 and avg_spd < 0.10

    return {
        "pass_gate": gate_passed,
        "pass_rate": round(pass_rate, 3),
        "avg_spd": avg_spd,
        "total_enrolled": len(exam_results),
        "passed_count": len(passed),
        "action": "UNLOCK_NEXT_PHASE" if gate_passed else "REOPEN_BATCH",
        "gate_conditions": {
            "pass_rate_required": "≥ 90%",
            "pass_rate_actual": f"{round(pass_rate * 100, 1)}%",
            "spd_required": "< 0.10",
            "spd_actual": avg_spd
        }
    }


def generate_action_items(
    exam_results: List[Dict],
    certs: List[Dict],
    plan_id: str,
    all_enrolled: List[Dict]
) -> List[Dict]:
    """根据进度状态生成CHO待执行事项"""
    actions: List[Dict] = []
    now = datetime.now(timezone.utc)

    # 从成绩单中提取 candidate_id
    exam_cids = {r.get("candidate_id") for r in exam_results if r.get("candidate_id")}
    cert_cids = {c.get("holder", {}).get("id") for c in certs if c.get("holder", {}).get("id")}
    enrolled_ids = {e.get("id") for e in all_enrolled}

    # 未开始培训
    not_started = enrolled_ids - exam_cids - cert_cids
    for cid in sorted(not_started):
        actions.append({
            "id": f"A{len(actions)+1:03d}",
            "type": "reminder",
            "priority": "P2",
            "target": [cid],
            "description": f"培训 {plan_id} 已公布，请尽快开始学习",
            "due": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "template": "reminder_training_start"
        })

    # 不合格（1次未通过 → 补训；2次 → 升级CRO）
    failed_ids = {r.get("candidate_id") for r in exam_results
                  if not r.get("pass", True) and r.get("candidate_id")}
    for cid in sorted(failed_ids):
        score = next((r.get("total_score", 0) for r in exam_results
                      if r.get("candidate_id") == cid), 0)
        # 检查是否有第二次考核记录（通过目录结构判断）
        cid_exam_dir = os.path.normpath(os.path.join(EXAMS_BASE, plan_id, cid))
        has_second_attempt = False
        if os.path.isdir(cid_exam_dir):
            score_files = [f for f in os.listdir(cid_exam_dir)
                           if f.startswith("score_total")]
            has_second_attempt = len(score_files) >= 2

        if has_second_attempt:
            actions.append({
                "id": f"A{len(actions)+1:03d}",
                "type": "escalation",
                "priority": "P1",
                "target": [cid],
                "description": f"连续2次未通过（{score}分），提交 CRO 启动退出审查",
                "due": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
                "template": "escalation_exit_review"
            })
        else:
            actions.append({
                "id": f"A{len(actions)+1:03d}",
                "type": "remedial",
                "priority": "P2",
                "target": [cid],
                "description": f"考核未通过（{score}分），请安排补训",
                "due": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
                "template": "remedial_training"
            })

    # 证书到期提醒（30天内）
    for cert in certs:
        vu = cert.get("valid_until", "")
        if not vu:
            continue
        try:
            expiry = datetime.fromisoformat(vu)
            days_left = (expiry - now).days
            if 0 <= days_left <= 30:
                holder = cert.get("holder", {})
                actions.append({
                    "id": f"A{len(actions)+1:03d}",
                    "type": "expiry_notice",
                    "priority": "P2",
                    "target": [holder.get("id", "")],
                    "description": f"证书 {cert.get('cert_id')} 将在 {days_left} 天后到期",
                    "due": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "template": "expiry_notice"
                })
        except (ValueError, TypeError):
            pass

    return actions


def generate_summary_report(
    plan_id: str,
    exam_results: List[Dict],
    certs: List[Dict],
    all_enrolled: List[Dict]
) -> Dict:
    """生成全员进度汇总报告"""
    total_enrolled = len(all_enrolled)
    certified_ids = {c.get("holder", {}).get("id") for c in certs}
    exam_cids = {r.get("candidate_id") for r in exam_results if r.get("candidate_id")}
    passed_ids = {r.get("candidate_id") for r in exam_results
                   if r.get("pass", False) and r.get("candidate_id")}
    failed_ids = exam_cids - passed_ids
    completed_not_cert = passed_ids - certified_ids
    not_started = {e.get("id") for e in all_enrolled} - exam_cids - certified_ids

    now = datetime.now(timezone.utc)
    expiry_warnings = []
    for cert in certs:
        vu = cert.get("valid_until", "")
        if not vu:
            continue
        try:
            days_left = (datetime.fromisoformat(vu) - now).days
            if 0 <= days_left <= 60:
                expiry_warnings.append({
                    "cert_id": cert.get("cert_id", ""),
                    "holder": cert.get("holder", {}).get("name", ""),
                    "expires": vu,
                    "days_left": days_left
                })
        except (ValueError, TypeError):
            pass

    scores = [r.get("total_score", 0) for r in exam_results]
    quality_gate = check_batch_quality_gate(exam_results)

    return {
        "plan_id": plan_id,
        "report_date": now.strftime("%Y-%m-%d"),
        "report_generated_at": now.isoformat(),
        "security_version": "v2.0",
        "total_enrolled": total_enrolled,
        "status_breakdown": {
            "not_started": len(not_started),
            "in_progress": len(exam_cids) - len(passed_ids) - len(failed_ids),
            "completed_not_certified": len(completed_not_cert),
            "certified": len(certified_ids),
            "failed_once": len(failed_ids),
            "failed_twice_pending_review": 0
        },
        "completion_rate": round(len(exam_cids) / total_enrolled, 3) if total_enrolled > 0 else 0,
        "certification_rate": round(len(certified_ids) / total_enrolled, 3) if total_enrolled > 0 else 0,
        "quality_gate": quality_gate,
        "expiry_warnings": expiry_warnings,
        "score_distribution": {
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0
        }
    }


def generate_detail_report(
    exam_results: List[Dict],
    certs: List[Dict]
) -> List[Dict]:
    """生成逐人详细状态报告"""
    cert_map = {c.get("holder", {}).get("id"): c for c in certs}
    details: List[Dict] = []
    for r in exam_results:
        cid = r.get("candidate_id", "")
        if not cid:
            continue
        cert = cert_map.get(cid)
        total_score = float(r.get("total_score", 0))
        is_pass = r.get("pass", False)
        details.append({
            "candidate_id": cid,
            "candidate_name": str(r.get("candidate_name", cid))[:64],
            "candidate_role": str(r.get("candidate_role", ""))[:32],
            "total_score": total_score,
            "grade": str(r.get("grade", ""))[:16],
            "pass": is_pass,
            "spd": float(r.get("spd", 0)),
            "theory_score": int(r.get("theory_score", 0)),
            "practical_score": float(r.get("practical_score", 0)),
            "weak_areas": r.get("theory_detail", {}).get("weak_areas", []),
            "certified": cert is not None,
            "cert_id": cert.get("cert_id") if cert else None,
            "cert_valid_until": cert.get("valid_until") if cert else None,
            "action_required": "remedial" if not is_pass else ("certify" if not cert else None)
        })
    return details


def generate_compliance_report(
    exam_results: List[Dict],
    certs: List[Dict],
    all_enrolled: List[Dict]
) -> Dict:
    """生成合规追踪报告（供 CLO 使用）"""
    certified_ids = {c.get("holder", {}).get("id") for c in certs}
    passed_ids = {r.get("candidate_id") for r in exam_results
                  if r.get("pass", False) and r.get("candidate_id")}
    failed_ids = {r.get("candidate_id") for r in exam_results
                  if not r.get("pass", True) and r.get("candidate_id")}
    enrolled_ids = {e.get("id") for e in all_enrolled}
    non_compliant = enrolled_ids - certified_ids - passed_ids

    enrolled_count = len(enrolled_ids) or 1
    non_compliant_count = len(non_compliant)
    compliance_status = "RED" if non_compliant_count > enrolled_count * 0.1 \
        else "YELLOW" if non_compliant_count > 0 else "GREEN"

    return {
        "plan_id": all_enrolled[0].get("plan_id", "UNKNOWN") if all_enrolled else "UNKNOWN",
        "report_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "security_version": "v2.0",
        "compliance_summary": {
            "total_enrolled": enrolled_count,
            "total_compliant": len(certified_ids),
            "total_passed_not_cert": len(passed_ids - certified_ids),
            "total_failed": len(failed_ids),
            "total_non_compliant": non_compliant_count,
            "compliance_rate": round(len(certified_ids) / enrolled_count, 3)
        },
        "non_compliant_list": [
            {"candidate_id": cid, "reason": "未完成培训", "action_required": "强制提醒"}
            for cid in sorted(non_compliant)
        ],
        "failed_list": [
            {
                "candidate_id": cid,
                "score": next((r.get("total_score", 0) for r in exam_results
                               if r.get("candidate_id") == cid), 0),
                "action_required": "补训或退出审查"
            }
            for cid in sorted(failed_ids)
        ],
        "compliance_status": compliance_status,
        "clor_action_required": non_compliant_count > 0,
        "cro_action_required": len(failed_ids) > 0
    }


# ── 主函数 ──────────────────────────────────────────────────

def track_progress(report_args: Dict) -> Dict:
    """
    生成培训进度追踪报告
    """
    # ① 输入安全校验
    plan_id = validate_id(report_args.get("plan_id", ""), "plan_id")
    report_type = str(report_args.get("report_type", "summary"))[:16]
    if report_type not in REPORT_TYPES:
        raise ValueError(f"report_type 非法：{report_type!r}，允许值：{REPORT_TYPES}")
    include_detail = bool(report_args.get("include_detail", True))

    # enrolled_list 必须显式传入，禁止自动扫描系统
    all_enrolled = validate_enrolled_list(report_args.get("enrolled_list", []))
    for e in all_enrolled:
        e["plan_id"] = plan_id

    # ② 加载数据（仅从指定 plan_id 目录加载）
    exam_results = load_all_exams(plan_id)
    certs = load_all_certs(plan_id)

    # ③ 生成报告
    out_dir = os.path.normpath(os.path.join(REPORTS_BASE, plan_id))
    os.makedirs(out_dir, exist_ok=True)
    reports: Dict[str, str] = {}
    now_str = datetime.now(timezone.utc).isoformat()

    if report_type in ("summary", "all"):
        summary = generate_summary_report(plan_id, exam_results, certs, all_enrolled)
        path = os.path.join(out_dir, "progress_summary.json")
        safe_write_json(path, summary)
        reports["progress_summary"] = path
        print(f"✅ progress_summary.json → {path}")

    if report_type in ("detail", "all") and include_detail:
        detail = generate_detail_report(exam_results, certs)
        path = os.path.join(out_dir, "progress_detail.json")
        safe_write_json(path, detail)
        reports["progress_detail"] = path
        print(f"✅ progress_detail.json → {path}")

    if report_type in ("compliance", "all"):
        compliance = generate_compliance_report(exam_results, certs, all_enrolled)
        path = os.path.join(out_dir, "compliance_report.json")
        safe_write_json(path, compliance)
        reports["compliance_report"] = path
        print(f"✅ compliance_report.json → {path}")

    # 批次 SPD 分析（供 CQO）
    batch_spd = calculate_batch_spd(exam_results)
    batch_quality_gate = check_batch_quality_gate(exam_results)
    spd_path = os.path.join(out_dir, "spd_batch_analysis.json")
    safe_write_json(spd_path, {
        "plan_id": plan_id,
        "batch_spd": batch_spd,
        "quality_gate": batch_quality_gate,
        "analyzed_at": now_str,
        "security_version": "v2.0"
    })
    reports["spd_batch_analysis"] = spd_path
    print(f"✅ spd_batch_analysis.json → {spd_path}")

    # 待办事项（供 CHO 执行）
    action_items = generate_action_items(exam_results, certs, plan_id, all_enrolled)
    action_path = os.path.join(out_dir, "action_items.json")
    action_payload: Dict[str, Any] = {
        "plan_id": plan_id,
        "generated_at": now_str,
        "total_actions": len(action_items),
        "actions": action_items,
        "security_version": "v2.0"
    }
    safe_write_json(action_path, action_payload)
    reports["action_items"] = action_path
    print(f"✅ action_items.json → {action_path}")

    return {
        "status": "COMPLETED",
        "plan_id": plan_id,
        "report_type": report_type,
        "generated_at": now_str,
        "security_version": "v2.0",
        "reports": reports,
        "key_findings": {
            "total_enrolled": len(all_enrolled),
            "total_completed": len(exam_results),
            "total_certified": len(certs),
            "quality_gate": batch_quality_gate.get("action", "UNKNOWN"),
            "batch_spd": batch_spd,
            "pending_actions": len(action_items)
        },
        "cho_next_steps": [
            "根据 action_items.json 执行待办事项",
            "如 quality_gate=REOPEN_BATCH，须重新开放培训报名",
            "向 CEO 提交月度培训进度报告",
            "向 CLO 同步合规缺口（compliance_report.json）"
        ]
    }


# ── CLI 入口 ────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_path = os.path.normpath(sys.argv[1])
            if not input_path.startswith(os.path.normpath(WORKSPACE_BASE)):
                print("❌ 错误：输入文件必须在 workspace 目录下", file=sys.stderr)
                sys.exit(1)
            with open(input_path, "r", encoding="utf-8") as f:
                report_args = json.load(f)
        else:
            report_args = {
                "plan_id": "PLAN-2026-Q2-001",
                "report_type": "all",
                "include_detail": True,
                "enrolled_list": [
                    {"id": "AGENT-CMO-001", "name": "CMO-Agent", "role": "CMO"},
                    {"id": "AGENT-CTO-001", "name": "CTO-Agent", "role": "CTO"},
                    {"id": "AGENT-CFO-001", "name": "CFO-Agent", "role": "CFO"},
                    {"id": "AGENT-COO-001", "name": "COO-Agent", "role": "COO"},
                    {"id": "AGENT-CLO-001", "name": "CLO-Agent", "role": "CLO"},
                    {"id": "AGENT-CQO-001", "name": "CQO-Agent", "role": "CQO"},
                    {"id": "AGENT-CRO-001", "name": "CRO-Agent", "role": "CRO"},
                    {"id": "AGENT-STAFF-001", "name": "Staff-001", "role": "Support"},
                ]
            }
        result = track_progress(report_args)
        print("\n📊 进度追踪报告生成完成：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, TypeError) as e:
        print(f"❌ 校验失败：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行异常：{e}", file=sys.stderr)
        sys.exit(1)
