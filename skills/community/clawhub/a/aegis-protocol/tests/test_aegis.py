#!/usr/bin/env python3
"""Aegis Protocol 单元测试套件

测试覆盖：
- 配置加载
- 检查函数
- 恢复函数
- 健康度评分
"""

import unittest
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加父目录到路径
WORKSPACE = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE))

# 直接导入模块
import importlib.util
spec = importlib.util.spec_from_file_location("aegis_protocol", WORKSPACE / "aegis-protocol.py")
aegis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aegis)

load_config = aegis.load_config
save_config = aegis.save_config
exec_cmd = aegis.exec_cmd
check_disk = aegis.check_disk
check_memory = aegis.check_memory
check_cpu_load = aegis.check_cpu_load
check_zombie_processes = aegis.check_zombie_processes
get_health_score = aegis.get_health_score


class TestConfig(unittest.TestCase):
    """配置相关测试"""
    
    @unittest.skip("需要配置文件存在")
    def test_load_config_returns_dict(self):
        """测试加载配置返回字典"""
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn("thresholds", config)
        self.assertIn("cooldowns", config)
        self.assertIn("actions", config)
    
    def test_save_config_persists(self):
        """测试保存配置可持久化"""
        test_config = {"test": "value", "number": 42}
        result = save_config(test_config)
        self.assertTrue(result)


class TestExecCmd(unittest.TestCase):
    """命令执行测试"""
    
    def test_exec_cmd_success(self):
        """测试成功执行命令"""
        code, out, err = exec_cmd("echo hello")
        self.assertEqual(code, 0)
        self.assertIn("hello", out)
    
    def test_exec_cmd_failure(self):
        """测试失败命令"""
        code, out, err = exec_cmd("exit 1")
        self.assertEqual(code, 1)
    
    def test_exec_cmd_timeout(self):
        """测试超时处理"""
        code, out, err = exec_cmd("sleep 3", timeout=1)
        self.assertEqual(code, -1)
        self.assertEqual(err, "Command timed out")


class TestChecks(unittest.TestCase):
    """检查函数测试"""
    
    @unittest.skip("需要配置文件存在")
    def test_check_disk(self):
        """测试磁盘检查"""
        result = check_disk()
        self.assertIn("status", result)
        self.assertIn("usage_percent", result)
        self.assertIn("threshold", result)
    
    @unittest.skip("需要配置文件存在")
    def test_check_memory(self):
        """测试内存检查"""
        result = check_memory()
        self.assertIn("status", result)
        self.assertIn("usage_percent", result)
        self.assertGreaterEqual(result["usage_percent"], 0)
        self.assertLessEqual(result["usage_percent"], 100)
    
    def test_check_cpu_load(self):
        """测试 CPU 负载检查"""
        result = check_cpu_load()
        self.assertIn("status", result)
        self.assertIn("load_1m", result)
        self.assertIn("cpu_count", result)
        self.assertGreaterEqual(result["load_1m"], 0)
    
    def test_check_zombie_processes(self):
        """测试僵尸进程检查"""
        result = check_zombie_processes()
        self.assertIn("status", result)
        self.assertIn("zombie_count", result)
        self.assertGreaterEqual(result["zombie_count"], 0)


class TestHealthScore(unittest.TestCase):
    """健康度评分测试"""
    
    def test_health_score_all_ok(self):
        """测试全部正常时评分为 100"""
        checks = {
            "check1": {"status": "ok"},
            "check2": {"status": "ok"},
            "check3": {"status": "ok"}
        }
        score = get_health_score(checks)
        self.assertEqual(score, 100)
    
    def test_health_score_mixed(self):
        """测试混合状态评分"""
        checks = {
            "check1": {"status": "ok"},      # 100
            "check2": {"status": "warning"}, # 50
            "check3": {"status": "error"}    # 0
        }
        score = get_health_score(checks)
        self.assertEqual(score, 50)  # (100+50+0)/3 = 50
    
    def test_health_score_empty(self):
        """测试空检查返回 0"""
        score = get_health_score({})
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
