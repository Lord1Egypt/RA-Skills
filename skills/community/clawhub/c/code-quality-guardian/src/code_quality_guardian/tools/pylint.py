"""
Pylint runner - 静态代码分析
"""

import subprocess
import json
import re
from pathlib import Path
from typing import List, Optional, Dict, Any

from .base import ToolRunner
from ..models import Issue, Severity, Category


class PylintRunner(ToolRunner):
    """Pylint 工具运行器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "pylint"
        
        # 严重程度映射
        self.severity_map = {
            "E": Severity.HIGH,     # 错误
            "W": Severity.MEDIUM,   # 警告
            "C": Severity.LOW,      # 惯例
            "R": Severity.INFO,     # 重构建议
            "I": Severity.INFO,     # 信息
        }
        
        # 类别映射
        self.category_map = {
            "R0902": Category.COMPLEXITY,  # 太多实例属性
            "R0903": Category.MAINTAINABILITY,  # 太少公共方法
            "R0911": Category.COMPLEXITY,  # 太多返回语句
            "R0912": Category.COMPLEXITY,  # 太多分支
            "R0913": Category.COMPLEXITY,  # 太多参数
            "R0914": Category.COMPLEXITY,  # 太多局部变量
            "R0915": Category.COMPLEXITY,  # 太多语句
            "C0103": Category.STYLE,       # 无效名称
            "C0301": Category.STYLE,       # 行太长
            "W0611": Category.MAINTAINABILITY,  # 未使用导入
            "W0613": Category.MAINTAINABILITY,  # 未使用参数
        }
    
    def run(self, path: str, files: Optional[List[Path]] = None) -> List[Issue]:
        """
        运行 Pylint
        
        Args:
            path: 要分析的路径
            files: 文件列表
            
        Returns:
            问题列表
        """
        if not self.is_available():
            return []
        
        cmd = [
            "pylint",
            "--output-format=text",
            "--msg-template={path}:{line}:{column}:{msg_id}:{msg}",
            "--score=n",  # 不显示分数
            path,
        ]
        
        # 添加配置
        disable = self.config.get("disable", [])
        if disable:
            cmd.extend(["--disable", ",".join(disable)])
        
        enable = self.config.get("enable", [])
        if enable:
            cmd.extend(["--enable", ",".join(enable)])
        
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
        解析 Pylint 输出
        
        Args:
            output: 工具输出
            
        Returns:
            问题列表
        """
        issues = []
        
        # 匹配格式: path:line:column:code:message
        pattern = r'^(.*?):(\d+):(\d+):([A-Z]\d{4}):(.*)$'
        
        for line in output.strip().split("\n"):
            if not line:
                continue
            
            match = re.match(pattern, line)
            if not match:
                continue
            
            try:
                file_path = match.group(1)
                line_num = int(match.group(2))
                col_num = int(match.group(3))
                code = match.group(4)
                message = match.group(5).strip()
                
                severity = self._get_severity(code)
                category = self._get_category(code)
                
                issues.append(Issue(
                    tool="pylint",
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
        prefix = code[0] if code else "C"
        return self.severity_map.get(prefix, Severity.LOW)
    
    def _get_category(self, code: str) -> Category:
        """根据代码确定类别"""
        return self.category_map.get(code, Category.MAINTAINABILITY)
