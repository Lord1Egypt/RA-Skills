#!/usr/bin/env python3
"""
Coordinator+Worker协作测试脚本（简化版）

功能：
1. 模拟Coordinator分配任务
2. 模拟Worker执行任务
3. 验证精确指令协议
4. 测试并行/串行执行策略

注意：这是简化版测试脚本，完整测试请参考参考资料中的测试场景文档。
"""

import json
import time
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class TaskType(Enum):
    """任务类型枚举"""
    READ_ONLY = "read_only"      # 只读任务（可并行）
    WRITE_OPERATION = "write"    # 写操作（需串行）
    EXTERNAL_COMM = "external"   # 外部通信（需审批）
    SYSTEM_MOD = "system"        # 系统修改（高风险）

class WorkerRole(Enum):
    """Worker角色枚举"""
    PRODUCT = "product"      # 产品部
    DEVELOPMENT = "dev"      # 开发部
    DESIGN = "design"        # 设计部
    MARKETING = "marketing"  # 市场部

@dataclass
class Task:
    """任务定义"""
    id: str
    type: TaskType
    description: str
    assigned_to: Optional[WorkerRole] = None
    status: str = "pending"  # pending, assigned, in_progress, completed, failed
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Dict] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

@dataclass
class Worker:
    """Worker定义"""
    role: WorkerRole
    name: str
    skills: List[str]
    current_task: Optional[Task] = None
    task_history: List[Task] = None
    
    def __post_init__(self):
        if self.task_history is None:
            self.task_history = []
    
    def assign_task(self, task: Task) -> bool:
        """分配任务给Worker"""
        if self.current_task is not None:
            return False
        
        self.current_task = task
        task.assigned_to = self.role
        task.status = "assigned"
        return True
    
    def execute_task(self) -> Dict:
        """执行当前任务（模拟）"""
        if self.current_task is None:
            return {"success": False, "error": "No task assigned"}
        
        task = self.current_task
        task.status = "in_progress"
        task.started_at = time.time()
        
        # 模拟任务执行时间
        execution_time = random.uniform(0.5, 2.0)
        time.sleep(execution_time)
        
        # 模拟任务结果
        success_rate = 0.9  # 90%成功率
        success = random.random() < success_rate
        
        task.completed_at = time.time()
        task.status = "completed" if success else "failed"
        
        result = {
            "success": success,
            "execution_time": execution_time,
            "worker": self.role.value,
            "task_type": task.type.value,
            "output": f"Task {task.id} completed by {self.name}"
        }
        
        if not success:
            result["error"] = "Simulated task failure"
        
        task.result = result
        self.task_history.append(task)
        self.current_task = None
        
        return result

