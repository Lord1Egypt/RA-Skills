"""
AKShare 数据适配器
"""

from typing import Optional, Dict, Any

try:
    import akshare as ak
except ImportError:
    ak = None


class AkshareAdapter:
    """AKShare 适配器"""

    def __init__(self):
        """初始化适配器"""
        if ak is None:
            # akshare 未安装，创建一个占位符适配器
            print("警告: akshare 未安装，部分功能将不可用")
            print("安装命令: pip install akshare")
            self.available = False
        else:
            self.available = True

    def get_realtime_quotes(self) -> Dict:
        """获取实时行情"""
        if not self.available:
            return {}

        try:
            return ak.stock_zh_a_spot_em()
        except Exception:
            return {}

    def get_financial_report(self, symbol: str, report_type: str = '利润表') -> Optional[Dict]:
        """获取财务报表"""
        if not self.available:
            return None

        try:
            # akshare 有多个财务数据接口，这里使用简化接口
            return ak.stock_financial_analysis_indicator(symbol=symbol)
        except Exception:
            return None

    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """获取股票信息"""
        if not self.available:
            return None

        try:
            return ak.stock_individual_info_em(symbol=symbol)
        except Exception:
            return None
