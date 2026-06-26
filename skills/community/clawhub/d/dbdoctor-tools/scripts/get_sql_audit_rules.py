"""
get_sql_audit_rules.py - Get SQL audit rules

Get SQL audit rule configuration.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_sql_audit_rules(
    engine: str = "",
    rule_name: str = "",
    priority: str = "",
) -> list:
    """
    Get SQL audit rules, return simplified fields.

    Args:
        engine: Database engine filter (optional)
        rule_name: Rule name filter (optional)
        priority: Risk level (ERROR/WARNING/DANGER, optional)
    Returns:
        Simplified rule list
    """
    params = {"UserId": config.user_id}
    if engine:
        params["engine"] = engine
    if rule_name:
        params["ruleNameCn"] = rule_name
    if priority:
        params["priority"] = priority

    response = client.get(
        "/drapi/QueryStaticSqlAuditRulesDetails",
        params=params,
    )

    raw_data = response.get("Data", [])
    if not isinstance(raw_data, list):
        return raw_data

    # Simplify returned fields
    result = []
    for item in raw_data:
        result.append({
            "engine": item.get("engine", ""),
            "ruleNameCn": item.get("ruleNameCn", ""),
            "priority": item.get("priority", ""),
        })

    return result


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get SQL audit rule configuration")
    parser.add_argument("--engine", default="", help="Database engine filter (optional)")
    parser.add_argument("--rule-name", default="", help="Rule name filter (optional)")
    parser.add_argument("--priority", default="", choices=["", "ERROR", "WARNING", "DANGER"],
                        help="Risk level (ERROR/WARNING/DANGER, optional)")
    args = parser.parse_args()

    try:
        result = get_sql_audit_rules(args.engine, args.rule_name, args.priority)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
