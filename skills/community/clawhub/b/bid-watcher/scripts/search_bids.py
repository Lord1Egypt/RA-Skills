#!/usr/bin/env python3
"""
search_bids.py - 基于可用行业平台的重写版
不再依赖政府平台/搜索引擎，直接抓取经过验证的信源
"""
import urllib.request
import urllib.parse
import json
import time
import re
import ssl
import os
from datetime import datetime

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 经过验证可用的行业平台
PLATFORMS = {
    "北极星能源网": {
        "base": "https://www.bjx.com.cn",
        "search_url": "https://www.bjx.com.cn/search/?query={keyword}&page={page}",
        "type": "list"
    },
    "能源界网": {
        "base": "https://www.escn.com.cn",
        "search_url": "https://www.escn.com.cn/search/?keyword={keyword}&page={page}",
        "type": "list"
    },
    "电力设备网": {
        "base": "https://www.cpem.org.cn",
        "search_url": "https://www.cpem.org.cn/search/?wd={keyword}&page={page}",
        "type": "list"
    },
    "中国能源网": {
        "base": "https://www.cnenergy.com",
        "search_url": "https://www.cnenergy.com/search/?keyword={keyword}",
        "type": "list"
    }
}

# 从 CSV 模板提取的已有链接（直接抓取）
CSV_LINKS = [
    ("https://m.bjx.com.cn/mnews/20231218/1350560.shtml", "北极星能源网", "亿纬新能源磷酸铁锂储能项目EPC"),
    ("https://www.escn.com.cn/news/show-2070171.html", "能源界网", "四川川投储能系统设备采购"),
    ("https://m.bjx.com.cn/mnews/20250214/1427048.shtml", "北极星能源网", "中国电建储能系统框采"),
    ("https://eraes.com.cn/newsinfo/9000663.html", "新能源网", "浙江星辰5GWh储能框采"),
    ("https://m.bjx.com.cn/mnews/20231007/1335127.shtml", "北极星能源网", "东阳储能电池模组PACK"),
    ("https://m.bjx.com.cn/mnews/20250218/1427649.shtml", "北极星能源网", "潜山用户侧储能EPCO"),
    ("https://www.cpem.org.cn/list35/117357.html", "电力设备网", "山东火天储能EPC"),
    ("https://finance.sina.com.cn/roll/2026-02-25/doc-inhnzrtk5110032.shtml", "新浪财经", "浙江星辰全钒液流储能"),
    ("https://www.inengyuan.com/chuneng/12982.html", "能源界", "中国石油济柴液冷储能"),
    ("https://finance.sina.com.cn/roll/2025-02-14/doc-inekmitf4256466.shtml", "新浪财经", "中国电建储能系统集采"),
    ("https://m.chu21.com/html/chunengy-22775.shtml", "储能网", "大唐重庆铜梁储能EPC"),
    ("https://pvyuan.com/ztb_details?id=469", "pv电站网", "四川川投安岳储能EPC"),
    ("https://www.dlnyzb.com/detail/26622347", "电力招标网", "民勤风电储能设备采购"),
    ("https://www.ggzy.gov.cn/html/b/130000/0104/202409/18/00134440182514414fd489650b6934c72ca2.shtml", "公共资源安徽", "张家口源网荷储储能"),
    ("https://www.ggzy.gov.cn/html/b/410000/0101/202508/29/0041da6726be7ff44e4783282172652bb0cb.shtml", "公共资源河南", "确山光储充EPC"),
]

COMPETITORS = {
    "先导智能": "无锡先导智能装备股份有限公司",
    "海目星": "海目星激光科技集团股份有限公司",
    "赢合科技": "深圳市赢合科技股份有限公司",
    "联赢激光": "深圳市联赢激光股份有限公司"
}

