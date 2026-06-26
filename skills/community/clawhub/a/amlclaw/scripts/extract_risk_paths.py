#!/usr/bin/env python3
"""
extract_risk_paths.py
--------------------
Reads the raw graph JSON from `fetch_graph.py` and the user's `rules.json`.
Extracts every node within 1-5 hops that matches any rule condition.
Supports scenario-based filtering: only applies rules matching the business scenario.
Outputs a deduplicated, LLM-friendly `risk_paths_*.json` for report generation.
"""
import argparse
import json
import os
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Scenario → Category mapping
# ---------------------------------------------------------------------------
SCENARIO_CATEGORIES = {
    "onboarding":  ["Deposit"],                  # onboarding = deposit rules (DEP-SELF-* + inflow + outflow history)
    "deposit":     ["Deposit"],
    "withdrawal":  ["Withdrawal"],
    "cdd":         ["CDD"],
    "monitoring":  ["Ongoing Monitoring"],
    "all":         None,                         # no filtering (legacy default)
}

# ---------------------------------------------------------------------------
# Scenario → allowed path directions (-1 = inflow, 1 = outflow)
# ---------------------------------------------------------------------------
SCENARIO_PATH_FILTER = {
    "onboarding":  None,    # both directions
    "deposit":     None,    # both directions (rules self-filter via direction field)
    "withdrawal":  [1],     # outflow only
    "cdd":         None,    # both directions
    "monitoring":  None,    # both directions
    "all":         None,    # both directions
}


def load_rules(rules_path: str):
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_graph(graph_path: str):
    with open(graph_path, "r", encoding="utf-8") as f:
        return json.load(f)


def prioritize_tag(tags):
    """Return the tag dict with the lowest `priority` value."""
    if not tags:
        return None
    def pr(tag):
        try:
            return int(tag.get("priority", 9999))
        except Exception:
            return 9999
    return min(tags, key=pr)


# ---------------------------------------------------------------------------
# Condition parameters evaluable at the node level (path traversal).
# ---------------------------------------------------------------------------
NODE_LEVEL_PARAMS = {
    "path.node.tags.primary_category",
    "path.node.tags.secondary_category",
    "path.node.tags.risk_level",
}

# ---------------------------------------------------------------------------
# Condition parameters evaluable at the target level (target self-tags).
# ---------------------------------------------------------------------------
TARGET_LEVEL_PARAMS = {
    "target.tags.primary_category",
    "target.tags.secondary_category",
    "target.tags.risk_level",
}


def eval_condition(cond, node_tag, node_deep):
    """
    Evaluate a single condition against a node.
    Returns:
        True  — condition matches
        False — condition does not match
        None  — condition is not node-evaluable (skip)
    """
    param = cond.get("parameter", "")
    op = cond.get("operator", "")
    value = cond.get("value")

    if param not in NODE_LEVEL_PARAMS:
        return None  # not evaluable at node level — skip

    # --- Tag matching ---
    if param == "path.node.tags.primary_category":
        actual = node_tag.get("primary_category") if node_tag else None
        if actual is None:
            return False
        if op == "IN":
            return actual in value
        elif op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "NOT_IN":
            return actual not in value
        return False

    if param == "path.node.tags.secondary_category":
        actual = node_tag.get("secondary_category") if node_tag else None
        if actual is None:
            return False
        if op == "IN":
            return actual in value
        elif op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "NOT_IN":
            return actual not in value
        return False

    if param == "path.node.tags.risk_level":
        actual = node_tag.get("risk_level") if node_tag else None
        if actual is None:
            return False
        if op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "IN":
            return actual in value
        return False

    return None


def eval_target_condition(cond, target_tag):
    """
    Evaluate a single target-level condition against a target tag.
    Returns:
        True  — condition matches
        False — condition does not match
        None  — condition is not target-evaluable (skip)
    """
    param = cond.get("parameter", "")
    op = cond.get("operator", "")
    value = cond.get("value")

    if param not in TARGET_LEVEL_PARAMS:
        return None

    if param == "target.tags.primary_category":
        actual = target_tag.get("primary_category") if target_tag else None
        if actual is None:
            return False
        if op == "IN":
            return actual in value
        elif op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "NOT_IN":
            return actual not in value
        return False

    if param == "target.tags.secondary_category":
        actual = target_tag.get("secondary_category") if target_tag else None
        if actual is None:
            return False
        if op == "IN":
            return actual in value
        elif op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "NOT_IN":
            return actual not in value
        return False

    if param == "target.tags.risk_level":
        actual = target_tag.get("risk_level") if target_tag else None
        if actual is None:
            return False
        if op == "==":
            return actual == value
        elif op == "!=":
            return actual != value
        elif op == "IN":
            return actual in value
        return False

    return None


