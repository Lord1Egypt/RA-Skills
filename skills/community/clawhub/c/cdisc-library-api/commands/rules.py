#!/usr/bin/env python3
"""
/cdisc-library-api rules [product] - 查询 CDISC 规则
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    product = sys.argv[1].lower() if len(sys.argv) > 1 else None
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        if product:
            # 查询具体产品规则
            endpoint = f"/mdr/rules/{product}"
            data = client._get(endpoint)
            
            rules = data.get("_embedded", {}).get("rule", [])
            
            if not rules:
                print(f"❌ 未找到规则：{product}")
                return
            
            print(f"📋 CDISC 规则：{product}\n")
            print(f"  规则数：{len(rules)}\n")
            
            # 按类型分组
            by_type = {}
            for rule in rules:
                rtype = rule.get("ruleType", "Other")
                if rtype not in by_type:
                    by_type[rtype] = []
                by_type[rtype].append(rule)
            
            for rtype, rule_list in sorted(by_type.items()):
                print(f"  [{rtype}]")
                for rule in rule_list[:10]:
                    rule_id = rule.get("ruleId", "N/A")
                    description = rule.get("description", "")[:60]
                    print(f"    {rule_id:15} {description}...")
                if len(rule_list) > 10:
                    print(f"    ... 共 {len(rule_list)} 项")
                print()
        
        else:
            # 列出所有规则类别
            data = client._get("/mdr/rules")
            links = data.get("_links", {})
            
            print("📋 CDISC 规则类别\n")
            
            for key, items in links.items():
                if isinstance(items, list):
                    print(f"  {key:20} {len(items)} 项")
            
            print(f"\n💡 使用 /cdisc-library-api rules <产品> 查看具体规则")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

