"""
简单的AI员工示例
展示如何创建一个基础的AI员工
"""

import json
from typing import Dict, List, Any


class SimpleAIEmployee:
    """简单的AI员工实现"""

    def __init__(self, name: str, role: str, version: str = "v1.0"):
        """
        初始化AI员工

        Args:
            name: AI员工名称
            role: 角色描述
            version: 版本号
        """
        self.name = name
        self.role = role
        self.version = version
        self.state = {}
        self.memory = []
        self.tools = []

    def load_prompt(self) -> str:
        """加载提示词"""
        prompt_file = f"prompts/{self.name}/{self.version}.md"
        try:
            with open(prompt_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"你是一个{self.role}，请协助完成任务。"

    def think(self, task: Dict[str, Any]) -> List[str]:
        """
        思考和规划

        Args:
            task: 任务字典

        Returns:
            行动计划列表
        """
        # 这里应该调用Claude API进行思考
        # 为了示例，我们返回一个简单的计划
        return [
            "分析任务需求",
            "收集必要信息",
            "执行任务",
            "验证结果"
        ]

    def work(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行任务

        Args:
            task: 任务字典

        Returns:
            执行结果
        """
        print(f"[{self.name}] 开始执行任务: {task.get('description', '无描述')}")

        # 1. 思考和规划
        plan = self.think(task)
        print(f"[{self.name}] 计划: {' → '.join(plan)}")

        # 2. 执行任务（这里应该调用实际的处理逻辑）
        result = {
            "status": "success",
            "employee": self.name,
            "task_id": task.get("id"),
            "output": f"任务完成 by {self.name}",
            "metadata": {
                "version": self.version,
                "timestamp": "2024-03-09T10:00:00"
            }
        }

        # 3. 记录到记忆中
        self.memory.append({
            "task": task,
            "result": result,
            "timestamp": "2024-03-09T10:00:00"
        })

        print(f"[{self.name}] 任务完成")
        return result

    def learn(self, experience: Dict[str, Any]):
        """
        从经验中学习

        Args:
            experience: 经验数据
        """
        self.memory.append(experience)

        # 保持记忆在合理大小
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]

    def save_state(self, state_file: str):
        """
        保存状态

        Args:
            state_file: 状态文件路径
        """
        with open(state_file, 'w') as f:
            json.dump({
                "name": self.name,
                "role": self.role,
                "version": self.version,
                "state": self.state,
                "memory": self.memory[-10:]  # 只保存最近10条
            }, f, indent=2)

    def load_state(self, state_file: str):
        """
        加载状态

        Args:
            state_file: 状态文件路径
        """
        try:
            with open(state_file, 'r') as f:
                data = json.load(f)
                self.state = data.get("state", {})
                self.memory = data.get("memory", [])
        except FileNotFoundError:
            print(f"[{self.name}] 未找到状态文件，使用初始状态")


# 使用示例
if __name__ == "__main__":
    # 创建一个市场研究AI员工
    market_researcher = SimpleAIEmployee(
        name="market_researcher",
        role="市场研究专家",
        version="v1.0"
    )

    # 执行一个任务
    task = {
        "id": "task_001",
        "description": "分析GitHub上的自动化测试工具需求",
        "type": "market_research"
    }

    result = market_researcher.work(task)
    print(f"\n结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

    # 保存状态
    market_researcher.save_state("shared/market_researcher_state.json")
    print(f"\n状态已保存")
