#!/usr/bin/env python3
"""
智能路由技能主程序
集成到OpenClaw技能系统，支持模型管理和成本优化
"""

import sys
import os
import json
import argparse
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smart_router import router
try:
    from model_manager import model_manager, ModelManager
    MODEL_MANAGER_AVAILABLE = True
except ImportError:
    MODEL_MANAGER_AVAILABLE = False

def analyze_request(prompt: str) -> dict:
    """分析用户请求并返回路由结果"""
    try:
        result = router.route_request(prompt)
        
        # 添加技能标识
        result["skill"] = "smart-router"
        result["version"] = "2.0.0"
        
        # 添加模型配置信息
        if MODEL_MANAGER_AVAILABLE:
            result["model_config"] = {
                "total_models": len(model_manager.models),
                "enabled_models": len(model_manager.get_enabled_models()),
                "local_models": len(model_manager.get_local_models()),
                "cloud_models": len(model_manager.get_cloud_models())
            }
        
        return result
    except Exception as e:
        return {
            "error": str(e),
            "skill": "smart-router",
            "recommended_model": "deepseek/deepseek-chat",  # 出错时默认使用云端模型
            "reason": f"路由分析失败: {e}"
        }

def get_model_recommendation(prompt: str) -> str:
    """获取推荐的模型名称"""
    try:
        return router.get_recommended_model(prompt)
    except Exception:
        return "deepseek/deepseek-chat"  # 出错时默认使用云端模型

def list_models() -> dict:
    """列出所有模型配置"""
    if MODEL_MANAGER_AVAILABLE:
        return {
            "models": model_manager.models,
            "summary": {
                "total": len(model_manager.models),
                "enabled": len(model_manager.get_enabled_models()),
                "local": len(model_manager.get_local_models()),
                "cloud": len(model_manager.get_cloud_models())
            }
        }
    else:
        return {
            "error": "模型管理器不可用",
            "models": router.get_available_models()
        }

def update_models() -> dict:
    """更新模型配置（检测可用模型）"""
    if MODEL_MANAGER_AVAILABLE:
        model_manager.update_config_from_detection()
        return {
            "status": "success",
            "message": "模型配置已更新",
            "models": model_manager.models
        }
    else:
        return {
            "status": "error",
            "message": "模型管理器不可用"
        }

def add_model(model_id: str, model_type: str, name: str, priority: str = "normal") -> dict:
    """添加新模型"""
    if not MODEL_MANAGER_AVAILABLE:
        return {
            "status": "error",
            "message": "模型管理器不可用"
        }
    
    config = {
        "enable": True,
        "type": model_type,
        "name": name,
        "model_priority": priority,
        "description": f"用户添加的{model_type}模型",
        "cost_weight": 0.3 if model_type == "local" else 1.0
    }
    
    if model_manager.add_model(model_id, config):
        return {
            "status": "success",
            "message": f"已添加模型: {model_id}",
            "model_id": model_id,
            "config": config
        }
    else:
        return {
            "status": "error",
            "message": "添加模型失败"
        }

def remove_model(model_id: str) -> dict:
    """删除模型"""
    if not MODEL_MANAGER_AVAILABLE:
        return {
            "status": "error",
            "message": "模型管理器不可用"
        }
    
    if model_manager.remove_model(model_id):
        return {
            "status": "success",
            "message": f"已删除模型: {model_id}"
        }
    else:
        return {
            "status": "error",
            "message": f"删除模型失败: {model_id}"
        }

def main():
    """主函数：处理命令行参数"""
    parser = argparse.ArgumentParser(description="智能路由技能")
    parser.add_argument("command", nargs="?", help="命令: route, list, update, add, remove")
    parser.add_argument("args", nargs="*", help="命令参数")
    
    # 如果只有一个参数且不是命令，则视为路由请求
    if len(sys.argv) == 2 and sys.argv[1] not in ["list", "update", "add", "remove"]:
        prompt = sys.argv[1]
        result = analyze_request(prompt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    args = parser.parse_args()
    
    if args.command == "route":
        if not args.args:
            print("错误: 需要提供用户请求")
            sys.exit(1)
        prompt = " ".join(args.args)
        result = analyze_request(prompt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        result = list_models()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "update":
        result = update_models()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "add":
        if len(args.args) < 3:
            print("错误: 需要提供 model_id type name [priority]")
            print("示例: add ollama-local/new-model local '新模型' normal")
            sys.exit(1)
        
        model_id = args.args[0]
        model_type = args.args[1]
        name = args.args[2]
        priority = args.args[3] if len(args.args) > 3 else "normal"
        
        result = add_model(model_id, model_type, name, priority)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "remove":
        if not args.args:
            print("错误: 需要提供 model_id")
            sys.exit(1)
        
        model_id = args.args[0]
        result = remove_model(model_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("智能路由技能 v2.0.0")
        print("=" * 40)
        print("用法:")
        print("  路由请求: python main.py <用户请求>")
        print("  列出模型: python main.py list")
        print("  更新配置: python main.py update")
        print("  添加模型: python main.py add <model_id> <type> <name> [priority]")
        print("  删除模型: python main.py remove <model_id>")
        print("")
        print("示例:")
        print("  python main.py '现在几点了'")
        print("  python main.py list")
        print("  python main.py add ollama-local/test local '测试模型' normal")

if __name__ == "__main__":
    main()