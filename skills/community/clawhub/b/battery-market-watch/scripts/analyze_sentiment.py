#!/usr/bin/env python3
"""
分析情感和影响，生成延展分析 - 优化版
增加本地 LLM 调用生成 200 字专业解读
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import httpx


def load_config() -> Dict:
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def call_local_llm(prompt: str, max_tokens: int = 300, temperature: float = 0.7) -> str:
    """
    调用本地 LLM 模型（支持 Ollama、vLLM 等）
    """
    llm_config = {
        "base_url": "http://localhost:11434",  # Ollama 默认端口，可改为其他本地 LLM
        "model": "qwen2:7b",  # 可改为其他本地模型
        "timeout": 60
    }
    
    try:
        response = httpx.post(
            f"{llm_config['base_url']}/api/generate",
            json={
                "model": llm_config["model"],
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            timeout=llm_config["timeout"]
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        print(f"❌ LLM 调用失败: {e}，将使用模板解读")
        return None


CONFIG = load_config()


def generate_professional_insight(news: Dict) -> str:
    """
    使用本地 LLM 生成 200 字左右的专业解读
    内容：新闻简介（50字）+ 政策/产业解读（100字）+ 投资影响（50字）
    """
    title = news.get("title_zh") or news.get("title", "")
    summary = news.get("summary_zh") or news.get("summary_original", "")
    country = news.get("country", "")
    news_type = news.get("type", "行业动态")
    sentiment = news.get("sentiment", "中性")
    
    prompt = f"""你是国际电池产业研究员。基于以下新闻，生成一份 200 字左右的专业解读：

【新闻标题】{title}
【发生国家】{country}
【新闻类型】{news_type}
【新闻摘要】{summary}

请按以下结构组织（段落连贯，不含序号）：

第一部分（50字）：用简洁专业语言复述新闻核心事实
第二部分（100字）：从产业政策、监管导向、竞争格局等角度分析这条新闻的深层含义
第三部分（50字）：对全球电池产业链、供应链、相关企业的潜在影响

要求：
- 专业术语准确，适合机构投资者阅读
- 避免重复摘要内容
- 突出政策信号和市场机制
- 包含具体数据或时间节点（如有）

