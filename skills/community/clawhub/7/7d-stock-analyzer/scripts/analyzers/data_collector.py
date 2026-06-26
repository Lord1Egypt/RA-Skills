"""
数据收集与分析
"""

import pandas as pd
from typing import Dict, Any
from .base import BaseAnalyzer


class DataCollector(BaseAnalyzer):
    """数据收集器"""

    @property
    def name(self) -> str:
        return "数据收集与验证"

    @property
    def dimensions(self) -> list:
        return ['realtime_quotes', 'basic_info', 'financial']

    def analyze(self, symbol: str) -> Dict[str, Any]:
        """
        收集股票数据

        Args:
            symbol: 股票代码

        Returns:
            数据收集结果
        """
        self.log(f"开始收集数据: {symbol}")

        result = {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now().isoformat(),
            'data': {},
            'errors': []
        }

        # 1. 实时行情
        try:
            self.log("获取实时行情...")
            quotes = self.get_data('efinance', 'get_realtime_quotes')
            symbol_quotes = quotes[quotes['股票代码'] == symbol]

            if not symbol_quotes.empty:
                result['data']['realtime'] = symbol_quotes.iloc[0].to_dict()
                self.log(f"  ✓ 获取实时行情成功")
            else:
                result['errors'].append(f"未找到股票 {symbol} 的实时行情")
        except Exception as e:
            result['errors'].append(f"获取实时行情失败: {e}")

        # 2. 基础信息
        try:
            self.log("获取基础信息...")
            info = self.get_data('efinance', 'get_base_info', symbol=symbol)
            if info:
                result['data']['basic_info'] = info
                self.log(f"  ✓ 获取基础信息成功")
        except Exception as e:
            result['errors'].append(f"获取基础信息失败: {e}")

        # 3. 财务数据
        try:
            self.log("获取财务数据...")
            financial = self.get_data('efinance', 'get_financial_data', symbol=symbol)
            if financial:
                result['data']['financial'] = financial
                self.log(f"  ✓ 获取财务数据成功")
        except Exception as e:
            result['errors'].append(f"获取财务数据失败: {e}")

        self.data['data_collector'] = result['data']
        return result
