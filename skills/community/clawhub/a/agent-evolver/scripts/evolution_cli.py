#!/usr/bin/env python3
"""
Evolution CLI - 命令行工具
提供易用的命令行接口来操作自进化引擎
"""

import argparse
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evolver_core import EvolutionManager, ExperienceStore, LLMIntegration
from experience_vectorizer import ExperienceVectorizer


def cmd_evolve(args):
    """执行进化周期"""
    evolver = EvolutionManager(agent_id=args.agent_id)
    
    result = evolver.run_evolution(
        task_input=args.input,
        task_type=args.task_type
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"任务类型: {result['task_type']}")
        print(f"执行状态: {result['execute_result']['status']}")
        print(f"策略更新: {'是' if result['strategy_updated'] else '否'}")
        
        if result['experience'].get('solution'):
            print(f"\n解决方案: {result['experience']['solution']}")


def cmd_analyze(args):
    """分析执行结果"""
    llm = LLMIntegration()
    store = ExperienceStore()
    
    if args.result_file:
        with open(args.result_file, 'r') as f:
            result_data = json.load(f)
    else:
        result_data = {"error": args.result}
    
    error_info = {
        "error_type": result_data.get("error", {}).get("type", "Unknown"),
        "error_message": result_data.get("error", {}).get("message", args.result),
        "task_type": result_data.get("task_type", "general"),
        "trigger_input": result_data.get("input", "")
    }
    
    analysis = llm.analyze_error(error_info, result_data.get("context", {}))
    
    if args.json:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print("=== 错误分析 ===")
        print(f"原因: {analysis['analysis']}")
        print(f"\n解决方案: {analysis['solution']}")
        print(f"\n策略优化: {analysis['strategy_delta']}")
        print(f"\n关键词: {', '.join(analysis['keywords'])}")


def cmd_search(args):
    """搜索相似经验"""
    store = ExperienceStore()
    vectorizer = ExperienceVectorizer()
    
    if vectorizer.vector_store:
        results = vectorizer.search_similar_experiences(args.query, args.limit)
        
        if args.json:
            output = []
            for r in results:
                exp = store.get_experience(r.experience_id)
                if exp:
                    output.append({
                        "similarity": r.similarity,
                        "experience": exp.__dict__ if hasattr(exp, '__dict__') else exp
                    })
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(f"找到 {len(results)} 条相似经验:\n")
            for i, r in enumerate(results, 1):
                exp = store.get_experience(r.experience_id)
                if exp:
                    print(f"{i}. 相似度: {r.similarity:.2%}")
                    print(f"   错误类型: {exp.error_type}")
                    print(f"   解决方案: {exp.solution}")
                    print()
    else:
        experiences = store.query_experiences(limit=args.limit * 2)
        
        results = []
        query_lower = args.query.lower()
        
        for exp in experiences:
            score = 0
            for keyword in exp.keywords:
                if keyword.lower() in query_lower:
                    score += 1
            
            if exp.error_message and exp.error_message.lower() in query_lower:
                score += 2
            
            if score > 0:
                results.append({
                    "experience": exp,
                    "similarity": score / (len(exp.keywords) + 2)
                })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        results = results[:args.limit]
        
        if args.json:
            output = []
            for r in results:
                output.append({
                    "similarity": r["similarity"],
                    "experience": r["experience"].__dict__ if hasattr(r["experience"], '__dict__') else r["experience"]
                })
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(f"找到 {len(results)} 条相似经验:\n")
            for i, r in enumerate(results, 1):
                exp = r["experience"]
                print(f"{i}. 相似度: {r['similarity']:.2%}")
                print(f"   错误类型: {exp.error_type}")
                print(f"   解决方案: {exp.solution}")
                print()


def cmd_stats(args):
    """查看进化统计"""
    store = ExperienceStore()
    vectorizer = ExperienceVectorizer()
    
    stats = store.get_stats(args.agent_id)
    vector_stats = vectorizer.get_collection_stats()
    
    result = {
        **stats,
        "vector_search": vector_stats
    }
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=== 进化统计 ===\n")
        print(f"总经验数: {stats['total_experiences']}")
        print(f"成功次数: {stats['success_count']}")
        print(f"失败次数: {stats['failed_count']}")
        print(f"改进次数: {stats['improved_count']}")
        print(f"成功率: {stats['success_rate']:.2%}")
        print(f"改进率: {stats['improvement_rate']:.2%}")
        print(f"\n任务类型: {', '.join(stats['task_types'])}")
        print(f"错误类型: {', '.join(stats['error_types'])}")
        print(f"\n向量搜索: {'已启用' if vector_stats['enabled'] else '未启用'}")
        if vector_stats['enabled']:
            print(f"向量数量: {vector_stats['count']}")


def cmd_history(args):
    """查看进化历史"""
    store = ExperienceStore()
    
    experiences = store.query_experiences(
        task_type=args.task_type,
        error_type=args.error_type,
        limit=args.limit
    )
    
    if args.json:
        output = [exp.__dict__ if hasattr(exp, '__dict__') else exp for exp in experiences]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"=== 进化历史 (最近 {len(experiences)} 条) ===\n")
        
        for i, exp in enumerate(experiences, 1):
            status_icon = "✅" if exp.status == "success" else "❌" if exp.status == "failed" else "🔄"
            
            print(f"{i}. {status_icon} [{exp.task_type}] {exp.error_type}")
            print(f"   时间: {exp.created_at}")
            print(f"   解决方案: {exp.solution[:50]}..." if len(exp.solution) > 50 else f"   解决方案: {exp.solution}")
            print()


def cmd_export(args):
    """导出经验库"""
    store = ExperienceStore()
    
    experiences = store.query_experiences(limit=10000)
    
    output = {
        "export_time": __import__('datetime').datetime.now().isoformat(),
        "stats": store.get_stats(),
        "experiences": [exp.__dict__ if hasattr(exp, '__dict__') else exp for exp in experiences]
    }
    
    with open(args.output, 'w') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"已导出 {len(experiences)} 条经验到 {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="Agent Evolver CLI - AI Agent 自进化引擎命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    evolve_parser = subparsers.add_parser("evolve", help="执行进化周期")
    evolve_parser.add_argument("input", help="任务输入")
    evolve_parser.add_argument("--agent-id", default="default", help="Agent ID")
    evolve_parser.add_argument("--task-type", default="general", help="任务类型")
    evolve_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    analyze_parser = subparsers.add_parser("analyze", help="分析执行结果")
    analyze_parser.add_argument("result", nargs="?", help="执行结果")
    analyze_parser.add_argument("--result-file", help="结果文件路径")
    analyze_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    search_parser = subparsers.add_parser("search", help="搜索相似经验")
    search_parser.add_argument("query", help="搜索查询")
    search_parser.add_argument("--limit", type=int, default=5, help="结果数量")
    search_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    stats_parser = subparsers.add_parser("stats", help="查看进化统计")
    stats_parser.add_argument("--agent-id", help="Agent ID")
    stats_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    history_parser = subparsers.add_parser("history", help="查看进化历史")
    history_parser.add_argument("--limit", type=int, default=10, help="显示数量")
    history_parser.add_argument("--task-type", help="任务类型过滤")
    history_parser.add_argument("--error-type", help="错误类型过滤")
    history_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    export_parser = subparsers.add_parser("export", help="导出经验库")
    export_parser.add_argument("output", help="输出文件路径")
    
    args = parser.parse_args()
    
    if args.command == "evolve":
        cmd_evolve(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "history":
        cmd_history(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
