#!/usr/bin/env python3
"""
validate_rules.py
-----------------
Validates rules.json against the rule_schema.json JSON Schema
and checks that condition values use valid TrustIn AML labels.

Usage:
    python3 amlclaw/aml-rule-generator/scripts/validate_rules.py [rules.json]
"""

import json
import sys
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)  # amlclaw/
SCHEMA_PATH = os.path.join(SKILL_DIR, "schema", "rule_schema.json")
LABELS_PATH = os.path.join(SKILL_DIR, "references", "trustin-labels.md")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_trustin_labels(labels_path):
    """Extract valid primary_category and secondary_category values from the Trustin AML labels Markdown table."""
    primary_categories = set()
    secondary_categories = set()

    if not os.path.exists(labels_path):
        print(f"  WARNING: Labels file not found at {labels_path}, skipping tag validation")
        return primary_categories, secondary_categories

    with open(labels_path, "r", encoding="utf-8") as f:
        content = f.read()

    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| :") or line.startswith("| 一级"):
            continue
        cols = [c.strip() for c in line.split("|")]
        # cols: ['', primary_en, primary_cn, secondary_en, secondary_cn, risk, '']
        if len(cols) >= 6:
            primary_en = cols[1].strip()
            secondary_en = cols[3].strip()
            if primary_en and primary_en != "一级分类「英文」":
                primary_categories.add(primary_en)
            if secondary_en and secondary_en != "二级分类「英文」":
                secondary_categories.add(secondary_en)

    return primary_categories, secondary_categories


def validate_schema_structure(rules, schema):
    """Validate rules against the JSON Schema structure (lightweight, no jsonschema dependency)."""
    errors = []

    if not isinstance(rules, list):
        errors.append("Root element must be a JSON array")
        return errors

    valid_categories = schema["items"]["properties"]["category"]["enum"]
    valid_risk_levels = schema["items"]["properties"]["risk_level"]["enum"]
    valid_actions = schema["items"]["properties"]["action"]["enum"]
    valid_parameters = schema["items"]["properties"]["conditions"]["items"]["properties"]["parameter"]["enum"]
    valid_operators = schema["items"]["properties"]["conditions"]["items"]["properties"]["operator"]["enum"]
    required_fields = schema["items"]["required"]

    for i, rule in enumerate(rules):
        prefix = f"Rule [{i}] (id={rule.get('rule_id', '???')})"

        # Required fields
        for field in required_fields:
            if field not in rule:
                errors.append(f"{prefix}: missing required field '{field}'")

        # Enum validation
        if "category" in rule and rule["category"] not in valid_categories:
            errors.append(f"{prefix}: invalid category '{rule['category']}'. Valid: {valid_categories}")

        if "risk_level" in rule and rule["risk_level"] not in valid_risk_levels:
            errors.append(f"{prefix}: invalid risk_level '{rule['risk_level']}'. Valid: {valid_risk_levels}")

        if "action" in rule and rule["action"] not in valid_actions:
            errors.append(f"{prefix}: invalid action '{rule['action']}'. Valid: {valid_actions}")

        # New V2 fields validation
        if "direction" in rule:
            if rule["direction"] not in ("inflow", "outflow"):
                errors.append(f"{prefix}: invalid direction '{rule['direction']}'. Valid: ['inflow', 'outflow']")
        if "min_hops" in rule:
            if not isinstance(rule["min_hops"], int) or rule["min_hops"] < 1:
                errors.append(f"{prefix}: min_hops must be a positive integer, got '{rule['min_hops']}'")
        if "max_hops" in rule:
            if not isinstance(rule["max_hops"], int) or rule["max_hops"] < 1:
                errors.append(f"{prefix}: max_hops must be a positive integer, got '{rule['max_hops']}'")
        if "min_hops" in rule and "max_hops" in rule:
            if isinstance(rule["min_hops"], int) and isinstance(rule["max_hops"], int):
                if rule["min_hops"] > rule["max_hops"]:
                    errors.append(f"{prefix}: min_hops ({rule['min_hops']}) > max_hops ({rule['max_hops']})")

        # Conditions validation
        if "conditions" in rule:
            if not isinstance(rule["conditions"], list):
                errors.append(f"{prefix}: 'conditions' must be an array")
            else:
                for j, cond in enumerate(rule["conditions"]):
                    cprefix = f"{prefix} condition[{j}]"
                    for req in ["parameter", "operator", "value"]:
                        if req not in cond:
                            errors.append(f"{cprefix}: missing required field '{req}'")
                    if "parameter" in cond and cond["parameter"] not in valid_parameters:
                        errors.append(f"{cprefix}: invalid parameter '{cond['parameter']}'")
                    if "operator" in cond and cond["operator"] not in valid_operators:
                        errors.append(f"{cprefix}: invalid operator '{cond['operator']}'")

    return errors


