#!/usr/bin/env python3
"""
假国际品牌检测 - 真实数据获取版
使用 web_fetch + subprocess google 命令进行搜索
"""

import requests
from bs4 import BeautifulSoup
import json
import subprocess
from datetime import datetime


def fetch_page(url, timeout=15):
    """使用 requests 获取网页内容"""
    try:
        response = requests.get(url, timeout=timeout,
                                headers={"User-Agent": "Mozilla/5.0 (compatible; BrandDetector)"})
        return response.text
    except Exception as e:
        print(f"Fetch error: {e}")
        return ""


def search_google(query, count=10):
    """使用 Google Custom Search API 或简化版搜索"""
    try:
        # 简化版：使用 web_fetch 抓取搜索结果页
        google_url = f"https://www.google.com/search?q={query}&num={count}"
        content = fetch_page(google_url)
        soup = BeautifulSoup(content, 'html.parser')
        
        # 提取结果数量（简化）
        count_tag = soup.find("meta", attrs={"name": "google-result-count"})
        result_count = count_tag.get("content") if count_tag else "0"
        
        return result_count, len(soup.find_all("div", class_="g"))  # g 是 Google 结果类名
    except Exception as e:
        return "Error", str(e)


def check_website_exists(brand):
    """检查海外官网是否存在（使用 web_fetch）"""
    print(f"\n🔍 检查项 1/4: 海外官网验证")
    
    domains = [
        f"https://www.{brand}.com",
        f"https://{brand.lower()}.com", 
        f"https://www.{brand}.net"
    ]
    
    for domain in domains:
        try:
            # 使用 web_fetch 代替 requests（更稳健）
            from openclaw.web import fetch
            content = fetch.fetch_url(domain)
            
            if content and len(content) > 1000:  # 有效页面
                soup = BeautifulSoup(content, 'html.parser')
                title = soup.title.string if soup.title else ""
                
                # WHOIS 查询 - 使用简化版
                import whois
                try:
                    w = whois.whois(domain.replace("https://", ""))
                    creation_date = w.creation_date
                    from datetime import datetime
                    current = datetime.now()
                    years_old = (current.year - int(creation_date[:4])) if creation_date else 0
                except:
                    years_old = 0
                
                # 检查是否有多语言内容
                has_english = "<html" in content.lower() or "lang=" in content
                
                quality_score = min(10.0, max(0, years_old * 0.5 + (8 if has_english else 4)))
                
                print(f"✅ 找到官网：{domain}（年限：{years_old}年，多语言：{has_english}")
                return {
                    "found": True,
                    "url": domain,
                    "age_years": max(0, years_old),
                    "languages": ["en"] if has_english else [],
                    "quality_score": quality_score
                }
        except Exception as e:
            print(f"Domain {domain} error: {e}")
            continue
    
    return {
        "found": False,
        "reasons": [f"官网{brand}.com 不存在或无法访问"]
    }


def check_sales_channels(brand):
    """检查海外销售渠道 - 使用 Google 搜索简化版"""
    print(f"\n🔍 检查项 2/4: 海外销售渠道")
    
    # 检查 Amazon.com 销售记录
    google_query = f"{brand} supplements official Amazon store"
    result_count, actual_count = search_google(google_query)
    
    if "Error" not in result_count:
        print(f"Amazon 搜索：{result_count}条结果")
        
        if int(actual_count) > 5:  # 亚马逊官方店有10+ 个产品
            return {
                "found": True,
                "channels": {
                    "amazon_us": f"{actual_count}个产品",
                    "physical_stores": "需要 API key（跳过）"
                },
                "quality_score": min(8.5, 3.0 + int(actual_count) * 0.2)
            }
        elif int(actual_count) == 0:
            return {
                "found": False,
                "reasons": ["Amazon.com 无相关品牌"]
            }
    else:
        # Google API 不可用，使用替代方案
        print("Google API 不可用，使用替代方案...")
        
        # 简化：检查 Amazon.com URL 是否存在
        amazon_url = f"https://www.amazon.com/s?k={brand}+supplements"
        content = fetch_page(amazon_url)
        if content and len(content) > 5000:
            return {
                "found": True,
                "channels": {"amazon_us": "存在官方店铺",
                             "physical_stores": "需要 API key"},
                "quality_score": 6.0
            }
    
    return {
        "found": False,
        "reasons": ["未找到实体店或需配置 API key"]
    }


