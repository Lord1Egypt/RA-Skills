"""
数据采集器核心类
"""

import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from .config import Config, SourceConfig, ProcessingConfig, ExportConfig
from .adapters import SourceAdapter, AdapterFactory
from .processors import ProcessorPipeline
from .exporters import Exporter, ExportFactory
from .scheduler import Scheduler
from .exceptions import DataHarvesterError, ConfigurationError

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """数据源类型枚举"""
    WEB = "web"
    API = "api"
    FILE = "file"
    DATABASE = "database"
    CUSTOM = "custom"


@dataclass
class HarvestResult:
    """采集结果数据类"""
    success: bool
    data: Any
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "data_count": len(self.data) if isinstance(self.data, list) else 1,
            "metadata": self.metadata,
            "errors": self.errors
        }


class DataHarvester:
    """智能数据采集器主类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化数据采集器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = Config.load(config_path) if config_path else Config()
        self.adapters: Dict[str, SourceAdapter] = {}
        self.processors: ProcessorPipeline = ProcessorPipeline()
        self.exporters: Dict[str, Exporter] = {}
        self.scheduler: Optional[Scheduler] = None
        self._initialized = False
        
        logger.info(f"DataHarvester v{__version__} 初始化")
    
    def initialize(self) -> None:
        """初始化采集器组件"""
        if self._initialized:
            return
            
        try:
            # 初始化适配器
            self._init_adapters()
            
            # 初始化处理器管道
            self._init_processors()
            
            # 初始化导出器
            self._init_exporters()
            
            # 初始化调度器（如果启用）
            if self.config.scheduler.enabled:
                try:
                    # 尝试使用APScheduler实现
                    from .scheduler import APScheduler
                    self.scheduler = APScheduler(self.config.scheduler)
                except (ImportError, AttributeError):
                    # 回退到基础调度器
                    logger.warning("APScheduler不可用，使用基础调度器（功能受限）")
                    from .scheduler import Scheduler
                    self.scheduler = Scheduler(self.config.scheduler)
                
                self.scheduler.start()
                
            self._initialized = True
            logger.info("数据采集器初始化完成")
            
        except Exception as e:
            logger.error(f"数据采集器初始化失败: {e}")
            raise DataHarvesterError(f"初始化失败: {e}")
    
    def _init_adapters(self) -> None:
        """初始化数据源适配器"""
        for source_name, source_config in self.config.sources.items():
            try:
                adapter = AdapterFactory.create_adapter(source_config)
                self.adapters[source_name] = adapter
                logger.debug(f"初始化适配器: {source_name} ({source_config.type})")
            except Exception as e:
                logger.error(f"初始化适配器失败 {source_name}: {e}")
                if self.config.strict_mode:
                    raise
    
    def _init_processors(self) -> None:
        """初始化处理器管道"""
        for processor_config in self.config.processing.pipeline:
            try:
                processor = ProcessorFactory.create_processor(processor_config)
                self.processors.add_processor(processor)
                logger.debug(f"添加处理器: {processor_config.name}")
            except Exception as e:
                logger.error(f"添加处理器失败 {processor_config.name}: {e}")
                if self.config.strict_mode:
                    raise
    
    def _init_exporters(self) -> None:
        """初始化导出器"""
        for export_config in self.config.exports:
            try:
                exporter = ExportFactory.create_exporter(export_config)
                self.exporters[export_config.name] = exporter
                logger.debug(f"初始化导出器: {export_config.name}")
            except Exception as e:
                logger.error(f"初始化导出器失败 {export_config.name}: {e}")
                if self.config.strict_mode:
                    raise
    
    def collect(self, source_name: str, **kwargs) -> HarvestResult:
        """
        从指定数据源采集数据
        
        Args:
            source_name: 数据源名称
            **kwargs: 传递给适配器的额外参数
            
        Returns:
            HarvestResult: 采集结果
        """
        if not self._initialized:
            self.initialize()
            
        if source_name not in self.adapters:
            error_msg = f"未找到数据源适配器: {source_name}"
            logger.error(error_msg)
            return HarvestResult(
                success=False,
                data=None,
                source=source_name,
                errors=[error_msg]
            )
        
        try:
            adapter = self.adapters[source_name]
            logger.info(f"开始采集数据源: {source_name}")
            
            # 执行采集
            raw_data = adapter.fetch(**kwargs)
            
            # 处理数据
            processed_data = self.processors.process(raw_data)
            
            # 创建结果
            result = HarvestResult(
                success=True,
                data=processed_data,
                source=source_name,
                metadata={
                    "adapter_type": adapter.__class__.__name__,
                    "data_size": len(processed_data) if isinstance(processed_data, list) else 1,
                    "processing_time": datetime.now()
                }
            )
            
            logger.info(f"数据采集完成: {source_name}, 数据量: {result.metadata['data_size']}")
            return result
            
        except Exception as e:
            error_msg = f"数据采集失败 {source_name}: {e}"
            logger.error(error_msg, exc_info=True)
            return HarvestResult(
                success=False,
                data=None,
                source=source_name,
                errors=[str(e)]
            )
    
    def collect_all(self, **kwargs) -> Dict[str, HarvestResult]:
        """
        从所有配置的数据源采集数据
        
        Args:
            **kwargs: 传递给适配器的额外参数
            
        Returns:
            Dict[str, HarvestResult]: 每个数据源的采集结果
        """
        if not self._initialized:
            self.initialize()
            
        results = {}
        for source_name in self.adapters:
            result = self.collect(source_name, **kwargs)
            results[source_name] = result
            
        return results
    
    def export(self, data: Any, exporter_name: str, **kwargs) -> bool:
        """
        导出数据
        
        Args:
            data: 要导出的数据
            exporter_name: 导出器名称
            **kwargs: 导出器额外参数
            
        Returns:
            bool: 导出是否成功
        """
        if exporter_name not in self.exporters:
            logger.error(f"未找到导出器: {exporter_name}")
            return False
            
        try:
            exporter = self.exporters[exporter_name]
            success = exporter.export(data, **kwargs)
            
            if success:
                logger.info(f"数据导出成功: {exporter_name}")
            else:
                logger.warning(f"数据导出失败: {exporter_name}")
                
            return success
            
        except Exception as e:
            logger.error(f"数据导出异常 {exporter_name}: {e}")
            return False
    
    def schedule_task(self, source_name: str, schedule: str, **kwargs) -> Optional[str]:
        """
        调度定时采集任务
        
        Args:
            source_name: 数据源名称
            schedule: 调度表达式（Cron格式）
            **kwargs: 采集参数
            
        Returns:
            Optional[str]: 任务ID，如果调度失败则返回None
        """
        if not self.scheduler:
            logger.error("调度器未启用")
            return None
            
        try:
            task_id = self.scheduler.add_task(
                func=self.collect,
                args=(source_name,),
                kwargs=kwargs,
                schedule=schedule,
                name=f"harvest_{source_name}"
            )
            
            logger.info(f"调度任务创建成功: {task_id} ({source_name})")
            return task_id
            
        except Exception as e:
            logger.error(f"调度任务创建失败 {source_name}: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """获取采集器状态"""
        return {
            "initialized": self._initialized,
            "adapter_count": len(self.adapters),
            "processor_count": self.processors.count,
            "exporter_count": len(self.exporters),
            "scheduler_enabled": self.scheduler is not None,
            "scheduler_running": self.scheduler.running if self.scheduler else False,
            "active_tasks": self.scheduler.task_count if self.scheduler else 0,
            "version": __version__,
            "config_path": self.config.config_path
        }
    
    def shutdown(self) -> None:
        """关闭采集器"""
        if self.scheduler:
            self.scheduler.shutdown()
            
        self._initialized = False
        logger.info("数据采集器已关闭")


# 导入版本信息
from . import __version__