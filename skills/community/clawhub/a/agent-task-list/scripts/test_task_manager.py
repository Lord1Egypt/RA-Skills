#!/usr/bin/env python3
"""
Agent 独立任务列表系统 - 单元测试
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent))

import task_manager


def setup_test_env():
    """设置测试环境"""
    # 创建临时目录
    test_dir = Path(tempfile.mkdtemp())
    
    # 覆盖全局路径
    task_manager.WORKSPACE_ROOT = test_dir
    task_manager.TASK_DATA_DIR = test_dir / "agent-tasks"
    task_manager.AGENTS_DIR = test_dir / "agent-tasks" / "agents"
    task_manager.HISTORY_DIR = test_dir / "agent-tasks" / "history"
    task_manager.TASK_COUNTER_FILE = test_dir / "agent-tasks" / "task-counter.txt"
    task_manager.INDEX_FILE = test_dir / "agent-tasks" / "index.json"
    
    # 确保目录存在
    task_manager.ensure_dirs()
    
    return test_dir


def teardown_test_env(test_dir: Path):
    """清理测试环境"""
    shutil.rmtree(test_dir, ignore_errors=True)


def test_create_task():
    """测试创建任务"""
    test_dir = setup_test_env()
    
    try:
        result = task_manager.create_task(
            agent_id="test-agent",
            name="测试任务",
            description="这是一个测试任务",
            priority=8
        )
        
        assert result["status"] == "success", f"期望 status 为 success，实际为 {result['status']}"
        assert "task_id" in result, "结果应包含 task_id"
        assert result["task"]["name"] == "测试任务", "任务名称不匹配"
        assert result["task"]["priority"] == 8, "任务优先级不匹配"
        assert result["task"]["status"] == task_manager.TASK_STATUS_PENDING, "任务状态应为 pending"
        
        print("✓ test_create_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_create_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_create_multiple_tasks():
    """测试创建多个任务"""
    test_dir = setup_test_env()
    
    try:
        # 创建 3 个不同优先级的任务
        result1 = task_manager.create_task("test-agent", "任务 1", "描述 1", priority=3)
        result2 = task_manager.create_task("test-agent", "任务 2", "描述 2", priority=8)
        result3 = task_manager.create_task("test-agent", "任务 3", "描述 3", priority=5)
        
        assert result1["status"] == "success"
        assert result2["status"] == "success"
        assert result3["status"] == "success"
        
        # 检查任务 ID 是否递增
        assert result1["task_id"] == "task-001"
        assert result2["task_id"] == "task-002"
        assert result3["task_id"] == "task-003"
        
        # 检查待办队列是否按优先级排序
        task_list = task_manager.list_tasks("test-agent")
        pending = task_list["pending_tasks"]
        
        assert len(pending) == 3, f"待办任务数量应为 3，实际为 {len(pending)}"
        assert pending[0]["priority"] == 8, "最高优先级任务应在最前面"
        assert pending[1]["priority"] == 5, "第二高优先级任务应在第二位"
        assert pending[2]["priority"] == 3, "最低优先级任务应在最后"
        
        print("✓ test_create_multiple_tasks 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_create_multiple_tasks 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_start_task():
    """测试开始执行任务"""
    test_dir = setup_test_env()
    
    try:
        # 先创建任务
        create_result = task_manager.create_task(
            "test-agent", "测试任务", "测试描述", priority=5
        )
        assert create_result["status"] == "success"
        
        # 开始执行任务
        start_result = task_manager.start_task("test-agent")
        
        assert start_result["status"] == "success", f"期望 status 为 success，实际为 {start_result['status']}"
        assert start_result["task"]["status"] == task_manager.TASK_STATUS_RUNNING
        assert "started_at" in start_result["task"]
        
        # 检查任务列表
        task_list = task_manager.list_tasks("test-agent")
        assert task_list["current_task"] is not None, "应有当前任务"
        assert len(task_list["pending_tasks"]) == 0, "待办队列应为空"
        
        print("✓ test_start_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_start_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_complete_task():
    """测试完成任务"""
    test_dir = setup_test_env()
    
    try:
        # 创建并开始任务
        task_manager.create_task("test-agent", "测试任务", "测试描述", priority=5)
        task_manager.start_task("test-agent")
        
        # 完成任务
        complete_result = task_manager.complete_task("test-agent")
        
        assert complete_result["status"] == "success"
        assert complete_result["task_id"] == "task-001"
        
        # 检查任务列表
        task_list = task_manager.list_tasks("test-agent")
        assert task_list["current_task"] is None, "当前任务应为 None"
        assert len(task_list["completed_tasks"]) == 1, "已完成任务应为 1"
        assert task_list["completed_tasks"][0]["status"] == task_manager.TASK_STATUS_COMPLETED
        
        # 检查历史记录是否已归档
        history_dir = task_manager.HISTORY_DIR
        history_files = list(history_dir.rglob("task-001.json"))
        assert len(history_files) == 1, "应有一个历史归档文件"
        
        print("✓ test_complete_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_complete_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_fail_task():
    """测试任务失败"""
    test_dir = setup_test_env()
    
    try:
        # 创建并开始任务
        task_manager.create_task("test-agent", "测试任务", "测试描述", priority=5)
        task_manager.start_task("test-agent")
        
        # 标记任务失败
        fail_result = task_manager.fail_task("test-agent", "测试错误信息")
        
        assert fail_result["status"] == "success"
        assert fail_result["task_id"] == "task-001"
        
        # 检查任务列表
        task_list = task_manager.list_tasks("test-agent")
        assert task_list["current_task"] is None, "当前任务应为 None"
        assert len(task_list["failed_tasks"]) == 1, "失败任务应为 1"
        assert task_list["failed_tasks"][0]["status"] == task_manager.TASK_STATUS_FAILED
        assert task_list["failed_tasks"][0]["error_message"] == "测试错误信息"
        assert task_list["failed_tasks"][0]["retry_count"] == 1
        
        print("✓ test_fail_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_fail_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_retry_task():
    """测试重试失败任务"""
    test_dir = setup_test_env()
    
    try:
        # 创建、开始、失败任务
        task_manager.create_task("test-agent", "测试任务", "测试描述", priority=5)
        task_manager.start_task("test-agent")
        task_manager.fail_task("test-agent", "错误信息")
        
        # 重试任务
        retry_result = task_manager.retry_task("test-agent", "task-001")
        
        assert retry_result["status"] == "success"
        
        # 检查任务列表
        task_list = task_manager.list_tasks("test-agent")
        assert len(task_list["failed_tasks"]) == 0, "失败任务应为 0"
        assert len(task_list["pending_tasks"]) == 1, "待办任务应为 1"
        assert task_list["pending_tasks"][0]["status"] == task_manager.TASK_STATUS_PENDING
        
        print("✓ test_retry_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_retry_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_cancel_task():
    """测试取消任务"""
    test_dir = setup_test_env()
    
    try:
        # 测试取消待办任务
        task_manager.create_task("test-agent", "测试任务", "测试描述", priority=5)
        
        cancel_result = task_manager.cancel_task("test-agent", "task-001")
        assert cancel_result["status"] == "success"
        
        task_list = task_manager.list_tasks("test-agent")
        assert len(task_list["pending_tasks"]) == 0, "待办任务应为 0"
        
        # 测试取消当前任务
        task_manager.create_task("test-agent", "测试任务 2", "测试描述 2", priority=5)
        task_manager.start_task("test-agent")
        
        cancel_result = task_manager.cancel_task("test-agent", "task-002")
        assert cancel_result["status"] == "success"
        
        task_list = task_manager.list_tasks("test-agent")
        assert task_list["current_task"] is None, "当前任务应为 None"
        
        print("✓ test_cancel_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_cancel_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_query_tasks():
    """测试查询任务"""
    test_dir = setup_test_env()
    
    try:
        # 创建多个任务
        task_manager.create_task("test-agent", "任务 1", "描述 1", priority=3)
        task_manager.create_task("test-agent", "任务 2", "描述 2", priority=8)
        task_manager.create_task("test-agent", "任务 3", "描述 3", priority=5)
        
        # 查询所有任务
        query_result = task_manager.query_tasks("test-agent")
        assert query_result["status"] == "success"
        assert query_result["total"] == 3
        
        # 按优先级查询
        query_result = task_manager.query_tasks("test-agent", min_priority=5)
        assert query_result["total"] == 2, "应有 2 个任务优先级>=5"
        
        print("✓ test_query_tasks 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_query_tasks 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_get_stats():
    """测试统计信息"""
    test_dir = setup_test_env()
    
    try:
        # 创建任务
        task_manager.create_task("test-agent", "任务 1", "描述 1", priority=5)
        task_manager.create_task("test-agent", "任务 2", "描述 2", priority=5)
        
        # 获取统计
        stats = task_manager.get_stats("test-agent")
        
        assert stats["status"] == "success"
        assert stats["total"]["pending"] == 2
        assert stats["total"]["all"] == 2
        
        # 完成一个任务
        task_manager.start_task("test-agent")
        task_manager.complete_task("test-agent")
        
        stats = task_manager.get_stats("test-agent")
        assert stats["total"]["current"] == 0
        assert stats["total"]["pending"] == 1
        assert stats["total"]["completed"] == 1
        assert stats["success_rate"] == 1.0
        
        print("✓ test_get_stats 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_get_stats 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_get_task():
    """测试获取任务详情"""
    test_dir = setup_test_env()
    
    try:
        # 创建任务
        task_manager.create_task("test-agent", "测试任务", "测试描述", priority=5)
        
        # 获取任务详情
        result = task_manager.get_task("task-001")
        
        assert result["status"] == "success"
        assert result["task"]["id"] == "task-001"
        assert result["task"]["name"] == "测试任务"
        assert result["location"] == "pending_tasks"
        
        print("✓ test_get_task 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_get_task 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_list_all_agents():
    """测试获取所有 Agent 概览"""
    test_dir = setup_test_env()
    
    try:
        # 为不同 Agent 创建任务
        task_manager.create_task("agent-a", "任务 A", "描述 A", priority=5)
        task_manager.create_task("agent-b", "任务 B", "描述 B", priority=5)
        task_manager.create_task("agent-b", "任务 B2", "描述 B2", priority=5)
        
        # 获取所有 Agent 概览
        result = task_manager.list_all_agents()
        
        assert "agents" in result
        assert len(result["agents"]) == 2
        
        # 查找 agent-a
        agent_a = next((a for a in result["agents"] if a["agent_id"] == "agent-a"), None)
        assert agent_a is not None
        assert agent_a["task_count"]["pending"] == 1
        
        # 查找 agent-b
        agent_b = next((a for a in result["agents"] if a["agent_id"] == "agent-b"), None)
        assert agent_b is not None
        assert agent_b["task_count"]["pending"] == 2
        
        print("✓ test_list_all_agents 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_list_all_agents 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_priority_validation():
    """测试优先级验证"""
    test_dir = setup_test_env()
    
    try:
        # 测试无效优先级
        result = task_manager.create_task("test-agent", "任务", "描述", priority=0)
        assert result["status"] == "error"
        assert "优先级" in result["error"]
        
        result = task_manager.create_task("test-agent", "任务", "描述", priority=11)
        assert result["status"] == "error"
        assert "优先级" in result["error"]
        
        print("✓ test_priority_validation 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_priority_validation 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_start_task_without_pending():
    """测试没有待办任务时开始任务"""
    test_dir = setup_test_env()
    
    try:
        # 没有待办任务时开始任务
        result = task_manager.start_task("test-agent")
        
        assert result["status"] == "error"
        assert "没有待办任务" in result["error"]
        
        print("✓ test_start_task_without_pending 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_start_task_without_pending 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def test_complete_task_without_current():
    """测试没有当前任务时完成任务"""
    test_dir = setup_test_env()
    
    try:
        # 没有当前任务时完成任务
        result = task_manager.complete_task("test-agent")
        
        assert result["status"] == "error"
        assert "没有当前任务" in result["error"]
        
        print("✓ test_complete_task_without_current 通过")
        return True
        
    except Exception as e:
        print(f"✗ test_complete_task_without_current 失败：{e}")
        return False
        
    finally:
        teardown_test_env(test_dir)


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Agent 独立任务列表系统 - 单元测试")
    print("=" * 60)
    
    tests = [
        test_create_task,
        test_create_multiple_tasks,
        test_start_task,
        test_complete_task,
        test_fail_task,
        test_retry_task,
        test_cancel_task,
        test_query_tasks,
        test_get_stats,
        test_get_task,
        test_list_all_agents,
        test_priority_validation,
        test_start_task_without_pending,
        test_complete_task_without_current,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"测试完成：{passed}/{total} 通过")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
