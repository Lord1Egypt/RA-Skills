#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺爱问财股票概念查询脚本
通过爬取同花顺 F10 页面获取股票所属概念板块信息
"""

import requests
import re
from bs4 import BeautifulSoup
import json
import sys

def get_stock_concepts(stock_code):
    """
    获取股票所属概念板块
    
    Args:
        stock_code: 股票代码（如 300059）
    
    Returns:
        dict: 包含股票信息和概念列表
    """
    url = f"https://basic.10jqka.com.cn/{stock_code}/concept.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": f"https://basic.10jqka.com.cn/{stock_code}/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # 同花顺使用 GBK 编码
        response.encoding = "gbk"
        
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 获取股票名称
        stock_name = ""
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # 提取股票名称（格式：股票名称 (股票代码)）
            match = re.match(r"([^(]+)\((\d+)\)", title_text)
            if match:
                stock_name = match.group(1).strip()
        
        # 解析概念板块 - 多种可能的选择器
        concepts = []
        
        # 方式 1：查找 concept 相关的 div
        concept_sections = soup.find_all("div", string=re.compile("概念|板块"))
        for section in concept_sections:
            parent = section.find_parent()
            if parent:
                links = parent.find_all("a", href=re.compile("gn/detail"))
                for link in links:
                    concept_name = link.get_text(strip=True)
                    concept_url = link.get("href", "")
                    if concept_name and concept_name not in [c["name"] for c in concepts]:
                        concepts.append({
                            "name": concept_name,
                            "url": concept_url if concept_url.startswith("http") else f"https://{concept_url}"
                        })
        
        # 方式 2：查找所有概念链接
        if not concepts:
            all_links = soup.find_all("a", href=re.compile("gn/detail|concept"))
            for link in all_links:
                concept_name = link.get_text(strip=True)
                concept_url = link.get("href", "")
                # 过滤无效概念
                if concept_name and len(concept_name) > 1 and concept_name not in ["返回", "首页", "更多"]:
                    if concept_name not in [c["name"] for c in concepts]:
                        concepts.append({
                            "name": concept_name,
                            "url": concept_url if concept_url.startswith("http") else f"https://q.10jqka.com.cn{concept_url}"
                        })
        
        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "concepts": concepts,
            "concept_count": len(concepts)
        }
        
    except requests.exceptions.Timeout:
        return {"error": "请求超时"}
    except requests.exceptions.RequestException as e:
        return {"error": f"网络错误：{str(e)}"}
    except Exception as e:
        return {"error": f"解析错误：{str(e)}"}


def get_concept_stocks(concept_name):
    """
    获取概念板块成分股（简化版）
    
    Args:
        concept_name: 概念名称
    
    Returns:
        list: 成分股列表
    """
    # 同花顺概念板块 URL 格式
    search_url = f"https://q.10jqka.com.cn/gn/index/field/199112/order/asc/page/1/prep/1/quote/{concept_name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = "gbk"
        
        soup = BeautifulSoup(response.text, "html.parser")
        stocks = []
        
        # 查找股票表格
        table = soup.find("table", {"id": "resultList"})
        if table:
            rows = table.find_all("tr")[1:]  # 跳过表头
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    code_link = cols[0].find("a")
                    name_link = cols[1].find("a")
                    if code_link and name_link:
                        stocks.append({
                            "code": code_link.get_text(strip=True),
                            "name": name_link.get_text(strip=True)
                        })
        
        return stocks
        
    except Exception as e:
        return [{"error": str(e)}]


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 query_concept.py <股票代码>")
        print("示例：python3 query_concept.py 300059")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    
    print(f"查询股票 {stock_code} 的概念板块...")
    result = get_stock_concepts(stock_code)
    
    if "error" in result:
        print(f"错误：{result['error']}")
        sys.exit(1)
    
    print(f"\n股票：{result['stock_name']} ({result['stock_code']})")
    print(f"概念数量：{result['concept_count']}")
    print("\n概念板块:")
    for i, concept in enumerate(result['concepts'], 1):
        print(f"  {i}. {concept['name']}")
    
    # 输出 JSON 格式
    print("\n--- JSON 输出 ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
