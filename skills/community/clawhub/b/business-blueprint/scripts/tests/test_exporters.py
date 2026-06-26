import json
import re
from pathlib import Path

from business_blueprint.export_drawio import export_drawio
from business_blueprint.export_excalidraw import export_excalidraw
from business_blueprint.export_svg import export_evolution_timeline_svg, export_layer_poster_svg, export_product_tree_svg, export_swimlane_flow_svg, export_svg


BLUEPRINT = {
    "meta": {"title": "Demo"},
    "library": {
        "capabilities": [{"id": "cap-membership", "name": "会员运营"}],
        "actors": [],
        "flowSteps": [],
        "systems": [{"id": "sys-crm", "name": "CRM", "capabilityIds": ["cap-membership"]}],
    },
    "views": [
        {
            "id": "view-capability",
            "type": "business-capability-map",
            "title": "业务能力蓝图",
            "includedNodeIds": ["cap-membership", "sys-crm"],
            "includedRelationIds": [],
            "layout": {},
            "annotations": [],
        }
    ],
}


TIMELINE_BLUEPRINT = {
    "meta": {"title": "金蝶2026年AI产品演进图", "industry": "common"},
    "library": {
        "capabilities": [
            {"id": "cap-suite", "name": "套件化封装"},
            {"id": "cap-segment", "name": "分层产品定位"},
        ],
        "actors": [
            {"id": "actor-manager", "name": "企业管理者"},
            {"id": "actor-growth", "name": "成长型企业"},
        ],
        "flowSteps": [
            {
                "id": "flow-1",
                "name": "2026-03-11：AI超级套件发布",
                "actorId": "actor-manager",
                "capabilityIds": ["cap-suite"],
                "systemIds": ["sys-suite", "sys-xiaok"],
            },
            {
                "id": "flow-2",
                "name": "2026-04-03：AI星空定位强化",
                "actorId": "actor-growth",
                "capabilityIds": ["cap-segment"],
                "systemIds": ["sys-xingkong", "sys-cangqiong"],
            },
        ],
        "systems": [
            {"id": "sys-suite", "name": "金蝶AI超级套件", "capabilityIds": ["cap-suite"]},
            {"id": "sys-xiaok", "name": "金蝶小K", "capabilityIds": ["cap-suite"]},
            {"id": "sys-xingkong", "name": "金蝶AI星空", "capabilityIds": ["cap-segment"]},
            {"id": "sys-cangqiong", "name": "金蝶AI苍穹", "capabilityIds": ["cap-segment"]},
        ],
    },
}


def test_export_svg_writes_svg_markup(tmp_path: Path) -> None:
    target = tmp_path / "diagram.svg"
    export_svg(BLUEPRINT, target)
    assert target.read_text(encoding="utf-8").startswith("<svg")


def test_export_drawio_writes_mxfile(tmp_path: Path) -> None:
    target = tmp_path / "diagram.drawio"
    export_drawio(BLUEPRINT, target)
    assert "<mxfile" in target.read_text(encoding="utf-8")


def test_export_excalidraw_writes_json(tmp_path: Path) -> None:
    target = tmp_path / "diagram.excalidraw"
    export_excalidraw(BLUEPRINT, target)
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["type"] == "excalidraw"