def rule_has_target_conditions(rule):
    """Check if a rule contains any target-level conditions."""
    for cond in rule.get("conditions", []):
        if cond.get("parameter", "") in TARGET_LEVEL_PARAMS:
            return True
    return False


def rule_matches_target_tag(rule, target_tag):
    """
    Match a rule against a single target tag.
    Only evaluates target-level conditions (AND logic).
    Non-target conditions are skipped.
    """
    conditions = rule.get("conditions", [])
    if not conditions:
        return False

    target_conditions_evaluated = 0

    for cond in conditions:
        result = eval_target_condition(cond, target_tag)
        if result is None:
            continue
        target_conditions_evaluated += 1
        if not result:
            return False

    return target_conditions_evaluated > 0


def evaluate_target_rules(rules, target_tags):
    """
    Evaluate rules against the target address's own tags.
    Returns a list of findings: [{tag, matched_rules}]
    """
    target_rules = [r for r in rules if rule_has_target_conditions(r)]
    if not target_rules or not target_tags:
        return []

    findings = []
    for tag in target_tags:
        matched_rule_ids = []
        for rule in target_rules:
            if rule_matches_target_tag(rule, tag):
                matched_rule_ids.append(rule.get("rule_id"))
        if matched_rule_ids:
            findings.append({
                "tag": {
                    "primary_category": tag.get("primary_category", ""),
                    "secondary_category": tag.get("secondary_category", ""),
                    "tertiary_category": tag.get("tertiary_category", ""),
                    "quaternary_category": tag.get("quaternary_category", ""),
                    "risk_level": tag.get("risk_level", ""),
                },
                "matched_rules": sorted(matched_rule_ids),
            })

    return findings


def rule_applies_to_context(rule, path_dir, node_deep):
    """
    Check if a rule applies to the current path direction and hop distance.
    Uses top-level rule fields: direction, min_hops, max_hops.
    Rules without these fields match any context (direction-agnostic, hop-agnostic).
    """
    # Direction check: -1 = inflow, 1 = outflow
    rule_dir = rule.get("direction")
    if rule_dir:
        dir_map = {"inflow": -1, "outflow": 1}
        if dir_map.get(rule_dir) != path_dir:
            return False

    # Hop range check
    min_h = rule.get("min_hops")
    max_h = rule.get("max_hops")
    if min_h is not None and node_deep < min_h:
        return False
    if max_h is not None and node_deep > max_h:
        return False

    return True


def rule_matches_node(rule, node_tag, node_deep):
    """
    Match a rule against a node's tag and computed deep value.

    Logic:
    - Evaluate all node-level conditions (AND logic).
    - If ANY node-level condition fails → no match.
    - If ZERO node-level conditions exist → no match (rule is not node-evaluable).
    - Non-node conditions are skipped (LLM evaluates them later).
    """
    conditions = rule.get("conditions", [])
    if not conditions:
        return False

    node_conditions_evaluated = 0

    for cond in conditions:
        result = eval_condition(cond, node_tag, node_deep)
        if result is None:
            continue  # non-node-level condition, skip
        node_conditions_evaluated += 1
        if not result:
            return False  # AND logic: one fail = rule fails

    # Must have evaluated at least one node-level condition
    return node_conditions_evaluated > 0


def format_evidence_path(nodes, illicit_index, path_direction):
    """
    Format the evidence string for the fund flow.
    INFLOW (-1): [Source, ..., Target] — show from illicit node to target.
    OUTFLOW (1): [Target, ..., Destination] — show from target to illicit node.
    """
    if path_direction == -1:
        relevant_nodes = nodes[illicit_index:]
    elif path_direction == 1:
        relevant_nodes = nodes[:illicit_index + 1]
    else:
        relevant_nodes = nodes

    parts = []
    for i, n in enumerate(relevant_nodes):
        addr = n.get("address", "Unknown")
        amount = n.get("amount", 0)
        if amount is None:
            amount = 0

        tags = n.get("tags", [])
        label_str = ""
        if tags:
            best_tag = prioritize_tag(tags)
            if best_tag:
                lbl = (best_tag.get("quaternary_category")
                       or best_tag.get("tertiary_category")
                       or best_tag.get("secondary_category")
                       or best_tag.get("primary_category"))
                if lbl:
                    label_str = f" ({lbl})"

        if i > 0:
            parts.append(f"--({amount} USD)-->")
        parts.append(f"[{addr}{label_str}]")

    return " ".join(parts)


