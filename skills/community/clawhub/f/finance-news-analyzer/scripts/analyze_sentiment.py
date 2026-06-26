#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感分析脚本

使用 LLM API 对财经新闻进行情感分析

用法:
    python analyze_sentiment.py --input news.json --output analyzed.json
    python analyze_sentiment.py --text "英伟达发布新一代 AI 芯片" --model gpt-4o-mini
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# 尝试导入 OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# 尝试导入 Anthropic
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# 尝试导入 DashScope (阿里通义千问)
try:
    import dashscope
    HAS_DASHSCOPE = True
except ImportError:
    HAS_DASHSCOPE = False

# 尝试导入百度文心一言
try:
    import qianfan
    HAS_QIANFAN = True
except ImportError:
    HAS_QIANFAN = False

# 尝试导入智谱 AI
try:
    from zhipuai import ZhipuAI
    HAS_ZHIPU = True
except ImportError:
    HAS_ZHIPU = False


def get_api_client(model: str):
    """获取 API 客户端"""
    
    # OpenAI 系列
    if any(x in model.lower() for x in ['gpt-', 'gpt4', 'gpt-4', 'gpt-3.5', 'openai']):
        if not HAS_OPENAI:
            raise ImportError("请安装 openai: pip install openai")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 OPENAI_API_KEY")
        return OpenAI(api_key=api_key), 'openai'
    
    # Anthropic Claude 系列
    elif any(x in model.lower() for x in ['claude', 'anthropic']):
        if not HAS_ANTHROPIC:
            raise ImportError("请安装 anthropic: pip install anthropic")
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 ANTHROPIC_API_KEY")
        return Anthropic(api_key=api_key), 'anthropic'
    
    # 阿里通义千问 (DashScope)
    elif any(x in model.lower() for x in ['qwen', '通义', 'dashscope', 'aliyun']):
        if not HAS_DASHSCOPE:
            raise ImportError("请安装 dashscope: pip install dashscope")
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")
        dashscope.api_key = api_key
        return dashscope, 'dashscope'
    
    # 百度文心一言
    elif any(x in model.lower() for x in ['ernie', '文心', 'baidu', 'qianfan']):
        if not HAS_QIANFAN:
            raise ImportError("请安装 qianfan: pip install qianfan")
        api_key = os.getenv('QIANFAN_AK')
        secret_key = os.getenv('QIANFAN_SK')
        if not api_key or not secret_key:
            raise ValueError("请设置环境变量 QIANFAN_AK 和 QIANFAN_SK")
        qianfan.AK = api_key
        qianfan.SK = secret_key
        return qianfan, 'qianfan'
    
    # 智谱 AI (GLM)
    elif any(x in model.lower() for x in ['glm', '智谱', 'zhipu']):
        if not HAS_ZHIPU:
            raise ImportError("请安装 zhipuai: pip install zhipuai")
        api_key = os.getenv('ZHIPUAI_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 ZHIPUAI_API_KEY")
        return ZhipuAI(api_key=api_key), 'zhipu'
    
    # Ollama 本地模型
    elif 'ollama' in model.lower():
        if not HAS_OPENAI:
            raise ImportError("请安装 openai: pip install openai (用于 Ollama 兼容)")
        base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
        return OpenAI(base_url=base_url, api_key='ollama'), 'ollama'
    
    # 默认使用 OpenAI
    else:
        if not HAS_OPENAI:
            raise ImportError("请安装 openai: pip install openai")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 OPENAI_API_KEY 或其他模型 API 密钥")
        return OpenAI(api_key=api_key), 'openai'


def build_sentiment_prompt(news_item: Dict[str, Any]) -> str:
    """构建情感分析提示词"""
    
    title = news_item.get('title', '')
    summary = news_item.get('summary', '')
    source = news_item.get('source', '')
    
    prompt = f"""你是一位专业的财经分析师，请对以下新闻进行情感分析。

**新闻标题**: {title}
**新闻摘要**: {summary}
**新闻来源**: {source}

请按以下 JSON 格式输出分析结果：

```json
{{
  "sentiment": "positive|negative|neutral",
  "sentiment_score": 0-100,
  "confidence": "high|medium|low",
  "sentiment_label": "🟢|🔴|⚪",
  "key_points": ["关键信息点 1", "关键信息点 2"],
  "affected_sectors": ["受影响行业 1", "受影响行业 2"],
  "affected_stocks": [{{"ticker": "股票代码", "impact": "positive|negative|neutral"}}],
  "timeframe": "short|medium|long",
  "reasoning": "判断依据，50 字以内"
}}
```

分析规则:
1. 利好信号：营收超预期、新产品发布、大合同签订、政策支持、高管增持等
2. 利空信号：营收不及预期、产品召回、高管离职、监管处罚、竞争加剧等
3. 中性信号：符合预期、常规业务、未证实传言等
4. 置信度：官方公告/权威媒体=高，主流媒体=中，社交媒体/传言=低
5. 时间维度：产品发布/合同=短期，财报/战略=中期，技术突破/政策=长期

请直接输出 JSON，不要有其他内容。"""
    
    return prompt


def analyze_with_openai(client: OpenAI, model: str, prompt: str) -> Dict[str, Any]:
    """使用 OpenAI 进行分析"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位专业的财经分析师，擅长从新闻中提取投资信号。请严格输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    
    content = response.choices[0].message.content.strip()
    
    # 提取 JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    return json.loads(content)


def analyze_with_anthropic(client: Anthropic, model: str, prompt: str) -> Dict[str, Any]:
    """使用 Anthropic 进行分析"""
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        system="你是一位专业的财经分析师，擅长从新闻中提取投资信号。请严格输出 JSON 格式。",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    content = response.content[0].text.strip()
    
    # 提取 JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    return json.loads(content)


def analyze_with_dashscope(model: str, prompt: str) -> Dict[str, Any]:
    """使用阿里通义千问进行分析"""
    response = dashscope.Generation.call(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位专业的财经分析师，擅长从新闻中提取投资信号。请严格输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    
    content = response.output.choices[0].message.content.strip()
    
    # 提取 JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    return json.loads(content)


def analyze_with_qianfan(model: str, prompt: str) -> Dict[str, Any]:
    """使用百度文心一言进行分析"""
    chat_comp = qianfan.ChatCompletion()
    response = chat_comp.do(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位专业的财经分析师，擅长从新闻中提取投资信号。请严格输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    content = response.body.get('result', '').strip()
    
    # 提取 JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    return json.loads(content)


def analyze_with_zhipu(client: ZhipuAI, model: str, prompt: str) -> Dict[str, Any]:
    """使用智谱 AI 进行分析"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位专业的财经分析师，擅长从新闻中提取投资信号。请严格输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    
    content = response.choices[0].message.content.strip()
    
    # 提取 JSON
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    return json.loads(content)


def analyze_single_news(news_item: Dict[str, Any], model: str = 'gpt-4o-mini') -> Dict[str, Any]:
    """分析单条新闻"""
    
    client, provider = get_api_client(model)
    prompt = build_sentiment_prompt(news_item)
    
    try:
        if provider == 'openai':
            result = analyze_with_openai(client, model, prompt)
        elif provider == 'anthropic':
            result = analyze_with_anthropic(client, model, prompt)
        elif provider == 'dashscope':
            result = analyze_with_dashscope(model, prompt)
        elif provider == 'qianfan':
            result = analyze_with_qianfan(model, prompt)
        elif provider == 'zhipu':
            result = analyze_with_zhipu(client, model, prompt)
        elif provider == 'ollama':
            result = analyze_with_openai(client, model, prompt)  # Ollama 使用 OpenAI 兼容 API
        else:
            result = analyze_with_openai(client, model, prompt)
        
        # 合并结果
        news_item.update(result)
        return news_item
    
    except Exception as e:
        print(f"分析失败：{e}")
        # 返回默认中性结果
        news_item.update({
            'sentiment': 'neutral',
            'sentiment_score': 50,
            'confidence': 'low',
            'sentiment_label': '⚪',
            'key_points': [],
            'affected_sectors': [],
            'affected_stocks': [],
            'timeframe': 'short',
            'reasoning': f'分析失败：{str(e)}'
        })
        return news_item


def analyze_batch(news_items: List[Dict[str, Any]], model: str = 'gpt-4o-mini', 
                  max_concurrent: int = 5) -> List[Dict[str, Any]]:
    """批量分析新闻"""
    
    import concurrent.futures
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = {
            executor.submit(analyze_single_news, item, model): item 
            for item in news_items
        }
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                result = future.result()
                results.append(result)
                print(f"✅ 已分析 {i+1}/{len(news_items)} 条")
            except Exception as e:
                print(f"❌ 分析失败：{e}")
                results.append(futures[future])
    
    return results


def analyze_text(text: str, model: str = 'gpt-4o-mini') -> Dict[str, Any]:
    """分析单段文本"""
    news_item = {
        'title': text[:100],
        'summary': text,
        'source': '用户输入'
    }
    return analyze_single_news(news_item, model)


def main():
    parser = argparse.ArgumentParser(description='财经新闻情感分析')
    
    parser.add_argument('--input', type=str, help='输入 JSON 文件路径')
    parser.add_argument('--output', type=str, help='输出 JSON 文件路径')
    parser.add_argument('--text', type=str, help='直接分析文本')
    parser.add_argument('--model', type=str, default='gpt-4o-mini',
                        help='LLM 模型（默认：gpt-4o-mini）')
    parser.add_argument('--max-concurrent', type=int, default=5,
                        help='最大并发数（默认：5）')
    
    args = parser.parse_args()
    
    # 检查 API 密钥
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ 错误：请设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量")
        print("\n使用方法:")
        print("  export OPENAI_API_KEY=sk-xxx")
        print("  # 或")
        print("  export ANTHROPIC_API_KEY=sk-ant-xxx")
        sys.exit(1)
    
    # 分析单段文本
    if args.text:
        print(f"🧠 分析文本...")
        result = analyze_text(args.text, args.model)
        print("\n" + "=" * 50)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 分析文件
    if not args.input:
        print("❌ 错误：请提供 --input 文件路径或 --text 文本")
        sys.exit(1)
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 错误：文件不存在：{input_path}")
        sys.exit(1)
    
    print(f"📂 加载新闻：{input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    if not isinstance(news_items, list):
        news_items = [news_items]
    
    print(f"📰 共 {len(news_items)} 条新闻")
    print(f"🤖 使用模型：{args.model}")
    print(f"🔧 最大并发：{args.max_concurrent}")
    print("\n开始分析...\n")
    
    # 批量分析
    results = analyze_batch(news_items, args.model, args.max_concurrent)
    
    # 统计
    positive = len([r for r in results if r.get('sentiment') == 'positive'])
    negative = len([r for r in results if r.get('sentiment') == 'negative'])
    neutral = len([r for r in results if r.get('sentiment') == 'neutral'])
    
    print("\n" + "=" * 50)
    print("📊 分析完成！")
    print(f"   🟢 利好：{positive} 条 ({positive/len(results)*100:.1f}%)")
    print(f"   🔴 利空：{negative} 条 ({negative/len(results)*100:.1f}%)")
    print(f"   ⚪ 中性：{neutral} 条 ({neutral/len(results)*100:.1f}%)")
    
    # 保存结果
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存：{output_path}")
    else:
        print("\n" + "=" * 50)
        print("详细结果:")
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
