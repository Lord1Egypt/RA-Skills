#!/usr/bin/env python3
"""
/cdisc-library-api products - 列出所有产品类别
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        products = client.get_products()
        links = products.get("_links", {})
        
        print("📦 CDISC 产品类别\n")
        
        # 实际 API 返回的类别
        categories = {
            "qrs": ("QRS", "问卷、评级和量表"),
            "data-analysis": ("ADaM", "分析数据模型"),
            "data-collection": ("CDASH", "临床数据采集标准"),
            "data-tabulation": ("SDTM", "研究数据标签标准"),
            "terminology": ("CT", "受控术语"),
            "integrated": ("Integrated", "整合标准"),
            "documents": ("Documents", "文档"),
        }
        
        for key, (name, desc) in categories.items():
            if key in links:
                items = links[key]
                count = len(items) if isinstance(items, list) else 1
                print(f"  {name:15} {count} 项  -  {desc}")
        
        print(f"\n💡 使用 /cdisc-library-api qrs <代码> 查询具体量表")
        print(f"   使用 /cdisc-library-api adam <产品> 查询 ADaM")
        print(f"   使用 /cdisc-library-api ct <代码表> 查询受控术语")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

