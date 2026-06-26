#!/usr/bin/env python3
"""
企业舆情查询脚本 (Company Information)

基于 FEEDAX API 的企业舆情监测与风险预警工具，提供全面的企业资讯查询能力。

用法:
    python query_company_information.py --api-key "your-api-key" --company "万科" --sentiments 负面 --days 7
    python query_company_information.py --keyword "恒大集团" --days 14

输出:
    - company_information_<timestamp>.csv: 资讯结果 CSV 文件
    - company_information_<timestamp>.md: 数据说明文件

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


def query_company_information(
    api_key: str,
    company_name: str = None,
    keyword: str = None,
    sentiments: list = None,
    days: int = 7,
    page: int = 0,
    size: int = 20,
    sort_by: str = "publish_date",
    sort_type: str = "DESC"
):
    """
    查询企业舆情
    
    Args:
        api_key: FEEDAX API Key
        company_name: 公司名称
        keyword: 搜索关键词（与公司名称二选一）
        sentiments: 情感倾向列表（正面/负面/中性）
        days: 查询天数（默认 7 天）
        page: 页码（从 0 开始）
        size: 每页数量
        sort_by: 排序字段
        sort_type: 排序类型（ASC/DESC）
    
    Returns:
        dict: API 响应数据
    """
    if not company_name and not keyword:
        print("错误：公司名称和关键词至少填写一个")
        sys.exit(1)
    
    url = f"{FEEDAX_BASE_URL}/data-service/v1/news/company/external/query?apiKey={api_key}"
    
    # 计算时间范围
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    # 构建请求体
    payload = {
        "companyName": company_name if company_name else "",
        "csrcIndustries": [],
        "endTime": end_time,
        "industrySwResults": [],
        "keyWordQuery": {
            "keyword": keyword if keyword else (company_name if company_name else ""),
            "queryFields": ["1", "2"]  # 1-正文，2-标题
        },
        "newsImportanceLevels": [],
        "pageNum": page,
        "pageSize": size,
        "sentiments": sentiments if sentiments else [],
        "sortBy": sort_by,
        "sortType": sort_type,
        "startTime": start_time
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
    
    必须展示 10 个核心字段：
    1. 新闻标题 2. 摘要 3. 情感倾向 4. 来源 5. 股票代码
    6. 股票简称 7. 行业分类 8. 公司名称 9. 公司别称 10. 舆情热度
    
    Args:
        data_list: 资讯数据数组
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入表头（必须展示 10 个核心字段）
        headers = [
            "发布时间", "标题", "摘要", "来源", "情感倾向", "股票代码", "股票简称", "行业分类", "公司名称", "公司别称", "舆情热度", "事件标签", "URL"
        ]
        f.write(','.join(headers) + '\n')
        
        # 写入数据行
        for item in data_list:
            # 格式化发布时间
            release_date = item.get('releaseDate', 0)
            if release_date:
                release_date_str = datetime.fromtimestamp(release_date / 1000).strftime('%Y-%m-%d %H:%M')
            else:
                release_date_str = ''
            
            # 提取公司信息
            company_tags = item.get('golaxyCompanyTagResults', [])
            if company_tags:
                company_info = company_tags[0]
                comp_name = company_info.get('compName', '')
                comp_alias = ', '.join(company_info.get('compAlias', [])) if company_info.get('compAlias') else ''
                stock_info = company_info.get('stockInfo', {})
                stock_code = stock_info.get('stockCode', '') if stock_info else ''
                stock_short = stock_info.get('stockShortName', '') if stock_info else ''
            else:
                comp_name = comp_alias = stock_code = stock_short = ''
            
            # 提取行业信息
            industry_sw = item.get('industrySwVos', [])
            industry_name = industry_sw[0].get('industrySw1Name', '') if industry_sw else ''
            
            # 提取事件标签（三级标签）
            company_tags = item.get('golaxyCompanyTagResults', [])
            event_tags = []
            if company_tags:
                company_info = company_tags[0]
                tags = company_info.get('companyTags') or []
                for tag in tags[:3]:  # 取前 3 个最相关的标签
                    tag_name = tag.get('tag_name', '')
                    if tag_name:
                        # 提取三级标签（去掉"新版公司事件标签 -"前缀）
                        if tag_name.startswith('新版公司事件标签-'):
                            tag_level3 = tag_name.replace('新版公司事件标签-', '')
                            event_tags.append(tag_level3)
            event_tag_str = '; '.join(event_tags) if event_tags else ''
            
            row = [
                release_date_str,
                item.get('articleTitle', '') or '',
                item.get('articleSummary', '') or '',
                item.get('infoSource', '') or '',
                item.get('articleSentiment', '') or '',
                stock_code,
                stock_short,
                industry_name,
                comp_name,
                comp_alias,
                str(item.get('publicOpinionHeatScore', 0) or 0),
                event_tag_str,
                item.get('articleUrl', '') or ''
            ]
            # 清理逗号
            row = [str(v).replace(',', ' ').replace('\n', ' ') for v in row]
            f.write(','.join(row) + '\n')
    
    print(f"CSV 文件已生成：{output_path}")


def generate_description(response: dict, output_path: str, company_name: str, keyword: str, days: int):
    """
    生成数据说明文件
    
    Args:
        response: API 响应数据
        output_path: 输出文件路径
        company_name: 公司名称
        keyword: 关键词
        days: 查询天数
    """
    code = response.get('code', 0)
    message = response.get('message', '')
    total = response.get('total', 0)
    data = response.get('data', [])
    
    search_term = company_name if company_name else keyword
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 企业资讯查询结果说明\n\n")
        f.write(f"**查询对象**: {search_term}\n")
        if company_name:
            f.write(f"**公司名称**: {company_name}\n")
        if keyword:
            f.write(f"**关键词**: {keyword}\n")
        f.write(f"**查询时间范围**: 近 {days} 天\n")
        f.write(f"**数据日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**结果总数**: {total} 条\n")
        f.write(f"**接口状态**: code={code}, message={message}\n\n")
        
        # 情感分布统计
        sentiment_count = {}
        for item in data:
            sentiment = item.get('articleSentiment', '未知')
            sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1
        
        f.write("## 情感分布\n\n")
        for sentiment, count in sentiment_count.items():
            f.write(f"- {sentiment}: {count} 条\n")
        
        # 公司情感得分统计
        f.write("\n## 公司情感得分分布\n\n")
        comp_sentiment_count = {'正面': 0, '中性': 0, '负面': 0}
        for item in data:
            for tag in item.get('golaxyCompanyTagResults', []):
                score = tag.get('compSentimentScore', 0)
                if score > 0:
                    comp_sentiment_count['正面'] += 1
                elif score < 0:
                    comp_sentiment_count['负面'] += 1
                else:
                    comp_sentiment_count['中性'] += 1
        
        for sentiment, count in comp_sentiment_count.items():
            if count > 0:
                f.write(f"- {sentiment}: {count} 条\n")
        
        # 重要程度分布
        importance_count = {}
        for item in data:
            level = item.get('articleImportanceLevel', '未知')
            importance_count[level] = importance_count.get(level, 0) + 1
        
        f.write("\n## 重要程度分布\n\n")
        for level, count in importance_count.items():
            f.write(f"- {level}: {count} 条\n")
        
        # 涉及公司统计
        f.write("\n## 涉及公司\n\n")
        companies = set()
        for item in data:
            for tag in item.get('golaxyCompanyTagResults', []):
                comp_name = tag.get('compName', '')
                if comp_name:
                    companies.add(comp_name)
        
        if companies:
            for name in list(companies)[:20]:  # 只显示前 20 个
                f.write(f"- {name}\n")
            if len(companies) > 20:
                f.write(f"... 共 {len(companies)} 家公司\n")
        else:
            f.write("未识别到具体公司\n")
        
        # 涉及行业统计
        f.write("\n## 涉及行业\n\n")
        csrc_industries = set()
        sw_industries = set()
        
        for item in data:
            for ind in item.get('industryCsrcVos', []):
                category = ind.get('industryCategoryName', '')
                specific = ind.get('industrySpecificName', '')
                if category:
                    csrc_industries.add(category)
                if specific:
                    csrc_industries.add(f"{category}>{specific}")
            
            for ind in item.get('industrySwVos', []):
                sw1 = ind.get('industrySw1Name', '')
                sw2 = ind.get('industrySw2Name', '')
                if sw1:
                    sw_industries.add(sw1)
                if sw2:
                    sw_industries.add(f"{sw1}>{sw2}")
        
        if csrc_industries:
            f.write("### 证监会行业\n\n")
            for name in list(csrc_industries)[:10]:
                f.write(f"- {name}\n")
        
        if sw_industries:
            f.write("\n### 申万行业\n\n")
            for name in list(sw_industries)[:10]:
                f.write(f"- {name}\n")
        
        # 数据来源说明
        f.write("\n## 数据来源\n\n")
        f.write("数据来自 FEEDAX 企业舆情监测平台，涵盖新闻、微信公众号、微博等多种信源。\n")
        f.write("\n---\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"说明文件已生成：{output_path}")


def format_output(data_list: list, verbose: bool = False):
    """
    格式化输出结果到终端
    
    必须展示 10 个核心字段：
    1. 新闻标题 2. 摘要 3. 情感倾向 4. 来源 5. 股票代码
    6. 股票简称 7. 行业分类 8. 公司名称 9. 公司别称 10. 舆情热度
    
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
        release_date = item.get('releaseDate', 0)
        if release_date:
            date_str = datetime.fromtimestamp(release_date / 1000).strftime('%Y-%m-%d %H:%M')
        else:
            date_str = '未知时间'
        
        sentiment = item.get('articleSentiment', '未知')
        sentiment_emoji = {'正面': '🟢', '负面': '🔴', '中性': '🟡'}.get(sentiment, '⚪')
        
        # 1. 新闻标题
        title = item.get('articleTitle', '')
        
        # 2. 摘要
        summary = item.get('articleSummary', '')
        
        # 4. 来源
        source = item.get('infoSource', '')
        
        # 5-6. 股票信息
        company_tags = item.get('golaxyCompanyTagResults', [])
        if company_tags:
            company_info = company_tags[0]
            stock_info = company_info.get('stockInfo', {})
            stock_code = stock_info.get('stockCode', '') if stock_info else ''
            stock_short = stock_info.get('stockShortName', '') if stock_info else ''
            comp_name = company_info.get('compName', '')
            comp_alias = ', '.join(company_info.get('compAlias', [])) if company_info.get('compAlias') else ''
        else:
            stock_code = stock_short = comp_name = comp_alias = ''
        
        # 7. 行业分类
        industry_sw = item.get('industrySwVos', [])
        industry_name = industry_sw[0].get('industrySw1Name', '') if industry_sw else ''
        
        # 10. 舆情热度
        heat = item.get('publicOpinionHeatScore', 0)
        
        # 11. 事件标签（三级标签）
        event_tags = []
        if company_tags:
            company_info = company_tags[0]
            tags = company_info.get('companyTags') or []
            for tag in tags[:3]:  # 取前 3 个最相关的标签
                tag_name = tag.get('tag_name', '')
                if tag_name:
                    # 提取三级标签（去掉"新版公司事件标签 -"前缀）
                    if tag_name.startswith('新版公司事件标签-'):
                        tag_level3 = tag_name.replace('新版公司事件标签-', '')
                        event_tags.append(tag_level3)
        event_tag_str = '; '.join(event_tags) if event_tags else ''
        
        # 格式化输出（必须展示的 11 个字段）
        print(f"{i}. [{date_str}] {sentiment_emoji} {sentiment}")
        print(f"   📰 标题：{title}")
        print(f"   📝 摘要：{summary[:150] if summary else '无'}...")
        print(f"   📍 来源：{source} | 🔥 舆情热度：{heat}")
        print(f"   🏢 公司：{comp_name if comp_name else '未识别'}")
        if comp_alias:
            print(f"   🏷️ 公司别称：{comp_alias}")
        if stock_code or stock_short:
            print(f"   💹 股票：{stock_code} {stock_short}")
        if industry_name:
            print(f"   🏭 行业：{industry_name}")
        if event_tag_str:
            print(f"   🏷️ 事件标签：{event_tag_str}")
        
        print("-" * 80)



