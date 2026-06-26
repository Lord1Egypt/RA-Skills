#!/usr/bin/env python3
"""
/cdisc-library-api cdash <version> [domain] - 查询 CDASH 标准
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api cdash <版本号> [域代码]")
        print("示例：/cdisc-library-api cdash 1-0")
        print("      /cdisc-library-api cdash 1-0 DM")
        print("\n常用版本：1-0, 1-1")
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
            # 查询具体域字段
            endpoint = f"/mdr/cdash/{version}/domains/{domain}/fields"
            data = client._get(endpoint)
            
            fields = data.get("_embedded", {}).get("cdashField", [])
            
            if not fields:
                print(f"❌ 未找到域：{version} / {domain}")
                return
            
            print(f"📋 CDASH 域：{domain} (v{version})\n")
            print(f"  字段数：{len(fields)}\n")
            
            # 显示字段详情
            for field in fields:
                ordinal = field.get("ordinal", "?")
                name = field.get("name", "N/A")
                label = field.get("label", "")[:50]
                req = field.get("requirement", "")
                
                req_mark = "★" if "Required" in req else "○" if "Conditional" in req else "·"
                print(f"  {req_mark} {ordinal:3}. {name:15} {label}...")
            
            print(f"\n图例：★ 必填  ○ 条件必填  · 可选")
        
        else:
            # 查询版本
            data = client.get_cdash(version)
            
            print(f"📋 CDASH 标准：v{version}\n")
            print(f"  名称：{data.get('name', 'N/A')}")
            print(f"  版本：{data.get('version', 'N/A')}")
            print(f"  状态：{data.get('registrationStatus', 'N/A')}")
            
            # 获取域列表
            domains = client.get_cdash_domains(version)
            
            if domains:
                print(f"\n  域列表（共 {len(domains)} 项）:\n")
                for d in domains:
                    name = d.get("name", "N/A")
                    label = d.get("label", "")
                    print(f"    {name:6} {label}")
            
            print(f"\n💡 使用 /cdisc-library-api cdash {version} <域代码> 查看具体域字段")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

