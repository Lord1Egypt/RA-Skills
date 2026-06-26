#!/usr/bin/env python3
"""
parse_bids.py - 抓取详情页并提取结构化数据
"""
import urllib.request
import urllib.parse
import json
import time
import re
import ssl
import os
from datetime import datetime

# 忽略 SSL 证书
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

def fetch_detail(url):
    """抓取招标详情页"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=15, context=SSL_CTX)
        html = resp.read().decode('utf-8', errors='replace')
        resp.close()
        
        if len(html) < 500:
            return None
        
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        def extract(patterns):
            for p in patterns:
                m = re.search(p, text, re.DOTALL)
                if m:
                    val = m.group(1).strip()
                    if val:
                        return val[:100]
            return ""
        
        return {
            "url": url,
            "title": extract([r'<title>([^<]+)</title>']),
            "company": extract([
                r'招标[人方][：:]\s*([^\s，,。]{2,40})',
                r'采购[人方][：:]\s*([^\s，,。]{2,40})',
                r'([^\s，,。]{5,30})(?:招标|采购)公告',
            ]),
            "budget": extract([
                r'预算[：:]\s*[￥$]?\s*([\d,，.]+\s*(?:万|元|千万)?)',
                r'采购预算[：:]\s*([\d,，.]+\s*(?:万|元)?)',
                r'金额[：:]\s*([\d,，.]+\s*(?:万|元)?)',
                r'([\d,，.]+\s*(?:亿|万|元))(?:人民币)?',
            ]),
            "bid_deadline": extract([
                r'(?:截止?|截稿)[^0-9]*(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}[日]?)',
                r'投标截止[^0-9]*(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}[日]?)',
                r'开标[^0-9]*(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}[日]?)',
            ]),
            "publish_date": extract([
                r'发布时间[：:]\s*(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}[日]?)',
                r'发布日期[：:]\s*(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}[日]?)',
            ]),
            "contact": extract([
                r'联系人[：:]\s*([^\s，,]{2,20})',
                r'电话[：:]\s*([\d\-\s]{7,20})',
                r'联系方式[：:]\s*([^\n\r]{5,50})',
            ]),
            "found_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None

def get_latest_raw():
    """获取最新 raw 文件"""
    files = [f for f in os.listdir(DATA_DIR) if f.startswith('bids_raw_') and f.endswith('.json')]
    if not files:
        return None
    files.sort()
    return os.path.join(DATA_DIR, files[-1])

def parse_bids(raw_file=None):
    """解析 raw 文件中的 URL"""
    if raw_file is None:
        raw_file = get_latest_raw()
    
    if raw_file is None:
        print("[!] 没有找到 raw 数据文件，请先运行 search_bids.py")
        return []
    
    print(f"[读取] {raw_file}")
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    
    # 去重
    seen = set()
    unique = []
    for r in raw:
        if r['url'] not in seen:
            seen.add(r['url'])
            unique.append(r)
    
    print(f"去重: {len(raw)} -> {len(unique)}\n")
    
    # 限制每次抓取数量
    max_fetch = 20
    results = []
    
    for i, r in enumerate(unique[:max_fetch], 1):
        url = r['url']
        short = url.split('/')[-1][:40]
        print(f"[{i}/{min(max_fetch, len(unique))}] {short}")
        
        detail = fetch_detail(url)
        if detail:
            detail['keyword'] = r.get('keyword', '')
            detail['competitor'] = r.get('competitor', '')
            results.append(detail)
            title = detail.get('title', '无标题')
            budget = detail.get('budget', '无预算')
            print(f"    OK | {title[:40]}")
            print(f"         预算: {budget[:20]}")
        else:
            print(f"    FAIL")
        
        time.sleep(0.5)
    
    return results

def save_parsed(results):
    """保存解析结果"""
    if not results:
        print("[!] 没有结果")
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)
    output_file = f"{DATA_DIR}/bids_parsed_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    has_budget = sum(1 for d in results if d.get('budget'))
    has_company = sum(1 for d in results if d.get('company'))
    has_deadline = sum(1 for d in results if d.get('bid_deadline'))
    
    print(f"\n[保存] {output_file}")
    print(f"[统计] 共 {len(results)} 条")
    print(f"       有预算: {has_budget}/{len(results)}")
    print(f"       有公司: {has_company}/{len(results)}")
    print(f"       有截止: {has_deadline}/{len(results)}")

if __name__ == "__main__":
    results = parse_bids()
    save_parsed(results)
