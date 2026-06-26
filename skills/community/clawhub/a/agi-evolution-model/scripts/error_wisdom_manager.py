#!/usr/bin/env python3
"""
错误智慧库管理器 (Error Wisdom Manager)

功能：
- 错误记录与存储
- 错误分析与归类
- 预防规则生成
- 预防知识查询
- 时效性管理
- 统计与报告

基于：error_wisdom_spec.md 规范
"""

import os
import json
import time
import hashlib
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import math


# ==================== 数据结构 ====================

@dataclass
class ErrorDiscovery:
    """错误发现"""
    错误类型: str  # 工具性错误/认知性错误
    子类型: str
    错误码: str
    错误描述: str
    严重程度: str  # none/mild/moderate/severe/critical
    触发场景: str
    影响范围: str = "单次调用"


@dataclass
class RootCauseAnalysis:
    """原因分析"""
    根本原因: str
    认知偏差: str = ""
    环境因素: str = ""
    责任归属: str = ""
    可预防性: str = "medium"  # high/medium/low


@dataclass
class Solution:
    """解决方案"""
    即时纠错: str
    纠错成本: str = "medium"  # low/medium/high
    有效性: str = "已验证有效"
    用户体验补偿: str = ""


@dataclass
class PreventionRule:
    """前置检查规则"""
    rule_id: str
    condition: str
    check: str
    action: str
    auto_fixable: bool = False
    fix_method: str = ""


@dataclass
class PreventionKnowledge:
    """预防知识"""
    预防策略: str
    前置检查规则: Optional[PreventionRule] = None
    适用场景: List[str] = field(default_factory=list)
    不适用场景: List[str] = field(default_factory=list)
    预防优先级: str = "medium"  # high/medium/low
    预防成本: str = "low"


@dataclass
class ValidationRecord:
    """验证记录"""
    timestamp: str
    trace_id: str
    场景: str
    效果: str  # 成功预防/预防失败/未触发
    预防触发: str = ""
    用户反馈: str = ""  # positive/neutral/negative


@dataclass
class RelatedErrors:
    """关联错误"""
    相似错误ID: List[str] = field(default_factory=list)
    共性模式: str = ""
    抽象规则ID: str = ""


@dataclass
class ErrorWisdomMetadata:
    """元数据"""
    创建时间: str
    最后更新: str
    验证次数: int = 0
    成功预防次数: int = 0
    置信度: float = 0.8
    时效性标记: str = "active"  # active/deprecated/archived


@dataclass
class ErrorWisdomEntry:
    """错误智慧条目"""
    id: str
    timestamp: str
    trace_id: str
    version: str = "1.0"
    错误发现: Optional[ErrorDiscovery] = None
    原因分析: Optional[RootCauseAnalysis] = None
    解决方案: Optional[Solution] = None
    预防知识: Optional[PreventionKnowledge] = None
    验证历史: List[ValidationRecord] = field(default_factory=list)
    关联错误: Optional[RelatedErrors] = None
    元数据: Optional[ErrorWisdomMetadata] = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        data = {
            "id": self.id,
            "timestamp": self.timestamp,
            "trace_id": self.trace_id,
            "version": self.version,
            "错误发现": asdict(self.错误发现) if self.错误发现 else {},
            "原因分析": asdict(self.原因分析) if self.原因分析 else {},
            "解决方案": asdict(self.解决方案) if self.解决方案 else {},
            "预防知识": self._prevention_to_dict(),
            "验证历史": [asdict(v) for v in self.验证历史],
            "关联错误": asdict(self.关联错误) if self.关联错误 else {},
            "元数据": asdict(self.元数据) if self.元数据 else {}
        }
        return data
    
    def _prevention_to_dict(self) -> dict:
        """预防知识转换为字典"""
        if not self.预防知识:
            return {}
        
        data = asdict(self.预防知识)
        if self.预防知识.前置检查规则:
            data["前置检查规则"] = asdict(self.预防知识.前置检查规则)
        return data


# ==================== 错误智慧库管理器 ====================