class Coordinator:
    """Coordinator协调器"""
    
    def __init__(self, workers: List[Worker]):
        self.workers = {worker.role: worker for worker in workers}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
    
    def create_task(self, task_type: TaskType, description: str) -> Task:
        """创建新任务"""
        task_id = f"task_{len(self.task_queue) + 1:03d}"
        task = Task(id=task_id, type=task_type, description=description)
        self.task_queue.append(task)
        return task
    
    def analyze_requirements(self, user_request: str) -> List[Task]:
        """分析用户需求，拆解为具体任务"""
        print(f"📋 Coordinator分析需求: {user_request}")
        
        tasks = []
        
        # 简单需求分析逻辑（实际应该更复杂）
        if "产品需求" in user_request or "PRD" in user_request:
            tasks.append(self.create_task(
                TaskType.WRITE_OPERATION,
                "撰写产品需求文档，包含用户故事和验收标准"
            ))
        
        if "开发" in user_request or "代码" in user_request:
            tasks.append(self.create_task(
                TaskType.WRITE_OPERATION,
                "实现功能模块，包含单元测试和文档"
            ))
        
        if "设计" in user_request or "UI" in user_request:
            tasks.append(self.create_task(
                TaskType.WRITE_OPERATION,
                "设计用户界面，包含原型和设计规范"
            ))
        
        if "搜索" in user_request or "查询" in user_request:
            tasks.append(self.create_task(
                TaskType.READ_ONLY,
                "搜索相关信息并整理结果"
            ))
        
        if "消息" in user_request or "通知" in user_request:
            tasks.append(self.create_task(
                TaskType.EXTERNAL_COMM,
                "发送外部消息，需要审批"
            ))
        
        print(f"  拆解为 {len(tasks)} 个任务")
        return tasks
    
    def assign_tasks(self):
        """分配任务给合适的Worker"""
        # 按任务类型排序：先只读（可并行），后写操作（需串行）
        read_tasks = [t for t in self.task_queue if t.type == TaskType.READ_ONLY]
        write_tasks = [t for t in self.task_queue if t.type != TaskType.READ_ONLY]
        
        assigned_count = 0
        
        # 分配只读任务（可并行）
        for task in read_tasks:
            if task.status != "pending":
                continue
            
            # 根据任务描述匹配Worker
            assigned = False
            for worker in self.workers.values():
                if worker.current_task is None:
                    if worker.assign_task(task):
                        print(f"  📤 分配只读任务 {task.id} 给 {worker.name}")
                        assigned_count += 1
                        assigned = True
                        break
            
            if not assigned:
                print(f"  ⚠️ 没有可用的Worker处理只读任务 {task.id}")
        
        # 分配写操作任务（串行）
        for task in write_tasks:
            if task.status != "pending":
                continue
            
            # 根据任务类型匹配Worker角色
            target_role = None
            if "产品需求" in task.description or "PRD" in task.description:
                target_role = WorkerRole.PRODUCT
            elif "开发" in task.description or "代码" in task.description:
                target_role = WorkerRole.DEVELOPMENT
            elif "设计" in task.description or "UI" in task.description:
                target_role = WorkerRole.DESIGN
            elif "消息" in task.description or "通知" in task.description:
                target_role = WorkerRole.MARKETING
            
            if target_role and target_role in self.workers:
                worker = self.workers[target_role]
                if worker.current_task is None:
                    if worker.assign_task(task):
                        print(f"  📤 分配写任务 {task.id} 给 {worker.name} ({task.type.value})")
                        assigned_count += 1
                else:
                    print(f"  ⏳ Worker {worker.name} 忙，等待处理任务 {task.id}")
            else:
                print(f"  ⚠️ 没有合适的Worker处理任务 {task.id}: {task.description}")
        
        return assigned_count
    
    def execute_tasks(self):
        """执行已分配的任务"""
        completed = []
        failed = []
        
        for worker in self.workers.values():
            if worker.current_task is not None:
                print(f"  🔧 {worker.name} 执行任务 {worker.current_task.id}")
                result = worker.execute_task()
                
                task = worker.current_task
                if result["success"]:
                    completed.append(task)
                    print(f"    ✅ 任务完成: {task.description[:50]}...")
                else:
                    failed.append(task)
                    print(f"    ❌ 任务失败: {result.get('error', 'Unknown error')}")
        
        # 更新任务列表
        for task in completed:
            self.task_queue.remove(task)
            self.completed_tasks.append(task)
        
        for task in failed:
            self.task_queue.remove(task)
            self.failed_tasks.append(task)
        
        return len(completed), len(failed)
    
    def generate_report(self) -> Dict:
        """生成执行报告"""
        total_tasks = len(self.completed_tasks) + len(self.failed_tasks)
        
        return {
            "total_tasks": total_tasks,
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "pending": len(self.task_queue),
            "success_rate": len(self.completed_tasks) / total_tasks if total_tasks > 0 else 0,
            "workers_performance": {
                role.value: {
                    "completed": len([t for t in self.completed_tasks if t.assigned_to == role]),
                    "failed": len([t for t in self.failed_tasks if t.assigned_to == role])
                }
                for role in self.workers.keys()
            }
        }

