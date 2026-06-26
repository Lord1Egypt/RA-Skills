#!/usr/bin/env python3
"""
测试 Task Orchestrator 模块
- 任务 YAML 解析
- 依赖解析
- 任务派发
- 上下文构建
- 循环依赖检测
"""

import os
import sys
import tempfile
import unittest

# 添加 lib 到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.task_orchestrator import (
    CyclicDependencyError,
    Task,
    TaskState,
    TaskStateInfo,
    TasksConfig,
    approve_task,
    build_prompt,
    detect_cyclic_dependencies,
    dispatch_next_task,
    format_task_progress,
    get_all_completed,
    get_ready_tasks,
    get_task_by_id,
    load_tasks,
    mark_task_complete,
    mark_task_running,
)


class TestLoadTasks(unittest.TestCase):
    """测试任务 YAML 解析"""
    
    def setUp(self):
        """创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理临时文件"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _write_yaml(self, content: str) -> str:
        """写入 YAML 文件"""
        path = os.path.join(self.temp_dir, "tasks.yaml")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path
    
    def test_load_simple_tasks(self):
        """测试加载简单任务"""
        yaml_content = """
project:
  name: "TestProject"
  dir: "/test/path"
  description: "测试项目"
  enabled: true
  priority: 1

defaults:
  min_file_size: 100

tasks:
  - id: "task-1"
    name: "任务一"
    prompt: |
      这是任务一的说明
  - id: "task-2"
    name: "任务二"
    depends_on: ["task-1"]
    prompt: "任务二"
"""
        path = self._write_yaml(yaml_content)
        config = load_tasks(path)
        
        self.assertIsNotNone(config)
        self.assertEqual(config.project_name, "TestProject")
        self.assertEqual(len(config.tasks), 2)
        self.assertEqual(config.tasks[0].id, "task-1")
        self.assertEqual(config.tasks[1].depends_on, ["task-1"])
    
    def test_load_with_done_when(self):
        """测试加载带完成条件的任务"""
        yaml_content = """
project:
  name: "Test"
  dir: "/test"

tasks:
  - id: "task-1"
    name: "任务"
    prompt: "说明"
    done_when:
      files:
        - path: "package.json"
          min_size: 200
          contains: ["name", "version"]
      files_glob:
        - pattern: "src/**/*.ts"
          min_count: 5
      commands:
        - cmd: "npm test"
          expect_exit: 0
"""
        path = self._write_yaml(yaml_content)
        config = load_tasks(path)
        
        self.assertIsNotNone(config)
        task = config.tasks[0]
        self.assertIsNotNone(task.done_when)
        self.assertEqual(len(task.done_when["files"]), 1)
        self.assertEqual(task.done_when["files"][0]["min_size"], 200)
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        config = load_tasks("/nonexistent/path/tasks.yaml")
        self.assertIsNone(config)
    
    def test_load_invalid_yaml(self):
        """测试加载无效 YAML"""
        path = self._write_yaml("invalid: yaml: content: [")
        config = load_tasks(path)
        self.assertIsNone(config)
    
    def test_load_with_human_review(self):
        """测试加载需要人工审核的任务"""
        yaml_content = """
project:
  name: "Test"
  dir: "/test"

tasks:
  - id: "task-1"
    name: "需要审核"
    prompt: "说明"
    requires_human_review: true
"""
        path = self._write_yaml(yaml_content)
        config = load_tasks(path)
        
        self.assertTrue(config.tasks[0].requires_human_review)


class TestDependencyResolution(unittest.TestCase):
    """测试依赖解析"""
    
    def test_linear_dependency(self):
        """测试线性依赖 A -> B -> C"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=[]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
            Task(id="c", name="C", prompt="", depends_on=["b"]),
        ]
        task_states = {}
        
        # 初始状态：只有 A 可执行
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "a")
        
        # A 完成后，B 可执行
        task_states["a"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "b")
        
        # B 完成后，C 可执行
        task_states["b"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "c")
    
    def test_parallel_dependency(self):
        """测试并行依赖 A, B -> C"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=[]),
            Task(id="b", name="B", prompt="", depends_on=[]),
            Task(id="c", name="C", prompt="", depends_on=["a", "b"]),
        ]
        task_states = {}
        
        # 初始状态：A 和 B 都可执行
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 2)
        
        # 只有 A 完成，C 不可执行
        task_states["a"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "b")
        
        # A 和 B 都完成，C 可执行
        task_states["b"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "c")
    
    def test_diamond_dependency(self):
        """测试菱形依赖 A -> B, C -> D"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=[]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
            Task(id="c", name="C", prompt="", depends_on=["a"]),
            Task(id="d", name="D", prompt="", depends_on=["b", "c"]),
        ]
        task_states = {}
        
        # A 完成后，B 和 C 可执行
        task_states["a"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 2)
        
        # B 和 C 都完成，D 可执行
        task_states["b"] = TaskStateInfo(status="COMPLETED")
        task_states["c"] = TaskStateInfo(status="COMPLETED")
        ready = get_ready_tasks(tasks, task_states)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].id, "d")


