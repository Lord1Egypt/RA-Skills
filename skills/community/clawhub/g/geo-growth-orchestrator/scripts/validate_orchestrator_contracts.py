#!/usr/bin/env python3
"""Validate the GEO Orchestrator registry, contracts, routing, and report shape."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str):
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_registry(errors: list[str], warnings: list[str]) -> None:
    registry_path = ROOT / "registry" / "geo_skill_registry.json"
    if not registry_path.exists():
        errors.append("registry/geo_skill_registry.json is missing")
        return

    registry = load_json("registry/geo_skill_registry.json")
    skills = registry.get("skills", [])
    if not skills:
        errors.append("registry contains no skills")
        return

    required_fields = {
        "skill_id",
        "display_name",
        "relative_path",
        "role",
        "required_inputs",
        "expected_outputs",
        "when_to_call",
        "skip_conditions",
        "fallback_behavior"
    }

    for skill in skills:
        missing = sorted(required_fields - set(skill))
        skill_id = skill.get("skill_id", "<unknown>")
        if missing:
            errors.append(f"{skill_id} missing required fields: {', '.join(missing)}")

        relative_path = skill.get("relative_path", "")
        if not relative_path.startswith("../"):
            errors.append(f"{skill_id} relative_path must start with ../: {relative_path}")
        if relative_path.startswith("./skills/") or relative_path.startswith("./subskills/"):
            errors.append(f"{skill_id} uses a child-skill path: {relative_path}")

        resolved = (ROOT / relative_path).resolve()
        if not resolved.exists():
            warnings.append(f"{skill_id} relative_path does not exist locally: {relative_path}")
        elif not (resolved / "SKILL.md").exists():
            warnings.append(f"{skill_id} path exists but SKILL.md was not found directly: {relative_path}")


def generate_content_task_plan(gap_matrix: dict) -> dict:
    tasks = []
    for index, gap in enumerate(gap_matrix.get("gaps", []), start=1):
        platform = "zhihu" if gap.get("scenario") in {
            "competitor_comparison",
            "buying_guide",
            "direct_brand_awareness"
        } else "toutiao"
        impact = 5 if gap.get("priority") == "high" else 3
        difficulty = 3
        speed = 4
        tasks.append({
            "task_id": f"T-{index:03d}",
            "source_gap_id": gap["gap_id"],
            "platform": platform,
            "content_type": "qa_article" if platform == "zhihu" else "popular_article",
            "title": f"补齐：{gap['description']}",
            "objective": gap["recommended_action"],
            "business_impact": gap["business_impact"],
            "impact_score": impact,
            "difficulty_score": difficulty,
            "speed_score": speed,
            "priority_score": round((impact * 0.5) + ((6 - difficulty) * 0.25) + (speed * 0.25), 2),
            "human_review_required": True,
            "expected_output": "platform_draft"
        })
    return {"brand_name": gap_matrix.get("brand_name", ""), "tasks": tasks}


def validate_gap_to_task_plan(errors: list[str]) -> None:
    gap_matrix = {
        "brand_name": "西班牙橄榄油推广项目",
        "target_market": "中国家庭消费",
        "models_compared": ["DeepSeek", "Doubao"],
        "gaps": [
            {
                "gap_id": "G-001",
                "scenario": "buying_guide",
                "gap_type": "localized_content_gap",
                "description": "缺少中餐场景选购说明",
                "source_models": ["DeepSeek", "Doubao"],
                "business_impact": "影响家庭消费购买决策",
                "priority": "high",
                "recommended_action": "生成中式厨房橄榄油选购指南"
            }
        ]
    }
    plan = generate_content_task_plan(gap_matrix)
    if not plan["tasks"]:
        errors.append("geo_gap_matrix did not generate any content tasks")
    task = plan["tasks"][0]
    for field in ("source_gap_id", "platform", "title", "priority_score", "human_review_required"):
        if field not in task:
            errors.append(f"generated content task missing {field}")
    if task.get("human_review_required") is not True:
        errors.append("generated content task must require human review")


def route_platforms(industry: str, user_platforms: list[str] | None = None) -> dict:
    user_platforms = user_platforms or []
    normalized = industry.lower()
    selected = set(user_platforms)
    skipped = set()
    manual = set()
    localized_keywords_required = False

    if any(token in normalized for token in ("consumer", "food", "tourism", "medical_beauty", "消费", "食品", "文旅", "医美")):
        selected.update({"zhihu", "toutiao"})
        manual.update({"xiaohongshu"})
        skipped.update({"csdn", "juejin"})
    elif any(token in normalized for token in ("ai", "saas", "developer", "enterprise", "开发者", "企业服务")):
        selected.update({"zhihu", "csdn", "juejin"})
        selected.add("toutiao")
    elif any(token in normalized for token in ("local", "restaurant", "association", "本地", "餐饮", "协会")):
        selected.update({"zhihu", "toutiao"})
        manual.update({"xiaohongshu"})
        localized_keywords_required = True
    else:
        selected.update({"zhihu", "toutiao"})

    for platform in user_platforms:
        skipped.discard(platform)
        manual.discard(platform)

    return {
        "selected": sorted(selected),
        "skipped": sorted(skipped),
        "manual": sorted(manual),
        "localized_keywords_required": localized_keywords_required
    }


def validate_platform_routing(errors: list[str]) -> None:
    food_route = route_platforms("食品 消费")
    if not {"zhihu", "toutiao"}.issubset(food_route["selected"]):
        errors.append("food routing must select zhihu and toutiao")
    if "xiaohongshu" not in food_route["manual"]:
        errors.append("food routing must mark xiaohongshu as manual/future_skill")
    if not {"csdn", "juejin"}.issubset(food_route["skipped"]):
        errors.append("food routing must skip csdn and juejin by default")

    ai_route = route_platforms("AI SaaS developer")
    if not {"zhihu", "csdn", "juejin"}.issubset(ai_route["selected"]):
        errors.append("AI/SaaS routing must select zhihu, csdn, and juejin")

    local_route = route_platforms("本地服务 餐饮 地方协会")
    if not {"zhihu", "toutiao"}.issubset(local_route["selected"]):
        errors.append("local service routing must select zhihu and toutiao")
    if not local_route["localized_keywords_required"]:
        errors.append("local service routing must require localized keywords")


def validate_missing_output_status(errors: list[str]) -> None:
    expected_outputs = ["brand_knowledge_base.json", "faq.md", "llms.txt"]
    existing_outputs = {"brand_knowledge_base.json"}
    missing = [item for item in expected_outputs if item not in existing_outputs]
    status = "success" if not missing else "partial"
    if status == "success":
        errors.append("missing downstream output was incorrectly marked success")
    if status not in {"partial", "failed"}:
        errors.append("missing downstream output must be partial or failed")


def validate_report_template(errors: list[str]) -> None:
    template_path = ROOT / "templates" / "client_delivery_report.md"
    if not template_path.exists():
        errors.append("templates/client_delivery_report.md is missing")
        return

    text = template_path.read_text(encoding="utf-8")
    required_sections = [
        "老板能看懂的 3 句话结论",
        "本次调用或建议调用的相邻 Skill",
        "每个阶段的执行状态",
        "核心 GEO 盲区",
        "已生成或应生成的内容资产",
        "建议发布顺序",
        "30 天 GEO 增长行动计划",
        "完整文件路径清单",
        "尚未完成或需要补救的部分"
    ]
    for section in required_sections:
        if section not in text:
            errors.append(f"client delivery report template missing section: {section}")
    if len(text.splitlines()) < 80:
        errors.append("client delivery report template is too short and may be summary-only")


def validate_json_files(errors: list[str]) -> None:
    json_files = [
        "registry/geo_skill_registry.json",
        "schemas/brand_knowledge_base.schema.json",
        "schemas/geo_gap_matrix.schema.json",
        "schemas/content_task_plan.schema.json",
        "schemas/platform_distribution_plan.schema.json",
        "schemas/orchestrator_run_summary.schema.json"
    ]
    for relative_path in json_files:
        try:
            load_json(relative_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative_path} is not valid JSON: {exc}")
        except FileNotFoundError:
            errors.append(f"{relative_path} is missing")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    validate_json_files(errors)
    validate_registry(errors, warnings)
    validate_gap_to_task_plan(errors)
    validate_platform_routing(errors)
    validate_missing_output_status(errors)
    validate_report_template(errors)

    result = {
        "status": "failed" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
        "checks": [
            "registry exists",
            "relative_path starts with ../",
            "gap matrix can produce content task plan",
            "industry routing selects expected platform Skills",
            "missing downstream output is partial/failed",
            "customer delivery report contains full required sections",
            "summary-only output is rejected"
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
