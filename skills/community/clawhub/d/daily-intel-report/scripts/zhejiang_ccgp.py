#!/usr/bin/env python3
"""浙江政府采购网数据抓取模块 - 按关键词筛选公告"""

import urllib.request
import json
import sys
from datetime import datetime

# API配置
API_URL = "http://www.ccgp-zhejiang.gov.cn/portal/searchHome"

# 公告分类
CATEGORIES = {
    "采购项目公告": {
        "code": "110-606633",
        "subCodes": ["110-306476", "110-684034", "110-511933"]
    },
    "采购意向公开": {
        "code": "110-606633",
        "subCodes": ["110-600268"]
    },
    "采购结果公告": {
        "code": "110-606633",
        "subCodes": ["110-188043", "110-631167"]
    }
}

# 默认关键词
DEFAULT_KEYWORDS = ["AI", "人工智能", "语音", "语音室", "云桌面", "大模型", "智能", "算力", "软件", "系统", "平台", "数据"]


def fetch_notices(category_name="采购项目公告", page_size=50):
    """获取指定分类的公告列表"""
    cat = CATEGORIES.get(category_name, CATEGORIES["采购项目公告"])
    
    payload = json.dumps({
        "code": cat["code"],
        "subCodes": cat["subCodes"],
        "pageSize": page_size
    }).encode()
    
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": "http://www.ccgp-zhejiang.gov.cn/"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("result", {}).get("data", {}).get("children", [])
    except Exception as e:
        print(f"[错误] 获取{category_name}失败: {e}", file=sys.stderr)
        return []


def filter_by_keywords(notices, keywords=None):
    """按关键词筛选公告"""
    if keywords is None:
        keywords = DEFAULT_KEYWORDS
    
    matched = []
    for notice in notices:
        title = notice.get("title", "")
        purchase_name = notice.get("purchaseName", "")
        text = title + purchase_name
        
        for kw in keywords:
            if kw in text:
                matched.append(notice)
                break
    
    return matched


def format_notice(notice, index=None):
    """格式化单条公告"""
    title = notice.get("title", "无标题")
    pub_date = notice.get("publishDateString", "")
    district = notice.get("districtName", "")
    buyer = notice.get("purchaseName", "")
    article_id = notice.get("articleId", "")
    bid_time_ts = notice.get("bidOpeningTime")
    
    # 计算开标时间
    bid_time = ""
    if bid_time_ts:
        bid_time = datetime.fromtimestamp(bid_time_ts / 1000).strftime("%Y-%m-%d")
    
    # 构建详情链接
    link = f"http://www.ccgp-zhejiang.gov.cn/site/detail?articleId={article_id}" if article_id else ""
    
    prefix = f"{index}. " if index else ""
    lines = [
        f"{prefix}【{pub_date}】{title}",
        f"   采购人：{buyer} | 地区：{district}",
    ]
    if bid_time:
        lines.append(f"   开标时间：{bid_time}")
    if link:
        lines.append(f"   链接：{link}")
    
    return "\n".join(lines)


def run(keywords=None, page_size=50):
    """主执行函数：抓取+筛选+格式化输出"""
    all_matched = []
    
    for cat_name in CATEGORIES:
        notices = fetch_notices(cat_name, page_size)
        matched = filter_by_keywords(notices, keywords)
        for m in matched:
            m["_category"] = cat_name
        all_matched.extend(matched)
    
    # 去重（按articleId）
    seen = set()
    unique = []
    for n in all_matched:
        aid = n.get("articleId", "")
        if aid and aid not in seen:
            seen.add(aid)
            unique.append(n)
    
    return unique


if __name__ == "__main__":
    # 支持命令行传入关键词
    kw = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    results = run(keywords=kw)
    
    if not results:
        print("今日暂无匹配公告")
    else:
        print(f"共筛选到 {len(results)} 条匹配公告：\n")
        for i, notice in enumerate(results, 1):
            print(format_notice(notice, i))
            print()
