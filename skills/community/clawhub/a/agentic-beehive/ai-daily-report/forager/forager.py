#!/usr/bin/env python3
"""
采蜜管线 — playwright 爬新闻+计费页

蜂巢采蜜：不是机械爬取，而是根据花期状态决定采蜜深度。
盛开 → 全量采蜜（新闻+计费+评测）
开花 → 标准采蜜（新闻+计费）
含苞 → 轻量检查（仅计费页）
凋谢 → 跳过
"""

import asyncio
import json
import re
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
REGISTRY_PATH = OUTPUT_DIR / "vendor_registry.json"


class Forager:
    """采蜜器 — 根据花期状态决定采蜜策略"""
    
    def __init__(self, registry_data: dict):
        self.vendors = registry_data.get("vendors", {})
    
    def get_forage_plan(self) -> dict:
        """根据花期状态生成采蜜计划"""
        plan = {
            "date": date.today().isoformat(),
            "full": [],      # 全量：新闻+计费
            "standard": [],  # 标准：新闻+计费
            "light": [],     # 轻量：仅计费
            "skip": [],      # 跳过
        }
        
        for name, v in self.vendors.items():
            score = v.get("bloom_score", 0)
            if score >= 0.7:
                plan["full"].append(name)
            elif score >= 0.4:
                plan["standard"].append(name)
            elif score >= 0.2:
                plan["light"].append(name)
            else:
                plan["skip"].append(name)
        
        return plan
    
    async def forage_all(self) -> dict:
        """执行全部采蜜任务"""
        plan = self.get_forage_plan()
        results = {
            "date": date.today().isoformat(),
            "forage_time": datetime.now().isoformat(),
            "plan_summary": {
                "full": len(plan["full"]),
                "standard": len(plan["standard"]),
                "light": len(plan["light"]),
                "skip": len(plan["skip"]),
            },
            "news": {},
            "pricing": {},
            "errors": [],
        }
        
        # 全量+标准采蜜：新闻+计费
        targets = plan["full"] + plan["standard"]
        for name in targets:
            v = self.vendors[name]
            urls = v.get("urls", {})
            
            # 采新闻
            if urls.get("news"):
                news_result = await self._forage_news(name, urls["news"])
                results["news"][name] = news_result
            
            # 采计费
            if urls.get("pricing"):
                price_result = await self._forage_pricing(name, urls["pricing"])
                results["pricing"][name] = price_result
        
        # 轻量：仅计费
        for name in plan["light"]:
            v = self.vendors[name]
            urls = v.get("urls", {})
            if urls.get("pricing"):
                price_result = await self._forage_pricing(name, urls["pricing"])
                results["pricing"][name] = price_result
        
        return results
    
    async def _forage_news(self, vendor_name: str, url: str) -> dict:
        """用 playwright 采蜜新闻页"""
        result = {
            "vendor": vendor_name,
            "url": url,
            "status": "pending",
            "headlines": [],
            "raw_text": "",
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                    await page.wait_for_timeout(2000)  # 等待 JS 渲染
                    
                    # 提取页面文本
                    text = await page.inner_text("body")
                    result["raw_text"] = text[:5000]  # 截断
                    
                    # 提取标题/链接
                    links = await page.eval_on_selector_all("a", """
                        (elements) => elements.slice(0, 30).map(a => ({
                            text: a.textContent?.trim()?.substring(0, 100),
                            href: a.href
                        })).filter(l => l.text && l.text.length > 5)
                    """)
                    
                    # 过滤有意义的新闻标题
                    for link in links:
                        text = link.get("text", "")
                        # 排除导航栏等噪声
                        if len(text) > 8 and not any(kw in text for kw in ["登录", "注册", "首页", "关于", "客服"]):
                            result["headlines"].append({
                                "title": text,
                                "url": link.get("href", ""),
                            })
                    
                    result["status"] = "ok"
                    
                except Exception as e:
                    result["status"] = "error"
                    result["error"] = str(e)
                finally:
                    await browser.close()
                    
        except ImportError:
            # playwright 不可用，降级为 web_fetch
            result = await self._forage_news_fallback(vendor_name, url)
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def _forage_news_fallback(self, vendor_name: str, url: str) -> dict:
        """降级采蜜：用 urllib 抓取"""
        result = {
            "vendor": vendor_name,
            "url": url,
            "status": "pending",
            "headlines": [],
            "raw_text": "",
        }
        
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "Accept": "text/html",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            
            # 简单提取文本
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            result["raw_text"] = text[:3000]
            
            # 提取 title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
            if title_match:
                result["headlines"].append({
                    "title": title_match.group(1).strip(),
                    "url": url,
                })
            
            result["status"] = "ok_fallback"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def _forage_pricing(self, vendor_name: str, url: str) -> dict:
        """用 playwright 采蜜计费页"""
        result = {
            "vendor": vendor_name,
            "url": url,
            "status": "pending",
            "models": [],
            "raw_text": "",
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                    await page.wait_for_timeout(2000)
                    
                    text = await page.inner_text("body")
                    result["raw_text"] = text[:8000]
                    
                    # 尝试提取价格信息
                    result["models"] = self._parse_pricing_text(vendor_name, text)
                    
                    result["status"] = "ok"
                    
                except Exception as e:
                    result["status"] = "error"
                    result["error"] = str(e)
                finally:
                    await browser.close()
                    
        except ImportError:
            result = await self._forage_pricing_fallback(vendor_name, url)
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def _forage_pricing_fallback(self, vendor_name: str, url: str) -> dict:
        """降级采蜜计费页"""
        result = {
            "vendor": vendor_name,
            "url": url,
            "status": "pending",
            "models": [],
            "raw_text": "",
        }
        
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "Accept": "text/html",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            result["raw_text"] = text[:5000]
            result["models"] = self._parse_pricing_text(vendor_name, text)
            result["status"] = "ok_fallback"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _parse_pricing_text(self, vendor_name: str, text: str) -> list:
        """
        从计费页文本中提取模型定价信息。
        这是一个通用解析器，各家格式不同，尝试多种模式。
        """
        models = []
        
        # 模式1: "模型名 ... ¥X / 百万token" 或 "$X / 1M tokens"
        # 模式2: "输入 ¥X/M  输出 ¥Y/M"
        # 模式3: "X 元/万token"
        
        # 常见国内厂商计费格式
        price_patterns = [
            # ¥X/百万token
            r'([\w\-\.]+(?:pro|max|lite|mini|plus|turbo|flash|v\d)?)\s*[：:]*\s*¥?\s*([\d.]+)\s*/\s*百万\s*token',
            # ¥X/M tokens
            r'([\w\-\.]+)\s*[：:]*\s*¥?\s*([\d.]+)\s*/\s*M\s*token',
            # X元/万token
            r'([\w\-\.]+)\s*[：:]*\s*([\d.]+)\s*元\s*/\s*万\s*token',
            # 输入/输出分开
            r'([\w\-\.]+)\s*.*?输入[：:]*\s*¥?\s*([\d.]+).*?输出[：:]*\s*¥?\s*([\d.]+)',
            # $X per 1M tokens
            r'([\w\-\.]+)\s*[：:]*\s*\$\s*([\d.]+)\s*(?:per|/)\s*1M\s*tokens?',
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for m in matches:
                model_name = m.group(1).strip()
                if len(model_name) < 2 or len(model_name) > 40:
                    continue
                
                entry = {
                    "vendor": vendor_name,
                    "model": model_name,
                    "source": "auto_parsed",
                }
                
                if m.lastindex == 2:
                    entry["price_per_million"] = float(m.group(2))
                    entry["unit"] = "per_million_tokens"
                elif m.lastindex == 3:
                    entry["input_price_per_million"] = float(m.group(2))
                    entry["output_price_per_million"] = float(m.group(3))
                    entry["unit"] = "per_million_tokens"
                
                # 去重
                if not any(e["model"] == model_name for e in models):
                    models.append(entry)
        
        return models


async def run_forage():
    """主采蜜入口"""
    # 加载注册表
    if not REGISTRY_PATH.exists():
        print("❌ 厂商注册表不存在，请先运行 scanner.py 初始化")
        return
    
    with open(REGISTRY_PATH) as f:
        registry_data = json.load(f)
    
    forager = Forager(registry_data)
    
    # 显示采蜜计划
    plan = forager.get_forage_plan()
    print(f"📋 采蜜计划 ({date.today()}):")
    print(f"  全量: {', '.join(plan['full']) or '无'}")
    print(f"  标准: {', '.join(plan['standard']) or '无'}")
    print(f"  轻量: {', '.join(plan['light']) or '无'}")
    print(f"  跳过: {', '.join(plan['skip']) or '无'}")
    
    # 执行采蜜
    print("\n🐝 开始采蜜...")
    results = await forager.forage_all()
    
    # 保存结果
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"forage_{date.today().isoformat()}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 采蜜完成，结果保存到 {output_path}")
    
    # 摘要
    news_count = sum(1 for v in results["news"].values() if v["status"].startswith("ok"))
    price_count = sum(1 for v in results["pricing"].values() if v["status"].startswith("ok"))
    print(f"  新闻采集: {news_count}/{len(results['news'])} 成功")
    print(f"  计费采集: {price_count}/{len(results['pricing'])} 成功")
    print(f"  错误: {len(results['errors'])}")


if __name__ == "__main__":
    asyncio.run(run_forage())
