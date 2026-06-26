"""
财务报表审查示例脚本
展示如何使用财务审查工具进行报表分析
"""
from statement_analyzer import FinancialStatementAnalyzer
from tax_analyzer import TaxAnalyzer
from report_generator import ReviewReportGenerator


def demo_financial_review():
    """演示财务报表审查流程"""
    
    print("=" * 70)
    print("财务报表审查演示")
    print("=" * 70)
    
    # 1. 准备示例财务数据
    print("\n【步骤1】准备财务数据...")
    
    # 资产负债表数据
    balance_sheet = {
        '资产总计': 50_000_000,
        '负债合计': 30_000_000,
        '所有者权益合计': 20_000_000,
        '流动资产合计': 25_000_000,
        '流动负债合计': 20_000_000,
        '存货': 8_000_000,
        '应收账款': 12_000_000,
        '货币资金': 3_000_000,
        '固定资产': 15_000_000
    }
    
    # 利润表数据
    income_statement = {
        '营业收入': 80_000_000,
        '营业成本': 56_000_000,
        '营业利润': 12_000_000,
        '利润总额': 12_500_000,
        '净利润': 9_375_000
    }
    
    # 现金流量表数据
    cash_flow = {
        '经营活动现金流量净额': 8_000_000,
        '投资活动现金流量净额': -5_000_000,
        '筹资活动现金流量净额': -2_000_000,
        '现金及现金等价物净增加额': 1_000_000,
        '销售商品、提供劳务收到的现金': 72_000_000
    }
    
    # 税务相关数据
    tax_data = {
        '营业收入': 80_000_000,
        '利润总额': 12_500_000,
        '工资薪金': 10_000_000,
        '职工福利费': 1_600_000,  # 16%，超过14%限额
        '职工教育经费': 900_000,   # 9%，超过8%限额
        '业务招待费': 600_000,    # 需要按60%且不超过收入5‰扣除
        '广告费和业务宣传费': 10_000_000,  # 12.5%，超过15%限额
        '公益性捐赠支出': 1_800_000  # 超过利润12%限额
    }
    
    # 2. 财务分析
    print("\n【步骤2】进行财务分析...")
    analyzer = FinancialStatementAnalyzer()
    
    bs_result = analyzer.analyze_balance_sheet(balance_sheet)
    print(f"  - 资产负债表分析完成，发现 {len(bs_result['risks'])} 个风险，{len(bs_result['warnings'])} 个提示")
    
    is_result = analyzer.analyze_income_statement(income_statement)
    print(f"  - 利润表分析完成，发现 {len(is_result['risks'])} 个风险，{len(is_result['warnings'])} 个提示")
    
    cf_result = analyzer.analyze_cash_flow(cash_flow, income_statement)
    print(f"  - 现金流量表分析完成，发现 {len(cf_result['risks'])} 个风险")
    
    cross_result = analyzer.cross_statement_analysis(balance_sheet, income_statement, cash_flow)
    print(f"  - 跨报表勾稽分析完成，发现 {len(cross_result['risks'])} 个风险")
    
    # 3. 税务分析
    print("\n【步骤3】进行税务合规分析...")
    tax_analyzer = TaxAnalyzer()
    
    cit_result = tax_analyzer.analyze_cit_compliance(tax_data)
    print(f"  - 企业所得税分析完成，发现 {len(cit_result['risks'])} 个风险")
    print(f"  - 建议纳税调整项目：{len(cit_result['adjustments'])} 项")
    
    # 4. 生成报告
    print("\n【步骤4】生成审查报告...")
    
    financial_results = {
        '资产负债表分析': bs_result,
        '利润表分析': is_result,
        '现金流量表分析': cf_result,
        '跨报表勾稽分析': cross_result
    }
    
    tax_results = {
        '企业所得税分析': cit_result
    }
    
    generator = ReviewReportGenerator("示例科技股份有限公司")
    report = generator.generate_full_report(financial_results, tax_results)
    
    # 保存报告
    filename = generator.save_report(report, "示例审查报告.md")
    print(f"  - 报告已保存至: {filename}")
    
    # 5. 输出摘要
    print("\n【审查摘要】")
    summary = analyzer.generate_summary(financial_results)
    print(summary)
    
    # 税务风险摘要
    print("\n【税务风险摘要】")
    tax_report = tax_analyzer.generate_tax_risk_report(tax_results)
    print(tax_report[:1500] + "...")
    
    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)


if __name__ == '__main__':
    demo_financial_review()
