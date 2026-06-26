"""
Kimi API Client for Newsman
Supports Allegretto subscription and various Moonshot models.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import List, Dict, Optional
from pathlib import Path


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from TOML file."""
    if config_path is None:
        # 查找配置文件
        script_dir = Path(__file__).parent.parent
        config_path = script_dir / "config" / "config.toml"
    
    config = {
        'api': {'provider': 'local'},
        'kimi': {
            'base_url': 'https://api.moonshot.cn/v1',
            'api_key': '',
            'model': 'moonshot-v1-8k',
            'max_tokens': 500,
            'temperature': 0.3
        },
        'summarization': {
            'default_method': 'extractive',
            'max_length': 150,
            'chinese_output': True
        }
    }
    
    # 解析 TOML (简化版)
    if Path(config_path).exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_section = None
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
            
            if '=' in line and current_section:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                # 处理环境变量
                if value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]
                    value = os.getenv(env_var, '')
                
                if current_section in config:
                    config[current_section][key] = value
    
    # 从环境变量覆盖
    if os.getenv('KIMI_API_KEY'):
        config['kimi']['api_key'] = os.getenv('KIMI_API_KEY')
    if os.getenv('KIMI_BASE_URL'):
        config['kimi']['base_url'] = os.getenv('KIMI_BASE_URL')
    if os.getenv('KIMI_MODEL'):
        config['kimi']['model'] = os.getenv('KIMI_MODEL')
    
    return config


def create_summary_prompt(title: str, content: str, max_words: int = 150, chinese: bool = True) -> str:
    """Create prompt for news summarization."""
    if chinese:
        return f"""请为以下新闻生成简洁的摘要，限制在 {max_words} 个词以内：

标题：{title}

内容：
{content}

请生成一个简洁、准确的中文摘要，突出关键信息："""
    else:
        return f"""Please generate a concise summary of the following news article, limited to {max_words} words:

Title: {title}

Content:
{content}

Generate a brief, accurate summary highlighting the key information:"""


def summarize_with_kimi(title: str, content: str, config: Dict) -> str:
    """Summarize news using Kimi API."""
    kimi_config = config.get('kimi', {})
    
    api_key = kimi_config.get('api_key', '')
    base_url = kimi_config.get('base_url', 'https://api.moonshot.cn/v1')
    model = kimi_config.get('model', 'moonshot-v1-8k')
    max_tokens = int(kimi_config.get('max_tokens', 500))
    temperature = float(kimi_config.get('temperature', 0.3))
    chinese = config.get('summarization', {}).get('chinese_output', True)
    max_words = config.get('summarization', {}).get('max_length', 150)
    
    if not api_key:
        raise ValueError("Kimi API key not configured. Set KIMI_API_KEY environment variable.")
    
    # 构建请求
    prompt = create_summary_prompt(title, content, max_words, chinese)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': '你是一个专业的新闻摘要助手。请生成简洁、准确的新闻摘要。'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': max_tokens,
        'temperature': temperature
    }
    
    req = urllib.request.Request(
        f'{base_url}/chat/completions',
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"Kimi API error: {e.code} - {error_body}")
    except Exception as e:
        raise Exception(f"Failed to call Kimi API: {e}")


def batch_summarize_with_kimi(items: List[Dict], config: Dict) -> List[Dict]:
    """Summarize multiple items using Kimi API."""
    results = []
    max_words = config.get('summarization', {}).get('max_length', 150)
    
    for item in items:
        title = item.get('title', '')
        content = item.get('summary', '') or item.get('description', '')
        
        # 合并标题和内容进行摘要
        full_text = f"{title}\n\n{content}" if content else title
        
        try:
            summary = summarize_with_kimi(title, full_text, config)
            item['ai_summary'] = summary
            item['summary_method'] = 'kimi-api'
        except Exception as e:
            # 如果 API 失败，保留原始内容
            item['ai_summary'] = content[:200] + '...' if len(content) > 200 else content
            item['summary_method'] = 'fallback'
            item['summary_error'] = str(e)
        
        results.append(item)
    
    return results


if __name__ == '__main__':
    # 测试 API 连接
    config = load_config()
    
    print("Kimi API Configuration:")
    print(f"  Base URL: {config['kimi']['base_url']}")
    print(f"  Model: {config['kimi']['model']}")
    print(f"  API Key: {'*' * 10 if config['kimi']['api_key'] else 'NOT SET'}")
    
    if config['kimi']['api_key']:
        # 测试 API 调用
        test_item = {
            'title': 'Test News Article',
            'summary': 'This is a test article to verify the Kimi API connection is working properly.'
        }
        
        try:
            result = batch_summarize_with_kimi([test_item], config)
            print("\n✅ API test successful!")
            print(f"Generated summary: {result[0].get('ai_summary', 'N/A')}")
        except Exception as e:
            print(f"\n❌ API test failed: {e}")
            sys.exit(1)
    else:
        print("\n⚠️ API key not configured. Set KIMI_API_KEY environment variable.")