class TestCyclicDependency(unittest.TestCase):
    """测试循环依赖检测"""
    
    def test_no_cycle(self):
        """测试无循环"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=[]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
        ]
        cycle = detect_cyclic_dependencies(tasks)
        self.assertIsNone(cycle)
    
    def test_simple_cycle(self):
        """测试简单循环 A -> B -> A"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=["b"]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
        ]
        cycle = detect_cyclic_dependencies(tasks)
        self.assertIsNotNone(cycle)
        self.assertIn("a", cycle)
        self.assertIn("b", cycle)
    
    def test_self_cycle(self):
        """测试自环 A -> A"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=["a"]),
        ]
        cycle = detect_cyclic_dependencies(tasks)
        self.assertIsNotNone(cycle)
    
    def test_complex_cycle(self):
        """测试复杂循环 A -> B -> C -> A"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=["c"]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
            Task(id="c", name="C", prompt="", depends_on=["b"]),
        ]
        cycle = detect_cyclic_dependencies(tasks)
        self.assertIsNotNone(cycle)


class TestDispatchNextTask(unittest.TestCase):
    """测试任务派发"""
    
    def test_dispatch_first_task(self):
        """测试派发第一个任务"""
        tasks = [
            Task(id="a", name="A", prompt="Task A prompt"),
        ]
        task_states = {}
        
        next_task, prompt = dispatch_next_task(tasks, task_states)
        
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.id, "a")
        self.assertIn("Task A prompt", prompt)
        self.assertEqual(task_states["a"].status, "RUNNING")
    
    def test_dispatch_with_completed(self):
        """测试完成一个任务后派发下一个"""
        tasks = [
            Task(id="a", name="A", prompt="Task A"),
            Task(id="b", name="B", prompt="Task B", depends_on=["a"]),
        ]
        task_states = {"a": TaskStateInfo(status="COMPLETED")}
        
        next_task, prompt = dispatch_next_task(tasks, task_states)
        
        self.assertEqual(next_task.id, "b")
        self.assertIn("Task B", prompt)
    
    def test_dispatch_all_completed(self):
        """测试所有任务完成"""
        tasks = [
            Task(id="a", name="A", prompt="Task A"),
        ]
        task_states = {"a": TaskStateInfo(status="COMPLETED")}
        
        next_task, prompt = dispatch_next_task(tasks, task_states)
        
        self.assertIsNone(next_task)
        self.assertIsNone(prompt)
    
    def test_dispatch_human_review(self):
        """测试需要人工审核的任务"""
        tasks = [
            Task(id="a", name="A", prompt="Task A", requires_human_review=True),
        ]
        task_states = {}
        
        next_task, prompt = dispatch_next_task(tasks, task_states)
        
        self.assertIsNotNone(next_task)
        self.assertIsNone(prompt)  # 不生成 prompt
        self.assertEqual(task_states["a"].status, "BLOCKED")
    
    def test_dispatch_raises_on_cycle(self):
        """测试循环依赖抛出异常"""
        tasks = [
            Task(id="a", name="A", prompt="", depends_on=["b"]),
            Task(id="b", name="B", prompt="", depends_on=["a"]),
        ]
        task_states = {}
        
        with self.assertRaises(CyclicDependencyError):
            dispatch_next_task(tasks, task_states)
    
    def test_dispatch_marks_current_complete(self):
        """测试派发时标记当前任务完成"""
        tasks = [
            Task(id="a", name="A", prompt="Task A"),
            Task(id="b", name="B", prompt="Task B", depends_on=["a"]),
        ]
        task_states = {"a": TaskStateInfo(status="RUNNING")}
        
        next_task, prompt = dispatch_next_task(
            tasks, task_states,
            current_task_id="a",
            codex_summary="A 完成了"
        )
        
        self.assertEqual(task_states["a"].status, "COMPLETED")
        self.assertEqual(task_states["a"].codex_summary, "A 完成了")
        self.assertEqual(next_task.id, "b")