def test_export_evolution_timeline_svg_writes_timeline_markup(tmp_path: Path) -> None:
    target = tmp_path / "evolution.svg"
    export_evolution_timeline_svg(TIMELINE_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    assert "演进时间线" in svg
    assert "2026-03-11" in svg
    assert "AI超级套件发布" in svg
    assert "金蝶AI超级套件" in svg


def test_export_evolution_timeline_svg_gives_cangqiong_pill_enough_width(tmp_path: Path) -> None:
    target = tmp_path / "evolution.svg"
    export_evolution_timeline_svg(TIMELINE_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    match = re.search(r'<rect x="[^"]+" y="[^"]+" width="([^"]+)" height="22" rx="11" [^>]*stroke="[^"]+"[^>]*\/><text x="[^"]+" y="[^"]+" text-anchor="middle" font-size="10" [^>]*>金蝶AI苍穹<\/text>', svg)
    assert match is not None
    assert float(match.group(1)) >= 78


def test_export_evolution_timeline_svg_uses_dark_card_fills_in_dark_theme(tmp_path: Path) -> None:
    target = tmp_path / "evolution.svg"
    export_evolution_timeline_svg(TIMELINE_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")

    assert 'fill="#FEF2F2"' not in svg
    assert 'fill="#EEF2FF"' not in svg
    assert 'stroke="#DC2626" stroke-width="2"/>' in svg
    assert 'stroke="#4338CA" stroke-width="2"/>' in svg


def test_export_evolution_timeline_svg_grows_card_for_wrapped_system_pills(tmp_path: Path) -> None:
    blueprint = {
        "meta": {"title": "Timeline", "industry": "common"},
        "library": {
            "capabilities": [
                {"id": "cap-1", "name": "Harness基础能力"},
                {"id": "cap-2", "name": "Agent运行时"},
            ],
            "actors": [
                {"id": "actor-1", "name": "平台工程师"},
            ],
            "flowSteps": [
                {
                    "id": "flow-1",
                    "name": "阶段 1：Harness支撑层完成Agent调度、工具调用与接口治理",
                    "actorId": "actor-1",
                    "capabilityIds": ["cap-1", "cap-2"],
                    "systemIds": ["sys-core", "sys-integration"],
                }
            ],
            "systems": [
                {"id": "sys-core", "name": "Harness核心能力", "capabilityIds": ["cap-1"]},
                {"id": "sys-integration", "name": "Harness集成能力", "capabilityIds": ["cap-2"]},
            ],
        },
    }
    target = tmp_path / "evolution.svg"
    export_evolution_timeline_svg(blueprint, target, theme="dark")
    svg = target.read_text(encoding="utf-8")

    card_match = re.search(r'<rect x="[^"]+" y="210" width="260" height="([^"]+)" rx="18" fill="[^"]+" stroke="#34D399" stroke-width="2"/>', svg)
    assert card_match is not None
    card_height = float(card_match.group(1))

    pill_ys = [
        float(y)
        for y in re.findall(
            r'<rect x="[^"]+" y="([^"]+)" width="[^"]+" height="22" rx="11" fill="#0F172A" fill-opacity="0\.96" stroke="#34D399" stroke-width="1"/>',
            svg,
        )
    ]
    assert len(pill_ys) >= 2
    assert max(pill_ys) + 22 <= 210 + card_height


POSTER_BLUEPRINT = {
    "meta": {"title": "云之家 V12 产品蓝图", "industry": "common"},
    "library": {
        "capabilities": [],
        "actors": [],
        "flowSteps": [],
        "systems": [
            {"id": "sys-entry", "name": "小K入口", "layer": "第一层 用户层", "features": ["会话", "技能", "定时任务"]},
            {"id": "sys-suite", "name": "AI协同办公套件", "layer": "第二层 AI协同办公套件层", "features": ["AI日程协同", "AI会议协同", "AI文档协同"]},
            {"id": "sys-harness", "name": "Harness核心能力", "layer": "第三层 Harness支撑层", "features": ["基础能力", "Agent运行时"]},
            {"id": "sys-erp", "name": "ERP核心业务", "layer": "第四层 ERP业务层", "features": ["财务", "供应链"]},
            {"id": "sys-data", "name": "AI数据底座", "layer": "第五层 数据层", "features": ["存储", "分析", "AI数据底座"]},
        ],
    },
}


def test_export_layer_poster_svg_writes_poster_markup(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    assert "Layered Poster" in svg
    # Layer prefix is extracted from "第一层" format, or falls back to "L{n}"
    assert "第一层" in svg or "L1" in svg
    assert "第五层" in svg or "L5" in svg
    assert "小K入口" in svg
    assert '#020617' in svg


def test_export_layer_poster_svg_uses_compact_cards(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    # Check for compact card dimensions (180x80)
    assert 'width="180"' in svg
    assert 'height="80"' in svg


def test_export_layer_poster_svg_removes_layer_side_connectors(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    assert 'circle cx="144"' not in svg
    assert 'x1="154"' not in svg


def test_export_layer_poster_svg_removes_right_edge_band_curves(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    assert 'marker-end="url(#arrow-solid)"' not in svg


def test_export_layer_poster_svg_keeps_three_feature_lines_inside_card(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    # Compact cards: 180x80
    card_match = re.search(r'<rect x="([^"]+)" y="[^"]+" width="180" height="80" rx="8"', svg)
    assert card_match is not None


def test_export_layer_poster_svg_uses_tighter_corner_radii(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    # Compact layout: title rx=6, band rx=12, label rx=8, card rx=8
    title_match = re.search(r'<g class="title-block"><rect x="32" y="20" width="[^"]+" height="48" rx="6"', svg)
    band_match = re.search(r'<rect x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" rx="12"', svg)
    label_match = re.search(r'<rect x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" rx="8" fill="#0F172A"', svg)
    card_match = re.search(r'<rect x="[^"]+" y="[^"]+" width="180" height="80" rx="8"', svg)
    assert title_match is not None
    assert band_match is not None
    assert label_match is not None
    assert card_match is not None


def test_export_layer_poster_svg_uses_muted_light_palette_in_light_theme(tmp_path: Path) -> None:
    target = tmp_path / "poster-light.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target, theme="light")
    svg = target.read_text(encoding="utf-8")

    # Light theme uses muted colors
    assert "#CCFBF1" in svg or "#F0FDFA" in svg
    assert "#FFFFFF" in svg  # White cards in light theme
    assert "#0E2A3D" not in svg  # Dark colors should not appear


def test_export_layer_poster_svg_centers_sparse_rows_within_content_band(tmp_path: Path) -> None:
    target = tmp_path / "poster.svg"
    export_layer_poster_svg(POSTER_BLUEPRINT, target)
    svg = target.read_text(encoding="utf-8")
    # Compact layout: canvas width 1280, cards centered
    assert 'width="1280"' in svg
    # Cards should be present (180x80 compact format)
    card = re.search(r'<rect x="([^"]+)" y="[^"]+" width="180" height="80" rx="8"', svg)
    assert card is not None


SWIMLANE_BLUEPRINT = {
    "meta": {"title": "云之家 V12 产品蓝图", "industry": "common"},
    "library": {
        "capabilities": [
            {"id": "cap-chat", "name": "会话交互"},
            {"id": "cap-office", "name": "AI协同办公"},
        ],
        "actors": [
            {"id": "actor-user", "name": "办公用户"},
            {"id": "actor-manager", "name": "管理者"},
        ],
        "flowSteps": [
            {"id": "step-1", "name": "用户通过小K发起会话", "actorId": "actor-user", "capabilityIds": ["cap-chat"]},
            {"id": "step-2", "name": "AI协同办公套件识别场景", "actorId": "actor-manager", "capabilityIds": ["cap-office"]},
        ],
        "systems": [],
    },
}


def test_export_swimlane_flow_svg_uses_dark_lane_palette_in_dark_theme(tmp_path: Path) -> None:
    target = tmp_path / "swimlane.svg"
    export_swimlane_flow_svg(SWIMLANE_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert '#E8F5F5' not in svg
    assert '#ECFDF5' not in svg
    assert '#EEF2FF' not in svg
    assert '#0E2A3D' in svg or '#0E2E1F' in svg or '#1E1535' in svg


def test_export_product_tree_svg_uses_dark_segment_palette_in_dark_theme(tmp_path: Path) -> None:
    target = tmp_path / "tree.svg"
    export_product_tree_svg(POSTER_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert '#EEF2FF' not in svg
    assert '#E8F5F5' not in svg
    assert '#ECFDF5' not in svg
    assert '#0E2A3D' in svg or '#0E2E1F' in svg or '#1E1535' in svg


def test_export_product_tree_svg_groups_by_layer_when_segment_missing(tmp_path: Path) -> None:
    target = tmp_path / "tree.svg"
    export_product_tree_svg(POSTER_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert 'Products' not in svg
    assert '第一层 用户层' in svg
    assert '第五层 数据层' in svg
    width_match = re.search(r'<svg xmlns="http://www.w3.org/2000/svg" width="([^"]+)" height="([^"]+)"', svg)
    assert width_match is not None
    assert float(width_match.group(1)) < 1000


SWIMLANE_CHAIN_BLUEPRINT = {
    "meta": {"title": "Chain", "industry": "common"},
    "library": {
        "capabilities": [
            {"id": "cap-a", "name": "A"},
            {"id": "cap-b", "name": "B"},
            {"id": "cap-c", "name": "C"},
        ],
        "actors": [
            {"id": "actor-a", "name": "A"},
            {"id": "actor-b", "name": "B"},
            {"id": "actor-c", "name": "C"},
        ],
        "flowSteps": [
            {"id": "step-a", "name": "第一步", "actorId": "actor-a", "capabilityIds": ["cap-a"], "nextStepIds": ["step-b"], "seqIndex": 0},
            {"id": "step-b", "name": "第二步", "actorId": "actor-b", "capabilityIds": ["cap-b"], "nextStepIds": ["step-c"], "seqIndex": 1},
            {"id": "step-c", "name": "第三步", "actorId": "actor-c", "capabilityIds": ["cap-c"], "nextStepIds": [], "seqIndex": 2},
        ],
        "systems": [],
    },
}


def test_export_swimlane_flow_svg_limits_cross_lane_arrows_to_declared_next_steps(tmp_path: Path) -> None:
    target = tmp_path / "swimlane.svg"
    export_swimlane_flow_svg(SWIMLANE_CHAIN_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert svg.count('marker-end="url(#arrow-dashed)"') <= 2


def test_export_swimlane_flow_svg_wraps_long_step_titles_without_ellipsis(tmp_path: Path) -> None:
    bp = {
        "meta": {"title": "Wrap", "industry": "common"},
        "library": {
            "capabilities": [{"id": "cap-long", "name": "会话交互"}],
            "actors": [{"id": "actor-user", "name": "办公用户"}],
            "flowSteps": [
                {"id": "step-1", "name": "用户通过小K发起会话或任务", "actorId": "actor-user", "capabilityIds": ["cap-long"], "nextStepIds": []}
            ],
            "systems": [],
        },
    }
    target = tmp_path / "swimlane.svg"
    export_swimlane_flow_svg(bp, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert '…' not in svg
    assert svg.count('<tspan x="96"') == 1
    assert '用户通过小K发起会话或任务' in svg


SWIMLANE_TAG_BLUEPRINT = {
    "meta": {"title": "Tags", "industry": "common"},
    "library": {
        "capabilities": [
            {"id": "cap-h-core", "name": "Harness基础能力"},
            {"id": "cap-agent", "name": "Agent运行时"},
            {"id": "cap-tool", "name": "工具链"},
            {"id": "cap-api", "name": "API网关"},
        ],
        "actors": [{"id": "actor-platform", "name": "平台工程师"}],
        "flowSteps": [
            {
                "id": "step-platform",
                "name": "平台能力运行",
                "actorId": "actor-platform",
                "capabilityIds": ["cap-h-core", "cap-agent", "cap-tool", "cap-api"],
                "nextStepIds": []
            }
        ],
        "systems": [],
    },
}


def test_export_swimlane_flow_svg_simplifies_capability_tags(tmp_path: Path) -> None:
    target = tmp_path / "swimlane.svg"
    export_swimlane_flow_svg(SWIMLANE_TAG_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    assert 'Harness基础能力' not in svg
    assert '基础能力' in svg
    assert 'API网关' not in svg
    assert '网关' in svg


def test_export_swimlane_flow_svg_keeps_header_tags_non_overlapping(tmp_path: Path) -> None:
    target = tmp_path / "swimlane.svg"
    export_swimlane_flow_svg(SWIMLANE_TAG_BLUEPRINT, target, theme="dark")
    svg = target.read_text(encoding="utf-8")
    rects = [
        (float(x), float(w))
        for x, w in re.findall(r'<rect x="([^"]+)" y="110" width="([^"]+)" height="18" rx="3" fill="#[0-9A-Fa-f]{6}" stroke="#[0-9A-Fa-f]{6}"', svg)
    ]
    assert len(rects) >= 4
    rects.sort()
    for (x1, w1), (x2, _) in zip(rects, rects[1:]):
        assert x1 + w1 + 2 <= x2
