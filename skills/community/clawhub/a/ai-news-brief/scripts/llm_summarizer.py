#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型摘要生成模块
功能：使用大模型生成更好的文章摘要
"""

import sys
import io
import os
import json

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "llm_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "llm_config.json.default")


def load_llm_config():
    """加载LLM配置（优先用户配置）"""
    # 优先读取用户配置目录
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认LLM配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
            return None
    
    return None


def generate_summary_with_llm(title, content, config=None):
    """
    使用大模型生成摘要
    """
    if config is None:
        config = load_llm_config()
        if config is None:
            return None, "配置加载失败"
    
    llm_config = config.get('config', {})
    
    if not llm_config.get('enabled', False):
        return None, "LLM未启用，请在llm_config.json中设置enabled:true"
    
    provider = llm_config.get('provider', 'deepseek')
    provider_config = llm_config.get(provider, {})
    
    api_key = provider_config.get('api_key', '')
    api_url = provider_config.get('api_url', '')
    model = provider_config.get('model', '')
    
    if not api_key or api_key == "your_api_key_here":
        return None, "API Key未配置"
    
    # 构建prompt
    prompt_template = config.get('prompt_template', 
        "请为以下文章生成50字以内的核心摘要：\n标题：{title}\n内容：{content}\n摘要：")
    
    prompt = prompt_template.format(title=title[:100], content=content[:2000])
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.3
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            return summary, "success"
        else:
            return None, f"API错误: {response.status_code}"
    
    except Exception as e:
        return None, f"请求失败: {str(e)[:50]}"


def generate_bulk_summaries(articles, config=None, max_at_once=5):
    """
    批量生成摘要
    - 为了节省token，每次最多处理N条
    - 只对没有成功摘要的文章进行处理
    """
    if config is None:
        config = load_llm_config()
    
    llm_config = config.get('config', {}) if config else {}
    if not llm_config.get('enabled', False):
        print("  ℹ️ LLM未启用，跳过AI摘要生成")
        return articles
    
    print(f"  🤖 正在使用LLM生成摘要 (最多 {max_at_once} 条)...")
    
    count = 0
    for i, article in enumerate(articles[:max_at_once]):
        # 如果已有较好摘要，跳过
        existing_summary = article.get('summary', '')
        if existing_summary and len(existing_summary) > 50:
            continue
        
        title = article.get('title', '')
        content = article.get('summary', '') or article.get('content', '')[:2000]
        
        if not content:
            continue
        
        summary, status = generate_summary_with_llm(title, content, config)
        
        if status == "success" and summary:
            article['llm_summary'] = summary
            count += 1
            print(f"    {i+1}. ✅ {title[:30]}...")
            time.sleep(0.5)  # 避免请求过快
        else:
            print(f"    {i+1}. ❌ {title[:30]}... ({status})")
    
    if count > 0:
        print(f"  📝 已为 {count} 篇文章生成LLM摘要")
    else:
        print(f"  ℹ️ 没有需要生成摘要的文章")
    
    return articles


def test_llm_config():
    """测试LLM配置"""
    config = load_llm_config()
    
    if not config:
        print("❌ 配置加载失败")
        return
    
    llm = config.get('config', {})
    
    print("=" * 50)
    print("LLM 配置检查")
    print("=" * 50)
    print(f"启用状态: {'✅ 已启用' if llm.get('enabled') else '❌ 未启用'}")
    print(f"服务商: {llm.get('provider', '未选择')}")
    
    provider = llm.get(llm.get('provider', 'deepseek'), {})
    api_key = provider.get('api_key', '')
    
    if api_key and api_key != "your_api_key_here":
        print(f"API Key: {'✅ 已配置' if api_key else '❌ 未配置'}")
    else:
        print(f"API Key: ❌ 未配置")
    
    print("=" * 50)
    
    if not llm.get('enabled'):
        print("\n请编辑 llm_config.json 设置 enabled: true 和 API Key")


if __name__ == "__main__":
    test_llm_config()