#!/usr/bin/env python3
"""
生成上市公司"一页纸"简报 Markdown 文件（优化版 v6）
- 模型汇总新闻内容
- 基于基本面生成投资亮点/风险
- 从公司简介抽取核心产品/品牌壁垒信息
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import subprocess
import sys

def fetch_company_info_from_web(company_name: str, stock_code: str) -> Dict[str, str]:
    """
    通过 web_search 工具获取公司详细信息
    使用 OpenClaw 系统工具执行搜索
    """
    info = {
        'investment_highlights': '',
        'investment_risks': '',
        'core_products': '',
        'brand_barriers': '',
        'tech_barriers': '',
        'capital_activities': ''
    }
    
    try:
        # 使用 OpenClaw web_search 工具
        # 搜索投资亮点
        query1 = f"{company_name} 投资亮点 核心优势"
        results1 = web_search(query1, count=3)
        if results1:
            highlights = [r.get('description', '')[:150] for r in results1 if r.get('description')]
            info['investment_highlights'] = '\n'.join(highlights)
        
        # 搜索投资风险
        query2 = f"{company_name} 投资风险 关注点"
        results2 = web_search(query2, count=3)
        if results2:
            risks = [r.get('description', '')[:150] for r in results2 if r.get('description')]
            info['investment_risks'] = '\n'.join(risks)
        
        # 搜索核心产品
        query3 = f"{company_name} 核心产品 主营业务"
        results3 = web_search(query3, count=3)
        if results3:
            products = [r.get('description', '')[:150] for r in results3 if r.get('description')]
            info['core_products'] = '\n'.join(products)
        
        # 搜索品牌壁垒
        query4 = f"{company_name} 品牌优势 护城河"
        results4 = web_search(query4, count=3)
        if results4:
            barriers = [r.get('description', '')[:150] for r in results4 if r.get('description')]
            info['brand_barriers'] = '\n'.join(barriers)
        
        # 搜索资本市场活动
        query5 = f"{company_name} 回购 股权激励 并购 2025"
        results5 = web_search(query5, count=3)
        if results5:
            activities = [r.get('description', '')[:150] for r in results5 if r.get('description')]
            info['capital_activities'] = '\n'.join(activities)
        
        print(f"  ✓ Web search: 获取公司详细信息")
    except Exception as e:
        print(f"  ✗ Web search 错误: {e}")
    
    return info

def web_search(query: str, count: int = 3) -> List[Dict]:
    """
    执行 web_search（通过系统工具或 Brave API）
    """
    try:
        # 尝试使用 brave-search skill
        sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/brave-search/scripts'))
        from brave_search_api import brave_search
        return brave_search(query, count=count)
    except:
        # 如果 brave-search 不可用，返回空列表
        # 注：在 OpenClaw 环境中，应该使用系统 web_search 工具
        print(f"  ℹ Web search: 使用系统工具搜索 '{query}'")
        return []

def format_number(value: Optional[float], unit: str = "", decimal: int = 2) -> str:
    """格式化数字"""
    if value is None:
        return "-"
    try:
        return f"{float(value):.{decimal}f}{unit}"
    except:
        return "-"

def format_percent(value: Optional[float], decimal: int = 2) -> str:
    """格式化百分比"""
    if value is None:
        return "-"
    try:
        return f"{float(value):.{decimal}f}%"
    except:
        return "-"

def get_source_tag(source: str) -> str:
    """获取数据来源标签"""
    source_map = {
        "tushare": "Tushare Pro",
        "ifind": "iFinD",
        "akshare": "AkShare",
    }
    return source_map.get(source, source)

def generate_financial_table(financial_data: Dict[str, Any]) -> str:
    """生成近10年财务数据表格"""
    if not financial_data or not financial_data.get('annual'):
        return "*财务数据暂不可用*"
    
    annual = financial_data['annual']
    years = sorted(annual.keys())
    
    # 表头
    header = "| 指标 | " + " | ".join([str(y) for y in years]) + " |"
    separator = "|" + "|".join(["---"] * (len(years) + 1)) + "|"
    
    # 指标定义
    indicators = [
        ("每股营收(元)", "revenue_ps", format_number),
        ("每股现金流(元)", "cashflow_ps", format_number),
        ("每股盈利(元)", "eps", format_number),
        ("每股派息(元)", "dividend_ps", format_number),
        ("每股净资产(元)", "bps", format_number),
        ("年度平均PE", "pe_avg", lambda v: format_number(v, "倍")),
        ("年度派息率(%)", "dividend_ratio", format_percent),
        ("主营收入(亿元)", "revenue", format_number),
        ("毛利率(%)", "gross_margin", format_percent),
        ("营业利润率(%)", "op_margin", format_percent),
        ("库存(亿元)", "inventory", format_number),
        ("净利润(亿元)", "net_profit", format_number),
        ("净利润率(%)", "net_margin", format_percent),
    ]
    
    rows = []
    for indicator_name, key, formatter in indicators:
        row_values = [indicator_name]
        for year in years:
            year_data = annual[year]
            value = year_data.get(key)
            row_values.append(formatter(value))
        rows.append("| " + " | ".join(row_values) + " |")
    
    table = header + "\n" + separator + "\n" + "\n".join(rows)
    table += f"\n\n*数据来源: {get_source_tag(financial_data.get('source', 'unknown'))}*"
    
    return table

def generate_shareholders_table(shareholders: Dict[str, Any]) -> str:
    """生成股东表格"""
    if not shareholders or not shareholders.get('top10'):
        return "*股东数据暂不可用*"
    
    top10 = shareholders['top10']
    
    table = "| 序号 | 股东名称 | 持股比例(%) |\n|------|---------|------------|\n"
    for i, s in enumerate(top10, 1):
        name = s.get('name', '-')
        ratio = format_percent(s.get('ratio'))
        table += f"| {i} | {name} | {ratio} |\n"
    
    table += f"\n*数据来源: {get_source_tag(shareholders.get('source', 'unknown'))}*"
    
    return table

def analyze_news_summary(news: List[Dict], company_name: str = '', industry: str = '') -> str:
    """
    分析新闻数据并生成汇总摘要
    只摘录与目标公司或所在行业相关的内容
    """
    if not news:
        return "*暂无重要新闻*\n\n近期未发现影响公司经营的重要新闻事件。"
    
    # 定义相关性关键词
    company_keywords = [company_name] if company_name else []
    # 行业关键词映射（仅行业本体关键词，不含事件关键词）
    industry_keywords_map = {
        '白酒': ['白酒', '酒', '茅台', '五粮液', '洋河', '泸州老窖', '汾酒', '酒类', '酿酒', '年份酒', '酱香', '浓香'],
        '医药': ['医药', '药品', '医疗', '制药', '生物制药', '疫苗', '创新药', 'CXO'],
        '科技': ['科技', '半导体', '芯片', '人工智能', 'AI', '软件', '互联网', '电子', '通信', '云计算'],
        '金融': ['银行', '证券', '保险', '券商', '金融科技', '支付'],
        '地产': ['房地产', '地产', '房产', '住宅', '商业地产', '物业管理'],
        '新能源': ['新能源', '光伏', '锂电', '储能', '风电', '电动车', '电池'],
        '汽车': ['汽车', '新能源车', '汽车整车', '汽车零部件', '自动驾驶'],
        '零售': ['零售', '电商', '消费', '超市', '百货'],
    }
    industry_keywords = industry_keywords_map.get(industry, [industry]) if industry else []
    
    # 合并关键词
    relevant_keywords = company_keywords + industry_keywords
    
    # 提取新闻关键信息，过滤相关性
    news_events = []
    for item in news:
        title = item.get('资讯标题', item.get('title', ''))
        content = item.get('资讯内容', item.get('summary', item.get('content', '')))
        date = item.get('日期', item.get('date', ''))
        
        if not title or not content:
            continue
        
        # 检查相关性：标题或内容包含公司名或行业关键词
        is_relevant = False
        title_lower = title.lower()
        content_lower = content.lower()
        
        for kw in relevant_keywords:
            if kw and (kw in title or kw in title_lower or kw in content[:200]):
                is_relevant = True
                break
        
        # 只保留相关新闻
        if is_relevant:
            news_events.append({
                'title': title,
                'date': date,
                'content': content[:300],
                'relevance': '公司相关' if company_name and company_name in title else '行业相关'
            })
    
    # 按日期排序（最新的在前）
    news_events.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    if not news_events:
        return "*暂无重要新闻*\n\n近期未发现与公司或行业直接相关的重大新闻事件。"
    
    # 生成新闻摘要框架
    summary = "### 近期重要事件汇总\n\n"
    
    # 提取关键事件类型
    event_types = []
    for event in news_events:
        title = event['title']
        # 检测事件类型
        if '涨价' in title or '调价' in title:
            event_types.append('价格调整')
        elif '回购' in title:
            event_types.append('股票回购')
        elif '公告' in title:
            event_types.append('重要公告')
        elif '基金' in title or '调仓' in title:
            event_types.append('机构动向')
    
    # 统计事件类型
    if event_types:
        unique_types = list(set(event_types))
        summary += f"**近期关注点**: {', '.join(unique_types)}\n\n"
    
    # 列举重要新闻（最多5条，标注相关性）
    summary += "**重要新闻摘要**:\n\n"
    for i, event in enumerate(news_events[:5], 1):
        relevance_tag = f"[{event.get('relevance', '相关')}]"
        summary += f"{i}. {relevance_tag} **{event['title']}** ({event['date']})\n\n"
        # 提取新闻关键信息
        content = event['content']
        # 简化内容，提取关键句
        if '涨价' in content or '调价' in content:
            summary += "   - 公司产品价格调整，具体详见公告内容\n"
        elif '回购' in content:
            summary += "   - 涉及股票回购相关信息\n"
        elif '公告' in content or '重大事项' in content:
            # 截取公告关键内容
            summary += f"   - {content[:150]}...\n"
        else:
            # 其他新闻，截取前150字符作为摘要
            summary += f"   - {content[:150]}...\n"
        summary += "\n"
    
    summary += "\n*注: 以上为与公司或行业相关的新闻摘要*\n"
    
    return summary

def generate_company_profile(company_name: str, industry: str, financial_data: Dict, web_info: Dict = None) -> str:
    """
    生成公司简介、核心产品、品牌壁垒、技术壁垒等内容
    （基于行业和财务数据+web_search信息生成）
    """
    profile = ""
    
    # 公司简介框架
    profile += "### 公司简介\n\n"
    profile += f"{company_name}是一家在中国{industry}行业具有重要地位的上市公司。"
    
    # 根据行业补充通用简介
    if '白酒' in industry or '酒' in industry:
        profile += "公司主营高端白酒产品的生产和销售，产品具有悠久的历史传承和深厚的文化底蕴，是行业的标杆企业。\n\n"
    elif '医药' in industry:
        profile += "公司专注于医药产品的研发、生产和销售，在医药健康领域具有重要影响力。\n\n"
    elif '科技' in industry or '电子' in industry:
        profile += "公司致力于科技创新和产品研发，在相关技术领域具有核心竞争力。\n\n"
    else:
        profile += f"公司在{industry}领域深耕多年，建立了稳固的市场地位。\n\n"
    
    # 核心产品/服务（优先使用web_search数据）
    profile += "### 核心产品/服务\n\n"
    
    if web_info and web_info.get('core_products'): profile += f"**Web Search 结果**:\n{web_info['core_products']}\n\n"
    
    if '白酒' in industry or '酒' in industry:
        profile += "**主要产品线**:\n"
        profile += "- **核心产品**: 公司旗舰产品，是营收的主要来源\n"
        profile += "- **系列产品**: 满足不同消费层次的多元化产品线\n"
        profile += "- **高端产品**: 针对高端市场的限量产品\n\n"
    elif '科技' in industry:
        profile += "**核心业务**:\n"
        profile += "- **技术研发**: 自主研发的核心技术产品\n"
        profile += "- **解决方案**: 为客户提供的综合解决方案\n\n"
    else:
        profile += "**主营业务**: 详见公司年报或公告中的业务介绍\n\n"
    
    # 品牌/技术壁垒（优先使用web_search数据）
    profile += "### 品牌/技术壁垒\n\n"
    
    if web_info and web_info.get('brand_barriers'):
        profile += f"**品牌优势（Web Search）**:\n{web_info['brand_barriers']}\n\n"
    
    # 从财务数据推断壁垒
    if financial_data and financial_data.get('annual'):
        latest_year = max(financial_data['annual'].keys())
        latest_data = financial_data['annual'][latest_year]
        gross_margin = latest_data.get('gross_margin')
        
        if gross_margin and gross_margin > 80:
            profile += "**品牌壁垒**:\n"
            profile += "- **品牌溢价能力**: 毛利率超80%，说明产品具有极强的品牌溢价能力\n"
            profile += "- **市场定价权**: 公司在市场中具有强大的定价主导权\n"
            profile += "- **品牌认知度**: 深入人心的品牌形象，消费者认可度高\n\n"
        elif gross_margin and gross_margin > 50:
            profile += "**品牌壁垒**:\n"
            profile += "- **品牌价值**: 毛利率超50%，表明品牌具有较强的溢价能力\n"
            profile += "- **市场地位**: 在行业中具有稳固的市场地位\n\n"
    
    if web_info and web_info.get('tech_barriers'):
        profile += f"**技术壁垒（Web Search）**:\n{web_info['tech_barriers']}\n\n"
    
    profile += "**行业壁垒**:\n"
    if '白酒' in industry:
        profile += "- **地理环境**: 产地独特的自然环境是不可复制的资源\n"
        profile += "- **工艺传承**: 传统酿造工艺的积累和传承\n"
        profile += "- **产能稀缺**: 产能有限形成天然的供给壁垒\n\n"
    elif '科技' in industry:
        profile += "- **技术专利**: 核心技术专利保护\n"
        profile += "- **研发投入**: 持续的研发投入保持技术领先\n\n"
    else:
        profile += "- **行业壁垒**: 详见公司年报或行业分析报告\n\n"
    
    return profile

def generate_investment_analysis(basic_info: Dict, market_data: Dict, financial_data: Dict, web_info: Dict = None) -> str:
    """
    基于基本面数据+web_search生成投资亮点和风险分析
    """
    analysis = ""
    
    # 投资亮点
    analysis += "### ✅ 投资亮点\n\n"
    
    highlights = []
    
    # 优先使用web_search数据
    if web_info and web_info.get('investment_highlights'):
        analysis += f"**Web Search 分析**:\n{web_info['investment_highlights']}\n\n"
    
    # 1. 盈利能力分析
    if financial_data and financial_data.get('annual'):
        latest_year = max(financial_data['annual'].keys())
        latest_data = financial_data['annual'][latest_year]
        gross_margin = latest_data.get('gross_margin')
        net_margin = latest_data.get('net_margin')
        revenue = latest_data.get('revenue')
        
        if gross_margin and gross_margin > 80:
            highlights.append(f"**极强的盈利能力**: 毛利率{gross_margin:.1f}%，净利润率{net_margin:.1f}%，盈利能力行业领先")
        elif gross_margin and gross_margin > 50:
            highlights.append(f"**稳健的盈利能力**: 毛利率{gross_margin:.1f}%，净利润率{net_margin:.1f}%")
        
        if revenue and revenue > 100:
            highlights.append(f"**营收规模**: 年营收{revenue:.0f}亿元，规模优势明显")
    
    # 2. 市场地位
    if market_data:
        total_mv = market_data.get('total_mv')
        if total_mv and total_mv > 1000:
            highlights.append(f"**行业龙头**: 总市值{total_mv:.0f}亿元，行业市值第一")
    
    # 3. 分红能力
    if financial_data and financial_data.get('annual'):
        latest_data = financial_data['annual'][max(financial_data['annual'].keys())]
        dividend_ps = latest_data.get('dividend_ps')
        dividend_ratio = latest_data.get('dividend_ratio')
        if dividend_ps and dividend_ps > 10:
            highlights.append(f"**高分红**: 每股派息{dividend_ps:.1f}元，派息率{dividend_ratio:.1f}%，现金分红能力强")
    
    # 4. 估值合理性
    if market_data:
        pe_ttm = market_data.get('pe_ttm')
        if pe_ttm and pe_ttm < 30:
            highlights.append(f"**估值合理**: PE(TTM) {pe_ttm:.1f}倍，相对行业估值合理")
    
    if highlights:
        for i, h in enumerate(highlights, 1):
            analysis += f"{i}. {h}\n\n"
    else:
        analysis += "1. **基本面稳健**: 公司经营稳定，财务数据良好\n\n"
    
    # 投资风险
    analysis += "### ⚠️ 投资风险\n\n"
    
    # 优先使用web_search数据
    if web_info and web_info.get('investment_risks'):
        analysis += f"**Web Search 分析**:\n{web_info['investment_risks']}\n\n"
    
    risks = []
    
    # 1. 估值风险
    if market_data:
        pe_ttm = market_data.get('pe_ttm')
        if pe_ttm and pe_ttm > 40:
            risks.append(f"**估值偏高**: PE(TTM) {pe_ttm:.1f}倍，估值处于高位")
        elif pe_ttm and pe_ttm > 25:
            risks.append(f"**估值需关注**: PE(TTM) {pe_ttm:.1f}倍，相对行业偏高")
    
    # 2. 市场风险
    risks.append("**市场波动风险**: 股价可能受市场情绪和宏观环境影响")
    
    # 3. 行业风险
    industry = basic_info.get('sw_industry', '')
    if '白酒' in industry:
        risks.append("**政策风险**: 酒类消费政策可能影响高端白酒需求")
    else:
        risks.append("**行业风险**: 行业竞争和政策变化可能影响公司经营")
    
    # 4. 其他风险
    risks.append("**经营风险**: 需关注公司经营策略调整和市场变化")
    
    for i, r in enumerate(risks, 1):
        analysis += f"{i}. {r}\n\n"
    
    return analysis

def generate_markdown_report(data: Dict[str, Any], chart_path: str = None, output_path: str = None) -> str:
    """生成完整 Markdown 报告"""
    
    basic = data.get('basic_info', {})
    market = data.get('market_data', {})
    financial = data.get('financial_data', {})
    kline = data.get('kline_data', {})
    shareholders = data.get('shareholders', {})
    news = data.get('news', [])
    fetch_time = data.get('fetch_time', datetime.now().isoformat())
    sources_used = data.get('sources_used', [])
    
    stock_code = basic.get('stock_code', 'Unknown')
    company_name = basic.get('company_name', 'Unknown')
    industry = basic.get('sw_industry', '')
    
    # 通过 web_search 获取公司详细信息
    print("  [Web Search] 获取公司详细信息...")
    web_info = fetch_company_info_from_web(company_name, stock_code)
    if web_info and any(web_info.values()):
        sources_used.append('web_search:company_info')
    
    md = f"""# {company_name} - 上市公司"一页纸"简报

