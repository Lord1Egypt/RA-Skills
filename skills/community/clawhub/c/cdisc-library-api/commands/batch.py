#!/usr/bin/env python3
"""
/cdisc-library-api batch <file> - 批量查询（从文件读取 ID 列表）
"""

import sys
import time
from pathlib import Path

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    if len(sys.argv) < 2:
        print("用法：/cdisc-library-api batch <文件路径>")
        print("\n文件格式（每行一个查询）:")
        print("  qrs AIMS01")
        print("  qrs CGI01 1-0")
        print("  items AIMS01 2-0")
        print("  adam adam-2-1")
        print("  ct C102111")
        print("\n示例文件内容:")
        print("  qrs AIMS01")
        print("  qrs HAM-D 1-0")
        print("  items CGI01 1-0")
        return
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ 文件不存在：{file_path}")
        return
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        lines = file_path.read_text(encoding="utf-8").strip().split("\n")
        queries = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
        
        print(f"📋 批量查询：{len(queries)} 项\n")
        
        results = {
            "成功": 0,
            "失败": 0,
            "跳过": 0
        }
        
        for i, query in enumerate(queries, 1):
            parts = query.split()
            if len(parts) < 2:
                print(f"[{i}/{len(queries)}] 跳过：无效格式 - {query}")
                results["跳过"] += 1
                continue
            
            cmd = parts[0].lower()
            
            try:
                if cmd == "qrs":
                    instrument = parts[1].upper()
                    version = parts[2] if len(parts) > 2 else None
                    
                    if not version:
                        root = client.get_root_instrument(instrument)
                        versions = root.get("_links", {}).get("versions", [])
                        if versions:
                            version = versions[-1].get("href", "").split("/")[-1]
                    
                    data = client.get_instrument(instrument, version)
                    items_count = len(data.get("items", []))
                    print(f"[{i}/{len(queries)}] ✓ {instrument} v{version} - {items_count} 个项目")
                    results["成功"] += 1
                
                elif cmd == "items":
                    if len(parts) < 3:
                        print(f"[{i}/{len(queries)}] 失败：items 需要版本号 - {query}")
                        results["失败"] += 1
                        continue
                    
                    instrument = parts[1].upper()
                    version = parts[2]
                    items = client.get_instrument_items(instrument, version)
                    print(f"[{i}/{len(queries)}] ✓ {instrument} v{version} - {len(items)} 个项目")
                    results["成功"] += 1
                
                elif cmd == "adam":
                    product = parts[1].lower()
                    data = client.get_adam_product(product)
                    ds_count = len(data.get("_links", {}).get("dataStructures", []))
                    print(f"[{i}/{len(queries)}] ✓ {product} - {ds_count} 个数据结构")
                    results["成功"] += 1
                
                elif cmd == "ct":
                    codelist = parts[1]
                    data = client.get_ct_codelist(codelist)
                    terms = client.get_ct_terms(codelist)
                    print(f"[{i}/{len(queries)}] ✓ {codelist} - {len(terms)} 个术语")
                    results["成功"] += 1
                
                else:
                    print(f"[{i}/{len(queries)}] 跳过：未知命令 - {cmd}")
                    results["跳过"] += 1
                
                # 速率限制
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[{i}/{len(queries)}] 失败：{e}")
                results["失败"] += 1
        
        print(f"\n📊 完成：成功={results['成功']}, 失败={results['失败']}, 跳过={results['跳过']}")
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

