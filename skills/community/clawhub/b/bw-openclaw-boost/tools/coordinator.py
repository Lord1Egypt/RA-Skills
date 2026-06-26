#!/usr/bin/env python3
"""
Multi-Agent Coordinator
协调多个 Agent 工作

功能：
1. 接收用户任务描述
2. 分析任务类型，分发到合适的 Agent
3. 收集结果，汇总返回给用户

Agent 列表：
- main: 谷宝主助手
- graphic-designer: 美工设计
- video-production: 影视制作
- bid-quotation: 投标报价
"""

import os
import json
import subprocess
import time
from pathlib import Path

# 技能本地目录
SKILL_ROOT = Path(__file__).parent.parent
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

MEMORY_ROOT = SKILL_ROOT / "memory"
COORDINATOR_LOG = MEMORY_ROOT / "logs" / "coordinator" / "tasks.json"

# Agent 能力定义
AGENT_CAPABILITIES = {
    "graphic-designer": {
        "keywords": ["海报", "设计", "图片", "logo", "banner", "封面", "画册", "宣传单", "名片", "包装", "PS", "修图", "美工", "设计图"],
        "description": "美工设计",
        "channel": "feishu"  # 或其他
    },
    "video-production": {
        "keywords": ["视频", "剪辑", "影片", "宣传片", "短视频", "AE", "PR", "动画", "特效", "字幕", "配音", "影视"],
        "description": "影视制作",
        "channel": "feishu"
    },
    "bid-quotation": {
        "keywords": ["投标", "报价", "标书", "竞标", "招标", "预算", "报价单", "方案"],
        "description": "投标报价",
        "channel": "feishu"
    },
    "main": {
        "keywords": ["写", "查", "搜索", "整理", "总结", "翻译", "对话", "聊天", "日程", "提醒"],
        "description": "主助手（谷宝）",
        "channel": "weixin"
    }
}


@dataclass
class Task:
    """任务"""
    id: str
    description: str
    target_agent: str
    status: str  # pending / running / completed / failed
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None


class Coordinator:
    """多 Agent 协调器"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """加载任务历史"""
        COORDINATOR_LOG.parent.mkdir(parents=True, exist_ok=True)
        if COORDINATOR_LOG.exists():
            try:
                data = json.loads(COORDINATOR_LOG.read_text())
                self.tasks = {t["id"]: Task(**t) for t in data.get("tasks", [])}
            except:
                pass
    
    def _save_tasks(self):
        """保存任务"""
        data = {"tasks": [vars(t) for t in self.tasks.values()]}
        COORDINATOR_LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def analyze_task(self, description: str) -> List[str]:
        """
        分析任务，返回需要的 Agent 列表
        """
        description_lower = description.lower()
        matched_agents = []
        
        for agent_id, caps in AGENT_CAPABILITIES.items():
            score = 0
            for keyword in caps["keywords"]:
                if keyword.lower() in description_lower:
                    score += 1
            if score > 0:
                matched_agents.append((agent_id, score))
        
        # 按匹配分数排序
        matched_agents.sort(key=lambda x: x[1], reverse=True)
        
        # 如果没有匹配，默认给 main
        if not matched_agents:
            return ["main"]
        
        return [agent_id for agent_id, score in matched_agents]
    
    def create_task(self, description: str, target_agent: Optional[str] = None) -> Task:
        """创建任务"""
        import uuid
        
        # 分析任务，确定目标 Agent
        if not target_agent:
            target_agents = self.analyze_task(description)
            target_agent = target_agents[0]  # 取最匹配的
        
        task_id = str(uuid.uuid4())[:8]
        task = Task(
            id=task_id,
            description=description,
            target_agent=target_agent,
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return task
    
    def dispatch_task(self, task: Task) -> bool:
        """
        分发任务到目标 Agent（仅本地记录，不发送消息）
        
        注意：此版本仅做本地任务记录，不实际发送消息到其他 Agent。
        如需启用消息发送功能，请自行配置 openclaw sessions send。
        """
        try:
            task.status = "running"
            self._save_tasks()
            
            # 仅做本地记录，不发送实际消息
            task.status = "pending"
            task.result = "[本地记录模式] 任务已记录，等待手动处理"
            self._save_tasks()
            return True
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now().isoformat()
            self._save_tasks()
            return False
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """获取任务状态"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """列出任务"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)
    
    def format_task_list(self, tasks: List[Task]) -> str:
        """格式化任务列表"""
        if not tasks:
            return "暂无任务"
        
        lines = ["=" * 50, "📋 任务列表", "=" * 50, ""]
        
        for t in tasks[:10]:
            status_emoji = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅",
                "failed": "❌"
            }.get(t.status, "❓")
            
            lines.append(f"{status_emoji} [{t.id}] {t.target_agent}")
            lines.append(f"   描述: {t.description[:50]}...")
            lines.append(f"   时间: {t.created_at[:19]}")
            if t.completed_at:
                lines.append(f"   完成: {t.completed_at[:19]}")
            if t.error:
                lines.append(f"   错误: {t.error[:50]}")
            lines.append("")
        
        return "\n".join(lines)


def get_coordinator() -> Coordinator:
    return Coordinator()


if __name__ == "__main__":
    import sys
    
    coordinator = get_coordinator()
    
    if len(sys.argv) < 2:
        print(coordinator.format_task_list(coordinator.list_tasks()))
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        print(coordinator.format_task_list(coordinator.list_tasks()))
    
    elif cmd == "pending":
        print(coordinator.format_task_list(coordinator.list_tasks("pending")))
    
    elif cmd == "create" and len(sys.argv) >= 3:
        description = sys.argv[2]
        target = sys.argv[3] if len(sys.argv) > 3 else None
        
        task = coordinator.create_task(description, target)
        print(f"✅ 任务已创建: [{task.id}] -> {task.target_agent}")
        print(f"   描述: {task.description}")
        
        # 自动分发
        print("\n正在分发任务...")
        if coordinator.dispatch_task(task):
            print("✅ 任务分发成功")
        else:
            print(f"❌ 任务分发失败: {task.error}")
    
    elif cmd == "status" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        task = coordinator.get_task_status(task_id)
        if task:
            print(f"任务: {task.description}")
            print(f"状态: {task.status}")
            print(f"目标: {task.target_agent}")
            if task.result:
                print(f"结果: {task.result[:200]}")
            if task.error:
                print(f"错误: {task.error}")
        else:
            print(f"未找到任务: {task_id}")
    
    elif cmd == "analyze" and len(sys.argv) >= 3:
        description = " ".join(sys.argv[2:])
        agents = coordinator.analyze_task(description)
        print(f"分析结果: {agents}")
        for agent in agents:
            print(f"  - {agent}: {AGENT_CAPABILITIES.get(agent, {}).get('description', '')}")
    
    else:
        print("用法:")
        print("  coordinator.py list                    # 列出所有任务")
        print("  coordinator.py pending                # 列出待处理任务")
        print("  coordinator.py create <描述> [agent]  # 创建任务")
        print("  coordinator.py status <id>            # 查看任务状态")
        print("  coordinator.py analyze <描述>         # 分析任务类型")