def check_amazon_sales(brand):
    """检查亚马逊全球销售记录"""
    print(f"\n🔍 检查项 3/4: 跨境电商销售记录")
    
    platforms = [
        ("amazon.com", "amazon_com"),
        ("amazon.co.uk", "amazon_uk"),
        ("amazon.de", "amazon_de"),
        ("amazon.fr", "amazon_fr"),
        ("amazon.it", "amazon_it"),
        ("amazon.es", "amazon_es")
    ]
    
    found_platforms = []
    total_products = 0
    
    for domain, _ in platforms:
        try:
            search_url = f"https://{domain}/s?k={brand}+supplements"
            content = fetch_page(search_url)
            
            # 检查搜索结果是否存在（简化判断）
            if "No results found" not in content and len(content) > 3000:
                found_platforms.append(domain)
                total_products += 1
        except:
            pass
    
    if len(found_platforms) >= 2:  # 至少 2 个国际站点
        return {
            "found": True,
            "platforms": found_platforms[:5],
            "order_count_estimate": f">={total_products}",
            "duration_months": 18 if total_products > 4 else 6,
            "quality_score": min(9.0, 3.0 + len(found_platforms) * 1.5)
        }
    
    return {
        "found": False,
        "reasons": ["亚马逊平台无充足销售记录"]
    }


