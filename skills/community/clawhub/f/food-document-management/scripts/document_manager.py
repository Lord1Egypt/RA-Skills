#!/usr/bin/env python3
"""
文档管理脚本
功能：文档索引管理、版本追踪、模板生成
"""

import os
import json
import csv
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DATA_DIR = Path(__file__).parent.parent / "data" / "docs"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def search_document_standards() -> dict:
    """搜索文档管理规范"""
    queries = [
        "食品研发 文档管理 规范",
        "技术报告 格式 规范",
        "研发项目 文档模板 范例"
    ]

    return {
        "action": "web_search",
        "queries": queries
    }


def create_document_index() -> Dict:
    """创建文档索引"""
    index = {
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "categories": [
            {"name": "市场调研", "code": "MR", "description": "市场调研报告和分析"},
            {"name": "配方研发", "code": "FR", "description": "配方设计和优化记录"},
            {"name": "工艺开发", "code": "PD", "description": "工艺流程和参数文件"},
            {"name": "质量管理", "code": "QC", "description": "质量标准和检测报告"},
            {"name": "合规文件", "code": "CP", "description": "法规和合规资料"},
            {"name": "项目管理", "code": "PM", "description": "项目计划和进度文档"}
        ],
        "documents": []
    }

    return index


def register_document(doc_info: Dict) -> Dict:
    """登记文档"""
    doc_id = doc_info.get("doc_id") or f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    record = {
        "doc_id": doc_id,
        "title": doc_info.get("title", ""),
        "category": doc_info.get("category", ""),
        "version": doc_info.get("version", "v1.0"),
        "author": doc_info.get("author", ""),
        "create_date": datetime.now().strftime("%Y-%m-%d"),
        "update_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "草稿",
        "file_path": doc_info.get("file_path", ""),
        "keywords": doc_info.get("keywords", ""),
        "remarks": doc_info.get("remarks", "")
    }

    return record


def save_document_record(record: Dict):
    """保存文档记录"""
    index_file = DATA_DIR / "document_index.json"

    index = {"documents": []}
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)

    # 检查是否已存在
    for i, doc in enumerate(index["documents"]):
        if doc.get("doc_id") == record["doc_id"]:
            record["update_date"] = datetime.now().strftime("%Y-%m-%d")
            index["documents"][i] = record
            break
    else:
        index["documents"].append(record)

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"文档已登记: {record['title']} ({record['doc_id']})")


def search_documents(keyword: str = "", category: str = "") -> List[Dict]:
    """搜索文档"""
    index_file = DATA_DIR / "document_index.json"

    if not index_file.exists():
        return []

    with open(index_file, "r", encoding="utf-8") as f:
        index = json.load(f)

    results = index.get("documents", [])

    if keyword:
        results = [d for d in results if keyword.lower() in d.get("title", "").lower()
                  or keyword.lower() in d.get("keywords", "").lower()]

    if category:
        results = [d for d in results if d.get("category") == category]

    return results


def generate_document_template(template_type: str) -> str:
    """生成文档模板"""
    templates = {
        "mr": "# 市场调研报告\n\n## 一、调研背景\n\n## 二、调研方法\n\n## 三、调研结果\n\n## 四、结论与建议\n",
        "fr": "# 配方设计文档\n\n## 一、配方名称\n\n## 二、配方目标\n\n## 三、配方组成\n\n| 原料 | 用量 | 比例 | 备注 |\n|------|------|------|------|\n\n## 四、工艺要点\n\n## 五、验证结果\n",
        "pd": "# 工艺开发文档\n\n## 一、工艺名称\n\n## 二、工艺流程\n\n## 三、关键参数\n\n## 四、设备要求\n\n## 五、质量控制点\n",
        "qc": "# 质量标准文档\n\n## 一、标准名称\n\n## 二、适用范围\n\n## 三、质量指标\n\n| 指标 | 限值 | 检测方法 |\n|------|------|----------|\n\n## 四、判定规则\n"
    }

    return templates.get(template_type.lower(), "# 新建文档\n\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="文档管理")
    parser.add_argument("--action", "-a", choices=["search", "register", "list", "template", "report"],
                       default="search")
    parser.add_argument("--title", "-t", help="文档标题")
    parser.add_argument("--category", "-c", help="文档类别")
    parser.add_argument("--type", help="模板类型")
    parser.add_argument("--keyword", "-k", help="搜索关键词")
    args = parser.parse_args()

    print("=" * 50)
    print("文档管理工具")
    print("=" * 50)

    if args.action == "search":
        print("\n请使用 web_search 工具搜索文档规范：\n")
        result = search_document_standards()
        for query in result["queries"]:
            print(f'  web_search(query="{query}")')

    elif args.action == "register":
        info = {"title": args.title or "示例文档", "category": args.category or "PM"}
        record = register_document(info)
        save_document_record(record)
        print(f"\n文档已登记: {record['doc_id']}")

    elif args.action == "list":
        docs = search_documents(keyword=args.keyword, category=args.category)
        print(f"\n找到 {len(docs)} 个文档：")
        for d in docs[:10]:
            print(f"  - [{d.get('doc_id')}] {d.get('title')} ({d.get('version')})")

    elif args.action == "template":
        template = generate_document_template(args.type or "mr")
        print("\n文档模板：")
        print(template)

    elif args.action == "report":
        print("报告功能")


if __name__ == "__main__":
    main()
