#!/usr/bin/env python3
"""
/cdisc-library-api ct-packages - 查询受控术语包列表
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
        # 从 terminology 获取包列表
        data = client._get("/mdr/products")
        tl = data.get("_links", {}).get("terminology", {})
        packages = tl.get("_links", {}).get("packages", [])
        
        if not packages:
            print("❌ 未找到术语包")
            return
        
        print(f"📋 CDISC 受控术语包（共 {len(packages)} 项）\n")
        
        # 显示最新 20 个包
        print("  最新术语包:")
        for pkg in packages[-20:]:
            href = pkg.get("href", "")
            title = pkg.get("title", "")
            
            # 从 href 提取包 ID
            pkg_id = href.split("/")[-1] if "/" in href else href
            
            print(f"    {pkg_id:30} {title[:50]}...")
        
        print(f"\n💡 提示：术语包包含代码表和术语定义")
        
        # 找出最新的 SDTM 包
        sdtm_packages = [p for p in packages if p.get('href', '').startswith('/mdr/ct/packages/sdtmct')]
        if sdtm_packages:
            latest = sdtm_packages[-1]
            pkg_id = latest.get('href', '').split('/')[-1]
            print(f"\n   最新 SDTM 包：{pkg_id}")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

