#!/usr/bin/env python3
"""
/cdisc-library-api docs - 查询 CDISC 文档
"""

import sys
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdisc_client import CDISCClient


def main():
    category = sys.argv[1].lower() if len(sys.argv) > 1 else None
    
    try:
        client = CDISCClient()
    except ValueError as e:
        print(f"❌ 错误：{e}")
        return
    
    try:
        endpoint = "/mdr/documents"
        if category:
            endpoint += f"?category={category}"
        
        data = client._get(endpoint)
        documents = data.get("_embedded", {}).get("document", [])
        
        if not documents:
            print("❌ 未找到文档")
            return
        
        print(f"📚 CDISC 文档")
        if category:
            print(f"   类别：{category}")
        print(f"   共 {len(documents)} 项\n")
        
        # 按类别分组
        by_category = {}
        for doc in documents:
            cat = doc.get("category", "Other")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(doc)
        
        for cat, docs in sorted(by_category.items()):
            print(f"  [{cat}]")
            for doc in docs[:10]:
                title = doc.get("title", "N/A")
                version = doc.get("version", "")
                status = doc.get("status", "")
                print(f"    • {title} ({version})")
            if len(docs) > 10:
                print(f"    ... 共 {len(docs)} 项")
            print()
        
    except ValueError as e:
        print(f"❌ 错误：{e}")


if __name__ == "__main__":
    main()

