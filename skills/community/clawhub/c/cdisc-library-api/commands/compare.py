#!/usr/bin/env python3
"""
/cdisc-library-api compare <type> <id> <v1> <v2> - 版本比较
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 5:
        print("用法：/cdisc-library-api compare <产品类型> <产品 ID> <版本 1> <版本 2>")
        print("示例：/cdisc-library-api compare qrs AIMS01 1-0 2-0")
        print("      /cdisc-library-api compare adam adam-2-1 1-0 1-1")
        print("\n产品类型：qrs, adam, cdash, sdtmig")
        return
    
    product_type = sys.argv[1].lower()
    product_id = sys.argv[2]
    v1 = sys.argv[3]
    v2 = sys.argv[4]
    
    valid_types = ["qrs", "adam", "cdash", "sdtmig", "ct"]
    if product_type not in valid_types:
        print(f"❌ 无效的产品类型：{product_type}")
        print(f"   有效类型：{', '.join(valid_types)}")
        return
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        print(f"🔄 比较 {product_type.upper()} {product_id}: {v1} → {v2}\n")
        
        result = client.compare_versions(product_type, product_id, v1, v2)
        
        # 解析比较结果（根据实际 API 响应结构调整）
        changes = result.get("changes", {})
        
        added = changes.get("added", [])
        removed = changes.get("removed", [])
        modified = changes.get("modified", [])
        
        print(f"  新增：{len(added)} 项")
        print(f"  删除：{len(removed)} 项")
        print(f"  修改：{len(modified)} 项")
        
        if added:
            print(f"\n  📝 新增项:")
            for item in added[:10]:
                name = item.get("name", item.get("title", "N/A"))
                print(f"    + {name}")
            if len(added) > 10:
                print(f"    ... 共 {len(added)} 项")
        
        if removed:
            print(f"\n  🗑️  删除项:")
            for item in removed[:10]:
                name = item.get("name", item.get("title", "N/A"))
                print(f"    - {name}")
            if len(removed) > 10:
                print(f"    ... 共 {len(removed)} 项")
        
        if modified:
            print(f"\n  ✏️  修改项:")
            for item in modified[:10]:
                name = item.get("name", item.get("title", "N/A"))
                print(f"    ~ {name}")
            if len(modified) > 10:
                print(f"    ... 共 {len(modified)} 项")
        
        if not added and not removed and not modified:
            print("\n  ℹ️  两个版本无差异")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

