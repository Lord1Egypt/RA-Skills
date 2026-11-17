"""
test_pii_redactor.py - PII 脱敏模块单元测试（6 项）

覆盖：
  1. L1 姓名脱敏（含复姓）
  2. L2 身份证脱敏（中文上下文 + 15/18 位）
  3. L3 手机号脱敏（中文上下文）
  4. L4 家庭住址脱敏
  5. 递归脱敏（redact_abstract_data）
  6. 5% 抽样审计（sample_audit）
"""
import sys
import os
import unittest

# 将 scripts/ 目录加入 sys.path
_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)

from pii_redactor import (
    redact, detect_pii, redact_abstract_data, sample_audit,
    L1_NAME_RE, L2_ID_RE, L3_PHONE_RE,
)


class TestPIIL1Name(unittest.TestCase):
    """测试 L1 姓名脱敏（含复姓）。"""

    def test_single_surname_name(self):
        """单姓姓名应被检测并脱敏。"""
        text = "学生张三的成绩优秀"
        masked, detected = redact(text)
        self.assertTrue(detected)
        self.assertNotIn("张三", masked)
        self.assertIn("张", masked)  # 保留姓

    def test_compound_surname_name(self):
        """复姓姓名应被检测并脱敏。"""
        text = "欧阳娜娜提交了作业"
        masked, detected = redact(text)
        self.assertTrue(detected)
        self.assertNotIn("欧阳娜娜", masked)
        self.assertIn("欧", masked)  # 保留复姓首字


class TestPIIL2IDCard(unittest.TestCase):
    """测试 L2 身份证脱敏（中文上下文 + 15/18 位）。"""

    def test_18_digit_id_chinese_context(self):
        """中文上下文中的 18 位身份证应被检测。"""
        text = "身份证是110101199001011234，请登记"
        masked, detected = redact(text)
        self.assertTrue(detected, "中文上下文中的 18 位身份证应被检测")
        self.assertNotIn("110101199001011234", masked)

    def test_15_digit_id(self):
        """15 位旧版身份证应被检测。"""
        text = "旧身份证号110101900101123"
        masked, detected = redact(text)
        self.assertTrue(detected, "15 位身份证应被检测")
        self.assertNotIn("110101900101123", masked)


class TestPIIL3Phone(unittest.TestCase):
    """测试 L3 手机号脱敏（中文上下文）。"""

    def test_phone_chinese_context(self):
        """中文上下文中的手机号应被检测。"""
        text = "手机13812345678，请联系"
        masked, detected = redact(text)
        self.assertTrue(detected, "中文上下文中的手机号应被检测")
        self.assertNotIn("13812345678", masked)
        self.assertIn("138", masked)  # 保留前 3 位
        self.assertIn("5678", masked)  # 保留后 4 位


class TestPIIL4Address(unittest.TestCase):
    """测试 L4 家庭住址脱敏。"""

    def test_address_masking(self):
        """家庭住址中的门牌号应被脱敏。"""
        text = "地址是北京市朝阳区XX路1号"
        masked, detected = redact(text)
        self.assertTrue(detected)


class TestRecursiveRedact(unittest.TestCase):
    """测试递归脱敏（redact_abstract_data）。"""

    def test_recursive_redact_dict(self):
        """嵌套 dict 中的 PII 应被递归脱敏。"""
        data = {
            "student": "张三",
            "info": {
                "phone": "13812345678",
                "note": "身份证110101199001011234",
            },
            "tags": ["机器学习", "张三"],
        }
        redacted, detected = redact_abstract_data(data)
        self.assertTrue(detected)
        self.assertNotIn("13812345678", str(redacted))
        self.assertNotIn("110101199001011234", str(redacted))


class TestSampleAudit(unittest.TestCase):
    """测试 5% 抽样审计（sample_audit）。"""

    def test_sample_audit_pass(self):
        """无 PII 的数据审计应通过。"""
        data = {"topic": "机器学习", "tags": ["AI", "深度学习"]}
        report = sample_audit(data, rate=1.0)  # 100% 抽样
        self.assertEqual(report["compliance"], "pass")
        self.assertFalse(report["pii_detected"])

    def test_sample_audit_fail(self):
        """含 PII 的数据审计应失败。"""
        data = {"student": "张三", "phone": "13812345678"}
        report = sample_audit(data, rate=1.0)
        self.assertEqual(report["compliance"], "fail")
        self.assertTrue(report["pii_detected"])


if __name__ == "__main__":
    unittest.main()
