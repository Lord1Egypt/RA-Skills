"""
Flake8 runner - 代码风格检查
"""

import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from .base import ToolRunner
from ..models import Issue, Severity, Category


class Flake8Runner(ToolRunner):
    """Flake8 工具运行器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "flake8"
        
        # 严重程度映射
        self.severity_map = {
            "E": Severity.MEDIUM,   # 错误
            "W": Severity.LOW,      # 警告
            "F": Severity.HIGH,     # 致命错误
            "C": Severity.LOW,      # 惯例
            "N": Severity.LOW,      # 命名
        }
        
        # 类别映射
        self.category_map = {
            "E501": Category.STYLE,  # 行太长
            "E401": Category.STYLE,  # 一行多导入
            "W291": Category.STYLE,  # 行尾空白
            "F401": Category.MAINTAINABILITY,  # 未使用导入
            "F821": Category.ERROR,  # 未定义名称
        }
    
    def run(self, path: str, files: Optional[List[Path]] = None) -> List[Issue]:
        """
        运行 Flake8
        
        Args:
            path: 要分析的路径
            files: 文件列表
            
        Returns:
            问题列表
        """
        if not self.is_available():
            return []
        
        cmd = [
            "flake8",
            "--format=%(path)s:%(row)d:%(col)d:%(code)s:%(text)s",
            path,
        ]
        
        # 添加配置选项
        max_line = self.config.get("max_line_length")
        if max_line:
            cmd.extend(["--max-line-length", str(max_line)])
        
        ignore = self.config.get("ignore", [])
        if ignore:
            cmd.extend(["--ignore", ",".join(ignore)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            return self._parse_output(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def _parse_output(self, output: str) -> List[Issue]:
        """
        解析 Flake8 输出
        
        Args:
            output: 工具输出
            
        Returns:
            问题列表
        """
        issues = []
        
        for line in output.strip().split("\n"):
            if not line:
                continue
            
            parts = line.split(":", 4)
            if len(parts) < 5:
                continue
            
            try:
                file_path = parts[0]
                line_num = int(parts[1])
                col_num = int(parts[2])
                code = parts[3]
                message = parts[4].strip()
                
                # 确定严重程度
                severity = self._get_severity(code)
                category = self._get_category(code)
                
                issues.append(Issue(
                    tool="flake8",
                    severity=severity,
                    category=category,
                    message=message,
                    file=file_path,
                    line=line_num,
                    column=col_num,
                    code=code,
                ))
                
            except (ValueError, IndexError):
                continue
        
        return issues
    
    def _get_severity(self, code: str) -> Severity:
        """根据代码确定严重程度"""
        prefix = code[0] if code else "E"
        return self.severity_map.get(prefix, Severity.LOW)
    
    def _get_category(self, code: str) -> Category:
        """根据代码确定类别"""
        return self.category_map.get(code, Category.STYLE)
