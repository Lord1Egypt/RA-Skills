#!/usr/bin/env python3
"""
债券资讯查询脚本 (Bond Information)

基于 FEEDAX API 的债券资讯与信用风险监测工具，提供全面的债券舆情查询能力。

用法:
    python query_bond_information.py --api-key "your-api-key" --keyword "违约" --sentiments 负面 --days 7
    python query_bond_information.py --keyword "20 万科 01" --page 0 --size 20

输出:
    - bond_information_<timestamp>.csv: 资讯结果 CSV 文件
    - bond_information_<timestamp>.md: 数据说明文件

API Key 配置（三选一）:
    1. 命令行参数：--api-key "your-api-key"
    2. 环境变量：export FEEDAX_API_KEY="your-api-key"
    3. 配置文件：在 scripts/ 目录创建 config.json，内容为 {"api_key": "your-api-key"}
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta


# FEEDAX API 配置
# API Key 需要通过以下方式之一提供：
# 1. 环境变量：export FEEDAX_API_KEY="your-api-key"
# 2. 命令行参数：--api-key "your-api-key"
# 3. 配置文件：在同目录创建 config.json，内容为 {"api_key": "your-api-key"}
FEEDAX_API_KEY = os.environ.get('FEEDAX_API_KEY', '')
FEEDAX_BASE_URL = "http://221.6.15.90:18011"


def query_bond_information(
    api_key: str,
    keyword: str,
    sentiments: list = None,
    bond_types: list = None,
    days: int = 7,
    page: int = 0,
    size: int = 20,
    sort_by: str = "publish_date",
    sort_type: str = "DESC"
):
    """
    查询债券资讯
    
    Args:
        api_key: FEEDAX API Key
        keyword: 搜索关键词
        sentiments: 情感倾向列表（正面/负面/中性）
        bond_types: 债券类型列表
        days: 查询天数（默认 7 天）
        page: 页码（从 0 开始）
        size: 每页数量
        sort_by: 排序字段
        sort_type: 排序类型（ASC/DESC）
    
    Returns:
        dict: API 响应数据
    """
    url = f"{FEEDAX_BASE_URL}/data-service/v1/news/bond/external/query?apiKey={api_key}"
    
    # 计算时间范围
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    # 构建请求体
    payload = {
        "bondTypes": bond_types if bond_types else [],
        "csrcIndustries": [],
        "endTime": end_time,
        "industrySwResults": [],
        "keyWordQuery": {
            "keyword": keyword,
            "queryFields": ["1", "2"]  # 1-正文，2-标题
        },
        "mediaTypes": [],
        "newsImportanceLevels": [],
        "pageNum": page,
        "pageSize": size,
        "sentiments": sentiments if sentiments else [],
        "sortBy": sort_by,
        "sortType": sort_type,
        "sseNewsTags": [],
        "startTime": start_time,
        "themeRresults": []
    }
    
    params = {"apiKey": api_key}
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        sys.exit(1)


def generate_csv(data_list: list, output_path: str):
    """
    生成 CSV 文件
    
    Args:
        data_list: 资讯数据数组
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入表头
        headers = [
            "发布时间", "标题", "来源", "情感倾向", "重要程度",
            "热度得分", "浏览数", "转发数", "债券名称", "债券类型", "发行人", "URL"
        ]
        f.write(','.join(headers) + '\n')
        
        # 写入数据行
        for item in data_list:
            # 格式化发布时间
            publish_date = item.get('publishDate', 0)
            if publish_date:
                publish_date_str = datetime.fromtimestamp(publish_date / 1000).strftime('%Y-%m-%d %H:%M')
            else:
                publish_date_str = ''
            
            # 提取债券信息
            bond_results = item.get('sseBondResults', [])
            if bond_results:
                bond_info = bond_results[0]
                bond_name = bond_info.get('bondName', '')
                bond_type = bond_info.get('bondType', '')
                bond_issuer = bond_info.get('bondIssuer', '')
            else:
                bond_name = bond_type = bond_issuer = ''
            
            row = [
                publish_date_str,
                item.get('title', '') or '',
                item.get('source', '') or '',
                item.get('sentiment', '') or '',
                item.get('newsImportanceLevel', '') or '',
                str(item.get('heatScores', 0) or 0),
                str(item.get('viewNum', 0) or 0),
                str(item.get('forwardedNum', 0) or 0),
                (bond_name or ''),
                (bond_type or ''),
                (bond_issuer or ''),
                item.get('url', '') or ''
            ]
            # 清理逗号
            row = [str(v).replace(',', ' ').replace('\n', ' ') for v in row]
            f.write(','.join(row) + '\n')
    
    print(f"CSV 文件已生成：{output_path}")


