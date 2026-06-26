"""
AKShare 财务数据获取模块
用于获取真实财务数据，替代估算值

依赖: akshare (可选安装)
使用: python3 scripts/analyze_stock.py 600919 --akshare

版本: 1.2.5
"""
import pandas as pd
from typing import Dict, Optional, List
import warnings

# 忽略一些常见警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class FinancialDataFetcherAKShare:
    """
    AKShare财务数据获取器
    
    说明:
        - 数据来源: 东方财富、同花顺等
        - 数据类型: 真实财报数据
        - 稳定性: 中等（接口可能变更）
        - 成本: 免费
    
    使用示例:
        fetcher = FinancialDataFetcherAKShare()
        data = fetcher.get_financial_indicator("600919")
        print(f"ROE: {data['roe']}%")
    """

    def __init__(self):
        self.source_name = "AKShare"
        self._ak = None  # 延迟导入

    def _ensure_akshare(self):
        """确保akshare已导入"""
        if self._ak is None:
            try:
                import akshare as ak
                self._ak = ak
            except ImportError:
                raise ImportError(
                    "AKShare未安装。请运行: pip install akshare\n"
                    "或使用基础模式（估算值）: python3 analyze_stock.py 600919"
                )

    def get_financial_indicator(self, stock_code: str) -> Dict:
        """
        获取主要财务指标（真实财报数据）

        Args:
            stock_code: 股票代码（如 "600919"）

        Returns:
            财务指标字典，包含：
            - roe: 净资产收益率
            - roa: 总资产收益率
            - gross_margin: 毛利率
            - net_margin: 净利率
            - revenue_growth: 营收增速
            - profit_growth: 利润增速
            - debt_ratio: 资产负债率
            - current_ratio: 流动比率
            - source: 数据来源
            - is_estimated: 是否估算
        """
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_financial_analysis_indicator(symbol=stock_code)

            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的财务数据")

            # 取最新一期数据
            latest = df.iloc[0]

            return {
                "roe": self._safe_float(latest.get('roe')),
                "roa": self._safe_float(latest.get('roa')),
                "gross_margin": self._safe_float(latest.get('grossprofitmargin')),
                "net_margin": self._safe_float(latest.get('netprofitmargin')),
                "revenue_growth": self._safe_float(latest.get('revenue_growth')),
                "profit_growth": self._safe_float(latest.get('net_profit_growth')),
                "debt_ratio": self._safe_float(latest.get('debt_to_asset')),
                "current_ratio": self._safe_float(latest.get('current_ratio')),
                "ocf_ratio": self._safe_float(latest.get('ocf_to_revenue')),
                "source": self.source_name,
                "is_estimated": False,
                "report_date": str(latest.get('report_date', '')),
            }
        except Exception as e:
            raise RuntimeError(f"AKShare获取财务指标失败: {e}")

    def get_balance_sheet(self, stock_code: str) -> Dict:
        """获取资产负债表"""
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_balance_sheet_by_report_em(symbol=stock_code)
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的资产负债表")

            latest = df.iloc[0]

            return {
                "total_assets": self._safe_float(latest.get('资产总计')),
                "total_liabilities": self._safe_float(latest.get('负债合计')),
                "net_assets": self._safe_float(latest.get('所有者权益合计')),
                "cash": self._safe_float(latest.get('货币资金')),
                "accounts_receivable": self._safe_float(latest.get('应收账款')),
                "inventory": self._safe_float(latest.get('存货')),
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            raise RuntimeError(f"AKShare获取资产负债表失败: {e}")

    def get_income_statement(self, stock_code: str) -> Dict:
        """获取利润表"""
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_profit_sheet_by_report_em(symbol=stock_code)
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的利润表")

            latest = df.iloc[0]

            return {
                "revenue": self._safe_float(latest.get('营业收入')),
                "cost": self._safe_float(latest.get('营业成本')),
                "gross_profit": self._safe_float(latest.get('毛利润')),
                "net_profit": self._safe_float(latest.get('净利润')),
                "op_profit": self._safe_float(latest.get('营业利润')),
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            raise RuntimeError(f"AKShare获取利润表失败: {e}")

    def get_cash_flow(self, stock_code: str) -> Dict:
        """获取现金流量表"""
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_cash_flow_sheet_by_report_em(symbol=stock_code)
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的现金流量表")

            latest = df.iloc[0]

            return {
                "ocf": self._safe_float(latest.get('经营活动产生的现金流量净额')),
                "icf": self._safe_float(latest.get('投资活动产生的现金流量净额')),
                "fcf": self._safe_float(latest.get('筹资活动产生的现金流量净额')),
                "free_cash_flow": self._safe_float(latest.get('现金流量净额')),
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            raise RuntimeError(f"AKShare获取现金流量表失败: {e}")

    def get_historical_financial(self, stock_code: str, years: int = 5) -> pd.DataFrame:
        """
        获取历史财务数据（多年趋势）

        Args:
            stock_code: 股票代码
            years: 年数（默认5年）

        Returns:
            历史财务数据DataFrame
        """
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_financial_analysis_indicator(symbol=stock_code)
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的历史财务数据")

            # 取最近N年数据
            df = df.head(years)
            return df
        except Exception as e:
            raise RuntimeError(f"AKShare获取历史财务数据失败: {e}")

    def get_valuation(self, stock_code: str) -> Dict:
        """获取估值指标"""
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_a_lg_indicator(symbol=stock_code)
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的估值数据")

            # 取最新数据
            latest = df.iloc[-1] if len(df) > 0 else df

            return {
                "pe_ttm": self._safe_float(latest.get('pe_ttm')),
                "pe_static": self._safe_float(latest.get('pe')),
                "pb": self._safe_float(latest.get('pb')),
                "ps_ttm": self._safe_float(latest.get('ps_ttm')),
                "dv_ratio": self._safe_float(latest.get('dv_ratio')),
                "dv_ttm": self._safe_float(latest.get('dv_ttm')),
                "total_mv": self._safe_float(latest.get('total_mv')),
                "circ_mv": self._safe_float(latest.get('circ_mv')),
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            raise RuntimeError(f"AKShare获取估值指标失败: {e}")

    def get_fund_flow(self, stock_code: str) -> Dict:
        """获取资金流向"""
        self._ensure_akshare()
        
        try:
            df = self._ak.stock_individual_fund_flow(stock=stock_code, market="sh")
            if df is None or df.empty:
                raise ValueError(f"未找到 {stock_code} 的资金流向")

            latest = df.iloc[0]

            return {
                "main_inflow": self._safe_float(latest.get('主力净流入-净额')),
                "main_inflow_pct": self._safe_float(latest.get('主力净流入-净占比')),
                "super_inflow": self._safe_float(latest.get('超大单净流入-净额')),
                "large_inflow": self._safe_float(latest.get('大单净流入-净额')),
                "medium_inflow": self._safe_float(latest.get('中单净流入-净额')),
                "small_inflow": self._safe_float(latest.get('小单净流入-净额')),
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            # 尝试深市
            try:
                df = self._ak.stock_individual_fund_flow(stock=stock_code, market="sz")
                if df is None or df.empty:
                    raise ValueError(f"未找到 {stock_code} 的资金流向")

                latest = df.iloc[0]
                return {
                    "main_inflow": self._safe_float(latest.get('主力净流入-净额')),
                    "source": self.source_name,
                    "is_estimated": False,
                }
            except:
                raise RuntimeError(f"AKShare获取资金流向失败: {e}")

    def get_market_data(self, stock_code: str) -> Dict:
        """获取市场数据"""
        self._ensure_akshare()
        
        try:
            # 行业信息
            df = self._ak.stock_individual_info_em(symbol=stock_code)
            if df is not None and not df.empty:
                industry = df.iloc[0].get('行业', '未知')
            else:
                industry = '未知'
                
            # 行业涨跌
            try:
                board_df = self._ak.stock_board_industry_name_em()
                if board_df is not None:
                    board_row = board_df[board_df['名称'] == industry]
                    if not board_row.empty:
                        industry_change = self._safe_float(board_row.iloc[0].get('涨跌幅', 0))
                    else:
                        industry_change = 0
                else:
                    industry_change = 0
            except:
                industry_change = 0

            return {
                "industry": industry,
                "industry_change": industry_change,
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            return {
                "industry": "未知",
                "industry_change": 0,
                "source": self.source_name,
                "is_estimated": False,
                "error": str(e)
            }

    def get_all_data(self, stock_code: str) -> Dict:
        """
        获取所有财务数据（统一接口）

        Args:
            stock_code: 股票代码

        Returns:
            完整财务数据字典
        """
        result = {
            "stock_code": stock_code,
            "timestamp": pd.Timestamp.now().isoformat(),
        }

        # 财务指标
        try:
            result["financial_indicator"] = self.get_financial_indicator(stock_code)
        except Exception as e:
            result["financial_indicator"] = {"error": str(e), "source": self.source_name}

        # 估值指标
        try:
            result["valuation"] = self.get_valuation(stock_code)
        except Exception as e:
            result["valuation"] = {"error": str(e), "source": self.source_name}

        # 资金流向
        try:
            result["fund_flow"] = self.get_fund_flow(stock_code)
        except Exception as e:
            result["fund_flow"] = {"error": str(e), "source": self.source_name}

        # 市场数据
        try:
            result["market_data"] = self.get_market_data(stock_code)
        except Exception as e:
            result["market_data"] = {"error": str(e), "source": self.source_name}

        return result

    def _safe_float(self, value) -> Optional[float]:
        """安全转换为float"""
        if value is None or pd.isna(value):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


def test_akshare():
    """测试AKShare数据获取"""
    print("=" * 60)
    print("AKShare 财务数据获取测试")
    print("=" * 60)
    
    try:
        fetcher = FinancialDataFetcherAKShare()
        
        # 测试股票
        test_code = "600919"  # 江苏银行
        
        print(f"\n📊 获取股票 {test_code} 财务数据...\n")
        
        # 财务指标
        fi = fetcher.get_financial_indicator(test_code)
        print(f"【财务指标】")
        print(f"  ROE: {fi.get('roe')}%")
        print(f"  毛利率: {fi.get('gross_margin')}%")
        print(f"  净利率: {fi.get('net_margin')}%")
        print(f"  营收增速: {fi.get('revenue_growth')}%")
        print(f"  利润增速: {fi.get('profit_growth')}%")
        print(f"  数据来源: {fi.get('source')}")
        print(f"  是否估算: {fi.get('is_estimated')}")
        
        # 估值
        val = fetcher.get_valuation(test_code)
        print(f"\n【估值指标】")
        print(f"  PE-TTM: {val.get('pe_ttm')}倍")
        print(f"  PB: {val.get('pb')}倍")
        print(f"  股息率: {val.get('dv_ratio')}%")
        print(f"  总市值: {val.get('total_mv')}亿")
        
        # 资金流向
        ff = fetcher.get_fund_flow(test_code)
        print(f"\n【资金流向】")
        print(f"  主力净流入: {ff.get('main_inflow')}万")
        
        # 行业
        md = fetcher.get_market_data(test_code)
        print(f"\n【市场数据】")
        print(f"  所属行业: {md.get('industry')}")
        print(f"  行业涨跌: {md.get('industry_change')}%")
        
        print("\n" + "=" * 60)
        print("✅ AKShare 数据获取测试成功!")
        print("=" * 60)
        
    except ImportError as e:
        print("\n❌ AKShare 未安装")
        print(f"   错误: {e}")
        print("\n📝 安装命令: pip install akshare")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("=" * 60)


if __name__ == "__main__":
    test_akshare()