#!/usr/bin/env python3
"""
/cdisc-library-api search <keyword> - 搜索变量/域/量表
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api search <关键词>")
        print("示例：/cdisc-library-api search USUBJID")
        print("      /cdisc-library-api search depression")
        print("      /cdisc-library-api search AE")
        return
    
    keyword = sys.argv[1]
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        results = {
            "QRS 量表": [],
            "ADaM 变量": [],
            "SDTM 变量": [],
            "CDASH 字段": [],
            "受控术语": []
        }
        
        print(f"🔍 搜索：{keyword}\n")
        print("  正在搜索各产品类别...\n")
        
        # 搜索 QRS 量表
        try:
            instruments = client.search_instruments(keyword)
            if instruments:
                results["QRS 量表"] = instruments[:5]
        except:
            pass
        
        # 搜索 ADaM（遍历常用产品）
        adam_products = ["adam-2-1", "adamig-1-3", "adamig-1-2"]
        for product in adam_products:
            try:
                datastructures = client.get_adam_datastructures(product)
                for ds in datastructures:
                    title = ds.get("title", "")
                    href = ds.get("href", "")
                    if keyword.upper() in title.upper() or keyword.upper() in href.upper():
                        results["ADaM 变量"].append({
                            "product": product,
                            "title": title,
                            "href": href
                        })
            except:
                continue
        
        # 搜索 SDTM（遍历常用版本）
        sdtm_versions = ["3-4", "3-3"]
        for version in sdtm_versions:
            try:
                domains = client.get_sdtmig_domains(version)
                for d in domains:
                    name = d.get("name", "")
                    label = d.get("label", "")
                    if keyword.upper() in name.upper() or keyword.upper() in label.upper():
                        results["SDTM 变量"].append({
                            "version": version,
                            "domain": name,
                            "label": label
                        })
            except:
                continue
        
        # 显示结果
        found_any = False
        for category, items in results.items():
            if items:
                found_any = True
                print(f"  [{category}]")
                for item in items[:5]:
                    if "title" in item:
                        # ADaM
                        print(f"    • {item['title']} ({item['product']})")
                    elif "domain" in item:
                        # SDTM
                        print(f"    • {item['domain']}: {item['label']} (v{item['version']})")
                    elif "href" in item:
                        # QRS
                        title = item.get("title", item.get("href", ""))
                        print(f"    • {title}")
                    else:
                        print(f"    • {item}")
                if len(items) > 5:
                    print(f"    ... 共 {len(items)} 项")
                print()
        
        if not found_any:
            print("  未找到匹配结果")
            print("\n💡 提示:")
            print("   - 尝试使用大写字母代码（如 USUBJID、AE）")
            print("   - 尝试使用英文关键词（如 depression、anxiety）")
            print("   - 使用 /cdisc-library-api qrs <代码> 直接查询已知量表")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

