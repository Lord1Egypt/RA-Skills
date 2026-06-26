"""
业务规则引擎 - 基础使用示例
Business Rule Engine - Basic Usage Examples
"""

import sys
import os
import json

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from rule_engine import RuleEngine, Rule, RuleChain, RuleDSL


def example_basic_rule():
    """
    示例1: 基础规则定义和执行
    Example 1: Basic rule definition and execution
    """
    print("=" * 60)
    print("示例1: 基础规则 | Example 1: Basic Rule")
    print("=" * 60)
    
    # 创建规则引擎 | Create rule engine
    engine = RuleEngine()
    
    # 定义规则：老年人折扣 | Senior discount rule
    rule = Rule(
        name="senior_discount",
        condition="age >= 60",
        action={"type": "discount", "value": 0.8},
        description="60岁以上享受8折优惠"
    )
    
    # 添加规则 | Add rule
    engine.add_rule(rule)
    
    print("\n规则定义 | Rule defined:")
    print(f"  名称 | Name: {rule.name}")
    print(f"  条件 | Condition: {rule.condition}")
    print(f"  动作 | Action: {rule.action}")
    
    # 测试场景1：符合条件的老年人
    context1 = {"age": 65, "order_total": 100}
    result1 = engine.evaluate(context1)
    
    print(f"\n场景1 | Scenario 1:")
    print(f"  上下文 | Context: {context1}")
    print(f"  结果 | Result: {json.dumps(result1, indent=4, ensure_ascii=False)}")
    
    # 测试场景2：不符合条件的年轻人
    context2 = {"age": 30, "order_total": 100}
    result2 = engine.evaluate(context2)
    
    print(f"\n场景2 | Scenario 2:")
    print(f"  上下文 | Context: {context2}")
    print(f"  结果 | Result: {json.dumps(result2, indent=4, ensure_ascii=False)}")


def example_complex_rules():
    """
    示例2: 复杂规则组合
    Example 2: Complex rule combination
    """
    print("\n" + "=" * 60)
    print("示例2: 复杂规则 | Example 2: Complex Rules")
    print("=" * 60)
    
    engine = RuleEngine()
    
    # 添加VIP规则 | VIP rule
    engine.add_rule(Rule(
        name="vip_discount",
        condition="vip_level >= 3 and order_amount > 500",
        action={"type": "discount", "value": 0.7},
        priority=10
    ))
    
    # 添加会员规则 | Member rule
    engine.add_rule(Rule(
        name="member_discount",
        condition="is_member == True and order_amount > 100",
        action={"type": "discount", "value": 0.9},
        priority=5
    ))
    
    # 添加新用户奖励 | New user bonus
    engine.add_rule(Rule(
        name="new_user_bonus",
        condition="is_new_user == True",
        action={"type": "bonus", "value": 50},
        priority=8
    ))
    
    print(f"\n已添加 {len(engine.get_rules())} 条规则")
    
    # 场景1：高等级VIP大额订单
    context1 = {
        "vip_level": 4,
        "is_member": True,
        "is_new_user": False,
        "order_amount": 600
    }
    result1 = engine.evaluate(context1)
    
    print(f"\n场景1: VIP大额订单 | VIP large order")
    print(f"  上下文: {json.dumps(context1, ensure_ascii=False)}")
    print(f"  结果:")
    for rule_name, rule_result in result1.items():
        match_status = "✓ 匹配" if rule_result['matched'] else "✗ 不匹配"
        print(f"    {rule_name}: {match_status}")
        if rule_result['matched'] and rule_result['action']:
            print(f"      动作: {json.dumps(rule_result['action'], ensure_ascii=False)}")
    
    # 场景2：新会员首单
    context2 = {
        "vip_level": 1,
        "is_member": True,
        "is_new_user": True,
        "order_amount": 150
    }
    result2 = engine.evaluate(context2)
    
    print(f"\n场景2: 新会员首单 | New member first order")
    print(f"  上下文: {json.dumps(context2, ensure_ascii=False)}")
    print(f"  结果:")
    for rule_name, rule_result in result2.items():
        match_status = "✓ 匹配" if rule_result['matched'] else "✗ 不匹配"
        print(f"    {rule_name}: {match_status}")


