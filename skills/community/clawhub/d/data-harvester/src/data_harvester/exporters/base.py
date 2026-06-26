"""
导出器基类模块
定义数据导出器的通用接口
"""

import logging
import json
import csv
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
import io

from ..config import ExportFormat
from ..exceptions import ExportError

logger = logging.getLogger(__name__)


class Exporter(ABC):
    """数据导出器基类"""
    
    def __init__(self, name: str, format: ExportFormat, enabled: bool = True, **config):
        """
        初始化导出器
        
        Args:
            name: 导出器名称
            format: 导出格式
            enabled: 是否启用
            **config: 导出器配置
        """
        self.name = name
        self.format = format
        self.enabled = enabled
        self.config = config
        
        # 统计信息
        self.export_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_export_time = 0.0
        self.last_export_time: Optional[datetime] = None
        self.total_data_size = 0
        
        logger.debug(f"初始化导出器: {self.name} ({format})")
    
    def export(self, data: Any, **kwargs) -> bool:
        """
        导出数据（包装方法，包含错误处理和统计）
        
        Args:
            data: 要导出的数据
            **kwargs: 额外参数
            
        Returns:
            bool: 导出是否成功
        """
        if not self.enabled:
            logger.warning(f"导出器已禁用: {self.name}")
            return False
        
        import time
        start_time = time.time()
        self.export_count += 1
        self.last_export_time = datetime.now()
        
        try:
            logger.info(f"开始导出数据: {self.name}")
            
            # 合并配置参数和传递的参数
            export_kwargs = {**self.config, **kwargs}
            
            # 验证数据
            if data is None:
                raise ExportError(f"导出数据不能为空: {self.name}")
            
            # 执行实际的数据导出
            success = self._export_impl(data, **export_kwargs)
            
            # 统计
            end_time = time.time()
            export_time = end_time - start_time
            self.total_export_time += export_time
            
            if success:
                self.success_count += 1
                data_size = self._get_data_size(data)
                self.total_data_size += data_size
                
                logger.info(
                    f"数据导出成功: {self.name}, "
                    f"数据大小: {data_size}, "
                    f"耗时: {export_time:.2f}s"
                )
            else:
                self.error_count += 1
                logger.warning(f"数据导出失败: {self.name}")
            
            return success
            
        except Exception as e:
            # 统计失败
            end_time = time.time()
            export_time = end_time - start_time
            self.total_export_time += export_time
            self.error_count += 1
            
            error_msg = f"数据导出异常 {self.name}: {e}"
            logger.error(error_msg, exc_info=True)
            return False
    
    @abstractmethod
    def _export_impl(self, data: Any, **kwargs) -> bool:
        """
        实际的数据导出实现（子类必须实现）
        
        Args:
            data: 要导出的数据
            **kwargs: 导出参数
            
        Returns:
            bool: 导出是否成功
        """
        pass
    
    def _get_data_size(self, data: Any) -> int:
        """获取数据大小（字节数估计）"""
        if data is None:
            return 0
        
        try:
            if isinstance(data, (list, dict)):
                return len(str(data).encode('utf-8'))
            elif isinstance(data, str):
                return len(data.encode('utf-8'))
            elif isinstance(data, bytes):
                return len(data)
            else:
                return len(str(data).encode('utf-8'))
        except:
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取导出器统计信息"""
        avg_time = 0
        if self.export_count > 0:
            avg_time = self.total_export_time / self.export_count
        
        success_rate = 0
        if self.export_count > 0:
            success_rate = (self.success_count / self.export_count) * 100
        
        avg_data_size = 0
        if self.success_count > 0:
            avg_data_size = self.total_data_size / self.success_count
        
        return {
            "name": self.name,
            "format": self.format.value,
            "enabled": self.enabled,
            "export_count": self.export_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "total_export_time": f"{self.total_export_time:.2f}s",
            "average_export_time": f"{avg_time:.2f}s",
            "total_data_size": self.total_data_size,
            "average_data_size": f"{avg_data_size:.1f} bytes",
            "last_export_time": self.last_export_time.isoformat() if self.last_export_time else None
        }
    
    def validate_config(self) -> bool:
        """
        验证导出器配置
        
        Returns:
            bool: 配置是否有效
        """
        try:
            if not self.name:
                logger.error("导出器名称不能为空")
                return False
            
            logger.debug(f"导出器配置验证通过: {self.name}")
            return True
            
        except Exception as e:
            logger.error(f"导出器配置验证失败 {self.name}: {e}")
            return False


class CsvExporter(Exporter):
    """CSV导出器"""
    
    def __init__(self, name: str = "csv", **config):
        default_config = {
            "output_path": "output.csv",
            "encoding": "utf-8",
            "delimiter": ",",
            "write_header": True,
            "quote_all": False,
            "quoting": csv.QUOTE_MINIMAL,
        }
        default_config.update(config)
        super().__init__(name, ExportFormat.CSV, **default_config)
    
    def _export_impl(self, data: Any, **kwargs) -> bool:
        """
        导出数据为CSV格式
        
        Args:
            data: 要导出的数据
            **kwargs: 导出参数
            
        Returns:
            bool: 导出是否成功
        """
        output_path = kwargs.get("output_path", "output.csv")
        encoding = kwargs.get("encoding", "utf-8")
        delimiter = kwargs.get("delimiter", ",")
        write_header = kwargs.get("write_header", True)
        quote_all = kwargs.get("quote_all", False)
        
        try:
            # 确保输出目录存在
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 准备数据
            if isinstance(data, list):
                rows = data
            elif isinstance(data, dict):
                rows = [data]
            else:
                rows = [{"value": data}]
            
            if not rows:
                logger.warning(f"导出数据为空: {self.name}")
                # 创建空文件
                output_file.touch()
                return True
            
            # 确定字段名
            if rows and isinstance(rows[0], dict):
                fieldnames = list(rows[0].keys())
            else:
                fieldnames = ["value"]
            
            # 写入CSV文件
            with open(output_file, 'w', newline='', encoding=encoding) as f:
                writer = csv.DictWriter(
                    f, 
                    fieldnames=fieldnames,
                    delimiter=delimiter,
                    quoting=csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL
                )
                
                if write_header:
                    writer.writeheader()
                
                for row in rows:
                    if isinstance(row, dict):
                        writer.writerow(row)
                    else:
                        writer.writerow({"value": row})
            
            logger.debug(f"CSV导出完成: {output_path}, 行数: {len(rows)}")
            return True
            
        except Exception as e:
            logger.error(f"CSV导出失败: {e}")
            return False


class JsonExporter(Exporter):
    """JSON导出器"""
    
    def __init__(self, name: str = "json", **config):
        default_config = {
            "output_path": "output.json",
            "encoding": "utf-8",
            "indent": 2,
            "ensure_ascii": False,
            "sort_keys": False,
        }
        default_config.update(config)
        super().__init__(name, ExportFormat.JSON, **default_config)
    
    def _export_impl(self, data: Any, **kwargs) -> bool:
        """
        导出数据为JSON格式
        
        Args:
            data: 要导出的数据
            **kwargs: 导出参数
            
        Returns:
            bool: 导出是否成功
        """
        output_path = kwargs.get("output_path", "output.json")
        encoding = kwargs.get("encoding", "utf-8")
        indent = kwargs.get("indent", 2)
        ensure_ascii = kwargs.get("ensure_ascii", False)
        sort_keys = kwargs.get("sort_keys", False)
        
        try:
            # 确保输出目录存在
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入JSON文件
            with open(output_file, 'w', encoding=encoding) as f:
                json.dump(
                    data, 
                    f, 
                    indent=indent, 
                    ensure_ascii=ensure_ascii,
                    sort_keys=sort_keys,
                    default=str  # 处理日期时间等不可序列化对象
                )
            
            logger.debug(f"JSON导出完成: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"JSON导出失败: {e}")
            return False


class ExcelExporter(Exporter):
    """Excel导出器"""
    
    def __init__(self, name: str = "excel", **config):
        default_config = {
            "output_path": "output.xlsx",
            "sheet_name": "Sheet1",
            "include_index": False,
            "engine": "openpyxl",
        }
        default_config.update(config)
        super().__init__(name, ExportFormat.EXCEL, **default_config)
    
    def _export_impl(self, data: Any, **kwargs) -> bool:
        """
        导出数据为Excel格式
        
        Args:
            data: 要导出的数据
            **kwargs: 导出参数
            
        Returns:
            bool: 导出是否成功
        """
        try:
            import pandas as pd
        except ImportError:
            logger.error("Excel导出需要pandas和openpyxl库")
            return False
        
        output_path = kwargs.get("output_path", "output.xlsx")
        sheet_name = kwargs.get("sheet_name", "Sheet1")
        include_index = kwargs.get("include_index", False)
        
        try:
            # 确保输出目录存在
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 转换数据为DataFrame
            if isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if all(isinstance(v, (list, tuple)) for v in data.values()):
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([data])
            else:
                df = pd.DataFrame({"value": [data]})
            
            # 写入Excel文件
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(
                    writer, 
                    sheet_name=sheet_name, 
                    index=include_index
                )
            
            logger.debug(f"Excel导出完成: {output_path}, 形状: {df.shape}")
            return True
            
        except Exception as e:
            logger.error(f"Excel导出失败: {e}")
            return False