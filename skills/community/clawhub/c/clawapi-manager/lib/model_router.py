#!/usr/bin/env python3
"""
API Cockpit - Model Priority & Auto-Switch
配置模型优先级，处理简单任务时自动切换到免费模型
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'model_priority.json')

# 免费模型列表
FREE_MODELS = {
    "openrouter": {
        "qwen-qwen-2.5-0.5b-instruct": {"cost": 0, "context": 32},
        "llama-3.2-1b-instruct": {"cost": 0, "context": 128},
        "mistral-7b-instruct": {"cost": 0, "context": 32},
    },
    "nvidia": {
        "nvidia/llama-3.1-nemotron-70b-instruct": {"cost": 0, "context": 128},
        "nvidia/mitre-8b": {"cost": 0, "context": 32},
    }
}

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return get_default_config()

def get_default_config():
    """默认配置"""
    return {
        "default_model": "minimax/MiniMax-M2.5",
        "priority": ["minimax/MiniMax-M2.5", "volcengine", "aiclauder"],
        "confirm_before_switch": True,
        "free_models": {
            "enabled": True,
            "providers": ["openrouter"],
            "simple_signals": ["search", "weather", "translate", "time", "date", "simple", "check"]
        },
        "thresholds": {
            "quota_warning_percent": 80,
            "quota_critical_percent": 95
        }
    }

def save_config(config):
    """保存配置"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def is_simple_task(task_description):
    """判断是否为简单任务"""
    config = load_config()
    signals = config.get('free_models', {}).get('simple_signals', [])
    task_lower = task_description.lower()
    return any(signal in task_lower for signal in signals)

def get_next_model(current_model):
    """获取下一个可用模型"""
    config = load_config()
    priority = config.get('priority', [])
    
    if current_model not in priority:
        return priority[0] if priority else config.get('default_model')
    
    try:
        idx = priority.index(current_model)
        return priority[idx + 1] if idx + 1 < len(priority) else priority[0]
    except:
        return config.get('default_model')

def get_free_model():
    """获取免费模型"""
    config = load_config()
    providers = config.get('free_models', {}).get('providers', ['openrouter'])
    
    for provider in providers:
        if provider in FREE_MODELS:
            models = list(FREE_MODELS[provider].keys())
            if models:
                return models[0]
    
    return "openrouter/qwen-qwen-2.5-0.5b-instruct"

def should_switch_to_free(task_description):
    """判断是否应切换到免费模型"""
    config = load_config()
    
    if not config.get('free_models', {}).get('enabled', False):
        return False
    
    return is_simple_task(task_description)

def generate_confirmation_message(model_info):
    """生成确认消息"""
    return f"""⚠️ API 配额不足警告

当前模型: {model_info.get('current', 'N/A')}
剩余配额: {model_info.get('remaining', 'N/A')}
使用比例: {model_info.get('percent', 'N/A')}%

建议切换到: {model_info.get('suggested', 'N/A')}

确认切换？回复 [yes/no] 或指定模型 [模型名]"""

def main():
    """CLI"""
    if len(sys.argv) < 2:
        config = load_config()
        print(json.dumps(config, indent=2))
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'set':
        # 设置默认模型
        config = load_config()
        config['default_model'] = sys.argv[2] if len(sys.argv) > 2 else config['default_model']
        save_config(config)
        print(f"默认模型已设为: {config['default_model']}")
    
    elif cmd == 'priority':
        # 设置优先级
        config = load_config()
        config['priority'] = sys.argv[2:] if len(sys.argv) > 2 else config['priority']
        save_config(config)
        print(f"优先级: {config['priority']}")
    
    elif cmd == 'next':
        # 获取下一个模型
        current = sys.argv[2] if len(sys.argv) > 2 else ""
        print(get_next_model(current))
    
    elif cmd == 'free':
        # 获取免费模型
        print(get_free_model())
    
    elif cmd == 'check':
        # 检查任务是否应用免费模型
        task = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        result = should_switch_to_free(task)
        print(json.dumps({
            "task": task,
            "should_use_free": result,
            "free_model": get_free_model() if result else None
        }, indent=2))
    
    elif cmd == 'enable-free':
        # 启用免费模型路由
        config = load_config()
        config['free_models']['enabled'] = True
        save_config(config)
        print("免费模型路由已启用")
    
    elif cmd == 'disable-free':
        # 禁用免费模型路由
        config = load_config()
        config['free_models']['enabled'] = False
        save_config(config)
        print("免费模型路由已禁用")

if __name__ == '__main__':
    main()
