#!/usr/bin/env python3
"""
合并多次搜索结果
功能：去重、重新编号、生成统计信息
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

SKILL_ROOT = Path(__file__).resolve().parent.parent
OFFICIAL_DOCS_DIR = SKILL_ROOT / "official-docs"
SEARCH_RESULTS_DIR = OFFICIAL_DOCS_DIR / "search-results"
ALLOWED_INPUT_DIRS = (
    OFFICIAL_DOCS_DIR / "input",
    OFFICIAL_DOCS_DIR / "output",
    SEARCH_RESULTS_DIR,
)


def is_relative_to(path: Path, parent: Path) -> bool:
    """兼容旧 Python 版本的 Path.is_relative_to。"""
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def resolve_input_json(file_path: str) -> Path:
    """只允许读取 skill 工作目录内的 JSON 搜索结果。"""
    raw_path = Path(file_path).expanduser()
    if raw_path.is_absolute():
        resolved = raw_path.resolve()
    elif raw_path.parent == Path("."):
        resolved = (SEARCH_RESULTS_DIR / raw_path.name).resolve()
    else:
        resolved = (SKILL_ROOT / raw_path).resolve()

    if resolved.suffix.lower() != ".json":
        raise ValueError(f"只允许读取 JSON 文件: {file_path}")
    if not any(is_relative_to(resolved, allowed.resolve()) for allowed in ALLOWED_INPUT_DIRS):
        raise ValueError(f"输入文件必须位于 skill 工作目录内: {file_path}")
    return resolved


def resolve_output_json(output_path: str) -> Path:
    """只允许将合并结果写入搜索结果目录。"""
    raw_path = Path(output_path).expanduser()
    if raw_path.is_absolute():
        resolved = raw_path.resolve()
    elif raw_path.parent == Path("."):
        resolved = (SEARCH_RESULTS_DIR / raw_path.name).resolve()
    else:
        resolved = (SKILL_ROOT / raw_path).resolve()

    if resolved.suffix.lower() != ".json":
        resolved = resolved.with_suffix(".json")
    if not is_relative_to(resolved, SEARCH_RESULTS_DIR.resolve()):
        raise ValueError(f"输出文件必须位于搜索结果目录内: {SEARCH_RESULTS_DIR}")
    return resolved


def merge_results(result_files: List[str]) -> Dict:
    """
    合并多个搜索结果文件
    
    Args:
        result_files: 搜索结果文件路径列表
        
    Returns:
        合并后的结果字典
    """
    all_articles = []
    seen_titles = set()
    duplicates_count = 0
    regions_searched = []
    searches = []
    knowledge_bases = []
    
    for file_path in result_files:
        try:
            safe_file_path = resolve_input_json(file_path)
            with safe_file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}", file=sys.stderr)
            continue
        
        # 检查是否是清洗后的格式
        if data.get("cleaned") and "articles" in data:
            articles = data["articles"]
        elif "content" in data and "data" in data.get("content", {}):
            articles = data["content"]["data"].get("检索文章", [])
        else:
            print(f"警告: 文件 {file_path} 格式不识别", file=sys.stderr)
            continue
        
        search_meta = data.get("search_meta", {})
        region = search_meta.get("area") or infer_region_from_filename(str(safe_file_path))
        regions_searched.append(region)
        searches.append({
            "file": str(safe_file_path),
            "query": search_meta.get("query", ""),
            "area": region,
            "time": search_meta.get("time", ""),
            "policy": search_meta.get("policy", False),
            "full": search_meta.get("full", False),
            "segmentCount": search_meta.get("segmentCount"),
            "knowledgeBase": data.get("knowledgeBase", ""),
        })
        if data.get("knowledgeBase"):
            knowledge_bases.append({
                "file": str(safe_file_path),
                "query": search_meta.get("query", ""),
                "area": region,
                "knowledgeBase": data.get("knowledgeBase", ""),
            })
        
        # 去重合并
        for article in articles:
            title = article.get("文章标题", "")
            if title in seen_titles:
                duplicates_count += 1
                continue
            
            seen_titles.add(title)
            article.setdefault("搜索地域", region)
            if search_meta.get("query"):
                article.setdefault("搜索词", search_meta.get("query"))
            all_articles.append(article)
    
    # 重新编号段落
    global_id = 1
    total_paragraphs = 0
    for article in all_articles:
        paragraphs = article.get("段落", [])
        for p in paragraphs:
            p["id"] = global_id
            global_id += 1
            total_paragraphs += 1
    
    # 返回合并结果
    return {
        "cleaned": True,
        "articles": all_articles,
        "search_summary": {
            "total_searches": len(result_files),
            "regions": list(set(regions_searched)),
            "total_articles": len(all_articles),
            "total_paragraphs": total_paragraphs,
            "duplicates_removed": duplicates_count,
            "searches": searches,
            "knowledge_bases": knowledge_bases
        }
    }


def infer_region_from_filename(file_path: str) -> str:
    """兼容旧结果文件：从文件名推断地域。新结果优先使用 search_meta.area。"""
    lower_path = file_path.lower()
    if "gd" in lower_path or "guangdong" in lower_path:
        return "广东省"
    if "bj" in lower_path or "beijing" in lower_path:
        return "北京市"
    if "sh" in lower_path or "shanghai" in lower_path:
        return "上海市"
    return "未知地区"


def main():
    parser = argparse.ArgumentParser(
        description="合并多次搜索结果（去重+重新编号）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s result_gd.json result_bj.json result_sh.json
  %(prog)s result_gd.json result_bj.json --output merged.json
        """
    )
    parser.add_argument("files", nargs="+", help="搜索结果文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径（可选，默认输出到标准输出）")
    
    args = parser.parse_args()
    
    # 合并结果
    merged = merge_results(args.files)
    
    # 输出
    output_json = json.dumps(merged, ensure_ascii=False, indent=2)
    
    if args.output:
        output_path = resolve_output_json(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"✅ 已合并 {merged['search_summary']['total_searches']} 次搜索结果")
        print(f"   - 文章数: {merged['search_summary']['total_articles']}")
        print(f"   - 段落数: {merged['search_summary']['total_paragraphs']}")
        print(f"   - 去重: {merged['search_summary']['duplicates_removed']} 篇")
        print(f"   - 输出: {output_path}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
