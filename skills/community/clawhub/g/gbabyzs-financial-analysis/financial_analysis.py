"""
Financial Analysis - 财务分析工具

功能：
- 估值指标计算 (PE/PB/PS/PEG)
- 盈利能力分析 (ROE/ROA/毛利率)
- 财务健康度评估
- DCF 估值模型
"""

import akshare as ak
import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime


def get_financial_data(code: str) -> Dict:
    """获取财务数据"""
    try:
        # 获取基本面数据
        fundamental = ak.stock_financial_analysis_indicator(symbol=code)
        
        # 获取估值数据
        valuation = ak.stock_value_em(symbol=code)
        
        return {
            "fundamental": fundamental,
            "valuation": valuation
        }
    except Exception as e:
        print(f"获取财务数据失败：{e}")
        return {}


def calculate_pe(code: str) -> Dict:
    """计算市盈率"""
    try:
        stock_info = ak.stock_info_a_code_name()
        stock_data = ak.stock_zh_a_spot_em()
        stock_item = stock_data[stock_data['代码'] == code]
        
        if stock_item.empty:
            return {"error": "未找到股票数据"}
        
        price = float(stock_item['最新价'].iloc[0])
        eps = float(stock_item['每股收益'].iloc[0]) if '每股收益' in stock_item.columns else 0
        
        pe_ttm = price / eps if eps > 0 else None
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "price": round(price, 2),
            "eps": round(eps, 4),
            "pe_ttm": round(pe_ttm, 2) if pe_ttm else None,
            "pe_level": "高" if pe_ttm and pe_ttm > 50 else ("中" if pe_ttm and pe_ttm > 20 else "低")
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_pb(code: str) -> Dict:
    """计算市净率"""
    try:
        stock_data = ak.stock_zh_a_spot_em()
        stock_item = stock_data[stock_data['代码'] == code]
        
        if stock_item.empty:
            return {"error": "未找到股票数据"}
        
        price = float(stock_item['最新价'].iloc[0])
        bvps = float(stock_item['每股净资产'].iloc[0]) if '每股净资产' in stock_item.columns else 0
        
        pb = price / bvps if bvps > 0 else None
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "price": round(price, 2),
            "bvps": round(bvps, 2),
            "pb": round(pb, 2) if pb else None,
            "pb_level": "高" if pb and pb > 5 else ("中" if pb and pb > 2 else "低")
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_roe(code: str) -> Dict:
    """计算 ROE"""
    try:
        financial_data = ak.stock_financial_analysis_indicator(symbol=code)
        
        # 获取最新 ROE
        latest_roe = float(financial_data['加权净资产收益率 (%)'].iloc[0]) if not financial_data.empty else 0
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "roe": round(latest_roe, 2),
            "roe_level": "优秀" if latest_roe > 20 else ("良好" if latest_roe > 15 else ("一般" if latest_roe > 10 else "较差"))
        }
    except Exception as e:
        return {"error": str(e)}


def financial_health_score(code: str) -> Dict:
    """财务健康度评分"""
    try:
        financial_data = ak.stock_financial_analysis_indicator(symbol=code)
        
        if financial_data.empty:
            return {"error": "数据获取失败"}
        
        score = 0
        details = {}
        
        # ROE 评分 (0-30 分)
        roe = float(financial_data['加权净资产收益率 (%)'].iloc[0])
        if roe > 20:
            score += 30
            details["roe"] = "优秀"
        elif roe > 15:
            score += 25
            details["roe"] = "良好"
        elif roe > 10:
            score += 20
            details["roe"] = "一般"
        else:
            score += 10
            details["roe"] = "较差"
        
        # 资产负债率评分 (0-25 分)
        debt_ratio = float(financial_data['资产负债率 (%)'].iloc[0])
        if debt_ratio < 40:
            score += 25
            details["debt"] = "优秀"
        elif debt_ratio < 60:
            score += 20
            details["debt"] = "良好"
        elif debt_ratio < 70:
            score += 15
            details["debt"] = "一般"
        else:
            score += 5
            details["debt"] = "高风险"
        
        # 毛利率评分 (0-25 分)
        gross_margin = float(financial_data['销售毛利率 (%)'].iloc[0])
        if gross_margin > 40:
            score += 25
            details["margin"] = "优秀"
        elif gross_margin > 25:
            score += 20
            details["margin"] = "良好"
        elif gross_margin > 15:
            score += 15
            details["margin"] = "一般"
        else:
            score += 5
            details["margin"] = "较差"
        
        # 营收增长评分 (0-20 分)
        revenue_growth = float(financial_data['营业收入同比增长率 (%)'].iloc[0])
        if revenue_growth > 30:
            score += 20
            details["growth"] = "高增长"
        elif revenue_growth > 15:
            score += 15
            details["growth"] = "中增长"
        elif revenue_growth > 5:
            score += 10
            details["growth"] = "低增长"
        else:
            score += 5
            details["growth"] = "负增长"
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "score": score,
            "level": "优秀" if score >= 80 else ("良好" if score >= 60 else ("一般" if score >= 40 else "较差")),
            "details": details
        }
    except Exception as e:
        return {"error": str(e)}


def dcf_valuation(code: str, growth_rate: float = 0.15, discount_rate: float = 0.1, terminal_growth: float = 0.03) -> Dict:
    """DCF 估值模型"""
    try:
        # 获取财务数据
        financial_data = ak.stock_financial_analysis_indicator(symbol=code)
        stock_data = ak.stock_zh_a_spot_em()
        stock_item = stock_data[stock_data['代码'] == code]
        
        if financial_data.empty or stock_item.empty:
            return {"error": "数据获取失败"}
        
        # 获取自由现金流 (简化为经营现金流)
        fcf = float(financial_data['每股经营性现金流'].iloc[0])
        shares = float(stock_item['总股本'].iloc[0]) * 10000  # 转换为股
        
        # 预测未来 5 年现金流
        projected_fcf = []
        for i in range(5):
            projected_fcf.append(fcf * (1 + growth_rate) ** (i + 1))
        
        # 计算终值
        terminal_value = projected_fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
        
        # 折现
        pv_fcf = sum([fcf / (1 + discount_rate) ** (i + 1) for i, fcf in enumerate(projected_fcf)])
        pv_terminal = terminal_value / (1 + discount_rate) ** 5
        
        # 计算每股价值
        equity_value = (pv_fcf + pv_terminal) * shares
        intrinsic_value = equity_value / shares
        
        current_price = float(stock_item['最新价'].iloc[0])
        margin_of_safety = (intrinsic_value - current_price) / current_price * 100
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "intrinsic_value": round(intrinsic_value, 2),
            "current_price": round(current_price, 2),
            "margin_of_safety": round(margin_of_safety, 2),
            "recommendation": "买入" if margin_of_safety > 20 else ("持有" if margin_of_safety > 0 else "卖出"),
            "assumptions": {
                "growth_rate": growth_rate,
                "discount_rate": discount_rate,
                "terminal_growth": terminal_growth
            }
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # 测试示例
    print("测试 300308 中际旭创财务分析")
    print("=" * 50)
    
    pe_result = calculate_pe("300308")
    print(f"PE 结果：{pe_result}")
    
    roe_result = calculate_roe("300308")
    print(f"ROE 结果：{roe_result}")
    
    health_result = financial_health_score("300308")
    print(f"财务健康度：{health_result}")