# 精准采购关键词（采购方视角）
KEYWORDS = [
    "储能系统设备采购招标",
    "锂电池生产设备招标采购",
    "电池PACK生产线招标",
    "储能电池采购招标公告",
    "电芯生产设备采购招标",
    "动力电池设备招标采购",
    "储能电站设备招标公告",
    "锂电设备招标采购公告",
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

def fetch_url(url, timeout=15):
    """通用抓取函数"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)
        html = resp.read().decode("utf-8", errors="replace")
        resp.close()
        return html
    except Exception as e:
        return None

def extract_title_from_html(html):
    """从HTML提取标题"""
    m = re.search(r"<title>([^<]+)</title>", html)
    return m.group(1).strip() if m else ""

def fetch_bjx_list(keyword, max_pages=2):
    """北极星能源网列表页抓取"""
    encoded = urllib.parse.quote(keyword)
    results = []
    
    for page in range(1, max_pages + 1):
        url = f"https://www.bjx.com.cn/search/?query={encoded}&page={page}"
        
        html = fetch_url(url)
        if not html:
            print(f"  [北极星] p{page}: FAIL")
            continue
        
        # 提取链接（简单粗暴）
        links = re.findall(r'href="([^"]*bjx\.com\.cn[^"]*)"', html)
        content = [l for l in links if ".shtml" in l and "m.bjx" not in l]
        results.extend(content)
        print(f"  [北极星] p{page}: +{len(content)}")
        time.sleep(2)
    
    return list(set(results))

def fetch_escn_list(keyword, max_pages=2):
    """能源界网列表页"""
    encoded = urllib.parse.quote(keyword)
    results = []
    
    for page in range(1, max_pages + 1):
        url = f"https://www.escn.com.cn/search/?keyword={encoded}&page={page}"
        
        html = fetch_url(url)
        if not html:
            print(f"  [能源界] p{page}: FAIL")
            continue
        
        links = re.findall(r'href="([^"]*escn\.com\.cn[^"]*)"', html)
        content = [l for l in links if ".shtml" in l]
        results.extend(content)
        print(f"  [能源界] p{page}: +{len(content)}")
        time.sleep(2)
    
    return list(set(results))

def fetch_csv_links():
    """直接抓取CSV模板里的已有链接"""
    results = []
    
    for url, platform, desc in CSV_LINKS:
        html = fetch_url(url)
        if html and len(html) > 1000:
            title = extract_title_from_html(html)
            results.append({
                "url": url,
                "platform": platform,
                "title": title,
                "desc": desc,
                "found_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            print(f"  [CSV] {platform}: OK - {title[:40] if title else '无标题'}")
        else:
            print(f"  [CSV] {platform}: FAIL")
        
        time.sleep(1)
    
    return results

def search_all():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    all_results = []
    
    print(f"[{timestamp}] 投标情报搜索（行业平台版）")
    print(f"{len(PLATFORMS)} 个平台 + {len(KEYWORDS)} 个关键词\n")
    
    # Step 1: 直接抓 CSV 已有链接
    print("[1] 抓取已验证链接...")
    csv_results = fetch_csv_links()
    all_results.extend(csv_results)
    
    # Step 2: 行业平台关键词搜索
    print("\n[2] 行业平台关键词搜索...")
    for kw in KEYWORDS:
        print(f"\n[{kw}]")
        
        bjx_links = fetch_bjx_list(kw, max_pages=2)
        for url in bjx_links:
            all_results.append({"keyword": kw, "url": url, "platform": "北极星能源网", "found_at": timestamp})
        
        escn_links = fetch_escn_list(kw, max_pages=2)
        for url in escn_links:
            all_results.append({"keyword": kw, "url": url, "platform": "能源界网", "found_at": timestamp})
        
        time.sleep(3)
    
    return all_results

def save_results(results):
    os.makedirs(DATA_DIR, exist_ok=True)
    out = f"{DATA_DIR}/bids_raw_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[保存] {out}")
    print(f"共 {len(results)} 条")

if __name__ == "__main__":
    results = search_all()
    save_results(results)
