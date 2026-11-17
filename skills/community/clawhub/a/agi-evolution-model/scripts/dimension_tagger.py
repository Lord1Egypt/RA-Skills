#!/usr/bin/env python3

# 日志记录
__version__ = "1.0.0"

import logging
logger = logging.getLogger(__name__)
"""
五维智力标签生成器 (Dimension Tagger)

功能：
- 提供维度标签生成的接口框架
- 接收模型的识别结果
- 存储维度标签到记录层
- 提供维度标签查询接口

基于：
- references/dimension_definitions.md
- references/dimension_data_structure.md
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from interfaces import TraceContext, create_trace_context


# ==================== 数据类定义 ====================

@dataclass
class DimensionState:
    """当前维度状态"""
    active: List[str]
    primary: str
    secondary: List[str]
    intensity: Dict[str, str]


@dataclass
class DimensionRelationship:
    """维度关系"""
    type: str
    source: str
    target: str
    description: str


@dataclass
class DimensionConfidence:
    """维度置信度"""
    overall: float
    # 各维度的置信度
    algorithmic: Optional[float] = None
    narrative: Optional[float] = None
    systemic: Optional[float] = None
    execution: Optional[float] = None
    meta: Optional[float] = None


@dataclass
class DimensionTags:
    """维度标签"""
    current_dimensions: DimensionState
    relationships: List[DimensionRelationship]
    confidence: DimensionConfidence


# ==================== 验证函数 ====================

def validate_dimension_names(dimension_names: List[str]) -> bool:
    """
    验证维度名称是否有效
    
    Args:
        dimension_names: 维度名称列表
    
    Returns:
        bool: 是否有效
    """
    valid_dimensions = {
        "algorithmic",
        "narrative",
        "systemic",
        "execution",
        "meta"
    }
    
    return all(dim in valid_dimensions for dim in dimension_names)


def validate_intensity_value(intensity: str) -> bool:
    """
    验证强度值是否有效
    
    Args:
        intensity: 强度值
    
    Returns:
        bool: 是否有效
    """
    valid_intensities = {"high", "medium", "low", "none"}
    return intensity in valid_intensities


def validate_relationship_type(relationship_type: str) -> bool:
    """
    验证关系类型是否有效
    
    Args:
        relationship_type: 关系类型
    
    Returns:
        bool: 是否有效
    """
    valid_types = {"enhance", "support", "collaborate", "complement"}
    return relationship_type in valid_types


def validate_confidence_value(confidence: float) -> bool:
    """
    验证置信度是否有效
    
    Args:
        confidence: 置信度
    
    Returns:
        bool: 是否有效
    """
    return 0.0 <= confidence <= 1.0


def validate_dimension_tags(tags: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证维度标签数据结构
    
    Args:
        tags: 维度标签字典
    
    Returns:
        Dict[str, Any]: 验证结果 {"valid": bool, "errors": List[str]}
    """
    errors = []
    
    # 验证current_dimensions
    if "current_dimensions" not in tags:
        errors.append("缺少字段: current_dimensions")
    else:
        current_dims = tags["current_dimensions"]
        
        # 验证active
        if "active" not in current_dims:
            errors.append("缺少字段: current_dimensions.active")
        elif not isinstance(current_dims["active"], list):
            errors.append("current_dimensions.active应该是列表")
        elif not validate_dimension_names(current_dims["active"]):
            errors.append(f"current_dimensions.active包含无效的维度名称: {current_dims['active']}")
        
        # 验证intensity
        if "intensity" in current_dims:
            intensity = current_dims["intensity"]
            if not isinstance(intensity, dict):
                errors.append("current_dimensions.intensity应该是字典")
            else:
                for dim, value in intensity.items():
                    if not validate_intensity_value(value):
                        errors.append(f"current_dimensions.intensity.{dim}的值无效: {value}")
    
    # 验证relationships
    if "relationships" in tags:
        if not isinstance(tags["relationships"], list):
            errors.append("relationships应该是列表")
        else:
            for i, rel in enumerate(tags["relationships"]):
                if not isinstance(rel, dict):
                    errors.append(f"relationships[{i}]应该是字典")
                elif "type" not in rel:
                    errors.append(f"relationships[{i}]缺少字段: type")
                elif not validate_relationship_type(rel["type"]):
                    errors.append(f"relationships[{i}].type的值无效: {rel['type']}")
    
    # 验证confidence
    if "confidence" in tags:
        conf = tags["confidence"]
        if not isinstance(conf, dict):
            errors.append("confidence应该是字典")
        elif "overall" not in conf:
            errors.append("confidence缺少字段: overall")
        elif not validate_confidence_value(conf["overall"]):
            errors.append(f"confidence.overall的值无效: {conf['overall']}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ==================== 存储函数 ====================

def get_dimension_tags_storage_path():
    """
    获取维度标签存储路径
    
    Returns:
        str: 存储路径
    """
    # 存储于技能目录的 agi_memory/dimension_tags 下，避免硬编码容器路径导致数据落到错误位置
    base = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "agi_memory", "dimension_tags"
    )
    return os.path.abspath(base)


