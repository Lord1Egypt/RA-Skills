#!/usr/bin/env python3
"""
conduct_exam.py
接口二：执行考核、自动评分、输出成绩单

【安全标准 — v2.0】
- 输入验证：所有 ID 参数均经白名单校验
- 路径安全：读写路径锁定在 TRAINING_BASE
- 无外部网络：无任何 HTTP/网络调用
- 无敏感凭据：不访问任何凭据文件或 token
- 沙箱评分：rubric 分数硬编码，禁止外部传入计算公式
- 版本标签：所有输出文件含 security_version 字段

版本：v2.0（安全加固版）
"""

import json
import os
import sys
import math
import re
from datetime import datetime, timezone
from typing import Dict, List, Any

# ── 安全配置 ──────────────────────────────────────────────
WORKSPACE_BASE = os.environ.get(
    "TRAINING_WORKSPACE",
    os.path.join(os.path.expanduser("~"), ".qclaw", "workspace")
)
TRAINING_BASE = os.path.join(WORKSPACE_BASE, "knowledge-base", "training")

# ID 白名单正则
RE_SAFE_ID = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
RE_SAFE_ROLE = re.compile(r"^[A-Za-z0-9_\-]{1,32}$")


# ── 安全工具函数 ────────────────────────────────────────────

def validate_id(value: str, name: str) -> str:
    """ID 白名单校验：仅允许字母/数字/连字符/下划线，最大64字符"""
    if not value:
        raise ValueError(f"{name} 不能为空")
    if not RE_SAFE_ID.match(value):
        raise ValueError(f"{name} 包含非法字符：{value!r}")
    return value


