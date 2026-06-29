#!/usr/bin/env python3
"""
高考录取分数线数据抓取
数据源: 阳光高考网/各省考试院/教育在线
"""
import sys
import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote

UA = 'Mozilla/5.0 (Linux; Android 13; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'

def fetch_url(url, timeout=8):
    """Fetch URL with timeout and user agent"""
    req = Request(url, headers={
        'User-Agent': UA,
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    })
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f'请求失败: {e}', file=sys.stderr)
        return None

def search_baidu_education(query):
    """百度搜索获取教育类数据"""
    url = f'https://www.baidu.com/s?wd={quote(query)}&rn=5'
    html = fetch_url(url)
    if not html:
        return None
    # 提取结果摘要
    results = re.findall(r'<div class="c-abstract".*?>(.*?)</div>', html)
    return [re.sub(r'<.*?>', '', r).strip() for r in results[:5]]

def get_score_line(province, year):
    """获取省份分数线（特殊类型线、本科线）"""
    query = f'{year}年{province}高考分数线 特殊类型控制线 本科批'
    results = search_baidu_education(query)
    return results

def get_university_scores(university, province):
    """获取高校在某省的录取分数"""
    query = f'{university} {province} 录取分数线 近三年'
    results = search_baidu_education(query)
    return results

def get_yicifenyiduan(province, score):
    """位次换算（通过一分一段表）"""
    query = f'{province}高考一分一段表 2025 {score}分'
    results = search_baidu_education(query)
    return results

def get_admission_plan(university, province, year=2026):
    """获取招生计划"""
    query = f'{university} {province} {year}年招生计划'
    results = search_baidu_education(query)
    return results

def get_ranking(major_type='综合'):
    """高校排名"""
    query = f'2026年{major_type}大学排名 高考'
    results = search_baidu_education(query)
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 fetch_scores.py score_line <省份> <年份>")
        print("  python3 fetch_scores.py university <学校> <省份>")
        print("  python3 fetch_scores.py position <省份> <分数>")
        print("  python3 fetch_scores.py plan <学校> <省份>")
        print("  python3 fetch_scores.py ranking")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'score_line':
        province = sys.argv[2] if len(sys.argv) > 2 else '江苏'
        year = sys.argv[3] if len(sys.argv) > 3 else '2025'
        result = get_score_line(province, year)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else '未找到数据')
    elif cmd == 'university':
        uni = sys.argv[2] if len(sys.argv) > 2 else '南京大学'
        prov = sys.argv[3] if len(sys.argv) > 3 else '江苏'
        result = get_university_scores(uni, prov)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else '未找到数据')
    elif cmd == 'position':
        prov = sys.argv[2] if len(sys.argv) > 2 else '江苏'
        score = sys.argv[3] if len(sys.argv) > 3 else '580'
        result = get_yicifenyiduan(prov, score)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else '未找到数据')
    elif cmd == 'plan':
        uni = sys.argv[2] if len(sys.argv) > 2 else '南京大学'
        prov = sys.argv[3] if len(sys.argv) > 3 else '江苏'
        result = get_admission_plan(uni, prov)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else '未找到数据')
    elif cmd == 'ranking':
        result = get_ranking()
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else '未找到数据')