class ErrorWisdomManager:
    """
    错误智慧库管理器
    
    负责：
    - 错误记录与存储
    - 预防规则生成
    - 查询与统计
    - 时效性管理
    """
    
    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        self.wisdom_dir = os.path.join(memory_dir, "error_wisdom")
        os.makedirs(self.wisdom_dir, exist_ok=True)
        
        # 存储文件
        self.entries_file = os.path.join(self.wisdom_dir, "error_wisdom_entries.json")
        self.rules_file = os.path.join(self.wisdom_dir, "prevention_rules.json")
        self.patterns_file = os.path.join(self.wisdom_dir, "error_patterns.json")
        self.stats_file = os.path.join(self.wisdom_dir, "statistics.json")
        
        # 加载数据
        self.entries = self._load_json(self.entries_file, {"entries": {}, "metadata": {"total_count": 0}})
        self.rules = self._load_json(self.rules_file, {"rules": {}, "metadata": {"total_count": 0}})
        self.patterns = self._load_json(self.patterns_file, {"patterns": {}, "metadata": {"total_count": 0}})
        self.stats = self._load_json(self.stats_file, self._default_stats())
        
        # ===== Phase 3: 集成时效性管理器 =====
        try:
            from error_wisdom_timeliness import TimelinessManager
            self.timeliness_manager = TimelinessManager(memory_dir)
        except ImportError:
            self.timeliness_manager = None
        # ===== 时效性集成结束 =====
    
    def _load_json(self, filepath: str, default: dict) -> dict:
        """加载JSON文件"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load {filepath}: {e}")
                return default
        return default
    
    def _save_json(self, filepath: str, data: dict):
        """保存JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _default_stats(self) -> dict:
        """默认统计数据"""
        return {
            "总错误数": 0,
            "工具性错误数": 0,
            "认知性错误数": 0,
            "成功预防数": 0,
            "预防成功率": 0.0,
            "按错误类型统计": {},
            "按严重程度统计": {},
            "最近更新": ""
        }
    
    # ==================== 错误记录 ====================
    
    def record_error(
        self,
        error_type: str,
        error_subtype: str,
        error_code: str,
        error_description: str,
        root_cause: str,
        solution: str,
        prevention_strategy: str,
        trace_id: str,
        severity: str = "mild",
        trigger_scenario: str = "",
        metadata: dict = None
    ) -> str:
        """
        记录错误到智慧库
        
        Args:
            error_type: 错误类型（工具性错误/认知性错误）
            error_subtype: 错误子类型
            error_code: 错误码
            error_description: 错误描述
            root_cause: 根本原因
            solution: 解决方案
            prevention_strategy: 预防策略
            trace_id: 追踪ID
            severity: 严重程度
            trigger_scenario: 触发场景
            metadata: 额外元数据
        
        Returns:
            错误智慧条目ID
        """
        # 生成ID
        date_str = datetime.utcnow().strftime("%Y%m%d")
        entry_count = len(self.entries["entries"]) + 1
        entry_id = f"ew_{date_str}_{entry_count:03d}"
        
        # 创建条目
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        entry = ErrorWisdomEntry(
            id=entry_id,
            timestamp=now,
            trace_id=trace_id,
            version="1.0",
            错误发现=ErrorDiscovery(
                错误类型=error_type,
                子类型=error_subtype,
                错误码=error_code,
                错误描述=error_description,
                严重程度=severity,
                触发场景=trigger_scenario
            ),
            原因分析=RootCauseAnalysis(
                根本原因=root_cause
            ),
            解决方案=Solution(
                即时纠错=solution
            ),
            预防知识=PreventionKnowledge(
                预防策略=prevention_strategy
            ),
            元数据=ErrorWisdomMetadata(
                创建时间=now,
                最后更新=now,
                置信度=0.8
            )
        )
        
        # 存储条目
        self.entries["entries"][entry_id] = entry.to_dict()
        self.entries["metadata"]["total_count"] = len(self.entries["entries"])
        self._save_json(self.entries_file, self.entries)
        
        # 更新统计
        self._update_stats(entry)
        
        # ===== Phase 3: 同步时效性管理器 =====
        if self.timeliness_manager:
            self.timeliness_manager._initialize_entry(entry_id, base_confidence=0.85)
        # ===== 时效性同步结束 =====
        
        # 检查是否需要生成预防规则
        self._check_and_generate_rule(error_type, error_subtype)
        
        return entry_id
    
    def _update_stats(self, entry: ErrorWisdomEntry):
        """更新统计数据"""
        self.stats["总错误数"] += 1
        
        if entry.错误发现.错误类型 == "工具性错误":
            self.stats["工具性错误数"] += 1
        else:
            self.stats["认知性错误数"] += 1
        
        # 按错误类型统计
        subtype = entry.错误发现.子类型
        if subtype not in self.stats["按错误类型统计"]:
            self.stats["按错误类型统计"][subtype] = 0
        self.stats["按错误类型统计"][subtype] += 1
        
        # 按严重程度统计
        severity = entry.错误发现.严重程度
        if severity not in self.stats["按严重程度统计"]:
            self.stats["按严重程度统计"][severity] = 0
        self.stats["按严重程度统计"][severity] += 1
        
        self.stats["最近更新"] = entry.timestamp
        self._save_json(self.stats_file, self.stats)
    
    # ==================== 预防查询 ====================
    
    def query_prevention(
        self,
        context: dict,
        tool_name: str = None,
        params: dict = None
    ) -> List[dict]:
        """
        查询预防知识
        
        Args:
            context: 当前上下文
            tool_name: 工具名称（可选）
            params: 参数（可选）
        
        Returns:
            相关的预防规则列表
        """
        applicable_rules = []
        
        for rule_id, rule in self.rules.get("rules", {}).items():
            if self._rule_applicable(rule, context, tool_name, params):
                # 计算时效性调整后的置信度
                adjusted_confidence = self._calculate_adjusted_confidence(rule)
                rule["adjusted_confidence"] = adjusted_confidence
                
                if adjusted_confidence > 0.3:  # 只返回置信度足够高的规则
                    applicable_rules.append(rule)
        
        # 按优先级和置信度排序
        applicable_rules.sort(
            key=lambda r: (
                {"high": 3, "medium": 2, "low": 1}.get(r.get("预防优先级", "medium"), 2),
                r.get("adjusted_confidence", 0)
            ),
            reverse=True
        )
        
        return applicable_rules
    
    def _rule_applicable(self, rule: dict, context: dict, tool_name: str, params: dict) -> bool:
        """检查规则是否适用"""
        # 检查工具范围
        applicable_tools = rule.get("适用范围", {}).get("工具列表", ["*"])
        if "*" not in applicable_tools and tool_name and tool_name not in applicable_tools:
            return False
        
        # 检查排除场景
        excluded = rule.get("适用范围", {}).get("排除场景", [])
        current_scenario = context.get("scenario", "")
        if current_scenario in excluded:
            return False
        
        return True
    
    def _calculate_adjusted_confidence(self, rule: dict) -> float:
        """计算时效性调整后的置信度"""
        base_confidence = rule.get("时效性", {}).get("置信度", 0.8)
        
        # 时间衰减
        creation_time = rule.get("创建时间", "")
        if creation_time:
            try:
                created = datetime.fromisoformat(creation_time.replace("Z", "+00:00"))
                days_since = (datetime.now(created.tzinfo) - created).days
                time_decay = math.exp(-0.01 * days_since)  # 每天衰减1%
                base_confidence *= time_decay
            except:
                pass
        
        return base_confidence
    
    # ==================== 前置检查 ====================
    
    def pre_check(
        self,
        tool_name: str,
        params: dict,
        tool_schema: dict = None
    ) -> dict:
        """
        工具调用前的前置检查
        
        Args:
            tool_name: 工具名称
            params: 调用参数
            tool_schema: 工具schema（可选）
        
        Returns:
            检查结果
        """
        result = {
            "pass": True,
            "warnings": [],
            "auto_fixes": {},
            "suggestions": []
        }
        
        # 1. 查询预防规则
        applicable_rules = self.query_prevention(
            context={"tool_call": True},
            tool_name=tool_name,
            params=params
        )
        
        # 2. 执行规则检查
        for rule in applicable_rules:
            check_result = self._execute_rule_check(rule, params, tool_schema)
            
            if not check_result["pass"]:
                result["pass"] = False
                
                if check_result.get("auto_fix"):
                    result["auto_fixes"].update(check_result["auto_fix"])
                else:
                    result["warnings"].append({
                        "rule_id": rule.get("rule_id"),
                        "message": check_result.get("message", "检查未通过"),
                        "severity": rule.get("预防优先级", "medium")
                    })
            
            if check_result.get("suggestion"):
                result["suggestions"].append(check_result["suggestion"])
        
        # 3. 内置检查（基于schema）
        if tool_schema:
            schema_checks = self._schema_based_checks(params, tool_schema)
            result["warnings"].extend(schema_checks.get("warnings", []))
            result["suggestions"].extend(schema_checks.get("suggestions", []))
        
        return result
    
    def _execute_rule_check(self, rule: dict, params: dict, tool_schema: dict) -> dict:
        """执行规则检查"""
        prevention_rule = rule.get("前置检查规则", {})
        
        if not prevention_rule:
            return {"pass": True}
        
        # 简化的规则执行逻辑
        condition = prevention_rule.get("condition", "")
        check = prevention_rule.get("check", "")
        
        # 枚举验证示例
        if "enum" in condition.lower() or "enum" in check.lower():
            return self._check_enum_params(params, tool_schema, prevention_rule)
        
        # 必需参数检查
        if "required" in condition.lower() or "缺少" in check:
            return self._check_required_params(params, tool_schema)
        
        # 默认通过
        return {"pass": True}
    
    def _check_enum_params(self, params: dict, tool_schema: dict, rule: dict) -> dict:
        """检查枚举参数"""
        if not tool_schema:
            return {"pass": True}
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            enum_values = param_def.get("enum", [])
            
            if enum_values and param_value not in enum_values:
                auto_fixable = rule.get("auto_fixable", False)
                
                if auto_fixable:
                    # 尝试找到最接近的有效值
                    closest = self._find_closest_enum_value(param_value, enum_values)
                    if closest:
                        return {
                            "pass": False,
                            "auto_fix": {param_name: closest},
                            "message": f"参数 '{param_name}' 值 '{param_value}' 不在允许范围内，已自动修正为 '{closest}'"
                        }
                
                return {
                    "pass": False,
                    "message": f"参数 '{param_name}' 值 '{param_value}' 不在允许范围 {enum_values} 内",
                    "suggestion": f"请使用以下值之一: {enum_values}"
                }
        
        return {"pass": True}
    
    def _find_closest_enum_value(self, value: Any, enum_values: List[Any]) -> Optional[Any]:
        """找到最接近的枚举值"""
        # 简化实现：字符串匹配
        if isinstance(value, str):
            value_lower = value.lower()
            for enum_val in enum_values:
                if isinstance(enum_val, str) and enum_val.lower() == value_lower:
                    return enum_val
        return None
    
    def _check_required_params(self, params: dict, tool_schema: dict) -> dict:
        """检查必需参数"""
        if not tool_schema:
            return {"pass": True}
        
        required = tool_schema.get("parameters", {}).get("required", [])
        missing = [r for r in required if r not in params]
        
        if missing:
            return {
                "pass": False,
                "message": f"缺少必需参数: {missing}",
                "suggestion": f"请提供以下参数: {missing}"
            }
        
        return {"pass": True}
    
    def _schema_based_checks(self, params: dict, tool_schema: dict) -> dict:
        """基于schema的检查"""
        result = {"warnings": [], "suggestions": []}
        
        properties = tool_schema.get("parameters", {}).get("properties", {})
        
        for param_name, param_value in params.items():
            param_def = properties.get(param_name, {})
            
            # 类型检查
            expected_type = param_def.get("type")
            if expected_type and not self._check_type(param_value, expected_type):
                result["warnings"].append({
                    "param": param_name,
                    "message": f"参数类型不匹配，期望 {expected_type}"
                })
        
        return result
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """检查类型"""
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected = type_mapping.get(expected_type)
        if expected:
            return isinstance(value, expected)
        
        return True
    
    # ==================== 预防规则生成 ====================
    
    def _check_and_generate_rule(self, error_type: str, error_subtype: str):
        """检查并生成预防规则"""
        # 查找相似错误
        similar_errors = self._find_similar_errors(error_type, error_subtype)
        
        # 相似错误达到阈值时生成规则
        if len(similar_errors) >= 3:
            self._generate_prevention_rule(similar_errors)
    
    def _find_similar_errors(self, error_type: str, error_subtype: str) -> List[dict]:
        """查找相似错误"""
        similar = []
        
        for entry_id, entry in self.entries.get("entries", {}).items():
            discovery = entry.get("错误发现", {})
            if discovery.get("错误类型") == error_type and discovery.get("子类型") == error_subtype:
                similar.append(entry)
        
        return similar
    
    def _generate_prevention_rule(self, similar_errors: List[dict]):
        """从相似错误生成预防规则"""
        if not similar_errors:
            return
        
        # 提取共性
        first_error = similar_errors[0]
        error_subtype = first_error.get("错误发现", {}).get("子类型", "unknown")
        
        # 生成规则ID
        date_str = datetime.utcnow().strftime("%Y%m%d")
        rule_id = f"rule_{error_subtype}_{date_str}"
        
        # 创建规则（简化实现）
        rule = {
            "rule_id": rule_id,
            "rule_name": f"{error_subtype}预防规则",
            "创建时间": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "来源错误ID": [e.get("id") for e in similar_errors],
            "触发条件": {
                "错误类型": first_error.get("错误发现", {}).get("错误类型"),
                "子类型": error_subtype
            },
            "前置检查规则": self._extract_check_rule(similar_errors),
            "适用范围": {
                "工具列表": ["*"],
                "排除场景": []
            },
            "效果统计": {
                "应用次数": 0,
                "成功预防次数": 0,
                "失败次数": 0,
                "成功率": 0.0
            },
            "时效性": {
                "状态": "active",
                "置信度": 0.9,
                "最后验证": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "衰减系数": 1.0
            },
            "预防优先级": "high",
            "预防知识": first_error.get("预防知识", {})
        }
        
        # 存储规则
        self.rules["rules"][rule_id] = rule
        self.rules["metadata"]["total_count"] = len(self.rules["rules"])
        self._save_json(self.rules_file, self.rules)
        
        # 更新关联错误
        for error in similar_errors:
            entry_id = error.get("id")
            if entry_id in self.entries["entries"]:
                self.entries["entries"][entry_id]["关联错误"] = {
                    "相似错误ID": [e.get("id") for e in similar_errors if e.get("id") != entry_id],
                    "共性模式": error_subtype,
                    "抽象规则ID": rule_id
                }
        
        self._save_json(self.entries_file, self.entries)
    
    def _extract_check_rule(self, similar_errors: List[dict]) -> dict:
        """从相似错误提取检查规则"""
        # 简化实现：基于错误子类型生成规则
        error_subtype = similar_errors[0].get("错误发现", {}).get("子类型", "")
        
        if "参数" in error_subtype or "enum" in error_subtype.lower():
            return {
                "rule_id": f"check_{error_subtype}",
                "condition": "参数类型为enum",
                "check": "value in allowed_values",
                "action": "提示错误或自动修正",
                "auto_fixable": True
            }
        
        return {
            "rule_id": f"check_{error_subtype}",
            "condition": "通用检查",
            "check": "基于历史错误模式",
            "action": "警告提示"
        }
    
    # ==================== 验证记录 ====================
    
    def record_validation(
        self,
        entry_id: str,
        trace_id: str,
        scenario: str,
        effect: str,
        prevention_triggered: str = "",
        user_feedback: str = ""
    ):
        """
        记录验证结果
        
        Args:
            entry_id: 错误智慧条目ID
            trace_id: 追踪ID
            scenario: 场景
            effect: 效果（成功预防/预防失败/未触发）
            prevention_triggered: 预防触发描述
            user_feedback: 用户反馈
        """
        if entry_id not in self.entries["entries"]:
            return
        
        entry = self.entries["entries"][entry_id]
        
        # 添加验证记录
        validation = ValidationRecord(
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            trace_id=trace_id,
            场景=scenario,
            效果=effect,
            预防触发=prevention_triggered,
            用户反馈=user_feedback
        )
        
        entry["验证历史"].append(asdict(validation))
        
        # 更新元数据
        entry["元数据"]["验证次数"] = len(entry["验证历史"])
        entry["元数据"]["最后更新"] = validation.timestamp
        
        if effect == "成功预防":
            entry["元数据"]["成功预防次数"] = entry["元数据"].get("成功预防次数", 0) + 1
            self.stats["成功预防数"] = self.stats.get("成功预防数", 0) + 1
        
        # 重新计算置信度
        entry["元数据"]["置信度"] = self._calculate_confidence(entry)
        
        # 更新时效性标记
        entry["元数据"]["时效性标记"] = self._determine_timeliness_status(entry["元数据"]["置信度"])
        
        self._save_json(self.entries_file, self.entries)
        self._save_json(self.stats_file, self.stats)
    
    def _calculate_confidence(self, entry: dict) -> float:
        """计算置信度"""
        base = 0.8
        validations = entry.get("元数据", {}).get("验证次数", 0)
        successes = entry.get("元数据", {}).get("成功预防次数", 0)
        
        if validations > 0:
            success_rate = successes / validations
            # 基础置信度 + 验证加成
            confidence = base + (success_rate - 0.5) * 0.4
            return max(0.1, min(1.0, confidence))
        
        return base
    
    def _determine_timeliness_status(self, confidence: float) -> str:
        """确定时效性状态"""
        if confidence > 0.7:
            return "active"
        elif confidence > 0.3:
            return "deprecated"
        else:
            return "archived"
    
    # ==================== 时效性管理 ====================
    
    def decay_all_confidence(self):
        """对所有条目应用时间衰减"""
        now = datetime.utcnow()
        
        for entry_id, entry in self.entries.get("entries", {}).items():
            creation_time = entry.get("元数据", {}).get("创建时间", "")
            
            if creation_time:
                try:
                    created = datetime.fromisoformat(creation_time.replace("Z", "+00:00"))
                    days_since = (now - created.replace(tzinfo=None)).days
                    
                    # 时间衰减
                    current_confidence = entry["元数据"].get("置信度", 0.8)
                    decayed_confidence = current_confidence * math.exp(-0.01 * days_since)
                    
                    entry["元数据"]["置信度"] = decayed_confidence
                    entry["元数据"]["时效性标记"] = self._determine_timeliness_status(decayed_confidence)
                except:
                    pass
        
        self._save_json(self.entries_file, self.entries)
    
    # ==================== 统计与报告 ====================
    
    def get_statistics(self) -> dict:
        """获取统计数据"""
        return self.stats.copy()
    
    def get_recent_errors(self, limit: int = 10) -> List[dict]:
        """获取最近的错误"""
        entries = list(self.entries.get("entries", {}).values())
        entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        return entries[:limit]
    
    def get_top_prevention_rules(self, limit: int = 10) -> List[dict]:
        """获取最有效的预防规则"""
        rules = list(self.rules.get("rules", {}).values())
        rules.sort(
            key=lambda r: r.get("效果统计", {}).get("成功率", 0),
            reverse=True
        )
        return rules[:limit]