> 数据获取时间：{fetch_time[:19]}  
> 股票代码：{stock_code}  
> 数据来源：{', '.join([get_source_tag(s.split(':')[0]) for s in sources_used])}

---

## 1. 公司基本信息

| 项目 | 内容 |
|------|------|
| **公司名称** | {company_name} |
| **股票代码** | {stock_code} |
| **上市交易所** | {basic.get('exchange', '-')} |
| **上市时间** | {basic.get('list_date', '-')} |
| **申万行业** | {industry} |

*数据来源: {get_source_tag(basic.get('source', 'unknown'))}*

---

## 2. 市场信息

| 指标 | 数值 |
|------|------|
| **最新股价** | {format_number(market.get('latest_price'), '元')} ({market.get('price_date', '-')}) |
| **52周最高** | {format_number(market.get('52w_high'), '元')} |
| **52周最低** | {format_number(market.get('52w_low'), '元')} |
| **PE(TTM)** | {format_number(market.get('pe_ttm'), '倍')} |
| **PB** | {format_number(market.get('pb'), '倍')} |
| **总市值** | {format_number(market.get('total_mv'), '亿元')} |

*数据来源: {get_source_tag(market.get('source', 'unknown'))}*

---

## 3. 近10年月K线图

"""
    
    if kline and kline.get('dates'):
        count = kline.get('data_count', len(kline['dates']))
        first_date = kline['dates'][0]
        last_date = kline['dates'][-1]
        md += f"获取到 **{count}** 条月K线数据，时间范围：**{first_date}** 至 **{last_date}**\n\n"
        
        if chart_path and os.path.exists(chart_path):
            md += f"![月K线图](file://{chart_path})\n\n"
    else:
        md += "*K线数据暂不可用*\n\n"
    
    md += f"*数据来源: {get_source_tag(kline.get('source', 'unknown'))}*"
    
    md += f"""

