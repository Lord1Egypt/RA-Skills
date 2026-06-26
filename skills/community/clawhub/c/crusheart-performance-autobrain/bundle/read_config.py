#!/usr/bin/env python3
"""
read_config.py — 读取本地配置（模型/channel）v1.0

功能：
  1. 读取 openclaw.json 中的模型配置
  2. 读取 openclaw.json 中的 channel 配置
  3. 输出标准化 JSON，供其他模块调用

用法：
  python3 scripts/read_config.py                    # 全部输出
  python3 scripts/read_config.py --models           # 仅模型
  python3 scripts/read_config.py --channels         # 仅渠道
  python3 scripts/read_config.py --channel-names    # 仅渠道名列表
  python3 scripts/read_config.py --model-ids        # 仅模型ID列表
  python3 scripts/read_config.py --json             # JSON 格式输出
"""

import json, os, sys
from typing import Dict, List, Optional

CONFIG_DIR = os.environ.get("OPENCLAW_CONFIG_DIR", os.path.expanduser("~/.openclaw"))
CONFIG_FILE = os.path.join(CONFIG_DIR, "openclaw.json")


def load_config() -> Dict:
    """加载 openclaw.json 配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}"}
    return {"error": "openclaw.json not found"}


def get_models(config: Dict = None) -> List[Dict]:
    """提取模型配置列表"""
    if config is None:
        config = load_config()
    
    models = config.get("models", {})
    if not models:
        return []
    
    result = []
    
    # models.providers.{provider}.models[] 结构
    providers = models.get("providers", {})
    for provider_name, provider_config in providers.items():
        provider_models = provider_config.get("models", [])
        for model in provider_models:
            result.append({
                "provider": provider_name,
                "id": model.get("id", ""),
                "name": model.get("name", ""),
                "context_window": model.get("contextWindow", 0),
                "max_tokens": model.get("maxTokens", 0),
                "reasoning": model.get("reasoning", False),
                "input_types": model.get("input", []),
                "cost_input": model.get("cost", {}).get("input", 0),
                "cost_output": model.get("cost", {}).get("output", 0),
                "base_url": provider_config.get("baseUrl", ""),
            })
    
    return result


def get_model_ids(config: Dict = None) -> List[str]:
    """获取所有模型 ID"""
    return [m["id"] for m in get_models(config)]


def get_channels(config: Dict = None) -> Dict:
    """提取 channel 配置"""
    if config is None:
        config = load_config()
    
    channels = config.get("channels", {})
    if not channels:
        return {}
    
    result = {}
    for name, ch_config in channels.items():
        result[name] = {
            "name": name,
            "enabled": ch_config.get("enabled", False),
            "agent_id": ch_config.get("agentId", ""),
            "uid": ch_config.get("uid", ""),
            "api_id": ch_config.get("apiId", ""),
            "push_id": ch_config.get("pushId", ""),
        }
    
    return result


def get_channel_names(config: Dict = None) -> List[str]:
    """获取所有 channel 名称"""
    return list(get_channels(config).keys())


def get_primary_channel(config: Dict = None) -> Optional[str]:
    """获取主渠道（第一个启用的）"""
    channels = get_channels(config)
    for name, info in channels.items():
        if info.get("enabled"):
            return name
    return list(channels.keys())[0] if channels else None


def read() -> Dict:
    """外部统一调用：返回完整配置摘要"""
    config = load_config()
    if "error" in config:
        return config
    
    models = get_models(config)
    channels = get_channels(config)
    
    return {
        "status": "ok",
        "model_count": len(models),
        "models": models,
        "channel_count": len(channels),
        "channels": channels,
        "primary_channel": get_primary_channel(config),
        "model_ids": [m["id"] for m in models],
        "channel_names": list(channels.keys()),
    }


if __name__ == "__main__":
    config = load_config()
    
    if "--models" in sys.argv:
        models = get_models(config)
        if "--json" in sys.argv:
            print(json.dumps(models, indent=2, ensure_ascii=False))
        else:
            print(f"模型配置 ({len(models)} 个):")
            for m in models:
                print(f"  [{m['provider']}] {m['id']} (ctx: {m['context_window']}, max: {m['max_tokens']})")
        sys.exit(0)

    elif "--channels" in sys.argv:
        channels = get_channels(config)
        if "--json" in sys.argv:
            print(json.dumps(channels, indent=2, ensure_ascii=False))
        else:
            print(f"渠道配置 ({len(channels)} 个):")
            for name, info in channels.items():
                print(f"  {name}: enabled={info.get('enabled', False)}, agentId={info.get('agent_id', '')}")
        sys.exit(0)

    elif "--channel-names" in sys.argv:
        names = get_channel_names(config)
        if "--json" in sys.argv:
            print(json.dumps(names))
        else:
            print("渠道名:", ", ".join(names))
        sys.exit(0)

    elif "--model-ids" in sys.argv:
        ids = get_model_ids(config)
        if "--json" in sys.argv:
            print(json.dumps(ids))
        else:
            print("模型ID:", ", ".join(ids))
        sys.exit(0)

    # 默认：完整输出
    result = read()
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"📋 本地配置摘要")
        print(f"  模型: {result.get('model_count', 0)} 个")
        for m in result.get("models", []):
            print(f"    [{m['provider']}] {m['id']}")
        print(f"  渠道: {result.get('channel_count', 0)} 个")
        for name in result.get("channel_names", []):
            print(f"    {name}")
        print(f"  主渠道: {result.get('primary_channel', 'N/A')}")
