#!/usr/bin/env python3
"""错误处理增强模块 - v2.7.5 完善异常体系"""

import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class DocProcessorError(Exception):
    """基础异常类"""
    def __init__(self, message: str, suggestion: str = None, details: Dict = None):
        super().__init__(message)
        self.message = message
        self.suggestion = suggestion
        self.details = details or {}
    
    def __str__(self):
        result = self.message
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            result += f" ({details_str})"
        if self.suggestion:
            result += f"\n建议：{self.suggestion}"
        return result
    
    def to_dict(self) -> Dict:
        return {'message': self.message, 'suggestion': self.suggestion, 'details': self.details}


class FileFormatError(DocProcessorError):
    """不支持的文件格式"""
    def __init__(self, format: str, supported: List[str] = None):
        supported_list = supported or ['.docx', '.xlsx', '.pdf', '.csv', '.txt', '.md']
        super().__init__(
            f"不支持的格式：{format}",
            f"支持的格式：{', '.join(supported_list)}",
            {'format': format}
        )


class ReadError(DocProcessorError):
    """读取失败"""
    def __init__(self, path: str, reason: str = None):
        msg = f"读取失败：{path}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, "检查文件权限和格式是否正确", {'path': path})


class WriteError(DocProcessorError):
    """写入失败"""
    def __init__(self, path: str, reason: str = None):
        msg = f"写入失败：{path}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, "检查目标目录是否有写入权限", {'path': path})


class ConvertError(DocProcessorError):
    """转换失败"""
    def __init__(self, src: str, dst: str, reason: str = None):
        msg = f"转换失败：{src} → {dst}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, "检查源文件格式和目标格式是否兼容", {'source': src, 'target': dst})


class TemplateError(DocProcessorError):
    """模板错误"""
    def __init__(self, template: str, reason: str = None):
        msg = f"模板错误：{template}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg, "检查模板文件是否完整", {'template': template})


class BatchError(DocProcessorError):
    """批量处理错误"""
    def __init__(self, failed: List[str], total: int):
        failed_preview = ', '.join(failed[:5]) + ('...' if len(failed) > 5 else '')
        super().__init__(
            f"批量处理失败：{len(failed)}/{total}",
            f"失败文件：{failed_preview}",
            {'failed_count': len(failed), 'total': total, 'failed_files': failed[:10]}
        )


class DependencyError(DocProcessorError):
    """依赖缺失"""
    def __init__(self, message: str):
        super().__init__(message, "运行 setup.sh 安装缺失的依赖")


# ========== 便捷工厂函数 ==========

def file_not_found(path: str, suggestion: str = None) -> DocProcessorError:
    return DocProcessorError(f"文件不存在：{path}", suggestion=suggestion or "检查文件路径是否正确", details={'path': path})

def dependency_missing(name: str, install_cmd: str = None) -> DocProcessorError:
    suggestion = install_cmd or f"请安装依赖：pip install {name}"
    return DocProcessorError(f"依赖缺失：{name}", suggestion=suggestion, details={'dependency': name})

def format_error(format: str, supported: List[str] = None) -> FileFormatError:
    return FileFormatError(format, supported)

def read_error(path: str, reason: str = None) -> ReadError:
    return ReadError(path, reason)

def write_error(path: str, reason: str = None) -> WriteError:
    return WriteError(path, reason)

def convert_error(src: str, dst: str, reason: str = None) -> ConvertError:
    return ConvertError(src, dst, reason)

def template_error(template: str, reason: str = None) -> TemplateError:
    return TemplateError(template, reason)

def batch_error(failed: List[str], total: int) -> BatchError:
    return BatchError(failed, total)
