#!/usr/bin/env python3
"""CCCC Gates — show plan/milestone/final/safety gate status."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", subprocess.getoutput("git rev-parse --show-toplevel 2>/dev/null || pwd")).strip())
WORKSPACE = ROOT / "docs/cccc"


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def lang() -> str:
    cfg = read_json(WORKSPACE / "config.json")
    if cfg:
        return cfg.get("language", {}).get("user_language", "zh")
    return "zh"


def check_plan_gate(cfg: dict, st: dict):
    print("Plan review gate:")
    plan_status = st.get("codex_plan_review_status", "not_run")
    plan_file = st.get("last_codex_plan_review_file")
    roadmap_status = st.get("roadmap_status", "not_reviewed")
    impl_allowed = plan_status == "pass"

    print(f"  Codex plan review: {plan_status}")
    if plan_file:
        exists = Path(plan_file).exists() if not plan_file.startswith("/tmp") else True
        print(f"  Review file: {plan_file} ({'exists' if exists else 'missing'})")
    else:
        print(f"  Review file: (none)")

    print(f"  Roadmap status: {roadmap_status}")
    print(f"  Implementation allowed: {'yes' if impl_allowed else 'no'}")
    if not impl_allowed:
        if plan_status == "not_run":
            print(f"  原因: Codex plan review 尚未执行。运行 /cc-codex-collaborate plan-review")
        elif plan_status == "fail":
            print(f"  原因: Codex plan review 未通过。修复后重新提交。")
        elif plan_status == "needs_human":
            print(f"  原因: Codex plan review 需要人工干预。")
        else:
            print(f"  原因: plan review 状态为 {plan_status}")
    print()


def check_milestone_gate(cfg: dict, st: dict):
    print("Milestone review gate:")
    mid = st.get("current_milestone_id")
    review_status = st.get("current_milestone_codex_review_status", "not_run")
    review_file = st.get("current_milestone_codex_review_file")
    pass_allowed = review_status == "pass"

    print(f"  Current milestone: {mid or '(none)'}")
    if not mid:
        print(f"  Milestone pass allowed: no — no current milestone")
        print(f"  原因: 当前没有活跃 milestone")
        print()
        return

    print(f"  Codex review: {review_status}")
    if review_file:
        exists = Path(review_file).exists() if not review_file.startswith("/tmp") else True
        print(f"  Review file: {review_file} ({'exists' if exists else 'missing'})")
    else:
        print(f"  Review file: (none)")

    print(f"  Milestone pass allowed: {'yes' if pass_allowed else 'no'}")
    if not pass_allowed:
        if review_status == "not_run":
            print(f"  原因: Codex milestone review 尚未执行。不允许直接标记 milestone passed。")
        elif review_status == "fail":
            print(f"  原因: Codex milestone review 未通过。修复后重新提交 review。")
        elif review_status == "needs_human":
            print(f"  原因: Codex milestone review 需要人工干预。")
        else:
            print(f"  原因: review 状态为 {review_status}")
    print()


def check_final_gate(cfg: dict, st: dict):
    print("Final review gate:")
    final_status = st.get("codex_final_review_status", "not_run")
    final_file = st.get("last_codex_final_review_file")
    completion_allowed = final_status == "pass"

    print(f"  Codex final review: {final_status}")
    if final_file:
        exists = Path(final_file).exists() if not final_file.startswith("/tmp") else True
        print(f"  Review file: {final_file} ({'exists' if exists else 'missing'})")
    else:
        print(f"  Review file: (none)")

    print(f"  Task completion allowed: {'yes' if completion_allowed else 'no'}")
    if not completion_allowed:
        if final_status == "not_run":
            print(f"  原因: Codex final review 尚未执行。")
        elif final_status == "fail":
            print(f"  原因: Codex final review 未通过。")
        else:
            print(f"  原因: final review 状态为 {final_status}")
    print()


def check_safety_gate(st: dict):
    print("Safety gate:")
    status = st.get("status", "UNKNOWN")
    pause_reason = st.get("pause_reason")
    blocked = status in ("NEEDS_SECRET", "SENSITIVE_OPERATION", "UNSAFE",
                         "PAUSED_FOR_HUMAN", "NEEDS_HUMAN", "PAUSED_FOR_SYSTEM")

    print(f"  Status: {status}")
    print(f"  Pause reason: {pause_reason or '无'}")

    if blocked:
        print(f"  Safe to continue: no")
        print(f"  原因: 状态 {status} 需要人工处理。")
    else:
        print(f"  Safe to continue: yes")
    print()


def check_testing_gate(st: dict):
    print("Testing gate:")
    # Check if there's recent test info in context or reviews
    reviews_dir = WORKSPACE / "reviews" / "milestones"
    latest_review = None
    if reviews_dir.exists():
        for f in sorted(reviews_dir.glob("*.json"), reverse=True):
            data = read_json(f)
            if data:
                latest_review = data
                break

    if latest_review:
        test_assessment = latest_review.get("test_assessment", "not_evaluated")
        print(f"  Latest review test assessment: {test_assessment}")
    else:
        print(f"  No milestone review artifacts found")

    cont = st.get("stop_hook_continuations", 0)
    max_cont = 10
    print(f"  Continuation budget: {cont} used")
    print()


def main():
    cfg = read_json(WORKSPACE / "config.json")
    st = read_json(WORKSPACE / "state.json")

    if not cfg or not st:
        print("ERROR: docs/cccc/config.json 或 state.json 不存在或无效。", file=sys.stderr)
        print("运行 /cc-codex-collaborate setup", file=sys.stderr)
        return 1

    print("当前 Gates：")
    print()

    check_plan_gate(cfg, st)
    check_milestone_gate(cfg, st)
    check_final_gate(cfg, st)
    check_safety_gate(st)
    check_testing_gate(st)

    # Next steps
    plan_ok = st.get("codex_plan_review_status") == "pass"
    ms_ok = st.get("current_milestone_codex_review_status") == "pass"
    final_ok = st.get("codex_final_review_status") == "pass"
    mid = st.get("current_milestone_id")

    print("下一步：")
    if not plan_ok:
        print("  - 运行 Codex plan review 后才能开始实现")
    elif not mid:
        print("  - 没有活跃 milestone，运行 /cc-codex-collaborate resume 或开始新任务")
    elif not ms_ok:
        print(f"  - 运行 Codex milestone review (milestone {mid})，不允许直接标记 passed")
    elif not final_ok:
        print("  - 所有 milestone review 通过后运行 Codex final review")
    else:
        print("  - 所有 gate 通过，可以完成任务")

    return 0


if __name__ == "__main__":
    sys.exit(main())
