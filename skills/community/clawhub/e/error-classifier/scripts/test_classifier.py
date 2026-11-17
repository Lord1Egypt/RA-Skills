"""
Error Classifier 测试用例

覆盖：
- 四类错误分类正确性
- 处理动作正确性
- 指数退避计算
- 重试次数上限
- 边界情况
"""

import sys
import os
import unittest

# 确保能导入同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classifier import ErrorClassifier, ErrorType, ErrorAction


class TestErrorClassification(unittest.TestCase):
    """测试错误分类"""

    def setUp(self):
        self.classifier = ErrorClassifier()

    # ---- TRANSIENT（临时错误）----

    def test_timeout_is_transient(self):
        error = Exception("Connection timeout after 30s")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_timed_out_is_transient(self):
        error = Exception("Request timed out")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_rate_limit_is_transient(self):
        error = Exception("Rate limit exceeded, 429 Too Many Requests")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_503_is_transient(self):
        error = Exception("HTTP 503 Service Unavailable")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_connection_reset_is_transient(self):
        error = Exception("Connection reset by peer")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_chinese_timeout_is_transient(self):
        error = Exception("连接超时，请稍后重试")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_chinese_rate_limit_is_transient(self):
        error = Exception("请求被限流")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    # ---- PERMANENT（永久错误）----

    def test_permission_denied_is_permanent(self):
        error = Exception("Permission denied: /etc/shadow")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_403_is_permanent(self):
        error = Exception("HTTP 403 Forbidden")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_404_is_permanent(self):
        error = Exception("HTTP 404 Not Found")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_unauthorized_is_permanent(self):
        error = Exception("401 Unauthorized: invalid token")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_access_denied_is_permanent(self):
        error = Exception("Access denied to resource")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_invalid_api_key_is_permanent(self):
        error = Exception("Invalid API key provided")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    # ---- VALIDATION（验证错误）----

    def test_syntax_error_is_validation(self):
        error = Exception("SyntaxError: invalid syntax at line 42")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_test_failed_is_validation(self):
        error = Exception("Test failed: expected 42, got 43")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_type_error_is_validation(self):
        error = Exception("TypeError: cannot concatenate str and int")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_import_error_is_validation(self):
        error = Exception("ImportError: No module named 'requests'")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_chinese_compile_failed_is_validation(self):
        error = Exception("编译失败：缺少分号")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_chinese_test_failed_is_validation(self):
        error = Exception("测试失败：断言不通过")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    def test_assertion_error_is_validation(self):
        error = Exception("AssertionError: x > 0")
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)

    # ---- CONTEXT（上下文错误）----

    def test_token_limit_is_context(self):
        error = Exception("Token limit exceeded: 150000 > 128000")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    def test_context_length_is_context(self):
        error = Exception("Context length exceeded maximum")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    def test_max_tokens_is_context(self):
        error = Exception("Max tokens reached for this model")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    def test_chinese_context_overflow_is_context(self):
        error = Exception("上下文超限，请压缩对话历史")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    def test_prompt_too_long_is_context(self):
        error = Exception("Prompt too long for model context window")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    # ---- 优先级测试 ----

    def test_context_priority_over_transient(self):
        """上下文错误优先于临时错误"""
        error = Exception("Token limit exceeded, timeout occurred")
        self.assertEqual(self.classifier.classify(error), ErrorType.CONTEXT)

    def test_validation_priority_over_permanent(self):
        """验证错误优先于永久错误"""
        error = Exception("SyntaxError in file not found")
        # "not found" 是 PERMANENT，但 "syntax error" 是 VALIDATION
        # 优先级：VALIDATION > PERMANENT
        self.assertEqual(self.classifier.classify(error), ErrorType.VALIDATION)


