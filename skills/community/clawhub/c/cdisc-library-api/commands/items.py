#!/usr/bin/env python3
"""
/cdisc-library-api items <code> <version> - 查询量表项目列表
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 3:
        print("用法：/cdisc-library-api items <量表代码> <版本号>")
        print("示例：/cdisc-library-api items AIMS01 2-0")
        return
    
    instrument = sys.argv[1].upper()
    version = sys.argv[2]
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        items = client.get_instrument_items(instrument, version)
        
        if not items:
            print(f"❌ 未找到项目：{instrument} v{version}")
            return
        
        print(f"📋 量表项目：{instrument} v{version}（共 {len(items)} 项）\n")
        
        # 显示所有项目
        for item in items:
            ordinal = item.get("ordinal", "?")
            code = item.get("itemCode", "N/A")
            label = item.get("label", "")
            
            # 截断长标签
            if len(label) > 60:
                label = label[:57] + "..."
            
            print(f"  {ordinal:3}. {code:12} {label}")
        
        print(f"\n💡 使用 /cdisc-library-api qrs {instrument} {version} 返回量表详情")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

