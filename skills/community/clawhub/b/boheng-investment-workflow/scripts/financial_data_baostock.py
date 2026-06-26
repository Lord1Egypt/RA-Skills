#!/usr/bin/env python3
"""
baostock 财务数据获取模块
用于获取真实财务数据，替代估算值

依赖: baostock (可选安装)
使用: python3 scripts/analyze_stock.py 600919 --baostock

版本: 1.1.0 (新增日期智能选择功能)
"""
import baostock as bs
import pandas as pd
from typing import Dict, Optional, Tuple
from datetime import datetime
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)


class FinancialDataFetcherBaostock:
    """
    baostock财务数据获取器
    
    说明:
        - 数据来源: 东方财富/证券交易所
        - 数据类型: 真实财报数据
        - 稳定性: 高
        - 成本: 免费
    
    使用示例:
        fetcher = FinancialDataFetcherBaostock()
        data = fetcher.get_financial_indicator("002594")
        print(f"ROE: {data['roe']}%")
    """

    def __init__(self):
        self.source_name = "baostock"
        self._logged_in = False

    def get_latest_report_period(self, query_date: str = None) -> Tuple[int, int]:
        """
        根据查询日期确定可获取的最新财报期间
        
        财报披露规则:
        - 1月-4月30日: 可获取上一年度年报 (Q4)
        - 5月-8月31日: 可获取当年一季报 (Q1)
        - 9月-10月31日: 可获取当年半年报 (Q2)
        - 11月-12月: 可获取当年三季报 (Q3)
        
        Args:
            query_date: 查询日期，格式 "YYYY-MM-DD"，默认使用当前时间
            
        Returns:
            (year, quarter) 元组
        """
        if query_date is None:
            query_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            dt = datetime.strptime(query_date, "%Y-%m-%d")
        except:
            dt = datetime.now()
        
        year = dt.year
        month = dt.month
        
        # 判断逻辑
        if month <= 4:
            # 1月-4月：获取去年年报
            return year - 1, 4
        elif month <= 8:
            # 5月-8月：获取当年一季报
            return year, 1
        elif month <= 10:
            # 9月-10月：获取当年半年报
            return year, 2
        else:
            # 11月-12月：获取当年三季报
            return year, 3

    def _ensure_login(self):
        """确保已登录baostock"""
        if not self._logged_in:
            lg = bs.login()
            if lg.error_code != '0':
                raise RuntimeError(f"baostock登录失败: {lg.error_msg}")
            self._logged_in = True

    def _logout(self):
        """登出"""
        if self._logged_in:
            bs.logout()
            self._logged_in = False

    def get_financial_indicator(self, stock_code: str, query_date: str = None) -> Dict:
        """
        获取主要财务指标（真实财报数据）

        Args:
            stock_code: 股票代码（如 "002594"）
            query_date: 查询日期（可选，格式: "YYYY-MM-DD"）
                       默认使用当前系统时间，自动判断可获取的最新财报

        Returns:
            财务指标字典
        """
        # 获取最新的财报期间
        year, quarter = self.get_latest_report_period(query_date)
        print(f"   📊 正在获取 {year}年第{quarter}季度财报数据...")
        
        self._ensure_login()
        
        # 转换代码格式
        bs_code = self._format_code(stock_code)
        
        # 记录实际获取的财报期间
        actual_year, actual_quarter = year, quarter
        
        try:
            # 获取利润数据 - 使用动态年份和季度
            rs = bs.query_profit_data(code=bs_code, year=year, quarter=quarter)
            profit_data = []
            while (rs.error_code == '0') & rs.next():
                profit_data.append(rs.get_row_data())
            
            if not profit_data:
                # 回退逻辑：优先尝试同年的前一季度
                fallback_quarter = quarter - 1 if quarter > 1 else 4
                fallback_year = year if quarter > 1 else year - 1
                rs = bs.query_profit_data(code=bs_code, year=fallback_year, quarter=fallback_quarter)
                while (rs.error_code == '0') & rs.next():
                    profit_data.append(rs.get_row_data())
                if profit_data:
                    actual_year, actual_quarter = fallback_year, fallback_quarter
                else:
                    # 再次回退：尝试前一年Q4（年报）
                    rs = bs.query_profit_data(code=bs_code, year=year-1, quarter=4)
                    while (rs.error_code == '0') & rs.next():
                        profit_data.append(rs.get_row_data())
                    if profit_data:
                        actual_year, actual_quarter = year-1, 4
            
            if not profit_data:
                raise ValueError(f"未找到 {stock_code} 的财务数据")
            
            latest = profit_data[0]
            
            # 获取资产负债率 - 使用动态年份和季度
            debt_ratio = None
            current_ratio = None
            try:
                rs_bal = bs.query_balance_data(code=bs_code, year=actual_year, quarter=actual_quarter)
                bal_data = []
                while rs_bal.next():
                    bal_data.append(rs_bal.get_row_data())
                if not bal_data:
                    # 回退到前一年Q4
                    rs_bal = bs.query_balance_data(code=bs_code, year=actual_year-1, quarter=4)
                    while rs_bal.next():
                        bal_data.append(rs_bal.get_row_data())
                if bal_data:
                    # currentRatio字段在位置3, assetToEquity在位置8
                    current_ratio = self._safe_float(bal_data[0][3])  # currentRatio
                    # liabilityToAsset可能是小数形式，尝试从assetToEquity计算
                    asset_to_equity = self._safe_float(bal_data[0][8])  # assetToEquity
                    if asset_to_equity and asset_to_equity > 0:
                        debt_ratio = (asset_to_equity - 1) / asset_to_equity  # 计算资产负债率
                    else:
                        debt_ratio = self._safe_float(bal_data[0][7])  # liabilityToAsset
            except Exception as e:
                print(f"   ⚠️ 资产负债率获取失败: {e}")
                pass
            
            # 获取成长数据（营收增速、利润增速）- 使用动态年份和季度
            revenue_growth = None
            profit_growth = None
            try:
                rs_growth = bs.query_growth_data(code=bs_code, year=actual_year, quarter=actual_quarter)
                growth_data = []
                while rs_growth.next():
                    growth_data.append(rs_growth.get_row_data())
                if not growth_data:
                    # 回退到前一年Q4
                    rs_growth = bs.query_growth_data(code=bs_code, year=actual_year-1, quarter=4)
                    while rs_growth.next():
                        growth_data.append(rs_growth.get_row_data())
                if growth_data:
                    # YOYNI: 净利润增速（利润增速）在位置5
                    # YOYPNI: 归属于母公司净利润增速
                    profit_growth = self._safe_float(growth_data[0][5]) * 100  # 转换为百分比
                    # 营收增速使用YOYAsset（资产增速作为参考）或估算
                    revenue_growth = self._safe_float(growth_data[0][4]) * 100 if growth_data[0][4] else None  # YOYAsset
            except:
                pass
            
            result = {
                "roe": self._safe_float(latest[3]),  # roeAvg
                "net_margin": self._safe_float(latest[4]),  # npMargin
                "gross_margin": self._safe_float(latest[5]),  # gpMargin
                "net_profit": self._safe_float(latest[6]),  # netProfit
                "eps": self._safe_float(latest[7]),  # epsTTM
                "revenue": self._safe_float(latest[8]),  # MBRevenue
                "debt_ratio": debt_ratio,  # 资产负债率
                "current_ratio": current_ratio,  # 流动比率
                "revenue_growth": revenue_growth,  # 营收增速
                "profit_growth": profit_growth,  # 利润增速
                "source": self.source_name,
                "is_estimated": False,
                "report_date": latest[2],  # statDate
                "report_period": {
                    "year": actual_year,
                    "quarter": actual_quarter,
                    "display": f"{actual_year}年{actual_quarter}季度"
                },  # 新增：财报期间结构化标记
            }
            return result
        except Exception as e:
            raise RuntimeError(f"baostock获取财务指标失败: {e}")

    def get_dupont(self, stock_code: str) -> Dict:
        """获取杜邦分析数据"""
        self._ensure_login()
        
        bs_code = self._format_code(stock_code)
        
        try:
            rs = bs.query_dupont_data(code=bs_code, year=2024, quarter=4)
            data = []
            while (rs.error_code == '0') & rs.next():
                data.append(rs.get_row_data())
            
            if not data:
                rs = bs.query_dupont_data(code=bs_code, year=2023, quarter=4)
                while (rs.error_code == '0') & rs.next():
                    data.append(rs.get_row_data())
            
            if not data:
                return {}
            
            latest = data[0]
            
            return {
                "dupont_roe": self._safe_float(latest[3]),  # dupontROE
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_operation(self, stock_code: str) -> Dict:
        """获取经营数据"""
        self._ensure_login()
        
        bs_code = self._format_code(stock_code)
        
        try:
            rs = bs.query_operation_data(code=bs_code, year=2024, quarter=4)
            data = []
            while (rs.error_code == '0') & rs.next():
                data.append(rs.get_row_data())
            
            if not data:
                return {}
            
            latest = data[0]
            
            return {
                "nr_turn_ratio": self._safe_float(latest[3]),  # NRTurnRatio
                "inv_turn_ratio": self._safe_float(latest[5]),  # INVTurnRatio
                "source": self.source_name,
                "is_estimated": False,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_all_data(self, stock_code: str) -> Dict:
        """获取所有财务数据（统一接口）"""
        self._ensure_login()
        
        result = {
            "stock_code": stock_code,
            "timestamp": pd.Timestamp.now().isoformat(),
        }
        
        # 财务指标
        try:
            result["financial_indicator"] = self.get_financial_indicator(stock_code)
        except Exception as e:
            result["financial_indicator"] = {"error": str(e), "source": self.source_name}
        
        # 杜邦分析
        try:
            result["dupont"] = self.get_dupont(stock_code)
        except:
            pass
        
        # 经营数据
        try:
            result["operation"] = self.get_operation(stock_code)
        except:
            pass
        
        return result

    def _format_code(self, stock_code: str) -> str:
        """格式化股票代码为baostock格式"""
        code = stock_code.strip()
        if code.startswith('6'):
            return f"sh.{code}"
        else:
            return f"sz.{code}"

    def _safe_float(self, value) -> Optional[float]:
        """安全转换为float"""
        if value is None or value == '':
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def __del__(self):
        """析构时登出"""
        self._logout()



    def get_dividend_yield(self, stock_code: str) -> float:
        """
        获取股息率
        """
        import baostock as bs
        
        try:
            # 登录
            lg = bs.login()
            if lg.error_code != '0':
                return 0.0
            
            # 转换股票代码格式
            if stock_code.startswith('6'):
                bs_code = f"sh.{stock_code}"
            elif stock_code.startswith('0') or stock_code.startswith('3'):
                bs_code = f"sz.{stock_code}"
            else:
                bs.logout()
                return 0.0
            
            # 获取最近年份的股息数据
            rs = bs.query_dividend_data(code=bs_code, year="2025")
            
            total_yield = 0.0
            count = 0
            
            while rs.next():
                data = rs.get_row_data()
                if len(data) >= 10 and data[9]:
                    try:
                        div = float(data[9])
                        total_yield += div
                        count += 1
                    except:
                        pass
            
            # 登出
            bs.logout()
            
            if count > 0:
                return round(total_yield / count, 2)
            
            # 尝试2024年 - 需要重新登录
            lg = bs.login()
            if lg.error_code != '0':
                return 0.0
            
            rs = bs.query_dividend_data(code=bs_code, year="2024")
            while rs.next():
                data = rs.get_row_data()
                if len(data) >= 10 and data[9]:
                    try:
                        div = float(data[9])
                        bs.logout()
                        return round(div, 2)
                    except:
                        pass
            
            bs.logout()
            return 0.0
            
        except Exception as e:
            try:
                bs.logout()
            except:
                pass
            print(f"获取股息率失败: {e}")
            return 0.0

def test_baostock():
    """测试baostock"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from financial_data_baostock import FinancialDataFetcherBaostock
    
    bs = FinancialDataFetcherBaostock()
    result = bs.get_financial_indicator('601857')
    print("财务指标:", result)
    
    div = bs.get_dividend_yield('601857')
    print("股息率:", div)
    
if __name__ == "__main__":
    test_baostock()
