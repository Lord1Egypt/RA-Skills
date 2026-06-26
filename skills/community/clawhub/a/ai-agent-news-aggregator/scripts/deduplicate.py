#!/usr/bin/env python3
"""
deduplicate.py - 新闻去重

基于标题和 URL 相似度去除重复新闻。
使用简单的字符串相似度算法（无需额外依赖）。

用法:
    python deduplicate.py --input results.json --output deduped.json [--threshold 0.85]
"""

import json
import sys
import re
from pathlib import Path
from difflib import SequenceMatcher

def normalize_text(text):
    """标准化文本（用于相似度比较）"""
    if not text:
        return ""
    # 转小写
    text = text.lower()
    # 移除特殊字符
    text = re.sub(r'[^\w\s]', ' ', text)
    # 移除多余空格
    text = ' '.join(text.split())
    return text

def similarity(a, b):
    """计算两个字符串的相似度 (0-1)"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()

def extract_domain(url):
    """从 URL 提取域名"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ""

def are_duplicates(item1, item2, threshold=0.85):
    """判断两个新闻项是否重复"""
    # 1. URL 完全相同
    if item1.get("url") == item2.get("url"):
        return True
    
    # 2. 域名相同且标题高度相似
    domain1 = extract_domain(item1.get("url", ""))
    domain2 = extract_domain(item2.get("url", ""))
    
    if domain1 and domain1 == domain2:
        title_sim = similarity(item1.get("title", ""), item2.get("title", ""))
        if title_sim >= threshold:
            return True
    
    # 3. 标题极度相似（不同来源）
    title_sim = similarity(item1.get("title", ""), item2.get("title", ""))
    if title_sim >= 0.95:
        return True
    
    return False

def deduplicate(items, threshold=0.85):
    """
    对新闻列表去重
    
    策略：保留第一条出现的新闻，移除后续重复项
    
    返回:
    {
        "items": [...],  # 去重后的列表
        "removed_count": int,  # 移除的数量
        "original_count": int  # 原始数量
    }
    """
    if not items:
        return {"items": [], "removed_count": 0, "original_count": 0}
    
    deduped = []
    removed = 0
    
    for item in items:
        is_dup = False
        
        # 检查是否与已保留的项重复
        for kept in deduped:
            if are_duplicates(item, kept, threshold):
                is_dup = True
                break
        
        if not is_dup:
            deduped.append(item)
        else:
            removed += 1
    
    return {
        "items": deduped,
        "removed_count": removed,
        "original_count": len(items)
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="新闻去重")
    parser.add_argument("--input", type=str, required=True,
                        help="输入文件路径 (JSON)")
    parser.add_argument("--output", type=str, default="",
                        help="输出文件路径")
    parser.add_argument("--threshold", type=float, default=0.85,
                        help="相似度阈值 (0-1, 默认 0.85)")
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    # 去重
    result = deduplicate(items, args.threshold)
    
    # 添加元数据
    result["threshold"] = args.threshold
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"去重完成：{result['original_count']} → {len(result['items'])} (移除 {result['removed_count']} 条)", 
              file=sys.stderr)
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
