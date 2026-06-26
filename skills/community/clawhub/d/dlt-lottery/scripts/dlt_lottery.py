#!/usr/bin/env python3
"""
大乐透开奖结果查询脚本 (多数据源版)
支持多个数据源自动切换，优先官方渠道，提升获取稳定性

数据源优先级:
1. https://www.lottery.gov.cn/kj/kjlb.html?dlt  (中国体彩网 - 官方)
2. https://zx.500.com/dlt/  (500 彩票网 - 第三方，新地址)
3. https://m.china-lottery.cn/list/1000/  (中华彩讯 - 第三方)
4. https://kaijiang.78500.cn/dlt/  (彩宝贝 - 第三方)
5. https://www.cjcp.cn/kaijiang/dlt/  (彩经网 - 第三方)
6. https://lottery.sina.com.cn/dlt/  (新浪彩票 - 第三方)

Usage: python dlt_lottery.py [期号]
Example: 
    python dlt_lottery.py           # 查询最新一期
    python dlt_lottery.py 2026025   # 查询指定期号
"""

import sys
import urllib.request
import urllib.error
import re
import gzip
from html import unescape


# 数据源配置 (按优先级排序)
DATA_SOURCES = [
    {
        'name': '中国体彩网',
        'url_list': 'https://www.lottery.gov.cn/kj/kjlb.html?dlt',
        'url_issue': 'https://www.lottery.gov.cn/kj/{issue}.html',
        'priority': 'official',
        'timeout': 15,
    },
    {
        'name': '500 彩票网',
        'url_list': 'https://zx.500.com/dlt/',
        'url_issue': 'https://zx.500.com/dlt/',  # 新地址不支持按期号查询，返回列表页
        'priority': 'third_party',
        'timeout': 10,
    },
    {
        'name': '中华彩讯',
        'url_list': 'https://m.china-lottery.cn/list/1000/',
        'url_issue': 'https://m.china-lottery.cn/list/1000/',
        'priority': 'third_party',
        'timeout': 10,
    },
    {
        'name': '彩宝贝',
        'url_list': 'https://kaijiang.78500.cn/dlt/',
        'url_issue': 'https://kaijiang.78500.cn/dlt/',
        'priority': 'third_party',
        'timeout': 10,
    },
    {
        'name': '彩经网',
        'url_list': 'https://www.cjcp.cn/kaijiang/dlt/',
        'url_issue': 'https://www.cjcp.cn/kaijiang/dlt/',
        'priority': 'third_party',
        'timeout': 10,
    },
    {
        'name': '新浪彩票',
        'url_list': 'https://lottery.sina.com.cn/dlt/',
        'url_issue': 'https://lottery.sina.com.cn/dlt/{issue}/',
        'priority': 'third_party',
        'timeout': 10,
    },
]

# HTTP 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