def safe_read_json(base_subdir: str, plan_id: str, filename: str) -> Dict:
    """
    安全读取 JSON 文件
    路径锁定在 TRAINING_BASE 下，防止路径遍历
    """
    # plan_id 已经过 validate_id 校验，但仍需路径防御
    safe_plan = re.sub(r"[^A-Za-z0-9_\-]", "_", plan_id)
    rel_path = os.path.join(safe_plan, filename)
    full_path = os.path.normpath(os.path.join(TRAINING_BASE, base_subdir, rel_path))
    base = os.path.normpath(os.path.join(TRAINING_BASE, base_subdir))
    if not full_path.startswith(base):
        raise ValueError(f"路径遍历拦截：{full_path}")
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"文件不存在：{full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_write_dir(exam_id: str, candidate_id: str) -> str:
    """安全创建输出目录，返回规范化路径"""
    safe_exam = re.sub(r"[^A-Za-z0-9_\-]", "_", exam_id)
    safe_cand = re.sub(r"[^A-Za-z0-9_\-]", "_", candidate_id)
    out_dir = os.path.normpath(os.path.join(
        TRAINING_BASE, "exams", safe_exam, safe_cand
    ))
    base = os.path.normpath(os.path.join(TRAINING_BASE, "exams"))
    if not out_dir.startswith(base):
        raise ValueError(f"输出路径越界：{out_dir}")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def safe_write_json(path: str, data: Dict) -> None:
    """安全写入 JSON 到规范化路径"""
    path = os.path.normpath(path)
    base = os.path.normpath(TRAINING_BASE)
    if not path.startswith(base):
        raise ValueError(f"路径遍历拦截：{path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 评分核心（沙箱、无外部依赖）─────────────────────────────

def grade_theory(plan_id: str, candidate_answers: Dict[str, str]) -> Dict:
    """
    理论评分：读取本地 answer_key，比对候选人答案
    candidate_answers: {"T001": "B", "T002": "C", ...}
    """
    answer_key = safe_read_json("plans", plan_id, "exam_answer_key.json")

    all_answers: Dict[str, str] = {}
    for mod in answer_key.get("modules", []):
        all_answers.update(mod.get("theory_answers", {}))

    correct = 0
    wrong_questions = []
    for qid, cand_ans in candidate_answers.items():
        # 校验题目ID格式
        if not RE_SAFE_ID.match(qid):
            continue  # 跳过非法题目ID
        if qid in all_answers and cand_ans.upper() == all_answers[qid].upper():
            correct += 1
        else:
            wrong_questions.append({
                "question_id": qid,
                "candidate_answer": cand_ans or "未作答",
                "correct_answer": all_answers.get(qid, "未知"),
                "result": "WRONG"
            })

    score = correct
    theory_pass_score = 40
    total = len(all_answers)
    weak_areas = list(set(w["question_id"][:3] for w in wrong_questions))

    return {
        "total_questions": total,
        "correct": correct,
        "score": score,
        "max_score": 50,
        "pass_score": theory_pass_score,
        "passed": score >= theory_pass_score,
        "wrong_questions": wrong_questions,
        "weak_areas": weak_areas,
        "accuracy_rate": round(correct / total, 3) if total > 0 else 0.0
    }


def grade_practical(plan_id: str, scenario_answers: Dict[str, Dict]) -> Dict:
    """
    实操评分：读取本地 rubric（仅本地计算，禁止外部传入计算逻辑）
    scenario_answers: {"S-A": {"grade": 8, "grader_comments": "..."}, ...}
    """
    answer_key = safe_read_json("plans", plan_id, "exam_answer_key.json")

    all_rubrics: Dict[str, Dict] = {}
    for mod in answer_key.get("modules", []):
        all_rubrics.update(mod.get("scenario_rubrics", {}))

    results = []
    total_score = 0.0
    total_max = 0

    for scenario_id, answer_data in scenario_answers.items():
        # 校验 scenario_id 格式
        if not RE_SAFE_ID.match(scenario_id):
            continue
        rubric = all_rubrics.get(scenario_id, {})
        max_score = float(sum(rubric.values())) if rubric else 10.0

        # 分数硬编码边界：0 ≤ grade ≤ max_score
        raw_grade = answer_data.get("grade", 0)
        try:
            grade = float(raw_grade)
        except (TypeError, ValueError):
            grade = 0.0
        grade = max(0.0, min(grade, max_score))

        grader = str(answer_data.get("grader", "UNKNOWN"))[:32]
        if not RE_SAFE_ID.match(grader) and grader not in {"CTO+CISO", "UNKNOWN"}:
            grader = "UNKNOWN"

        results.append({
            "scenario_id": scenario_id,
            "score": grade,
            "max_score": max_score,
            "grader": grader,
            "comments": str(answer_data.get("grader_comments", ""))[:200],
            "pass": grade >= max_score * 0.75
        })
        total_score += grade
        total_max += max_score

    practical_pass_score = 37.5
    return {
        "total_scenarios": len(results),
        "score": round(total_score, 1),
        "max_score": total_max,
        "pass_score": practical_pass_score,
        "passed": total_score >= practical_pass_score,
        "scenarios": results,
        "accuracy_rate": round(total_score / total_max, 3) if total_max > 0 else 0.0
    }


def calculate_spd(batch_scores: List[float]) -> float:
    """计算 SPD（Statistical Process Deviation）：本地算术，无外部依赖"""
    if not batch_scores:
        return 0.0
    mean = sum(batch_scores) / len(batch_scores)
    if mean <= 0:
        return 0.0
    variance = sum((s - mean) ** 2 for s in batch_scores) / len(batch_scores)
    return round(math.sqrt(variance) / mean, 4)


def check_quality_gate(batch_results: List[Dict]) -> Dict:
    """质量门禁判定（纯本地计算）"""
    if not batch_results:
        return {
            "pass_gate": False, "pass_rate": 0.0, "avg_spd": 0.0,
            "action": "INSUFFICIENT_DATA",
            "note": "批次无数据，无法判定"
        }
    passed = [r for r in batch_results if r.get("pass", False)]
    pass_rate = len(passed) / len(batch_results)
    all_scores = [float(r.get("total_score", 0)) for r in batch_results]
    avg_spd = calculate_spd(all_scores)
    gate_passed = pass_rate >= 0.90 and avg_spd < 0.10

    return {
        "pass_gate": gate_passed,
        "pass_rate": round(pass_rate, 3),
        "avg_spd": avg_spd,
        "total_in_batch": len(batch_results),
        "passed_count": len(passed),
        "action": "UNLOCK_NEXT_PHASE" if gate_passed else "REOPEN_BATCH",
        "gate_conditions": {
            "pass_rate_required": "≥ 90%",
            "pass_rate_actual": f"{round(pass_rate * 100, 1)}%",
            "spd_required": "< 0.10",
            "spd_actual": avg_spd
        }
    }


def grade_recommendation(
    total_score: float,
    theory_score: int,
    practical_score: float,
    spd: float
) -> Dict:
    """生成考核结论与后续建议（硬编码逻辑，无外部配置）"""
    if total_score >= 90 and spd < 0.05:
        return {
            "grade": "优秀",
            "recommendation": "PASS — 建议纳入优秀案例库，CTO可考虑让其担任学习大使"
        }
    elif total_score >= 77.5:
        if spd >= 0.10:
            return {
                "grade": "合格（波动）",
                "recommendation": "PASS — 关注薄弱环节，1个月后复评"
            }
        return {"grade": "合格", "recommendation": "PASS — 建议纳入合格学员库"}
    elif total_score >= 60:
        return {
            "grade": "待改进",
            "recommendation": "CONDITIONAL — 需参加补训，重新考核未通过模块"
        }
    return {
        "grade": "不合格",
        "recommendation": "FAIL — 需重新参加完整培训（含阶段②全流程）"
    }


# ── 主函数 ──────────────────────────────────────────────────

def conduct_exam(exam_args: Dict) -> Dict:
    """
    执行考核，生成成绩单
    """
    # ① 输入安全校验
    exam_id = validate_id(exam_args.get("exam_id", ""), "exam_id")
    plan_id = validate_id(exam_args.get("plan_id", ""), "plan_id")
    candidate_id = validate_id(exam_args.get("candidate_id", ""), "candidate_id")
    candidate_name = str(exam_args.get("candidate_name", candidate_id))[:64]
    candidate_role = str(exam_args.get("candidate_role", ""))[:32]
    if candidate_role and not RE_SAFE_ROLE.match(candidate_role):
        candidate_role = re.sub(r"[^A-Za-z0-9_\-]", "_", candidate_role)
    mode = str(exam_args.get("mode", "online"))[:16]
    if mode not in {"online", "offline", "hybrid"}:
        mode = "online"

    # ② 加载候选人答案（沙箱：若字段缺失则用空数据，不执行外部逻辑）
    raw_answers = exam_args.get("candidate_answers", {})
    if not isinstance(raw_answers, dict):
        raw_answers = {}
    candidate_answers: Dict[str, str] = {}
    for k, v in raw_answers.items():
        if RE_SAFE_ID.match(str(k)):
            candidate_answers[str(k)] = str(v)[:10]

    raw_scenarios = exam_args.get("scenario_answers", {})
    if not isinstance(raw_scenarios, dict):
        raw_scenarios = {}
    scenario_answers: Dict[str, Dict] = {}
    for k, v in raw_scenarios.items():
        if RE_SAFE_ID.match(str(k)) and isinstance(v, dict):
            scenario_answers[str(k)] = v

    # ③ 评分
    theory_result = grade_theory(plan_id, candidate_answers)
    practical_result = grade_practical(plan_id, scenario_answers)
    total_score = float(theory_result["score"]) + practical_result["score"]
    total_pass = (
        theory_result["passed"]
        and practical_result["passed"]
        and total_score >= 77.5
    )
    spd = calculate_spd([total_score])
    recommendation = grade_recommendation(
        total_score, theory_result["score"],
        practical_result["score"], spd
    )

    # ④ 构成绩单
    score_total: Dict[str, Any] = {
        "exam_id": exam_id, "plan_id": plan_id,
        "candidate_id": candidate_id, "candidate_name": candidate_name,
        "candidate_role": candidate_role,
        "theory_score": theory_result["score"],
        "theory_max": 50, "theory_pass": 40,
        "theory_passed": theory_result["passed"],
        "practical_score": practical_result["score"],
        "practical_max": practical_result["max_score"],
        "practical_pass": 37.5,
        "practical_passed": practical_result["passed"],
        "total_score": total_score, "total_max": 100,
        "total_pass_score": 77.5,
        "pass": total_pass,
        "grade": recommendation["grade"],
        "spd": spd,
        "theory_detail": theory_result,
        "practical_detail": practical_result,
        "recommendation": recommendation["recommendation"],
        "graded_at": datetime.now(timezone.utc).isoformat(),
        "grader_cto": "AUTO (rubric-based)",
        "grader_ciso": "AUTO (rubric-based)",
        "security_version": "v2.0"
    }

    quality_gate: Dict[str, Any] = {
        "note": "单人次质量门禁参考，实际门禁需CHO调用 track_progress 汇总批次后判定",
        "individual_spd": spd,
        "spd_stable": spd < 0.10
    }

    # ⑤ 安全写入输出文件
    out_dir = safe_write_dir(exam_id, candidate_id)
    files: Dict[str, Any] = {
        "score_theory.json": theory_result,
        "score_practical.json": practical_result,
        "score_total.json": score_total,
        "quality_gate_result.json": quality_gate,
        "metadata.json": {
            "exam_id": exam_id, "plan_id": plan_id,
            "candidate_id": candidate_id,
            "conducted_at": datetime.now(timezone.utc).isoformat(),
            "mode": mode, "status": "COMPLETED",
            "security_version": "v2.0"
        }
    }
    for fname, data in files.items():
        safe_write_json(os.path.join(out_dir, fname), data)
        print(f"✅ {fname} → {os.path.join(out_dir, fname)}")

    return {
        "status": "COMPLETED",
        "exam_id": exam_id, "plan_id": plan_id,
        "candidate_id": candidate_id,
        "total_score": total_score,
        "pass": total_pass,
        "grade": recommendation["grade"],
        "spd": spd,
        "recommendation": recommendation["recommendation"],
        "output_dir": out_dir,
        "quality_gate_hint": quality_gate,
        "security_version": "v2.0"
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
                exam_args = json.load(f)
        else:
            exam_args = {
                "exam_id": "EXAM-2026-Q2-001",
                "plan_id": "PLAN-2026-Q2-001",
                "candidate_id": "AGENT-CMO-001",
                "candidate_name": "CMO-Agent",
                "candidate_role": "CMO",
                "mode": "online"
            }
        result = conduct_exam(exam_args)
        print("\n📊 考核结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, TypeError) as e:
        print(f"❌ 校验失败：{e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ 文件未找到：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行异常：{e}", file=sys.stderr)
        sys.exit(1)