def compute_true_deep(node_index, num_nodes, path_dir, raw_deep):
    """
    Compute hop distance from target based on position in path array.
    Falls back to positional calculation when API deep field is unreliable (all zeros).

    Inflow (-1): path = [Source(far), ..., Target(near)]
        → hop distance = num_nodes - 1 - node_index
    Outflow (1): path = [Target(near), ..., Dest(far)]
        → hop distance = node_index
    """
    if path_dir == -1:  # inflow
        return num_nodes - 1 - node_index
    else:  # outflow
        return node_index


def extract_risk_paths(graph_data, rules, max_depth=5, scenario="all"):
    """
    Core extraction: walk every path, compute true hop distances,
    match nodes against rules, deduplicate by address.
    Supports scenario-based category filtering and path direction filtering.
    """
    data = graph_data.get("graph_data", {}).get("data", {})
    target_address = graph_data.get("address", "")

    # --- Scenario: filter rules by category ---
    categories = SCENARIO_CATEGORIES.get(scenario)
    rules_total_loaded = len(rules)
    if categories:
        rules = [r for r in rules if r.get("category") in categories]
    rules_after_filter = len(rules)

    # --- Scenario: determine allowed path directions ---
    allowed_dirs = SCENARIO_PATH_FILTER.get(scenario)

    # --- Target self-tag evaluation ---
    target_tags_raw = data.get("tags", [])
    target_findings = evaluate_target_rules(rules, target_tags_raw)
    target_self_matched_rules = set()
    for tf in target_findings:
        target_self_matched_rules.update(tf["matched_rules"])

    # --- Path traversal ---
    findings = {}  # address -> { tag, deep_min, matched_rules: set, evidence_paths: [], occurrences }

    all_paths = data.get("paths", [])
    paths_direction_filtered = 0

    for path_idx, path in enumerate(all_paths):
        nodes = path.get("path", [])
        path_dir = path.get("direction", -1)

        if not nodes:
            continue

        # Filter paths by scenario direction
        if allowed_dirs and path_dir not in allowed_dirs:
            paths_direction_filtered += 1
            continue

        num_nodes = len(nodes)

        for node_idx, node in enumerate(nodes):
            addr = node.get("address", "")

            # Skip the target address itself — it's the investigation subject
            if addr == target_address:
                continue

            raw_deep = node.get("deep")
            true_deep = compute_true_deep(node_idx, num_nodes, path_dir, raw_deep)

            if true_deep is None or true_deep < 1 or true_deep > max_depth:
                continue

            tag = prioritize_tag(node.get("tags", []))
            if not tag:
                continue

            # Match rules (check direction + hop range, then node-level conditions)
            matched_rule_ids = []
            for rule in rules:
                if not rule_applies_to_context(rule, path_dir, true_deep):
                    continue
                if rule_matches_node(rule, tag, true_deep):
                    matched_rule_ids.append(rule.get("rule_id"))

            if not matched_rule_ids:
                continue

            # Build evidence path string
            evidence = format_evidence_path(nodes, node_idx, path_dir)

            # Aggregate into findings dict
            key = addr
            if key not in findings:
                findings[key] = {
                    "address": addr,
                    "min_deep": true_deep,
                    "tag": {
                        "primary_category": tag.get("primary_category", ""),
                        "secondary_category": tag.get("secondary_category", ""),
                        "tertiary_category": tag.get("tertiary_category", ""),
                        "quaternary_category": tag.get("quaternary_category", ""),
                        "risk_level": tag.get("risk_level", ""),
                    },
                    "matched_rules": set(),
                    "evidence_paths": [],
                    "occurrences": 0,
                }

            entry = findings[key]
            entry["matched_rules"].update(matched_rule_ids)
            entry["min_deep"] = min(entry["min_deep"], true_deep)
            entry["occurrences"] += 1

            # Keep evidence paths but cap per entity to avoid explosion
            if len(entry["evidence_paths"]) < 3:
                entry["evidence_paths"].append({
                    "path_index": path_idx,
                    "deep": true_deep,
                    "flow": evidence,
                })

    # Convert sets to sorted lists and sort findings by severity
    severity_order = {"severe": 0, "high": 1, "medium": 2, "low": 3}
    result = []
    for f in findings.values():
        f["matched_rules"] = sorted(f["matched_rules"])
        result.append(f)

    result.sort(key=lambda x: (
        severity_order.get(x["tag"].get("risk_level", "low"), 3),
        x["min_deep"],
    ))

    # Build summary
    all_triggered = set()
    for f in result:
        all_triggered.update(f["matched_rules"])
    # Include target self-matched rules in triggered set
    all_triggered.update(target_self_matched_rules)

    highest_severity = "Low"
    for f in result:
        rl = f["tag"].get("risk_level", "low").lower()
        if rl in ("severe", "high") and severity_order.get(rl, 3) < severity_order.get(highest_severity.lower(), 3):
            highest_severity = {"severe": "Severe", "high": "High", "medium": "Medium", "low": "Low"}.get(rl, "Low")

    # Check rules for highest action
    rule_severity = {}
    for rule in rules:
        rule_severity[rule["rule_id"]] = rule.get("risk_level", "Low")
    for rid in all_triggered:
        rs = rule_severity.get(rid, "Low")
        if severity_order.get(rs.lower(), 3) < severity_order.get(highest_severity.lower(), 3):
            highest_severity = rs

    summary = {
        "scenario": scenario,
        "categories_applied": categories if categories else ["ALL"],
        "total_paths_analyzed": len(all_paths),
        "paths_direction_filtered": paths_direction_filtered,
        "unique_risk_entities": len(result),
        "rules_loaded": rules_after_filter,
        "rules_total_available": rules_total_loaded,
        "rules_triggered": sorted(all_triggered),
        "highest_severity": highest_severity,
    }

    return result, summary, target_findings, target_tags_raw


