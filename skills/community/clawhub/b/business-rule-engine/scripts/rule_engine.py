"""
业务规则引擎 - 核心实现
Business Rule Engine - Core Implementation
"""

import json
import re
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum


class Operator(Enum):
    """运算符枚举 | Operator enumeration"""
    EQ = "=="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    AND = "and"
    OR = "or"
    IN = "in"
    CONTAINS = "contains"


@dataclass
class Rule:
    """规则类 | Rule class"""
    name: str
    condition: str
    action: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 | Convert to dict"""
        return {
            "name": self.name,
            "condition": self.condition,
            "action": self.action,
            "priority": self.priority,
            "enabled": self.enabled,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        """从字典创建 | Create from dict"""
        return cls(
            name=data["name"],
            condition=data["condition"],
            action=data.get("action", {}),
            priority=data.get("priority", 0),
            enabled=data.get("enabled", True),
            description=data.get("description", "")
        )


class ExpressionEvaluator:
    """表达式求值器 | Expression evaluator"""
    
    def __init__(self, context: Dict[str, Any]):
        """
        初始化求值器
        Initialize evaluator
        
        Args:
            context: 变量上下文 | Variable context
        """
        self.context = context
    
    def evaluate(self, expression: str) -> bool:
        """
        评估表达式
        Evaluate expression
        
        Args:
            expression: 条件表达式 | Condition expression
            
        Returns:
            评估结果 | Evaluation result
        """
        try:
            # 安全的表达式求值 | Safe expression evaluation
            return self._safe_eval(expression)
        except Exception as e:
            return False
    
    def _safe_eval(self, expression: str) -> bool:
        """安全求值 | Safe evaluation"""
        # 替换变量 | Replace variables
        expr = self._replace_variables(expression)
        
        # 解析逻辑运算符 | Parse logical operators
        expr = self._parse_logical_operators(expr)
        
        # 安全求值 | Safe evaluation
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            return bool(result)
        except:
            return False
    
    def _replace_variables(self, expression: str) -> str:
        """替换变量 | Replace variables"""
        # 按长度降序排序变量名，避免部分匹配
        sorted_vars = sorted(self.context.keys(), key=len, reverse=True)
        
        result = expression
        for var_name in sorted_vars:
            value = self.context[var_name]
            str_value = self._value_to_string(value)
            result = result.replace(var_name, str_value)
        
        return result
    
    def _value_to_string(self, value: Any) -> str:
        """值转字符串 | Value to string"""
        if isinstance(value, str):
            return repr(value)
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif value is None:
            return "None"
        else:
            return repr(str(value))
    
    def _parse_logical_operators(self, expression: str) -> str:
        """解析逻辑运算符 | Parse logical operators"""
        # 替换 and/or | Replace and/or
        expr = expression.replace(" and ", " and ").replace(" or ", " or ")
        return expr


class RuleEngine:
    """规则引擎类 | Rule engine class"""
    
    def __init__(self):
        """初始化规则引擎 | Initialize rule engine"""
        self.rules: List[Rule] = []
        self.actions: Dict[str, Callable] = {}
        self._register_default_actions()
    
    def _register_default_actions(self):
        """注册默认动作 | Register default actions"""
        self.actions["discount"] = self._action_discount
        self.actions["bonus"] = self._action_bonus
        self.actions["log"] = self._action_log
    
    def add_rule(self, rule: Rule) -> None:
        """
        添加规则
        Add rule
        
        Args:
            rule: 规则对象 | Rule object
        """
        self.rules.append(rule)
        # 按优先级排序 | Sort by priority
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, name: str) -> bool:
        """
        移除规则
        Remove rule
        
        Args:
            name: 规则名称 | Rule name
            
        Returns:
            是否成功移除 | Whether successfully removed
        """
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                self.rules.pop(i)
                return True
        return False
    
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估所有规则
        Evaluate all rules
        
        Args:
            context: 评估上下文 | Evaluation context
            
        Returns:
            规则执行结果 | Rule execution results
        """
        results = {}
        evaluator = ExpressionEvaluator(context)
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            # 评估条件 | Evaluate condition
            matched = evaluator.evaluate(rule.condition)
            
            results[rule.name] = {
                "matched": matched,
                "action": None
            }
            
            if matched and rule.action:
                # 执行动作 | Execute action
                action_result = self._execute_action(rule.action, context)
                results[rule.name]["action"] = action_result
        
        return results
    
    def evaluate_single(self, rule_name: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        评估单个规则
        Evaluate single rule
        
        Args:
            rule_name: 规则名称 | Rule name
            context: 评估上下文 | Evaluation context
            
        Returns:
            规则执行结果 | Rule execution result
        """
        for rule in self.rules:
            if rule.name == rule_name and rule.enabled:
                evaluator = ExpressionEvaluator(context)
                matched = evaluator.evaluate(rule.condition)
                
                result = {
                    "matched": matched,
                    "action": None
                }
                
                if matched and rule.action:
                    result["action"] = self._execute_action(rule.action, context)
                
                return result
        
        return None
    
    def _execute_action(self, action: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """执行动作 | Execute action"""
        action_type = action.get("type", "")
        
        if action_type in self.actions:
            return self.actions[action_type](action, context)
        
        return action
    
    def _action_discount(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """折扣动作 | Discount action"""
        value = action.get("value", 1.0)
        order_total = context.get("order_total", 0)
        discounted = order_total * value
        
        return {
            "type": "discount",
            "original": order_total,
            "discounted": round(discounted, 2),
            "savings": round(order_total - discounted, 2)
        }
    
    def _action_bonus(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """奖励动作 | Bonus action"""
        value = action.get("value", 0)
        
        return {
            "type": "bonus",
            "bonus_amount": value,
            "applied": True
        }
    
    def _action_log(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """日志动作 | Log action"""
        message = action.get("message", "")
        
        return {
            "type": "log",
            "message": message,
            "logged": True
        }
    
    def register_action(self, name: str, handler: Callable) -> None:
        """
        注册自定义动作
        Register custom action
        
        Args:
            name: 动作名称 | Action name
            handler: 动作处理函数 | Action handler
        """
        self.actions[name] = handler
    
    def load_rules_from_json(self, json_str: str) -> None:
        """
        从JSON加载规则
        Load rules from JSON
        
        Args:
            json_str: JSON字符串 | JSON string
        """
        rules_data = json.loads(json_str)
        for rule_data in rules_data:
            rule = Rule.from_dict(rule_data)
            self.add_rule(rule)
    
    def export_rules_to_json(self) -> str:
        """
        导出规则为JSON
        Export rules to JSON
        
        Returns:
            JSON字符串 | JSON string
        """
        rules_data = [rule.to_dict() for rule in self.rules]
        return json.dumps(rules_data, indent=2, ensure_ascii=False)
    
    def get_rules(self) -> List[Rule]:
        """获取所有规则 | Get all rules"""
        return self.rules.copy()
    
    def clear_rules(self) -> None:
        """清空所有规则 | Clear all rules"""
        self.rules.clear()


class RuleChain:
    """规则链类 | Rule chain class"""
    
    def __init__(self, stop_on_fail: bool = True):
        """
        初始化规则链
        Initialize rule chain
        
        Args:
            stop_on_fail: 失败时是否停止 | Whether to stop on failure
        """
        self.rules: List[Rule] = []
        self.stop_on_fail = stop_on_fail
        self.context_transformers: List[Callable] = []
    
    def add_rule(self, rule: Rule) -> None:
        """添加规则 | Add rule"""
        self.rules.append(rule)
    
    def add_transformer(self, transformer: Callable) -> None:
        """添加上下文转换器 | Add context transformer"""
        self.context_transformers.append(transformer)
    
    def execute(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行规则链
        Execute rule chain
        
        Args:
            initial_context: 初始上下文 | Initial context
            
        Returns:
            执行结果 | Execution results
        """
        context = initial_context.copy()
        results = {
            "success": True,
            "executed_rules": [],
            "failed_rules": [],
            "final_context": context
        }
        
        # 应用转换器 | Apply transformers
        for transformer in self.context_transformers:
            context = transformer(context)
        
        engine = RuleEngine()
        
        for rule in self.rules:
            engine.clear_rules()
            engine.add_rule(rule)
            
            rule_result = engine.evaluate_single(rule.name, context)
            
            if rule_result:
                if rule_result["matched"]:
                    results["executed_rules"].append({
                        "name": rule.name,
                        "result": rule_result
                    })
                    
                    # 更新上下文 | Update context
                    if rule_result.get("action"):
                        context[f"{rule.name}_result"] = rule_result["action"]
                else:
                    results["failed_rules"].append(rule.name)
                    
                    if self.stop_on_fail:
                        results["success"] = False
                        break
        
        results["final_context"] = context
        return results


# 简单的DSL解析器 | Simple DSL parser
class RuleDSL:
    """规则DSL解析器 | Rule DSL parser"""
    
    @staticmethod
    def parse(rule_text: str) -> Rule:
        """
        解析规则文本
        Parse rule text
        
        Args:
            rule_text: 规则文本 | Rule text
            
        Returns:
            规则对象 | Rule object
        """
        # 简单解析: RULE name WHEN condition THEN action
        pattern = r'RULE\s+(\w+)\s+WHEN\s+(.+?)\s+THEN\s+(.+)'
        match = re.match(pattern, rule_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            name = match.group(1)
            condition = match.group(2).strip()
            action_text = match.group(3).strip()
            
            # 解析动作 | Parse action
            action = RuleDSL._parse_action(action_text)
            
            return Rule(name=name, condition=condition, action=action)
        
        raise ValueError(f"Invalid rule syntax: {rule_text}")
    
    @staticmethod
    def _parse_action(action_text: str) -> Dict[str, Any]:
        """解析动作文本 | Parse action text"""
        # 简单解析: discount 0.9 或 bonus 50
        parts = action_text.split()
        
        if len(parts) >= 2:
            action_type = parts[0]
            try:
                value = float(parts[1])
            except:
                value = parts[1]
            
            return {"type": action_type, "value": value}
        
        return {"type": action_text}


if __name__ == '__main__':
    # 简单演示
    print("业务规则引擎演示 | Business Rule Engine Demo")
    print("=" * 50)
    
    # 创建引擎 | Create engine
    engine = RuleEngine()
    
    # 添加规则 | Add rules
    engine.add_rule(Rule(
        name="senior_discount",
        condition="age >= 60",
        action={"type": "discount", "value": 0.8}
    ))
    
    engine.add_rule(Rule(
        name="vip_discount",
        condition="is_vip == True and order_total > 100",
        action={"type": "discount", "value": 0.9}
    ))
    
    # 评估 | Evaluate
    context = {"age": 65, "is_vip": True, "order_total": 200}
    result = engine.evaluate(context)
    
    print(f"\n上下文 | Context: {context}")
    print(f"评估结果 | Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
