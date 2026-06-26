"""
业务规则引擎 - 单元测试
Business Rule Engine - Unit Tests
"""

import unittest
import sys
import os
import json

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from rule_engine import RuleEngine, Rule, RuleChain, ExpressionEvaluator, RuleDSL, BackupResult


class TestRule(unittest.TestCase):
    """规则类测试"""
    
    def test_rule_init(self):
        """测试规则初始化"""
        rule = Rule(
            name="test_rule",
            condition="age > 18",
            action={"type": "allow"},
            priority=5
        )
        
        self.assertEqual(rule.name, "test_rule")
        self.assertEqual(rule.condition, "age > 18")
        self.assertEqual(rule.action, {"type": "allow"})
        self.assertEqual(rule.priority, 5)
        self.assertTrue(rule.enabled)
    
    def test_rule_to_dict(self):
        """测试规则转字典"""
        rule = Rule(name="test", condition="x > 0", action={"type": "test"})
        data = rule.to_dict()
        
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["condition"], "x > 0")
        self.assertEqual(data["action"], {"type": "test"})
    
    def test_rule_from_dict(self):
        """测试从字典创建规则"""
        data = {
            "name": "test",
            "condition": "x > 0",
            "action": {"type": "test"},
            "priority": 3,
            "enabled": False
        }
        
        rule = Rule.from_dict(data)
        
        self.assertEqual(rule.name, "test")
        self.assertEqual(rule.priority, 3)
        self.assertFalse(rule.enabled)


class TestExpressionEvaluator(unittest.TestCase):
    """表达式求值器测试"""
    
    def test_simple_comparison(self):
        """测试简单比较"""
        context = {"age": 25, "score": 85}
        evaluator = ExpressionEvaluator(context)
        
        self.assertTrue(evaluator.evaluate("age > 18"))
        self.assertTrue(evaluator.evaluate("score >= 80"))
        self.assertFalse(evaluator.evaluate("age < 20"))
    
    def test_logical_operators(self):
        """测试逻辑运算符"""
        context = {"is_member": True, "age": 25, "is_vip": False}
        evaluator = ExpressionEvaluator(context)
        
        self.assertTrue(evaluator.evaluate("is_member == True and age > 18"))
        self.assertFalse(evaluator.evaluate("is_member == True and is_vip == True"))
        self.assertTrue(evaluator.evaluate("is_member == True or is_vip == True"))
    
    def test_string_comparison(self):
        """测试字符串比较"""
        context = {"role": "admin", "status": "active"}
        evaluator = ExpressionEvaluator(context)
        
        self.assertTrue(evaluator.evaluate("role == 'admin'"))
        self.assertTrue(evaluator.evaluate("status == 'active'"))
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        context = {
            "vip_level": 3,
            "order_amount": 600,
            "is_new_user": False
        }
        evaluator = ExpressionEvaluator(context)
        
        self.assertTrue(evaluator.evaluate("vip_level >= 3 and order_amount > 500"))
        self.assertFalse(evaluator.evaluate("vip_level >= 3 and is_new_user == True"))


class TestRuleEngine(unittest.TestCase):
    """规则引擎测试"""
    
    def setUp(self):
        """测试前准备"""
        self.engine = RuleEngine()
    
    def test_add_rule(self):
        """测试添加规则"""
        rule = Rule(name="test", condition="x > 0", action={"type": "test"})
        self.engine.add_rule(rule)
        
        self.assertEqual(len(self.engine.get_rules()), 1)
        self.assertEqual(self.engine.get_rules()[0].name, "test")
    
    def test_remove_rule(self):
        """测试移除规则"""
        rule = Rule(name="test", condition="x > 0", action={"type": "test"})
        self.engine.add_rule(rule)
        
        removed = self.engine.remove_rule("test")
        self.assertTrue(removed)
        self.assertEqual(len(self.engine.get_rules()), 0)
        
        # 移除不存在的规则
        removed = self.engine.remove_rule("nonexistent")
        self.assertFalse(removed)
    
    def test_evaluate_single_rule(self):
        """测试单规则评估"""
        rule = Rule(name="age_check", condition="age >= 18", action={"type": "allow"})
        self.engine.add_rule(rule)
        
        # 匹配
        result = self.engine.evaluate_single("age_check", {"age": 25})
        self.assertIsNotNone(result)
        self.assertTrue(result["matched"])
        
        # 不匹配
        result = self.engine.evaluate_single("age_check", {"age": 15})
        self.assertIsNotNone(result)
        self.assertFalse(result["matched"])
    
    def test_evaluate_multiple_rules(self):
        """测试多规则评估"""
        self.engine.add_rule(Rule(name="rule1", condition="x > 0", action={"type": "a"}))
        self.engine.add_rule(Rule(name="rule2", condition="x > 10", action={"type": "b"}))
        
        result = self.engine.evaluate({"x": 15})
        
        self.assertTrue(result["rule1"]["matched"])
        self.assertTrue(result["rule2"]["matched"])
    
    def test_priority_sorting(self):
        """测试优先级排序"""
        self.engine.add_rule(Rule(name="low", condition="x > 0", priority=1))
        self.engine.add_rule(Rule(name="high", condition="x > 0", priority=10))
        self.engine.add_rule(Rule(name="medium", condition="x > 0", priority=5))
        
        rules = self.engine.get_rules()
        self.assertEqual(rules[0].name, "high")
        self.assertEqual(rules[1].name, "medium")
        self.assertEqual(rules[2].name, "low")
    
    def test_disabled_rule(self):
        """测试禁用规则"""
        rule = Rule(name="disabled", condition="x > 0", enabled=False)
        self.engine.add_rule(rule)
        
        result = self.engine.evaluate({"x": 10})
        self.assertNotIn("disabled", result)
    
    def test_json_load_export(self):
        """测试JSON加载和导出"""
        rules = [
            {"name": "rule1", "condition": "x > 0", "action": {"type": "a"}, "priority": 1},
            {"name": "rule2", "condition": "y < 10", "action": {"type": "b"}, "priority": 2}
        ]
        
        self.engine.load_rules_from_json(json.dumps(rules))
        self.assertEqual(len(self.engine.get_rules()), 2)
        
        # 导出验证
        exported = self.engine.export_rules_to_json()
        exported_data = json.loads(exported)
        self.assertEqual(len(exported_data), 2)
    
    def test_clear_rules(self):
        """测试清空规则"""
        self.engine.add_rule(Rule(name="test", condition="x > 0"))
        self.assertEqual(len(self.engine.get_rules()), 1)
        
        self.engine.clear_rules()
        self.assertEqual(len(self.engine.get_rules()), 0)