def example_rule_chain():
    """
    示例3: 规则链执行
    Example 3: Rule chain execution
    """
    print("\n" + "=" * 60)
    print("示例3: 规则链 | Example 3: Rule Chain")
    print("=" * 60)
    
    # 创建规则链 | Create rule chain
    chain = RuleChain(stop_on_fail=False)
    
    # 添加库存检查规则 | Inventory check
    chain.add_rule(Rule(
        name="check_stock",
        condition="stock >= quantity",
        action={"type": "log", "message": "Stock sufficient"}
    ))
    
    # 添加会员折扣规则 | Member discount
    chain.add_rule(Rule(
        name="member_discount",
        condition="is_member == True",
        action={"type": "discount", "value": 0.95}
    ))
    
    # 添加满减规则 | Full reduction
    chain.add_rule(Rule(
        name="full_reduction",
        condition="(price * quantity) >= 200",
        action={"type": "bonus", "value": 20}
    ))
    
    # 执行场景1：库存充足 + 会员 + 满减
    context1 = {
        "stock": 100,
        "quantity": 2,
        "is_member": True,
        "price": 120,
        "order_total": 240
    }
    
    print("\n场景1: 完整订单流程 | Complete order flow")
    print(f"  初始上下文: {json.dumps(context1, ensure_ascii=False)}")
    
    result1 = chain.execute(context1)
    
    print(f"\n  执行结果:")
    print(f"    成功: {result1['success']}")
    print(f"    执行规则数: {len(result1['executed_rules'])}")
    print(f"    失败规则: {result1['failed_rules']}")
    
    for executed in result1['executed_rules']:
        print(f"    - {executed['name']}: {executed['result']}")


def example_json_rules():
    """
    示例4: JSON规则加载
    Example 4: JSON rules loading
    """
    print("\n" + "=" * 60)
    print("示例4: JSON规则 | Example 4: JSON Rules")
    print("=" * 60)
    
    # 定义JSON规则 | Define JSON rules
    rules_json = '''
    [
        {
            "name": "student_discount",
            "condition": "is_student == True",
            "action": {"type": "discount", "value": 0.85},
            "priority": 5,
            "description": "学生8.5折优惠"
        },
        {
            "name": "first_order_discount",
            "condition": "order_count == 0",
            "action": {"type": "discount", "value": 0.9},
            "priority": 3,
            "description": "首单9折优惠"
        },
        {
            "name": "birthday_bonus",
            "condition": "is_birthday == True",
            "action": {"type": "bonus", "value": 100},
            "priority": 10,
            "description": "生日赠送100积分"
        }
    ]
    '''
    
    print("\nJSON规则定义 | JSON Rules Definition:")
    print(rules_json)
    
    # 加载规则 | Load rules
    engine = RuleEngine()
    engine.load_rules_from_json(rules_json)
    
    print(f"已加载 {len(engine.get_rules())} 条规则")
    
    # 测试场景 | Test scenario
    context = {
        "is_student": True,
        "order_count": 0,
        "is_birthday": True,
        "order_total": 200
    }
    
    result = engine.evaluate(context)
    
    print(f"\n上下文: {json.dumps(context, ensure_ascii=False)}")
    print(f"评估结果:")
    
    for rule_name, rule_result in result.items():
        if rule_result['matched']:
            action_str = json.dumps(rule_result['action'], ensure_ascii=False) if rule_result['action'] else "无"
            print(f"  ✓ {rule_name}: {action_str}")


def example_dsl_parser():
    """
    示例5: DSL规则解析
    Example 5: DSL rule parsing
    """
    print("\n" + "=" * 60)
    print("示例5: DSL规则 | Example 5: DSL Rules")
    print("=" * 60)
    
    # DSL规则文本 | DSL rule text
    dsl_rules = [
        "RULE senior_discount WHEN age >= 60 THEN discount 0.8",
        "RULE vip_discount WHEN is_vip == True and order_total > 100 THEN discount 0.9",
        "RULE new_user WHEN is_new == True THEN bonus 50"
    ]
    
    engine = RuleEngine()
    
    print("\n解析DSL规则 | Parsing DSL Rules:")
    for dsl_text in dsl_rules:
        print(f"\n  DSL: {dsl_text}")
        try:
            rule = RuleDSL.parse(dsl_text)
            print(f"  解析结果 | Parsed:")
            print(f"    名称: {rule.name}")
            print(f"    条件: {rule.condition}")
            print(f"    动作: {rule.action}")
            engine.add_rule(rule)
        except Exception as e:
            print(f"  解析失败 | Parse error: {e}")
    
    # 测试DSL规则
    context = {
        "age": 65,
        "is_vip": True,
        "is_new": True,
        "order_total": 150
    }
    
    print(f"\n测试DSL规则 | Testing DSL Rules:")
    print(f"  上下文: {json.dumps(context, ensure_ascii=False)}")
    
    result = engine.evaluate(context)
    
    print(f"\n  结果:")
    for rule_name, rule_result in result.items():
        status = "✓" if rule_result['matched'] else "✗"
        print(f"    {status} {rule_name}")


def main():
    """运行所有示例 | Run all examples"""
    print("\n" + "=" * 60)
    print("业务规则引擎 - 完整示例")
    print("Business Rule Engine - Complete Examples")
    print("=" * 60)
    
    try:
        example_basic_rule()
        example_complex_rules()
        example_rule_chain()
        example_json_rules()
        example_dsl_parser()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！| All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误 | Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
