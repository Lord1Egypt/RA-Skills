#!/usr/bin/env python3
"""
Built-in Provider Templates
内置 Provider 配置模板
"""

BUILTIN_PROVIDERS = {
    'openai': {
        'name': 'OpenAI',
        'baseUrl': 'https://api.openai.com/v1',
        'api': 'openai-responses',  # ← 修复：使用有效协议
        'models': [
            {'id': 'gpt-4', 'name': 'GPT-4'},
            {'id': 'gpt-4-turbo', 'name': 'GPT-4 Turbo'},
            {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo'}
        ],
        'env_key': 'OPENAI_API_KEY'
    },
    'anthropic': {
        'name': 'Anthropic',
        'baseUrl': 'https://api.anthropic.com',
        'api': 'anthropic-messages',
        'models': [
            {'id': 'claude-opus-4-6', 'name': 'Claude Opus 4.6'},
            {'id': 'claude-sonnet-4-5', 'name': 'Claude Sonnet 4.5'},
            {'id': 'claude-3-opus-20240229', 'name': 'Claude 3 Opus'}
        ],
        'env_key': 'ANTHROPIC_API_KEY'
    },
    'openrouter': {
        'name': 'OpenRouter',
        'baseUrl': 'https://openrouter.ai/api/v1',
        'api': 'openai-responses',  # ← 修复：使用有效协议
        'models': [
            {'id': 'anthropic/claude-opus-4-6', 'name': 'Claude Opus 4.6'},
            {'id': 'openai/gpt-4-turbo', 'name': 'GPT-4 Turbo'},
            {'id': 'qwen/qwen-2.5-coder-32b-instruct:free', 'name': 'Qwen 2.5 Coder (Free)'}
        ],
        'env_key': 'OPENROUTER_API_KEY'
    },
    'google': {
        'name': 'Google Gemini',
        'baseUrl': 'https://generativelanguage.googleapis.com/v1beta',
        'api': 'google-generative-ai',
        'models': [
            {'id': 'gemini-3-pro-preview', 'name': 'Gemini 3 Pro'},
            {'id': 'gemini-2-flash', 'name': 'Gemini 2 Flash'}
        ],
        'env_key': 'GEMINI_API_KEY'
    },
    'moonshot': {
        'name': 'Moonshot AI (Kimi)',
        'baseUrl': 'https://api.moonshot.ai/v1',
        'api': 'openai-completions',
        'models': [
            {'id': 'kimi-k2.5', 'name': 'Kimi K2.5'},
            {'id': 'kimi-k2-turbo-preview', 'name': 'Kimi K2 Turbo'}
        ],
        'env_key': 'MOONSHOT_API_KEY'
    },
    'ollama': {
        'name': 'Ollama (Local)',
        'baseUrl': 'http://127.0.0.1:11434/v1',
        'api': 'ollama',  # ← 修复：使用 ollama 协议
        'models': [
            {'id': 'llama3.3', 'name': 'Llama 3.3'},
            {'id': 'qwen2.5-coder', 'name': 'Qwen 2.5 Coder'}
        ],
        'env_key': None  # 本地服务，不需要 API Key
    },
    'groq': {
        'name': 'Groq',
        'baseUrl': 'https://api.groq.com/openai/v1',
        'api': 'openai-responses',  # ← 修复：使用有效协议
        'models': [
            {'id': 'llama-3.3-70b-versatile', 'name': 'Llama 3.3 70B'},
            {'id': 'mixtral-8x7b-32768', 'name': 'Mixtral 8x7B'}
        ],
        'env_key': 'GROQ_API_KEY'
    },
    'deepseek': {
        'name': 'DeepSeek',
        'baseUrl': 'https://api.deepseek.com/v1',
        'api': 'openai-responses',  # ← 修复：使用有效协议
        'models': [
            {'id': 'deepseek-chat', 'name': 'DeepSeek Chat'},
            {'id': 'deepseek-coder', 'name': 'DeepSeek Coder'}
        ],
        'env_key': 'DEEPSEEK_API_KEY'
    },
    'volcengine': {
        'name': 'VolcEngine (火山引擎)',
        'baseUrl': 'https://ark.cn-beijing.volces.com/api/coding',
        'api': 'anthropic-messages',  # ← 兼容 Anthropic 接口协议
        'models': [
            {'id': 'doubao-seed-2.0-code', 'name': 'Doubao Seed 2.0 Code'}
        ],
        'env_key': 'VOLCENGINE_API_KEY'
    }
}

def list_builtin_providers():
    """列出所有内置 provider"""
    result = []
    for provider_id, config in BUILTIN_PROVIDERS.items():
        result.append({
            'id': provider_id,
            'name': config['name'],
            'protocol': config['api'],
            'model_count': len(config['models']),
            'requires_key': config['env_key'] is not None
        })
    return result

def get_provider_template(provider_id: str):
    """获取 provider 配置模板"""
    if provider_id not in BUILTIN_PROVIDERS:
        return None
    return BUILTIN_PROVIDERS[provider_id]

def format_provider_list():
    """格式化 provider 列表"""
    output = "**内置 Provider**\n\n"
    for p in list_builtin_providers():
        key_status = "需要 API Key" if p['requires_key'] else "本地服务"
        output += f"• {p['id']}: {p['name']} ({p['protocol']}) - {p['model_count']} 个模型 - {key_status}\n"
    return output

def main():
    """测试"""
    print(format_provider_list())
    
    print("\n=== OpenAI 模板 ===")
    template = get_provider_template('openai')
    print(f"Name: {template['name']}")
    print(f"Base URL: {template['baseURL']}")
    print(f"Protocol: {template['api']}")
    print(f"Models: {len(template['models'])}")

if __name__ == '__main__':
    main()