def generate_description(response: dict, output_path: str, keyword: str, days: int):
    """
    生成数据说明文件
    
    Args:
        response: API 响应数据
        output_path: 输出文件路径
        keyword: 原始查询关键词
        days: 查询天数
    """
    code = response.get('code', 0)
    message = response.get('message', '')
    total = response.get('total', 0)
    data = response.get('data', [])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 债券资讯查询结果说明\n\n")
        f.write(f"**查询关键词**: {keyword}\n")
        f.write(f"**查询时间范围**: 近 {days} 天\n")
        f.write(f"**数据日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**结果总数**: {total} 条\n")
        f.write(f"**接口状态**: code={code}, message={message}\n\n")
        
        # 情感分布统计
        sentiment_count = {}
        for item in data:
            sentiment = item.get('sentiment', '未知')
            sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1
        
        f.write("## 情感分布\n\n")
        for sentiment, count in sentiment_count.items():
            f.write(f"- {sentiment}: {count} 条\n")
        
        # 重要程度分布
        importance_count = {}
        for item in data:
            level = item.get('newsImportanceLevel', '未知')
            importance_count[level] = importance_count.get(level, 0) + 1
        
        f.write("\n## 重要程度分布\n\n")
        for level, count in importance_count.items():
            f.write(f"- {level}: {count} 条\n")
        
        # 债券信息统计
        f.write("\n## 涉及债券\n\n")
        bond_names = set()
        for item in data:
            bond_results = item.get('sseBondResults') or []
            for bond in bond_results:
                bond_name = bond.get('bondName', '')
                if bond_name:
                    bond_names.add(bond_name)
        
        if bond_names:
            for name in list(bond_names)[:20]:  # 只显示前 20 个
                f.write(f"- {name}\n")
            if len(bond_names) > 20:
                f.write(f"... 共 {len(bond_names)} 只债券\n")
        else:
            f.write("未识别到具体债券\n")
        
        # 债券类型统计
        f.write("\n## 债券类型分布\n\n")
        bond_type_count = {}
        for item in data:
            bond_results = item.get('sseBondResults') or []
            for bond in bond_results:
                bond_type = bond.get('bondType', '')
                if bond_type:
                    bond_type_count[bond_type] = bond_type_count.get(bond_type, 0) + 1
        
        if bond_type_count:
            for bond_type, count in sorted(bond_type_count.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {bond_type}: {count} 条\n")
        else:
            f.write("未识别到债券类型\n")
        
        # 数据来源说明
        f.write("\n## 数据来源\n\n")
        f.write("数据来自 FEEDAX 债券资讯监测平台，涵盖新闻、微信公众号、微博等多种信源。\n")
        f.write("\n---\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"说明文件已生成：{output_path}")


def format_output(data_list: list, verbose: bool = False):
    """
    格式化输出结果到终端
    
    Args:
        data_list: 资讯数据数组
        verbose: 是否显示详细内容
    """
    if not data_list:
        print("未找到相关资讯数据")
        return
    
    print(f"\n共找到 {len(data_list)} 条资讯:\n")
    print("=" * 80)
    
    for i, item in enumerate(data_list, 1):
        publish_date = item.get('publishDate', 0)
        if publish_date:
            date_str = datetime.fromtimestamp(publish_date / 1000).strftime('%Y-%m-%d %H:%M')
        else:
            date_str = '未知时间'
        
        sentiment = item.get('sentiment', '未知')
        sentiment_emoji = {'正面': '🟢', '负面': '🔴', '中性': '🟡'}.get(sentiment, '⚪')
        
        title = item.get('title', '')
        source = item.get('source', '')
        heat = item.get('heatScores', 0)
        
        print(f"{i}. [{date_str}] {sentiment_emoji} {sentiment}")
        print(f"   标题：{title}")
        print(f"   来源：{source} | 热度：{heat}")
        
        # 债券信息
        bond_results = item.get('sseBondResults', [])
        if bond_results:
            bonds = []
            for bond in bond_results[:3]:  # 最多显示 3 个债券
                bond_name = bond.get('bondName', '')
                bond_type = bond.get('bondType', '')
                if bond_name:
                    bonds.append(f"{bond_name}({bond_type})")
            if bonds:
                print(f"   债券：{', '.join(bonds)}")
        
        if verbose:
            summary = item.get('summary', '')
            if summary:
                print(f"   摘要：{summary[:200]}...")
        
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='债券资讯查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query_bond_information.py --api-key "your-api-key" --keyword "违约" --sentiments 负面 --days 7
  python query_bond_information.py --keyword "20 万科 01" --page 0 --size 20
  python query_bond_information.py --api-key "your-api-key" --keyword "城投债" --sentiments 负面 中性 --days 30
        """
    )
    
    parser.add_argument('--keyword', '-k', required=True, help='搜索关键词')
    parser.add_argument('--sentiments', '-s', nargs='+', choices=['正面', '负面', '中性'],
                        help='情感倾向（可多选）')
    parser.add_argument('--bond-types', '-b', nargs='+',
                        choices=['政策性金融债', '中期票据', '企业债', '地方政府债', '国债', 
                                'ABS', '可转债', 'REIT', '公司债', '短期融资券', '城投'],
                        help='债券类型（可多选）')
    parser.add_argument('--days', '-d', type=int, default=7, help='查询天数（默认 7 天）')
    parser.add_argument('--page', '-p', type=int, default=0, help='页码（从 0 开始，默认 0）')
    parser.add_argument('--size', '-n', type=int, default=20, help='每页数量（默认 20）')
    parser.add_argument('--sort-by', default='publish_date', help='排序字段（默认 publish_date）')
    parser.add_argument('--sort-type', choices=['ASC', 'DESC'], default='DESC', help='排序类型（默认 DESC）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细内容')
    parser.add_argument('--output-dir', default='.', help='输出目录（默认当前目录）')
    parser.add_argument('--no-output', action='store_true', help='不生成输出文件，仅显示结果')
    parser.add_argument('--api-key', help='FEEDAX API Key（也可通过环境变量 FEEDAX_API_KEY 提供）')
    
    args = parser.parse_args()
    
    # 获取 API Key（优先级：命令行参数 > 环境变量 > 配置文件）
    if args.api_key:
        api_key = args.api_key
    elif os.environ.get('FEEDAX_API_KEY'):
        api_key = os.environ.get('FEEDAX_API_KEY')
    else:
        # 尝试从配置文件读取
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('api_key', '')
        else:
            api_key = ''
    
    if not api_key:
        print("错误：未提供 API Key")
        print("请通过以下方式之一提供：")
        print("  1. 命令行参数：--api-key \"your-api-key\"")
        print("  2. 环境变量：export FEEDAX_API_KEY=\"your-api-key\"")
        print("  3. 配置文件：在 scripts/ 目录创建 config.json，内容为 {\"api_key\": \"your-api-key\"}")
        sys.exit(1)
    
    # 调用 API
    print(f"正在查询债券资讯...")
    print(f"关键词：{args.keyword}")
    print(f"时间范围：近 {args.days} 天")
    if args.sentiments:
        print(f"情感倾向：{', '.join(args.sentiments)}")
    if args.bond_types:
        print(f"债券类型：{', '.join(args.bond_types)}")
    
    response = query_bond_information(
        api_key=api_key,
        keyword=args.keyword,
        sentiments=args.sentiments,
        bond_types=args.bond_types,
        days=args.days,
        page=args.page,
        size=args.size,
        sort_by=args.sort_by,
        sort_type=args.sort_type
    )
    
    # 检查响应
    code = response.get('code')
    message = response.get('message', '')
    
    if code != 200:
        print(f"查询失败：code={code}, message={message}")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    data = response.get('data', [])
    total = response.get('total', 0)
    
    print(f"\n查询成功！共 {total} 条结果，当前返回 {len(data)} 条")
    
    # 格式化输出到终端
    format_output(data, verbose=args.verbose)
    
    # 生成输出文件
    if not args.no_output and data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = args.output_dir
        
        csv_path = os.path.join(output_dir, f"bond_information_{timestamp}.csv")
        md_path = os.path.join(output_dir, f"bond_information_{timestamp}.md")
        
        generate_csv(data, csv_path)
        generate_description(response, md_path, args.keyword, args.days)


if __name__ == '__main__':
    main()
