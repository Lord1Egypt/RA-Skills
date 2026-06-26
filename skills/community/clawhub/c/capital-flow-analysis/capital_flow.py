"""
Capital Flow Analysis - 资金流向分析

功能：
- 主力资金流向
- 北向资金分析
- 龙虎榜数据
"""

import akshare as ak
import pandas as pd
from typing import Dict
from datetime import datetime


def analyze_main_force(code: str) -> Dict:
    """主力资金分析"""
    try:
        # 获取资金流向数据
        fund_flow = ak.stock_individual_fund_flow(symbol=code, market="sz" if code.startswith('3') else "sh")
        
        if fund_flow.empty:
            return {"error": "数据获取失败"}
        
        latest = fund_flow.iloc[-1]
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "main_force_net": round(float(latest['主力净流入 - 净额']) / 10000, 2),
            "main_force_5day": round(float(latest['主力净流入 -5 日']) / 10000, 2),
            "signal": "流入" if float(latest['主力净流入 - 净额']) > 0 else "流出",
            "trend": "连续流入" if float(latest['主力净流入 -5 日']) > 0 else "连续流出"
        }
    except Exception as e:
        return {"error": str(e)}


def analyze_northbound(code: str) -> Dict:
    """北向资金分析"""
    try:
        # 获取北向资金持股数据
        northbound = ak.stock_hsgt_individual_em(symbol=code)
        
        if northbound.empty:
            return {"error": "无北向资金数据"}
        
        latest = northbound.iloc[-1]
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "holding_shares": round(float(latest['持股数']) / 1000000, 2),
            "holding_pct": round(float(latest['持股比例']), 2),
            "change": round(float(latest['持股变动']), 2),
            "signal": "增持" if float(latest['持股变动']) > 0 else "减持"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("测试资金流向分析")
    print("=" * 50)
    
    main_result = analyze_main_force("300308")
    print(f"主力资金：{main_result}")
    
    northbound_result = analyze_northbound("300308")
    print(f"北向资金：{northbound_result}")
