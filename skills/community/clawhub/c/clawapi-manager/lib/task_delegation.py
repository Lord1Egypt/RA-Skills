#!/usr/bin/env python3
"""
API Cockpit - Task Delegation via OpenRouter
根据任务复杂度分配到正确的模型，通过 sessions_spawn 委派
"""

import os
import sys
import json
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'openrouter.json')

# OpenRouter API
API_KEY = os.getenv('OPENROUTER_API_KEY', '')
API_BASE = "https://openrouter.ai/api/v1"

# 免费/低成本模型
FREE_MODELS = [
    "qwen/qwen-2.5-0.5b-instruct",
    "qwen/qwen3.5-35b-a3b",
    "meta-llama/llama-3.2-1b-instruct",
]

# 中等成本模型
MEDIUM_MODELS = [
    "google/gemini-3.1-flash-image-preview",
    "bytedance-seed/seed-2.0-mini",
]

# 高成本模型（复杂任务）
EXPENSIVE_MODELS = [
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4o",
]

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return get_default_config()

def get_default_config():
    """默认配置"""
    return {
        "api_key": API_KEY,
        "routing": {
            "free_models": FREE_MODELS,
            "medium_models": MEDIUM_MODELS,
            "expensive_models": EXPENSIVE_MODELS,
        },
        "thresholds": {
            "simple_signals": ["search", "weather", "translate", "time", "date", "check", "list", "find"],
            "complex_signals": ["analyze", "write code", "debug", "architect", "design", "implement"],
        }
    }

def save_config(config):
    """保存配置"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def analyze_task(task_description):
    """分析任务复杂度（AI 预测）"""
    try:
        # 尝试使用 AI 预测
        from ai_complexity_predictor import AIComplexityPredictor
        predictor = AIComplexityPredictor()
        return predictor.predict_complexity(task_description)
    except Exception as e:
        # Fallback to keyword matching
        config = load_config()
        simple = config['thresholds']['simple_signals']
        complex = config['thresholds']['complex_signals']
        
        task_lower = task_description.lower()
        
        # 简单任务
        if any(s in task_lower for s in simple):
            return "free"
        # 复杂任务
        if any(c in task_lower for c in complex):
            return "expensive"
        # 默认中等
        return "medium"

def get_model_for_task(task_description):
    """获取适合任务的模型"""
    complexity = analyze_task(task_description)
    config = load_config()
    
    if complexity == "free":
        models = config['routing']['free_models']
    elif complexity == "expensive":
        models = config['routing']['expensive_models']
    else:
        models = config['routing']['medium_models']
    
    return models[0] if models else config['routing']['free_models'][0]

def generate_route_message(task, model):
    """生成路由消息"""
    complexity = analyze_task(task)
    return f"""🤖 任务路由

任务: {task[:50]}...
复杂度: {complexity}
路由模型: {model}

正在委派给 subagent...
"""

def delegate_task(task, target_model=None):
    """委派任务（返回委派指令）"""
    if target_model is None:
        target_model = get_model_for_task(task)
    
    complexity = analyze_task(task)
    
    # 构建委派指令
    delegation = {
        "task": task,
        "model": target_model,
        "complexity": complexity,
        "instruction": f"请用 {target_model} 模型完成以下任务：{task}"
    }
    
    return delegation

def main():
    """CLI"""
    if len(sys.argv) < 2:
        config = load_config()
        print(json.dumps(config, indent=2))
        return
    
    cmd = sys.argv[1]
    
    if cmd == "route":
        # 路由任务
        task = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        result = delegate_task(task)
        print(json.dumps(result, indent=2))
    
    elif cmd == "test":
        # 测试 OpenRouter 连接
        r = requests.get(f"{API_BASE}/models", 
                         headers={"Authorization": f"Bearer {API_KEY}"})
        if r.status_code == 200:
            print(f"✅ OpenRouter API OK, {len(r.json().get('data', []))} models available")
        else:
            print(f"❌ OpenRouter API Error: {r.status_code}")
    
    elif cmd == "models":
        # 列出可用模型
        r = requests.get(f"{API_BASE}/models",
                         headers={"Authorization": f"Bearer {API_KEY}"})
        if r.status_code == 200:
            models = r.json().get('data', [])[:10]
            for m in models:
                print(f"- {m.get('id')}")
    
    elif cmd == "set-free":
        config = load_config()
        config['routing']['free_models'] = sys.argv[2:] if len(sys.argv) > 2 else []
        save_config(config)
        print("免费模型已更新")

if __name__ == '__main__':
    main()
