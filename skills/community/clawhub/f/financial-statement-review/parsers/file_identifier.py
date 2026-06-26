"""
文件识别器模块

识别文件类型和财务软件来源
"""
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import os
import struct


class FileType(Enum):
    """文件类型枚举"""
    UNKNOWN = auto()
    EXCEL = auto()           # .xlsx, .xls
    WORD = auto()            # .docx
    PDF = auto()             # .pdf
    CSV = auto()             # .csv
    TXT = auto()             # .txt
    XML = auto()             # .xml
    JSON = auto()            # .json
    ZIP = auto()             # .zip (可能是压缩的财务数据)


class SoftwareType(Enum):
    """财务软件类型枚举"""
    UNKNOWN = auto()
    GENERIC = auto()         # 通用格式
    # 国内主流财务软件
    KINGDEE = auto()         # 金蝶
    UFIDA = auto()           # 用友
    SAP = auto()             # SAP
    ORACLE = auto()          # Oracle
    INSPUR = auto()          # 浪潮
    # 其他
    CUSTOM = auto()          # 自定义格式


class FileIdentifier:
    """文件识别器"""
    
    # 文件扩展名到类型的映射
    EXTENSION_MAP = {
        '.xlsx': FileType.EXCEL,
        '.xls': FileType.EXCEL,
        '.xlsm': FileType.EXCEL,
        '.docx': FileType.WORD,
        '.doc': FileType.WORD,
        '.pdf': FileType.PDF,
        '.csv': FileType.CSV,
        '.txt': FileType.TXT,
        '.xml': FileType.XML,
        '.json': FileType.JSON,
        '.zip': FileType.ZIP,
    }
    
    # 财务软件特征标识
    SOFTWARE_SIGNATURES = {
        # 金蝶特征
        'KINGDEE': {
            'file_markers': ['金蝶', 'Kingdee', 'KIS', 'K3', 'EAS', '云星空'],
            'sheet_names': ['资产负债表', '利润表', '现金流量表', '科目余额表'],
            'file_patterns': ['*.xlsx', '*.xls', '*.xml'],
        },
        # 用友特征
        'UFIDA': {
            'file_markers': ['用友', 'UFIDA', 'U8', 'NC', 'YonSuite', '畅捷通'],
            'sheet_names': ['资产负债表', '利润表', '现金流量表', 'GL_accvouch'],
            'file_patterns': ['*.xlsx', '*.xls', '*.csv'],
        },
        # SAP特征
        'SAP': {
            'file_markers': ['SAP'],
            'sheet_names': ['Balance Sheet', 'Income Statement', 'Cash Flow'],
            'file_patterns': ['*.xlsx', '*.xls'],
        },
        # 浪潮特征
        'INSPUR': {
            'file_markers': ['浪潮', 'Inspur', 'GS'],
            'sheet_names': ['资产负债表', '利润表'],
            'file_patterns': ['*.xlsx', '*.xls'],
        },
    }
    
    @classmethod
    def identify_file_type(cls, file_path: str) -> FileType:
        """
        识别文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            FileType: 文件类型
        """
        ext = Path(file_path).suffix.lower()
        return cls.EXTENSION_MAP.get(ext, FileType.UNKNOWN)
    
    @classmethod
    def identify_software_type(cls, file_path: str, 
                                preview_content: str = None) -> SoftwareType:
        """
        识别财务软件类型
        
        Args:
            file_path: 文件路径
            preview_content: 文件内容预览（用于更精确识别）
            
        Returns:
            SoftwareType: 软件类型
        """
        file_name = Path(file_path).name.lower()
        
        # 根据文件名特征识别
        for software, signatures in cls.SOFTWARE_SIGNATURES.items():
            markers = [m.lower() for m in signatures['file_markers']]
            
            # 检查文件名中是否包含软件标识
            for marker in markers:
                if marker in file_name:
                    return getattr(SoftwareType, software, SoftwareType.UNKNOWN)
        
        # 根据文件类型判断
        file_type = cls.identify_file_type(file_path)
        
        if file_type == FileType.UNKNOWN:
            return SoftwareType.UNKNOWN
        elif file_type in [FileType.EXCEL, FileType.CSV]:
            # 可能是通用Excel格式
            return SoftwareType.GENERIC
        elif file_type in [FileType.WORD, FileType.PDF]:
            return SoftwareType.GENERIC
        
        return SoftwareType.UNKNOWN
    
    @classmethod
    def get_file_info(cls, file_path: str) -> Dict:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 文件信息
        """
        if not os.path.exists(file_path):
            return {'error': '文件不存在'}
        
        stat = os.stat(file_path)
        file_type = cls.identify_file_type(file_path)
        software_type = cls.identify_software_type(file_path)
        
        return {
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'file_extension': Path(file_path).suffix.lower(),
            'file_size': stat.st_size,
            'file_size_human': cls._format_file_size(stat.st_size),
            'file_type': file_type.name,
            'software_type': software_type.name,
            'modified_time': stat.st_mtime,
        }
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    @classmethod
    def is_excel_file(cls, file_path: str) -> bool:
        """检查是否为Excel文件"""
        return cls.identify_file_type(file_path) == FileType.EXCEL
    
    @classmethod
    def is_pdf_file(cls, file_path: str) -> bool:
        """检查是否为PDF文件"""
        return cls.identify_file_type(file_path) == FileType.PDF
    
    @classmethod
    def is_word_file(cls, file_path: str) -> bool:
        """检查是否为Word文件"""
        return cls.identify_file_type(file_path) == FileType.WORD
    
    @classmethod
    def is_csv_file(cls, file_path: str) -> bool:
        """检查是否为CSV文件"""
        return cls.identify_file_type(file_path) == FileType.CSV
    
    @classmethod
    def scan_directory(cls, directory: str, 
                       recursive: bool = True) -> List[Dict]:
        """
        扫描目录中的财务文件
        
        Args:
            directory: 目录路径
            recursive: 是否递归扫描
            
        Returns:
            List[Dict]: 文件信息列表
        """
        results = []
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        path = Path(directory)
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                file_type = cls.identify_file_type(str(file_path))
                if file_type != FileType.UNKNOWN:
                    info = cls.get_file_info(str(file_path))
                    results.append(info)
        
        return results


# 快捷函数
def identify_file(file_path: str) -> Tuple[FileType, SoftwareType]:
    """
    识别文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        Tuple[FileType, SoftwareType]: (文件类型, 软件类型)
    """
    identifier = FileIdentifier()
    file_type = identifier.identify_file_type(file_path)
    software_type = identifier.identify_software_type(file_path)
    return file_type, software_type


__all__ = [
    'FileType',
    'SoftwareType',
    'FileIdentifier',
    'identify_file',
]
