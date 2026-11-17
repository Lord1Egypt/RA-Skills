#!/usr/bin/env python3
"""Bind validated visual-plan intents to the PPT IR used by delivery and builders.

This is deliberately fail-closed: a relationship page without a real renderer must
not silently retain an unrelated chart/table from an earlier PPT IR draft.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


COMPILABLE = {"phase_roadmap", "drill_down_stair", "layered_architecture", "heat_matrix", "causal_chain"}
RELATIONSHIP_EXPRESSIONS = {"relationship_visual", "sequence_visual"}
RELATIONSHIP_LABELS = {
    "feedback_loop": "反馈闭环",
    "cause_effect": "因果链",
    "dependency": "依赖关系",
    "data_flow": "数据流",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _native_component_base(slide: dict[str, Any], component_type: str) -> dict[str, Any]:
    return {
        "id": f"{slide['id']}-{component_type}",
        "type": "diagram",
        "component_type": component_type,
        "semantic_role": component_type,
        "source_refs": list(slide.get("source_refs") or []),
        "editability": "native_required",
        "priority": "primary",
        "delivery_preferences": {
            "preferred_route": "native_diagram",
            "allowed_fallbacks": [],
        },
    }


def _roadmap_object(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    message = str(slide.get("message") or intent.get("message") or "关键阶段").strip()
    return {
        **_native_component_base(slide, "phase_roadmap"),
        "content": {
            "phases": [
                {"label": "当前判断", "detail": message},
                {"label": "关键行动", "detail": "以证据验证并形成决策门禁"},
                {"label": "下一阶段", "detail": "复盘结果并决定是否扩大应用"},
            ],
            "milestones": [
                {"label": "决策门禁", "phase": 1},
            ],
        },
        "diagram_ir": {
            "diagram_id": f"{slide['id']}-phase-roadmap",
            "diagram_type": "timeline",
            "nodes": [
                {
                    "id": "current",
                    "label": "当前判断",
                    "priority": "primary",
                },
                {
                    "id": "action",
                    "label": "关键行动",
                    "priority": "secondary",
                },
                {
                    "id": "next",
                    "label": "下一阶段",
                    "priority": "secondary",
                },
            ],
            "edges": [
                {"id": "current-to-action", "source": "current", "target": "action", "relation": "sequence", "priority": "primary"},
                {"id": "action-to-next", "source": "action", "target": "next", "relation": "sequence", "priority": "secondary"},
            ],
            "main_paths": [
                {"id": "main", "node_ids": ["current", "action", "next"], "priority": "primary"},
            ],
        },
        "complexity": {"node_count": 3, "edge_count": 2},
    }


def _drill_down_object(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    message = str(slide.get("message") or intent.get("message") or "关键判断").strip()
    levels = [
        {"label": "总体判断", "detail": message},
        {"label": "关键维度", "detail": "按证据逐层拆解影响因素"},
        {"label": "行动焦点", "detail": "聚焦最需验证的优先事项"},
    ]
    return {
        **_native_component_base(slide, "drill_down_stair"),
        "content": {"levels": levels},
        "diagram_ir": {
            "diagram_id": f"{slide['id']}-drill-down-stair",
            "diagram_type": "hierarchy",
            "nodes": [
                {"id": f"level-{index}", "label": level["label"], "priority": "primary" if index == 0 else "secondary"}
                for index, level in enumerate(levels)
            ],
            "edges": [
                {"id": f"level-{index}-to-{index + 1}", "source": f"level-{index}", "target": f"level-{index + 1}", "relation": "drill_down", "priority": "primary" if index == 0 else "secondary"}
                for index in range(len(levels) - 1)
            ],
            "main_paths": [{"id": "main", "node_ids": [f"level-{index}" for index in range(len(levels))], "priority": "primary"}],
        },
        "complexity": {"node_count": len(levels), "edge_count": len(levels) - 1},
    }



def _layered_architecture_object(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    message = str(slide.get("message") or intent.get("message") or "关键判断").strip()
    layers = [
        {"label": "业务与体验层", "nodes": [message]},
        {"label": "能力编排层", "nodes": ["规则、流程与协同机制"]},
        {"label": "数据与治理层", "nodes": ["证据、数据与风险控制"]},
    ]
    return {
        **_native_component_base(slide, "layered_architecture"),
        "content": {"boundary_label": "系统能力边界", "layers": layers},
        "diagram_ir": {
            "diagram_id": f"{slide['id']}-layered-architecture",
            "diagram_type": "layered_architecture",
            "nodes": [
                {"id": f"layer-{index}", "label": layer["label"], "priority": "primary" if index == 0 else "secondary"}
                for index, layer in enumerate(layers)
            ],
            "edges": [
                {"id": f"layer-{index}-to-{index + 1}", "source": f"layer-{index}", "target": f"layer-{index + 1}", "relation": "dependency", "priority": "primary" if index == 0 else "secondary"}
                for index in range(len(layers) - 1)
            ],
            "main_paths": [{"id": "main", "node_ids": [f"layer-{index}" for index in range(len(layers))], "priority": "primary"}],
            "groups": [
                {"id": f"layer-group-{index}", "label": layer["label"], "node_ids": [f"layer-{index}"], "group_type": "layer", "visual_role": "container", "layout": "horizontal"}
                for index, layer in enumerate(layers)
            ],
        },
        "complexity": {"node_count": len(layers), "edge_count": len(layers) - 1},
    }


def _causal_chain_object(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    data = intent.get("causal_data")
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
        raise ValueError(f"VISUAL_PLAN_IR_COMPONENT_MISMATCH:{slide['id']}:causal_chain_data")
    nodes = data["nodes"]
    return {
        **_native_component_base(slide, "causal_chain"),
        "content": data,
        "diagram_ir": {
            "diagram_id": f"{slide['id']}-causal-chain",
            "diagram_type": "causal_chain",
            "nodes": [
                {"id": f"node-{index}", "label": str(node["label"]), "role": str(node.get("role") or "mechanism"), "priority": "primary" if index < 3 else "supporting"}
                for index, node in enumerate(nodes)
            ],
            "groups": [],
            "edges": [
                {"id": f"node-{index}-to-{index + 1}", "source": f"node-{index}", "target": f"node-{index + 1}", "relation": "influence", "priority": "primary" if index == 0 else "secondary"}
                for index in range(len(nodes) - 1)
            ],
            "main_paths": [{"id": "main", "node_ids": [f"node-{index}" for index in range(min(3, len(nodes)))], "priority": "primary"}],
        },
        "complexity": {"node_count": len(nodes), "edge_count": len(nodes) - 1},
    }


def _heat_matrix_object(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    data = intent.get("visual_data")
    if not isinstance(data, dict):
        raise ValueError(f"VISUAL_PLAN_IR_COMPONENT_MISMATCH:{slide['id']}:heat_matrix_data")
    return {
        **_native_component_base(slide, "heat_matrix"),
        "type": "shape",
        "content": data,
        "complexity": {
            "row_count": len(data.get("rows") or []),
            "column_count": len(data.get("columns") or []),
        },
    }


def _unsupported_placeholder(slide: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    relationships = intent.get("evidence_refs")
    relation_names = []
    storyline_relationships = slide.get("relationships")
    if isinstance(storyline_relationships, list):
        relation_names = [RELATIONSHIP_LABELS.get(str(item), str(item)) for item in storyline_relationships]
    detail = "、".join(relation_names) if relation_names else "该关系"
    return {
        "id": f"{slide['id']}-unsupported-placeholder",
        "type": "shape",
        "component_type": "comparison_card",
        "semantic_role": "unsupported_component_placeholder",
        "component_status": "unsupported_placeholder",
        "content": {
            "title": "待补齐：关系图组件",
            "claim": (
                f"此处应展示「{detail}」的原生可编辑关系图。当前 PPTSmith 尚未提供经验证的 renderer，"
                "因此未以图表或表格替代。建议联系 MeowClaw / PPTSmith 团队进行专项优化。\n"
                f"原始判断：{slide.get('message') or intent.get('message') or ''}"
            ),
        },
        "source_refs": list(slide.get("source_refs") or []),
        "editability": "native_required",
        "priority": "primary",
        "delivery_preferences": {
            "preferred_route": "native_ppt",
            "allowed_fallbacks": [],
        },
    }


def compile_visual_plan(ppt_ir: dict[str, Any], visual_plan: dict[str, Any]) -> dict[str, Any]:
    intents = visual_plan.get("slides")
    slides = ppt_ir.get("slides")
    if not isinstance(intents, list) or not isinstance(slides, list):
        raise ValueError("VISUAL_PLAN_IR_COMPONENT_MISMATCH: document structure")
    by_id = {slide.get("id"): slide for slide in slides if isinstance(slide, dict) and isinstance(slide.get("id"), str)}
    bind_records: list[dict[str, str]] = []

    for intent in intents:
        if not isinstance(intent, dict):
            raise ValueError("VISUAL_PLAN_IR_COMPONENT_MISMATCH: invalid intent")
        slide_id = intent.get("slide_id")
        if not isinstance(slide_id, str) or slide_id not in by_id:
            raise ValueError("VISUAL_PLAN_IR_COMPONENT_MISMATCH: slide id")
        slide = by_id[slide_id]
        component = intent.get("semantic_component")
        expression = intent.get("primary_expression")
        if not isinstance(component, str) or not isinstance(expression, str):
            raise ValueError(f"VISUAL_PLAN_IR_COMPONENT_MISMATCH:{slide_id}")

        slide["page_design_intent"] = intent
        existing_components = {
            str(obj.get("component_type") or obj.get("type") or "")
            for obj in slide.get("objects", []) or []
            if isinstance(obj, dict)
        }
        if existing_components & {"product_ui_overview", "interaction_storyboard"}:
            bind_records.append({"slide_id": slide_id, "planned_component": component, "actual_component": "design_evidence_prototype"})
            continue
        if component in COMPILABLE:
            compiler = {
                "phase_roadmap": _roadmap_object,
                "drill_down_stair": _drill_down_object,
                "layered_architecture": _layered_architecture_object,
                "heat_matrix": _heat_matrix_object,
                "causal_chain": _causal_chain_object,
            }[component]
            slide["primary_expression"] = "relationship_visual"
            generated = compiler(slide, intent)
            existing = [obj for obj in slide.get("objects", []) or [] if isinstance(obj, dict)]
            # Visual planning may add the dominant semantic component, but it
            # must never discard source-backed evidence or interpretation
            # objects already present in the IR. One primary anchor is a
            # composition rule, not a one-object page rule.
            if not any(obj.get("id") == generated["id"] for obj in existing):
                existing.insert(0, generated)
            slide["objects"] = existing
            bind_records.append({"slide_id": slide_id, "planned_component": component, "actual_component": component})
            continue
        if expression in RELATIONSHIP_EXPRESSIONS and component == "unsupported":
            slide["primary_expression"] = "structured_cards"
            supporting = [
                obj
                for obj in slide.get("objects", []) or []
                if isinstance(obj, dict)
                and (
                    obj.get("priority") != "primary"
                    or str(obj.get("semantic_role") or "").lower()
                    in {"evidence", "interpretation", "source", "source_note"}
                )
            ]
            slide["objects"] = [_unsupported_placeholder(slide, intent), *supporting]
            bind_records.append({"slide_id": slide_id, "planned_component": component, "actual_component": "unsupported_placeholder"})
            continue
        bind_records.append({"slide_id": slide_id, "planned_component": component, "actual_component": "preserved"})

    ppt_ir["visual_plan_bindings"] = bind_records
    return ppt_ir


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Compile visual-plan intents into PPT IR.")
    parser.add_argument("--ppt-ir", type=Path, required=True)
    parser.add_argument("--visual-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        compiled = compile_visual_plan(load_json(args.ppt_ir), load_json(args.visual_plan))
        write_json(args.output, compiled)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"compile_visual_plan: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
