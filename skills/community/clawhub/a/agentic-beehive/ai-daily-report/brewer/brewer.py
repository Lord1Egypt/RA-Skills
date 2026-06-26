#!/usr/bin/env python3
"""
酿蜜引擎 — 性价比计算 + 综合排名 + 日报生成

蜂巢酿蜜：采回来的花蜜是原始数据，酿蜜是加工决策。
- 性价比排行 = 能力分 / 归一化价格
- 综合排名 = 多维度加权
- 日报 = 结构化输出
"""

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"


# ==================== 性价比计算 ====================

# 手动维护的模型能力参考分（MMLU/C-Eval 综合近似）
# 来源：各官方公布 + 社区评测，会随版本更新
CAPABILITY_SCORES = {
    # 百度
    "ernie-5.1": 0.87, "ernie-4.0": 0.82, "ernie-4.0-8k": 0.82, "ernie-4.0-turbo-8k": 0.80,
    "ernie-3.5": 0.72, "ernie-3.5-8k": 0.72,
    "ernie-speed": 0.65, "ernie-speed-8k": 0.65,
    "ernie-lite": 0.55, "ernie-lite-8k": 0.55,
    "ernie-tiny": 0.45,
    # 阿里
    "qwen-max": 0.84, "qwen-max-latest": 0.85, "qwen-plus": 0.76, "qwen-plus-latest": 0.77,
    "qwen-turbo": 0.68, "qwen-turbo-latest": 0.69, "qwen-long": 0.70,
    "qwen-vl-max": 0.78, "qwen-vl-plus": 0.73,
    # 字节
    "doubao-pro": 0.74, "doubao-lite": 0.60, "doubao-128k": 0.72,
    "doubao-pro-32k": 0.74, "doubao-pro-128k": 0.74,
    "doubao-pro-256k": 0.73, "doubao-lite-32k": 0.60, "doubao-lite-128k": 0.60,
    "doubao-1.5-pro-256k": 0.78, "doubao-1.5-pro-32k": 0.77,
    # 智谱
    "glm-4": 0.83, "glm-4-plus": 0.85, "glm-4-flash": 0.68,
    "glm-4-air": 0.72, "glm-4-long": 0.70,
    # DeepSeek
    "deepseek-chat": 0.80, "deepseek-reasoner": 0.88,
    "deepseek-v3": 0.83, "deepseek-r1": 0.90,
    "deepseek-v4-flash": 0.84, "deepseek-v4-pro": 0.90,
    # 月之暗面
    "moonshot-v1-8k": 0.73, "moonshot-v1-32k": 0.73, "moonshot-v1-128k": 0.73,
    # MiniMax
    "minimax-m1": 0.78, "minimax-m2": 0.82, "minimax-m2.7": 0.83,
    "abab-6.5": 0.75, "abab-6.5s": 0.68, "hailuo": 0.76,
    "MiniMax-M2.7": 0.83,
    # 零一万物
    "yi-large": 0.80, "yi-medium": 0.70, "yi-spark": 0.60,
    "yi-vision": 0.72,
    # 阶跃星辰
    "step-2": 0.79, "step-2-16k": 0.79, "step-2-1m": 0.79,
    "step-1-8k": 0.70, "step-1v-8k": 0.72,
    # 讯飞
    "spark-4.0-ultra": 0.80, "spark-3.5-max": 0.74,
    "spark-3.5-pro": 0.68, "spark-3.5-lite": 0.55,
    # 华为
    "pangu-large": 0.78, "pangu-medium": 0.68,
    # 昆仑
    "skywork-13b": 0.62, "skywork-max": 0.72,
    # 蚂蚁百灵
    "ring-2.6-1t": 0.85, "ring-2.6": 0.80,
    # 商汤
    "日日新": 0.78, "sensenova-5o": 0.78, "sensenova-5": 0.75,
    # Google
    "gemini-2.5-pro": 0.90, "gemini-2.5-flash": 0.82,
    "gemini-2.0-flash": 0.78, "gemini-1.5-pro": 0.84,
    # Anthropic
    "claude-4-opus": 0.92, "claude-4-sonnet": 0.88,
    "claude-3.5-sonnet": 0.85, "claude-3.5-haiku": 0.75,
    # OpenAI
    "gpt-4.1": 0.88, "gpt-4.1-mini": 0.80, "gpt-4.1-nano": 0.72,
    "o3": 0.91, "o4-mini": 0.82, "gpt-4o": 0.86, "gpt-4o-mini": 0.76,
}

