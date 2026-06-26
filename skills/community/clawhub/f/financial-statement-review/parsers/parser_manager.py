"""
文件解析器管理器

统一管理所有文件解析器，提供统一的文件解析接口
"""
import os
from typing import Dict, List, Type, Any, Optional, Union
from pathlib import Path

from .base_parser import BaseParser, ParseResult, FinancialData
from .file_identifier import FileIdentifier, FileType, SoftwareType


class FileParserManager:
    """
    文件解析器管理器
    
    负责管理所有解析器，提供统一的文件解析接口
    """
    
    def __init__(self):
        """初始化解析器管理器"""
        self.parsers: Dict[str, BaseParser] = {}
        self.parser_classes: Dict[str, Type[BaseParser]] = {}
        
        # 注册内置解析器
        self._register_builtin_parsers()
    
    def _register_builtin_parsers(self):
        """注册内置解析器"""
        # 延迟导入，避免循环依赖
        from .excel_parser import ExcelParser, XLSParser
        from .csv_parser import CSVParser
        from .word_parser import WordParser
        from .pdf_parser import PDFParser
        from .kingdee_parser import KingdeeParser
        from .ufida_parser import UfidaParser
        
        parsers = [
            ExcelParser,
            XLSParser,
            CSVParser,
            WordParser,
            PDFParser,
            KingdeeParser,
            UfidaParser,
        ]
        
        for parser_class in parsers:
            self.register_parser(parser_class)
    
    def register_parser(self, parser_class: Type[BaseParser], config: Dict = None):
        """
        注册解析器
        
        Args:
            parser_class: 解析器类
            config: 解析器配置
        """
        if not issubclass(parser_class, BaseParser):
            raise ValueError(f"解析器类必须继承自 BaseParser: {parser_class}")
        
        parser_name = parser_class.name
        self.parser_classes[parser_name] = parser_class
        self.parsers[parser_name] = parser_class(config)
    
    def unregister_parser(self, parser_name: str):
        """
        注销解析器
        
        Args:
            parser_name: 解析器名称
        """
        if parser_name in self.parsers:
            del self.parsers[parser_name]
        if parser_name in self.parser_classes:
            del self.parser_classes[parser_name]
    
    def get_parser(self, parser_name: str) -> Optional[BaseParser]:
        """
        获取解析器实例
        
        Args:
            parser_name: 解析器名称
            
        Returns:
            解析器实例或 None
        """
        return self.parsers.get(parser_name)
    
    def list_parsers(self) -> List[Dict[str, Any]]:
        """
        列出所有可用解析器
        
        Returns:
            解析器信息列表
        """
        result = []
        for name, parser in self.parsers.items():
            result.append({
                'name': name,
                'description': parser.description,
                'supported_extensions': parser.supported_extensions,
                'supported_software': parser.supported_software,
            })
        return result
    
    def identify_file(self, file_path: str) -> Dict[str, Any]:
        """
        识别文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息
        """
        return FileIdentifier.get_file_info(file_path)
    
    def find_suitable_parser(self, file_path: str) -> Optional[BaseParser]:
        """
        查找适合解析该文件的解析器
        
        Args:
            file_path: 文件路径
            
        Returns:
            最适合的解析器实例
        """
        # 首先识别文件类型和软件类型
        file_type, software_type = FileIdentifier.identify_file(file_path)
        
        suitable_parsers = []
        
        for parser in self.parsers.values():
            # 检查是否能解析
            if parser.can_parse(file_path):
                # 检查是否为专用软件解析器
                if software_type.name in parser.supported_software:
                    # 专用解析器优先级更高
                    suitable_parsers.insert(0, parser)
                else:
                    suitable_parsers.append(parser)
        
        return suitable_parsers[0] if suitable_parsers else None
    
    def parse_file(self, file_path: str, parser_name: str = None) -> ParseResult:
        """
        解析文件
        
        Args:
            file_path: 文件路径
            parser_name: 指定解析器名称（可选）
            
        Returns:
            ParseResult: 解析结果
        """
        # 验证文件存在
        if not os.path.exists(file_path):
            return ParseResult(
                success=False,
                file_path=file_path,
                errors=['文件不存在']
            )
        
        if not os.path.isfile(file_path):
            return ParseResult(
                success=False,
                file_path=file_path,
                errors=['路径不是文件']
            )
        
        # 如果指定了解析器，使用指定解析器
        if parser_name:
            parser = self.get_parser(parser_name)
            if parser is None:
                return ParseResult(
                    success=False,
                    file_path=file_path,
                    errors=[f'未找到解析器: {parser_name}']
                )
            return parser.parse(file_path)
        
        # 自动选择最合适的解析器
        parser = self.find_suitable_parser(file_path)
        
        if parser is None:
            return ParseResult(
                success=False,
                file_path=file_path,
                errors=['未找到适合该文件的解析器']
            )
        
        return parser.parse(file_path)
    
    def parse_files(self, file_paths: List[str], 
                    parser_name: str = None) -> List[ParseResult]:
        """
        批量解析多个文件
        
        Args:
            file_paths: 文件路径列表
            parser_name: 指定解析器名称（可选）
            
        Returns:
            ParseResult 列表
        """
        results = []
        for file_path in file_paths:
            result = self.parse_file(file_path, parser_name)
            results.append(result)
        return results
    
    def scan_and_parse(self, directory: str, 
                       recursive: bool = True,
                       extensions: List[str] = None) -> List[ParseResult]:
        """
        扫描目录并解析所有支持的文件
        
        Args:
            directory: 目录路径
            recursive: 是否递归扫描
            extensions: 指定文件扩展名（可选）
            
        Returns:
            ParseResult 列表
        """
        results = []
        
        path = Path(directory)
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in path.glob(pattern):
            if not file_path.is_file():
                continue
            
            # 检查扩展名
            if extensions:
                ext = file_path.suffix.lower()
                if ext not in extensions:
                    continue
            else:
                # 只处理支持的文件类型
                file_type = FileIdentifier.identify_file_type(str(file_path))
                if file_type == FileType.UNKNOWN:
                    continue
            
            result = self.parse_file(str(file_path))
            results.append(result)
        
        return results
    
    def merge_financial_data(self, results: List[ParseResult]) -> FinancialData:
        """
        合并多个解析结果的财务数据
        
        Args:
            results: 解析结果列表
            
        Returns:
            合并后的财务数据
        """
        merged = FinancialData()
        
        for result in results:
            if not result.success or not result.data:
                continue
            
            data = result.data
            
            # 合并基本信息
            if data.company_name and not merged.company_name:
                merged.company_name = data.company_name
            if data.tax_id and not merged.tax_id:
                merged.tax_id = data.tax_id
            if data.report_period and not merged.report_period:
                merged.report_period = data.report_period
            
            # 合并报表数据（优先保留非空值）
            for key, value in data.balance_sheet.items():
                if key not in merged.balance_sheet:
                    merged.balance_sheet[key] = value
            
            for key, value in data.income_statement.items():
                if key not in merged.income_statement:
                    merged.income_statement[key] = value
            
            for key, value in data.cash_flow.items():
                if key not in merged.cash_flow:
                    merged.cash_flow[key] = value
            
            # 合并原始数据
            merged.raw_data.update(data.raw_data)
        
        return merged
    
    def get_parsing_summary(self, results: List[ParseResult]) -> Dict[str, Any]:
        """
        获取批量解析的摘要信息
        
        Args:
            results: 解析结果列表
            
        Returns:
            摘要信息
        """
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        
        file_types = {}
        software_types = {}
        
        for result in results:
            # 统计文件类型
            file_type = result.file_type or 'UNKNOWN'
            file_types[file_type] = file_types.get(file_type, 0) + 1
            
            # 统计软件类型
            software_type = result.software_type or 'UNKNOWN'
            software_types[software_type] = software_types.get(software_type, 0) + 1
        
        return {
            'total_files': total,
            'successful': successful,
            'failed': failed,
            'success_rate': f"{(successful/total*100):.1f}%" if total > 0 else "N/A",
            'file_types': file_types,
            'software_types': software_types,
        }


# 全局解析器管理器实例
_default_manager = None


def get_parser_manager() -> FileParserManager:
    """获取默认解析器管理器实例"""
    global _default_manager
    if _default_manager is None:
        _default_manager = FileParserManager()
    return _default_manager


# 便捷函数
def parse_file(file_path: str, parser_name: str = None) -> ParseResult:
    """
    解析文件（便捷函数）
    
    Args:
        file_path: 文件路径
        parser_name: 指定解析器名称（可选）
        
    Returns:
        ParseResult: 解析结果
    """
    manager = get_parser_manager()
    return manager.parse_file(file_path, parser_name)


def parse_files(file_paths: List[str], parser_name: str = None) -> List[ParseResult]:
    """
    批量解析文件（便捷函数）
    
    Args:
        file_paths: 文件路径列表
        parser_name: 指定解析器名称（可选）
        
    Returns:
        ParseResult 列表
    """
    manager = get_parser_manager()
    return manager.parse_files(file_paths, parser_name)


__all__ = [
    'FileParserManager',
    'get_parser_manager',
    'parse_file',
    'parse_files',
]
