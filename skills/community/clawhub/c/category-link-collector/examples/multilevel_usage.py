#!/usr/bin/env python3
"""
多级分类采集使用示例
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.collect_categories import collect_category_links

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 简单的分类链接
    links = [
        "https://example.com/collections/women-dresses",
        "https://example.com/collections/men-shirts-casual",
        "https://example.com/collections/kids-shoes-sneakers-running",
    ]
    
    csv_path = collect_category_links(links)
    print(f"CSV文件: {csv_path}")
    print()

def example_deep_hierarchy():
    """深度层级示例"""
    print("=== 深度层级示例 ===")
    
    # 深度分类链接
    links = [
        "https://example.com/collections/women-clothing-dresses-summer-cotton",
        "https://example.com/collections/men-accessories-watches-digital-smart",
        "https://example.com/collections/kids-toys-educational-science-chemistry",
    ]
    
    csv_path = collect_category_links(links, max_levels=6)
    print(f"CSV文件: {csv_path}")
    print()

def example_custom_output():
    """自定义输出示例"""
    print("=== 自定义输出示例 ===")
    
    links = [
        "https://zaraoutlet.top/collections/woman-collection-dresses",
        "https://zaraoutlet.top/collections/man-collection-shirts",
    ]
    
    # 自定义输出目录
    custom_dir = "/tmp/category_data"
    csv_path = collect_category_links(links, output_dir=custom_dir)
    print(f"CSV文件: {csv_path}")
    print()

def example_batch_processing():
    """批量处理示例"""
    print("=== 批量处理示例 ===")
    
    # 从文件读取链接
    def read_links_from_file(filepath):
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    # 假设有一个links.txt文件
    # links = read_links_from_file("links.txt")
    
    # 示例链接
    links = [
        "https://zaraoutlet.top/collections/woman-collection-dresses",
        "https://zaraoutlet.top/collections/woman-collection-tops",
        "https://zaraoutlet.top/collections/woman-collection-jeans",
        "https://zaraoutlet.top/collections/man-collection-shirts",
        "https://zaraoutlet.top/collections/man-collection-pants",
        "https://zaraoutlet.top/collections/kids-collection-shoes",
        "https://zaraoutlet.top/collections/kids-collection-clothes",
        "https://zaraoutlet.top/collections/beauty-perfumes",
    ]
    
    csv_path = collect_category_links(links)
    print(f"处理了 {len(links)} 个链接")
    print(f"CSV文件: {csv_path}")
    print()

def main():
    """主函数"""
    print("Category Link Collector - 多级分类采集示例")
    print("=" * 50)
    
    example_basic_usage()
    example_deep_hierarchy()
    example_custom_output()
    example_batch_processing()
    
    print("所有示例完成！")

if __name__ == "__main__":
    main()