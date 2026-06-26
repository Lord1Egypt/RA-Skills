"""
处理管道
将多个处理器组合成处理流水线
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from .base import DataProcessor, ProcessingResult
from .factory import ProcessorFactory
from ..exceptions import ProcessingError

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """管道处理结果数据类"""
    success: bool
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    total_time: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
            "step_count": len(self.steps),
            "successful_steps": sum(1 for step in self.steps if step.get("success", False)),
            "total_time": self.total_time,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "final_data_size": len(self.data) if isinstance(self.data, list) else 1,
            "steps": self.steps
        }


class ProcessorPipeline:
    """处理器管道"""
    
    def __init__(self, processors: Optional[List[DataProcessor]] = None):
        """
        初始化处理管道
        
        Args:
            processors: 处理器列表，如果为None则创建空管道
        """
        self.processors: List[DataProcessor] = processors or []
        self._current_data: Any = None
        self._pipeline_stats: Dict[str, Any] = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_processing_time": 0.0,
            "average_processing_time": 0.0
        }
        
        logger.debug(f"初始化处理管道，包含 {len(self.processors)} 个处理器")
    
    def add_processor(self, processor: DataProcessor, position: Optional[int] = None) -> None:
        """
        添加处理器到管道
        
        Args:
            processor: 要添加的处理器
            position: 插入位置，如果为None则添加到末尾
        """
        if position is None:
            self.processors.append(processor)
            logger.debug(f"添加处理器到管道末尾: {processor.name}")
        else:
            if position < 0 or position > len(self.processors):
                raise ValueError(f"无效的插入位置: {position}")
            self.processors.insert(position, processor)
            logger.debug(f"添加处理器到管道位置 {position}: {processor.name}")
    
    def remove_processor(self, processor_name: str) -> bool:
        """
        从管道中移除处理器
        
        Args:
            processor_name: 处理器名称
            
        Returns:
            bool: 是否成功移除
        """
        for i, processor in enumerate(self.processors):
            if processor.name == processor_name:
                del self.processors[i]
                logger.debug(f"从管道中移除处理器: {processor_name}")
                return True
        
        logger.warning(f"未找到要移除的处理器: {processor_name}")
        return False
    
    def reorder_processors(self, new_order: List[str]) -> None:
        """
        重新排序处理器
        
        Args:
            new_order: 新的处理器名称顺序列表
        """
        # 验证新顺序包含所有处理器
        processor_names = {p.name for p in self.processors}
        new_order_set = set(new_order)
        
        if processor_names != new_order_set:
            missing = processor_names - new_order_set
            extra = new_order_set - processor_names
            raise ValueError(f"无效的排序: 缺失 {missing}, 多余 {extra}")
        
        # 创建新的处理器列表
        processor_map = {p.name: p for p in self.processors}
        self.processors = [processor_map[name] for name in new_order]
        
        logger.debug(f"重新排序处理器管道: {new_order}")
    
    def process(self, data: Any, stop_on_error: bool = False) -> PipelineResult:
        """
        处理数据（通过所有处理器）
        
        Args:
            data: 输入数据
            stop_on_error: 出错时是否停止处理
            
        Returns:
            PipelineResult: 管道处理结果
        """
        import time
        start_time = time.time()
        self._pipeline_stats["total_runs"] += 1
        
        # 初始化结果
        pipeline_result = PipelineResult(
            success=True,
            data=data,
            steps=[]
        )
        
        current_data = data
        
        try:
            logger.info(f"开始管道处理，包含 {len(self.processors)} 个处理器")
            
            for i, processor in enumerate(self.processors):
                step_start_time = time.time()
                
                try:
                    # 执行处理器
                    step_result = processor.process(current_data)
                    
                    # 记录步骤信息
                    step_info = {
                        "index": i,
                        "processor": processor.name,
                        "success": step_result.success,
                        "processing_time": step_result.metadata.get("processing_time", 0),
                        "input_size": step_result.metadata.get("input_size", "unknown"),
                        "output_size": step_result.metadata.get("output_size", "unknown"),
                        "errors": step_result.errors,
                        "warnings": step_result.warnings
                    }
                    
                    pipeline_result.steps.append(step_info)
                    
                    # 处理步骤结果
                    if step_result.success:
                        # 更新当前数据
                        current_data = step_result.data
                        
                        # 添加警告
                        if step_result.warnings:
                            pipeline_result.warnings.extend(step_result.warnings)
                        
                        logger.debug(
                            f"管道步骤 {i+1}/{len(self.processors)} 完成: "
                            f"{processor.name}, 耗时: {step_info['processing_time']:.2f}s"
                        )
                    
                    else:
                        # 步骤失败
                        pipeline_result.errors.extend(step_result.errors)
                        
                        if stop_on_error:
                            logger.error(
                                f"管道步骤 {i+1}/{len(self.processors)} 失败且停止处理: "
                                f"{processor.name}, 错误: {step_result.errors}"
                            )
                            pipeline_result.success = False
                            break
                        else:
                            logger.warning(
                                f"管道步骤 {i+1}/{len(self.processors)} 失败但继续处理: "
                                f"{processor.name}, 错误: {step_result.errors}"
                            )
                            # 继续使用当前数据（不更新）
                
                except Exception as e:
                    # 处理器抛出异常
                    error_msg = f"管道步骤 {i+1}/{len(self.processors)} 异常: {processor.name}, 错误: {e}"
                    logger.error(error_msg, exc_info=True)
                    
                    step_info = {
                        "index": i,
                        "processor": processor.name,
                        "success": False,
                        "processing_time": time.time() - step_start_time,
                        "error": str(e)
                    }
                    
                    pipeline_result.steps.append(step_info)
                    pipeline_result.errors.append(error_msg)
                    
                    if stop_on_error:
                        pipeline_result.success = False
                        break
            
            # 更新管道结果
            end_time = time.time()
            pipeline_result.total_time = end_time - start_time
            pipeline_result.data = current_data
            
            # 更新统计信息
            if pipeline_result.success:
                self._pipeline_stats["successful_runs"] += 1
            else:
                self._pipeline_stats["failed_runs"] += 1
            
            self._pipeline_stats["total_processing_time"] += pipeline_result.total_time
            if self._pipeline_stats["total_runs"] > 0:
                self._pipeline_stats["average_processing_time"] = (
                    self._pipeline_stats["total_processing_time"] / self._pipeline_stats["total_runs"]
                )
            
            logger.info(
                f"管道处理完成: 成功={pipeline_result.success}, "
                f"步骤数={len(pipeline_result.steps)}, "
                f"总耗时={pipeline_result.total_time:.2f}s"
            )
            
            return pipeline_result
            
        except Exception as e:
            # 管道整体异常
            end_time = time.time()
            error_msg = f"管道处理异常: {e}"
            logger.error(error_msg, exc_info=True)
            
            self._pipeline_stats["failed_runs"] += 1
            
            return PipelineResult(
                success=False,
                data=data,
                total_time=end_time - start_time,
                errors=[error_msg],
                steps=pipeline_result.steps
            )
    
    def clear(self) -> None:
        """清空管道中的所有处理器"""
        self.processors.clear()
        logger.debug("清空处理管道")
    
    @property
    def count(self) -> int:
        """获取管道中的处理器数量"""
        return len(self.processors)
    
    @property
    def enabled_count(self) -> int:
        """获取启用的处理器数量"""
        return sum(1 for p in self.processors if p.enabled)
    
    def get_processor(self, name: str) -> Optional[DataProcessor]:
        """
        根据名称获取处理器
        
        Args:
            name: 处理器名称
            
        Returns:
            处理器实例，如果未找到则返回None
        """
        for processor in self.processors:
            if processor.name == name:
                return processor
        return None
    
    def enable_processor(self, name: str) -> bool:
        """
        启用处理器
        
        Args:
            name: 处理器名称
            
        Returns:
            bool: 是否成功启用
        """
        processor = self.get_processor(name)
        if processor:
            processor.enabled = True
            logger.debug(f"启用处理器: {name}")
            return True
        return False
    
    def disable_processor(self, name: str) -> bool:
        """
        禁用处理器
        
        Args:
            name: 处理器名称
            
        Returns:
            bool: 是否成功禁用
        """
        processor = self.get_processor(name)
        if processor:
            processor.enabled = False
            logger.debug(f"禁用处理器: {name}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取管道统计信息"""
        processor_stats = []
        for processor in self.processors:
            processor_stats.append({
                "name": processor.name,
                "enabled": processor.enabled,
                **processor.get_stats()
            })
        
        return {
            "pipeline_stats": self._pipeline_stats,
            "processor_count": self.count,
            "enabled_processor_count": self.enabled_count,
            "processor_details": processor_stats
        }
    
    def validate(self) -> Dict[str, Any]:
        """
        验证管道配置
        
        Returns:
            验证结果
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "processor_validations": []
        }
        
        try:
            if not self.processors:
                result["warnings"].append("管道为空")
            
            for i, processor in enumerate(self.processors):
                processor_result = {
                    "index": i,
                    "name": processor.name,
                    "enabled": processor.enabled,
                    "valid": True,
                    "errors": [],
                    "warnings": []
                }
                
                # 验证处理器配置
                if not processor.validate_config():
                    processor_result["valid"] = False
                    processor_result["errors"].append("处理器配置验证失败")
                
                # 检查处理器名称唯一性
                duplicate_names = [p.name for p in self.processors if p.name == processor.name]
                if len(duplicate_names) > 1:
                    processor_result["warnings"].append("处理器名称重复")
                
                result["processor_validations"].append(processor_result)
                
                # 更新总体验证结果
                if not processor_result["valid"]:
                    result["valid"] = False
                    result["errors"].append(f"处理器验证失败: {processor.name}")
                
                if processor_result["warnings"]:
                    result["warnings"].extend([
                        f"处理器警告 {processor.name}: {w}" 
                        for w in processor_result["warnings"]
                    ])
            
            logger.debug("管道验证完成")
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"管道验证异常: {e}")
        
        return result
    
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> 'ProcessorPipeline':
        """
        从配置创建管道
        
        Args:
            config: 管道配置
            
        Returns:
            ProcessorPipeline: 创建的管道
        """
        processors = []
        
        # 获取处理器配置
        processor_configs = config.get("processors", [])
        
        for proc_config in processor_configs:
            try:
                processor_type = proc_config.get("type")
                processor_name = proc_config.get("name", processor_type)
                enabled = proc_config.get("enabled", True)
                processor_params = proc_config.get("params", {})
                
                # 创建处理器
                processor = ProcessorFactory.create_processor(
                    processor_type,
                    name=processor_name,
                    enabled=enabled,
                    **processor_params
                )
                
                processors.append(processor)
                logger.debug(f"从配置创建处理器: {processor_name}")
                
            except Exception as e:
                logger.error(f"从配置创建处理器失败: {e}")
                if config.get("strict_mode", False):
                    raise
        
        return cls(processors)