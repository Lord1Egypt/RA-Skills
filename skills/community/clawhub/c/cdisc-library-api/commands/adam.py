#!/usr/bin/env python3
"""
/cdisc-library-api adam <product> [datastructure] - 查询 ADaM 产品/数据结构
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api adam <产品 ID> [数据结构]")
        print("示例：/cdisc-library-api adam adam-2-1")
        print("      /cdisc-library-api adam adam-2-1 ADSL")
        return
    
    product = sys.argv[1].lower()
    datastructure = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        if datastructure:
            # 查询具体数据结构
            varsets = client.get_adam_varsets(product, datastructure)
            
            if not varsets:
                print(f"❌ 未找到数据结构：{product} / {datastructure}")
                return
            
            print(f"📋 ADaM 数据结构：{product} / {datastructure}\n")
            print(f"  变量集数量：{len(varsets)}\n")
            
            for vs in varsets[:10]:
                name = vs.get("title", "N/A")
                href = vs.get("href", "")
                print(f"    {name}")
            
            if len(varsets) > 10:
                print(f"    ... 共 {len(varsets)} 个变量集")
            
            print(f"\n💡 使用 /cdisc-library-api structure {product} {datastructure} <varset> 查看变量详情")
        
        else:
            # 查询产品
            data = client.get_adam_product(product)
            
            print(f"📋 ADaM 产品：{product}\n")
            print(f"  名称：{data.get('name', 'N/A')}")
            print(f"  版本：{data.get('version', 'N/A')}")
            print(f"  状态：{data.get('registrationStatus', 'N/A')}")
            
            # 获取数据结构列表
            datastructures = client.get_adam_datastructures(product)
            
            if datastructures:
                print(f"\n  数据结构列表（共 {len(datastructures)} 项）:\n")
                for ds in datastructures[:15]:
                    title = ds.get("title", "N/A")
                    print(f"    {title}")
                
                if len(datastructures) > 15:
                    print(f"    ... 共 {len(datastructures)} 项")
            
            print(f"\n💡 使用 /cdisc-library-api adam {product} <数据结构> 查看具体结构")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