# 手动维护的模型定价参考（元/百万token，输入价）
# 这些是 fallback 值，优先用爬取到的实际价格
PRICING_REFERENCE = {
    # 百度（元/百万token）
    "ernie-4.0": {"input": 120, "output": 120},
    "ernie-4.0-8k": {"input": 120, "output": 120},
    "ernie-3.5": {"input": 12, "output": 12},
    "ernie-speed": {"input": 4, "output": 8},
    "ernie-lite": {"input": 2, "output": 6},
    # 阿里
    "qwen-max": {"input": 40, "output": 120},
    "qwen-plus": {"input": 4, "output": 12},
    "qwen-turbo": {"input": 2, "output": 6},
    "qwen-long": {"input": 4, "output": 4},
    # 字节
    "doubao-pro": {"input": 4, "output": 16},
    "doubao-pro-32k": {"input": 4, "output": 16},
    "doubao-pro-128k": {"input": 5, "output": 16},
    "doubao-lite": {"input": 0.3, "output": 0.6},
    # 智谱
    "glm-4": {"input": 100, "output": 100},
    "glm-4-plus": {"input": 50, "output": 50},
    "glm-4-flash": {"input": 0.1, "output": 0.1},
    "glm-4-air": {"input": 1, "output": 1},
    "glm-4-long": {"input": 1, "output": 1},
    # 百度（文心5.1新定价）
    "ernie-5.1": {"input": 24, "output": 48},
    "文心5.1": {"input": 24, "output": 48},
    # DeepSeek
    "deepseek-chat": {"input": 1, "output": 2},
    "deepseek-reasoner": {"input": 4, "output": 16},
    "deepseek-v4-flash": {"input": 0.7, "output": 2.8},
    # 月之暗面
    "moonshot-v1-8k": {"input": 12, "output": 12},
    "moonshot-v1-32k": {"input": 24, "output": 24},
    "moonshot-v1-128k": {"input": 60, "output": 60},
    # MiniMax
    "minimax-m1": {"input": 2, "output": 8},
    "minimax-m2": {"input": 4, "output": 16},
    "abab-6.5": {"input": 10, "output": 10},
    "abab-6.5s": {"input": 2, "output": 2},
    # 零一万物
    "yi-large": {"input": 20, "output": 20},
    "yi-medium": {"input": 2.5, "output": 2.5},
    "yi-spark": {"input": 0.6, "output": 0.6},
    # 阶跃星辰
    "step-2": {"input": 30, "output": 30},
    "step-1-8k": {"input": 5, "output": 5},
    # 讯飞
    "spark-4.0-ultra": {"input": 50, "output": 50},
    "spark-3.5-max": {"input": 30, "output": 30},
    "spark-3.5-pro": {"input": 4, "output": 4},
    "spark-3.5-lite": {"input": 0.5, "output": 0.5},
    # 蚂蚁百灵（估计定价，待爬取确认）
    "ring-2.6-1t": {"input": 16, "output": 64},
    "ring-2.6": {"input": 8, "output": 32},
    # 商汤
    "sensenova-5o": {"input": 15, "output": 15},
    "sensenova-5": {"input": 8, "output": 8},
    # Google (USD → CNY ≈ 7.2)
    "gemini-2.5-pro": {"input": 9.36, "output": 37.44},  # $1.3/$5.2
    "gemini-2.5-flash": {"input": 1.08, "output": 4.32},  # $0.15/$0.6
    # Anthropic (USD → CNY)
    "claude-4-sonnet": {"input": 21.6, "output": 108},  # $3/$15
    "claude-3.5-sonnet": {"input": 21.6, "output": 108},
    "claude-3.5-haiku": {"input": 6.48, "output": 32.4},  # $0.9/$4.5
    # OpenAI (USD → CNY)
    "gpt-4.1": {"input": 14.4, "output": 57.6},  # $2/$8
    "gpt-4.1-mini": {"input": 2.88, "output": 11.52},  # $0.4/$1.6
    "gpt-4.1-nano": {"input": 0.72, "output": 2.88},  # $0.1/$0.4
    "gpt-4o": {"input": 17.28, "output": 69.12},  # $2.4/$9.6
    "gpt-4o-mini": {"input": 1.08, "output": 4.32},  # $0.15/$0.6
    "o3": {"input": 72, "output": 288},  # $10/$40
    "o4-mini": {"input": 8.64, "output": 34.56},  # $1.2/$4.8
}


