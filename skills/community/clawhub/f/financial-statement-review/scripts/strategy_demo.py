"""
策略库使用演示脚本

演示如何使用策略库进行财务报表审查，特别是税款比对分析策略。
"""
import sys
import os

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies import StrategyManager


def demo_tax_reconciliation_strategy():
    """演示税款比对分析策略"""
    
    print("=" * 80)
    print("策略库演示：税款比对分析策略")
    print("=" * 80)
    
    # 1. 初始化策略管理器
    print("\n【步骤1】初始化策略管理器...")
    manager = StrategyManager()
    
    # 2. 加载策略（仅加载税款比对策略）
    print("\n【步骤2】加载策略...")
    
    # 配置策略参数
    config_map = {
        'tax_reconciliation': {
            'enabled': True,
            'priority': 10,
            'vat_rate': 0.13,  # 增值税率13%
            'industry_type': 'manufacturing'  # 制造业
        }
    }
    
    manager.load_all_strategies(config_map=config_map)
    
    # 显示加载的策略
    print("\n已加载的策略：")
    for info in manager.list_strategies():
        print(f"  - {info['name']}: {info['description']}")
        print(f"    适用税种: {', '.join(info['applicable_tax_types'])}")
    
    # 3. 准备审查数据（模拟有问题的企业数据）
    print("\n【步骤3】准备审查数据...")
    
    review_data = {
        # 财务报表数据
        'financial_statements': {
            'revenue': 100_000_000,        # 营业收入1亿元
            'cost': 70_000_000,            # 营业成本7000万
            'profit': 8_000_000,           # 利润总额800万
            'salary': 10_000_000,          # 工资薪金1000万
            'welfare': 1_600_000,          # 职工福利费160万（超标）
            'education': 900_000,          # 职工教育经费90万（超标）
            'entertainment': 600_000,      # 业务招待费60万（超标）
            'advertising': 16_000_000,     # 广告费1600万（超标）
            'donation': 1_200_000,         # 公益性捐赠120万
            'inventory': 25_000_000,       # 存货2500万
            'accounts_receivable': 30_000_000,  # 应收账款3000万
        },
        
        # 纳税申报数据（存在问题的申报）
        'tax_returns': {
            'vat_revenue': 92_000_000,     # 增值税申报收入9200万（少报800万）
            'vat_paid': 1_100_000,         # 已缴增值税110万（偏低）
            'cit_income': 100_000_000,     # 所得税申报收入1亿
            'cit_taxable_income': 5_000_000,  # 应纳税所得额500万（偏低）
            'cit_paid': 1_250_000,         # 已缴企业所得税125万
        },
        
        # 企业信息
        'company_info': {
            'is_small_profit': False,      # 非小型微利企业
            'industry': '制造业',
        }
    }
    
    print("  模拟企业数据：")
    print(f"    营业收入: {review_data['financial_statements']['revenue']:,.0f}元")
    print(f"    利润总额: {review_data['financial_statements']['profit']:,.0f}元")
    print(f"    增值税申报收入: {review_data['tax_returns']['vat_revenue']:,.0f}元")
    print(f"    已缴增值税: {review_data['tax_returns']['vat_paid']:,.0f}元")
    print(f"    已缴企业所得税: {review_data['tax_returns']['cit_paid']:,.0f}元")
    
    # 4. 执行税款比对策略
    print("\n【步骤4】执行税款比对分析策略...")
    result = manager.execute_strategy('tax_reconciliation', review_data)
    
    # 5. 输出结果
    print("\n【步骤5】分析结果：")
    print(f"\n策略执行状态: {result.status.upper()}")
    print(f"执行时间: {result.executed_at}")
    
    if result.findings:
        print(f"\n发现 {len(result.findings)} 个问题：")
        print("-" * 80)
        
        # 按严重程度排序
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_findings = sorted(result.findings, 
                                  key=lambda x: severity_order.get(x['severity'], 3))
        
        for i, finding in enumerate(sorted_findings, 1):
            severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(finding['severity'], '⚪')
            print(f"\n{i}. {severity_emoji} [{finding['severity'].upper()}] {finding['type']}")
            print(f"   税种: {finding.get('tax_type', '通用')}")
            print(f"   描述: {finding['description']}")
            if 'amount' in finding:
                print(f"   涉及金额: {finding['amount']:,.2f}元")
            if 'regulation' in finding:
                print(f"   法规依据: {finding['regulation']}")
    else:
        print("\n✅ 未发现明显问题")
    
    if result.recommendations:
        print(f"\n改进建议：")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"  {i}. {rec}")
    
    # 详细信息
    if result.details:
        print(f"\n详细信息：")
        if 'deduction_adjustments' in result.details:
            print("  限额扣除调整项目：")
            for item, amount in result.details['deduction_adjustments']:
                print(f"    - {item}: {amount:,.2f}元")
        if 'total_adjustment' in result.details:
            print(f"  应调增应纳税所得额合计: {result.details['total_adjustment']:,.2f}元")
    
    return result


