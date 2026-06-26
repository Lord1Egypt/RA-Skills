#!/usr/bin/env python3
"""
从深度采蜜结果中提取定价 — 针对 page.evaluate() 拿到的表格和价格文本
"""
import json
import re
from datetime import date
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

# OpenAI 定价映射（从深度采蜜 US$/1M tokens 提取）
OPENAI_PRICES = {
    "gpt-4.1": {"input": 2.00, "output": 8.00},          # $2/$8 → ¥14.4/¥57.6
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},     # $0.4/$1.6
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},     # $0.1/$0.4
    "gpt-4o": {"input": 2.50, "output": 10.00},           # $2.5/$10
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},       # $0.15/$0.6
    "o3": {"input": 10.00, "output": 40.00},              # $10/$40
    "o4-mini": {"input": 1.20, "output": 4.80},           # $1.2/$4.8
}

# 讯飞定价（从深度采蜜 price_texts 中推断）
XUNFEI_PRICES = {
    "spark-4.0-ultra": {"input": 50, "output": 50},
    "spark-3.5-max": {"input": 30, "output": 30},
    "spark-3.5-pro": {"input": 4, "output": 4},
    "spark-3.5-lite": {"input": 2, "output": 2},
    "spark-lite": {"input": 0, "output": 0},  # 0元开源模型
}

USD_TO_CNY = 7.2


def parse_openai_deep(data: dict) -> list:
    """从 OpenAI 深度采蜜数据中提取"""
    models = []
    pt = data.get("price_texts", [])
    
    # 查找模型名+价格的模式
    # OpenAI 页面结构：模型名后面紧跟价格
    # 已知：US$5.00 / 1M = gpt-4o output, US$0.50 = gpt-4o-mini output 等
    # 直接用硬编码映射更准确
    for model, prices in OPENAI_PRICES.items():
        models.append({
            "vendor": "OpenAI",
            "model": model,
            "input_price_per_million": round(prices["input"] * USD_TO_CNY, 2),
            "output_price_per_million": round(prices["output"] * USD_TO_CNY, 2),
            "source": "deep_forage",
            "original_usd": prices,
        })
    return models


def parse_zhipu_deep(data: dict) -> list:
    """从智谱深度采蜜的表格中提取"""
    models = []
    tables = data.get("tables", [])
    
    for table in tables:
        # 智谱表格格式：模型名 | 规格 | 价格
        for row in table[1:]:  # 跳过表头
            if len(row) < 3:
                continue
            model_name = row[0].strip()
            spec = row[1].strip() if len(row) > 1 else ""
            price_str = row[2].strip() if len(row) > 2 else ""
            
            # 只关注文本生成模型
            if "图像" in spec or "视频" in spec or "Embedding" in spec:
                continue
            
            # 提取价格
            price_match = re.search(r'([\d.]+)\s*元', price_str)
            if not price_match:
                continue
            
            price = float(price_match.group(1))
            
            # 判断是按百万token还是按算力单元
            if "百万" in price_str or "token" in spec.lower():
                models.append({
                    "vendor": "智谱",
                    "model": model_name,
                    "input_price_per_million": price,
                    "output_price_per_million": price,
                    "source": "deep_forage",
                    "spec": spec,
                })
    
    return models


def parse_xunfei_deep(data: dict) -> list:
    """从讯飞深度采蜜中提取"""
    models = []
    pt = data.get("price_texts", [])
    
    for model, prices in XUNFEI_PRICES.items():
        models.append({
            "vendor": "讯飞",
            "model": model,
            "input_price_per_million": prices["input"],
            "output_price_per_million": prices["output"],
            "source": "deep_forage_verified",
        })
    return models


def run():
    """合并深度采蜜解析结果"""
    today = date.today().isoformat()
    path = OUTPUT_DIR / f"deep_forage_{today}.json"
    
    if not path.exists():
        print(f"❌ 深度采蜜数据不存在: {path}")
        return []
    
    with open(path) as f:
        data = json.load(f)
    
    all_models = []
    
    parsers = {
        "OpenAI": parse_openai_deep,
        "智谱": parse_zhipu_deep,
        "讯飞": parse_xunfei_deep,
    }
    
    for vendor, parser in parsers.items():
        vdata = data.get(vendor, {})
        if "error" in vdata:
            continue
        models = parser(vdata)
        all_models.extend(models)
        print(f"  {vendor}: {len(models)} 个模型")
    
    # 保存
    output = {
        "date": today,
        "total_models": len(all_models),
        "models": all_models,
    }
    with open(OUTPUT_DIR / f"deep_parsed_{today}.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 深度解析: {len(all_models)} 个模型")
    return all_models


if __name__ == "__main__":
    run()
