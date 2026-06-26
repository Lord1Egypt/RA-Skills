#!/usr/bin/env python3
"""
模型管理CLI工具
用于管理模型配置的独立命令行工具
"""

import sys
import json
import argparse
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from model_manager import model_manager, ModelManager
    MODEL_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"错误: 无法导入模型管理器: {e}")
    MODEL_MANAGER_AVAILABLE = False
    sys.exit(1)

def print_colored(text: str, color: str = "reset") -> None:
    """打印彩色文本"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def command_list(args):
    """列出所有模型"""
    print_colored("\n📋 模型配置列表", "cyan")
    print("=" * 60)
    
    enabled_models = model_manager.get_enabled_models()
    disabled_models = {k: v for k, v in model_manager.models.items() 
                      if not v.get("enable", False)}
    
    print_colored(f"总模型数: {len(model_manager.models)}", "yellow")
    print_colored(f"启用模型: {len(enabled_models)}", "green")
    print_colored(f"禁用模型: {len(disabled_models)}", "red")
    
    if enabled_models:
        print_colored("\n✅ 启用模型:", "green")
        for i, (model_id, config) in enumerate(enabled_models.items(), 1):
            type_color = "blue" if config.get("type") == "local" else "magenta"
            priority_color = "yellow" if config.get("model_priority") == "normal" else "red"
            
            print(f"  {i}. {model_id}")
            print(f"     名称: {config.get('name', 'N/A')}")
            print(f"     类型: {print_colored(config.get('type', 'N/A'), type_color)}")
            print(f"     优先级: {print_colored(config.get('model_priority', 'N/A'), priority_color)}")
            print(f"     成本权重: {config.get('cost_weight', 'N/A')}")
            print(f"     描述: {config.get('description', 'N/A')}")
    
    if disabled_models:
        print_colored("\n❌ 禁用模型:", "red")
        for i, (model_id, config) in enumerate(disabled_models.items(), 1):
            print(f"  {i}. {model_id} - {config.get('name', 'N/A')}")

def command_show(args):
    """显示单个模型详情"""
    model_id = args.model_id
    if model_id not in model_manager.models:
        print_colored(f"错误: 模型不存在: {model_id}", "red")
        return
    
    config = model_manager.models[model_id]
    
    print_colored(f"\n🔍 模型详情: {model_id}", "cyan")
    print("=" * 60)
    
    status = "✅ 启用" if config.get("enable", False) else "❌ 禁用"
    status_color = "green" if config.get("enable", False) else "red"
    
    print_colored(f"状态: {status}", status_color)
    print(f"名称: {config.get('name', 'N/A')}")
    print(f"类型: {config.get('type', 'N/A')}")
    print(f"优先级: {config.get('model_priority', 'N/A')}")
    print(f"成本权重: {config.get('cost_weight', 'N/A')}")
    print(f"描述: {config.get('description', 'N/A')}")
    
    # 显示所有字段
    print_colored("\n📄 完整配置:", "yellow")
    print(json.dumps(config, ensure_ascii=False, indent=2))

def command_detect(args):
    """检测可用模型"""
    print_colored("\n🔍 检测可用模型中...", "cyan")
    
    detected_models = model_manager.detect_available_models()
    
    print_colored(f"检测到 {len(detected_models)} 个可用模型:", "green")
    for model_id, config in detected_models.items():
        status = "✅" if config.get("detected", False) else "❌"
        print(f"  {status} {model_id} - {config.get('name', 'N/A')}")
    
    if args.update:
        print_colored("\n🔄 更新配置中...", "yellow")
        model_manager.update_config_from_detection()
        print_colored("✅ 配置已更新", "green")
        command_list(args)

def command_enable(args):
    """启用模型"""
    model_id = args.model_id
    if model_id not in model_manager.models:
        print_colored(f"错误: 模型不存在: {model_id}", "red")
        return
    
    if model_manager.enable_model(model_id):
        print_colored(f"✅ 已启用模型: {model_id}", "green")
    else:
        print_colored(f"❌ 启用模型失败: {model_id}", "red")

def command_disable(args):
    """禁用模型"""
    model_id = args.model_id
    if model_id not in model_manager.models:
        print_colored(f"错误: 模型不存在: {model_id}", "red")
        return
    
    if model_manager.disable_model(model_id):
        print_colored(f"✅ 已禁用模型: {model_id}", "yellow")
    else:
        print_colored(f"❌ 禁用模型失败: {model_id}", "red")

def command_add(args):
    """添加新模型"""
    model_id = args.model_id
    model_type = args.type
    name = args.name
    priority = args.priority
    
    if model_id in model_manager.models:
        print_colored(f"警告: 模型已存在: {model_id}", "yellow")
        if not args.force:
            print_colored("使用 --force 参数覆盖", "yellow")
            return
    
    config = {
        "enable": True,
        "type": model_type,
        "name": name,
        "model_priority": priority,
        "description": args.description or f"用户添加的{model_type}模型",
        "cost_weight": args.cost_weight or (0.3 if model_type == "local" else 1.0)
    }
    
    if model_manager.add_model(model_id, config):
        print_colored(f"✅ 已添加模型: {model_id}", "green")
        command_show(argparse.Namespace(model_id=model_id))
    else:
        print_colored(f"❌ 添加模型失败: {model_id}", "red")

def command_remove(args):
    """删除模型"""
    model_id = args.model_id
    if model_id not in model_manager.models:
        print_colored(f"错误: 模型不存在: {model_id}", "red")
        return
    
    if not args.force:
        confirm = input(f"确认删除模型 '{model_id}'? [y/N]: ")
        if confirm.lower() != 'y':
            print_colored("取消删除", "yellow")
            return
    
    if model_manager.remove_model(model_id):
        print_colored(f"✅ 已删除模型: {model_id}", "green")
    else:
        print_colored(f"❌ 删除模型失败: {model_id}", "red")

def command_cost(args):
    """成本优化分析"""
    print_colored("\n💰 成本优化分析", "cyan")
    print("=" * 60)
    
    enabled_models = model_manager.get_enabled_models()
    
    if not enabled_models:
        print_colored("没有启用的模型", "red")
        return
    
    # 按成本排序
    sorted_models = sorted(
        enabled_models.items(),
        key=lambda x: x[1].get("cost_weight", 1.0)
    )
    
    print_colored("成本从低到高排序:", "yellow")
    for i, (model_id, config) in enumerate(sorted_models, 1):
        cost = config.get("cost_weight", 1.0)
        cost_bar = "█" * int(cost * 10)
        
        type_icon = "🖥️ " if config.get("type") == "local" else "☁️ "
        priority_icon = "⭐" if config.get("model_priority") == "max" else "⚪"
        
        print(f"  {i}. {type_icon} {model_id}")
        print(f"     成本: {cost:.2f} {cost_bar}")
        print(f"     优先级: {priority_icon} {config.get('model_priority', 'N/A')}")
    
    # 推荐模型
    print_colored("\n🎯 推荐使用:", "green")
    print(f"  简单任务: {model_manager.get_cost_effective_model('simple')}")
    print(f"  复杂任务: {model_manager.get_cost_effective_model('complex')}")

def command_test(args):
    """测试路由"""
    prompt = args.prompt
    if not prompt:
        print_colored("错误: 需要提供测试文本", "red")
        return
    
    print_colored(f"\n🧪 路由测试: '{prompt}'", "cyan")
    print("=" * 60)
    
    # 导入路由器
    try:
        from smart_router import router
    except ImportError:
        print_colored("错误: 无法导入路由器", "red")
        return
    
    result = router.route_request(prompt)
    
    print(f"请求: {result.get('prompt_length', 0)} 字符")
    print(f"复杂度: {result.get('complexity', 'unknown')}")
    print(f"判断方法: {result.get('method', 'unknown')}")
    print(f"推荐模型: {result.get('model', 'unknown')}")
    print(f"模型类型: {result.get('model_type', 'unknown')}")
    print(f"成本权重: {result.get('cost_weight', 1.0):.2f}")
    print(f"理由: {result.get('reason', 'N/A')}")
    print(f"成本优化: {'✅ 是' if result.get('cost_optimized', False) else '❌ 否'}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="模型管理CLI工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s list                    # 列出所有模型
  %(prog)s show <model_id>         # 显示模型详情
  %(prog)s detect --update         # 检测并更新模型
  %(prog)s add <id> <type> <name>  # 添加新模型
  %(prog)s remove <model_id>       # 删除模型
  %(prog)s cost                    # 成本分析
  %(prog)s test "现在几点了"       # 测试路由
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有模型")
    list_parser.set_defaults(func=command_list)
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示模型详情")
    show_parser.add_argument("model_id", help="模型ID")
    show_parser.set_defaults(func=command_show)
    
    # detect 命令
    detect_parser = subparsers.add_parser("detect", help="检测可用模型")
    detect_parser.add_argument("--update", action="store_true", help="检测后更新配置")
    detect_parser.set_defaults(func=command_detect)
    
    # enable 命令
    enable_parser = subparsers.add_parser("enable", help="启用模型")
    enable_parser.add_argument("model_id", help="模型ID")
    enable_parser.set_defaults(func=command_enable)
    
    # disable 命令
    disable_parser = subparsers.add_parser("disable", help="禁用模型")
    disable_parser.add_argument("model_id", help="模型ID")
    disable_parser.set_defaults(func=command_disable)
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新模型")
    add_parser.add_argument("model_id", help="模型ID")
    add_parser.add_argument("type", choices=["local", "cloud"], help="模型类型")
    add_parser.add_argument("name", help="模型名称")
    add_parser.add_argument("--priority", choices=["normal", "max"], default="normal", help="模型优先级")
    add_parser.add_argument("--description", help="模型描述")
    add_parser.add_argument("--cost-weight", type=float, help="成本权重")
    add_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的模型")
    add_parser.set_defaults(func=command_add)
    
    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="删除模型")
    remove_parser.add_argument("model_id", help="模型ID")
    remove_parser.add_argument("--force", action="store_true", help="强制删除")
    remove_parser.set_defaults(func=command_remove)
    
    # cost 命令
    cost_parser = subparsers.add_parser("cost", help="成本优化分析")
    cost_parser.set_defaults(func=command_cost)
    
    # test 命令
    test_parser = subparsers.add_parser("test", help="测试路由")
    test_parser.add_argument("prompt", help="测试文本")
    test_parser.set_defaults(func=command_test)
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # 执行命令
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
    except Exception as e:
        print_colored(f"错误: {e}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()