class TestErrorHandling(unittest.TestCase):
    """测试错误处理动作"""

    def setUp(self):
        self.classifier = ErrorClassifier()

    def test_transient_returns_retry(self):
        error = Exception("Connection timeout")
        action = self.classifier.handle(error, context={"retry_count": 0})
        self.assertEqual(action.action, "retry")
        self.assertEqual(action.retry_delay, 1)
        self.assertEqual(action.retry_count, 1)

    def test_transient_second_retry(self):
        error = Exception("Connection timeout")
        action = self.classifier.handle(error, context={"retry_count": 1})
        self.assertEqual(action.action, "retry")
        self.assertEqual(action.retry_delay, 2)
        self.assertEqual(action.retry_count, 2)

    def test_transient_third_retry(self):
        error = Exception("Connection timeout")
        action = self.classifier.handle(error, context={"retry_count": 2})
        self.assertEqual(action.action, "retry")
        self.assertEqual(action.retry_delay, 4)
        self.assertEqual(action.retry_count, 3)

    def test_transient_exhausted_returns_report_user(self):
        """超过3次重试后返回 report_user"""
        error = Exception("Connection timeout")
        action = self.classifier.handle(error, context={"retry_count": 3})
        self.assertEqual(action.action, "report_user")
        self.assertIn("3次", action.message)

    def test_permanent_returns_report_user(self):
        error = Exception("Permission denied")
        action = self.classifier.handle(error)
        self.assertEqual(action.action, "report_user")
        self.assertIn("不可恢复", action.message)

    def test_validation_returns_fix(self):
        error = Exception("SyntaxError: invalid syntax")
        action = self.classifier.handle(error)
        self.assertEqual(action.action, "fix")
        self.assertIn("修复", action.message)

    def test_context_returns_compress(self):
        error = Exception("Token limit exceeded")
        action = self.classifier.handle(error)
        self.assertEqual(action.action, "compress")
        self.assertIn("压缩", action.message)


class TestExponentialBackoff(unittest.TestCase):
    """测试指数退避"""

    def setUp(self):
        self.classifier = ErrorClassifier()

    def test_first_delay_is_1s(self):
        self.assertEqual(self.classifier.get_retry_delay(0), 1)

    def test_second_delay_is_2s(self):
        self.assertEqual(self.classifier.get_retry_delay(1), 2)

    def test_third_delay_is_4s(self):
        self.assertEqual(self.classifier.get_retry_delay(2), 4)

    def test_fourth_delay_is_8s(self):
        self.assertEqual(self.classifier.get_retry_delay(3), 8)

    def backoff_is_exponential(self):
        """验证退避呈指数增长"""
        delays = [self.classifier.get_retry_delay(i) for i in range(5)]
        self.assertEqual(delays, [1, 2, 4, 8, 16])


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.classifier = ErrorClassifier()

    def test_empty_error_message(self):
        """空错误消息默认为 TRANSIENT"""
        error = Exception("")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_unknown_error_is_transient(self):
        """未知错误默认为 TRANSIENT"""
        error = Exception("Something completely unexpected happened")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

    def test_case_insensitive_matching(self):
        """模式匹配不区分大小写"""
        error = Exception("TIMEOUT occurred")
        self.assertEqual(self.classifier.classify(error), ErrorType.TRANSIENT)

        error = Exception("PERMISSION DENIED")
        self.assertEqual(self.classifier.classify(error), ErrorType.PERMANENT)

    def test_handle_with_no_context(self):
        """不提供 context 时默认 retry_count=0"""
        error = Exception("Connection timeout")
        action = self.classifier.handle(error)
        self.assertEqual(action.action, "retry")
        self.assertEqual(action.retry_count, 1)

    def test_metadata_contains_error_type(self):
        """ErrorAction.metadata 包含 error_type"""
        error = Exception("SyntaxError")
        action = self.classifier.handle(error)
        self.assertEqual(action.metadata.get("error_type"), "validation")


class TestPatternCount(unittest.TestCase):
    """验证模式库覆盖度"""

    def test_total_patterns_at_least_40(self):
        """总模式数 >= 40"""
        from patterns import (
            TRANSIENT_PATTERNS,
            PERMANENT_PATTERNS,
            VALIDATION_PATTERNS,
            CONTEXT_PATTERNS,
        )
        total = (
            len(TRANSIENT_PATTERNS)
            + len(PERMANENT_PATTERNS)
            + len(VALIDATION_PATTERNS)
            + len(CONTEXT_PATTERNS)
        )
        self.assertGreaterEqual(total, 40, f"总模式数 {total} < 40")


if __name__ == "__main__":
    unittest.main(verbosity=2)
