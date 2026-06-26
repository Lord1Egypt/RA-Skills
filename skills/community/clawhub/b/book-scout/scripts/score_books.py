#!/usr/bin/env python3
"""
Book scoring algorithm for book-scout skill.
Calculates comprehensive score based on rating, popularity, and recency.
"""

import sys
import json
import math
import re
from datetime import datetime

def calculate_score(book):
    """
    Calculate comprehensive book score with fault tolerance.
    
    Formula: Total Score = (Base Quality + Popularity Bonus) × Recency Multiplier
    
    Args:
        book (dict): Book dictionary with rating, review_count, publish_date
    
    Returns:
        dict: Book with calculated score
    """
    # 1. 容错提取：防止某些字段缺失
    rating = float(book.get('rating', 0))
    review_count = int(book.get('review_count', 0))
    publish_date_str = str(book.get('publish_date', '2020'))

    # 2. 动态年份提取与时效性计算
    # 用正则抓取 4 位数年份，抓不到则默认 2020
    # findall + take last match: "第2000次印刷 2023年出版" → 2023
    matches = re.findall(r'((?:19|20)\d{2})', publish_date_str)
    publish_year = int(matches[-1]) if matches else 2020

    current_year = datetime.now().year
    age = current_year - publish_year

    if age <= 2:
        recency = 1.2    # 2年内新书
    elif 3 <= age <= 5:
        recency = 1.0    # 3-5年
    else:
        recency = 0.8    # 5年以上老书

    # 3. 计算基础分 (A)
    base = rating * 10
    if review_count < 100:
        base *= 0.8  # 小样本惩罚

    # 4. 计算热度加成 (B)
    # 防崩溃：评价数为0时，按1算，log10(1) = 0
    safe_count = max(1, review_count)
    bonus = math.log10(safe_count) * 2

    # 5. 计算最终得分 (C)
    total_score = (base + bonus) * recency

    # 将得分回写，保留两位小数
    book['score'] = round(total_score, 2)
    return book

if __name__ == '__main__':
    try:
        # 读取标准输入流
        input_data = json.load(sys.stdin)

        # 兼容处理单本书字典和批量书单列表
        if isinstance(input_data, dict):
            result = calculate_score(input_data)
        elif isinstance(input_data, list):
            result = [calculate_score(b) for b in input_data]
            # 批量模式下，自动按 score 降序排列
            result.sort(key=lambda x: x.get('score', 0), reverse=True)
        else:
            raise ValueError("输入必须是 JSON 字典或列表")

        # 标准化输出
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "输入数据非有效 JSON 格式"}))
    except Exception as e:
        print(json.dumps({"error": f"打分脚本执行失败: {str(e)}"}))
