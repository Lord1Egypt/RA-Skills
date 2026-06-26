#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理技能主入口
基于《园区运营项目客户服务标准指引》续扩租管理章节
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from scripts.contract_renewal import ContractRenewalManager

def main():
    """主函数"""
    manager = ContractRenewalManager()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        
        if task == 'check':
            # 检查预警
            warnings = manager.check_renewal_warnings()
            print("\n续租预警统计:")
            for level, warning_list in warnings.items():
                if warning_list:
                    print(f"\n{level}:")
                    for i, warning in enumerate(warning_list, 1):
                        print(f"  {i}. {warning['客户名称']} - {warning['房号']} - 距到期{warning['距到期月数']}个月")
                else:
                    print(f"\n{level}: 无")
        
        elif task == 'profile':
            # 分析企业画像
            if len(sys.argv) > 2:
                customer_id = sys.argv[2]
                profile = manager.analyze_enterprise_profile(customer_id)
                if profile:
                    print("\n企业画像分析结果:")
                    print(f"  客户ID: {profile['客户ID']}")
                    print(f"  客户名称: {profile['客户名称']}")
                    print(f"  房号: {profile['房号']}")
                    print(f"\n画像维度:")
                    print(f"  企业规模: {profile['企业规模']}")
                    print(f"  行业类型: {profile['行业类型']}")
                    print(f"  经营状况: {profile['经营状况']}")
                    print(f"  租金承受力: {profile['租金承受力']}")
                    print(f"  合作意愿: {profile['合作意愿']}")
                    print(f"  增值服务需求: {profile['增值服务需求']}")
                    print(f"\n综合评价: {profile['综合评价']}")
            else:
                print("用法: python main.py profile <客户ID>")
        
        elif task == 'plan':
            # 生成续租方案
            if len(sys.argv) > 2:
                customer_id = sys.argv[2]
                plan = manager.generate_renewal_plan(customer_id)
                if plan:
                    print(f"\n续租方案已生成:")
                    print(f"  计划ID: {plan['计划ID']}")
                    print(f"  客户名称: {plan['客户名称']}")
                    print(f"  房号: {plan['房号']}")
                    print(f"\n匹配方案: {plan['匹配方案']}")
                    print(f"  租金策略: {plan['租金策略']}")
                    print(f"  预计成功率: {plan['预计成功率']}%")
                    print(f"\n方案要点:")
                    for i, point in enumerate(plan['方案要点'], 1):
                        print(f"  {i}. {point}")
                    print(f"\n建议措施:")
                    for i, measure in enumerate(plan['建议措施'], 1):
                        print(f"  {i}. {measure}")
            else:
                print("用法: python main.py plan <客户ID>")
        
        elif task == 'track':
            # 跟踪进度
            print("跟踪续租进度功能（需传入参数）")
        
        elif task == 'report':
            # 生成报告
            if len(sys.argv) > 3:
                start_date = sys.argv[2]
                end_date = sys.argv[3]
                report = manager.generate_renewal_report(start_date, end_date)
                if report:
                    print(f"\n{report['报告名称']}:")
                    print(f"  总计划数: {report['总计划数']}")
                    print(f"  已完成数: {report['已完成数']}")
                    print(f"  成功率: {report['成功率']}%")
                    print(f"\n状态分布:")
                    for status, count in report['状态分布'].items():
                        print(f"  - {status}: {count}个")
                    print(f"\n方案分布:")
                    for plan_type, count in report['方案分布'].items():
                        print(f"  - {plan_type}: {count}个")
                    print(f"\n预警统计:")
                    for level, count in report['预警统计'].items():
                        print(f"  - {level}: {count}个")
            else:
                print("用法: python main.py report <开始日期> <结束日期>")
        
        elif task == 'monthly':
            # 执行每月任务
            result = manager.run_monthly_task()
            print("\n每月任务完成:")
            for action in result['操作']:
                print(f"  - {action}")
        
        else:
            print(f"未知任务: {task}")
            print_usage()
    
    else:
        # 默认检查预警
        manager.check_renewal_warnings()

def print_usage():
    """打印使用说明"""
    print("""
合同续租管理技能使用说明:

1. 检查续租预警:
   python main.py check

2. 分析企业画像:
   python main.py profile <客户ID>
   示例: python main.py profile C-001

3. 生成续租方案:
   python main.py plan <客户ID>
   示例: python main.py plan C-001

4. 跟踪续租进度:
   python main.py track <计划ID> <进度数据JSON>

5. 生成续租报告:
   python main.py report <开始日期> <结束日期>
   示例: python main.py report 2026-01-01 2026-12-31

6. 执行每月任务:
   python main.py monthly

预警等级说明:
- 🔴 红色预警: 合同到期前3个月 - 需立即启动续租谈判
- 🟡 黄色预警: 合同到期前4个月 - 需制定续租方案
- 🟢 绿色预警: 合同到期前6个月 - 需提前了解续租意向

企业画像维度:
- 企业规模: 大型/中型/小型/微型
- 行业类型: 制造业/科技研发/商务服务/商贸物流/其他
- 经营状况: 优秀/良好/一般/困难
- 租金承受力: 强/中/弱
- 合作意愿: 强/中/弱
- 增值服务需求: 高/中/低

续租方案类型:

A类-稳租方案:
  适用条件: 经营良好+合作意愿强+租金承受力强/中
  租金策略: 市场价或略有优惠
  方案要点: 续租优惠、优先扩租、C+服务、长期锁定(3-5年)

B类-保持方案:
  适用条件: 经营一般+合作意愿中+租金承受力中
  租金策略: 市场价
  方案要点: 维持租金、灵活租期(1-2年)、基础服务、适度扩租

C类-调整方案:
  适用条件: 经营困难+合作意愿弱+租金承受力弱
  租金策略: 协商调整或市场化退出
  方案要点: 租金调整、缩租换租、协助招商、提前解约

综合评价:
- 优质客户-重点稳租: 得分 ≥ 8 (大型企业+经营优秀+意愿强+承受力强)
- 稳定客户-保持关系: 得分 6-7 (中型企业+经营良好+意愿中+承受力中)
- 一般客户-适度关注: 得分 4-5 (小型企业+经营一般+意愿中+承受力中)
- 风险客户-重点关注: 得分 < 4 (微型企业+经营困难+意愿弱+承受力弱)

成功率预测:
基础成功率50% + 经营状况调整(±20) + 合作意愿调整(±15) + 租金承受力调整(±10) + 方案匹配度调整(±10)
""")

if __name__ == "__main__":
    main()