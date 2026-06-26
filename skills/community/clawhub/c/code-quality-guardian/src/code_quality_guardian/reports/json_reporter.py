"""
JSON reporter - JSON格式报告
"""

import json
from typing import Optional
from pathlib import Path

from .base import Reporter
from ..models import AnalysisResult


class JsonReporter(Reporter):
    """JSON 报告生成器"""
    
    def render(self, result: AnalysisResult, output_path: Optional[str] = None) -> str:
        """
        渲染 JSON 报告
        
        Args:
            result: 分析结果
            output_path: 输出文件路径
            
        Returns:
            JSON 字符串
        """
        data = result.to_dict()
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            Path(output_path).write_text(json_str, encoding="utf-8")
        
        return json_str
