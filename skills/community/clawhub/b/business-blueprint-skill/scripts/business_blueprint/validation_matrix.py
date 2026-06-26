from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

try:
    from .export_html import export_html_viewer
    from .export_knowledge import is_knowledge_blueprint
    from .export_routes import resolve_export_route
    from .export_svg import export_svg_auto
    from .render_png import render_svg_to_png
    from .template_catalog import TEMPLATE_NAMES
    from .validate import validate_blueprint
except ImportError:
    from export_html import export_html_viewer
    from export_knowledge import is_knowledge_blueprint
    from export_routes import resolve_export_route
    from export_svg import export_svg_auto
    from render_png import render_svg_to_png
    from template_catalog import TEMPLATE_NAMES
    from validate import validate_blueprint


DEFAULT_TEMPLATE_PROFILES: dict[str, dict[str, str]] = {
    "common": {"visualProfile": "dark-ops", "theme": "dark", "templateName": TEMPLATE_NAMES["common"]},
    "retail": {"visualProfile": "warm-consulting", "theme": "light", "templateName": TEMPLATE_NAMES["retail"]},
    "finance": {"visualProfile": "executive-clean", "theme": "light", "templateName": TEMPLATE_NAMES["finance"]},
    "manufacturing": {"visualProfile": "blueprint-technical", "theme": "dark", "templateName": TEMPLATE_NAMES["manufacturing"]},
    "cross-border-ecommerce": {"visualProfile": "knowledge-canvas", "theme": "light", "templateName": TEMPLATE_NAMES["cross-border-ecommerce"]},
}


