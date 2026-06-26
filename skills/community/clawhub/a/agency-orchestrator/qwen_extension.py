#!/usr/bin/env python3
"""
Qwen-Code 扩展 - Agency Orchestrator 集成
"""

import sys
import json
from agency_orchestrator import AgencyOrchestrator

def main():
    if len(sys.argv) < 2:
        print("用法：qwen agency <command> [args]")
        print("命令:")
        print("  execute <任务>  - 执行任务")
        print("  list [分类]     - 列出 Agent")
        print("  status          - 系统状态")
        return
    
    command = sys.argv[1]
    orchestrator = AgencyOrchestrator()
    
    if command == "execute":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "未指定任务"
        result = orchestrator.coordinate(task)
        print(f"\n🎯 任务：{result['task']}")
        print(f"📊 分析：{result['analysis']['needed_categories']}")
        print(f"🤖 已选择 {result['agent_count']} 个 Agent:")
        for agent in result['selected_agents']:
            print(f"   - {agent['name']} ({agent['category']})")
        print(f"\n✅ {result['message']}")
    
    elif command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        result = orchestrator.get_agent_list(category)
        if category:
            print(f"\n📂 分类：{category}")
            print(f"📊 Agent 数量：{result['count']}")
            for agent in result['agents']:
                print(f"   - {agent['name']}")
        else:
            print(f"\n📊 总 Agent 数：{result['total']}")
            print("\n📂 分类统计:")
            for cat, count in result['categories'].items():
                print(f"   {cat}: {count} 个")
    
    elif command == "status":
        print("\n🧬 Agency Agents ZH 系统状态")
        print("=" * 50)
        print(f"📊 总 Agent 数：{sum(len(v) for v in orchestrator.agents.values())}")
        print(f"📂 分类数：{len(orchestrator.agents)}")
        print(f"📝 日志文件：~/.openclaw/agency-agents-zh/logs/")
        print("=" * 50)

if __name__ == "__main__":
    main()
