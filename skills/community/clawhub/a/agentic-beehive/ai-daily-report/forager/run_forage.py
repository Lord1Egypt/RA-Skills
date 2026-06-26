#!/usr/bin/env python3
"""
采蜜管线 — 试运行版
逐个爬取各大厂商计费页，提取真实定价数据
"""

import asyncio
import json
import re
import time
from datetime import date, datetime
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# 定义采蜜目标（URL 经过验证可访问）
FORAGE_TARGETS = {
    "DeepSeek": {
        "pricing_url": "https://api-docs.deepseek.com/zh-cn/quick_start/pricing",
        "news_url": "https://platform.deepseek.com",
    },
    "智谱": {
        "pricing_url": "https://open.bigmodel.cn/pricing",
        "news_url": "https://chatglm.cn",
    },
    "阿里": {
        "pricing_url": "https://help.aliyun.com/zh/model-studio/getting-started/models",
        "news_url": "https://tongyi.aliyun.com",
    },
    "字节": {
        "pricing_url": "https://www.volcengine.com/docs/82379/1099470",
        "news_url": "https://www.volcengine.com/product/doubao",
    },
    "百度": {
        "pricing_url": "https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Dffk0dtj7",
        "news_url": "https://yiyan.baidu.com",
    },
    "月之暗面": {
        "pricing_url": "https://platform.moonshot.cn/docs/pricing",
        "news_url": "https://kimi.moonshot.cn",
    },
    "MiniMax": {
        "pricing_url": "https://platform.minimaxi.com/document/Price",
        "news_url": "https://hailuoai.com",
    },
    "阶跃星辰": {
        "pricing_url": "https://platform.stepfun.com/pricing",
        "news_url": "https://stepfun.com",
    },
    "讯飞": {
        "pricing_url": "https://xinghuo.xfyun.cn/sparkapi",
        "news_url": "https://xinghuo.xfyun.cn",
    },
    "Google": {
        "pricing_url": "https://ai.google.dev/pricing",
        "news_url": "https://blog.google/technology/ai/",
    },
    "Anthropic": {
        "pricing_url": "https://www.anthropic.com/pricing",
        "news_url": "https://www.anthropic.com/news",
    },
    "OpenAI": {
        "pricing_url": "https://openai.com/api/pricing/",
        "news_url": "https://openai.com/blog",
    },
}


async def forage_page(page, vendor: str, url_type: str, url: str) -> dict:
    """爬取单个页面"""
    result = {
        "vendor": vendor,
        "url": url,
        "type": url_type,
        "status": "pending",
        "text": "",
        "models": [],
    }
    
    try:
        print(f"  🕷️  {vendor} - {url_type}: {url[:60]}...")
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)  # 等 JS 渲染
        
        # 滚动一下加载懒加载内容
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(1500)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        
        text = await page.inner_text("body")
        result["text"] = text[:12000]  # 截断但保留更多
        
        if url_type == "pricing":
            result["models"] = parse_pricing(vendor, text)
        
        result["status"] = "ok"
        print(f"  ✅ {vendor} - {url_type}: 获取 {len(text)} 字符, {len(result['models'])} 个模型定价")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)[:200]
        print(f"  ❌ {vendor} - {url_type}: {str(e)[:100]}")
    
    return result