def build_template_validation_matrix(
    *,
    output_dir: Path,
    render_png: bool = False,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    for industry, config in DEFAULT_TEMPLATE_PROFILES.items():
        blueprint = _blueprint_for_industry(industry)
        blueprint_type = blueprint.get("meta", {}).get("blueprintType", "architecture")
        visual_profile = config["visualProfile"]
        theme = config["theme"]

        target_dir = output_dir / industry
        target_dir.mkdir(parents=True, exist_ok=True)
        blueprint_path = target_dir / "solution.blueprint.json"
        svg_path = target_dir / "solution.svg"
        html_path = target_dir / "solution.html"

        blueprint_path.write_text(
            json.dumps(blueprint, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        export_svg_auto(
            copy.deepcopy(blueprint),
            svg_path,
            theme=theme,
            industry=industry,
            visual_profile=visual_profile,
        )
        export_html_viewer(
            copy.deepcopy(blueprint),
            html_path,
            theme=theme,
            visual_profile=visual_profile,
        )

        validation = validate_blueprint(blueprint)
        route = "knowledge" if is_knowledge_blueprint(blueprint) else resolve_export_route(blueprint).route
        png_status = "disabled"
        png_path: str | None = None
        if render_png:
            result = render_svg_to_png(svg_path)
            png_status = result.reason
            png_path = str(result.png_path) if result.ok and result.png_path else None

        counts = _entity_counts(blueprint)
        entries.append(
            {
                "industry": industry,
                "templateId": industry,
                "templateName": config["templateName"],
                "blueprintType": blueprint_type,
                "complexity": "medium",
                "visualProfile": visual_profile,
                "theme": theme,
                "route": route,
                "blueprintPath": str(blueprint_path),
                "svgPath": str(svg_path),
                "htmlPath": str(html_path),
                "pngPath": png_path,
                "pngStatus": png_status,
                "validation": {
                    **counts,
                    "errorCount": validation["summary"]["errorCount"],
                    "warningCount": validation["summary"]["warningCount"],
                },
            }
        )

    summary = {
        "version": "1.0",
        "entryCount": len(entries),
        "templates": list(DEFAULT_TEMPLATE_PROFILES),
        "entries": entries,
    }
    (output_dir / "template-validation-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def _entity_counts(blueprint: dict[str, Any]) -> dict[str, int]:
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}
    knowledge_count = 0
    if isinstance(knowledge, dict):
        knowledge_count = sum(len(v) for v in knowledge.values() if isinstance(v, list))
    return {
        "capabilityCount": len(library.get("capabilities", []) or []),
        "actorCount": len(library.get("actors", []) or []),
        "flowStepCount": len(library.get("flowSteps", []) or []),
        "systemCount": len(library.get("systems", []) or []),
        "knowledgeEntityCount": knowledge_count,
        "relationCount": len(blueprint.get("relations", []) or []),
    }


def _blueprint_for_industry(industry: str) -> dict[str, Any]:
    if industry == "common":
        return _architecture_blueprint(
            industry="common",
            title="企业协同运营中台蓝图",
            goals=["统一任务入口", "打通审批与数据看板", "提升跨部门响应速度"],
            actors=["业务负责人", "运营专员", "IT 管理员"],
            capabilities=["统一工作台", "流程审批", "数据看板", "权限治理", "消息触达"],
            systems=[
                ("协同门户", "frontend", [0, 4]),
                ("流程引擎", "backend", [1]),
                ("指标服务", "analytics", [2]),
                ("身份权限中心", "security", [3]),
                ("企业消息网关", "integration", [4]),
            ],
            steps=["提交任务", "自动分派", "审批流转", "指标汇总", "消息反馈"],
        )
    if industry == "retail":
        return _architecture_blueprint(
            industry="retail",
            title="全渠道门店履约蓝图",
            goals=["线上线下一盘货", "减少缺货与超卖", "提升会员复购"],
            actors=["店长", "导购", "会员运营"],
            capabilities=["门店库存", "会员触达", "订单履约", "促销编排", "售后服务"],
            systems=[
                ("POS 收银", "frontend", [0, 2]),
                ("OMS 订单中心", "backend", [2]),
                ("WMS 仓储", "database", [0, 2]),
                ("会员营销平台", "analytics", [1, 3]),
                ("客服工单", "integration", [4]),
                ("履约可视化看板", "analytics", [2, 4]),
            ],
            steps=["会员识别", "库存锁定", "门店拣货", "履约通知", "售后跟进"],
        )
    if industry == "finance":
        return _architecture_blueprint(
            industry="finance",
            title="小微信贷风控蓝图",
            goals=["缩短授信周期", "提升风险识别", "满足审计留痕"],
            actors=["客户经理", "风控专员", "合规审计"],
            capabilities=["客户画像", "授信评估", "反欺诈", "审批决策", "贷后预警"],
            systems=[
                ("客户进件端", "frontend", [0]),
                ("评分卡服务", "backend", [1]),
                ("反欺诈引擎", "security", [2]),
                ("决策流平台", "backend", [3]),
                ("贷后监控仓", "database", [4]),
                ("模型监控台", "analytics", [1, 4]),
            ],
            steps=["资料进件", "画像聚合", "风险评分", "额度审批", "贷后监测"],
        )
    if industry == "manufacturing":
        return _architecture_blueprint(
            industry="manufacturing",
            title="柔性制造排产蓝图",
            goals=["稳定交付节拍", "降低换线损耗", "提升设备可视化"],
            actors=["计划员", "车间主管", "质量工程师"],
            capabilities=["需求计划", "产能排程", "设备联动", "质量追溯", "物料齐套"],
            systems=[
                ("APS 排产", "analytics", [0, 1]),
                ("MES 执行", "backend", [1, 2]),
                ("设备 IoT 平台", "integration", [2]),
                ("QMS 质量", "security", [3]),
                ("WMS 物料", "database", [4]),
            ],
            steps=["订单拆解", "产能匹配", "工单下发", "过程采集", "质量放行"],
        )
    if industry == "cross-border-ecommerce":
        return _cross_border_knowledge_blueprint()
    raise ValueError(f"Unsupported industry template: {industry}")


def _architecture_blueprint(
    *,
    industry: str,
    title: str,
    goals: list[str],
    actors: list[str],
    capabilities: list[str],
    systems: list[tuple[str, str, list[int]]],
    steps: list[str],
) -> dict[str, Any]:
    actor_items = [{"id": f"actor-{idx + 1}", "name": name} for idx, name in enumerate(actors)]
    cap_items = [
        {
            "id": f"cap-{idx + 1}",
            "name": name,
            "level": 1,
            "description": f"{name}能力域",
            "ownerActorIds": [actor_items[idx % len(actor_items)]["id"]],
            "supportingSystemIds": [],
        }
        for idx, name in enumerate(capabilities)
    ]

    system_items = []
    for idx, (name, category, cap_indexes) in enumerate(systems):
        cap_ids = [cap_items[cap_idx]["id"] for cap_idx in cap_indexes]
        system_id = f"sys-{idx + 1}"
        for cap_id in cap_ids:
            next(cap for cap in cap_items if cap["id"] == cap_id)["supportingSystemIds"].append(system_id)
        system_items.append(
            {
                "id": system_id,
                "kind": "system",
                "name": name,
                "category": category,
                "aliases": [],
                "description": f"{name}支撑{industry}场景",
                "resolution": {"status": "canonical", "canonicalName": name},
                "capabilityIds": cap_ids,
            }
        )

    flow_items = []
    for idx, name in enumerate(steps):
        cap_id = cap_items[idx % len(cap_items)]["id"]
        sys_id = system_items[idx % len(system_items)]["id"]
        flow_items.append(
            {
                "id": f"flow-{idx + 1}",
                "name": name,
                "actorId": actor_items[idx % len(actor_items)]["id"],
                "capabilityIds": [cap_id],
                "systemIds": [sys_id],
                "stepType": "task",
                "seqIndex": idx + 1,
                "inputRefs": [],
                "outputRefs": [],
            }
        )

    relations = []
    rel_index = 1
    for system in system_items:
        for cap_id in system["capabilityIds"]:
            relations.append(
                {
                    "id": f"rel-{rel_index}",
                    "type": "supports",
                    "from": system["id"],
                    "to": cap_id,
                    "label": "支撑",
                }
            )
            rel_index += 1
    for left, right in zip(system_items, system_items[1:]):
        relations.append(
            {
                "id": f"rel-{rel_index}",
                "type": "depends",
                "from": left["id"],
                "to": right["id"],
                "label": "数据协同",
            }
        )
        rel_index += 1
    for step in flow_items[:3]:
        relations.append(
            {
                "id": f"rel-{rel_index}",
                "type": "realizes",
                "from": step["capabilityIds"][0],
                "to": step["id"],
                "label": "落地流程",
            }
        )
        rel_index += 1

    return {
        "version": "1.0",
        "meta": {
            "title": title,
            "industry": industry,
            "templateId": industry,
            "templateName": DEFAULT_TEMPLATE_PROFILES[industry]["templateName"],
            "blueprintType": "architecture",
            "revisionId": "rev-validation-001",
            "lastModifiedBy": "ai",
        },
        "context": {
            "goals": goals,
            "scope": [title],
            "assumptions": ["用于模板视觉与导出链路验证"],
            "constraints": ["中等复杂度，不覆盖超大图分页场景"],
            "sourceRefs": [{"id": "src-1", "excerpt": f"{title}验证样例"}],
            "clarifyRequests": [],
            "clarifications": [],
        },
        "library": {
            "capabilities": cap_items,
            "actors": actor_items,
            "flowSteps": flow_items,
            "systems": system_items,
        },
        "relations": relations,
        "views": [
            {
                "id": "view-capability-map",
                "type": "business-capability-map",
                "includedNodeIds": [cap["id"] for cap in cap_items],
            }
        ],
        "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
        "artifacts": {},
    }


def _cross_border_knowledge_blueprint() -> dict[str, Any]:
    return {
        "version": "1.0",
        "meta": {
            "title": "跨境电商广告增长 know-how 蓝图",
            "industry": "cross-border-ecommerce",
            "templateId": "cross-border-ecommerce",
            "templateName": DEFAULT_TEMPLATE_PROFILES["cross-border-ecommerce"]["templateName"],
            "blueprintType": "domain-knowledge",
            "detectedIntent": "梳理跨境电商广告投放从痛点、策略、规则到指标的可执行增长方法。",
            "revisionId": "rev-validation-001",
        },
        "context": {
            "goals": ["稳定 ROAS", "提升素材迭代效率", "降低平台政策风险"],
            "scope": ["Meta/TikTok/Google Ads 投放运营"],
            "assumptions": ["样例用于模板视觉和知识图导出验证"],
            "constraints": ["不同平台政策需人工复核"],
            "sourceRefs": [{"id": "src-1", "excerpt": "跨境电商广告增长方法论验证样例"}],
            "clarifyRequests": [
                {
                    "id": "clarify-1",
                    "targetEntityId": "pain-roas",
                    "question": "目标市场的 ROAS 盈亏平衡线是多少？",
                    "rationale": "不同品类毛利会改变优化目标。",
                },
                {
                    "id": "clarify-2",
                    "targetEntityId": "rule-policy",
                    "question": "当前主投平台是否存在类目投放限制？",
                    "rationale": "政策红线会影响素材与落地页策略。",
                },
                {
                    "id": "clarify-3",
                    "targetEntityId": "metric-cac",
                    "question": "是否按新客 CAC 与复购 LTV 分开看指标？",
                    "rationale": "混合指标会掩盖投放质量。",
                },
            ],
            "clarifications": [],
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
            "knowledge": {
                "painPoints": [
                    {"id": "pain-roas", "name": "ROAS 波动", "entityType": "painPoint", "severity": "high"},
                    {"id": "pain-creative", "name": "素材疲劳", "entityType": "painPoint", "severity": "medium"},
                    {"id": "pain-policy", "name": "政策误伤", "entityType": "painPoint", "severity": "high"},
                ],
                "strategies": [
                    {"id": "strategy-attribution", "name": "统一归因模型", "entityType": "strategy"},
                    {"id": "strategy-creative", "name": "AIGC 素材工厂", "entityType": "strategy"},
                    {"id": "strategy-risk", "name": "政策预审机制", "entityType": "strategy"},
                ],
                "rules": [
                    {"id": "rule-policy", "name": "平台政策红线", "entityType": "rule"},
                    {"id": "rule-budget", "name": "预算止损阈值", "entityType": "rule"},
                    {"id": "rule-localization", "name": "本地化承诺校验", "entityType": "rule"},
                ],
                "metrics": [
                    {"id": "metric-roas", "name": "ROAS 提升", "entityType": "metric"},
                    {"id": "metric-cac", "name": "新客 CAC", "entityType": "metric"},
                    {"id": "metric-fatigue", "name": "素材衰减率", "entityType": "metric"},
                ],
                "practices": [
                    {"id": "practice-sprint", "name": "7 天素材 Sprint", "entityType": "practice"},
                    {"id": "practice-dashboard", "name": "日报归因看板", "entityType": "practice"},
                ],
                "pitfalls": [
                    {"id": "pitfall-lastclick", "name": "只看末次点击", "entityType": "pitfall"},
                    {"id": "pitfall-copy", "name": "跨市场复制素材", "entityType": "pitfall"},
                ],
            },
        },
        "relations": [
            {"id": "rel-1", "from": "strategy-attribution", "to": "pain-roas", "type": "solves"},
            {"id": "rel-2", "from": "strategy-creative", "to": "pain-creative", "type": "solves"},
            {"id": "rel-3", "from": "strategy-risk", "to": "pain-policy", "type": "solves"},
            {"id": "rel-4", "from": "strategy-attribution", "to": "metric-roas", "type": "measures"},
            {"id": "rel-5", "from": "strategy-attribution", "to": "metric-cac", "type": "measures"},
            {"id": "rel-6", "from": "strategy-creative", "to": "metric-fatigue", "type": "measures"},
            {"id": "rel-7", "from": "rule-policy", "to": "strategy-risk", "type": "enforces"},
            {"id": "rel-8", "from": "rule-budget", "to": "strategy-attribution", "type": "enforces"},
            {"id": "rel-9", "from": "practice-sprint", "to": "strategy-creative", "type": "supports"},
            {"id": "rel-10", "from": "pitfall-lastclick", "to": "pain-roas", "type": "causes"},
        ],
        "views": [],
        "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
        "artifacts": {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="template-validation-matrix")
    parser.add_argument("--output", required=True)
    parser.add_argument("--png", action="store_true", help="Attempt optional CairoSVG PNG rendering.")
    args = parser.parse_args()

    summary = build_template_validation_matrix(
        output_dir=Path(args.output),
        render_png=args.png,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