def main():
    parser = argparse.ArgumentParser(
        description='企业资讯查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query_company_information.py --api-key "your-api-key" --company "万科" --sentiments 负面 --days 7
  python query_company_information.py --keyword "恒大集团" --days 14
  python query_company_information.py --api-key "your-api-key" --company "宁德时代" --sentiments 正面 --days 30
        """
    )
    
    parser.add_argument('--company', '-c', help='公司名称')
    parser.add_argument('--keyword', '-k', help='搜索关键词（与公司名称二选一）')
    parser.add_argument('--sentiments', '-s', nargs='+', choices=['正面', '负面', '中性'],
                        help='情感倾向（可多选）')
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
    
    if not args.company and not args.keyword:
        print("错误：公司名称 (--company) 和关键词 (--keyword) 至少填写一个")
        parser.print_help()
        sys.exit(1)
    
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
    print(f"正在查询企业资讯...")
    if args.company:
        print(f"公司名称：{args.company}")
    if args.keyword:
        print(f"关键词：{args.keyword}")
    print(f"时间范围：近 {args.days} 天")
    if args.sentiments:
        print(f"情感倾向：{', '.join(args.sentiments)}")
    
    response = query_company_information(
        api_key=api_key,
        company_name=args.company,
        keyword=args.keyword,
        sentiments=args.sentiments,
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
    
    data = response.get('data') or []
    total = response.get('total', 0)
    
    print(f"\n查询成功！共 {total} 条结果，当前返回 {len(data)} 条")
    
    # 格式化输出到终端
    format_output(data, verbose=args.verbose)
    
    # 生成输出文件
    if not args.no_output and data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = args.output_dir
        
        csv_path = os.path.join(output_dir, f"company_information_{timestamp}.csv")
        md_path = os.path.join(output_dir, f"company_information_{timestamp}.md")
        
        generate_csv(data, csv_path)
        generate_description(response, md_path, args.company, args.keyword, args.days)


if __name__ == '__main__':
    main()