# ==================== CLI 接口 ====================

def main():
    parser = argparse.ArgumentParser(description="错误智慧库管理器")
    parser.add_argument("--memory-dir", default="./agi_memory", help="记忆存储目录")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # record 命令
    record_parser = subparsers.add_parser("record", help="记录错误")
    record_parser.add_argument("--error-type", required=True, help="错误类型")
    record_parser.add_argument("--error-subtype", required=True, help="错误子类型")
    record_parser.add_argument("--error-code", default="", help="错误码")
    record_parser.add_argument("--description", required=True, help="错误描述")
    record_parser.add_argument("--root-cause", required=True, help="根本原因")
    record_parser.add_argument("--solution", required=True, help="解决方案")
    record_parser.add_argument("--prevention", required=True, help="预防策略")
    record_parser.add_argument("--trace-id", required=True, help="追踪ID")
    record_parser.add_argument("--severity", default="mild", help="严重程度")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="查询预防知识")
    query_parser.add_argument("--tool-name", help="工具名称")
    query_parser.add_argument("--params", help="参数（JSON格式）")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="前置检查")
    check_parser.add_argument("--tool-name", required=True, help="工具名称")
    check_parser.add_argument("--params", required=True, help="参数（JSON格式）")
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计")
    
    # recent 命令
    recent_parser = subparsers.add_parser("recent", help="查看最近错误")
    recent_parser.add_argument("--limit", type=int, default=10, help="数量限制")
    
    args = parser.parse_args()
    
    manager = ErrorWisdomManager(args.memory_dir)
    
    if args.command == "record":
        entry_id = manager.record_error(
            error_type=args.error_type,
            error_subtype=args.error_subtype,
            error_code=args.error_code,
            error_description=args.description,
            root_cause=args.root_cause,
            solution=args.solution,
            prevention_strategy=args.prevention,
            trace_id=args.trace_id,
            severity=args.severity
        )
        print(f"记录成功，ID: {entry_id}")
    
    elif args.command == "query":
        params = json.loads(args.params) if args.params else None
        rules = manager.query_prevention(
            context={},
            tool_name=args.tool_name,
            params=params
        )
        print(json.dumps(rules, ensure_ascii=False, indent=2))
    
    elif args.command == "check":
        params = json.loads(args.params)
        result = manager.pre_check(args.tool_name, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = manager.get_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "recent":
        errors = manager.get_recent_errors(args.limit)
        print(json.dumps(errors, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
