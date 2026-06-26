#!/usr/bin/env python3
"""
FocusMind CLI 入口
提供统一的命令行接口
"""

import argparse
import json
import sys
import os

# 添加当前目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from scripts.check_context import analyze_context_health, format_health_report, HealthChecker
from scripts.summarize import generate_summary, format_summary_markdown
from scripts.extract_goals import extract_goals, format_goals_markdown
from scripts.cache import get_cache
from scripts.stats import get_tracker, PerformanceTracker, timer
from scripts.export import export_report


def load_context_from_file(filepath: str) -> str:
    """从文件加载上下文"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_context_from_stdin() -> str:
    """从 stdin 加载上下文"""
    return sys.stdin.read()


def load_messages_from_file(filepath: str):
    """从 JSON 文件加载消息列表"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'messages' in data:
            return data['messages']
        else:
            return [data]


def get_context(args) -> str:
    """获取上下文"""
    if args.file:
        # 尝试 JSON 格式
        if args.file.endswith('.json'):
            try:
                return load_messages_from_file(args.file)
            except:
                return load_context_from_file(args.file)
        return load_context_from_file(args.file)
    elif not sys.stdin.isatty():
        return load_context_from_stdin()
    else:
        # 默认测试上下文
        return """
        用户: 请帮我开发一个 Python 博客网站
        Agent: 好的，我来帮你开发博客网站。先确定一下需求。
        用户: 需要用户登录、文章发布、评论功能，还有标签系统
        Agent: 明白了。我们需要：1) 用户系统 2) 文章CRUD 3) 评论系统 4) 标签管理
        用户: 使用 Flask 框架和 SQLite 数据库
        Agent: 好的，我已创建项目结构。实现了用户模型和认证功能。
        用户: 很好，接下来实现文章发布功能
        Agent: 正在实现文章CRUD，还没完成评论功能
        """ * 5


def cmd_health(args):
    """健康度检查命令"""
    context = get_context(args)
    health = analyze_context_health(context, threshold=args.threshold)
    
    if args.json:
        print(json.dumps(health, ensure_ascii=False, indent=2))
    else:
        print(format_health_report(health))
    
    return 0 if health["level"] != "red" else 1


def cmd_summarize(args):
    """生成摘要命令"""
    context = get_context(args)
    summary = generate_summary(context, style=args.style)
    
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_summary_markdown(summary))
    
    return 0


def cmd_goals(args):
    """目标提取命令"""
    context = get_context(args)
    goals = extract_goals(context)
    
    if args.json:
        print(json.dumps(goals, ensure_ascii=False, indent=2))
    else:
        print(format_goals_markdown(goals))
    
    return 0


def cmd_all(args):
    """完整分析命令"""
    context = get_context(args)
    
    tracker = get_tracker()
    
    # 健康度检查
    with timer(tracker, "health_check"):
        health = analyze_context_health(context, threshold=args.threshold)
    
    # 生成摘要
    with timer(tracker, "summarize"):
        summary = generate_summary(context, style=args.style)
    
    # 提取目标
    with timer(tracker, "extract_goals"):
        goals = extract_goals(context)
    
    output = f"""
{'='*50}
🧠 FocusMind 完整分析报告
{'='*50}

{format_health_report(health)}

{'-'*50}

{format_summary_markdown(summary)}

{'-'*50}

{format_goals_markdown(goals)}
"""
    
    print(output)
    
    if args.json:
        print("\n--- JSON (完整) ---")
        print(json.dumps({
            "health": health,
            "summary": summary,
            "goals": goals
        }, ensure_ascii=False, indent=2))
    
    return 0


def cmd_stats(args):
    """统计命令"""
    cache = get_cache()
    tracker = get_tracker()
    
    print("=== 缓存统计 ===")
    print(json.dumps(cache.get_stats(), ensure_ascii=False, indent=2))
    
    print("\n=== 性能统计 ===")
    print(json.dumps(tracker.get_summary(), ensure_ascii=False, indent=2))
    
    if args.detailed:
        tracker.print_report()
    
    return 0


def cmd_clear_cache(args):
    """清除缓存命令"""
    cache = get_cache()
    cache.clear()
    print("缓存已清除")
    return 0


def cmd_export(args):
    """导出报告命令"""
    context = get_context(args)
    
    # 生成数据
    health = analyze_context_health(context, threshold=args.threshold)
    summary = generate_summary(context, style=args.style)
    goals = extract_goals(context)
    
    # 导出
    return 0 if export_report(health, summary, goals, args.output, args.format) else 1


def main():
    parser = argparse.ArgumentParser(
        description="FocusMind - Agent 脑雾清除技能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python focus.py health                    # 检查上下文健康度
  python focus.py health --json             # JSON 格式输出
  python focus.py health --threshold 5000   # 自定义阈值
  python focus.py summarize                 # 生成摘要
  python focus.py summarize -s executive  # 执行摘要风格
  python focus.py goals                     # 提取目标
  python focus.py all                       # 完整分析
  python focus.py stats                     # 查看统计
  cat context.txt | python focus.py health  # 从文件读取
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # health 命令
    health_parser = subparsers.add_parser("health", help="检查上下文健康度")
    health_parser.add_argument("-f", "--file", help="从文件读取上下文")
    health_parser.add_argument("-t", "--threshold", type=int, default=10000, help="token 阈值")
    health_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    # summarize 命令
    summarize_parser = subparsers.add_parser("summarize", help="生成上下文摘要")
    summarize_parser.add_argument("-f", "--file", help="从文件读取上下文")
    summarize_parser.add_argument("-s", "--style", choices=["structured", "concise", "bullet", "executive"], default="structured", help="摘要风格")
    summarize_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    # goals 命令
    goals_parser = subparsers.add_parser("goals", help="提取核心目标")
    goals_parser.add_argument("-f", "--file", help="从文件读取上下文")
    goals_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    # all 命令
    all_parser = subparsers.add_parser("all", help="完整分析")
    all_parser.add_argument("-f", "--file", help="从文件读取上下文")
    all_parser.add_argument("-t", "--threshold", type=int, default=10000, help="token 阈值")
    all_parser.add_argument("-s", "--style", choices=["structured", "concise", "bullet", "executive"], default="structured", help="摘要风格")
    all_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看统计信息")
    stats_parser.add_argument("-d", "--detailed", action="store_true", help="详细报告")
    
    # cache 命令
    cache_parser = subparsers.add_parser("cache", help="缓存管理")
    cache_parser.add_argument("--clear", action="store_true", help="清除缓存")
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="导出报告")
    export_parser.add_argument("-f", "--file", help="从文件读取上下文")
    export_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    export_parser.add_argument("-t", "--threshold", type=int, default=10000, help="token 阈值")
    export_parser.add_argument("-s", "--style", choices=["structured", "concise", "bullet", "executive"], default="structured", help="摘要风格")
    export_parser.add_argument("-F", "--format", choices=["markdown", "json", "html"], default=None, help="导出格式")
    
    args = parser.parse_args()
    
    # 处理缓存命令
    if args.command == "cache":
        return cmd_clear_cache(args)
    
    # 处理导出命令
    if args.command == "export":
        return cmd_export(args)
    
    # 处理 stats 命令
    if args.command == "stats":
        return cmd_stats(args)
    
    # 其他命令
    if args.command == "health":
        return cmd_health(args)
    elif args.command == "summarize":
        return cmd_summarize(args)
    elif args.command == "goals":
        return cmd_goals(args)
    elif args.command == "all":
        return cmd_all(args)
    else:
        # 默认执行 health
        return cmd_health(args)


if __name__ == "__main__":
    sys.exit(main())