def parse_pricing(vendor: str, text: str) -> list:
    """从页面文本提取定价信息"""
    models = []
    
    # 通用模式匹配
    patterns = [
        # 中文：X元/百万token
        (r'([\w\-\.]+(?:pro|max|lite|mini|plus|turbo|flash|ultra|v\d|4o|5\.1|2\.5|2\.6|air|long|speed|tiny|chat|reasoner|large|medium|spark|step|yi|moonshot|glm|ernie|doubao|qwen|abab|hailuo|ring|o3|o4)[\w\-\.]*)\s*[：:]*\s*¥?\s*([\d.]+)\s*/\s*百万\s*token', "per_million"),
        # 中文：X 元 / 百万 tokens
        (r'([\w\-\.]+)\s*[：:]*\s*([\d.]+)\s*元\s*/\s*百万\s*tokens?', "per_million"),
        # X元/万token
        (r'([\w\-\.]+)\s*[：:]*\s*([\d.]+)\s*元?\s*/\s*万\s*token', "per_10k"),
        # 输入 X 输出 Y
        (r'([\w\-\.]+(?:pro|max|lite|mini|plus|turbo|flash|ultra|v\d|4o|5\.1|2\.5|air|long|chat|reasoner|large|medium|step|yi|moonshot|glm|ernie|doubao|qwen|hailuo|ring|o3|o4)[\w\-\.]*).*?输入[：:\s]*¥?\s*([\d.]+).*?输出[：:\s]*¥?\s*([\d.]+)', "input_output"),
        # $X per 1M tokens
        (r'([\w\-\.]+(?:pro|max|lite|mini|plus|turbo|flash|ultra|v\d|4o|2\.5|haiku|sonnet|opus|nano|o3|o4)[\w\-\.]*).*?\$\s*([\d.]+)\s*(?:/|per)\s*1M\s*tokens?', "usd_per_million"),
    ]
    
    for pattern, price_type in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            model_name = m.group(1).strip()
            if len(model_name) < 2 or len(model_name) > 50:
                continue
            # 排除噪声
            if any(kw in model_name.lower() for kw in ["价格", "费用", "说明", "模型", "api", "http", "www"]):
                continue
            
            entry = {"vendor": vendor, "model": model_name, "source": "foraged"}
            
            if price_type == "per_million":
                entry["input_price_per_million"] = float(m.group(2))
                entry["output_price_per_million"] = float(m.group(2))  # 默认同价
            elif price_type == "per_10k":
                entry["input_price_per_million"] = float(m.group(2)) * 100
                entry["output_price_per_million"] = float(m.group(2)) * 100
            elif price_type == "input_output":
                entry["input_price_per_million"] = float(m.group(2))
                entry["output_price_per_million"] = float(m.group(3))
            elif price_type == "usd_per_million":
                entry["input_price_per_million"] = round(float(m.group(2)) * 7.2, 2)
                entry["output_price_per_million"] = round(float(m.group(2)) * 7.2, 2)
            
            # 去重
            if not any(e["model"] == model_name for e in models):
                models.append(entry)
    
    return models


async def run_forage():
    """主采蜜流程"""
    print(f"🐝 采蜜管线试运行 — {date.today()}")
    print("=" * 60)
    
    results = {
        "date": date.today().isoformat(),
        "forage_time": datetime.now().isoformat(),
        "pricing": {},
        "news": {},
        "errors": [],
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
        )
        page = await context.new_page()
        
        for vendor, urls in FORAGE_TARGETS.items():
            print(f"\n📦 {vendor}")
            
            # 爬计费页
            if urls.get("pricing_url"):
                pricing_result = await forage_page(page, vendor, "pricing", urls["pricing_url"])
                results["pricing"][vendor] = pricing_result
            
            # 爬新闻页
            if urls.get("news_url"):
                news_result = await forage_page(page, vendor, "news", urls["news_url"])
                results["news"][vendor] = news_result
            
            # 礼貌间隔
            await asyncio.sleep(1)
        
        await browser.close()
    
    # 保存
    output_path = OUTPUT_DIR / f"forage_{date.today().isoformat()}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 摘要
    print(f"\n{'=' * 60}")
    print(f"🐝 采蜜完成！")
    
    total_models = 0
    for vendor, data in results["pricing"].items():
        if data["status"] == "ok":
            n = len(data["models"])
            total_models += n
            if n > 0:
                print(f"  💰 {vendor}: {n} 个模型定价")
                for m in data["models"][:5]:
                    inp = m.get("input_price_per_million", "?")
                    outp = m.get("output_price_per_million", "?")
                    print(f"     {m['model']}: ¥{inp}/{outp} 每百万token")
                if n > 5:
                    print(f"     ... 还有 {n-5} 个")
            else:
                print(f"  ⚠️  {vendor}: 页面获取成功但未解析到定价")
        else:
            print(f"  ❌ {vendor}: {data.get('error', '未知')[:80]}")
    
    news_ok = sum(1 for v in results["news"].values() if v["status"] == "ok")
    print(f"\n  新闻: {news_ok}/{len(results['news'])} 成功")
    print(f"  定价: {total_models} 个模型解析成功")
    print(f"  保存: {output_path}")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_forage())