class TestBuildPrompt(unittest.TestCase):
    """测试 Prompt 构建"""
    
    def test_simple_prompt(self):
        """测试简单 prompt"""
        task = Task(id="a", name="A", prompt="Do something")
        tasks = [task]
        task_states = {}
        
        prompt = build_prompt(task, task_states, tasks)
        
        self.assertIn("Do something", prompt)
        self.assertIn("当前任务: A", prompt)
    
    def test_prompt_with_context(self):
        """测试带上下文的 prompt"""
        tasks = [
            Task(id="a", name="A", prompt="Task A"),
            Task(id="b", name="B", prompt="Task B", depends_on=["a"]),
        ]
        task_states = {
            "a": TaskStateInfo(status="COMPLETED", codex_summary="A 创建了数据库")
        }
        
        prompt = build_prompt(tasks[1], task_states, tasks)
        
        self.assertIn("已完成的前置工作", prompt)
        self.assertIn("A: A 创建了数据库", prompt)
        self.assertIn("Task B", prompt)
    
    def test_prompt_progress(self):
        """测试进度显示"""
        tasks = [
            Task(id="a", name="A", prompt=""),
            Task(id="b", name="B", prompt=""),
            Task(id="c", name="C", prompt=""),
        ]
        task_states = {
            "a": TaskStateInfo(status="COMPLETED"),
        }
        
        prompt = build_prompt(tasks[1], task_states, tasks)
        
        self.assertIn("1/3", prompt)  # 1 of 3 completed


class TestTaskStateManagement(unittest.TestCase):
    """测试任务状态管理"""
    
    def test_mark_task_complete(self):
        """测试标记任务完成"""
        task_states = {"a": TaskStateInfo(status="RUNNING")}
        
        mark_task_complete("a", task_states, "完成摘要")
        
        self.assertEqual(task_states["a"].status, "COMPLETED")
        self.assertIsNotNone(task_states["a"].completed_at)
        self.assertEqual(task_states["a"].codex_summary, "完成摘要")
    
    def test_mark_task_running(self):
        """测试标记任务运行"""
        task_states = {}
        
        mark_task_running("a", task_states)
        
        self.assertEqual(task_states["a"].status, "RUNNING")
        self.assertIsNotNone(task_states["a"].started_at)
        self.assertEqual(task_states["a"].sends, 1)
    
    def test_approve_task(self):
        """测试批准任务"""
        task_states = {"a": TaskStateInfo(status="BLOCKED")}
        
        result = approve_task("a", task_states)
        
        self.assertTrue(result)
        self.assertEqual(task_states["a"].status, "PENDING")
    
    def test_approve_non_blocked(self):
        """测试批准非阻塞任务"""
        task_states = {"a": TaskStateInfo(status="RUNNING")}
        
        result = approve_task("a", task_states)
        
        self.assertFalse(result)


class TestHelperFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_get_task_by_id(self):
        """测试根据 ID 获取任务"""
        tasks = [
            Task(id="a", name="A", prompt=""),
            Task(id="b", name="B", prompt=""),
        ]
        
        task = get_task_by_id(tasks, "b")
        self.assertEqual(task.name, "B")
        
        task = get_task_by_id(tasks, "nonexistent")
        self.assertIsNone(task)
    
    def test_get_all_completed(self):
        """测试检查所有任务完成"""
        tasks = [
            Task(id="a", name="A", prompt=""),
            Task(id="b", name="B", prompt=""),
        ]
        
        # 未全部完成
        task_states = {"a": TaskStateInfo(status="COMPLETED")}
        self.assertFalse(get_all_completed(tasks, task_states))
        
        # 全部完成
        task_states["b"] = TaskStateInfo(status="COMPLETED")
        self.assertTrue(get_all_completed(tasks, task_states))
    
    def test_format_task_progress(self):
        """测试格式化任务进度"""
        tasks = [
            Task(id="a", name="A", prompt=""),
            Task(id="b", name="B", prompt=""),
        ]
        task_states = {
            "a": TaskStateInfo(status="COMPLETED"),
            "b": TaskStateInfo(status="RUNNING"),
        }
        
        progress = format_task_progress(tasks, task_states)
        
        self.assertIn("✅", progress)
        self.assertIn("🔄", progress)
        self.assertIn("1/2", progress)


class TestTaskStateInfoSerialization(unittest.TestCase):
    """测试 TaskStateInfo 序列化"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        state = TaskStateInfo(
            status="COMPLETED",
            started_at="2026-02-06T10:00:00",
            completed_at="2026-02-06T10:30:00",
            sends=3,
            codex_summary="完成了"
        )
        
        d = state.to_dict()
        
        self.assertEqual(d["status"], "COMPLETED")
        self.assertEqual(d["sends"], 3)
        self.assertIn("started_at", d)
    
    def test_from_dict(self):
        """测试从字典创建"""
        d = {
            "status": "RUNNING",
            "started_at": "2026-02-06T10:00:00",
            "sends": 2,
        }
        
        state = TaskStateInfo.from_dict(d)
        
        self.assertEqual(state.status, "RUNNING")
        self.assertEqual(state.sends, 2)
    
    def test_from_dict_defaults(self):
        """测试从空字典创建（使用默认值）"""
        state = TaskStateInfo.from_dict({})
        
        self.assertEqual(state.status, "PENDING")
        self.assertEqual(state.sends, 0)


if __name__ == '__main__':
    unittest.main()
