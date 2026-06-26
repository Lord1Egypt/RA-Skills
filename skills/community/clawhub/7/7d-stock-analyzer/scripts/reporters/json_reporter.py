"""
JSON 报告生成器
"""

import json
from typing import Dict, Any
from datetime import datetime


class JSONReporter:
    """JSON 报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self.timestamp = datetime.now().isoformat()

    def generate(self, symbol: str, results: Dict[str, Any], full: bool = False) -> str:
        """
        生成 JSON 格式报告

        Args:
            symbol: 股票代码
            results: 分析结果字典
            full: 是否包含所有数据

        Returns:
            JSON 格式字符串
        """
        report = {
            'meta': {
                'symbol': symbol,
                'generated_at': self.timestamp,
                'analysis_type': 'full' if full else 'summary'
            },
            'results': results
        }

        return json.dumps(report, ensure_ascii=False, indent=2)
