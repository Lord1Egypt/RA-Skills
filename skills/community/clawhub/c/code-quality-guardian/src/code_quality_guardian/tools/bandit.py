"""
Bandit runner - 安全漏洞扫描
"""

import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from .base import ToolRunner
from ..models import Issue, Severity, Category


class BanditRunner(ToolRunner):
    """Bandit 安全扫描工具运行器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "bandit"
    
    def run(self, path: str, files: Optional[List[Path]] = None) -> List[Issue]:
        """
        运行 Bandit
        
        Args:
            path: 要分析的路径
            files: 文件列表
            
        Returns:
            问题列表
        """
        if not self.is_available():
            return []
        
        cmd = [
            "bandit",
            "-f", "json",  # JSON 格式输出
            "-r",  # 递归
            path,
        ]
        
        # 配置选项
        severity = self.config.get("severity", "LOW")
        cmd.extend(["-ll", self._severity_to_level(severity)])
        
        confidence = self.config.get("confidence", "LOW")
        cmd.extend(["-ii", self._confidence_to_level(confidence)])
        
        skips = self.config.get("skips", [])
        if skips:
            cmd.extend(["-s", ",".join(skips)])
        
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
        解析 Bandit JSON 输出
        
        Args:
            output: 工具输出
            
        Returns:
            问题列表
        """
        issues = []
        
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return []
        
        for result in data.get("results", []):
            try:
                test_id = result.get("test_id", "B000")
                issue_text = result.get("issue_text", "")
                filename = result.get("filename", "")
                line_number = result.get("line_number", 0)
                line_range = result.get("line_range", [line_number])
                
                # 获取严重程度
                severity_str = result.get("issue_severity", "LOW")
                severity = self._parse_severity(severity_str)
                
                issues.append(Issue(
                    tool="bandit",
                    severity=severity,
                    category=Category.SECURITY,
                    message=issue_text,
                    file=filename,
                    line=line_number,
                    code=test_id,
                    suggestion=result.get("more_info", ""),
                ))
                
            except Exception:
                continue
        
        return issues
    
    def _parse_severity(self, severity: str) -> Severity:
        """解析严重程度"""
        mapping = {
            "CRITICAL": Severity.CRITICAL,
            "HIGH": Severity.HIGH,
            "MEDIUM": Severity.MEDIUM,
            "LOW": Severity.LOW,
        }
        return mapping.get(severity.upper(), Severity.LOW)
    
    def _severity_to_level(self, severity: str) -> str:
        """将严重程度转换为级别"""
        mapping = {
            "LOW": "1",
            "MEDIUM": "2",
            "HIGH": "3",
        }
        return mapping.get(severity.upper(), "1")
    
    def _confidence_to_level(self, confidence: str) -> str:
        """将置信度转换为级别"""
        mapping = {
            "LOW": "1",
            "MEDIUM": "2",
            "HIGH": "3",
        }
        return mapping.get(confidence.upper(), "1")
