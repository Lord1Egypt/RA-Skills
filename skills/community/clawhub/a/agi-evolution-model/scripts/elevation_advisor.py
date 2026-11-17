#!/usr/bin/env python3

# 日志记录
__version__ = "1.0.0"

import logging
logger = logging.getLogger(__name__)
"""
五维升维建议器 (Elevation Advisor)

功能：
- 提供升维建议的接口框架
- 接收模型的升维建议
- 记录升维历史
- 提供升维建议查询接口

基于：
- references/dimension_definitions.md
- references/dimension_data_structure.md
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from interfaces import TraceContext, create_trace_context


# ==================== 数据类定义 ====================

@dataclass
class ElevationSuggestion:
    """升维建议"""
    should_elevate: bool
    reason: str
    suggested_action: str
    suggested_dimensions: List[str]
    expected_effect: str
    confidence: float
    alternatives: Optional[List[Dict[str, Any]]] = None


@dataclass
class ElevationEvent:
    """升维事件"""
    timestamp: str
    action: str
    dimension: str
    before: List[str]
    after: List[str]
    trigger: str
    effect: str
    effect_details: Optional[Dict[str, Any]] = None
    confidence: float = 0.0


# ==================== 验证函数 ====================

def validate_action_type(action_type: str) -> bool:
    """
    验证动作类型是否有效
    
    Args:
        action_type: 动作类型
    
    Returns:
        bool: 是否有效
    """
    valid_actions = {"add_dimensions", "remove_dimensions", "replace_dimensions"}
    return action_type in valid_actions


def validate_effect_type(effect_type: str) -> bool:
    """
    验证效果类型是否有效
    
    Args:
        effect_type: 效果类型
    
    Returns:
        bool: 是否有效
    """
    valid_effects = {"positive", "negative", "neutral", "unknown"}
    return effect_type in valid_effects


def validate_elevation_suggestion(suggestion: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证升维建议数据结构
    
    Args:
        suggestion: 升维建议字典
    
    Returns:
        Dict[str, Any]: 验证结果 {"valid": bool, "errors": List[str]}
    """
    errors = []
    
    # 验证必需字段
    required_fields = [
        "should_elevate",
        "reason",
        "suggested_action",
        "suggested_dimensions",
        "expected_effect",
        "confidence"
    ]
    
    for field in required_fields:
        if field not in suggestion:
            errors.append(f"缺少字段: {field}")
    
    # 验证should_elevate
    if "should_elevate" in suggestion and not isinstance(suggestion["should_elevate"], bool):
        errors.append("should_elevate应该是布尔值")
    
    # 验证suggested_action
    if "suggested_action" in suggestion:
        if not validate_action_type(suggestion["suggested_action"]):
            errors.append(f"suggested_action的值无效: {suggestion['suggested_action']}")
    
    # 验证suggested_dimensions
    if "suggested_dimensions" in suggestion:
        if not isinstance(suggestion["suggested_dimensions"], list):
            errors.append("suggested_dimensions应该是列表")
        elif not suggestion["suggested_dimensions"]:
            errors.append("suggested_dimensions不能为空")
    
    # 验证confidence
    if "confidence" in suggestion:
        if not isinstance(suggestion["confidence"], (int, float)):
            errors.append("confidence应该是数字")
        elif not (0.0 <= suggestion["confidence"] <= 1.0):
            errors.append(f"confidence的值无效: {suggestion['confidence']}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_elevation_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证升维事件数据结构
    
    Args:
        event: 升维事件字典
    
    Returns:
        Dict[str, Any]: 验证结果 {"valid": bool, "errors": List[str]}
    """
    errors = []
    
    # 验证必需字段
    required_fields = [
        "timestamp",
        "action",
        "dimension",
        "before",
        "after",
        "trigger",
        "effect"
    ]
    
    for field in required_fields:
        if field not in event:
            errors.append(f"缺少字段: {field}")
    
    # 验证action
    if "action" in event:
        valid_actions = {"add_dimension", "remove_dimension", "replace_dimension"}
        if event["action"] not in valid_actions:
            errors.append(f"action的值无效: {event['action']}")
    
    # 验证before和after
    if "before" in event and "after" in event:
        if not isinstance(event["before"], list):
            errors.append("before应该是列表")
        if not isinstance(event["after"], list):
            errors.append("after应该是列表")
    
    # 验证effect
    if "effect" in event:
        if not validate_effect_type(event["effect"]):
            errors.append(f"effect的值无效: {event['effect']}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ==================== 存储函数 ====================

def get_elevation_history_storage_path(memory_dir: Optional[str] = None):
    """
    获取升维历史存储路径

    Args:
        memory_dir: 记忆存储目录（传入时优先使用，避免依赖当前工作目录导致写错位置）

    Returns:
        str: 存储路径
    """
    if memory_dir:
        base = os.path.join(memory_dir, "elevation_history")
    else:
        # 默认存储于技能目录的 agi_memory/elevation_history 下，避免硬编码容器路径导致数据丢失
        base = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "agi_memory", "elevation_history"
        )
    return os.path.abspath(base)


def ensure_storage_directory(memory_dir: Optional[str] = None):
    """
    确保存储目录存在
    """
    storage_path = get_elevation_history_storage_path(memory_dir)
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)


def record_elevation_event(record_id: str, event: Dict[str, Any], memory_dir: Optional[str] = None) -> bool:
    """
    记录升维事件

    Args:
        record_id: 记录ID
        event: 升维事件字典
        memory_dir: 记忆存储目录（可选，默认写入技能 agi_memory）

    Returns:
        bool: 是否记录成功
    """
    try:
        # 验证数据结构
        validation = validate_elevation_event(event)
        if not validation["valid"]:
            print(f"数据验证失败: {validation['errors']}")
            return False

        ensure_storage_directory(memory_dir)

        storage_path = get_elevation_history_storage_path(memory_dir)
        file_path = os.path.join(storage_path, f"{record_id}_history.json")
        
        # 加载现有历史
        history = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # 添加新事件
        history.append(event)
        
        # 保存历史
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"记录升维事件失败: {str(e)}")
        return False


def load_elevation_history(record_id: str, memory_dir: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    加载升维历史

    Args:
        record_id: 记录ID
        memory_dir: 记忆存储目录（可选）

    Returns:
        Optional[List[Dict[str, Any]]]: 升维历史列表，如果不存在返回None
    """
    try:
        storage_path = get_elevation_history_storage_path(memory_dir)
        file_path = os.path.join(storage_path, f"{record_id}_history.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        return history
    
    except Exception as e:
        print(f"加载升维历史失败: {str(e)}")
        return None


def save_elevation_suggestion(record_id: str, suggestion: Dict[str, Any], memory_dir: Optional[str] = None) -> bool:
    """
    保存升维建议

    Args:
        record_id: 记录ID
        suggestion: 升维建议字典
        memory_dir: 记忆存储目录（可选，默认写入技能 agi_memory）

    Returns:
        bool: 是否保存成功
    """
    try:
        # 验证数据结构
        validation = validate_elevation_suggestion(suggestion)
        if not validation["valid"]:
            print(f"数据验证失败: {validation['errors']}")
            return False

        ensure_storage_directory(memory_dir)

        storage_path = get_elevation_history_storage_path(memory_dir)
        file_path = os.path.join(storage_path, f"{record_id}_suggestion.json")
        
        # 添加元数据
        suggestion["metadata"] = {
            "record_id": record_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0"
        }
        
        # 保存建议
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(suggestion, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"保存升维建议失败: {str(e)}")
        return False


def load_elevation_suggestion(record_id: str, memory_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    加载升维建议

    Args:
        record_id: 记录ID
        memory_dir: 记忆存储目录（可选）

    Returns:
        Optional[Dict[str, Any]]: 升维建议字典，如果不存在返回None
    """
    try:
        storage_path = get_elevation_history_storage_path(memory_dir)
        file_path = os.path.join(storage_path, f"{record_id}_suggestion.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            suggestion = json.load(f)
        
        return suggestion
    
    except Exception as e:
        print(f"加载升维建议失败: {str(e)}")
        return None


# ==================== 接口函数 ====================

def suggest_dimension_elevation(current_record: Dict[str, Any], model) -> Dict[str, Any]:
    """
    获取升维建议（接口函数）
    
    Args:
        current_record: 当前记录（包含维度状态、升维历史等）
        model: 模型实例
    
    Returns:
        Dict[str, Any]: 升维建议字典
    
    Raises:
        ValueError: 当输入数据格式错误时
        Exception: 当模型分析失败时
    """
    # 1. 验证输入数据
    if not isinstance(current_record, dict):
        raise ValueError("current_record应该是字典")
    
    # 2. 调用模型提供升维建议
    # 注意：这里是接口框架，实际的升维建议由模型自主完成
    # 模型应该按照dimension_data_structure.md中定义的格式返回结果
    
    try:
        # 模型提供升维建议（这里需要模型实现）
        suggestion = model.suggest_elevation(current_record)
        
        # 3. 验证模型返回的数据结构
        validation = validate_elevation_suggestion(suggestion)
        if not validation["valid"]:
            raise ValueError(f"模型返回的数据结构无效: {validation['errors']}")
        
        # 4. 获取记录ID
        record_id = current_record.get("record_id", "")
        if not record_id:
            raise ValueError("current_record缺少record_id")
        
        # 5. 保存升维建议
        save_elevation_suggestion(record_id, suggestion)
        
        # 6. 返回升维建议
        suggestion["record_id"] = record_id
        return suggestion
    
    except Exception as e:
        print(f"获取升维建议失败: {str(e)}")
        raise


def record_elevation_decision(
    record_id: str,
    action: str,
    dimension: str,
    before: List[str],
    after: List[str],
    trigger: str,
    effect: str = "unknown",
    effect_details: Optional[Dict[str, Any]] = None,
    confidence: float = 0.0
) -> bool:
    """
    记录升维决策
    
    Args:
        record_id: 记录ID
        action: 动作类型（add_dimension、remove_dimension、replace_dimension）
        dimension: 涉及的维度
        before: 升维前的维度列表
        after: 升维后的维度列表
        trigger: 升维触发原因
        effect: 升维效果（positive、negative、neutral、unknown）
        effect_details: 效果详情
        confidence: 置信度
    
    Returns:
        bool: 是否记录成功
    """
    # 创建升维事件
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "dimension": dimension,
        "before": before,
        "after": after,
        "trigger": trigger,
        "effect": effect,
        "effect_details": effect_details,
        "confidence": confidence
    }
    
    # 记录升维事件
    return record_elevation_event(record_id, event)


def get_elevation_history(record_id: str, memory_dir: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    获取升维历史

    Args:
        record_id: 记录ID
        memory_dir: 记忆存储目录（可选）

    Returns:
        Optional[List[Dict[str, Any]]]: 升维历史列表，如果不存在返回None
    """
    return load_elevation_history(record_id, memory_dir)


def analyze_elevation_effectiveness(record_id: str, memory_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    分析升维效果

    Args:
        record_id: 记录ID
        memory_dir: 记忆存储目录（可选）

    Returns:
        Optional[Dict[str, Any]]: 升维效果分析，如果不存在返回None
    """
    history = load_elevation_history(record_id, memory_dir)
    
    if history is None:
        return None
    
    # 统计各类效果的数量
    effect_counts = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "unknown": 0
    }
    
    for event in history:
        effect = event.get("effect", "unknown")
        if effect in effect_counts:
            effect_counts[effect] += 1
    
    # 计算成功率
    total_events = len(history)
    if total_events > 0:
        success_rate = effect_counts["positive"] / total_events
    else:
        success_rate = 0.0
    
    return {
        "record_id": record_id,
        "total_elevations": total_events,
        "effect_counts": effect_counts,
        "success_rate": success_rate
    }


# ==================== 主函数（示例） ====================

if __name__ == "__main__":
    print("五维升维建议器")
    print("=" * 50)
    
    # 示例1：验证动作类型
    print("\n示例1：验证动作类型")
    valid = validate_action_type("add_dimensions")
    print(f"'add_dimensions' 是否有效: {valid}")
    
    invalid = validate_action_type("invalid_action")
    print(f"'invalid_action' 是否有效: {invalid}")
    
    # 示例2：验证效果类型
    print("\n示例2：验证效果类型")
    valid = validate_effect_type("positive")
    print(f"'positive' 是否有效: {valid}")
    
    invalid = validate_effect_type("invalid")
    print(f"'invalid' 是否有效: {invalid}")
    
    # 示例3：验证升维建议数据结构
    print("\n示例3：验证升维建议数据结构")
    test_suggestion = {
        "should_elevate": True,
        "reason": "当前问题涉及连锁反应，算法智力无法处理系统复杂性",
        "suggested_action": "add_dimensions",
        "suggested_dimensions": ["systemic"],
        "expected_effect": "引入系统智力后，可以评估连锁反应",
        "confidence": 0.9
    }
    
    validation = validate_elevation_suggestion(test_suggestion)
    print(f"验证结果: {validation}")
    
    # 示例4：验证升维事件数据结构
    print("\n示例4：验证升维事件数据结构")
    test_event = {
        "timestamp": "2024-01-01T10:00:00Z",
        "action": "add_dimension",
        "dimension": "systemic",
        "before": ["algorithmic"],
        "after": ["algorithmic", "systemic"],
        "trigger": "detected system complexity",
        "effect": "positive",
        "confidence": 0.9
    }
    
    validation = validate_elevation_event(test_event)
    print(f"验证结果: {validation}")
    
    # 示例5：记录升维决策
    print("\n示例5：记录升维决策")
    success = record_elevation_decision(
        record_id="test-record-001",
        action="add_dimension",
        dimension="systemic",
        before=["algorithmic"],
        after=["algorithmic", "systemic"],
        trigger="detected system complexity",
        effect="positive",
        confidence=0.9
    )
    print(f"记录升维决策: {'成功' if success else '失败'}")
    
    # 示例6：获取升维历史
    print("\n示例6：获取升维历史")
    history = get_elevation_history("test-record-001")
    print(f"升维历史: {history}")
    
    # 示例7：分析升维效果
    print("\n示例7：分析升维效果")
    effectiveness = analyze_elevation_effectiveness("test-record-001")
    print(f"升维效果分析: {effectiveness}")
    
    print("\n五维升维建议器 - 测试完成")