import math

def calculate_cost_effectiveness(
    model_name: str,
    capability: float,
    input_price: float,
    output_price: float,
    input_weight: float = 0.7,
    output_weight: float = 0.3,
) -> dict:
    """
    计算单个模型的性价比分。
    
    核心原则：便宜但不能用的模型不是性价比，是垃圾。
    
    公式：ce = capability² × log10(1000 / weighted_price)
    
    用 capability² 做乘数：
    - 能力 0.68 → 0.68² = 0.46 （弱模型被压制）
    - 能力 0.84 → 0.84² = 0.71 （强模型不被惩罚）
    - 能力 0.90 → 0.90² = 0.81 （顶级模型优势放大）
    
    对数缩放避免超低价爆炸：
    - ¥0.1/M → log10(10000) = 4.0
    - ¥1/M   → log10(1000)  = 3.0
    - ¥10/M  → log10(100)   = 2.0
    - ¥100/M → log10(10)    = 1.0
    """
    weighted_price = input_price * input_weight + output_price * output_weight
    
    if weighted_price <= 0:
        return {"model": model_name, "ce_score": 0, "error": "zero_price"}
    
    # 能力² 做乘数——弱模型即使免费也不会排第一
    ce_raw = (capability ** 2) * math.log10(max(1000 / weighted_price, 0.1))
    
    return {
        "model": model_name,
        "capability": round(capability, 3),
        "input_price": input_price,
        "output_price": output_price,
        "weighted_price": round(weighted_price, 2),
        "ce_raw": round(ce_raw, 3),
    }


# ==================== 综合排名 ====================

def calculate_comprehensive_ranking(
    models: list[dict],
    weights: Optional[dict] = None,
    min_capability: float = 0.70,
) -> list[dict]:
    """
    计算综合排名。
    
    综合分 = w1 * 能力分(归一化) + w2 * 性价比分(归一化) + w3 * 生态分 + w4 * 势头分
    
    min_capability: 综合排名的最低能力门槛（默认0.70）
    能力低于此值的模型只出现在性价比排行，不进综合排名。
    理由：能力不足的模型再便宜也不该排进 Top 10。
    """
    if weights is None:
        weights = {
            "capability": 0.35,
            "cost_effectiveness": 0.30,
            "ecosystem": 0.20,
            "momentum": 0.15,
        }
    
    if not models:
        return []
    
    # 能力门槛过滤——弱模型不进综合排名
    qualified = [m for m in models if m.get("capability", 0) >= min_capability]
    if not qualified:
        qualified = models  # 兜底：全都不够门槛则全部参与
    
    # 归一化
    max_cap = max(m.get("capability", 0) for m in qualified) or 1
    max_ce = max(m.get("ce_raw", 0) for m in qualified) or 1
    
    ranked = []
    for m in qualified:
        cap_norm = m.get("capability", 0) / max_cap
        ce_norm = m.get("ce_raw", 0) / max_ce
        eco = m.get("ecosystem_score", 0.5)  # 默认 0.5
        mom = m.get("momentum_score", 0.5)    # 默认 0.5
        
        composite = (
            weights["capability"] * cap_norm
            + weights["cost_effectiveness"] * ce_norm
            + weights["ecosystem"] * eco
            + weights["momentum"] * mom
        )
        
        ranked.append({
            **m,
            "cap_norm": round(cap_norm, 3),
            "ce_norm": round(ce_norm, 3),
            "ecosystem_score": round(eco, 3),
            "momentum_score": round(mom, 3),
            "composite_score": round(composite, 3),
        })
    
    # 排序
    ranked.sort(key=lambda x: x["composite_score"], reverse=True)
    
    # 加排名
    for i, r in enumerate(ranked, 1):
        r["rank"] = i
    
    return ranked


# ==================== 日报生成 ====================