def fetch_lottery_page(url: str, timeout: int = 15) -> str:
    """获取彩票网页面内容"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw_html = response.read()
            
            # 处理 gzip 压缩
            content_encoding = response.headers.get('Content-Encoding', '')
            if 'gzip' in content_encoding:
                try:
                    raw_html = gzip.decompress(raw_html)
                except:
                    pass
            
            # 尝试多种编码
            html = None
            for encoding in ['gb2312', 'gbk', 'utf-8']:
                try:
                    html = raw_html.decode(encoding)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            
            if html is None:
                html = raw_html.decode('utf-8', errors='ignore')
            
            # 检查是否是错误页面 (更精确的判断)
            if response.status == 404 or ('无法访问' in html and '页面不存在' in html):
                return f"ERROR:页面不存在 (404)"
            return html
    except urllib.error.HTTPError as e:
        return f"ERROR:HTTP {e.code}"
    except urllib.error.URLError as e:
        return f"ERROR:网络错误 - {e.reason}"
    except Exception as e:
        return f"ERROR:{type(e).__name__} - {str(e)}"


def parse_lottery_gov(html: str) -> dict:
    """解析中国体彩网数据"""
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '中国体彩网'}
    html = unescape(html)
    
    # 期号
    match = re.search(r'第\s*(\d{7,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日', html)
    if match:
        result['date'] = f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
    else:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
        if match:
            result['date'] = match.group(1)
    
    # 前区号码 (5 个)
    front_matches = re.findall(r'class="[^"]*ball_red[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    if not front_matches:
        front_matches = re.findall(r'<td[^>]*>\s*(\d{2})\s*</td>', html)[:5]
    result['front'] = sorted(set(front_matches), key=lambda x: int(x))[:5] if front_matches else []
    
    # 后区号码 (2 个)
    back_matches = re.findall(r'class="[^"]*ball_blue[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    if not back_matches:
        all_balls = re.findall(r'<td[^>]*>\s*(\d{2})\s*</td>', html)
        if len(all_balls) >= 7:
            back_matches = all_balls[5:7]
    result['back'] = back_matches[:2] if back_matches else []
    
    # 奖池
    pool_match = re.search(r'奖池.*?(\d[,\d\.]+)\s*亿元', html, re.IGNORECASE)
    if pool_match:
        result['prize_pool'] = pool_match.group(1) + '亿元'
    
    return result


def parse_500(html: str) -> dict:
    """
    解析 500 彩票网数据 (新地址：zx.500.com)
    
    新页面结构:
    - 前区：<li class="redball">XX</li> (5 个)
    - 后区：<li class="blueball">XX</li> (2 个)
    - 期号：从开奖链接提取 (如 /dlt/n_dt/kj/20260225_*.shtml)
    """
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '500 彩票网'}
    html = unescape(html)
    
    # 移除 HTML 注释干扰
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 期号：从开奖链接提取 (最新一期)
    # 格式：/dlt/n_dt/kj/20260225_699541.shtml
    matches = re.findall(r'/dlt/n_dt/kj/(\d{8})_\d+\.shtml', html)
    if matches:
        # 取最大的期号（最新一期）
        result['issue'] = max(matches)
    
    # 日期
    match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
    if match:
        result['date'] = match.group(1)
    
    # 前区：<li class="redball">XX</li>
    front_matches = re.findall(r'class="redball">(\d{2})<', html)
    if front_matches:
        result['front'] = front_matches[:5]
    
    # 后区：<li class="blueball">XX</li>
    back_matches = re.findall(r'class="blueball">(\d{2})<', html)
    if back_matches:
        result['back'] = back_matches[:2]
    
    # 如果上面的方法失败，回退到旧格式
    if not result['front'] or not result['back']:
        combo_match = re.search(r'(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})', html)
        if combo_match:
            result['front'] = list(combo_match.groups()[:5])
            result['back'] = list(combo_match.groups()[5:7]) if len(combo_match.groups()) > 5 else []
    
    return result


def parse_sina(html: str) -> dict:
    """解析新浪彩票数据"""
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '新浪彩票'}
    html = unescape(html)
    
    # 期号
    match = re.search(r'第\s*(\d{7,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
    if match:
        result['date'] = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
    
    # 号码
    numbers = re.findall(r'\b(\d{2})\b', html)
    if len(numbers) >= 7:
        result['front'] = sorted(set(numbers[:5]), key=lambda x: int(x))
        result['back'] = numbers[5:7]
    
    return result


def parse_china_lottery(html: str) -> dict:
    """解析中华彩讯数据"""
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '中华彩讯'}
    html = unescape(html)
    
    # 移除 HTML 注释 (中华彩讯有很多 <!----> 注释)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 期号 - 匹配类似 "第 26025 期"
    match = re.search(r'第\s*(\d{5,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期 - 尝试多种格式
    match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
    if match:
        result['date'] = match.group(1)
    else:
        # 尝试匹配 YY-MM-DD 格式 (如 26-03-11)
        match = re.search(r'(\d{2})-(\d{2})-(\d{2})', html)
        if match:
            result['date'] = f"20{match.group(1)}-{match.group(2)}-{match.group(3)}"
    
    # 前区号码 - 先定位到 header-item card-ball 区块，再提取前 5 个 em 标签
    # 格式：<div class="header-item card-ball ..."><div><em> 03</em><em> 15</em>...
    ball_section = re.search(r'class="header-item\s+card-ball[^"]*"[^>]*>.*?<div>(.*?)</div>', html, re.DOTALL)
    if ball_section:
        section = ball_section.group(1)
        # 提取不含 class="blue-ball" 的 em 标签中的号码
        front_matches = re.findall(r'<em(?![^>]*class="blue-ball")[^>]*>\s*(\d{2})\s*</em>', section)
        result['front'] = front_matches[:5]
    
    # 后区号码 - 匹配 class="blue-ball" 的 em 标签
    back_matches = re.findall(r'<em\s+class="blue-ball"[^>]*>\s*(\d{2})\s*</em>', html)
    if back_matches:
        result['back'] = back_matches[:2]
    
    # 奖池
    pool_match = re.search(r'奖池.*?(\d[,\d\.]+)\s*亿', html)
    if pool_match:
        result['prize_pool'] = pool_match.group(1) + '亿'
    
    return result


def parse_78500(html: str) -> dict:
    """解析彩宝贝数据"""
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '彩宝贝'}
    html = unescape(html)
    
    # 移除 HTML 注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 期号
    match = re.search(r'第\s*(\d{5,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
    if match:
        result['date'] = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
    
    # 号码 - 彩宝贝通常有明确的红球/蓝球标识
    # 尝试匹配 class 包含"red"或"ball"的元素
    front_matches = re.findall(r'class="[^"]*red[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    back_matches = re.findall(r'class="[^"]*blue[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    
    if front_matches and back_matches:
        result['front'] = front_matches[:5]
        result['back'] = back_matches[:2]
    else:
        # 回退到通用匹配 - 找连续的 7 个两位数
        combo_match = re.search(r'(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})', html)
        if combo_match:
            result['front'] = list(combo_match.groups()[:5])
            result['back'] = list(combo_match.groups()[5:7])
        else:
            numbers = re.findall(r'\b(\d{2})\b', html)
            if len(numbers) >= 7:
                result['front'] = sorted(set(numbers[:5]), key=lambda x: int(x))
                result['back'] = numbers[5:7]
    
    return result


def parse_cjcp(html: str) -> dict:
    """解析彩经网数据"""
    result = {'issue': '', 'date': '', 'front': [], 'back': [], 'prize_pool': '', 'source': '彩经网'}
    html = unescape(html)
    
    # 移除 HTML 注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 期号
    match = re.search(r'第\s*(\d{5,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
    if match:
        result['date'] = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
    
    # 号码 - 彩经网通常有表格格式
    # 尝试匹配表格中的号码
    table_matches = re.findall(r'<td[^>]*>\s*(\d{2})\s*</td>', html)
    if len(table_matches) >= 7:
        result['front'] = table_matches[:5]
        result['back'] = table_matches[5:7]
    else:
        # 回退到通用匹配 - 找连续的 7 个两位数
        combo_match = re.search(r'(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})', html)
        if combo_match:
            result['front'] = list(combo_match.groups()[:5])
            result['back'] = list(combo_match.groups()[5:7])
        else:
            numbers = re.findall(r'\b(\d{2})\b', html)
            if len(numbers) >= 7:
                result['front'] = sorted(set(numbers[:5]), key=lambda x: int(x))
                result['back'] = numbers[5:7]
    
    return result


def parse_draw(html: str, source_name: str) -> dict:
    """根据数据源选择解析器"""
    if 'lottery.gov.cn' in source_name.lower() or '体彩' in source_name:
        return parse_lottery_gov(html)
    elif '500' in source_name:
        return parse_500(html)
    elif 'sina' in source_name or '新浪' in source_name:
        return parse_sina(html)
    elif 'china-lottery' in source_name or '中华彩讯' in source_name:
        return parse_china_lottery(html)
    elif '78500' in source_name or '彩宝贝' in source_name:
        return parse_78500(html)
    elif 'cjcp' in source_name or '彩经网' in source_name:
        return parse_cjcp(html)
    else:
        return parse_lottery_gov(html)


def try_data_sources(issue: str = None) -> tuple:
    """按优先级尝试所有数据源"""
    for source in DATA_SOURCES:
        if issue:
            url = source['url_issue'].format(issue=issue)
        else:
            url = source['url_list']
        
        print(f"  尝试 {source['name']}...", file=sys.stderr)
        
        html = fetch_lottery_page(url, source['timeout'])
        
        if not html.startswith("ERROR:"):
            draw = parse_draw(html, source['name'])
            
            # 验证数据完整性
            if draw['issue'] or (len(draw['front']) >= 5 and len(draw['back']) >= 2):
                return (True, draw)
        
        print(f"  ❌ {source['name']} 失败", file=sys.stderr)
    
    return (False, {'error': '所有数据源都无法获取数据'})


def format_draw(draw: dict) -> str:
    """格式化单期开奖信息"""
    lines = []
    
    if draw.get('issue'):
        lines.append(f"🎱 大乐透第 {draw['issue']} 期")
    
    if draw.get('date'):
        lines.append(f"📅 开奖日期：{draw['date']}")
    
    if draw.get('front') and len(draw['front']) >= 5:
        front_str = ' '.join(draw['front'][:5])
        lines.append(f"🔴 前区：{front_str}")
    elif draw.get('front'):
        lines.append(f"🔴 前区：{' '.join(draw['front'])} (数据不完整)")
    
    if draw.get('back') and len(draw['back']) >= 2:
        back_str = ' '.join(draw['back'][:2])
        lines.append(f"🔵 后区：{back_str}")
    elif draw.get('back'):
        lines.append(f"🔵 后区：{' '.join(draw['back'])} (数据不完整)")
    
    if draw.get('prize_pool'):
        lines.append(f"💰 奖池：{draw['prize_pool']}")
    
    # 数据来源
    if draw.get('source'):
        source_type = "官方" if draw['source'] == '中国体彩网' else "第三方"
        lines.append(f"📊 数据来源：{draw['source']} ({source_type})")
    
    # 检查数据完整性
    if not draw.get('front') or len(draw['front']) < 5 or not draw.get('back') or len(draw['back']) < 2:
        lines.append("")
        lines.append("⚠️ 提示：数据可能不完整，建议访问官网核实")
        lines.append("   https://www.lottery.gov.cn/kj/kjlb.html?dlt")
    
    # 中奖规则说明
    if draw.get('front') and len(draw['front']) >= 5 and draw.get('back') and len(draw['back']) >= 2:
        lines.append("")
        lines.append("📋 中奖规则：")
        lines.append("   一等奖：5 前 + 2 后｜二等奖：5 前 + 1 后")
        lines.append("   三等奖：5 前 + 0 后｜四等奖：4 前 + 2 后")
        lines.append("   五等奖：4 前 + 1 后｜六等奖：3 前 + 2 后")
        lines.append("   七等奖：4 前 + 0 后｜八等奖：3 前 +1 后/2 前 +2 后")
        lines.append("   九等奖：3 前/2 前 +1 后/1 前 +2 后/0 前 +2 后")
        
        # 第三方数据源提示
        if draw.get('source') != '中国体彩网':
            lines.append("")
            lines.append("⚠️ 提示：第三方数据仅供参考，请以官网为准")
    
    lines.append("")
    lines.append("💡 温馨提示：理性购彩，量力而行")
    lines.append("📞 体彩客服：95086")
    lines.append("🌐 官方网站：https://www.lottery.gov.cn")
    
    return '\n'.join(lines)


def main():
    print("=" * 50, file=sys.stderr)
    print("大乐透开奖结果查询 (多数据源版)", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    # 确定查询模式
    if len(sys.argv) >= 2:
        issue = sys.argv[1]
        print(f"\n查询期号：{issue}", file=sys.stderr)
    else:
        issue = None
        print("\n查询最新开奖...", file=sys.stderr)
    
    print("\n数据源优先级:", file=sys.stderr)
    for i, source in enumerate(DATA_SOURCES, 1):
        print(f"  {i}. {source['name']} ({source['priority']})", file=sys.stderr)
    print(file=sys.stderr)
    
    # 尝试所有数据源
    success, draw = try_data_sources(issue)
    
    print(file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print(file=sys.stderr)
    
    # 输出结果
    if success:
        output = format_draw(draw)
        print(output)
    else:
        print("❌ 暂时无法获取开奖数据")
        print()
        print("可能原因：")
        print("  1. 网络连接问题")
        print("  2. 所有数据源暂时不可用")
        print("  3. 非开奖时间 (开奖日：周一、三、六)")
        print()
        print("建议访问官网查询：")
        print("  https://www.lottery.gov.cn/kj/kjlb.html?dlt")
        sys.exit(1)


if __name__ == '__main__':
    main()
