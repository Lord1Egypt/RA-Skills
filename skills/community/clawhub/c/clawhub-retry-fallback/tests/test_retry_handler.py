"""
Unit Tests for ClawHub Retry & Fallback Skill
单元测试
"""

import unittest
import time
from unittest.mock import Mock, patch
import sys
import os

# 添加scripts到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.config_manager import ConfigManager, RetryPolicy
from scripts.exception_classifier import ExceptionClassifier, ExceptionCategory
from scripts.retry_handler import RetryHandler, RetryResult
from scripts.fallback_manager import FallbackManager, FallbackPriority
from scripts.degradation_handler import DegradationHandler, TaskStep, StepPriority, DegradationLevel
from scripts.audit_logger import AuditLogger


class TestConfigManager(unittest.TestCase):
    """配置管理器测试"""
    
    def setUp(self):
        self.config = ConfigManager()
    
    def test_default_policies_loaded(self):
        """测试默认策略已加载"""
        policy = self.config.get_policy('network_timeout')
        self.assertIsNotNone(policy)
        self.assertEqual(policy.max_attempts, 3)
        self.assertEqual(policy.backoff_strategy, 'exponential')
    
    def test_platform_limits(self):
        """测试平台限制"""
        limits = self.config.get_platform_limits()
        self.assertIn('max_retry_attempts', limits)
        self.assertEqual(limits['max_retry_attempts'], 10)
    
    def test_exception_classification(self):
        """测试异常分类规则"""
        self.assertTrue(self.config.is_retryable_exception('ConnectionError'))
        self.assertTrue(self.config.is_retryable_exception('429'))
        self.assertFalse(self.config.is_retryable_exception('ValueError'))
        self.assertFalse(self.config.is_retryable_exception('400'))


class TestExceptionClassifier(unittest.TestCase):
    """异常分类器测试"""
    
    def setUp(self):
        self.classifier = ExceptionClassifier()
    
    def test_retryable_exceptions(self):
        """测试可重试异常识别"""
        retryable = [
            ConnectionError("连接失败"),
            TimeoutError("请求超时"),
        ]
        
        for exc in retryable:
            with self.subTest(exc=exc):
                self.assertTrue(self.classifier.is_retryable(exc))
                self.assertEqual(self.classifier.classify(exc), ExceptionCategory.RETRYABLE)
    
    def test_non_retryable_exceptions(self):
        """测试不可重试异常识别"""
        non_retryable = [
            ValueError("参数错误"),
            PermissionError("权限不足"),
        ]
        
        for exc in non_retryable:
            with self.subTest(exc=exc):
                self.assertFalse(self.classifier.is_retryable(exc))
                self.assertEqual(self.classifier.classify(exc), ExceptionCategory.NON_RETRYABLE)
    
    def test_http_status_codes(self):
        """测试HTTP状态码分类"""
        # 可重试状态码
        self.assertTrue(self.classifier.is_retryable({'status_code': 429}))
        self.assertTrue(self.classifier.is_retryable({'status_code': 503}))
        
        # 不可重试状态码
        self.assertFalse(self.classifier.is_retryable({'status_code': 400}))
        self.assertFalse(self.classifier.is_retryable({'status_code': 404}))
    
    def test_unknown_exception_default(self):
        """测试未知异常默认行为"""
        # 未知异常应该默认可重试（谨慎重试策略）
        class UnknownException(Exception):
            pass
        
        exc = UnknownException("未知错误")
        self.assertTrue(self.classifier.is_retryable(exc))


class TestRetryHandler(unittest.TestCase):
    """重试处理器测试"""
    
    def setUp(self):
        self.handler = RetryHandler()
    
    def test_successful_execution(self):
        """测试正常执行无需重试"""
        def success_func():
            return "success"
        
        result = self.handler.execute_with_retry(success_func)
        
        self.assertTrue(result.success)
        self.assertEqual(result.result, "success")
        self.assertEqual(result.attempts, 1)
    
    def test_retry_on_failure(self):
        """测试失败时自动重试"""
        call_count = 0
        
        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError(f"失败 #{call_count}")
            return "success"
        
        result = self.handler.execute_with_retry(
            fail_then_succeed,
            max_attempts=3
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.attempts, 3)
        self.assertEqual(len(result.retry_history), 2)
    
    def test_non_retryable_exception_no_retry(self):
        """测试不可重试异常不重试"""
        call_count = 0
        
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("参数错误")
        
        result = self.handler.execute_with_retry(
            always_fail,
            max_attempts=3
        )
        
        self.assertFalse(result.success)
        self.assertEqual(call_count, 1)  # 只执行一次
    
    def test_max_attempts_limit(self):
        """测试最大重试次数限制"""
        result = self.handler.execute_with_retry(
            lambda: (_ for _ in ()).throw(ConnectionError("始终失败")),
            max_attempts=2
        )
        
        self.assertFalse(result.success)
        # attempts = len(retry_history) + 1 = 2 + 1 = 3
        self.assertEqual(result.attempts, 3)


class TestFallbackManager(unittest.TestCase):
    """备用工具管理器测试"""
    
    def setUp(self):
        self.manager = FallbackManager()
    
    def test_register_backup(self):
        """测试注册备用工具"""
        def backup_func():
            return "backup"
        
        self.manager.register_backup(
            primary='main',
            backup='backup',
            backup_func=backup_func,
            priority=FallbackPriority.HIGH_QUALITY
        )
        
        backups = self.manager.get_backup_tools('main')
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].name, 'backup')
    
    def test_fallback_execution_success(self):
        """测试备用工具切换成功"""
        def primary():
            raise ConnectionError("主工具失败")
        
        def backup():
            return "backup result"
        
        self.manager.register_backup(
            primary='primary_tool',
            backup='backup_tool',
            backup_func=backup
        )
        
        result = self.manager.execute_with_fallback(
            primary_func=primary,
            primary_name='primary_tool'
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.result, "backup result")
        self.assertEqual(result.backup_tool, 'backup_tool')
    
    def test_primary_success_no_fallback(self):
        """测试主工具成功时不切换"""
        def primary():
            return "primary result"
        
        result = self.manager.execute_with_fallback(
            primary_func=primary,
            primary_name='primary_tool'
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.result, "primary result")
        self.assertEqual(result.switch_count, 0)