class TestRuleChain(unittest.TestCase):
    """规则链测试"""
    
    def test_chain_execution(self):
        """测试规则链执行"""
        chain = RuleChain(stop_on_fail=False)
        
        chain.add_rule(Rule(name="step1", condition="x > 0", action={"type": "a"}))
        chain.add_rule(Rule(name="step2", condition="y > 0", action={"type": "b"}))
        
        result = chain.execute({"x": 10, "y": 20})
        
        self.assertTrue(result["success"])
        self.assertEqual(len(result["executed_rules"]), 2)
    
    def test_chain_stop_on_fail(self):
        """测试失败时停止"""
        chain = RuleChain(stop_on_fail=True)
        
        chain.add_rule(Rule(name="pass", condition="x > 0"))
        chain.add_rule(Rule(name="fail", condition="x > 100"))  # 会失败
        chain.add_rule(Rule(name="never", condition="x > 0"))  # 不会执行
        
        result = chain.execute({"x": 50})
        
        self.assertFalse(result["success"])
        self.assertEqual(len(result["executed_rules"]), 1)
        self.assertEqual(len(result["failed_rules"]), 1)
    
    def test_chain_context_update(self):
        """测试上下文更新"""
        chain = RuleChain()
        
        chain.add_rule(Rule(name="calc", condition="x > 0", action={"type": "log"}))
        
        result = chain.execute({"x": 10})
        
        # 检查最终结果
        self.assertIn("final_context", result)


class TestRuleDSL(unittest.TestCase):
    """DSL解析器测试"""
    
    def test_parse_simple_rule(self):
        """测试解析简单规则"""
        dsl = "RULE test WHEN x > 0 THEN action"
        rule = RuleDSL.parse(dsl)
        
        self.assertEqual(rule.name, "test")
        self.assertEqual(rule.condition, "x > 0")
        self.assertEqual(rule.action["type"], "action")
    
    def test_parse_discount_rule(self):
        """测试解析折扣规则"""
        dsl = "RULE senior WHEN age >= 60 THEN discount 0.8"
        rule = RuleDSL.parse(dsl)
        
        self.assertEqual(rule.name, "senior")
        self.assertEqual(rule.condition, "age >= 60")
        self.assertEqual(rule.action["type"], "discount")
        self.assertEqual(rule.action["value"], 0.8)
    
    def test_parse_invalid_syntax(self):
        """测试无效语法"""
        with self.assertRaises(ValueError):
            RuleDSL.parse("INVALID RULE")


class TestActions(unittest.TestCase):
    """动作执行测试"""
    
    def setUp(self):
        self.engine = RuleEngine()
    
    def test_discount_action(self):
        """测试折扣动作"""
        self.engine.add_rule(Rule(
            name="discount",
            condition="x > 0",
            action={"type": "discount", "value": 0.8}
        ))
        
        result = self.engine.evaluate({"x": 10, "order_total": 100})
        
        self.assertTrue(result["discount"]["matched"])
        action = result["discount"]["action"]
        self.assertEqual(action["discounted"], 80.0)
        self.assertEqual(action["savings"], 20.0)
    
    def test_bonus_action(self):
        """测试奖励动作"""
        self.engine.add_rule(Rule(
            name="bonus",
            condition="x > 0",
            action={"type": "bonus", "value": 50}
        ))
        
        result = self.engine.evaluate({"x": 10})
        
        action = result["bonus"]["action"]
        self.assertEqual(action["bonus_amount"], 50)
        self.assertTrue(action["applied"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
