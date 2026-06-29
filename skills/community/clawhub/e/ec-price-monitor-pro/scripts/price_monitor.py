#!/usr/bin/env python3
"""
电商价格监控脚本
支持平台：淘宝、拼多多、京东
通过网页搜索获取商品价格信息
"""

import json
import os
import sys
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# === 配置加载 ===
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "references", "config.yaml")

def load_config():
    import yaml
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def search_platform(keyword, platform):
    """
    在指定平台搜索商品，返回价格列表
    使用通用搜索方式获取公开信息
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    search_urls = {
        "taobao": f"https://s.taobao.com/search?q={urllib.parse.quote(keyword)}",
        "pdd": f"https://mobile.yangkeduo.com/search_result.html?search_key={urllib.parse.quote(keyword)}",
        "jd": f"https://search.jd.com/Search?keyword={urllib.parse.quote(keyword)}&enc=utf-8",
    }
    
    url = search_urls.get(platform)
    if not url:
        return []
    
    results = []
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        
        # 提取价格（简化版）
        price_patterns = [
            r'"price"[:\s]*"?(\d+[\.\d]*)',
            r'price["\']?\s*[:=]\s*["\']?(\d+[\.\d]*)',
            r'"view_price"[:\s]*"?(\d+[\.\d]*)',
            r'¥(\d+[\.\d]*)',
        ]
        
        prices = []
        for pat in price_patterns:
            found = re.findall(pat, html)
            for p in found:
                try:
                    val = float(p)
                    if 1 < val < 999999:
                        prices.append(val)
                except ValueError:
                    continue
            if prices:
                break
        
        if prices:
            results = [{"platform": platform, "keyword": keyword, "price": min(prices)}]
    except Exception as e:
        results = [{"platform": platform, "keyword": keyword, "price": None, "error": str(e)}]
    
    return results


def check_price_diff(results):
    """检测同一商品在不同平台的价差"""
    if not results or len(results) < 2:
        return []
    
    alerts = []
    prices = [(r["platform"], r["price"]) for r in results if r.get("price")]
    
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            p1_name, p1 = prices[i]
            p2_name, p2 = prices[j]
            if p1 and p2:
                diff = abs(p1 - p2)
                if diff >= load_config().get("price_diff_threshold", 50):
                    cheaper = p1_name if p1 < p2 else p2_name
                    alerts.append({
                        "platform_a": p1_name, "price_a": p1,
                        "platform_b": p2_name, "price_b": p2,
                        "diff": diff,
                        "cheaper": cheaper
                    })
    return alerts


def format_report(results, alerts, item_config):
    """格式化输出报告"""
    lines = []
    lines.append(f"📊 价格监控报告 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 40)
    
    keyword = item_config["keyword"]
    lines.append(f"\n📍 {keyword}")
    
    for r in results:
        price_str = f"¥{r['price']:,.0f}" if r.get("price") else "获取失败"
        lines.append(f"  {r['platform']}: {price_str}")
    
    if alerts:
        lines.append(f"\n⚡ 价差提醒（阈值 ¥{load_config().get('price_diff_threshold', 50)}）:")
        for a in alerts:
            lines.append(f"  {a['platform_a']} ¥{a['price_a']:,.0f} ↔ {a['platform_b']} ¥{a['price_b']:,.0f}")
            lines.append(f"  差价: ¥{a['diff']:,.0f} → 推荐去 {a['cheaper']}")
    
    # 检测是否低于目标价
    max_price = item_config.get("max_price", 0)
    for r in results:
        if r.get("price") and max_price and r["price"] < max_price:
            lines.append(f"\n🎉 降价提醒！{r['platform']} ¥{r['price']:,.0f} 低于目标价 ¥{max_price:,.0f}")
    
    return "\n".join(lines)


def push_notify(message, config):
    """推送到配置的渠道"""
    notify = config.get("notify", {})
    
    # Feishu
    webhook = notify.get("feishu_webhook", "")
    if webhook:
        try:
            data = json.dumps({"msg_type": "text", "content": {"text": message}}).encode()
            req = urllib.request.Request(webhook, data=data, 
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
        except:
            pass
    
    # Telegram
    token = notify.get("telegram_token", "")
    chat_id = notify.get("telegram_chat_id", "")
    if token and chat_id:
        try:
            text = urllib.parse.quote(message[:4000])
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
            urllib.request.urlopen(url, timeout=5)
        except:
            pass


def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("请检查 references/config.yaml 是否存在且格式正确")
        sys.exit(1)
    
    # 支持命令行指定关键词
    if len(sys.argv) > 1:
        keywords = [{"keyword": " ".join(sys.argv[1:]), "max_price": 0, "platforms": ["taobao", "pdd", "jd"]}]
    else:
        keywords = config.get("items", [])
    
    if not keywords:
        print("❌ 未配置监控商品，请在 config.yaml 的 items 中添加")
        sys.exit(1)
    
    all_alerts = []
    for item in keywords:
        keyword = item["keyword"]
        platforms = item.get("platforms", ["taobao", "pdd", "jd"])
        
        results = []
        for p in platforms:
            time.sleep(0.5)  # 请求间隔
            pr = search_platform(keyword, p)
            results.extend(pr)
        
        alerts = check_price_diff(results)
        all_alerts.extend(alerts)
        
        report = format_report(results, alerts, item)
        print(report)
        print()
        
        # 有价差或降价时推送
        if alerts:
            push_notify(report, config)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
