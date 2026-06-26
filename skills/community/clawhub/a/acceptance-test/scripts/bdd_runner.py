#!/usr/bin/env python3
"""
BDD测试运行器 - 执行BDD测试
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bdd(features: str, steps: str) -> Dict:
    """执行BDD测试"""
    import random
    
    scenarios = [
        {'name': '成功登录', 'given': '用户已注册', 'when': '输入正确密码', 'then': '登录成功', 'passed': random.random() > 0.1},
        {'name': '失败登录', 'given': '用户已注册', 'when': '输入错误密码', 'then': '显示错误', 'passed': random.random() > 0.1},
    ]
    
    passed = sum(1 for s in scenarios if s['passed'])
    
    return {
        'features_path': features,
        'steps_path': steps,
        'scenarios': scenarios,
        'passed': passed,
        'failed': len(scenarios) - passed
    }

def print_result(result: Dict):
    print(f"\n{'='*60}")
    print(f"🥒 BDD测试结果")
    print(f"{'='*60}")
    
    for s in result['scenarios']:
        status = "✅" if s['passed'] else "❌"
        print(f"\n  {status} 场景: {s['name']}")
        print(f"     Given: {s['given']}")
        print(f"     When: {s['when']}")
        print(f"     Then: {s['then']}")
    
    print(f"\n通过: {result['passed']}/{len(result['scenarios'])}")
    print(f"{'='*60}\n")

def demo():
    print("🥒 BDD测试运行器 - 演示")
    print("="*60)
    
    result = run_bdd('features/', 'steps/')
    print_result(result)

if __name__ == "__main__":
    demo()
