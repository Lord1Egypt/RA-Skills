#!/usr/bin/env python3
"""
/cdisc-library-api export <type> <id> [version] - 导出数据为 JSON/CSV
"""

import sys
import json
import csv
import io
from pathlib import Path

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def export_json(data, filename):
    """导出为 JSON"""
    output_path = Path(filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_path


def export_csv(rows, filename, fieldnames=None):
    """导出为 CSV"""
    if not rows:
        return None
    
    output_path = Path(filename)
    if not fieldnames:
        fieldnames = list(rows[0].keys())
    
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def main():
    if len(sys.argv) < 3:
        print("用法：/cdisc-library-api export <类型> <ID> [版本号] [--format=json|csv]")
        print("\n类型:")
        print("  qrs     - QRS 量表")
        print("  items   - 量表项目")
        print("  adam    - ADaM 产品")
        print("  sdtm    - SDTM 域")
        print("  ct      - 受控术语代码表")
        print("\n示例:")
        print("  /cdisc-library-api export qrs AIMS01 2-0")
        print("  /cdisc-library-api export items AIMS01 2-0 --format=csv")
        print("  /cdisc-library-api export ct C102111")
        return
    
    export_type = sys.argv[1].lower()
    resource_id = sys.argv[2]
    version = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else None
    output_format = "json"
    
    # 解析格式参数
    for arg in sys.argv:
        if arg.startswith("--format="):
            output_format = arg.split("=")[1].lower()
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        data = None
        rows = []
        filename = f"cdisc_{export_type}_{resource_id}"
        if version:
            filename += f"_{version}"
        
        # 获取数据
        if export_type == "qrs":
            if not version:
                root = client.get_root_instrument(resource_id)
                versions = root.get("_links", {}).get("versions", [])
                if versions:
                    version = versions[-1].get("href", "").split("/")[-1]
            data = client.get_instrument(resource_id, version)
            filename += f".{output_format}"
        
        elif export_type == "items":
            if not version:
                print("❌ items 导出需要指定版本号")
                return
            rows = client.get_instrument_items(resource_id, version)
            filename += f".{output_format}"
        
        elif export_type == "adam":
            data = client.get_adam_product(resource_id)
            filename += f".{output_format}"
        
        elif export_type == "sdtm":
            if not version:
                print("❌ sdtm 导出需要指定版本号")
                return
            endpoint = f"/mdr/sdtmig/{version}/domains/{resource_id}/variables"
            result = client._get(endpoint)
            rows = result.get("_embedded", {}).get("sdtmVariable", [])
            filename += f".{output_format}"
        
        elif export_type == "ct":
            data = client.get_ct_codelist(resource_id)
            terms = client.get_ct_terms(resource_id)
            if terms:
                data["_terms"] = terms
            filename += f".{output_format}"
        
        else:
            print(f"❌ 未知的导出类型：{export_type}")
            return
        
        # 导出
        if output_format == "json":
            if data:
                output_path = export_json(data, filename)
            else:
                output_path = export_json(rows, filename)
            print(f"✓ 已导出到：{output_path}")
        
        elif output_format == "csv":
            if rows:
                output_path = export_csv(rows, filename)
                print(f"✓ 已导出到：{output_path}")
            else:
                print("❌ 没有可导出的数据")
        
        else:
            print(f"❌ 不支持的格式：{output_format}")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

