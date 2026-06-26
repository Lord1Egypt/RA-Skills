#!/usr/bin/env python3
"""
全维度对比决策助手
提供 SPU 参数/口碑/价格全方位对比评测
"""

import sys

from common import output_error, output_json, request_api


def compare(query):
    """
    对比两个商品

    Args:
        query: 对比查询语句，格式为"商品A和商品B对比"
               例如: "iphone16和iphone15对比"

    Returns:
        包含对比结果的 JSON
    """
    return request_api("param_compare", {"query": query})


def main():
    """TODO: add docstring."""
    if len(sys.argv) < 2:
        output_error("用法: python compare.py <对比查询>", example="python compare.py 'iphone16和iphone15对比'")

    query = sys.argv[1]
    result = compare(query)
    output_json(result)


if __name__ == "__main__":
    main()