输出仅含 200 字左右的解读内容，不含标题和其他文本。"""
    
    # 尝试调用 LLM
    insight = call_local_llm(prompt, max_tokens=300)
    
    if insight:
        return insight
    
    # 如果 LLM 调用失败，使用模板（原有逻辑）
    return generate_template_insight(news)


def generate_template_insight(news: Dict) -> str:
    """
    备用方案：当 LLM 不可用时，使用模板生成解读
    """
    title = news.get("title_zh") or news.get("title", "")
    country = news.get("country", "")
    news_type = news.get("type", "行业动态")
    sentiment = news.get("sentiment", "中性")
    impact = news.get("impact", "")
    summary = news.get("summary_zh") or news.get("summary_original", "")
    
    type_map = {
        "政策补贴": "政策补贴类信息通常直接刺激需求端预期和投资端决策，市场会重点关注补贴强度、覆盖范围、执行周期，以及是否形成实质订单释放。这类信息对电池产业链上游材料、中游制造和下游应用都有较强传导能力。",
        "法规": "法规类信息对产业链的影响体现在合规成本、产品设计路线和供应链准入门槛变化。通常先冲击产品认证周期和制造工艺，再向销售、盈利扩散。",
        "重大事件": "重大事件通常先冲击风险偏好，随后向监管、认证、客户采购等链条扩散，是典型的风险传导节点。安全事故尤其容易引发后续监管强化。",
        "行业动态": "行业动态类信息主要反映景气度、产能节奏、资本开支方向，是前瞻性指标。对设备、材料、电芯环节都有指导意义。"
    }
    
    p1 = f"本条新闻《{title}》发生在{country}，属于{news_type}类信息。事件本质是：{summary[:80]}。这说明该信息并非孤立，而是产业链中的一个关键节点。"
    p2 = type_map.get(news_type, "这类信息需要融入产业链框架理解。") + f"对{country}电池市场而言，这条新闻的政策信号或风险提示是：{impact}。"
    p3 = f"从投资角度看，更值得关注的是后续验证：政策是否正式落地、企业是否调整 CAPEX、客户是否改变采购节奏。这条新闻是一个前瞻信号，需要持续跟踪其在产业链上的实际传导效果。"
    
    return (p1 + p2 + p3)[:250] + "..."


def classify_news_type(title: str, content: str = "") -> str:
    """
    根据标题和内容分类新闻类型
    """
    text = (title + " " + content).lower()

    for news_type, keywords in CONFIG["news_types"].items():
        for kw in keywords:
            if kw.lower() in text:
                return news_type

    return "行业动态"


def analyze_sentiment(title: str, content: str = "") -> str:
    """
    分析新闻情感 - 基于关键词
    """
    text = (title + " " + content).lower()

    good_keywords = CONFIG["sentiment"]["good_keywords"]
    bad_keywords = CONFIG["sentiment"]["bad_keywords"]

    has_good = any(kw.lower() in text for kw in good_keywords)
    has_bad = any(kw.lower() in text for kw in bad_keywords)

    if has_bad and not has_good:
        return "利空"
    elif has_good and not has_bad:
        return "利好"
    elif has_good and has_bad:
        # 两者都有，检查哪个更明显
        good_count = sum(1 for kw in good_keywords if kw.lower() in text)
        bad_count = sum(1 for kw in bad_keywords if kw.lower() in text)
        if bad_count > good_count:
            return "利空"
        elif good_count > bad_count:
            return "利好"
        return "中性"

    return "中性"


def analyze_impact(news: Dict) -> str:
    """分析单条新闻对电池行业的影响"""
    title = news.get("title", "")
    content = news.get("content", "")
    sentiment = news.get("sentiment", "中性")
    news_type = news.get("type", "行业动态")
    text = title + " " + content

    if sentiment == "中性":
        return "无显著影响"

    # 利空分析
    if sentiment == "利空":
        if any(kw in text for kw in ["着火", "起火", "自燃", "fire", "fire incident"]):
            return "引发安全担忧，可能导致监管收紧、软包电池等争议技术需求下降"
        if any(kw in text for kw in ["爆炸", "explosion"]):
            return "重大安全事故，可能引发行业标准升级"
        if any(kw in text for kw in ["召回", "recall"]):
            return "影响消费者信心，短期销量下滑"
        if any(kw in text for kw in ["停车", "停车场"]):
            return "重大安全事故，可能引发密集场所电池使用限制"
        return "需关注后续发展"

    # 利好分析
    if sentiment == "利好":
        if any(kw in text for kw in ["补贴", "subsidy", "incentive", "tax credit"]):
            return "直接刺激相关电池产品需求"
        if any(kw in text for kw in ["PLI", "生产激励", "manufacturing incentive"]):
            return "推动本地电池制造产能建设"
        if any(kw in text for kw in ["可拆卸", "removable battery"]):
            return "2027年手机电池可拆卸要求，影响电池设计路线"
        if any(kw in text for kw in ["欧洲电池法案", "EU battery act", "battery regulation"]):
            return "欧盟电池法规趋严，再生材料要求提升"
        if any(kw in text for kw in ["IRA", "通胀削减", "inflation reduction"]):
            return "美国电动车税收抵免，影响电池供应链布局"
        if any(kw in text for kw in ["储能", "energy storage"]):
            return "储能市场扩大，带动储能电池需求"
        if any(kw in text for kw in ["扩产", "扩建造", "factory expansion"]):
            return "行业景气度提升，设备需求旺盛"
        return "需关注后续发展"

    return "无显著影响"


def generate_country_summary(news_list: List[Dict]) -> Dict:
    """生成单国新闻摘要"""
    country_news = defaultdict(list)
    for news in news_list:
        country_news[news["country"]].append(news)

    summary = {}
    for country, news in country_news.items():
        good = sum(1 for n in news if n["sentiment"] == "利好")
        bad = sum(1 for n in news if n["sentiment"] == "利空")
        neutral = sum(1 for n in news if n["sentiment"] == "中性")

        # 按类型分类统计
        policy = sum(1 for n in news if n.get("type") == "政策补贴")
        regulation = sum(1 for n in news if n.get("type") == "法规")
        incident = sum(1 for n in news if n.get("type") == "重大事件")
        industry = sum(1 for n in news if n.get("type") == "行业动态")

        summary[country] = {
            "总数": len(news),
            "利好": good,
            "利空": bad,
            "中性": neutral,
            "政策补贴": policy,
            "法规": regulation,
            "重大事件": incident,
            "行业动态": industry,
            "关键新闻": [n["title"] for n in news[:3]]
        }
    return summary


def generate_analysis(news_list: List[Dict]) -> str:
    """生成延展分析文本"""
    if not news_list:
        return "本周无相关新闻"

    # 按国家统计
    country_summary = generate_country_summary(news_list)

    # 找出重大新闻
    bad_news = [n for n in news_list if n["sentiment"] == "利空"]
    good_news = [n for n in news_list if n["sentiment"] == "利好"]

    analysis_parts = ["## 延展分析\n"]

    # 各国概览
    analysis_parts.append("### 各国新闻分布\n")
    for country in ["中国", "美国", "印度", "俄罗斯", "韩国"]:
        if country in country_summary:
            stats = country_summary[country]
            analysis_parts.append(f"- **{country}**: 利好{stats['利好']}条 / 利空{stats['利空']}条 / 中性{stats['中性']}条")

    # 重大利空分析
    if bad_news:
        analysis_parts.append("\n### 利空预警\n")
        for news in bad_news[:5]:
            impact = analyze_impact(news)
            analysis_parts.append(f"- {news['title']} -> {impact}")

    # 利好分析
    if good_news:
        analysis_parts.append("\n### 利好机遇\n")
        for news in good_news[:5]:
            impact = analyze_impact(news)
            analysis_parts.append(f"- {news['title']} -> {impact}")

    # 趋势判断
    total = len(news_list)
    if total > 0:
        bad_ratio = len(bad_news) / total
        good_ratio = len(good_news) / total

        analysis_parts.append("\n### 趋势判断\n")
        if bad_ratio > 0.3:
            analysis_parts.append("本周利空因素较多，需关注安全监管风险")
        elif good_ratio > 0.4:
            analysis_parts.append("本周政策利好为主，需求端表现强劲")
        elif good_ratio > 0.2:
            analysis_parts.append("本周有利好消息，可关注相关政策动态")
        else:
            analysis_parts.append("本周消息面相对均衡，行业运行平稳")

    return "\n".join(analysis_parts)


async def main():
    """主函数"""
    today = datetime.now().strftime("%Y%m%d")
    input_file = Path(__file__).parent.parent / "data" / f"news_parsed_{today}.json"

    if not input_file.exists():
        print(f"Parsed data not found: {input_file}")
        return

    with open(input_file, encoding="utf-8") as f:
        news_list = json.load(f)

    print(f"Analyzing {len(news_list)} news...")

    # 增强分析：先分类再分析情感再分析影响
    for news in news_list:
        news["type"] = classify_news_type(news.get("title", ""), news.get("content", ""))
        news["sentiment"] = analyze_sentiment(news.get("title", ""), news.get("content", ""))
        news["impact"] = analyze_impact(news)

    # 统计有效分类
    good_count = sum(1 for n in news_list if n["sentiment"] == "利好")
    bad_count = sum(1 for n in news_list if n["sentiment"] == "利空")
    print(f"  分类结果: 利好 {good_count} 条, 利空 {bad_count} 条")

    # 生成分析文本
    analysis_text = generate_analysis(news_list)

    output_file = Path(__file__).parent.parent / "data" / f"news_analyzed_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

    analysis_file = Path(__file__).parent.parent / "data" / f"news_analysis_{today}.md"
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(analysis_text)

    print(f"[DONE] Data: {output_file}, Analysis: {analysis_file}")
    return news_list, analysis_text


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