def test_scenario_1():
    """测试场景1：简单产品开发需求"""
    print("\n" + "=" * 60)
    print("测试场景1：简单产品开发需求")
    print("=" * 60)
    
    # 创建Worker团队
    workers = [
        Worker(WorkerRole.PRODUCT, "产品经理", ["需求分析", "PRD撰写"]),
        Worker(WorkerRole.DEVELOPMENT, "开发工程师", ["Python", "系统设计"]),
        Worker(WorkerRole.DESIGN, "UI设计师", ["Figma", "用户体验"]),
    ]
    
    coordinator = Coordinator(workers)
    
    # 用户需求
    user_request = "开发一个任务管理功能，需要产品需求、技术实现和UI设计"
    
    # Coordinator分析需求
    tasks = coordinator.analyze_requirements(user_request)
    
    # 分配任务
    print("\n📤 分配任务...")
    assigned = coordinator.assign_tasks()
    print(f"  共分配 {assigned}/{len(tasks)} 个任务")
    
    # 执行任务
    print("\n🔧 执行任务...")
    completed, failed = coordinator.execute_tasks()
    print(f"  完成 {completed} 个任务，失败 {failed} 个")
    
    # 生成报告
    report = coordinator.generate_report()
    print("\n📊 执行报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    return report["success_rate"] >= 0.8  # 80%成功率视为通过

def test_scenario_2():
    """测试场景2：混合只读和写操作"""
    print("\n" + "=" * 60)
    print("测试场景2：混合只读和写操作")
    print("=" * 60)
    
    workers = [
        Worker(WorkerRole.PRODUCT, "产品专员", ["市场调研", "竞品分析"]),
        Worker(WorkerRole.DEVELOPMENT, "全栈开发", ["前端", "后端"]),
        Worker(WorkerRole.MARKETING, "市场专员", ["内容创作", "社交媒体"]),
    ]
    
    coordinator = Coordinator(workers)
    
    # 创建混合任务
    coordinator.create_task(TaskType.READ_ONLY, "搜索竞品分析报告")
    coordinator.create_task(TaskType.READ_ONLY, "查询技术方案最佳实践")
    coordinator.create_task(TaskType.WRITE_OPERATION, "撰写产品发布公告")
    coordinator.create_task(TaskType.WRITE_OPERATION, "实现用户反馈功能")
    
    print("📤 分配混合任务...")
    assigned = coordinator.assign_tasks()
    
    print("\n🔧 执行任务...")
    completed, failed = coordinator.execute_tasks()
    
    report = coordinator.generate_report()
    print("\n📊 执行报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 验证并行执行：只读任务应该并行分配
    read_tasks_assigned = sum(1 for t in coordinator.completed_tasks + coordinator.failed_tasks 
                              if t.type == TaskType.READ_ONLY)
    return read_tasks_assigned >= 2  # 至少2个只读任务被分配

def test_scenario_3():
    """测试场景3：精确指令验证"""
    print("\n" + "=" * 60)
    print("测试场景3：精确指令验证")
    print("=" * 60)
    
    # 测试模糊指令和精确指令的区别
    vague_instructions = [
        "修复我们讨论的bug",
        "优化那个功能",
        "处理用户反馈",
    ]
    
    precise_instructions = [
        "修复登录页面的验证码显示问题（文件: src/login.js 第45行）",
        "优化用户列表的加载速度，目标从5秒降低到2秒以内",
        "处理用户ID为12345的反馈邮件，主题是'支付失败'",
    ]
    
    print("模糊指令示例（禁止使用）:")
    for instr in vague_instructions:
        print(f"  ❌ \"{instr}\"")
    
    print("\n精确指令示例（推荐使用）:")
    for instr in precise_instructions:
        print(f"  ✅ \"{instr}\"")
    
    # 验证精确指令包含必要元素
    required_elements = ["文件路径", "具体问题", "完成标准"]
    
    print("\n📋 精确指令检查清单:")
    for instr in precise_instructions:
        elements_present = []
        if any(keyword in instr for keyword in ["文件:", "第", "行"]):
            elements_present.append("文件路径")
        if any(keyword in instr for keyword in ["修复", "优化", "处理"]):
            elements_present.append("具体问题")
        if any(keyword in instr for keyword in ["目标", "降低到", "以内"]):
            elements_present.append("完成标准")
        
        score = len(elements_present) / len(required_elements)
        print(f"  \"{instr[:40]}...\" - 包含 {len(elements_present)}/{len(required_elements)} 必要元素 ({score:.0%})")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Coordinator+Worker协作测试")
    print("=" * 60)
    
    print("此脚本演示基于Claude Code架构的Coordinator+Worker模式。")
    print()
    
    test_results = {}
    
    # 运行测试场景
    try:
        test_results["scenario_1"] = test_scenario_1()
    except Exception as e:
        print(f"❌ 场景1测试失败: {e}")
        test_results["scenario_1"] = False
    
    try:
        test_results["scenario_2"] = test_scenario_2()
    except Exception as e:
        print(f"❌ 场景2测试失败: {e}")
        test_results["scenario_2"] = False
    
    try:
        test_results["scenario_3"] = test_scenario_3()
    except Exception as e:
        print(f"❌ 场景3测试失败: {e}")
        test_results["scenario_3"] = False
    
    # 总结报告
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总成绩: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！Coordinator+Worker协作模式验证成功。")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查实现。")
    
    print("\n📚 更多测试场景请参考:")
    print("   references/coordinator-worker-test-scenarios.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
        exit(1)