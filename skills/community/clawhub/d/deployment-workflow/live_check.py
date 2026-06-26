#!/usr/bin/env python3
"""
自动化巡检脚本
功能：主动巡检App落地页和下载链接存活状态

使用：python3 live_check.py
"""

import re
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

CDP_URL = "http://localhost:18800"

# 需要巡检的App配置
APPS = [
    {"name": "母狗园", "domains": ["mogu", "dg1113"]},
    {"name": "白嫖之家", "domains": ["baipiao", "dg1113"]},
    {"name": "ONE视频", "domains": ["onevideo", "dg1113"]},
]

def check_app_links(app_name, domains):
    """检查App的所有链接"""
    results = {
        "app": app_name,
        "links": [],
        "total": 0,
        "ok": 0,
        "error": 0
    }
    
    # 常见的落地页和下载链接模式
    link_patterns = [
        f"https://{domains[0]}.com",
        f"https://www.{domains[0]}.com",
        f"https://{domains[1]}.81dbyv81.work",
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        
        for pattern in link_patterns:
            link_result = {
                "url": pattern,
                "status": "unknown",
                "page_load": False,
                "download": False,
                "error": None
            }
            
            try:
                page = browser.new_page()
                response = page.goto(pattern, timeout=15000, wait_until="domcontentloaded")
                
                if response and response.ok:
                    link_result["page_load"] = True
                    link_result["status"] = "ok"
                    
                    # 检查下载相关元素
                    content = page.content().lower()
                    if any(kw in content for kw in ["下载", "download", "安装", "app"]):
                        link_result["download"] = True
                        
                page.close()
                
            except Exception as e:
                link_result["status"] = "error"
                link_result["error"] = str(e)[:50]
            
            results["links"].append(link_result)
            results["total"] += 1
            if link_result["status"] == "ok":
                results["ok"] += 1
            else:
                results["error"] += 1
        
        browser.close()
    
    return results

def check_all_apps():
    """巡检所有App"""
    all_results = []
    total_links = 0
    total_ok = 0
    
    print("=" * 50)
    print("开始自动化巡检...")
    print("=" * 50)
    
    for app in APPS:
        print(f"\n巡检 {app['name']}...")
        result = check_app_links(app["name"], app["domains"])
        all_results.append(result)
        total_links += result["total"]
        total_ok += result["ok"]
        
        print(f"  总链接: {result['total']}, 正常: {result['ok']}, 异常: {result['error']}")
    
    print("\n" + "=" * 50)
    print(f"巡检完成: {total_ok}/{total_links} 正常")
    print("=" * 50)
    
    return all_results

def format_report(results):
    """格式化巡检报告"""
    total = sum(r["total"] for r in results)
    ok = sum(r["ok"] for r in results)
    
    report = f"【自动化巡检报告】{ok}/{total} 正常\n\n"
    
    for r in results:
        status = "✓" if r["error"] == 0 else "⚠"
        report += f"{status} {r['app']}: {r['ok']}/{r['total']} 正常\n"
        for link in r["links"]:
            s = "✓" if link["status"] == "ok" else "✗"
            report += f"  {s} {link['url'][:40]}...\n"
    
    return report

if __name__ == "__main__":
    results = check_all_apps()
    report = format_report(results)
    print(report)
