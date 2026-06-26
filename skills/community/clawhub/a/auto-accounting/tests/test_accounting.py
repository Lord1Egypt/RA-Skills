#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动记账 Skill 测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.accounting_parser import AccountingParser
from scripts.user_preferences import UserPreferences


class TestAccountingParser:
    """记账解析器测试"""
    
    def __init__(self):
        self.parser = AccountingParser()
        self.passed = 0
        self.failed = 0
    
    def test_wechat_pay(self):
        """测试微信支付截图识别"""
        text = "微信支付成功，向星巴克支付¥28.50，时间：2026-04-02 13:45"
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["is_accounting"] == True, "is_accounting 应为 True"
        assert result["amount"] == 28.50, f"金额应为 28.50，实际为 {result['amount']}"
        assert result["type"] == "支出", f"类型应为支出，实际为 {result['type']}"
        assert result["category"] == "餐饮", f"分类应为餐饮，实际为 {result['category']}"
        
        print("✅ test_wechat_pay 通过")
        self.passed += 1
    
    def test_jd_order(self):
        """测试京东订单识别"""
        text = "京东订单，购买华为耳机，实付款299元"
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["amount"] == 299.0, f"金额应为 299.0，实际为 {result['amount']}"
        assert result["category"] == "购物", f"分类应为购物，实际为 {result['category']}"
        assert "京东" in result["description"], "描述应包含京东"
        
        print("✅ test_jd_order 通过")
        self.passed += 1
    
    def test_meituan_order(self):
        """测试美团外卖订单识别"""
        text = "美团外卖订单，肯德基午餐，实付金额35元"
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["amount"] == 35.0, f"金额应为 35.0，实际为 {result['amount']}"
        assert result["category"] == "餐饮", f"分类应为餐饮，实际为 {result['category']}"
        
        print("✅ test_meituan_order 通过")
        self.passed += 1
    
    def test_alipay_income(self):
        """测试支付宝收款识别"""
        text = "支付宝收款，收到¥100.00，来自张三"
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["amount"] == 100.0, f"金额应为 100.0，实际为 {result['amount']}"
        assert result["type"] == "收入", f"类型应为收入，实际为 {result['type']}"
        
        print("✅ test_alipay_income 通过")
        self.passed += 1
    
    def test_didi_transport(self):
        """测试滴滴出行识别"""
        text = "滴滴出行，打车费用¥25.50"
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["amount"] == 25.50, f"金额应为 25.50，实际为 {result['amount']}"
        assert result["category"] == "交通", f"分类应为交通，实际为 {result['category']}"
        
        print("✅ test_didi_transport 通过")
        self.passed += 1
    
    def test_non_accounting(self):
        """测试非记账图片"""
        text = "这是一张美丽的风景照片，有山有水"
        result = self.parser.parse_image_result(text)
        
        assert result is None, "不应识别为记账信息"
        
        print("✅ test_non_accounting 通过")
        self.passed += 1
    
    def test_gui_query_generation(self):
        """测试 GUI Query 生成"""
        data = {
            "is_accounting": True,
            "amount": 28.50,
            "type": "支出",
            "category": "餐饮",
            "description": "星巴克 - 咖啡"
        }
        query = self.parser.build_gui_query(data)
        
        assert query is not None, "应生成 GUI Query"
        assert "一日记账APP" in query, "Query 应包含一日记账APP"
        assert "28.5" in query, f"Query 应包含金额，实际 Query: {query}"
        assert "餐饮" in query, "Query 应包含分类"
        
        print("✅ test_gui_query_generation 通过")
        self.passed += 1
    
    def test_json_parsing(self):
        """测试 JSON 格式解析"""
        text = '''
        图片分析结果：
        {"is_accounting": true, "amount": 88.00, "type": "支出", "merchant": "海底捞", "description": "火锅"}
        '''
        result = self.parser.parse_image_result(text)
        
        assert result is not None, "应该识别为记账信息"
        assert result["amount"] == 88.0, f"金额应为 88.0，实际为 {result['amount']}"
        
        print("✅ test_json_parsing 通过")
        self.passed += 1
    
    def run_all(self):
        """运行所有测试"""
        print("=" * 50)
        print("开始运行测试...")
        print("=" * 50)
        
        tests = [
            self.test_wechat_pay,
            self.test_jd_order,
            self.test_meituan_order,
            self.test_alipay_income,
            self.test_didi_transport,
            self.test_non_accounting,
            self.test_gui_query_generation,
            self.test_json_parsing,
        ]
        
        for test in tests:
            try:
                test()
            except AssertionError as e:
                print(f"❌ {test.__name__} 失败: {e}")
                self.failed += 1
            except Exception as e:
                print(f"❌ {test.__name__} 异常: {e}")
                self.failed += 1
        
        print("=" * 50)
        print(f"测试完成: {self.passed} 通过, {self.failed} 失败")
        print("=" * 50)
        
        return self.failed == 0


class TestUserPreferences:
    """用户偏好测试"""
    
    def __init__(self):
        self.prefs = UserPreferences()
        self.passed = 0
        self.failed = 0
    
    def test_default_values(self):
        """测试默认值"""
        assert self.prefs.get("default_payment_method") == "微信支付"
        assert self.prefs.get("large_amount_threshold") == 1000
        print("✅ test_default_values 通过")
        self.passed += 1
    
    def test_confirm_threshold(self):
        """测试大额确认阈值"""
        assert self.prefs.should_confirm_before_save(500) == False
        assert self.prefs.should_confirm_before_save(1500) == True
        print("✅ test_confirm_threshold 通过")
        self.passed += 1
    
    def test_set_get(self):
        """测试设置和获取"""
        self.prefs.set("test_key", "test_value")
        assert self.prefs.get("test_key") == "test_value"
        print("✅ test_set_get 通过")
        self.passed += 1
    
    def run_all(self):
        """运行所有测试"""
        print("=" * 50)
        print("开始运行用户偏好测试...")
        print("=" * 50)
        
        tests = [
            self.test_default_values,
            self.test_confirm_threshold,
            self.test_set_get,
        ]
        
        for test in tests:
            try:
                test()
            except AssertionError as e:
                print(f"❌ {test.__name__} 失败: {e}")
                self.failed += 1
            except Exception as e:
                print(f"❌ {test.__name__} 异常: {e}")
                self.failed += 1
        
        print("=" * 50)
        print(f"测试完成: {self.passed} 通过, {self.failed} 失败")
        print("=" * 50)
        
        return self.failed == 0


def main():
    """主测试入口"""
    print("\n" + "=" * 50)
    print("自动记账 Skill 测试套件")
    print("=" * 50 + "\n")
    
    # 运行解析器测试
    parser_tests = TestAccountingParser()
    parser_result = parser_tests.run_all()
    
    print()
    
    # 运行偏好测试
    prefs_tests = TestUserPreferences()
    prefs_result = prefs_tests.run_all()
    
    print("\n" + "=" * 50)
    if parser_result and prefs_result:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败")
    print("=" * 50 + "\n")
    
    return parser_result and prefs_result


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
