#!/usr/bin/env python3
"""
分类链接采集脚本
从电商网站分类链接中提取分类信息并保存为CSV文件
"""

import re
import pandas as pd
from urllib.parse import urlparse
import os
from pathlib import Path
import sys


def extract_domain(url):
    """从URL中提取域名"""
    parsed = urlparse(url)
    return parsed.netloc


def extract_category_path(url):
    """从URL中提取分类路径"""
    # 匹配 /collections/ 后面的部分
    pattern = r'/collections/([^/?]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return ""


def parse_category_hierarchy(category_path):
    """
    解析分类路径，提取所有级别的分类
    
    Args:
        category_path: 分类路径字符串，如 "woman-collection-dresses-summer"
    
    Returns:
        list: 分类层级列表，如 ["Women", "Dresses", "Summer"]
    """
    if not category_path:
        return []
    
    # 处理特殊字符：将下划线替换为连字符，方便统一处理
    normalized_path = category_path.replace('_', '-')
    
    # 分割路径
    parts = normalized_path.split('-')
    
    # 如果路径为空，返回空列表
    if not parts:
        return []
    
    hierarchy = []
    
    # 处理一级分类
    first_level = parts[0]
    if first_level == 'woman':
        hierarchy.append('Women')
    elif first_level == 'man':
        hierarchy.append('Men')
    elif first_level == 'kids':
        hierarchy.append('Kids')
    elif first_level == 'beauty':
        hierarchy.append('Beauty')
    else:
        hierarchy.append(first_level.title())
    
    # 处理剩余部分作为下级分类
    remaining_parts = parts[1:]
    
    # 跳过一些常见的关键词
    skip_words = ['collection', 'view', 'all']
    filtered_parts = [p for p in remaining_parts if p not in skip_words]
    
    # 简单的层级构建：合并明显的词组，其他每个部分作为一个层级
    i = 0
    while i < len(filtered_parts):
        current = filtered_parts[i]
        
        # 检查是否可以与下一个词组成词组
        if i + 1 < len(filtered_parts):
            next_word = filtered_parts[i + 1]
            
            # 特殊词组处理
            # 1. t-shirts
            if current == 't' and next_word == 'shirts':
                hierarchy.append('T-shirts')
                i += 2
                continue
            # 2. co-ord
            elif current == 'co' and next_word == 'ord':
                hierarchy.append('Co-ord')
                i += 2
                continue
            # 3. 数字+单位
            elif (current.isdigit() or ('-' in current and current.replace('-', '').isdigit())) and next_word in ['months', 'years', 'cm', 'in']:
                hierarchy.append(f"{current} {next_word}".title())
                i += 2
                continue
            # 4. 短词组合（两个都短）
            elif len(current) <= 3 and len(next_word) <= 4:
                hierarchy.append(f"{current} {next_word}".title())
                i += 2
                continue
        
        # 默认情况：当前词作为一个层级
        hierarchy.append(current.title())
        i += 1
    
    return hierarchy


def parse_category_info(category_path):
    """
    解析分类路径，提取一级和二级分类（向后兼容）
    
    Args:
        category_path: 分类路径字符串
    
    Returns:
        tuple: (一级分类, 二级分类)
    """
    hierarchy = parse_category_hierarchy(category_path)
    
    first_level = hierarchy[0] if len(hierarchy) > 0 else ""
    second_level = hierarchy[1] if len(hierarchy) > 1 else ""
    
    return first_level, second_level


def collect_category_links(links, output_dir="/Users/zhangqirong/工作/caiji", max_levels=10):
    """
    采集分类链接信息，支持多级分类
    
    Args:
        links: 分类链接列表
        output_dir: 输出目录路径
        max_levels: 最大分类层级数
    
    Returns:
        CSV文件路径
    """
    data = []
    
    # 跟踪所有链接的最大分类层级
    all_hierarchies = []
    
    for link in links:
        # 提取信息
        domain = extract_domain(link)
        category_path = extract_category_path(link)
        
        # 解析分类层级
        hierarchy = parse_category_hierarchy(category_path)
        all_hierarchies.append(hierarchy)
        
        # 创建数据行
        row = {
            "完整链接": link,
            "分类路径": category_path,
            "域名": domain
        }
        
        # 添加分类层级
        for i, level in enumerate(hierarchy[:max_levels], 1):
            row[f"{i}级分类"] = level
        
        data.append(row)
    
    # 确定最大分类层级
    max_hierarchy_len = max(len(h) for h in all_hierarchies) if all_hierarchies else 0
    max_hierarchy_len = min(max_hierarchy_len, max_levels)
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 确保输出目录存在
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名（使用第一个链接的域名）
    if data:
        first_domain = data[0]["域名"]
        # 清理域名中的特殊字符
        safe_domain = first_domain.replace('.', '_').replace('-', '_')
        filename = f"{safe_domain}_multilevel.csv"
    else:
        filename = "categories_multilevel.csv"
    
    # 保存CSV文件
    csv_path = output_path / filename
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # 打印统计信息
    print(f"处理了 {len(links)} 个分类链接")
    print(f"最大分类层级: {max_hierarchy_len}")
    print(f"文件已保存: {csv_path}")
    
    return str(csv_path)


def main():
    """主函数，用于命令行调用"""
    # 示例链接
    example_links = [
        "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops",
        "https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear"
    ]
    
    print("分类链接采集脚本")
    print("=" * 50)
    
    # 获取输出目录（可从命令行参数或环境变量获取）
    output_dir = "/Users/zhangqirong/工作/caiji"
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    
    # 采集数据
    csv_path = collect_category_links(example_links, output_dir)
    
    print(f"数据已保存到: {csv_path}")
    print(f"采集了 {len(example_links)} 个分类链接")
    
    # 显示采集的数据
    df = pd.read_csv(csv_path)
    print("\n采集的数据:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()