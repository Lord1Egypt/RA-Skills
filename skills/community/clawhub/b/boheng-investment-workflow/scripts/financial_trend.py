#!/usr/bin/env python3
"""
财务趋势分析模块 - 多年财务数据对比分析
用于识别财务趋势变化和风险信号
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 尝试导入 akshare
try:
    import akshare as ak
    import pandas as pd
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ AKShare 未安装，部分功能不可用")


class FinancialTrendAnalyzer:
    """财务趋势分析器"""
    
    def __init__(self, stock_code: str):
        """
        初始化
        
        Args:
            stock_code: 股票代码（6位数字）
        """
        self.stock_code = stock_code
        self.income_data = None  # 利润表数据
        self.balance_data = None  # 资产负债表数据
        self.cashflow_data = None  # 现金流量表数据
        
    def fetch_multi_year_data(self, years: int = 5) -> bool:
        """
        获取多年财务数据
        
        Args:
            years: 获取最近N年数据
            
        Returns:
            是否成功获取数据
        """
        if not HAS_AKSHARE:
            print("❌ AKShare 未安装，无法获取财务数据")
            return False
            
        try:
            print(f"📊 正在获取 {self.stock_code} 最近{years}年财务数据...")
            
            # 获取利润表
            print("   ⏳ 获取利润表...")
            df_income = ak.stock_financial_report_sina(stock=self.stock_code, symbol="利润表")
            if df_income is not None and not df_income.empty:
                # 筛选年报数据
                df_income = df_income[df_income['报告日'].str.endswith('1231', na=False)]
                self.income_data = df_income.head(years)
                print(f"   ✅ 利润表: {len(self.income_data)}年数据")
            
            # 获取资产负债表
            print("   ⏳ 获取资产负债表...")
            df_balance = ak.stock_financial_report_sina(stock=self.stock_code, symbol="资产负债表")
            if df_balance is not None and not df_balance.empty:
                df_balance = df_balance[df_balance['报告日'].str.endswith('1231', na=False)]
                self.balance_data = df_balance.head(years)
                print(f"   ✅ 资产负债表: {len(self.balance_data)}年数据")
            
            # 获取现金流量表
            print("   ⏳ 获取现金流量表...")
            df_cashflow = ak.stock_financial_report_sina(stock=self.stock_code, symbol="现金流量表")
            if df_cashflow is not None and not df_cashflow.empty:
                df_cashflow = df_cashflow[df_cashflow['报告日'].str.endswith('1231', na=False)]
                self.cashflow_data = df_cashflow.head(years)
                print(f"   ✅ 现金流量表: {len(self.cashflow_data)}年数据")
            
            return True
            
        except Exception as e:
            print(f"❌ 获取财务数据失败: {e}")
            return False
    
    def get_latest_quarter_data(self) -> Optional[Dict]:
        """
        获取最新季度数据（用于同比对比）
        
        Returns:
            最新季度数据字典
        """
        if not HAS_AKSHARE:
            return None
            
        try:
            df_income = ak.stock_financial_report_sina(stock=self.stock_code, symbol="利润表")
            if df_income is not None and not df_income.empty:
                latest = df_income.iloc[0]
                return {
                    "report_date": latest['报告日'],
                    "revenue": float(latest['营业收入']) / 1e8 if pd.notna(latest['营业收入']) else 0,
                    "net_profit": float(latest['归属于母公司所有者的净利润']) / 1e8 if pd.notna(latest['归属于母公司所有者的净利润']) else 0,
                    "gross_profit": float(latest['营业收入']) / 1e8 - float(latest['营业成本']) / 1e8 if pd.notna(latest['营业收入']) else 0,
                }
        except Exception as e:
            print(f"获取最新季度数据失败: {e}")
            
        return None
    
    def calculate_trend_metrics(self) -> Dict:
        """
        计算趋势指标
        
        Returns:
            趋势指标字典
        """
        metrics = {
            "revenue": [],      # 营业收入趋势
            "net_profit": [],   # 净利润趋势
            "roe": [],          # ROE趋势
            "gross_margin": [], # 毛利率趋势
            "net_margin": [],   # 净利率趋势
            "debt_ratio": [],   # 资产负债率趋势
        }
        
        if self.income_data is None or self.balance_data is None:
            return metrics
            
        try:
            # 遍历每年数据（从旧到新）
            years = min(len(self.income_data), len(self.balance_data))
            
            for i in range(years - 1, -1, -1):
                income_row = self.income_data.iloc[i]
                balance_row = self.balance_data.iloc[i]
                
                report_date = income_row['报告日']
                year = report_date[:4]
                
                # 营业收入（亿）
                revenue = float(income_row['营业收入']) / 1e8 if pd.notna(income_row['营业收入']) else 0
                
                # 营业成本（亿）
                cost = float(income_row['营业成本']) / 1e8 if pd.notna(income_row['营业成本']) else 0
                
                # 归母净利润（亿）
                net_profit = float(income_row['归属于母公司所有者的净利润']) / 1e8 if pd.notna(income_row['归属于母公司所有者的净利润']) else 0
                
                # 总资产（亿）
                total_assets = float(balance_row['资产总计']) / 1e8 if pd.notna(balance_row['资产总计']) else 0
                
                # 总负债（亿）
                total_liab = float(balance_row['负债合计']) / 1e8 if pd.notna(balance_row['负债合计']) else 0
                
                # 归母股东权益（亿）
                equity = float(balance_row['归属于母公司股东权益合计']) / 1e8 if pd.notna(balance_row['归属于母公司股东权益合计']) else 0
                
                # 计算比率
                gross_margin = (revenue - cost) / revenue * 100 if revenue > 0 else 0
                net_margin = net_profit / revenue * 100 if revenue > 0 else 0
                debt_ratio = total_liab / total_assets * 100 if total_assets > 0 else 0
                roe = net_profit / equity * 100 if equity > 0 else 0
                
                # 添加到趋势列表
                metrics["revenue"].append({"year": year, "value": revenue})
                metrics["net_profit"].append({"year": year, "value": net_profit})
                metrics["roe"].append({"year": year, "value": roe})
                metrics["gross_margin"].append({"year": year, "value": gross_margin})
                metrics["net_margin"].append({"year": year, "value": net_margin})
                metrics["debt_ratio"].append({"year": year, "value": debt_ratio})
                
        except Exception as e:
            print(f"计算趋势指标失败: {e}")
            
        return metrics
    
    def identify_risk_signals(self, metrics: Dict) -> List[Dict]:
        """
        识别风险信号
        
        Args:
            metrics: 趋势指标字典
            
        Returns:
            风险信号列表
        """
        risks = []
        
        # 1. 营收下滑风险
        revenue = metrics.get("revenue", [])
        if len(revenue) >= 2:
            latest = revenue[-1]["value"]
            previous = revenue[-2]["value"]
            if latest < previous:
                change = (latest - previous) / previous * 100 if previous > 0 else 0
                risks.append({
                    "type": "营收下滑",
                    "severity": "高" if change < -10 else "中",
                    "description": f"营收同比下降 {abs(change):.1f}%",
                    "detail": f"{revenue[-2]['year']}: {previous:.2f}亿 → {revenue[-1]['year']}: {latest:.2f}亿"
                })
        
        # 2. 净利润下滑风险
        net_profit = metrics.get("net_profit", [])
        if len(net_profit) >= 2:
            latest = net_profit[-1]["value"]
            previous = net_profit[-2]["value"]
            if latest < previous:
                change = (latest - previous) / previous * 100 if previous > 0 else 0
                risks.append({
                    "type": "净利润下滑",
                    "severity": "高" if change < -20 else "中",
                    "description": f"净利润同比下降 {abs(change):.1f}%",
                    "detail": f"{net_profit[-2]['year']}: {previous:.2f}亿 → {net_profit[-1]['year']}: {latest:.2f}亿"
                })
        
        # 3. 毛利率下降风险
        gross_margin = metrics.get("gross_margin", [])
        if len(gross_margin) >= 2:
            latest = gross_margin[-1]["value"]
            previous = gross_margin[-2]["value"]
            if latest < previous - 2:  # 下降超过2个百分点
                change = latest - previous
                risks.append({
                    "type": "毛利率下降",
                    "severity": "中",
                    "description": f"毛利率同比下降 {abs(change):.1f}个百分点",
                    "detail": f"{gross_margin[-2]['year']}: {previous:.1f}% → {gross_margin[-1]['year']}: {latest:.1f}%"
                })
        
        # 4. ROE下降风险
        roe = metrics.get("roe", [])
        if len(roe) >= 2:
            latest = roe[-1]["value"]
            previous = roe[-2]["value"]
            if latest < previous - 3:  # 下降超过3个百分点
                change = latest - previous
                risks.append({
                    "type": "ROE下降",
                    "severity": "中",
                    "description": f"ROE同比下降 {abs(change):.1f}个百分点",
                    "detail": f"{roe[-2]['year']}: {previous:.1f}% → {roe[-1]['year']}: {latest:.1f}%"
                })
        
        # 5. 资产负债率上升风险
        debt_ratio = metrics.get("debt_ratio", [])
        if len(debt_ratio) >= 2:
            latest = debt_ratio[-1]["value"]
            previous = debt_ratio[-2]["value"]
            if latest > previous + 5:  # 上升超过5个百分点
                change = latest - previous
                risks.append({
                    "type": "负债率上升",
                    "severity": "中" if latest < 70 else "高",
                    "description": f"资产负债率同比上升 {change:.1f}个百分点",
                    "detail": f"{debt_ratio[-2]['year']}: {previous:.1f}% → {debt_ratio[-1]['year']}: {latest:.1f}%"
                })
        
        # 6. 连续下滑风险
        if len(revenue) >= 3:
            declining = all(revenue[i]["value"] < revenue[i-1]["value"] for i in range(1, len(revenue)))
            if declining:
                risks.append({
                    "type": "营收连续下滑",
                    "severity": "高",
                    "description": f"营收连续{len(revenue)}年下滑",
                    "detail": "需关注公司基本面变化"
                })
        
        return risks
    
    def generate_trend_report(self, metrics: Dict, risks: List[Dict]) -> str:
        """
        生成趋势分析报告
        
        Args:
            metrics: 趋势指标字典
            risks: 风险信号列表
            
        Returns:
            报告文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("📊 财务趋势分析报告")
        lines.append("=" * 60)
        
        # 营收趋势
        revenue = metrics.get("revenue", [])
        if revenue:
            lines.append("\n📈 营业收入趋势")
            lines.append("-" * 60)
            lines.append(f"{'年份':<8} {'营收(亿)':<12} {'同比':<10} {'趋势':<10}")
            lines.append("-" * 60)
            for i, item in enumerate(revenue):
                year = item["year"]
                value = item["value"]
                if i == 0:
                    yoy = "-"
                    trend = "-"
                else:
                    prev = revenue[i-1]["value"]
                    yoy = f"{(value - prev) / prev * 100:.1f}%" if prev > 0 else "-"
                    trend = "↑" if value > prev else "↓" if value < prev else "→"
                lines.append(f"{year:<8} {value:<12.2f} {yoy:<10} {trend:<10}")
        
        # 净利润趋势
        net_profit = metrics.get("net_profit", [])
        if net_profit:
            lines.append("\n💰 净利润趋势")
            lines.append("-" * 60)
            lines.append(f"{'年份':<8} {'净利(亿)':<12} {'同比':<10} {'趋势':<10}")
            lines.append("-" * 60)
            for i, item in enumerate(net_profit):
                year = item["year"]
                value = item["value"]
                if i == 0:
                    yoy = "-"
                    trend = "-"
                else:
                    prev = net_profit[i-1]["value"]
                    yoy = f"{(value - prev) / prev * 100:.1f}%" if prev > 0 else "-"
                    trend = "↑" if value > prev else "↓" if value < prev else "→"
                lines.append(f"{year:<8} {value:<12.2f} {yoy:<10} {trend:<10}")
        
        # ROE趋势
        roe = metrics.get("roe", [])
        if roe:
            lines.append("\n📊 ROE趋势")
            lines.append("-" * 60)
            lines.append(f"{'年份':<8} {'ROE':<12} {'变化':<10} {'评价':<10}")
            lines.append("-" * 60)
            for item in roe:
                year = item["year"]
                value = item["value"]
                if value >= 15:
                    rating = "优秀"
                elif value >= 10:
                    rating = "良好"
                elif value >= 5:
                    rating = "一般"
                else:
                    rating = "较差"
                lines.append(f"{year:<8} {value:<12.1f}% {'':<10} {rating:<10}")
        
        # 毛利率趋势
        gross_margin = metrics.get("gross_margin", [])
        if gross_margin:
            lines.append("\n📊 毛利率趋势")
            lines.append("-" * 60)
            lines.append(f"{'年份':<8} {'毛利率':<12} {'变化':<10} {'趋势':<10}")
            lines.append("-" * 60)
            for i, item in enumerate(gross_margin):
                year = item["year"]
                value = item["value"]
                if i == 0:
                    change = "-"
                    trend = "-"
                else:
                    prev = gross_margin[i-1]["value"]
                    change = f"{value - prev:.1f}%"
                    trend = "↑" if value > prev else "↓" if value < prev else "→"
                lines.append(f"{year:<8} {value:<12.1f}% {change:<10} {trend:<10}")
        
        # 风险信号
        if risks:
            lines.append("\n⚠️ 风险信号")
            lines.append("-" * 60)
            for i, risk in enumerate(risks, 1):
                severity = risk.get("severity", "中")
                icon = "🔴" if severity == "高" else "🟡"
                lines.append(f"{i}. {icon} {risk['type']} ({severity})")
                lines.append(f"   {risk['description']}")
                if "detail" in risk:
                    lines.append(f"   {risk['detail']}")
        else:
            lines.append("\n✅ 未发现明显风险信号")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
    
    def analyze(self, years: int = 5) -> Dict:
        """
        执行完整分析
        
        Args:
            years: 分析最近N年数据
            
        Returns:
            分析结果字典
        """
        # 获取数据
        success = self.fetch_multi_year_data(years)
        if not success:
            return {"error": "获取数据失败"}
        
        # 计算趋势指标
        metrics = self.calculate_trend_metrics()
        
        # 识别风险信号
        risks = self.identify_risk_signals(metrics)
        
        # 生成报告
        report = self.generate_trend_report(metrics, risks)
        
        return {
            "stock_code": self.stock_code,
            "metrics": metrics,
            "risks": risks,
            "report": report,
            "risk_count": len(risks),
            "high_risk_count": sum(1 for r in risks if r.get("severity") == "高"),
        }


def analyze_stock_trend(stock_code: str, years: int = 5) -> Dict:
    """
    分析股票财务趋势
    
    Args:
        stock_code: 股票代码
        years: 分析年数
        
    Returns:
        分析结果
    """
    analyzer = FinancialTrendAnalyzer(stock_code)
    return analyzer.analyze(years)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 financial_trend.py <股票代码> [年数]")
        print("示例: python3 financial_trend.py 603529 5")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    result = analyze_stock_trend(stock_code, years)
    
    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(result["report"])
    
    # 保存结果
    output_dir = f"/root/.openclaw/workspace/investment/trend"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/{stock_code}_trend.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 分析结果已保存: {output_file}")