def demo_multiple_strategies():
    """演示多个策略组合使用"""
    
    print("\n" + "=" * 80)
    print("策略库演示：多策略组合审查")
    print("=" * 80)
    
    # 初始化管理器
    manager = StrategyManager()
    
    # 加载所有策略
    print("\n【步骤1】加载所有策略...")
    manager.load_all_strategies()
    
    # 准备更完整的数据
    print("\n【步骤2】准备完整审查数据...")
    
    review_data = {
        'financial_statements': {
            'revenue': 100_000_000,
            'cost': 70_000_000,
            'profit': 8_000_000,
            'salary': 10_000_000,
            'welfare': 1_600_000,
            'entertainment': 600_000,
            'advertising': 16_000_000,
            'inventory': 25_000_000,
            'accounts_receivable': 30_000_000,
            'operating_cash_in': 65_000_000,  # 销售收现6500万
        },
        'tax_returns': {
            'vat_revenue': 95_000_000,
            'vat_paid': 1_235_000,
            'cit_taxable_income': 6_000_000,
            'cit_paid': 1_500_000,
        },
        'company_info': {
            'is_small_profit': False,
        },
        
        # 收入明细（用于收入确认策略）
        'revenue_details': {
            'monthly_revenue': [
                6_000_000, 6_500_000, 7_000_000, 7_500_000, 8_000_000, 8_500_000,
                8_000_000, 8_500_000, 9_000_000, 9_500_000, 12_000_000, 10_500_000
            ],
            'customer_concentration': {
                'top5_revenue': 60_000_000,
                'related_party_revenue': 35_000_000,
            }
        },
        
        # 历史数据（用于趋势分析）
        'historical_data': {
            'gross_margin': 0.28,  # 上期毛利率28%
            'inventory_days': 100,  # 上期存货周转100天
        },
    }
    
    # 执行所有策略
    print("\n【步骤3】执行所有策略...")
    results = manager.execute_all(review_data)
    
    # 生成汇总报告
    print("\n【步骤4】生成汇总报告...")
    summary = manager.generate_summary_report(results)
    print(summary)
    
    return results


def demo_strategy_registration():
    """演示动态注册策略"""
    
    print("\n" + "=" * 80)
    print("策略库演示：动态注册自定义策略")
    print("=" * 80)
    
    from strategies import BaseStrategy, StrategyResult
    
    # 定义自定义策略
    class CustomVATStrategy(BaseStrategy):
        name = "custom_vat_check"
        description = "自定义增值税检查策略 - 检查进销项匹配"
        applicable_tax_types = ["增值税"]
        required_data_fields = ["financial_statements"]
        
        def execute(self, data):
            result = StrategyResult(
                strategy_name=self.name,
                strategy_description=self.description,
                status='passed'
            )
            
            # 简单的检查逻辑
            fs = data.get('financial_statements', {})
            revenue = fs.get('revenue', 0)
            
            if revenue > 100_000_000:
                result.add_finding(
                    finding_type='收入规模风险',
                    description=f'年收入超过1亿元，应加强增值税管理',
                    severity='low',
                    tax_type='增值税'
                )
            
            return result
    
    # 初始化管理器并注册策略
    manager = StrategyManager()
    print("\n【步骤1】动态注册自定义策略...")
    manager.register_strategy(CustomVATStrategy)
    
    print("已注册策略：")
    for info in manager.list_strategies():
        print(f"  - {info['name']}: {info['description']}")
    
    # 执行策略
    print("\n【步骤2】执行自定义策略...")
    data = {'financial_statements': {'revenue': 120_000_000}}
    result = manager.execute_strategy('custom_vat_check', data)
    
    print(f"执行结果: {result.status}")
    for finding in result.findings:
        print(f"  - {finding['type']}: {finding['description']}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("财务报表审查策略库演示")
    print("=" * 80)
    print("\n本演示展示如何使用策略库进行专业的财务报表审查。")
    print("策略库采用模块化设计，支持灵活扩展。\n")
    
    try:
        # 演示1：税款比对策略
        input("按回车键开始演示1：税款比对分析策略...")
        demo_tax_reconciliation_strategy()
        
        # 演示2：多策略组合
        input("\n按回车键开始演示2：多策略组合审查...")
        demo_multiple_strategies()
        
        # 演示3：动态注册
        input("\n按回车键开始演示3：动态注册自定义策略...")
        demo_strategy_registration()
        
        print("\n" + "=" * 80)
        print("演示完成！")
        print("=" * 80)
        print("\n提示：")
        print("  - 策略库位于 strategies/ 目录")
        print("  - 可通过继承 BaseStrategy 添加新策略")
        print("  - 策略配置支持优先级、启用/禁用等参数")
        print("  - 策略结果支持风险分级和金额估算")
        
    except KeyboardInterrupt:
        print("\n\n演示已中断。")
    except Exception as e:
        print(f"\n演示出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
