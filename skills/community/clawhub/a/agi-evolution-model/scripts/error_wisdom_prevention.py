#!/usr/bin/env python3
"""
预防规则引擎 (Error Wisdom Prevention Engine)

功能：
- 工具调用前置检查
- 预防规则执行
- 自动修正
- 预防效果验证
- 与感知节点集成

基于：error_wisdom_spec.md 规范
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict


# ==================== 数据结构 ====================

@dataclass
class CheckResult:
    """检查结果"""
    pass_check: bool
    rule_id: str = ""
    message: str = ""
    severity: str = "medium"
    auto_fix_available: bool = False
    auto_fix: Optional[Dict[str, Any]] = None
    suggestion: str = ""


@dataclass
class PreventionResult:
    """预防执行结果"""
    success: bool
    original_params: Dict[str, Any]
    modified_params: Dict[str, Any]
    checks_performed: List[CheckResult]
    warnings: List[str]
    auto_fixes_applied: Dict[str, Any]
    trace_id: str = ""


# ==================== 内置预防规则 ====================

class BuiltinPreventionRules:
    """内置预防规则集"""
    
    @staticmethod
    def enum_validation(params: dict, tool_schema: dict) -> CheckResult:
        """
        枚举参数验证规则
        
        检查参数值是否在允许的枚举范围内
        """
        if not tool_schema:
            return CheckResult(pass_check=True)
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            enum_values = param_def.get("enum", [])
            
            if enum_values and param_value not in enum_values:
                # 尝试找到最接近的值（不区分大小写）
                closest = None
                if isinstance(param_value, str):
                    for enum_val in enum_values:
                        if isinstance(enum_val, str) and enum_val.lower() == param_value.lower():
                            closest = enum_val
                            break
                
                if closest:
                    return CheckResult(
                        pass_check=False,
                        rule_id="builtin_enum_validation",
                        message=f"参数 '{param_name}' 值 '{param_value}' 不在枚举范围内",
                        severity="mild",
                        auto_fix_available=True,
                        auto_fix={param_name: closest},
                        suggestion=f"已自动修正为 '{closest}'"
                    )
                else:
                    return CheckResult(
                        pass_check=False,
                        rule_id="builtin_enum_validation",
                        message=f"参数 '{param_name}' 值 '{param_value}' 不在允许范围内",
                        severity="moderate",
                        auto_fix_available=False,
                        suggestion=f"请使用以下值之一: {enum_values}"
                    )
        
        return CheckResult(pass_check=True)
    
    @staticmethod
    def required_params_check(params: dict, tool_schema: dict) -> CheckResult:
        """
        必需参数检查规则
        
        检查是否提供了所有必需参数
        """
        if not tool_schema:
            return CheckResult(pass_check=True)
        
        required = tool_schema.get("parameters", {}).get("required", [])
        missing = [r for r in required if r not in params]
        
        if missing:
            return CheckResult(
                pass_check=False,
                rule_id="builtin_required_params",
                message=f"缺少必需参数: {missing}",
                severity="severe",
                auto_fix_available=False,
                suggestion=f"请提供以下参数: {missing}"
            )
        
        return CheckResult(pass_check=True)
    
    @staticmethod
    def type_validation(params: dict, tool_schema: dict) -> CheckResult:
        """
        类型验证规则
        
        检查参数类型是否匹配schema定义
        """
        if not tool_schema:
            return CheckResult(pass_check=True)
        
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            expected_type = param_def.get("type")
            
            if expected_type:
                expected = type_mapping.get(expected_type)
                if expected and not isinstance(param_value, expected):
                    return CheckResult(
                        pass_check=False,
                        rule_id="builtin_type_validation",
                        message=f"参数 '{param_name}' 类型不匹配，期望 {expected_type}，实际 {type(param_value).__name__}",
                        severity="moderate",
                        auto_fix_available=False,
                        suggestion=f"请提供 {expected_type} 类型的值"
                    )
        
        return CheckResult(pass_check=True)
    
    @staticmethod
    def range_validation(params: dict, tool_schema: dict) -> CheckResult:
        """
        数值范围验证规则
        
        检查数值参数是否在允许范围内
        """
        if not tool_schema:
            return CheckResult(pass_check=True)
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            
            if not isinstance(param_value, (int, float)):
                continue
            
            minimum = param_def.get("minimum")
            maximum = param_def.get("maximum")
            exclusive_minimum = param_def.get("exclusiveMinimum")
            exclusive_maximum = param_def.get("exclusiveMaximum")
            
            if minimum is not None and param_value < minimum:
                return CheckResult(
                    pass_check=False,
                    rule_id="builtin_range_validation",
                    message=f"参数 '{param_name}' 值 {param_value} 小于最小值 {minimum}",
                    severity="moderate",
                    auto_fix_available=True,
                    auto_fix={param_name: minimum},
                    suggestion=f"已自动修正为最小值 {minimum}"
                )
            
            if maximum is not None and param_value > maximum:
                return CheckResult(
                    pass_check=False,
                    rule_id="builtin_range_validation",
                    message=f"参数 '{param_name}' 值 {param_value} 大于最大值 {maximum}",
                    severity="moderate",
                    auto_fix_available=True,
                    auto_fix={param_name: maximum},
                    suggestion=f"已自动修正为最大值 {maximum}"
                )
        
        return CheckResult(pass_check=True)
    
    @staticmethod
    def format_validation(params: dict, tool_schema: dict) -> CheckResult:
        """
        格式验证规则
        
        检查字符串参数是否符合指定格式
        """
        if not tool_schema:
            return CheckResult(pass_check=True)
        
        import re
        
        format_patterns = {
            "date": r"^\d{4}-\d{2}-\d{2}$",
            "date-time": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "uri": r"^https?://"
        }
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            param_format = param_def.get("format")
            
            if param_format and isinstance(param_value, str):
                pattern = format_patterns.get(param_format)
                
                if pattern and not re.match(pattern, param_value):
                    return CheckResult(
                        pass_check=False,
                        rule_id="builtin_format_validation",
                        message=f"参数 '{param_name}' 格式不正确，期望 {param_format} 格式",
                        severity="mild",
                        auto_fix_available=False,
                        suggestion=f"请使用正确的 {param_format} 格式"
                    )
        
        return CheckResult(pass_check=True)


# ==================== 预防规则引擎 ====================

class PreventionEngine:
    """
    预防规则引擎
    
    负责：
    - 执行内置预防规则
    - 执行自定义预防规则
    - 自动修正参数
    - 记录预防效果
    """
    
    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        
        # 内置规则（按优先级排序）
        self.builtin_rules = [
            ("required_params_check", BuiltinPreventionRules.required_params_check, "critical"),
            ("enum_validation", BuiltinPreventionRules.enum_validation, "high"),
            ("type_validation", BuiltinPreventionRules.type_validation, "high"),
            ("range_validation", BuiltinPreventionRules.range_validation, "medium"),
            ("format_validation", BuiltinPreventionRules.format_validation, "low")
        ]
        
        # 统计
        self.stats = {
            "checks_performed": 0,
            "errors_prevented": 0,
            "auto_fixes_applied": 0
        }
    
    def check(
        self,
        tool_name: str,
        params: dict,
        tool_schema: dict = None,
        custom_rules: List[dict] = None
    ) -> PreventionResult:
        """
        执行预防检查
        
        Args:
            tool_name: 工具名称
            params: 调用参数
            tool_schema: 工具schema
            custom_rules: 自定义规则（可选）
        
        Returns:
            预防执行结果
        """
        checks_performed = []
        warnings = []
        auto_fixes_applied = {}
        modified_params = params.copy()
        
        # 1. 执行内置规则
        for rule_name, rule_func, severity in self.builtin_rules:
            result = rule_func(modified_params, tool_schema)
            result.severity = severity  # 使用预设优先级
            
            checks_performed.append(result)
            self.stats["checks_performed"] += 1
            
            if not result.pass_check:
                # 应用自动修正
                if result.auto_fix_available and result.auto_fix:
                    modified_params.update(result.auto_fix)
                    auto_fixes_applied.update(result.auto_fix)
                    self.stats["auto_fixes_applied"] += 1
                    self.stats["errors_prevented"] += 1
                else:
                    warnings.append(f"[{severity}] {result.message}")
        
        # 2. 执行自定义规则（如果有）
        if custom_rules:
            for custom_rule in custom_rules:
                result = self._execute_custom_rule(custom_rule, modified_params, tool_schema)
                checks_performed.append(result)
                self.stats["checks_performed"] += 1
                
                if not result.pass_check:
                    if result.auto_fix_available and result.auto_fix:
                        modified_params.update(result.auto_fix)
                        auto_fixes_applied.update(result.auto_fix)
                        self.stats["auto_fixes_applied"] += 1
                        self.stats["errors_prevented"] += 1
                    else:
                        warnings.append(f"[{result.severity}] {result.message}")
        
        # 3. 判断整体是否通过
        all_passed = all(c.pass_check or c.auto_fix_available for c in checks_performed)
        
        return PreventionResult(
            success=all_passed,
            original_params=params,
            modified_params=modified_params,
            checks_performed=checks_performed,
            warnings=warnings,
            auto_fixes_applied=auto_fixes_applied
        )
    
    def _execute_custom_rule(self, rule: dict, params: dict, tool_schema: dict) -> CheckResult:
        """执行自定义规则"""
        rule_type = rule.get("type", "generic")
        
        if rule_type == "enum":
            return BuiltinPreventionRules.enum_validation(params, tool_schema)
        elif rule_type == "required":
            return BuiltinPreventionRules.required_params_check(params, tool_schema)
        elif rule_type == "range":
            return BuiltinPreventionRules.range_validation(params, tool_schema)
        
        # 通用规则执行
        condition = rule.get("condition", "")
        check = rule.get("check", "")
        
        # 简化实现：返回通过
        return CheckResult(pass_check=True)
    
    def quick_check(self, tool_name: str, params: dict, tool_schema: dict = None) -> dict:
        """
        快速检查（轻量级接口）
        
        Args:
            tool_name: 工具名称
            params: 调用参数
            tool_schema: 工具schema
        
        Returns:
            {
                "pass": bool,
                "warnings": [],
                "auto_fixes": {},
                "suggestions": []
            }
        """
        result = self.check(tool_name, params, tool_schema)
        
        return {
            "pass": result.success,
            "warnings": result.warnings,
            "auto_fixes": result.auto_fixes_applied,
            "suggestions": [c.suggestion for c in result.checks_performed if c.suggestion]
        }
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "checks_performed": 0,
            "errors_prevented": 0,
            "auto_fixes_applied": 0
        }


# ==================== 工具调用包装器 ====================

class ToolCallWrapper:
    """
    工具调用包装器
    
    在工具调用前后执行预防检查和错误记录
    """
    
    def __init__(self, prevention_engine: PreventionEngine, error_wisdom_manager):
        """
        初始化
        
        Args:
            prevention_engine: 预防引擎
            error_wisdom_manager: 错误智慧库管理器
        """
        self.prevention_engine = prevention_engine
        self.error_wisdom_manager = error_wisdom_manager
    
    def wrap_tool_call(
        self,
        tool_name: str,
        tool_func: Callable,
        params: dict,
        tool_schema: dict = None,
        trace_id: str = ""
    ) -> dict:
        """
        包装工具调用
        
        Args:
            tool_name: 工具名称
            tool_func: 工具函数
            params: 调用参数
            tool_schema: 工具schema
            trace_id: 追踪ID
        
        Returns:
            工具调用结果
        """
        # 1. 前置检查
        pre_check_result = self.prevention_engine.quick_check(tool_name, params, tool_schema)
        
        # 应用自动修正
        if pre_check_result["auto_fixes"]:
            params = params.copy()
            params.update(pre_check_result["auto_fixes"])
        
        # 检查是否有严重错误
        if not pre_check_result["pass"]:
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "PREVENTION_CHECK_FAILED",
                    "message": "; ".join(pre_check_result["warnings"]),
                    "suggestions": pre_check_result["suggestions"]
                },
                "metadata": {
                    "prevention_triggered": True,
                    "trace_id": trace_id
                }
            }
        
        # 2. 执行工具调用
        try:
            result = tool_func(**params)
            
            # 检查结果是否有错误
            if isinstance(result, dict) and result.get("success") is False:
                # 记录错误
                self._record_tool_error(tool_name, params, result, trace_id)
            
            return result
            
        except Exception as e:
            # 记录异常
            error_result = {
                "success": False,
                "status": "error",
                "error": {
                    "code": "TOOL_EXCEPTION",
                    "message": str(e)
                }
            }
            
            self._record_tool_error(tool_name, params, error_result, trace_id)
            
            return error_result
    
    def _record_tool_error(
        self,
        tool_name: str,
        params: dict,
        error_result: dict,
        trace_id: str
    ):
        """记录工具错误"""
        if not self.error_wisdom_manager:
            return
        
        error_code = error_result.get("error", {}).get("code", "UNKNOWN")
        error_message = error_result.get("error", {}).get("message", "")
        
        # 记录到错误智慧库
        self.error_wisdom_manager.record_error(
            error_type="工具性错误",
            error_subtype="调用失败类",
            error_code=error_code,
            error_description=f"工具 {tool_name} 调用失败: {error_message}",
            root_cause=f"参数: {params}",
            solution="检查参数和工具状态",
            prevention_strategy="前置参数验证",
            trace_id=trace_id,
            severity="moderate",
            trigger_scenario=f"工具调用: {tool_name}"
        )


# ==================== 便捷函数 ====================

def create_prevention_engine(memory_dir: str = "./agi_memory") -> PreventionEngine:
    """
    创建预防引擎实例
    
    Args:
        memory_dir: 记忆存储目录
    
    Returns:
        预防引擎实例
    """
    return PreventionEngine(memory_dir)


def quick_pre_check(
    tool_name: str,
    params: dict,
    tool_schema: dict = None,
    memory_dir: str = "./agi_memory"
) -> dict:
    """
    快速预防检查（便捷函数）
    
    Args:
        tool_name: 工具名称
        params: 调用参数
        tool_schema: 工具schema
        memory_dir: 记忆存储目录
    
    Returns:
        检查结果
    """
    engine = PreventionEngine(memory_dir)
    return engine.quick_check(tool_name, params, tool_schema)


# ==================== CLI 接口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="预防规则引擎")
    parser.add_argument("--memory-dir", default="./agi_memory", help="记忆存储目录")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="执行预防检查")
    check_parser.add_argument("--tool-name", required=True, help="工具名称")
    check_parser.add_argument("--params", required=True, help="参数（JSON格式）")
    check_parser.add_argument("--schema", help="工具schema（JSON文件路径）")
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计")
    
    args = parser.parse_args()
    
    engine = PreventionEngine(args.memory_dir)
    
    if args.command == "check":
        params = json.loads(args.params)
        
        tool_schema = None
        if args.schema:
            with open(args.schema, 'r', encoding='utf-8') as f:
                tool_schema = json.load(f)
        
        result = engine.quick_check(args.tool_name, params, tool_schema)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = engine.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