def ensure_storage_directory():
    """
    确保存储目录存在
    """
    storage_path = get_dimension_tags_storage_path()
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)


def generate_record_id(task_description: str, timestamp: str) -> str:
    """
    生成记录ID
    
    Args:
        task_description: 任务描述
        timestamp: 时间戳
    
    Returns:
        str: 记录ID
    """
    # 使用任务描述和时间戳生成唯一ID
    content = f"{task_description}_{timestamp}"
    hash_obj = hashlib.md5(content.encode())
    return f"record-{hash_obj.hexdigest()}"


def save_dimension_tags(record_id: str, dimension_tags: Dict[str, Any]) -> bool:
    """
    保存维度标签
    
    Args:
        record_id: 记录ID
        dimension_tags: 维度标签字典
    
    Returns:
        bool: 是否保存成功
    """
    try:
        ensure_storage_directory()
        
        storage_path = get_dimension_tags_storage_path()
        file_path = os.path.join(storage_path, f"{record_id}.json")
        
        # 验证数据结构
        validation = validate_dimension_tags(dimension_tags)
        if not validation["valid"]:
            print(f"数据验证失败: {validation['errors']}")
            return False
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dimension_tags, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"保存维度标签失败: {str(e)}")
        return False


def load_dimension_tags(record_id: str) -> Optional[Dict[str, Any]]:
    """
    加载维度标签
    
    Args:
        record_id: 记录ID
    
    Returns:
        Optional[Dict[str, Any]]: 维度标签字典，如果不存在返回None
    """
    try:
        storage_path = get_dimension_tags_storage_path()
        file_path = os.path.join(storage_path, f"{record_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            dimension_tags = json.load(f)
        
        return dimension_tags
    
    except Exception as e:
        print(f"加载维度标签失败: {str(e)}")
        return None


# ==================== 接口函数 ====================

def generate_dimension_tags(raw_data: Dict[str, Any], model) -> Dict[str, Any]:
    """
    生成维度标签（接口函数）
    
    Args:
        raw_data: 原始数据（三顶点运行数据）
        model: 模型实例
    
    Returns:
        Dict[str, Any]: 维度标签字典
    
    Raises:
        ValueError: 当输入数据格式错误时
        Exception: 当模型识别失败时
    """
    # 1. 验证输入数据
    if not isinstance(raw_data, dict):
        raise ValueError("raw_data应该是字典")
    
    # 2. 调用模型识别维度
    # 注意：这里是接口框架，实际的模型识别由模型自主完成
    # 模型应该按照dimension_data_structure.md中定义的格式返回结果
    
    try:
        # 模型识别维度（这里需要模型实现）
        dimension_tags = model.identify_dimensions(raw_data)
        
        # 3. 验证模型返回的数据结构
        validation = validate_dimension_tags(dimension_tags)
        if not validation["valid"]:
            raise ValueError(f"模型返回的数据结构无效: {validation['errors']}")
        
        # 4. 生成记录ID
        timestamp = datetime.utcnow().isoformat() + "Z"
        task_description = raw_data.get("task_description", "")
        record_id = generate_record_id(task_description, timestamp)
        
        # 5. 添加元数据
        dimension_tags["metadata"] = {
            "record_id": record_id,
            "timestamp": timestamp,
            "version": "1.0",
            "created_at": timestamp,
            "created_by": "model"
        }
        
        # 6. 保存维度标签
        save_dimension_tags(record_id, dimension_tags)
        
        # 7. 返回维度标签
        dimension_tags["record_id"] = record_id
        return dimension_tags
    
    except Exception as e:
        print(f"生成维度标签失败: {str(e)}")
        raise


def get_dimension_tags(record_id: str) -> Optional[Dict[str, Any]]:
    """
    获取维度标签
    
    Args:
        record_id: 记录ID
    
    Returns:
        Optional[Dict[str, Any]]: 维度标签字典，如果不存在返回None
    """
    return load_dimension_tags(record_id)


def get_current_dimensions(record_id: str) -> Optional[Dict[str, Any]]:
    """
    获取当前维度状态
    
    Args:
        record_id: 记录ID
    
    Returns:
        Optional[Dict[str, Any]]: 当前维度状态，如果不存在返回None
    """
    dimension_tags = load_dimension_tags(record_id)
    
    if dimension_tags is None:
        return None
    
    return dimension_tags.get("current_dimensions", None)


def search_by_dimension(dimension: str, intensity: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    按维度搜索记录
    
    Args:
        dimension: 维度名称
        intensity: 强度过滤（可选）
    
    Returns:
        List[Dict[str, Any]]: 匹配的记录列表
    """
    storage_path = get_dimension_tags_storage_path()
    
    if not os.path.exists(storage_path):
        return []
    
    matching_records = []
    
    for filename in os.listdir(storage_path):
        if filename.endswith('.json'):
            try:
                file_path = os.path.join(storage_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    dimension_tags = json.load(f)
                
                current_dims = dimension_tags.get("current_dimensions", {})
                active_dims = current_dims.get("active", [])
                intensity_dict = current_dims.get("intensity", {})
                
                # 检查维度是否激活
                if dimension in active_dims:
                    # 检查强度（如果指定）
                    if intensity is None or intensity_dict.get(dimension) == intensity:
                        matching_records.append(dimension_tags)
            
            except Exception as e:
                print(f"读取文件 {filename} 失败: {str(e)}")
                continue
    
    return matching_records


# ==================== 主函数（示例） ====================

if __name__ == "__main__":
    print("五维智力标签生成器")
    print("=" * 50)
    
    # 示例1：验证维度名称
    print("\n示例1：验证维度名称")
    valid = validate_dimension_names(["algorithmic", "systemic", "meta"])
    print(f"['algorithmic', 'systemic', 'meta'] 是否有效: {valid}")
    
    invalid = validate_dimension_names(["algorithmic", "invalid_dimension"])
    print(f"['algorithmic', 'invalid_dimension'] 是否有效: {invalid}")
    
    # 示例2：验证强度值
    print("\n示例2：验证强度值")
    valid = validate_intensity_value("high")
    print(f"'high' 是否有效: {valid}")
    
    invalid = validate_intensity_value("invalid")
    print(f"'invalid' 是否有效: {invalid}")
    
    # 示例3：验证维度标签数据结构
    print("\n示例3：验证维度标签数据结构")
    test_tags = {
        "current_dimensions": {
            "active": ["algorithmic", "systemic", "meta"],
            "primary": "algorithmic",
            "secondary": ["systemic"],
            "intensity": {
                "algorithmic": "high",
                "systemic": "medium"
            }
        },
        "relationships": [
            {
                "type": "enhance",
                "source": "systemic",
                "target": "algorithmic",
                "description": "系统智力增强算法智力的全局视角"
            }
        ],
        "confidence": {
            "overall": 0.85,
            "algorithmic": 0.9,
            "systemic": 0.8
        }
    }
    
    validation = validate_dimension_tags(test_tags)
    print(f"验证结果: {validation}")
    
    print("\n五维智力标签生成器 - 测试完成")
