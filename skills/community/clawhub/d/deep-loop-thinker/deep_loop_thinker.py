#!/usr/bin/env python3
"""
Deep Loop Thinker v2.0 - 多轮深度思考技能
借鉴OpenMythos循环推理架构

使用方式：
python deep_loop_thinker.py "你的问题" [轮次]
"""

import sys
import json
from datetime import datetime

def think_round(question, round_num):
    """每轮思考"""
    prompts = {
        1: ("直觉捕捉", """
- 第一时间想到什么？{q[:30]}...
- 表面原因是什么？
- 情绪反应是什么？
        """),
        2: ("利益分析", """
- 谁会从中受益？
- 谁会因此受损？
- 各方核心诉求是什么？
        """),
        3: ("风险挖掘", """
- 最坏情况是什么？
- 有什么隐藏成本？
- 3年后回头看，这还重要吗？
        """),
        4: ("本质洞察", """
- 根本原因是什么？（5Why追问）
- 这反映了什么模式/规律？
- 本质问题是什么？
        """),
        5: ("行动设计", """
- 具体的第一步是什么？
- 资源和时间需求？
- 如何衡量成功？
- Plan B是什么？
        """),
        6: ("反思验证", """
- 我的假设可靠吗？
- 我可能被什么偏见影响？
- 如果错了，哪里可能错？
        """)
    }
    
    name, prompt = prompts.get(round_num, ("完成", "思考完成"))
    return f"【{name}】\n{prompt}".format(q=question)

def deep_loop_think(question, rounds=4):
    """主函数：多轮深度思考"""
    
    print("=" * 60)
    print(f"【深度思考报告】")
    print(f"问题：{question}")
    print("=" * 60)
    
    results = []
    
    # 确定实际轮次（最多6轮）
    actual_rounds = min(rounds, 6)
    
    for i in range(1, actual_rounds + 1):
        print(f"\n{'─' * 60}")
        print(f"【第{i}轮】")
        print(f"{'─' * 60}")
        
        result = think_round(question, i)
        print(result)
        results.append(result)
    
    # 综合输出
    print(f"\n{'═' * 60}")
    print("【综合输出】")
    print(f"{'═' * 60}")
    
    if len(results) >= 1:
        print(f"▌直觉反应：{results[0][:50]}...")
    if len(results) >= 4:
        print(f"▌本质洞察：找到了{len(results)-1}个关键角度")
    if len(results) >= 5:
        print(f"▌行动计划：制定{len(results)-1}步计划")
    
    print(f"▌置信度：{'高' if len(results) >= 4 else '中' if len(results) >= 2 else '低'}")
    print(f"▌生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═' * 60}")
    
    return results

def interactive_mode():
    """交互模式"""
    print("=" * 60)
    print("Deep Loop Thinker v2.0 - 多轮深度思考")
    print("=" * 60)
    
    question = input("\n请输入你的问题：")
    
    print("\n选择思考深度：")
    print("1. 快速思考（1-2轮）")
    print("2. 标准思考（3-4轮）")
    print("3. 深度思考（5-6轮）")
    
    choice = input("\n请选择（1/2/3）：").strip()
    
    rounds_map = {"1": 2, "2": 4, "3": 6}
    rounds = rounds_map.get(choice, 4)
    
    deep_loop_think(question, rounds)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = sys.argv[1]
        rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        deep_loop_think(question, rounds)
    else:
        interactive_mode()
