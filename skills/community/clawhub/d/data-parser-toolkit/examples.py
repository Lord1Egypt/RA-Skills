#!/usr/bin/env python3
"""Data Parser - 使用示例"""

from data_parser import DataParser
import pandas as pd


def example_parse():
    """示例: 自动解析"""
    parser = DataParser()
    print("Data Parser ready")


def example_encoding():
    """示例: 检测编码"""
    parser = DataParser()
    encoding = parser.detect_encoding("data.csv")
    print(f"Encoding: {encoding}")


def example_clean():
    """示例: 数据清洗"""
    parser = DataParser()
    print("Cleaning...")


if __name__ == '__main__':
    example_parse()