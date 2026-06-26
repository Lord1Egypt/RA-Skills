#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务分析 CLI 工具 - 估值模块
作者：滚滚家族 🌪️
版本：1.0.0
"""

import sys
import os
from datetime import datetime

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠️ {text}{Colors.ENDC}")

def dcf_valuation(stock_code, revenue=10000, growth_rate=0.1, margin=0.2, tax_rate=0.25, 
                  capex=500, depreciation=300, nwc_change=200, wacc=0.08, terminal_growth=0.02, 
                  forecast_years=5):
    """
    DCF 估值模型
    
    参数:
        stock_code: 股票代码
        revenue: 最新年度收入（百万）
        growth_rate: 收入增长率
        margin: 净利润率
        tax_rate: 所得税率
        capex: 资本支出（百万）
        depreciation: 折旧摊销（百万）
        nwc_change: 营运资金变化（百万）
        wacc: 加权平均资本成本
        terminal_growth: 永续增长率
        forecast_years: 预测年限
    """
    print_header(f"💰 DCF 估值 - {stock_code}")
    
    print(f"{Colors.BOLD}【假设条件】{Colors.ENDC}")
    print(f"最新收入：¥{revenue}百万")
    print(f"收入增长率：{growth_rate*100:.1f}%")
    print(f"净利润率：{margin*100:.1f}%")
    print(f"所得税率：{tax_rate*100:.1f}%")
    print(f"WACC：{wacc*100:.1f}%")
    print(f"永续增长率：{terminal_growth*100:.1f}%")
    print(f"预测年限：{forecast_years}年\n")
    
    # 计算自由现金流
    print(f"{Colors.BOLD}【自由现金流预测】{Colors.ENDC}")
    print(f"{'年份':<10} {'收入':<12} {'净利润':<12} {'FCF':<12} {'折现因子':<12} {'现值':<12}")
    print(f"{'-' * 70}")
    
    fcfs = []
    present_values = []
    
    for year in range(1, forecast_years + 1):
        # 收入预测
        revenue_forecast = revenue * (1 + growth_rate) ** year
        
        # 净利润
        net_income = revenue_forecast * margin
        
        # 自由现金流 = 净利润 + 折旧 - 资本支出 - 营运资金变化
        fcf = net_income + depreciation - capex - nwc_change
        fcfs.append(fcf)
        
        # 折现因子
        discount_factor = 1 / (1 + wacc) ** year
        
        # 现值
        present_value = fcf * discount_factor
        present_values.append(present_value)
        
        print(f"{year:<10} {revenue_forecast:>10.0f} {net_income:>10.0f} {fcf:>10.0f} {discount_factor:>10.3f} {present_value:>10.0f}")
    
    # 计算终值
    terminal_fcf = fcfs[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    terminal_pv = terminal_value / (1 + wacc) ** forecast_years
    
    print(f"\n{Colors.BOLD}【终值计算】{Colors.ENDC}")
    print(f"终值：¥{terminal_value:,.0f}百万")
    print(f"终值现值：¥{terminal_pv:,.0f}百万")
    
    # 计算公司价值
    pv_forecast = sum(present_values)
    enterprise_value = pv_forecast + terminal_pv
    
    print(f"\n{Colors.BOLD}【估值结果】{Colors.ENDC}")
    print(f"预测期现金流现值：¥{pv_forecast:,.0f}百万")
    print(f"终值现值：¥{terminal_pv:,.0f}百万")
    print(f"{Colors.OKGREEN}公司价值：¥{enterprise_value:,.0f}百万{Colors.ENDC}")
    
    print_success("DCF 估值完成！")
    
    return enterprise_value

def relative_valuation(stock_code, pe=25, pb=5, ps=8, industry_pe=20, industry_pb=4, industry_ps=6):
    """
    相对估值
    
    参数:
        stock_code: 股票代码
        pe: 市盈率
        pb: 市净率
        ps: 市销率
        industry_pe: 行业平均 PE
        industry_pb: 行业平均 PB
        industry_ps: 行业平均 PS
    """
    print_header(f"💰 相对估值 - {stock_code}")
    
    print(f"{Colors.BOLD}【估值倍数】{Colors.ENDC}")
    print(f"{'指标':<15} {'公司':<12} {'行业平均':<12} {'溢价/折价':<12}")
    print(f"{'-' * 50}")
    
    # PE 对比
    pe_premium = (pe - industry_pe) / industry_pe * 100
    print(f"{'PE (市盈率)':<15} {pe:>10.1f}x {industry_pe:>10.1f}x {pe_premium:>+10.1f}%")
    
    # PB 对比
    pb_premium = (pb - industry_pb) / industry_pb * 100
    print(f"{'PB (市净率)':<15} {pb:>10.1f}x {industry_pb:>10.1f}x {pb_premium:>+10.1f}%")
    
    # PS 对比
    ps_premium = (ps - industry_ps) / industry_ps * 100
    print(f"{'PS (市销率)':<15} {ps:>10.1f}x {industry_ps:>10.1f}x {ps_premium:>+10.1f}%")
    
    # 综合评估
    avg_premium = (pe_premium + pb_premium + ps_premium) / 3
    
    print(f"\n{Colors.BOLD}【综合评估】{Colors.ENDC}")
    if avg_premium > 20:
        print(f"{Colors.WARNING}估值偏高：+{avg_premium:.1f}%{Colors.ENDC}")
        print("建议：谨慎买入或等待回调")
    elif avg_premium > 0:
        print(f"{Colors.OKBLUE}估值合理：+{avg_premium:.1f}%{Colors.ENDC}")
        print("建议：可以买入")
    elif avg_premium > -20:
        print(f"{Colors.OKGREEN}估值偏低：{avg_premium:.1f}%{Colors.ENDC}")
        print("建议：值得买入")
    else:
        print(f"{Colors.OKGREEN}估值极低：{avg_premium:.1f}%{Colors.ENDC}")
        print("建议：强烈买入")
    
    print_success("相对估值完成！")

def risk_assessment(stock_code, current_ratio=2.0, quick_ratio=1.5, debt_ratio=0.5, 
                    roe=0.15, revenue_growth=0.1, profit_growth=0.15):
    """
    风险评估
    
    参数:
        stock_code: 股票代码
        current_ratio: 流动比率
        quick_ratio: 速动比率
        debt_ratio: 资产负债率
        roe: 净资产收益率
        revenue_growth: 收入增长率
        profit_growth: 利润增长率
    """
    print_header(f"⚠️ 风险评估 - {stock_code}")
    
    print(f"{Colors.BOLD}【偿债能力】{Colors.ENDC}")
    print(f"流动比率：{current_ratio:.2f}", end="")
    if current_ratio > 2:
        print(f" {Colors.OKGREEN}✅ 良好{Colors.ENDC}")
    elif current_ratio > 1:
        print(f" {Colors.OKBLUE}⚠️ 一般{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 较差{Colors.ENDC}")
    
    print(f"速动比率：{quick_ratio:.2f}", end="")
    if quick_ratio > 1:
        print(f" {Colors.OKGREEN}✅ 良好{Colors.ENDC}")
    elif quick_ratio > 0.5:
        print(f" {Colors.OKBLUE}⚠️ 一般{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 较差{Colors.ENDC}")
    
    print(f"资产负债率：{debt_ratio*100:.1f}%", end="")
    if debt_ratio < 0.5:
        print(f" {Colors.OKGREEN}✅ 良好{Colors.ENDC}")
    elif debt_ratio < 0.7:
        print(f" {Colors.OKBLUE}⚠️ 一般{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 较高{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}【盈利能力】{Colors.ENDC}")
    print(f"ROE：{roe*100:.1f}%", end="")
    if roe > 0.15:
        print(f" {Colors.OKGREEN}✅ 强{Colors.ENDC}")
    elif roe > 0.1:
        print(f" {Colors.OKBLUE}⚠️ 中等{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 较弱{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}【成长能力】{Colors.ENDC}")
    print(f"收入增长率：{revenue_growth*100:.1f}%", end="")
    if revenue_growth > 0.2:
        print(f" {Colors.OKGREEN}✅ 高增长{Colors.ENDC}")
    elif revenue_growth > 0.1:
        print(f" {Colors.OKBLUE}⚠️ 中速增长{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 低速增长{Colors.ENDC}")
    
    print(f"利润增长率：{profit_growth*100:.1f}%", end="")
    if profit_growth > 0.2:
        print(f" {Colors.OKGREEN}✅ 高增长{Colors.ENDC}")
    elif profit_growth > 0.1:
        print(f" {Colors.OKBLUE}⚠️ 中速增长{Colors.ENDC}")
    else:
        print(f" {Colors.FAIL}❌ 低速增长{Colors.ENDC}")
    
    # 综合风险评分
    risk_score = 0
    
    # 偿债能力（40 分）
    if current_ratio > 2 and quick_ratio > 1 and debt_ratio < 0.5:
        risk_score += 40
    elif current_ratio > 1 and quick_ratio > 0.5 and debt_ratio < 0.7:
        risk_score += 25
    else:
        risk_score += 10
    
    # 盈利能力（30 分）
    if roe > 0.15:
        risk_score += 30
    elif roe > 0.1:
        risk_score += 20
    else:
        risk_score += 10
    
    # 成长能力（30 分）
    if revenue_growth > 0.2 and profit_growth > 0.2:
        risk_score += 30
    elif revenue_growth > 0.1 and profit_growth > 0.1:
        risk_score += 20
    else:
        risk_score += 10
    
    print(f"\n{Colors.BOLD}【综合风险评分】{Colors.ENDC}")
    print(f"总分：{risk_score}/100")
    
    if risk_score >= 80:
        print(f"{Colors.OKGREEN}⭐⭐⭐⭐⭐ 低风险{Colors.ENDC}")
    elif risk_score >= 60:
        print(f"{Colors.OKBLUE}⭐⭐⭐⭐☆ 中低风险{Colors.ENDC}")
    elif risk_score >= 40:
        print(f"{Colors.WARNING}⭐⭐⭐☆☆ 中等风险{Colors.ENDC}")
    elif risk_score >= 20:
        print(f"{Colors.FAIL}⭐⭐☆☆☆ 高风险{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}⭐☆☆☆☆ 极高风险{Colors.ENDC}")
    
    print_success("风险评估完成！")
    
    return risk_score

def main():
    """测试函数"""
    # DCF 估值测试
    dcf_valuation("600519.SH", 
                  revenue=100000, 
                  growth_rate=0.15, 
                  margin=0.5,
                  wacc=0.08,
                  terminal_growth=0.02)
    
    print("\n" + "="*60 + "\n")
    
    # 相对估值测试
    relative_valuation("600519.SH",
                       pe=35,
                       pb=12,
                       ps=15,
                       industry_pe=28,
                       industry_pb=8,
                       industry_ps=10)
    
    print("\n" + "="*60 + "\n")
    
    # 风险评估测试
    risk_assessment("600519.SH",
                    current_ratio=2.5,
                    quick_ratio=2.0,
                    debt_ratio=0.3,
                    roe=0.30,
                    revenue_growth=0.18,
                    profit_growth=0.20)

if __name__ == '__main__':
    main()
