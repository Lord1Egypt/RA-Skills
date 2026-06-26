#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业AI应用诊断工具 - 快速启动
"""

import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diagnosis_tool import EnterpriseAIDiagnosis

def run_quick_diagnosis():
    """运行快速诊断"""
    print("=" * 60)
    print("企业AI应用诊断工具")
    print("=" * 60)
    
    # 创建诊断实例
    diagnosis = EnterpriseAIDiagnosis()
    
    # 收集企业信息（示例数据）
    print("\n📋 正在收集企业信息...")
    enterprise_info = diagnosis.collect_enterprise_info({
        'company_name': input("企业名称：") or "示例公司",
        'industry': input("所属行业：") or "互联网",
        'scale': input("企业规模（如：50-100人）：") or "50-100人",
        'employees': int(input("员工人数：") or 80),
        'annual_revenue': int(input("年营收（万元）：") or 1000),
        'tech_level': input("当前技术水平（低/中等/高）：") or "中等",
        'budget': int(input("AI投入预算（元）：") or 10000),
    })
    
    # 分析业务流程
    print("\n🔍 正在分析业务流程...")
    processes = diagnosis.analyze_business_processes([
        {
            'name': '客服支持',
            'time_cost': 200,
            'labor_cost': 30000,
            'pain_level': '高',
            'repetitive': True,
            'customer_facing': True,
        },
        {
            'name': '内容营销',
            'time_cost': 100,
            'labor_cost': 20000,
            'pain_level': '中等',
            'repetitive': True,
            'creative': True,
        },
        {
            'name': '销售支持',
            'time_cost': 150,
            'labor_cost': 25000,
            'pain_level': '中等',
            'repetitive': False,
            'customer_facing': True,
        },
    ])
    
    # 计算ROI
    print("\n💰 正在计算ROI...")
    roi = diagnosis.calculate_roi(
        investment={
            'tools': 10000,
            'training': 5000,
            'time': 8000,
        },
        savings={
            'labor': 50000,
            'efficiency': 30000,
            'error_reduction': 10000,
        }
    )
    
    # 生成实施计划
    print("\n🚀 正在生成实施计划...")
    plan = diagnosis.generate_implementation_plan(processes, budget=10000)
    
    # 生成报告
    print("\n📄 正在生成诊断报告...")
    report = diagnosis.generate_report(enterprise_info, processes, roi, plan)
    
    # 保存报告
    filepath = diagnosis.save_report(report)
    
    print("\n" + "=" * 60)
    print("✅ 诊断完成！")
    print("=" * 60)
    print(f"\n📄 报告已保存：{filepath}")
    print(f"\n💰 ROI预测：")
    print(f"  - 总投入：{roi['total_investment']}元")
    print(f"  - 年化收益：{roi['annual_savings']}元")
    print(f"  - 投资回报率：{roi['roi_percentage']}%")
    print(f"  - 回报周期：{roi['payback_months']}个月")
    
    return filepath


if __name__ == '__main__':
    run_quick_diagnosis()
