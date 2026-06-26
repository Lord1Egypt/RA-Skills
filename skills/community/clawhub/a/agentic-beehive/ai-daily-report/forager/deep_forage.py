#!/usr/bin/env python3
"""
计费页深度解析 — 用 page.evaluate() 提取 JS 动态渲染的定价表格
"""
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).parent.parent / "output"


# JS 代码：提取页面中所有表格数据
EXTRACT_TABLES_JS = """
() => {
    const tables = [];
    document.querySelectorAll('table').forEach((table, ti) => {
        const rows = [];
        table.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('th, td').forEach(cell => {
                cells.push(cell.textContent.trim().replace(/\\s+/g, ' '));
            });
            if (cells.length > 0) rows.push(cells);
        });
        if (rows.length > 1) tables.push(rows);
    });
    return tables;
}
"""

# JS 代码：提取所有可能是价格信息的文本节点
EXTRACT_PRICE_TEXT_JS = """
() => {
    const results = [];
    // 搜索包含价格关键词的文本
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
        const text = walker.currentNode.textContent.trim();
        if (text.length > 5 && text.length < 200 && 
            (text.match(/[¥$￥]\\s*[\\d.]+/) || text.match(/[\\d.]+\\s*元/) || 
             text.match(/per\\s*1M/i) || text.match(/百万\\s*token/) || 
             text.match(/万\\s*token/))) {
            results.push(text);
        }
    }
    return results.slice(0, 100);
}
"""


async def deep_forage():
    """深度采蜜：用 evaluate 提取动态表格"""
    print(f"🕷️  计费页深度解析 — {date.today()}")
    print("=" * 60)
    
    targets = {
        "DeepSeek": "https://api-docs.deepseek.com/zh-cn/quick_start/pricing",
        "智谱": "https://open.bigmodel.cn/pricing",
        "阿里": "https://help.aliyun.com/zh/model-studio/getting-started/models",
        "字节": "https://www.volcengine.com/docs/82379/1099470",
        "百度": "https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Dffk0dtj7",
        "月之暗面": "https://platform.moonshot.cn/docs/pricing",
        "MiniMax": "https://platform.minimaxi.com/document/Price",
        "阶跃星辰": "https://platform.stepfun.com/pricing",
        "讯飞": "https://xinghuo.xfyun.cn/sparkapi",
        "商汤": "https://platform.sensenova.cn/pricing",
        "Anthropic": "https://www.anthropic.com/pricing",
        "OpenAI": "https://openai.com/api/pricing/",
    }
    
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
            locale="zh-CN",
        )
        page = await context.new_page()
        
        for vendor, url in targets.items():
            print(f"\n📦 {vendor}")
            try:
                await page.goto(url, timeout=25000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                
                # 滚动触发懒加载
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                await page.wait_for_timeout(1500)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(1500)
                await page.evaluate("window.scrollTo(0, 0)")
                await page.wait_for_timeout(1000)
                
                # 提取表格
                tables = await page.evaluate(EXTRACT_TABLES_JS)
                
                # 提取价格相关文本
                price_texts = await page.evaluate(EXTRACT_PRICE_TEXT_JS)
                
                # 也拿 inner_text 作为后备
                inner_text = await page.inner_text("body")
                
                vendor_result = {
                    "vendor": vendor,
                    "url": url,
                    "tables": tables,
                    "price_texts": price_texts[:50],
                    "inner_text_preview": inner_text[:2000],
                    "table_count": len(tables),
                    "price_text_count": len(price_texts),
                }
                
                results[vendor] = vendor_result
                print(f"  ✅ 表格 {len(tables)} 个, 价格文本 {len(price_texts)} 条")
                
                # 打印关键发现
                for i, table in enumerate(tables):
                    # 找包含价格的表格
                    flat = " ".join(" ".join(row) for row in table)
                    if any(kw in flat for kw in ["元", "¥", "$", "价格", "price", "token"]):
                        print(f"  📊 表格 {i+1}: {len(table)} 行 x {len(table[0]) if table else 0} 列")
                        for row in table[:6]:
                            print(f"     {' | '.join(row[:8])}")
                        if len(table) > 6:
                            print(f"     ... 还有 {len(table)-6} 行")
                
            except Exception as e:
                results[vendor] = {"vendor": vendor, "url": url, "error": str(e)[:200]}
                print(f"  ❌ {str(e)[:100]}")
            
            await asyncio.sleep(0.5)
        
        await browser.close()
    
    # 保存
    output_path = OUTPUT_DIR / f"deep_forage_{date.today().isoformat()}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 深度解析完成: {output_path}")
    return results


def parse_deep_forage():
    """从深度采蜜结果中提取定价"""
    today = date.today().isoformat()
    path = OUTPUT_DIR / f"deep_forage_{today}.json"
    
    if not path.exists():
        print("❌ 深度采蜜数据不存在")
        return []
    
    with open(path) as f:
        data = json.load(f)
    
    all_models = []
    
    for vendor, vdata in data.items():
        if "error" in vdata:
            continue
        
        tables = vdata.get("tables", [])
        price_texts = vdata.get("price_texts", [])
        
        # 从表格中提取
        for table in tables:
            flat = " ".join(" ".join(row) for row in table)
            if not any(kw in flat for kw in ["元", "¥", "$", "price", "token", "万"]):
                continue
            
            # 尝试识别表格结构
            if len(table) < 2:
                continue
            
            header = table[0]
            
            # 找模型名列和价格列
            for row in table[1:]:
                if len(row) < 2:
                    continue
                
                # 每行可能是一个模型
                row_text = " ".join(row)
                
                # 尝试提取价格
                prices = re.findall(r'[¥￥]?\s*([\d.]+)\s*(?:元|/百万|/1M|per 1M)', row_text)
                if not prices:
                    prices = re.findall(r'([\d.]+)\s*元', row_text)
                
                if prices and len(row[0]) > 2:
                    model_name = row[0].strip()
                    # 过滤噪声
                    if any(kw in model_name for kw in ["模型", "价格", "说明", "输入", "输出"]):
                        continue
                    
                    entry = {
                        "vendor": vendor,
                        "model": model_name,
                        "source": "deep_forage",
                        "raw_row": row[:6],
                    }
                    
                    if len(prices) >= 2:
                        entry["input_price_per_million"] = float(prices[0])
                        entry["output_price_per_million"] = float(prices[1])
                    elif len(prices) == 1:
                        entry["input_price_per_million"] = float(prices[0])
                        entry["output_price_per_million"] = float(prices[0])
                    
                    all_models.append(entry)
    
    # 去重
    seen = set()
    unique = []
    for m in all_models:
        key = f"{m['vendor']}:{m['model']}"
        if key not in seen:
            seen.add(key)
            unique.append(m)
    
    return unique


if __name__ == "__main__":
    asyncio.run(deep_forage())
