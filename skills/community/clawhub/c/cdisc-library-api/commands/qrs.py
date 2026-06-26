#!/usr/bin/env python3
"""
/cdisc-library-api qrs <code> [version] - 查询 QRS 量表
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api qrs <量表代码> [版本号]")
        print("示例：/cdisc-library-api qrs AIMS01")
        print("      /cdisc-library-api qrs AIMS01 2-0")
        return
    
    instrument = sys.argv[1].upper()
    version = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        # 如果没有指定版本，先获取根信息找最新版本
        if not version:
            root = client.get_root_instrument(instrument)
            versions = root.get("_links", {}).get("versions", [])
            if not versions:
                print(f"❌ 未找到量表：{instrument}")
                return
            
            # 取最新版本
            latest = versions[-1] if versions else versions[0]
            href = latest.get("href", "")
            version = href.split("/")[-1]
            print(f"ℹ️  未指定版本，使用最新版：{version}\n")
        
        # 获取量表详情
        data = client.get_instrument(instrument, version, expand=False)
        
        print(f"📋 QRS 量表：{instrument} v{version}\n")
        print(f"  名称：{data.get('name', 'N/A')}")
        print(f"  类型：{data.get('instrumentType', 'N/A')}")
        print(f"  状态：{data.get('registrationStatus', 'N/A')}")
        print(f"  项目数：{len(data.get('items', []))}")
        print(f"  响应组：{len(data.get('responseGroups', []))}")
        
        # 显示前 5 个项目预览
        items = data.get("items", [])
        if items:
            print(f"\n  项目预览（前 5 项）:")
            for item in items[:5]:
                ordinal = item.get("ordinal", "?")
                code = item.get("itemCode", "N/A")
                label = item.get("label", "")[:40]
                print(f"    {ordinal}. {code}: {label}...")
            if len(items) > 5:
                print(f"    ... 共 {len(items)} 项")
        
        print(f"\n💡 使用 /cdisc-library-api items {instrument} {version} 查看完整项目列表")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