def generate_daily_report(
    garden_results: dict,
    forage_results: dict,
    ranking_results: list[dict],
    vendor_registry: dict,
    taste_result: dict = None,
) -> str:
    """生成 Markdown 日报"""
    
    today = date.today().isoformat()
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.today().weekday()]
    
    lines = []
    lines.append(f"# 🐝 AI 市场日报 — {today} {weekday_cn}")
    lines.append("")
    lines.append("> 蜂巢自动感知·采蜜·酿蜜 | 动态厂商清单 | 实时定价计算")
    lines.append("")
    
    # ---- Section 1: 花园态势 ----
    lines.append("## 🌸 花园态势")
    lines.append("")
    
    vendors = vendor_registry.get("vendors", {})
    sorted_vendors = sorted(vendors.values(), key=lambda x: x.get("bloom_score", 0), reverse=True)
    
    status_emoji = {"盛开": "🌺", "开花": "🌸", "含苞": "🌷", "凋谢": "🥀", "new": "🌱", "seed": "🌱", "discovered": "🌿"}
    
    for v in sorted_vendors:
        score = v.get("bloom_score", 0)
        status = "凋谢"
        if score >= 0.7: status = "盛开"
        elif score >= 0.4: status = "开花"
        elif score >= 0.2: status = "含苞"
        
        emoji = status_emoji.get(status, "❓")
        cat = v.get("category", "")
        cat_tag = {"tier1": "🏆", "tier2": "🏅", "international": "🌍", "seed": "🌱", "discovered": "🌿"}.get(cat, "")
        
        lines.append(f"- {emoji} **{v['name']}** — 花期 {status} (bloom: {score:.2f}) {cat_tag}")
    
    # 状态变化
    status_changes = garden_results.get("status_changes", [])
    if status_changes:
        lines.append("")
        lines.append("**📈 花期变化：**")
        for sc in status_changes:
            lines.append(f"- {sc['name']}: {sc['from']} → {sc['to']}")
    
    lines.append("")
    
    # ---- Section 2: 厂商动态 ----
    lines.append("## 📰 厂商动态")
    lines.append("")
    
    news = forage_results.get("news", {})
    if news:
        for vendor_name, news_data in news.items():
            status = news_data.get("status", "")
            if not status.startswith("ok"):
                lines.append(f"### {vendor_name}")
                lines.append(f"⚠️ 采集失败: {news_data.get('error', '未知错误')}")
                lines.append("")
                continue
            
            lines.append(f"### {vendor_name}")
            headlines = news_data.get("headlines", [])
            if headlines:
                for h in headlines[:5]:
                    title = h.get("title", "").strip()
                    url = h.get("url", "")
                    if title:
                        if url and url.startswith("http"):
                            lines.append(f"- [{title}]({url})")
                        else:
                            lines.append(f"- {title}")
            else:
                lines.append("- _(无显著新闻)_")
            lines.append("")
    else:
        lines.append("_(今日未采集到新闻数据)_")
        lines.append("")
    
    # ---- Section 3: 性价比排行 ----
    lines.append("## 💰 大模型性价比排行")
    lines.append("")
    lines.append("> 性价比 = 能力分 / 加权价格 | 价格 = 输入×0.7 + 输出×0.3 (元/百万token)")
    lines.append("")
    
    if ranking_results:
        lines.append("| 排名 | 模型 | 厂商 | 能力分 | 性价比 | 输入价 | 输出价 | 综合分 |")
        lines.append("|:----:|------|------|:------:|:------:|:------:|:------:|:------:|")
        for r in ranking_results[:20]:
            lines.append(
                f"| {r.get('rank', '-')} "
                f"| {r.get('model', '-')} "
                f"| {r.get('vendor', '-')} "
                f"| {r.get('capability', 0):.2f} "
                f"| {r.get('ce_raw', 0):.2f} "
                f"| ¥{r.get('input_price', 0):.2f} "
                f"| ¥{r.get('output_price', 0):.2f} "
                f"| {r.get('composite_score', 0):.3f} |"
            )
    else:
        lines.append("_(暂无排行数据)_")
    
    lines.append("")
    
    # ---- Section 4: 综合排名 Top 10 ----
    lines.append("## 🏆 头部大模型综合排名 Top 10")
    lines.append("")
    lines.append("> 综合 = 0.35×能力 + 0.30×性价比 + 0.20×生态 + 0.15×势头 | 能力门槛 ≥ 0.70")
    lines.append("")
    
    if ranking_results:
        for i, r in enumerate(ranking_results[:10], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"**{i}.**")
            lines.append(
                f"{medal} **{r.get('model', '-')}** ({r.get('vendor', '-')})"
                f" — 综合 {r.get('composite_score', 0):.3f}"
                f" | 能力 {r.get('cap_norm', 0):.2f}"
                f" | 性价比 {r.get('ce_norm', 0):.2f}"
            )
    
    lines.append("")
    
    if taste_result is None:
        taste_result = {"rules_triggered": [], "fixes_applied": []}
    
    # ---- 品蜜报告 ----
    if taste_result.get("rules_triggered"):
        lines.append("## 🍯 品蜜报告")
        lines.append("")
        lines.append("> 品蜜 = 酿蜜后自检。蜂巢的第二个胃。")
        lines.append("")
        for t in taste_result["rules_triggered"]:
            lines.append(f"- ⚠️ **{t['name']}** — {t['diagnose']['reason_code']}")
            lines.append(f"  根因: {t['diagnose']['explanation']}")
            lines.append(f"  修正: {t['fix']['description']}")
        lines.append("")
    
    # ---- Footer ----
    lines.append("---")
    lines.append(f"*蜂巢 AI 日报 v1.2 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append(f"*厂商清单: 动态感知({len(vendors)}家) | 定价: 实时计算 | 排名: 可演化权重*")
    lines.append(f"*品蜜: {len(taste_result.get('rules_triggered', []))} 条触发 | {len(taste_result.get('fixes_applied', []))} 项修正*")
    
    return "\n".join(lines)


def brew(
    garden_path: Optional[Path] = None,
    forage_path: Optional[Path] = None,
) -> str:
    """
    酿蜜主入口：读取花园扫描+采蜜结果，生成日报。
    """
    today = date.today().isoformat()
    
    # 加载花园扫描结果
    if garden_path is None:
        garden_path = OUTPUT_DIR / f"garden_{today}.json"
    if forage_path is None:
        forage_path = OUTPUT_DIR / f"forage_{today}.json"
    
    garden_results = {}
    if garden_path.exists():
        with open(garden_path) as f:
            garden_results = json.load(f)
    
    forage_results = {}
    if forage_path.exists():
        with open(forage_path) as f:
            forage_results = json.load(f)
    
    # 加载厂商注册表
    registry_path = OUTPUT_DIR / "vendor_registry.json"
    vendor_registry = {}
    if registry_path.exists():
        with open(registry_path) as f:
            vendor_registry = json.load(f)
    
    # 构建模型列表
    models = []
    
    # 优先用采蜜到的定价数据
    pricing = forage_results.get("pricing", {})
    for vendor_name, price_data in pricing.items():
        if price_data.get("status", "").startswith("ok"):
            for m in price_data.get("models", []):
                model_name = m.get("model", "")
                # 匹配能力分
                cap = CAPABILITY_SCORES.get(model_name.lower(), 0.5)
                inp = m.get("input_price_per_million", m.get("price_per_million", 0))
                outp = m.get("output_price_per_million", m.get("price_per_million", 0))
                
                ce = calculate_cost_effectiveness(model_name, cap, inp, outp)
                ce["vendor"] = vendor_name
                models.append(ce)
    
    # 加载定向解析数据（更精准）
    parsed_path = OUTPUT_DIR / f"parsed_pricing_{date.today().isoformat()}.json"
    if parsed_path.exists():
        with open(parsed_path) as f:
            parsed_data = json.load(f)
        for m in parsed_data.get("models", []):
            model_name = m.get("model", "")
            if not any(existing.get("model", "") == model_name for existing in models):
                cap = CAPABILITY_SCORES.get(model_name.lower(), 0.5)
                inp = m.get("input_price_per_million", 0)
                outp = m.get("output_price_per_million", 0)
                ce = calculate_cost_effectiveness(model_name, cap, inp, outp)
                ce["vendor"] = m.get("vendor", _infer_vendor(model_name))
                ce["source"] = m.get("source", "parsed")
                models.append(ce)
    
    # 加载深度采蜜解析数据（最精准）
    deep_path = OUTPUT_DIR / f"deep_parsed_{date.today().isoformat()}.json"
    if deep_path.exists():
        with open(deep_path) as f:
            deep_data = json.load(f)
        for m in deep_data.get("models", []):
            model_name = m.get("model", "")
            if not any(existing.get("model", "") == model_name for existing in models):
                cap = CAPABILITY_SCORES.get(model_name.lower(), 0.5)
                inp = m.get("input_price_per_million", 0)
                outp = m.get("output_price_per_million", 0)
                ce = calculate_cost_effectiveness(model_name, cap, inp, outp)
                ce["vendor"] = m.get("vendor", _infer_vendor(model_name))
                ce["source"] = "deep_forage"
                models.append(ce)
    
    # 补充参考定价数据（以上都没覆盖的）
    seen_models = set()
    for model_name, pricing_ref in PRICING_REFERENCE.items():
        # 跳过别名重复（如 文心5.1 和 ernie-5.1 是同一个）
        canonical = model_name.lower()
        # 中文别名跳过，保留英文代号
        if any(ord(c) > 0x4e00 for c in model_name):
            continue
        if canonical in seen_models:
            continue
        seen_models.add(canonical)
        
        if not any(m.get("model", "").lower() == model_name for m in models):
            cap = CAPABILITY_SCORES.get(model_name, 0.5)
            # 从模型名推断厂商
            vendor = _infer_vendor(model_name)
            ce = calculate_cost_effectiveness(
                model_name, cap,
                pricing_ref["input"], pricing_ref["output"]
            )
            ce["vendor"] = vendor
            ce["source"] = "reference"
            models.append(ce)
    
    # 综合排名
    ranking = calculate_comprehensive_ranking(models)
    
    # 品蜜自检（防御性架构：酿完蜜必须自检）
    from brewer.taste import taste
    taste_result = taste(ranking)
    if taste_result["revised"]:
        ranking = taste_result["revised_rankings"]
        print(f"  🍯 品蜜修正: {len(taste_result['fixes_applied'])} 项")
    else:
        print(f"  ✅ 品蜜通过")
    
    # 生成日报
    report = generate_daily_report(garden_results, forage_results, ranking, vendor_registry, taste_result)
    
    # 保存
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIR / f"daily_report_{today}.md"
    with open(report_path, "w") as f:
        f.write(report)
    
    # 同时保存排名数据
    ranking_path = OUTPUT_DIR / f"ranking_{today}.json"
    with open(ranking_path, "w") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 日报生成: {report_path}")
    print(f"✅ 排名数据: {ranking_path}")
    
    return report


def _infer_vendor(model_name: str) -> str:
    """从模型名推断厂商"""
    vendor_hints = {
        "ernie": "百度", "文心": "百度",
        "qwen": "阿里", "通义": "阿里",
        "doubao": "字节", "豆包": "字节",
        "glm": "智谱", "chatglm": "智谱", "智谱": "智谱",
        "deepseek": "DeepSeek", "深度求索": "DeepSeek",
        "moonshot": "月之暗面", "kimi": "月之暗面",
        "minimax": "MiniMax", "abab": "MiniMax", "hailuo": "MiniMax", "海螺": "MiniMax",
        "yi-": "零一万物", "yi ": "零一万物",
        "step": "阶跃星辰", "跃问": "阶跃星辰",
        "spark": "讯飞", "星火": "讯飞",
        "pangu": "华为", "盘古": "华为",
        "skywork": "昆仑万维", "天工": "昆仑万维",
        "ring": "蚂蚁", "百灵": "蚂蚁", "蚂蚁": "蚂蚁",
        "日日新": "商汤", "sensenova": "商汤", "商汤": "商汤",
        "日日新": "商汤", "sensenova": "商汤",
        "gemini": "Google", "claude": "Anthropic", 
        "gpt": "OpenAI", "o3": "OpenAI", "o4": "OpenAI",
    }
    name_lower = model_name.lower()
    for prefix, vendor in vendor_hints.items():
        if prefix.lower() in name_lower:
            return vendor
    return "未知"


if __name__ == "__main__":
    report = brew()
    print("\n" + "=" * 60)
    print(report[:2000])
    if len(report) > 2000:
        print(f"\n... (共 {len(report)} 字符)")