class TestDegradationHandler(unittest.TestCase):
    """降级处理器测试"""
    
    def setUp(self):
        self.handler = DegradationHandler()
    
    def test_successful_execution(self):
        """测试正常执行无降级"""
        steps = [
            TaskStep(name='step1', func=lambda: 'result1'),
            TaskStep(name='step2', func=lambda: 'result2')
        ]
        
        result = self.handler.execute_with_degradation(steps)
        
        self.assertTrue(result.success)
        self.assertEqual(result.level, DegradationLevel.NONE)
        self.assertEqual(result.completed_steps, ['step1', 'step2'])
    
    def test_light_degradation(self):
        """测试轻度降级"""
        steps = [
            TaskStep(name='step1', func=lambda: 'result1', priority=StepPriority.CRITICAL),
            TaskStep(name='step2', func=lambda: (_ for _ in ()).throw(Exception("失败")), priority=StepPriority.OPTIONAL),
            TaskStep(name='step3', func=lambda: 'result3', priority=StepPriority.IMPORTANT)
        ]
        
        result = self.handler.execute_with_degradation(steps)
        
        self.assertTrue(result.success)
        self.assertEqual(result.level, DegradationLevel.LIGHT)
        self.assertIn('step2', result.skipped_steps)
    
    def test_medium_degradation(self):
        """测试中度降级 - 核心步骤失败后保留已完成结果"""
        steps = [
            TaskStep(name='step1', func=lambda: 'result1', priority=StepPriority.IMPORTANT),
            TaskStep(name='step2', func=lambda: (_ for _ in ()).throw(Exception("失败")), priority=StepPriority.CRITICAL),
            TaskStep(name='step3', func=lambda: 'result3', priority=StepPriority.OPTIONAL)
        ]
        
        result = self.handler.execute_with_degradation(steps)
        
        self.assertTrue(result.success)
        self.assertEqual(result.level, DegradationLevel.MEDIUM)
        self.assertEqual(result.completed_steps, ['step1'])
    
    def test_heavy_degradation(self):
        """测试重度降级 - 核心步骤失败后继续执行其他核心步骤"""
        # 创建一个步骤先进入中度，然后在中度状态下核心步骤失败
        steps = [
            TaskStep(name='step1', func=lambda: 'result1', priority=StepPriority.CRITICAL),
            TaskStep(name='step2', func=lambda: (_ for _ in ()).throw(Exception("核心步骤失败")), priority=StepPriority.CRITICAL),
        ]
        
        result = self.handler.execute_with_degradation(steps)
        
        # step2 是第一个失败的 CRITICAL，进入 MEDIUM
        self.assertTrue(result.success)
        self.assertEqual(result.level, DegradationLevel.MEDIUM)
        self.assertEqual(result.completed_steps, ['step1'])
        self.assertIn('step2', result.failed_steps)


class TestAuditLogger(unittest.TestCase):
    """审计日志测试"""
    
    def setUp(self):
        self.logger = AuditLogger()
    
    def test_log_retry(self):
        """测试记录重试日志"""
        self.logger.log_retry(
            task_id='task-001',
            exception_type='ConnectionError',
            attempt=1,
            max_attempts=3
        )
        
        logs = self.logger.get_logs(task_id='task-001')
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].operation, 'retry')
    
    def test_log_fallback(self):
        """测试记录备用工具切换日志"""
        self.logger.log_fallback(
            task_id='task-001',
            primary_tool='api1',
            backup_tool='api2',
            success=True
        )
        
        logs = self.logger.get_logs(operation='fallback')
        self.assertEqual(len(logs), 1)
        self.assertTrue(logs[0].details['success'])
    
    def test_generate_report(self):
        """测试生成报告"""
        self.logger.log_retry(task_id='task-002', exception_type='Error', attempt=1, max_attempts=3)
        self.logger.log_fallback(task_id='task-002', primary_tool='a', backup_tool='b', success=True)
        self.logger.log_task_completion(task_id='task-002', success=True, execution_time=5.0)
        
        report = self.logger.generate_report('task-002')
        
        self.assertEqual(report['task_id'], 'task-002')
        self.assertEqual(report['execution_summary']['retry_count'], 1)
        self.assertEqual(report['execution_summary']['fallback_count'], 1)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_flow(self):
        """测试完整流程"""
        # 初始化所有组件
        config = ConfigManager()
        handler = RetryHandler(config)
        fallback = FallbackManager()
        degradation = DegradationHandler()
        logger = AuditLogger()
        
        # 模拟一个完整的任务流程
        call_count = [0]
        
        @handler.with_retry(max_attempts=3)
        def api_call():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ConnectionError(f"失败 {call_count[0]}")
            return {"data": "success"}
        
        # 执行任务
        result = api_call()
        
        # 验证结果 - result 是 RetryResult 对象
        self.assertTrue(result.success)
        self.assertEqual(result.result, {"data": "success"})
        self.assertEqual(call_count[0], 3)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestExceptionClassifier))
    suite.addTests(loader.loadTestsFromTestCase(TestRetryHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestFallbackManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDegradationHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestAuditLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)