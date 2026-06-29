#!/usr/bin/env python3
"""
A股上市公司年报采集脚本
数据来源：巨潮资讯网 cninfo.com.cn（官方指定信息披露平台）

用法：
    python fetch_annual_reports.py --code 600903 --name "贵州燃气" --years 2022-2025 --dir ./output

参数：
    --code      股票代码（必填）
    --name      股票名称（必填）
    --years     年份范围，如 2022-2025（必填）
    --dir       输出目录（必填）
    --market    市场：sh=上交所, sz=深交所（默认：sh）
"""

import requests
import os
import sys
import time
import random
import json
import argparse
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def parse_args():
    parser = argparse.ArgumentParser(description="A股上市公司年报采集")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--name", required=True, help="股票名称")
    parser.add_argument("--years", required=True, help="年份范围，如 2022-2025")
    parser.add_argument("--dir", required=True, help="输出目录")
    parser.add_argument("--market", default="sh", choices=["sh", "sz"], help="市场")
    return parser.parse_args()


def get_org_id(code, market):
    """构建巨潮orgId"""
    prefix = "gssh0" if market == "sh" else "szse"
    return f"{prefix}{code}"


def cninfo_query_announcements(code, org_id, page_size=50):
    """从巨潮资讯查询年报公告列表"""
    url = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
    payload = {
        "stock": f"{code},{org_id}",
        "tabName": "fulltext",
        "pageSize": str(page_size),
        "pageNum": "1",
        "column": "szsh",
        "category": "category_ndbg_szsh",
        "plate": "",
        "seDate": "",
        "searchkey": "",
        "secid": "",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }
    headers = {
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.cninfo.com.cn/new/disclosure",
        "Origin": "https://www.cninfo.com.cn",
    }
    r = requests.post(url, data=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json().get("announcements", []) or []


def ts_to_date(ts):
    """巨潮时间戳（毫秒）转日期字符串"""
    if isinstance(ts, (int, float)) and ts > 0:
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
    return str(ts)[:10] if ts else ""


def filter_annual_reports(announcements, year_range):
    """筛选目标年份的年度报告"""
    start_year, end_year = year_range
    # 年报通常在次年3-4月发布，所以发布年份 = 财年 + 1
    publish_start = start_year + 1
    publish_end = end_year + 1

    target = []
    for ann in announcements:
        title = ann.get("announcementTitle", "")
        date_str = ts_to_date(ann.get("announcementTime"))

        if "年度报告" not in title:
            continue
        if any(kw in title for kw in ["摘要", "更正", "英文"]):
            continue
        if date_str:
            pub_year = int(date_str[:4])
            if pub_year < publish_start or pub_year > publish_end:
                continue

        target.append({
            "title": title,
            "date": date_str,
            "annId": ann.get("announcementId", ""),
            "url": ann.get("adjunctUrl", ""),
            "type": ann.get("announcementTypeName", "年度报告"),
        })

    target.sort(key=lambda x: x["date"])
    return target


def download_pdf(ann, save_dir, stock_name):
    """下载年报PDF文件"""
    title = ann["title"]
    date = ann["date"]
    ann_id = ann["annId"]
    adj_url = ann["url"]

    safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_")
    safe_title = safe_title.replace("*", "_").replace("?", "_").replace('"', "_")
    safe_title = safe_title.replace("<", "_").replace(">", "_").replace("|", "_")
    filename = f"{date}_{stock_name}_{safe_title}.pdf"
    save_path = os.path.join(save_dir, filename)

    result = {
        "title": title, "date": date, "annId": ann_id,
        "filename": filename, "save_path": save_path,
        "source_url": f"https://static.cninfo.com.cn/{adj_url}" if adj_url else "",
        "detail_url": f"https://www.cninfo.com.cn/new/disclosure/detail?annoId={ann_id}",
        "status": "pending", "error": "",
    }

    if os.path.exists(save_path):
        result["status"] = "exists"
        return result

    if not adj_url:
        result["status"] = "no_url"
        return result

    if adj_url.startswith("http"):
        pdf_url = adj_url
    else:
        pdf_url = f"https://static.cninfo.com.cn/{adj_url}"
    result["source_url"] = pdf_url

    headers = {
        "User-Agent": UA,
        "Referer": "https://www.cninfo.com.cn/",
        "Accept": "application/pdf,*/*",
    }

    try:
        r = requests.get(pdf_url, headers=headers, timeout=120, stream=True)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        file_size = os.path.getsize(save_path)
        if file_size < 10000:
            os.remove(save_path)
            result["status"] = "failed"
            result["error"] = f"文件太小({file_size}字节)"
        else:
            result["status"] = "success"
            result["file_size"] = file_size
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        if os.path.exists(save_path):
            os.remove(save_path)

    return result


def main():
    args = parse_args()

    # 解析年份范围
    parts = args.years.split("-")
    year_range = (int(parts[0]), int(parts[1]))

    org_id = get_org_id(args.code, args.market)

    print("=" * 60)
    print(f"{args.name}（{args.code}）年报采集")
    print(f"数据来源：巨潮资讯网 cninfo.com.cn")
    print(f"年份范围：{year_range[0]}-{year_range[1]}")
    print(f"目标目录：{args.dir}")
    print("=" * 60)

    os.makedirs(args.dir, exist_ok=True)

    # Step 1: 查询公告
    print("\n[Step 1] 查询巨潮年报公告列表...")
    all_announcements = cninfo_query_announcements(args.code, org_id)
    print(f"  共查询到 {len(all_announcements)} 条年报公告")

    # Step 2: 筛选
    print(f"\n[Step 2] 筛选 {year_range[0]}-{year_range[1]} 年度报告...")
    targets = filter_annual_reports(all_announcements, year_range)

    if not targets:
        print("  [警告] 未找到符合条件的年报")
        for ann in all_announcements[:20]:
            print(f"    {ts_to_date(ann.get('announcementTime'))} | {ann.get('announcementTitle', '')}")
        return

    for t in targets:
        print(f"    {t['date']} | {t['title']}")

    # Step 3: 下载
    print("\n[Step 3] 下载年报PDF...")
    results = []
    for i, ann in enumerate(targets):
        print(f"\n  [{i+1}/{len(targets)}] {ann['title']}")
        result = download_pdf(ann, args.dir, args.name)
        results.append(result)
        print(f"    [{result['status']}] {result.get('error', '')}")
        if i < len(targets) - 1:
            time.sleep(random.uniform(2, 4))

    # Step 4: 生成日志
    log_file = os.path.join(args.dir, "采集日志.json")
    log = {
        "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "股票信息": {"名称": args.name, "代码": args.code, "市场": args.market.upper(), "orgId": org_id},
        "数据来源": {"平台": "巨潮资讯网", "URL": "https://www.cninfo.com.cn"},
        "采集结果": results,
        "统计": {
            "总计": len(results),
            "成功": sum(1 for r in results if r["status"] == "success"),
            "已存在": sum(1 for r in results if r["status"] == "exists"),
            "失败": sum(1 for r in results if r["status"] == "failed"),
        }
    }
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n采集完成！成功: {log['统计']['成功']}, 失败: {log['统计']['失败']}")


if __name__ == "__main__":
    main()
