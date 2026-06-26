#!/usr/bin/env python3
"""异常类测试"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib.util

spec = importlib.util.spec_from_file_location("aegis_protocol", Path(__file__).parent.parent / "aegis-protocol.py")
aegis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aegis)

AegisError = aegis.AegisError
ConfigError = aegis.ConfigError
CheckError = aegis.CheckError
RecoveryError = aegis.RecoveryError
ExternalCommandError = aegis.ExternalCommandError


class TestExceptions(unittest.TestCase):
    """异常类测试"""
    
    def test_aegis_error_base(self):
        """测试基础异常"""
        with self.assertRaises(AegisError):
            raise AegisError("基础错误")
    
    def test_config_error(self):
        """测试配置异常"""
        with self.assertRaises(ConfigError):
            raise ConfigError("配置错误")
    
    def test_check_error(self):
        """测试检查异常"""
        with self.assertRaises(CheckError):
            raise CheckError("检查错误")
    
    def test_recovery_error(self):
        """测试恢复异常"""
        with self.assertRaises(RecoveryError):
            raise RecoveryError("恢复错误")
    
    def test_external_command_error(self):
        """测试外部命令异常"""
        err = ExternalCommandError("ls -la", 1, "permission denied")
        self.assertEqual(err.command, "ls -la")
        self.assertEqual(err.returncode, 1)
        self.assertIn("permission denied", str(err))
        self.assertIn("ls -la", str(err))
    
    def test_exception_hierarchy(self):
        """测试异常继承关系"""
        for exc_class in [ConfigError, CheckError, RecoveryError]:
            try:
                raise exc_class("test")
            except AegisError:
                pass  # 应该能被 AegisError 捕获
            except Exception:
                self.fail(f"{exc_class.__name__} 不是 AegisError 的子类")
    
    def test_external_command_error_hierarchy(self):
        """测试 ExternalCommandError 继承关系"""
        try:
            raise ExternalCommandError("test_cmd", 1, "error message")
        except AegisError:
            pass  # 应该能被 AegisError 捕获
        except Exception as e:
            self.fail(f"ExternalCommandError 不是 AegisError 的子类：{e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
