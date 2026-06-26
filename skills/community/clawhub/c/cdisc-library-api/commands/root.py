#!/usr/bin/env python3
"""
/cdisc-library-api root <product> - 查询版本无关的产品根信息
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api root <产品类型>")
        print("示例：/cdisc-library-api root qrs")
        print("      /cdisc-library-api root adam")
        print("\n产品类型：qrs, adam, cdash, sdtmig, ct")
        return
    
    product_type = sys.argv[1].lower()
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        # 根端点映射
        root_endpoints = {
            "qrs": "/mdr/root/qrs/instruments",
            "adam": "/mdr/root/adam",
            "cdash": "/mdr/root/cdash",
            "sdtmig": "/mdr/root/sdtmig",
            "ct": "/mdr/root/ct"
        }
        
        if product_type not in root_endpoints:
            print(f"❌ 无效的产品类型：{product_type}")
            print(f"   有效类型：{', '.join(root_endpoints.keys())}")
            return
        
        endpoint = root_endpoints[product_type]
        data = client._get(endpoint)
        
        print(f"📋 根资源：{product_type.upper()}\n")
        
        # 根据类型解析
        if product_type == "qrs":
            instruments = data.get("_embedded", {}).get("qrsRootInstrument", [])
            print(f"  量表数：{len(instruments)}\n")
            for inst in instruments[:20]:
                name = inst.get("name", "N/A")
                versions = inst.get("_links", {}).get("versions", [])
                version_count = len(versions) if isinstance(versions, list) else 0
                print(f"    {name:12} {version_count} 个版本")
            if len(instruments) > 20:
                print(f"    ... 共 {len(instruments)} 项")
        
        elif product_type == "adam":
            products = data.get("_links", {}).get("products", [])
            print(f"  产品数：{len(products)}\n")
            for p in products:
                title = p.get("title", "N/A")
                print(f"    {title}")
        
        elif product_type == "ct":
            codelists = data.get("_links", {}).get("codelists", [])
            print(f"  代码列表数：{len(codelists)}\n")
            for cl in codelists[:20]:
                title = cl.get("title", "N/A")
                print(f"    {title}")
            if len(codelists) > 20:
                print(f"    ... 共 {len(codelists)} 项")
        
        else:
            # 通用显示
            links = data.get("_links", {})
            for key, items in links.items():
                count = len(items) if isinstance(items, list) else 1
                print(f"  {key:20} {count} 项")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

