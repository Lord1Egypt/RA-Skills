"""
Radon runner - 代码复杂度分析
"""

import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from .base import ToolRunner
from ..models import Issue, Severity, Category


class RadonRunner(ToolRunner):
    """Radon 复杂度分析工具运行器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "radon"
    
    def run(self, path: str, files: Optional[List[Path]] = None) -> Dict[str, Any]:
        """
        运行 Radon
        
        Args:
            path: 要分析的路径
            files: 文件列表
            
        Returns:
            复杂度指标字典
        """
        if not self.is_available():
            return {"average_complexity": 0, "max_complexity": 0}
        
        # 分析圈复杂度
        cc_result = self._run_cc(path)
        
        # 分析可维护性指数
        mi_result = self._run_mi(path)
        
        return {
            "average_complexity": cc_result.get("average", 0),
            "max_complexity": cc_result.get("max", 0),
            "complexity_issues": cc_result.get("issues", []),
            "maintainability_index": mi_result.get("average", 0),
        }
    
    def _run_cc(self, path: str) -> Dict[str, Any]:
        """运行圈复杂度分析"""
        cmd = [
            "radon",
            "cc",
            "-j",  # JSON 输出
            "-a",  # 平均复杂度
            path,
        ]
        
        # 设置最小等级
        min_rank = self.config.get("cc_min", "C")
        cmd.extend(["-nc", min_rank])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            return self._parse_cc_output(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {"average": 0, "max": 0, "issues": []}
    
    def _run_mi(self, path: str) -> Dict[str, Any]:
        """运行可维护性指数分析"""
        cmd = [
            "radon",
            "mi",
            "-j",  # JSON 输出
            path,
        ]
        
        # 设置最小等级
        min_rank = self.config.get("mi_min", "C")
        cmd.extend(["-nc", min_rank])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            return self._parse_mi_output(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {"average": 0}
    
    def _parse_cc_output(self, output: str) -> Dict[str, Any]:
        """解析圈复杂度输出"""
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return {"average": 0, "max": 0, "issues": []}
        
        total_complexity = 0
        count = 0
        max_complexity = 0
        issues = []
        
        threshold = self.config.get("thresholds", {}).get("max_complexity", 10)
        
        for file_path, blocks in data.items():
            for block in blocks:
                complexity = block.get("complexity", 0)
                total_complexity += complexity
                count += 1
                max_complexity = max(max_complexity, complexity)
                
                # 如果超过阈值，创建问题
                if complexity > threshold:
                    issues.append(Issue(
                        tool="radon",
                        severity=Severity.MEDIUM,
                        category=Category.COMPLEXITY,
                        message=f"复杂度过高: {complexity} (阈值: {threshold})",
                        file=file_path,
                        line=block.get("lineno", 0),
                        code=f"CC{complexity}",
                    ))
        
        average = total_complexity / count if count > 0 else 0
        
        return {
            "average": round(average, 2),
            "max": max_complexity,
            "issues": issues,
        }
    
    def _parse_mi_output(self, output: str) -> Dict[str, Any]:
        """解析可维护性指数输出"""
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return {"average": 0}
        
        total_mi = 0
        count = 0
        
        for file_path, mi_data in data.items():
            if isinstance(mi_data, dict):
                mi = mi_data.get("mi", 0)
            else:
                mi = mi_data
            
            total_mi += mi
            count += 1
        
        average = total_mi / count if count > 0 else 0
        
        return {"average": round(average, 2)}