def main():
    parser = argparse.ArgumentParser(description="Extract risk-relevant paths within 1-5 hops.")
    parser.add_argument("--graph", required=True, help="Path to raw_graph JSON file.")
    parser.add_argument("--rules", default="rules.json", help="Path to rules.json (default: ./rules.json).")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum hop depth to consider.")
    parser.add_argument("--scenario", choices=list(SCENARIO_CATEGORIES.keys()), default="all",
                        help="Business scenario filter (default: all).")
    args = parser.parse_args()

    if not os.path.isfile(args.graph):
        print(json.dumps({"error": f"Graph file not found: {args.graph}"}))
        sys.exit(1)
    if not os.path.isfile(args.rules):
        print(json.dumps({"error": f"Rules file not found: {args.rules}"}))
        sys.exit(1)

    graph = load_graph(args.graph)
    rules = load_rules(args.rules)

    risk_entities, summary, target_findings, target_tags_raw = extract_risk_paths(
        graph, rules, max_depth=args.max_depth, scenario=args.scenario
    )

    # Prepare output path — reuse the same timestamp from the raw_graph filename
    base_name = os.path.basename(args.graph)
    stem = base_name.replace(".json", "").replace("raw_graph_", "")
    out_name = f"risk_paths_{stem}.json"
    out_dir = os.path.join(os.getcwd(), "graph_data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_name)

    # Build target block with self-tags and self-matched rules
    target_self_matched = set()
    target_tags_formatted = []
    for tag in target_tags_raw:
        target_tags_formatted.append({
            "primary_category": tag.get("primary_category", ""),
            "secondary_category": tag.get("secondary_category", ""),
            "tertiary_category": tag.get("tertiary_category", ""),
            "quaternary_category": tag.get("quaternary_category", ""),
            "risk_level": tag.get("risk_level", ""),
        })
    for tf in target_findings:
        target_self_matched.update(tf["matched_rules"])

    output = {
        "target": {
            "chain": graph.get("chain", ""),
            "address": graph.get("address", ""),
            "tags": target_tags_formatted,
            "self_matched_rules": sorted(target_self_matched),
        },
        "scenario": args.scenario,
        "summary": summary,
        "risk_entities": risk_entities,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(json.dumps({"status": "success", "output": out_path, "count": len(risk_entities),
                       "scenario": args.scenario, "target_self_hits": len(target_self_matched)}))


if __name__ == "__main__":
    main()
