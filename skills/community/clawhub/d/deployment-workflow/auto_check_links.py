#!/usr/bin/env python3
"""
测试链接自动验证脚本
功能：当群内有人发测试链接时，自动提取链接、验证、记录、汇报

使用方式：
1. 监听群消息
2. 检测到测试链接时自动触发
3. 用Playwright验证链接
4. 记录到memory
5. 汇报结果
"""

import re
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# CDP连接地址
CDP_URL = "http://localhost:18800"

# 测试链接关键词（用于识别测试汇报）
TEST_KEYWORDS = ["测试链接", "测试", "联通率", "验证"]

# 需要验证的域名（可根据实际情况配置）
VALID_DOMAINS = ["mogu", "baipiao", "one", "dg1113"]

def extract_links(text):
    """从文本中提取链接"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    return urls

def is_test_link(url):
    """判断是否为测试链接 - 使用严格域名解析"""
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # 必须是完整域名匹配，不能子串匹配
        return any(domain == d or domain.endswith('.' + d) for d in VALID_DOMAINS)
    except:
        return False

def verify_link(url, timeout=30000):
    """验证单个链接"""
    result = {
        "url": url,
        "status": "unknown",
        "page_load_ok": False,
        "download_ok": False,
        "video_ok": False,
        "error": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            page = browser.new_page()
            
            # 打开页面
            response = page.goto(url, wait_until="networkidle", timeout=timeout)
            
            # 检查页面加载
            if response and response.ok:
                result["page_load_ok"] = True
                result["status"] = "ok"
            
            # 检查下载按钮/提示
            download_keywords = ["下载", "download", "安装", "app"]
            page_content = page.content().lower()
            result["download_ok"] = any(kw in page_content for kw in download_keywords)
            
            # 检查视频播放
            video_elements = page.query_selector_all("video")
            result["video_ok"] = len(video_elements) > 0
            
            browser.close()
            
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    
    return result

def format_report(results):
    """格式化汇报"""
    total = len(results)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    
    report = f"【测试链接自动验证】{ok_count}/{total} 通过\n\n"
    
    for r in results:
        status = "✓" if r["status"] == "ok" else "✗"
        report += f"{status} {r['url'][:50]}...\n"
        report += f"  页面加载: {'是' if r['page_load_ok'] else '否'}\n"
        report += f"  下载提示: {'是' if r['download_ok'] else '否'}\n"
        if r.get("error"):
            report += f"  错误: {r['error'][:30]}\n"
        report += "\n"
    
    return report

def save_to_memory(results, reporter="白浅"):
    """保存到memory文件"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = f"/root/.openclaw/workspace/memory/{today}.md"
    
    timestamp = datetime.now().strftime("%H:%M")
    content = f"\n### {timestamp} - 测试链接自动验证\n"
    content += f"汇报人：{reporter}\n"
    content += f"验证结果：{len(results)}个链接\n"
    
    for r in results:
        status = "✓" if r["status"] == "ok" else "✗"
        content += f"- {status} {r['url']}\n"
    
    # 追加到文件
    try:
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"保存memory失败: {e}")
    
    return content

def process_message(text, sender="白浅"):
    """处理消息，提取并验证测试链接"""
    # 提取链接
    links = extract_links(text)
    
    if not links:
        return None
    
    # 过滤测试链接
    test_links = [link for link in links if is_test_link(link)]
    
    if not test_links:
        return None
    
    print(f"发现{len(test_links)}个测试链接，开始验证...")
    
    # 验证每个链接
    results = []
    for link in test_links:
        print(f"验证: {link}")
        result = verify_link(link)
        results.append(result)
        print(f"  结果: {result['status']}")
    
    # 保存到memory
    save_to_memory(results, sender)
    
    # 生成汇报
    report = format_report(results)
    
    return report

# 测试用
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行测试
        test_text = " ".join(sys.argv[1:])
        result = process_message(test_text)
        if result:
            print(result)
        else:
            print("未发现测试链接")
    else:
        print("使用方法: python3 auto_check_links.py <文本内容>")
        print("示例: python3 auto_check_links.py 测试链接 https://mogu6.com/test1")
