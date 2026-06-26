#!/usr/bin/env python3
"""
评论数据转换工具

完整数据流：
1. 原始CSV (reviews_sample.csv)
2. AI分析生成标签 (tagged_reviews.json)
3. 扁平化输出CSV (reviews_labeled_*.csv)

支持双向转换：
- JSON -> CSV: json_to_csv()
- CSV -> JSON: csv_to_json()
"""

import json
import csv
import sys
from pathlib import Path

def json_to_csv(json_file, csv_file):
    """
    将嵌套JSON结构的标签数据转换为扁平CSV格式

    JSON结构：
    {
      "review_id": "...",
      "body": "...",
      "rating": 5.0,
      "sentiment": "...",
      "info_score": 15,
      "tags": {
        "人群_性别": "...",
        "场景_使用场景": "...",
        ...
      }
    }

    输出CSV：将tags内的字段展开为独立列
    """

    # 读取JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    if not reviews:
        print("错误：JSON文件为空")
        return

    # CSV列定义：原始列 + 分析列 + 22维度标签列
    base_columns = ['review_id', 'body', 'rating', 'date', 'sentiment', 'info_score']

    # 22维度标签列（按8大维度分组）
    tag_columns = [
        # 人群维度 (4)
        '人群_性别', '人群_年龄段', '人群_职业', '人群_购买角色',
        # 场景维度 (1)
        '场景_使用场景',
        # 功能维度 (2)
        '功能_满意度', '功能_具体功能',
        # 质量维度 (3)
        '质量_材质', '质量_做工', '质量_耐用性',
        # 服务维度 (5)
        '服务_发货速度', '服务_包装质量', '服务_客服响应',
        '服务_退换货', '服务_保修',
        # 体验维度 (4)
        '体验_舒适度', '体验_易用性', '体验_外观设计', '体验_价格感知',
        # 市场维度 (2)
        '竞品_竞品对比', '复购_复购意愿',
        # 情感维度 (1)
        '情感_总体评价'
    ]

    all_columns = base_columns + tag_columns

    # 写入CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()

        for review in reviews:
            row = {
                'review_id': review.get('review_id', ''),
                'body': review.get('body', ''),
                'rating': review.get('rating', ''),
                'date': review.get('date', ''),
                'sentiment': review.get('sentiment', ''),
                'info_score': review.get('info_score', '')
            }

            # 展开tags字典
            tags = review.get('tags', {})
            for col in tag_columns:
                row[col] = tags.get(col, '未提及')

            writer.writerow(row)

    print(f"✓ 转换完成：{len(reviews)} 条评论")
    print(f"  输入：{json_file}")
    print(f"  输出：{csv_file}")


def csv_to_json(csv_file, json_file):
    """
    将扁平CSV格式转换回嵌套JSON结构

    CSV格式：review_id, body, rating, ..., 人群_性别, 场景_使用场景, ...

    输出JSON：嵌套tags结构
    """
    # 22维度标签列
    tag_columns = [
        '人群_性别', '人群_年龄段', '人群_职业', '人群_购买角色',
        '场景_使用场景',
        '功能_满意度', '功能_具体功能',
        '质量_材质', '质量_做工', '质量_耐用性',
        '服务_发货速度', '服务_包装质量', '服务_客服响应',
        '服务_退换货', '服务_保修',
        '体验_舒适度', '体验_易用性', '体验_外观设计', '体验_价格感知',
        '竞品_竞品对比', '复购_复购意愿',
        '情感_总体评价'
    ]

    reviews = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 提取基础字段
            review = {
                'review_id': row.get('review_id', ''),
                'body': row.get('body', ''),
                'rating': float(row.get('rating', 0)) if row.get('rating') else 0,
                'date': row.get('date', ''),
                'sentiment': row.get('sentiment', ''),
                'info_score': int(row.get('info_score', 0)) if row.get('info_score') else 0
            }

            # 提取tags字段
            tags = {}
            for col in tag_columns:
                val = row.get(col, '')
                if val and val != '未提及':
                    tags[col] = val

            review['tags'] = tags
            reviews.append(review)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"✓ 转换完成：{len(reviews)} 条评论")
    print(f"  输入：{csv_file}")
    print(f"  输出：{json_file}")


if __name__ == '__main__':
    print("=" * 50)
    print("评论数据转换工具")
    print("=" * 50)

    if len(sys.argv) < 3:
        print("\n使用方法：")
        print("  JSON -> CSV: python3 transform_logic.py json <input.json> <output.csv>")
        print("  CSV -> JSON: python3 transform_logic.py csv <input.csv> <output.json>")
        print("\n示例：")
        print("  python3 transform_logic.py json tagged.json output.csv")
        print("  python3 transform_logic.py csv reviews.csv tags.json")
        sys.exit(1)

    mode = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == 'json':
        json_to_csv(input_file, output_file)
    elif mode == 'csv':
        csv_to_json(input_file, output_file)
    else:
        print(f"错误：未知模式 '{mode}'，请使用 'json' 或 'csv'")
