"""认知力增强引擎 — 基础功能测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine import CognitiveEnhancer

def test_basic():
    brain = CognitiveEnhancer(long_term_capacity=10)
    
    # 测试记忆
    brain.memorize("Python is a programming language.", importance=0.8)
    brain.memorize("Lists are mutable in Python.", importance=0.7)
    
    # 测试检索
    results = brain.recall("Python programming", top_k=2)
    assert len(results) > 0, "Should find memories"
    print(f"[PASS] Recall: found {len(results)} results")
    
    # 测试感知
    brain.perceive("User asked about Python")
    status = brain.get_status()
    assert status['working_memories'] > 0, "Working memory should have entries"
    print(f"[PASS] Working memory: {status['working_memories']} entries")
    
    # 测试规划
    plan = brain.plan("Calculate 15 + 27")
    assert len(plan) > 0, "Should produce a plan"
    print(f"[PASS] Planning: {len(plan)} steps")
    
    # 测试推理
    answer = brain.reason("What programming language uses lists?")
    assert len(answer) > 0, "Should produce an answer"
    print(f"[PASS] Reasoning: produced answer")
    
    # 测试任务执行
    result = brain.execute_task("Calculate 15 + 27")
    assert result.get('success', False), "Task should complete"
    print(f"[PASS] Execute task: success={result.get('success')}")
    
    # 测试反思
    suggestions = brain.reflect()
    print(f"[PASS] Reflection: {len(suggestions)} suggestions")
    
    # 测试状态
    status = brain.get_status()
    print(f"[PASS] Status: {status['long_term_memories']} memories, "
          f"{status['working_memories']} working, "
          f"{status['tasks_executed']} tasks")
    
    print("\n=== ALL TESTS PASSED ===")

if __name__ == '__main__':
    test_basic()