def validate_rule_id_uniqueness(rules):
    """Check that all rule_ids are unique."""
    errors = []
    seen = {}
    for i, rule in enumerate(rules):
        rid = rule.get("rule_id")
        if rid is None:
            continue
        if rid in seen:
            errors.append(f"Duplicate rule_id '{rid}' at indices {seen[rid]} and {i}")
        else:
            seen[rid] = i
    return errors


def validate_tag_values(rules, primary_categories, secondary_categories):
    """Check that condition values referencing tag categories use valid TrustIn labels."""
    errors = []
    if not primary_categories and not secondary_categories:
        return errors  # Skip if labels not loaded

    tag_params = {
        "target.tags.primary_category": primary_categories,
        "target.tags.secondary_category": secondary_categories,
        "path.node.tags.primary_category": primary_categories,
        "path.node.tags.secondary_category": secondary_categories,
    }

    for i, rule in enumerate(rules):
        prefix = f"Rule [{i}] (id={rule.get('rule_id', '???')})"
        for j, cond in enumerate(rule.get("conditions", [])):
            param = cond.get("parameter", "")
            if param in tag_params:
                valid_tags = tag_params[param]
                value = cond.get("value")
                # Handle both single string and array values
                values = value if isinstance(value, list) else [value]
                for v in values:
                    if isinstance(v, str) and v not in valid_tags:
                        errors.append(
                            f"{prefix} condition[{j}]: tag value '{v}' not found in Trustin AML labels for parameter '{param}'"
                        )
    return errors


def main():
    rules_path = sys.argv[1] if len(sys.argv) > 1 else "rules.json"

    if not os.path.exists(rules_path):
        print(f"FAIL: Rules file not found: {rules_path}")
        sys.exit(1)

    if not os.path.exists(SCHEMA_PATH):
        print(f"FAIL: Schema file not found: {SCHEMA_PATH}")
        sys.exit(1)

    print(f"Validating: {rules_path}")
    print(f"Schema:     {SCHEMA_PATH}")
    print(f"Labels:     {LABELS_PATH}")
    print("-" * 50)

    try:
        rules = load_json(rules_path)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON - {e}")
        sys.exit(1)

    schema = load_json(SCHEMA_PATH)
    primary_cats, secondary_cats = parse_trustin_labels(LABELS_PATH)

    all_errors = []
    all_errors.extend(validate_schema_structure(rules, schema))
    all_errors.extend(validate_rule_id_uniqueness(rules))
    all_errors.extend(validate_tag_values(rules, primary_cats, secondary_cats))

    if all_errors:
        print(f"FAIL: {len(all_errors)} error(s) found:\n")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"PASS: {len(rules)} rule(s) validated successfully.")
        print(f"  - Schema structure: OK")
        print(f"  - Rule ID uniqueness: OK")
        if primary_cats:
            print(f"  - Tag values ({len(primary_cats)} primary, {len(secondary_cats)} secondary labels): OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
