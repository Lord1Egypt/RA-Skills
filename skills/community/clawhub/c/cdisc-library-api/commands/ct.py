#!/usr/bin/env python3
"""
/cdisc-library-api ct <codelist> - 查询受控术语代码表
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api ct <代码列表 ID>")
        print("示例：/cdisc-library-api ct C102111")
        print("\n💡 使用 /cdisc-library-api products 查看所有产品类别")
        return
    
    codelist = sys.argv[1]
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        # 获取代码列表详情
        data = client.get_ct_codelist(codelist)
        
        print(f"📋 受控术语：{codelist}\n")
        print(f"  名称：{data.get('name', 'N/A')}")
        print(f"  描述：{data.get('description', 'N/A')[:80]}...")
        print(f"  状态：{data.get('registrationStatus', 'N/A')}")
        
        # 获取术语列表
        terms = client.get_ct_terms(codelist)
        
        if terms:
            print(f"\n  术语列表（共 {len(terms)} 项）:\n")
            for term in terms[:20]:  # 只显示前 20 个
                term_code = term.get("ctTermCode", "N/A")
                definition = term.get("definition", "")[:50]
                print(f"    {term_code:12} {definition}...")
            
            if len(terms) > 20:
                print(f"\n    ... 共 {len(terms)} 项，仅显示前 20 项")
        
        print(f"\n💡 提示：术语 ID 格式为 C+5 位数字（如 C28077）")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

