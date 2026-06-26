"""
Quality Analyzer - 代码质量分析器
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import Config
from .models import AnalysisResult, Issue, FileMetrics
from .tools.base import ToolRunner
from .tools.flake8 import Flake8Runner
from .tools.pylint import PylintRunner
from .tools.bandit import BanditRunner
from .tools.radon import RadonRunner


class QualityAnalyzer:
    """代码质量分析器主类"""
    
    # 工具映射
    TOOL_RUNNERS = {
        "flake8": Flake8Runner,
        "pylint": PylintRunner,
        "bandit": BanditRunner,
        "radon": RadonRunner,
    }
    
    def __init__(
        self,
        config: Optional[Config] = None,
        language: Optional[str] = None,
        tools: Optional[List[str]] = None,
    ):
        """
        初始化分析器
        
        Args:
            config: 配置对象
            language: 目标语言 (如果未提供 config)
            tools: 工具列表 (如果未提供 config)
        """
        if config:
            self.config = config
        else:
            self.config = Config(
                language=language or "python",
                tools=tools,
            )
    
    def analyze(self, path: str) -> AnalysisResult:
        """
        分析指定路径的代码
        
        Args:
            path: 要分析的目录或文件路径
            
        Returns:
            AnalysisResult: 分析结果
        """
        start_time = time.time()
        
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        
        # 收集文件
        files = self._collect_files(path)
        
        # 初始化结果
        result = AnalysisResult(
            files_analyzed=len(files),
            thresholds=self.config.thresholds,
        )
        
        # 运行各工具
        all_issues = []
        complexity_scores = []
        
        for tool_name in self.config.tools:
            if tool_name not in self.TOOL_RUNNERS:
                continue
            
            runner_class = self.TOOL_RUNNERS[tool_name]
            runner = runner_class(self.config.get_tool_config(tool_name))
            
            try:
                tool_result = runner.run(str(path), files)
                
                if isinstance(tool_result, list):
                    # 返回的是问题列表
                    all_issues.extend(tool_result)
                elif isinstance(tool_result, dict):
                    # 返回的是指标
                    complexity_scores.append(tool_result.get("average_complexity", 0))
                    
            except Exception as e:
                # 记录工具执行错误但不中断
                print(f"警告: 工具 {tool_name} 执行失败: {e}")
        
        # 计算代码行数
        total_lines = sum(self._count_lines(f) for f in files)
        result.lines_of_code = total_lines
        
        # 处理问题
        result.issues = all_issues
        result.total_issues = len(all_issues)
        
        for issue in all_issues:
            result.issues_by_severity[issue.severity] += 1
            result.issues_by_category[issue.category] += 1
        
        # 计算复杂度分数
        if complexity_scores:
            result.complexity_score = sum(complexity_scores) / len(complexity_scores)
        
        # 计算安全分数
        security_issues = len(result.security_issues)
        if total_lines > 0:
            result.security_score = max(0, 100 - (security_issues / total_lines * 1000))
        
        # 计算可维护性等级
        result.maintainability_rank = self._calculate_maintainability(result)
        
        # 计算执行时间
        result.duration_ms = int((time.time() - start_time) * 1000)
        
        return result
    
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """
        分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            AnalysisResult: 分析结果
        """
        return self.analyze(file_path)
    
    def _collect_files(self, path: Path) -> List[Path]:
        """
        收集要分析的文件
        
        Args:
            path: 路径
            
        Returns:
            文件列表
        """
        files = []
        
        # 文件扩展名映射
        extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "go": [".go"],
        }
        
        exts = extensions.get(self.config.language, [".py"])
        
        if path.is_file():
            if path.suffix in exts:
                files.append(path)
        else:
            for ext in exts:
                files.extend(path.rglob(f"*{ext}"))
        
        # 应用忽略模式
        filtered = []
        for f in files:
            str_path = str(f)
            should_ignore = any(
                pattern.replace("*", "") in str_path or str_path.endswith(pattern.replace("*", ""))
                for pattern in self.config.ignore_patterns
            )
            if not should_ignore:
                filtered.append(f)
        
        return filtered
    
    def _count_lines(self, file_path: Path) -> int:
        """
        计算文件行数
        
        Args:
            file_path: 文件路径
            
        Returns:
            行数
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return len(f.readlines())
        except:
            return 0
    
    def _calculate_maintainability(self, result: AnalysisResult) -> str:
        """
        计算可维护性等级
        
        Args:
            result: 分析结果
            
        Returns:
            等级 (A-F)
        """
        score = result.quality_score
        
        if score >= 8.5:
            return "A"
        elif score >= 7.5:
            return "B"
        elif score >= 6.5:
            return "C"
        elif score >= 5.5:
            return "D"
        else:
            return "F"