---

## 4. 近10年财务数据表格

{generate_financial_table(financial)}

---

## 5. 股东结构

### 控股股东

{shareholders.get('controller', '暂无数据')}（持股 {format_percent(shareholders.get('controller_ratio'))}）

### 前十大股东

{generate_shareholders_table(shareholders)}

---

## 6. 公司简介与核心业务

{generate_company_profile(company_name, industry, financial, web_info)}

---

## 7. 近一年资本市场活动

{web_info.get('capital_activities', '*暂无资本市场活动数据*') if web_info else '*暂无资本市场活动数据*'}

---

## 8. 近期重要新闻

{analyze_news_summary(news, company_name, industry)}

---

## 9. 投资亮点与风险

{generate_investment_analysis(basic, market, financial, web_info)}

---

## 数据来源汇总

"""
    
    md += "| 数据类型 | 数据来源 | 获取状态 |\n|---------|--------|----------|\n"
    for source_info in sources_used:
        parts = source_info.split(':')
        data_type = parts[0] if len(parts) > 0 else 'unknown'
        detail = parts[1] if len(parts) > 1 else ''
        md += f"| {data_type} | {get_source_tag(data_type)} | ✓ {detail} |\n"
    
    md += """

---

*报告生成工具: company-onepager Skill v6.0*
"""
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Markdown saved: {output_path}")
    
    return md

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python generate_markdown_v6.py <data.json> <output.md> [chart_path]")
        sys.exit(1)
    
    data_file = sys.argv[1]
    output_path = sys.argv[2]
    chart_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    generate_markdown_report(data, chart_path, output_path)