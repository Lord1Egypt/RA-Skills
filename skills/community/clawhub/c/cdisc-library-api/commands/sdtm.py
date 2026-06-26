#!/usr/bin/env python3
"""
/cdisc-library-api sdtm <version> [domain] - 查询 SDTM 实施指南
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api sdtm <版本号> [域代码]")
        print("示例：/cdisc-library-api sdtm 3-4")
        print("      /cdisc-library-api sdtm 3-4 DM")
        print("\n常用版本：3-4, 3-3, 3-2")
        return
    
    version = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        if domain:
            # 查询具体域
            endpoint = f"/mdr/sdtmig/{version}/domains/{domain}/variables"
            data = client._get(endpoint)
            
            variables = data.get("_embedded", {}).get("sdtmVariable", [])
            
            if not variables:
                print(f"❌ 未找到域：{version} / {domain}")
                return
            
            print(f"📋 SDTM 域：{domain} (v{version})\n")
            print(f"  变量数：{len(variables)}\n")
            
            # 按角色分组显示
            by_role = {}
            for var in variables:
                role = var.get("role", "Other")
                if role not in by_role:
                    by_role[role] = []
                by_role[role].append(var)
            
            for role, vars_list in sorted(by_role.items()):
                print(f"  [{role}]")
                for var in vars_list[:15]:
                    name = var.get("name", "N/A")
                    label = var.get("label", "")[:40]
                    print(f"    {name:12} {label}...")
                if len(vars_list) > 15:
                    print(f"    ... 共 {len(vars_list)} 个变量")
                print()
        
        else:
            # 查询版本
            data = client.get_sdtmig(version)
            
            print(f"📋 SDTM 实施指南：v{version}\n")
            print(f"  名称：{data.get('name', 'N/A')}")
            print(f"  版本：{data.get('version', 'N/A')}")
            print(f"  状态：{data.get('registrationStatus', 'N/A')}")
            
            # 获取域列表
            domains = client.get_sdtmig_domains(version)
            
            if domains:
                print(f"\n  域列表（共 {len(domains)} 项）:\n")
                
                # 按类别分组
                categories = {
                    "Special Purpose": [],
                    "Trial Design": [],
                    "Findings": [],
                    "Events": [],
                    "Interventions": [],
                    "Relationship": [],
                    "Other": []
                }
                
                for d in domains:
                    name = d.get("name", "N/A")
                    label = d.get("label", "")
                    cat = d.get("domainClass", "Other")
                    if cat in categories:
                        categories[cat].append((name, label))
                    else:
                        categories["Other"].append((name, label))
                
                for cat, items in categories.items():
                    if items:
                        print(f"  [{cat}]")
                        for name, label in items:
                            print(f"    {name:6} {label}")
                        print()
            
            print(f"\n💡 使用 /cdisc-library-api sdtm {version} <域代码> 查看具体域变量")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

