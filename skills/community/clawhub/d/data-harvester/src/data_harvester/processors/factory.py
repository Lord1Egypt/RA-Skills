"""
处理器工厂
用于创建和管理数据处理器
"""

import logging
from typing import Dict, Type, Optional, Any

from ..config import ProcessingStrategy
from .base import DataProcessor, CleanProcessor, TransformProcessor
from ..exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ProcessorFactory:
    """处理器工厂类"""
    
    # 处理器类型映射
    _processor_registry: Dict[str, Type[DataProcessor]] = {
        "clean": CleanProcessor,
        "transform": TransformProcessor,
        # 其他处理器将在后续添加
    }
    
    # 自定义处理器注册表
    _custom_processors: Dict[str, Type[DataProcessor]] = {}
    
    @classmethod
    def create_processor(cls, processor_type: str, name: Optional[str] = None, **config) -> DataProcessor:
        """
        创建处理器实例
        
        Args:
            processor_type: 处理器类型
            name: 处理器名称（可选，默认为类型名）
            **config: 处理器配置
            
        Returns:
            DataProcessor: 处理器实例
            
        Raises:
            ConfigurationError: 配置错误或处理器类型不支持
        """
        try:
            # 获取处理器名称
            processor_name = name or processor_type
            
            # 获取处理器类
            processor_class = cls._get_processor_class(processor_type)
            if processor_class is None:
                raise ConfigurationError(f"不支持的处理器类型: {processor_type}")
            
            # 创建处理器实例
            processor = processor_class(name=processor_name, **config)
            
            # 验证处理器配置
            if not processor.validate_config():
                logger.warning(f"处理器配置验证警告: {processor_name}")
            
            logger.debug(f"创建处理器: {processor_name} ({processor_type})")
            return processor
            
        except Exception as e:
            logger.error(f"创建处理器失败 {processor_type}: {e}")
            raise ConfigurationError(f"创建处理器失败 {processor_type}: {e}") from e
    
    @classmethod
    def create_processor_by_strategy(cls, strategy: ProcessingStrategy, **config) -> DataProcessor:
        """
        根据处理策略创建处理器
        
        Args:
            strategy: 处理策略
            **config: 处理器配置
            
        Returns:
            DataProcessor: 处理器实例
        """
        # 策略到处理器的映射
        strategy_mapping = {
            ProcessingStrategy.CLEAN: "clean",
            ProcessingStrategy.TRANSFORM: "transform",
            ProcessingStrategy.ENRICH: "enrich",  # 将在后续实现
            ProcessingStrategy.VALIDATE: "validate",  # 将在后续实现
            ProcessingStrategy.DEDUPLICATE: "deduplicate",  # 将在后续实现
        }
        
        processor_type = strategy_mapping.get(strategy)
        if not processor_type:
            raise ConfigurationError(f"不支持的处理策略: {strategy}")
        
        return cls.create_processor(processor_type, name=str(strategy), **config)
    
    @classmethod
    def _get_processor_class(cls, processor_type: str) -> Optional[Type[DataProcessor]]:
        """
        获取处理器类
        
        Args:
            processor_type: 处理器类型
            
        Returns:
            处理器类，如果找不到则返回None
        """
        # 首先检查自定义处理器
        if processor_type in cls._custom_processors:
            return cls._custom_processors[processor_type]
        
        # 检查内置处理器
        return cls._processor_registry.get(processor_type)
    
    @classmethod
    def register_processor(cls, processor_type: str, processor_class: Type[DataProcessor]) -> None:
        """
        注册自定义处理器
        
        Args:
            processor_type: 处理器类型
            processor_class: 处理器类
        """
        if not issubclass(processor_class, DataProcessor):
            raise ValueError(f"处理器类必须继承自 DataProcessor: {processor_class}")
        
        cls._custom_processors[processor_type] = processor_class
        logger.info(f"注册自定义处理器: {processor_type} -> {processor_class.__name__}")
    
    @classmethod
    def unregister_processor(cls, processor_type: str) -> None:
        """
        注销自定义处理器
        
        Args:
            processor_type: 处理器类型
        """
        if processor_type in cls._custom_processors:
            del cls._custom_processors[processor_type]
            logger.info(f"注销自定义处理器: {processor_type}")
    
    @classmethod
    def list_available_processors(cls) -> Dict[str, str]:
        """
        列出可用的处理器
        
        Returns:
            处理器类型和类名的映射
        """
        processors = {}
        
        # 内置处理器
        for processor_type, processor_class in cls._processor_registry.items():
            processors[processor_type] = processor_class.__name__
        
        # 自定义处理器
        for processor_type, processor_class in cls._custom_processors.items():
            processors[processor_type] = processor_class.__name__
        
        return processors
    
    @classmethod
    def get_processor_info(cls, processor_type: str) -> Dict[str, Any]:
        """
        获取处理器信息
        
        Args:
            processor_type: 处理器类型
            
        Returns:
            处理器信息
        """
        processor_class = cls._get_processor_class(processor_type)
        if processor_class is None:
            return {"type": processor_type, "available": False}
        
        # 获取默认配置
        default_config = {}
        if hasattr(processor_class, '__init__'):
            import inspect
            init_signature = inspect.signature(processor_class.__init__)
            for param_name, param in init_signature.parameters.items():
                if param_name not in ['self', 'name', 'enabled'] and param.default != inspect.Parameter.empty:
                    default_config[param_name] = param.default
        
        return {
            "type": processor_type,
            "available": True,
            "class_name": processor_class.__name__,
            "module": processor_class.__module__,
            "description": processor_class.__doc__ or "无描述",
            "default_config": default_config
        }
    
    @classmethod
    def create_processors_from_strategies(cls, strategies: list, **configs) -> list:
        """
        从策略列表批量创建处理器
        
        Args:
            strategies: 处理策略列表
            **configs: 处理器配置（按类型）
            
        Returns:
            处理器列表
        """
        processors = []
        
        for strategy in strategies:
            try:
                # 获取该策略的特定配置
                strategy_config = configs.get(str(strategy), {})
                
                processor = cls.create_processor_by_strategy(strategy, **strategy_config)
                processors.append(processor)
                logger.info(f"创建处理器成功: {strategy}")
            except Exception as e:
                logger.error(f"创建处理器失败 {strategy}: {e}")
                # 根据需求决定是否抛出异常
                if configs.get("strict_mode", False):
                    raise
        
        return processors
    
    @classmethod
    def validate_processor_config(cls, processor_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证处理器配置
        
        Args:
            processor_type: 处理器类型
            config: 处理器配置
            
        Returns:
            验证结果
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "required_fields": [],
            "optional_fields": []
        }
        
        try:
            # 检查处理器类型是否支持
            processor_class = cls._get_processor_class(processor_type)
            if not processor_class:
                result["valid"] = False
                result["errors"].append(f"不支持的处理器类型: {processor_type}")
                return result
            
            # 检查配置项
            # 这里可以根据具体的处理器类添加验证逻辑
            
            # 示例：检查clean处理器的配置
            if processor_type == "clean":
                if "remove_duplicates" in config and not isinstance(config["remove_duplicates"], bool):
                    result["warnings"].append("remove_duplicates 应该是布尔值")
                
                if "encoding" in config and not isinstance(config["encoding"], str):
                    result["warnings"].append("encoding 应该是字符串")
            
            # 示例：检查transform处理器的配置
            elif processor_type == "transform":
                if "number_precision" in config and not isinstance(config["number_precision"], int):
                    result["warnings"].append("number_precision 应该是整数")
                
                if "date_format" in config and not isinstance(config["date_format"], str):
                    result["warnings"].append("date_format 应该是字符串")
            
            logger.debug(f"处理器配置验证完成: {processor_type}")
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"配置验证异常: {e}")
        
        return result