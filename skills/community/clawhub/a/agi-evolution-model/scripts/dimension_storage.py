#!/usr/bin/env python3

# 日志记录
__version__ = "1.0.0"

import logging
logger = logging.getLogger(__name__)
"""
五维智力存储管理器 (Dimension Storage Manager)

功能：
- 管理维度标签的存储和查询
- 管理升维历史的存储和查询
- 提供数据一致性保证
- 提供数据查询接口

基于：
- references/dimension_definitions.md
- references/dimension_data_structure.md
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import shutil
from interfaces import TraceContext, create_trace_context


# ==================== 存储路径管理 ====================

class StoragePaths:
    """存储路径管理"""
    
    _SKILL_MEMORY = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agi_memory")
    )
    DIMENSION_TAGS_DIR = os.path.join(_SKILL_MEMORY, "dimension_tags")
    ELEVATION_HISTORY_DIR = os.path.join(_SKILL_MEMORY, "elevation_history")
    
    @classmethod
    def ensure_directories(cls):
        """确保所有存储目录存在"""
        for dir_path in [cls.DIMENSION_TAGS_DIR, cls.ELEVATION_HISTORY_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)


# ==================== 数据一致性管理 ====================

class DataConsistency:
    """数据一致性管理"""
    
    @staticmethod
    def validate_record_consistency(record_id: str) -> Dict[str, Any]:
        """
        验证记录的数据一致性
        
        Args:
            record_id: 记录ID
        
        Returns:
            Dict[str, Any]: 一致性检查结果 {"consistent": bool, "errors": List[str]}
        """
        errors = []
        
        # 检查维度标签是否存在
        dimension_tags_path = os.path.join(
            StoragePaths.DIMENSION_TAGS_DIR,
            f"{record_id}.json"
        )
        
        if not os.path.exists(dimension_tags_path):
            errors.append(f"维度标签不存在: {record_id}")
        
        # 检查升维建议是否存在（可选）
        elevation_suggestion_path = os.path.join(
            StoragePaths.ELEVATION_HISTORY_DIR,
            f"{record_id}_suggestion.json"
        )
        
        if os.path.exists(elevation_suggestion_path):
            try:
                with open(elevation_suggestion_path, 'r', encoding='utf-8') as f:
                    suggestion = json.load(f)
                
                # 检查建议的维度是否在维度标签中
                if "suggested_dimensions" in suggestion:
                    suggested_dims = suggestion["suggested_dimensions"]
                    
                    with open(dimension_tags_path, 'r', encoding='utf-8') as f:
                        tags = json.load(f)
                    
                    active_dims = tags.get("current_dimensions", {}).get("active", [])
                    
                    for dim in suggested_dims:
                        if dim not in active_dims:
                            errors.append(f"建议的维度 {dim} 不在当前激活维度中")
            
            except Exception as e:
                errors.append(f"验证升维建议时出错: {str(e)}")
        
        return {
            "consistent": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def repair_record(record_id: str) -> Dict[str, Any]:
        """
        尝试修复记录
        
        Args:
            record_id: 记录ID
        
        Returns:
            Dict[str, Any]: 修复结果 {"success": bool, "actions": List[str]}
        """
        actions = []
        
        # 检查维度标签是否存在
        dimension_tags_path = os.path.join(
            StoragePaths.DIMENSION_TAGS_DIR,
            f"{record_id}.json"
        )
        
        if not os.path.exists(dimension_tags_path):
            actions.append("创建空的维度标签")
            # 创建空的维度标签
            empty_tags = {
                "current_dimensions": {
                    "active": [],
                    "primary": "",
                    "secondary": [],
                    "intensity": {}
                },
                "relationships": [],
                "confidence": {
                    "overall": 0.0
                },
                "metadata": {
                    "record_id": record_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "version": "1.0"
                }
            }
            
            with open(dimension_tags_path, 'w', encoding='utf-8') as f:
                json.dump(empty_tags, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "actions": actions
        }


# ==================== 查询接口 ====================

class DimensionQuery:
    """维度查询接口"""
    
    @staticmethod
    def get_all_records() -> List[str]:
        """
        获取所有记录ID
        
        Returns:
            List[str]: 记录ID列表
        """
        record_ids = []
        
        if not os.path.exists(StoragePaths.DIMENSION_TAGS_DIR):
            return record_ids
        
        for filename in os.listdir(StoragePaths.DIMENSION_TAGS_DIR):
            if filename.endswith('.json'):
                record_id = filename[:-5]  # 移除.json后缀
                record_ids.append(record_id)
        
        return record_ids
    
    @staticmethod
    def get_records_by_dimension(dimension: str, intensity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        按维度查询记录
        
        Args:
            dimension: 维度名称
            intensity: 强度过滤（可选）
        Returns:
            List[Dict[str, Any]]: 匹配的记录列表
        """
        from dimension_tagger import validate_dimension_names
        
        # 验证维度名称
        if not validate_dimension_names([dimension]):
            return []
        
        matching_records = []
        
        if not os.path.exists(StoragePaths.DIMENSION_TAGS_DIR):
            return matching_records
        
        for filename in os.listdir(StoragePaths.DIMENSION_TAGS_DIR):
            if filename.endswith('.json'):
                try:
                    file_path = os.path.join(StoragePaths.DIMENSION_TAGS_DIR, filename)
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
    
    @staticmethod
    def get_dimension_combination_distribution() -> List[Dict[str, Any]]:
        """
        获取维度组合分布
        
        Returns:
            List[Dict[str, Any]]: 维度组合分布列表
        """
        if not os.path.exists(StoragePaths.DIMENSION_TAGS_DIR):
            return []
        
        combination_counts = {}
        total_records = 0
        
        for filename in os.listdir(StoragePaths.DIMENSION_TAGS_DIR):
            if filename.endswith('.json'):
                try:
                    file_path = os.path.join(StoragePaths.DIMENSION_TAGS_DIR, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        dimension_tags = json.load(f)
                    
                    current_dims = dimension_tags.get("current_dimensions", {})
                    active_dims = current_dims.get("active", [])
                    
                    # 创建组合键（排序后的元组）
                    combination_key = tuple(sorted(active_dims))
                    
                    combination_counts[combination_key] = combination_counts.get(combination_key, 0) + 1
                    total_records += 1
                
                except Exception as e:
                    print(f"读取文件 {filename} 失败: {str(e)}")
                    continue
        
        # 转换为分布列表
        distribution = []
        for combination, count in combination_counts.items():
            distribution.append({
                "combination": list(combination),
                "count": count,
                "percentage": count / total_records if total_records > 0 else 0.0
            })
        
        # 按数量降序排序
        distribution.sort(key=lambda x: x["count"], reverse=True)
        
        return distribution
    
    @staticmethod
    def get_records_by_time_range(start_time: str, end_time: str) -> List[Dict[str, Any]]:
        """
        按时间范围查询记录
        
        Args:
            start_time: 开始时间（ISO 8601格式）
            end_time: 结束时间（ISO 8601格式）
        
        Returns:
            List[Dict[str, Any]]: 匹配的记录列表
        """
        matching_records = []
        
        if not os.path.exists(StoragePaths.DIMENSION_TAGS_DIR):
            return matching_records
        
        for filename in os.listdir(StoragePaths.DIMENSION_TAGS_DIR):
            if filename.endswith('.json'):
                try:
                    file_path = os.path.join(StoragePaths.DIMENSION_TAGS_DIR, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        dimension_tags = json.load(f)
                    
                    timestamp = dimension_tags.get("metadata", {}).get("timestamp", "")
                    
                    # 检查时间范围
                    if start_time <= timestamp <= end_time:
                        matching_records.append(dimension_tags)
                
                except Exception as e:
                    print(f"读取文件 {filename} 失败: {str(e)}")
                    continue
        
        return matching_records


# ==================== 数据清理 ====================

class DataCleanup:
    """数据清理管理"""
    
    @staticmethod
    def cleanup_orphaned_files() -> Dict[str, Any]:
        """
        清理孤立文件（没有对应记录ID的文件）
        
        Returns:
            Dict[str, Any]: 清理结果 {"cleaned": int, "errors": List[str]}
        """
        errors = []
        cleaned = 0
        
        try:
            # 获取所有有效的记录ID
            valid_record_ids = set(DimensionQuery.get_all_records())
            
            # 清理升维历史目录中的孤立文件
            if os.path.exists(StoragePaths.ELEVATION_HISTORY_DIR):
                for filename in os.listdir(StoragePaths.ELEVATION_HISTORY_DIR):
                    # 检查是否是历史文件
                    if filename.endswith('_history.json'):
                        record_id = filename[:-13]  # 移除_history.json后缀
                        if record_id not in valid_record_ids:
                            # 孤立文件，删除
                            file_path = os.path.join(
                                StoragePaths.ELEVATION_HISTORY_DIR,
                                filename
                            )
                            os.remove(file_path)
                            cleaned += 1
                    
                    # 检查是否是建议文件
                    elif filename.endswith('_suggestion.json'):
                        record_id = filename[:-15]  # 移除_suggestion.json后缀
                        if record_id not in valid_record_ids:
                            # 孤立文件，删除
                            file_path = os.path.join(
                                StoragePaths.ELEVATION_HISTORY_DIR,
                                filename
                            )
                            os.remove(file_path)
                            cleaned += 1
        
        except Exception as e:
            errors.append(f"清理孤立文件时出错: {str(e)}")
        
        return {
            "cleaned": cleaned,
            "errors": errors
        }
    
    @staticmethod
    def cleanup_old_records(days: int = 30) -> Dict[str, Any]:
        """
        清理旧记录（超过指定天数的记录）
        
        Args:
            days: 天数阈值
        
        Returns:
            Dict[str, Any]: 清理结果 {"cleaned": int, "errors": List[str]}
        """
        errors = []
        cleaned = 0
        
        try:
            from datetime import datetime, timedelta
            
            threshold_time = datetime.utcnow() - timedelta(days=days)
            threshold_str = threshold_time.isoformat() + "Z"
            
            # 获取所有记录
            all_records = DimensionQuery.get_all_records()
            
            for record_id in all_records:
                try:
                    # 读取维度标签
                    dimension_tags_path = os.path.join(
                        StoragePaths.DIMENSION_TAGS_DIR,
                        f"{record_id}.json"
                    )
                    
                    with open(dimension_tags_path, 'r', encoding='utf-8') as f:
                        dimension_tags = json.load(f)
                    
                    timestamp_str = dimension_tags.get("metadata", {}).get("timestamp", "")
                    
                    if timestamp_str:
                        record_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        
                        # 如果记录超过阈值，删除
                        if record_time < threshold_time:
                            # 删除维度标签
                            os.remove(dimension_tags_path)
                            
                            # 删除升维历史文件
                            history_path = os.path.join(
                                StoragePaths.ELEVATION_HISTORY_DIR,
                                f"{record_id}_history.json"
                            )
                            if os.path.exists(history_path):
                                os.remove(history_path)
                            
                            # 删除升维建议文件
                            suggestion_path = os.path.join(
                                StoragePaths.ELEVATION_HISTORY_DIR,
                                f"{record_id}_suggestion.json"
                            )
                            if os.path.exists(suggestion_path):
                                os.remove(suggestion_path)
                            
                            cleaned += 1
                
                except Exception as e:
                    errors.append(f"清理记录 {record_id} 时出错: {str(e)}")
                    continue
        
        except Exception as e:
            errors.append(f"清理旧记录时出错: {str(e)}")
        
        return {
            "cleaned": cleaned,
            "errors": errors
        }


# ==================== 主函数（示例） ====================

if __name__ == "__main__":
    print("五维智力存储管理器")
    print("=" * 50)
    
    # 确保存储目录存在
    StoragePaths.ensure_directories()
    print("\n存储目录已创建")
    
    # 示例1：获取所有记录
    print("\n示例1：获取所有记录")
    all_records = DimensionQuery.get_all_records()
    print(f"所有记录ID: {all_records}")
    
    # 示例2：按维度查询记录
    print("\n示例2：按维度查询记录")
    records = DimensionQuery.get_records_by_dimension("algorithmic")
    print(f"使用算法智力的记录数量: {len(records)}")
    
    # 示例3：获取维度组合分布
    print("\n示例3：获取维度组合分布")
    distribution = DimensionQuery.get_dimension_combination_distribution()
    print(f"维度组合分布: {distribution}")
    
    # 示例4：数据一致性检查
    print("\n示例4：数据一致性检查")
    if all_records:
        consistency = DataConsistency.validate_record_consistency(all_records[0])
        print(f"记录 {all_records[0]} 的一致性: {consistency}")
    
    # 示例5：清理孤立文件
    print("\n示例5：清理孤立文件")
    cleanup_result = DataCleanup.cleanup_orphaned_files()
    print(f"清理结果: {cleanup_result}")
    
    print("\n五维智力存储管理器 - 测试完成")
