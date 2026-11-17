#!/usr/bin/env python3
"""Shared Diagram IR semantics, complexity, and layout utilities."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

DIAGRAM_TYPES = {
    "process_flow",
    "process_lane",
    "swimlane",
    "timeline",
    "layered_architecture",
    "issue_tree",
    "decision_tree",
    "causal_chain",
    "flywheel",
    "hub_spoke",
    "zoned_ecosystem",
    "capability_landscape",
    "dependency_graph",
    "data_flow",
    "state_transition",
}
ACYCLIC_TYPES = {"process_flow", "timeline", "issue_tree", "decision_tree", "layered_architecture"}
NATIVE_LIMITS = {"max_nodes": 8, "max_edges": 10, "max_groups": 4, "max_boundaries": 2}


def edge_source(edge: dict[str, Any]) -> Any:
    return edge.get("source", edge.get("from"))


def edge_target(edge: dict[str, Any]) -> Any:
    return edge.get("target", edge.get("to"))


def edge_relation(edge: dict[str, Any]) -> Any:
    return edge.get("relation", edge.get("relationship"))


def edge_priority(edge: dict[str, Any]) -> str:
    if edge.get("priority"):
        return edge["priority"]
    if edge.get("semantic_role") == "main_path":
        return "primary"
    return "secondary"


def id_map(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item.get("id"): item for item in items if isinstance(item, dict) and item.get("id")}


def has_cycle(diagram: dict[str, Any]) -> bool:
    graph: dict[str, list[str]] = defaultdict(list)
    nodes = {node.get("id") for node in diagram.get("nodes", []) if isinstance(node, dict)}
    for edge in diagram.get("edges", []) or []:
        if isinstance(edge, dict):
            source = edge_source(edge)
            target = edge_target(edge)
            if source in nodes and target in nodes:
                graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in graph.get(node, []):
            if visit(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def reachable_from_main_path(diagram: dict[str, Any]) -> set[str]:
    main_paths = diagram.get("main_paths") or []
    if not main_paths:
        return set()
    starts = []
    for path in main_paths:
        if isinstance(path, dict) and path.get("priority") == "primary" and path.get("node_ids"):
            starts.append(path["node_ids"][0])
    if not starts:
        return set()
    graph: dict[str, list[str]] = defaultdict(list)
    for edge in diagram.get("edges", []) or []:
        if isinstance(edge, dict):
            graph[edge_source(edge)].append(edge_target(edge))
    seen: set[str] = set()
    queue = deque(starts)
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(graph.get(node, []))
    return seen


def relation_edge_lookup(diagram: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for edge in diagram.get("edges", []) or []:
        if isinstance(edge, dict):
            pairs.add((edge_source(edge), edge_target(edge)))
    return pairs


def analyze_diagram(diagram: dict[str, Any]) -> dict[str, Any]:
    nodes = [node for node in diagram.get("nodes", []) or [] if isinstance(node, dict)]
    edges = [edge for edge in diagram.get("edges", []) or [] if isinstance(edge, dict)]
    groups = [group for group in diagram.get("groups", []) or [] if isinstance(group, dict)]
    boundaries = [b for b in diagram.get("boundaries", []) or [] if isinstance(b, dict)]
    annotations = [a for a in diagram.get("annotations", []) or [] if isinstance(a, dict)]
    node_groups = {node.get("id"): node.get("group_id") for node in nodes}
    cross_group_edges = [
        edge for edge in edges
        if node_groups.get(edge_source(edge)) and node_groups.get(edge_target(edge))
        and node_groups.get(edge_source(edge)) != node_groups.get(edge_target(edge))
    ]
    primary_nodes = [node for node in nodes if node.get("priority") == "primary"]
    primary_edges = [edge for edge in edges if edge_priority(edge) == "primary"]
    node_count = len(nodes)
    edge_count = len(edges)
    max_total_nodes = (diagram.get("layout_constraints") or {}).get("max_total_nodes", 14)
    max_total_edges = (diagram.get("layout_constraints") or {}).get("max_total_edges", 18)
    density_score = (
        0.30 * min(node_count / max(max_total_nodes, 1), 2)
        + 0.30 * min(edge_count / max(max_total_edges, 1), 2)
        + 0.20 * (len(cross_group_edges) / max(edge_count, 1))
        + 0.10 * min(len(annotations) / 5, 2)
        + 0.10 * min(len(boundaries) / 3, 2)
    )
    avg_degree = (edge_count * 2) / max(node_count, 1)
    connector_web_risk = "low"
    if edge_count / max(node_count, 1) > 2 or len(cross_group_edges) > 8 or avg_degree > 3:
        connector_web_risk = "high"
    elif edge_count / max(node_count, 1) > 1.4 or len(cross_group_edges) > 4 or avg_degree > 2.2:
        connector_web_risk = "medium"
    recommended_layout = recommend_layout(diagram)["recommended_type"]
    recommended_delivery_route = "native_diagram"
    if node_count > NATIVE_LIMITS["max_nodes"] or edge_count > NATIVE_LIMITS["max_edges"] or len(groups) > NATIVE_LIMITS["max_groups"]:
        recommended_delivery_route = "hybrid_overlay"
    if node_count > 16 or edge_count > 24 or connector_web_risk == "high":
        recommended_delivery_route = "svg_component"
    return {
        "diagram_id": diagram.get("diagram_id"),
        "node_count": node_count,
        "primary_node_count": len(primary_nodes),
        "edge_count": edge_count,
        "primary_edge_count": len(primary_edges),
        "group_count": len(groups),
        "boundary_count": len(boundaries),
        "annotation_count": len(annotations),
        "cross_group_edge_count": len(cross_group_edges),
        "density_score": round(density_score, 3),
        "connector_web_risk": connector_web_risk,
        "recommended_layout": recommended_layout,
        "recommended_delivery_route": recommended_delivery_route,
        "split_recommended": node_count > 18 or edge_count > 24 or len(groups) > 6 or len(boundaries) > 3,
        "warnings": [],
    }


def recommend_layout(diagram: dict[str, Any]) -> dict[str, Any]:
    groups = [group for group in diagram.get("groups", []) or [] if isinstance(group, dict)]
    edges = [edge for edge in diagram.get("edges", []) or [] if isinstance(edge, dict)]
    nodes = [node for node in diagram.get("nodes", []) or [] if isinstance(node, dict)]
    declared = diagram.get("diagram_type")
    group_types = {group.get("group_type") for group in groups}
    relations = {edge_relation(edge) for edge in edges}
    recommended = declared
    confidence = 0.7
    reasons: list[str] = []
    if declared in {"dependency_graph", "state_transition"}:
        recommended = declared
        confidence = 0.8
        reasons.append("declared type allows cyclic or transition semantics")
    elif declared == "flywheel" or any(edge.get("feedback") for edge in edges) or "feedback" in relations:
        recommended = "flywheel"
        confidence = 0.82
        reasons.append("contains feedback/cycle semantics")
    elif declared == "hub_spoke" or any(node.get("emphasis") == "hero" for node in nodes):
        recommended = "hub_spoke"
        confidence = 0.78
        reasons.append("contains a central or hero node")
    elif "lane" in group_types or declared == "swimlane":
        recommended = "swimlane"
        confidence = 0.84
        reasons.append("contains lane groups or handoff semantics")
    elif "layer" in group_types or declared == "layered_architecture":
        recommended = "layered_architecture"
        confidence = 0.86
        reasons.append("contains layer groups and directional architecture edges")
    elif declared in {"zoned_ecosystem", "capability_landscape"}:
        recommended = declared
        confidence = 0.8
        reasons.append("declared type emphasizes grouping over sequence")
    if not reasons:
        reasons.append("declared type is acceptable")
    alternatives = []
    if recommended != "zoned_ecosystem" and len(groups) >= 4:
        alternatives.append({"type": "zoned_ecosystem", "confidence": 0.54})
    if recommended != "layered_architecture" and "layer" in group_types:
        alternatives.append({"type": "layered_architecture", "confidence": 0.58})
    return {
        "diagram_id": diagram.get("diagram_id"),
        "declared_type": declared,
        "recommended_type": recommended,
        "confidence": confidence,
        "reasons": reasons,
        "alternatives": alternatives,
    }


def validate_diagram_semantics(diagram: dict[str, Any], issue_fn, file: Any, pointer: str = "/", declared_sources: set[str] | None = None) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    base = "" if pointer == "/" else pointer
    declared_sources = declared_sources or set()
    nodes = [node for node in diagram.get("nodes", []) or [] if isinstance(node, dict)]
    groups = [group for group in diagram.get("groups", []) or [] if isinstance(group, dict)]
    edges = [edge for edge in diagram.get("edges", []) or [] if isinstance(edge, dict)]
    boundaries = [b for b in diagram.get("boundaries", []) or [] if isinstance(b, dict)]
    annotations = [a for a in diagram.get("annotations", []) or [] if isinstance(a, dict)]
    node_map = id_map(nodes)
    group_map = id_map(groups)
    edge_map = id_map(edges)
    path_map = id_map([p for p in diagram.get("main_paths", []) or [] if isinstance(p, dict)])
    boundary_map = id_map(boundaries)

    def add(ptr: str, code: str, actual: Any, allowed: Any, repair: str) -> None:
        errors.append(issue_fn(file, f"{base}{ptr}", code, actual, allowed, repair))

    for collection_name, collection in [("nodes", nodes), ("groups", groups), ("edges", edges), ("main_paths", list(path_map.values())), ("boundaries", boundaries), ("annotations", annotations)]:
        seen: set[str] = set()
        for idx, item in enumerate(collection):
            item_id = item.get("id")
            if item_id in seen:
                add(f"/{collection_name}/{idx}/id", f"DIAGRAM_DUPLICATE_{collection_name[:-1].upper()}_ID", item_id, "unique id", "Use unique ids within the diagram.")
            seen.add(item_id)

    primary_nodes = [node for node in nodes if node.get("priority") == "primary"]
    if not primary_nodes:
        add("/nodes", "DIAGRAM_PRIMARY_NODE_MISSING", 0, ">= 1", "Mark at least one node as priority=primary.")

    for idx, node in enumerate(nodes):
        group_id = node.get("group_id")
        if group_id and group_id not in group_map:
            add(f"/nodes/{idx}/group_id", "DIAGRAM_GROUP_REF_NOT_FOUND", group_id, sorted(group_map), "Reference an existing group id.")
        if node.get("node_type") == "decision" and node.get("shape") != "diamond":
            add(f"/nodes/{idx}/shape", "DIAGRAM_DECISION_SHAPE_UNUSUAL", node.get("shape"), "diamond", "Use diamond for decision nodes unless style contract overrides it.")
        if node.get("shape") == "custom" and not node.get("custom_shape_ref"):
            add(f"/nodes/{idx}/custom_shape_ref", "DIAGRAM_CUSTOM_SHAPE_REF_MISSING", None, "custom_shape_ref", "Declare the custom shape reference.")
        for ref_idx, source_id in enumerate(node.get("source_refs", []) or []):
            if declared_sources and source_id not in declared_sources:
                add(f"/nodes/{idx}/source_refs/{ref_idx}", "SOURCE_REF_NOT_FOUND", source_id, sorted(declared_sources), "Use a declared source_id from PPT IR /sources.")

    assigned_nodes: dict[str, str] = {}
    for g_idx, group in enumerate(groups):
        node_ids = group.get("node_ids", []) or []
        if len(node_ids) < 2 and group.get("visual_role") not in {"boundary", "container", "lane"} and group.get("group_type") != "lane":
            add(f"/groups/{g_idx}/node_ids", "DIAGRAM_GROUP_TOO_SMALL", node_ids, ">= 2 nodes or boundary/container group", "Merge tiny groups or mark them as semantic boundary/container.")
        for n_idx, node_id in enumerate(node_ids):
            if node_id not in node_map:
                add(f"/groups/{g_idx}/node_ids/{n_idx}", "DIAGRAM_GROUP_UNKNOWN_NODE", node_id, sorted(node_map), "Use node ids declared under /nodes.")
            if node_id in assigned_nodes and assigned_nodes[node_id] != group.get("id"):
                add(f"/groups/{g_idx}/node_ids/{n_idx}", "DIAGRAM_NODE_IN_MULTIPLE_PRIMARY_GROUPS", node_id, assigned_nodes[node_id], "Use one primary group; express secondary membership with annotations/tags.")
            assigned_nodes[node_id] = group.get("id")

    edge_pairs = relation_edge_lookup(diagram)
    for e_idx, edge in enumerate(edges):
        source = edge_source(edge)
        target = edge_target(edge)
        if source not in node_map:
            add(f"/edges/{e_idx}/source", "DIAGRAM_UNKNOWN_SOURCE_NODE", source, sorted(node_map), "Point the edge source to an existing node.")
        if target not in node_map:
            add(f"/edges/{e_idx}/target", "DIAGRAM_UNKNOWN_TARGET_NODE", target, sorted(node_map), "Point the edge target to an existing node.")
        if source == target and not edge.get("self_loop"):
            add(f"/edges/{e_idx}/self_loop", "DIAGRAM_UNDECLARED_SELF_LOOP", False, True, "Set self_loop=true for intentional self loops.")
        if edge.get("feedback") and edge.get("style") not in {"curved", "auto"}:
            add(f"/edges/{e_idx}/style", "DIAGRAM_FEEDBACK_STYLE_MISMATCH", edge.get("style"), ["curved", "auto"], "Use curved/auto style for feedback edges.")
        if (edge.get("optional") or edge.get("async")) and edge.get("line_semantics") not in {"dashed", "dotted", "muted"}:
            add(f"/edges/{e_idx}/line_semantics", "DIAGRAM_OPTIONAL_STYLE_MISMATCH", edge.get("line_semantics"), ["dashed", "dotted", "muted"], "Use dashed/dotted/muted line semantics for optional or async edges.")
        source_group = node_map.get(source, {}).get("group_id")
        target_group = node_map.get(target, {}).get("group_id")
        if source_group and target_group and source_group != target_group and edge.get("cross_boundary") is not True:
            add(f"/edges/{e_idx}/cross_boundary", "DIAGRAM_CROSS_BOUNDARY_NOT_DECLARED", False, True, "Mark cross-group edges as cross_boundary=true.")

    if edges and all(edge_priority(edge) == "primary" for edge in edges):
        add("/edges", "DIAGRAM_ALL_EDGES_PRIMARY", "all primary", "mixed priorities", "Keep main path edges primary and weaken secondary/supporting edges.")

    main_paths = [path for path in diagram.get("main_paths", []) or [] if isinstance(path, dict)]
    primary_paths = [path for path in main_paths if path.get("priority") == "primary"]
    if not primary_paths:
        add("/main_paths", "DIAGRAM_MAIN_PATH_MISSING", 0, ">= 1 primary main path", "Declare the dominant narrative path.")
    if len(primary_paths) > 1 and diagram.get("diagram_type") not in {"zoned_ecosystem", "capability_landscape"}:
        add("/main_paths", "DIAGRAM_TOO_MANY_PRIMARY_PATHS", len(primary_paths), "1 primary path", "Use one dominant path and mark alternatives secondary.")
    for p_idx, path in enumerate(main_paths):
        path_nodes = path.get("node_ids", []) or []
        for n_idx, node_id in enumerate(path_nodes):
            if node_id not in node_map:
                add(f"/main_paths/{p_idx}/node_ids/{n_idx}", "DIAGRAM_MAIN_PATH_UNKNOWN_NODE", node_id, sorted(node_map), "Use node ids declared under /nodes.")
        for a, b in zip(path_nodes, path_nodes[1:]):
            if (a, b) not in edge_pairs:
                add(f"/main_paths/{p_idx}/node_ids", "DIAGRAM_MAIN_PATH_BROKEN", f"{a}->{b}", "adjacent nodes connected by edge", "Add an edge between adjacent main path nodes or adjust the path.")
        for edge_id in path.get("edge_ids", []) or []:
            if edge_id not in edge_map:
                add(f"/main_paths/{p_idx}/edge_ids", "DIAGRAM_EDGE_REF_NOT_FOUND", edge_id, sorted(edge_map), "Use an edge id declared under /edges.")

    for b_idx, boundary in enumerate(boundaries):
        group_ids = boundary.get("contains_group_ids", []) or []
        node_ids = boundary.get("contains_node_ids", []) or []
        if not group_ids and not node_ids:
            add(f"/boundaries/{b_idx}", "DIAGRAM_EMPTY_BOUNDARY", boundary.get("id"), "group or node member", "Boundary must contain at least one group or node.")
        duplicates = set(group_ids).intersection(node_ids)
        if duplicates:
            add(f"/boundaries/{b_idx}", "DIAGRAM_BOUNDARY_DUPLICATE_MEMBER", sorted(duplicates), "unique members", "Do not list the same id as both group and node.")
        for g_idx, group_id in enumerate(group_ids):
            if group_id not in group_map:
                add(f"/boundaries/{b_idx}/contains_group_ids/{g_idx}", "DIAGRAM_BOUNDARY_UNKNOWN_GROUP", group_id, sorted(group_map), "Use an existing group id.")
        for n_idx, node_id in enumerate(node_ids):
            if node_id not in node_map:
                add(f"/boundaries/{b_idx}/contains_node_ids/{n_idx}", "DIAGRAM_BOUNDARY_UNKNOWN_NODE", node_id, sorted(node_map), "Use an existing node id.")
    if len(boundaries) > 3:
        add("/boundaries", "DIAGRAM_BOUNDARY_OVERLOAD", len(boundaries), "<= 3", "Split the diagram or merge boundaries.")

    targets = {"node": node_map, "edge": edge_map, "group": group_map, "boundary": boundary_map, "diagram": {diagram.get("diagram_id"): diagram}}
    for a_idx, annotation in enumerate(annotations):
        target_type = annotation.get("target_type")
        target_id = annotation.get("target_id")
        if target_id not in targets.get(target_type, {}):
            add(f"/annotations/{a_idx}/target_id", "DIAGRAM_ANNOTATION_TARGET_NOT_FOUND", target_id, sorted(targets.get(target_type, {})), "Reference an existing annotation target.")

    diagram_type = diagram.get("diagram_type")
    group_types = [group.get("group_type") for group in groups]
    if diagram_type == "swimlane" and group_types.count("lane") < 2:
        add("/groups", "DIAGRAM_REQUIRED_LANES_MISSING", group_types.count("lane"), ">= 2 lane groups", "Add lane groups or change diagram_type.")
    if diagram_type == "layered_architecture" and group_types.count("layer") < 2:
        add("/groups", "DIAGRAM_REQUIRED_LAYERS_MISSING", group_types.count("layer"), ">= 2 layer groups", "Add layer groups or change diagram_type.")
    if diagram_type == "decision_tree" and not any(node.get("node_type") == "decision" for node in nodes):
        add("/nodes", "DIAGRAM_DECISION_NODE_MISSING", None, "decision node", "Add at least one decision node.")
    cycle = has_cycle(diagram)
    if diagram_type == "flywheel" and not cycle:
        add("/edges", "DIAGRAM_CYCLE_REQUIRED", False, True, "Flywheel diagrams require a meaningful cycle.")
    if diagram_type in ACYCLIC_TYPES and cycle:
        add("/edges", "DIAGRAM_UNDECLARED_CYCLE", True, "acyclic graph", "Remove the cycle or change diagram_type to flywheel/state_transition/dependency_graph.")

    connected_nodes = {edge_source(edge) for edge in edges} | {edge_target(edge) for edge in edges}
    annotation_targets = {a.get("target_id") for a in annotations if a.get("target_type") == "node"}
    for n_idx, node in enumerate(nodes):
        if node.get("id") not in connected_nodes and node.get("id") not in assigned_nodes and node.get("id") not in annotation_targets and node.get("node_type") != "external":
            add(f"/nodes/{n_idx}", "DIAGRAM_ORPHAN_NODE", node.get("id"), "connected/grouped/annotated node", "Connect, group, annotate, or remove the orphan node.")

    if diagram_type in {"process_flow", "layered_architecture", "dependency_graph"}:
        reachable = reachable_from_main_path(diagram)
        for n_idx, node in enumerate(nodes):
            if node.get("priority") == "primary" and node.get("id") not in reachable:
                add(f"/nodes/{n_idx}", "DIAGRAM_PRIMARY_NODE_UNREACHABLE", node.get("id"), sorted(reachable), "Ensure primary nodes are reachable from the primary main path start.")

    analysis = analyze_diagram(diagram)
    delivery = diagram.get("delivery_contract") if isinstance(diagram.get("delivery_contract"), dict) else {}
    if delivery.get("preferred_route") == "raster_component":
        add(
            "/delivery_contract/preferred_route",
            "DIAGRAM_NATIVE_ROUTE_RASTER_FORBIDDEN",
            "raster_component",
            ["native_diagram", "hybrid_overlay", "svg_component"],
            "Use native_diagram, hybrid_overlay, or svg_component unless the user explicitly approves raster delivery.",
        )
    if analysis["connector_web_risk"] in {"medium", "high"}:
        add("/edges", "DIAGRAM_CONNECTOR_WEB_RISK", analysis["connector_web_risk"], "low", "Define a main path, weaken secondary edges, group nodes, or split the slide.")
    rec = recommend_layout(diagram)
    if rec["recommended_type"] != diagram_type and rec["confidence"] >= 0.8:
        add("/diagram_type", "DIAGRAM_LAYOUT_TYPE_MISMATCH", diagram_type, rec["recommended_type"], "Change diagram_type or adjust groups/relations to match the declared type.")
    return errors


def normalize_diagram(diagram: dict[str, Any]) -> dict[str, Any]:
    normalized = json_clone(diagram)
    for idx, edge in enumerate(normalized.get("edges", []) or []):
        edge.setdefault("id", f"E{idx + 1:02d}")
        relation = edge.get("relation")
        if edge.get("style") in {None, "auto"}:
            edge["style"] = "curved" if relation in {"feedback", "influence", "fallback"} else "orthogonal"
        if "line_semantics" not in edge:
            edge["line_semantics"] = "dashed" if relation in {"response", "dependency", "monitoring", "fallback"} else "solid"
    if "reading_order" not in normalized:
        preferred = (normalized.get("layout_constraints") or {}).get("preferred_layout")
        normalized["reading_order"] = "layer_then_left_to_right" if preferred == "layered" else "main_path_then_supporting"
    normalized["nodes"] = sorted(normalized.get("nodes", []) or [], key=lambda n: (n.get("sequence", 999), n.get("id", "")))
    return normalized


def json_clone(value: Any) -> Any:
    import json

    return json.loads(json.dumps(value, ensure_ascii=False))