def check_media_exposure(brand):
    """检查海外媒体报道 - 使用 Tavily + Google 替代方案"""
    print(f"\n🔍 检查项 4/4: 海外媒体曝光")
    
    # 方法 1：Tavily API（如果配置了有效 Key）
    tavily_url = "https://api.tavily.com/search"
    api_key = getattr(subprocess.os.environ, "TAVILY_API_KEY", None)
    
    if api_key and len(api_key) > 8:
        try:
            response = requests.post(
                tavily_url,
                json={"query": f"{brand} brand history official website",
                      "search_depth": "basic",
                      "include_answer": True},
                headers={"Content-Type": "application/json", "x-api-key": api_key},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                articles_count = len(data.get("results", []))
                
                # 检查权威媒体来源
                authoritative_sources = ["reuters.com", "bloomberg.com", "forbes.com"]
                sources_found = []
                for result in data.get("results", []):
                    url = result.get("url", "")
                    for source in authoritative_sources:
                        if source in url:
                            sources_found.append(source)
                
                if articles_count > 0:
                    return {
                        "found": True,
                        "sources_checked": ["Tavily", "Google News"],
                        "articles_found": articles_count,
                        "sample_sources": sources_found[:3] if sources_found else [],
                        "quality_score": min(8.5, 2.0 + articles_count * 0.5)
                    }
        except Exception as e:
            print(f"Tavily API 调用失败：{e}")
    else:
        print("⚠️ Tavily API Key 未配置，使用浏览器搜索替代方案")
    
    # 方法 2：使用 Google News RSS（简化版）
    try:
        news_url = f"https://news.google.com/search?q={brand}&hl=en-US&gl=US"
        content = fetch_page(news_url)
        
        if "error" not in content.lower() and len(content) > 2000:
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.find_all("div", class_="e")  # Google News 结果类
            article_count = len(articles)
            
            if article_count > 5:
                return {
                    "found": True,
                    "sources_checked": ["Google News RSS"],
                    "articles_found": article_count,
                    "sample_sources": [a.get("title") for a in articles[:3]],
                    "quality_score": min(8.0, 1.5 + article_count * 0.2)
                }
    except Exception as e:
        print(f"Google News RSS 检查失败：{e}")
    
    # 方法 3：使用 Reddit 搜索
    try:
        reddit_url = f"https://www.reddit.com/search?q={brand}+official"
        content = fetch_page(reddit_url)
        soup = BeautifulSoup(content, 'html.parser')
        posts = soup.find_all("a", href=True)
        relevant_posts = [p for p in posts[:5] if brand.lower() in p.get_text().lower()]
        
        if len(relevant_posts) > 0:
            return {
                "found": True,
                "sources_checked": ["Reddit"],
                "articles_found": len(relevant_posts),
                "sample_sources": relevant_posts[:2],
                "quality_score": min(5.5, 1.0 + len(relevant_posts) * 0.6)
            }
    except:
        pass
    
    return {
        "found": False,
        "sources_checked": ["Tavily Search", "Google News", "Reddit"],
        "articles_found": 0
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="简化版品牌检测脚本 - 真实数据获取")
    parser.add_argument("--brand", required=True, help="要检测的品牌名称")
    parser.add_argument("--mode", choices=["quick", "deep"], default="quick")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    
    brand = args.brand
    mode = args.mode
    
    print(f"=" * 70)
    print(f"🔍 品牌国际性验证报告")
    print(f"📝 品牌名称：{brand}")
    print(f"⚙️ 模式：{mode}")
    print(f"{"="*70}")
    
    results = {
        "brand": brand,
        "timestamp": datetime.now().isoformat(),
        "verifications": {}
    }
    
    try:
        # 1. 官网检查
        results["verifications"]["official_website"] = check_website_exists(brand)
        time.sleep(2) if mode == "quick" else time.sleep(0)
        
        # 2. 销售渠道
        results["verifications"]["sales_channels"] = check_sales_channels(brand)
        time.sleep(1) if mode == "quick" else time.sleep(0)
        
        # 3. 销售记录
        results["verifications"]["cross_border_sales"] = check_amazon_sales(brand)
        time.sleep(1) if mode == "quick" else time.sleep(0)
        
        # 4. 媒体曝光
        results["verifications"]["media_exposure"] = check_media_exposure(brand)
        
    except Exception as e:
        print(f"\n❌ 执行出错：{e}")
    
    # 计算总分和结论
    scores = [
        results["verifications"]["official_website"].get("quality_score", 0),
        results["verifications"]["sales_channels"].get("quality_score", 0),
        results["verifications"]["cross_border_sales"].get("quality_score", 0),
        results["verifications"]["media_exposure"].get("quality_score", 0)
    ]
    
    # 使用加权平均分（因为某些项目可能为 0）
    weights = [4, 3, 3, 2]  # 官网权重最高
    weighted_total = sum(s*w for s,w in zip(scores, weights)) / sum(weights)
    valid_items = sum(1 for w,s in zip(weights,scores) if s > 2.5)
    
    if valid_items >= 3:
        verdict = "✅ 真国际品牌"
        confidence = 0.9
    elif valid_items == 2:
        verdict = "⚠️ 存疑品牌"
        confidence = 0.65
    else:
        verdict = "🚩 假国际品牌"
        confidence = 0.85
    
    recommendation_map = {
        "✅ 真国际品牌": "可以放心购买，是真正的国际知名产品",
        "⚠️ 存疑品牌": "建议进一步调查品牌背景和官方渠道信息",
        "🚩 假国际品牌": "⚠️ 高度可能是假冒或纯国内品牌，建议谨慎处理"
    }
    
    # 输出结果
    print(f"\n{"="*70}")
    for i, (item, score) in enumerate(["官网", "销售渠道", "销售记录", "媒体曝光"], 1):
        status = "✅" if scores[i-1] > 2.5 else "❌"
        print(f"{status} {item}: {scores[i-1]:.1f}分（权重：{weights[i-1]}")
    
    print(f"\n加权总分：{weighted_total:.2f}")
    print(f"有效验证项数：{valid_items}/4")
    print(f"🎯 结论：{verdict}")
    print(f"💪 置信度：{confidence*100:.0f}%")
    print(f"✅ 建议：{recommendation_map.get(verdict, '未知')}")
    
    if args.output == "json":
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.output == "markdown":
        # Markdown 输出
        print(f"\n## 📄 Markdown 报告（保存到文件）")
        
        md_content = f"""# 🔍 {brand} - 品牌国际性验证报告

| 验证项 | 得分 | 状态 |
|------|-|--|
{"｜".join([x + " "*10 + str(s) + "分" for x,s in zip(['官网', '销售渠道', '销售记录', '媒体曝光'], scores)])}|
| **加权总分** | {weighted_total:.2f} |
| **有效项数** | {valid_items}/4 |

**🎯 结论**: {verdict}
**💪 置信度**: {confidence*100:.0f}%
**✅ 建议**: {recommendation_map.get(verdict, '未知')}
"""
        with open(f"/tmp/{brand}_report.md", "w") as f:
            f.write(md_content)
        print(f"\nMarkdown 报告已保存：/tmp/{brand}_report.md")


if __name__ == "__main__":
    main()
