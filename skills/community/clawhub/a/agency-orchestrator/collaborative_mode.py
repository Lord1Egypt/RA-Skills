#!/usr/bin/env python3
"""
Agency Orchestrator - 协作模式
集成多 Agent 协作能力
"""

import sys
sys.path.insert(0, '/Users/ghq/.openclaw/integration')
sys.path.insert(0, '/Users/ghq/.openclaw/evolution/week1')

from collaborative_agents import CollaborativeAgentSystem

class CollaborativeOrchestrator:
    """协作式编排器"""
    
    def __init__(self):
        self.system = CollaborativeAgentSystem()
        print("✅ 协作式编排器已初始化")
    
    def coordinate(self, task: str) -> dict:
        """
        协调多 Agent 完成任务
        
        Args:
            task: 任务描述
        
        Returns:
            执行结果
        """
        print(f"\n🎯 协调任务：{task}")
        print("=" * 60)
        
        # 使用协作系统执行
        result = self.system.execute_task(task)
        
        # 格式化输出
        print("\n" + "=" * 60)
        print("📊 执行报告:")
        print(f"  任务：{result['task']}")
        print(f"  分解：{result['subtasks_count']} 个子任务")
        print(f"  参与 Agent: {result['agents_involved']} 个")
        print(f"  执行时间：{result['execution_time']:.2f}秒")
        print(f"  质量评分：{result['final_confidence']:.2f}")
        
        return result

# ClawX 工具接口
def clawx_execute(task: str) -> dict:
    """ClawX 工具执行接口"""
    orchestrator = CollaborativeOrchestrator()
    return orchestrator.coordinate(task)

# 测试
if __name__ == '__main__':
    orchestrator = CollaborativeOrchestrator()
    
    test_tasks = [
        "开发一个产品官网",
        "制作一个产品演示 PPT",
        "测试这个系统",
    ]
    
    for task in test_tasks:
        result = orchestrator.coordinate(task)
        print("\n" + "=" * 60 + "\n")
