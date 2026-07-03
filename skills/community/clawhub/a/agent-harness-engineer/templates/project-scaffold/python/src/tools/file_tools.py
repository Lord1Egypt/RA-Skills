#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: tools.file_tools
# 说明: 文件操作工具实现
# 修改建议: 如需扩展，添加新的工具方法并注册
# ============================================

import os
import re
from typing import Dict, Any
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


class FileTools:
    """文件操作工具"""
    
    # 工具Schema定义
    read_file_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "offset": {"type": "integer", "description": "起始行号（1-based）", "minimum": 1},
            "limit": {"type": "integer", "description": "最大读取行数", "minimum": 1, "maximum": 2000}
        },
        "required": ["path"]
    }
    
    write_file_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "content": {"type": "string", "description": "文件内容"}
        },
        "required": ["path", "content"]
    }
    
    list_files_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "目录路径"},
            "recursive": {"type": "boolean", "description": "是否递归"},
            "pattern": {"type": "string", "description": "文件匹配模式"}
        },
        "required": ["path"]
    }
    
    def read_file(self, input_data: Dict[str, Any]) -> str:
        """读取文件内容"""
        path = input_data["path"]
        offset = input_data.get("offset", 1)
        limit = input_data.get("limit", 2000)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                start = max(0, offset - 1)
                end = min(start + limit, len(lines))
                return ''.join(lines[start:end])
        except Exception as e:
            return f"Error: {str(e)}"
    
    def write_file(self, input_data: Dict[str, Any]) -> str:
        """写入文件内容"""
        path = input_data["path"]
        content = input_data["content"]
        
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def list_files(self, input_data: Dict[str, Any]) -> list:
        """列出文件"""
        path = input_data["path"]
        recursive = input_data.get("recursive", False)
        pattern = input_data.get("pattern")
        
        try:
            result = []
            if recursive:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if pattern and not re.match(pattern, f):
                            continue
                        result.append(os.path.join(root, f))
            else:
                for item in os.listdir(path):
                    if pattern and not re.match(pattern, item):
                        continue
                    result.append(item)
            return result
        except Exception as e:
            return [f"Error: {str(e)}"]
