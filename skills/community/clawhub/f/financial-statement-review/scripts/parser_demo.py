"""
文件解析模块演示脚本

演示如何使用文件解析模块识别和解析各种财务文件
"""
import os
import sys

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import FileParserManager, parse_file
from parsers.file_identifier import FileIdentifier, identify_file


def demo_file_identification():
    """演示文件识别功能"""
    
    print("=" * 70)
    print("演示1：文件识别")
    print("=" * 70)
    
    # 模拟一些文件路径
    test_files = [
        "/data/金蝶_资产负债表_2024.xlsx",
        "/data/用友_U8_利润表.xlsx",
        "/data/financial_report.pdf",
        "/data/科目余额表.csv",
        "/data/审计报告.docx",
        "/data/SAP_export.xlsx",
    ]
    
    print("\n文件识别结果：\n")
    print(f"{'文件路径':<40} {'文件类型':<10} {'软件类型':<10}")
    print("-" * 70)
    
    for file_path in test_files:
        file_type, software_type = identify_file(file_path)
        file_name = os.path.basename(file_path)
        print(f"{file_name:<40} {file_type.name:<10} {software_type.name:<10}")
    
    print("\n支持的文件类型：")
    for ft in ['EXCEL', 'WORD', 'PDF', 'CSV']:
        print(f"  - {ft}")
    
    print("\n支持的财务软件：")
    for st in ['KINGDEE', 'UFIDA', 'SAP']:
        print(f"  - {st}")


def demo_parser_manager():
    """演示解析器管理器"""
    
    print("\n" + "=" * 70)
    print("演示2：解析器管理器")
    print("=" * 70)
    
    manager = FileParserManager()
    
    print("\n已注册的解析器：")
    print("-" * 70)
    
    for info in manager.list_parsers():
        print(f"\n  解析器: {info['name']}")
        print(f"  描述: {info['description']}")
        print(f"  支持扩展名: {', '.join(info['supported_extensions'])}")
        print(f"  支持软件: {', '.join(info['supported_software'])}")


def demo_mock_parsing():
    """演示解析过程（使用模拟数据）"""
    
    print("\n" + "=" * 70)
    print("演示3：财务数据结构")
    print("=" * 70)
    
    from parsers.base_parser import FinancialData
    
    # 创建模拟财务数据
    data = FinancialData(
        company_name="示例科技有限公司",
        tax_id="91110000XXXXXXXXXX",
        report_period="2024年度",
        source_file="financial_report.xlsx",
        source_software="金蝶"
    )
    
    # 填充资产负债表数据
    data.balance_sheet = {
        '货币资金': 50_000_000,
        '应收账款': 30_000_000,
        '存货': 20_000_000,
        '固定资产': 80_000_000,
        '资产总计': 200_000_000,
        '短期借款': 40_000_000,
        '应付账款': 25_000_000,
        '负债合计': 100_000_000,
        '所有者权益合计': 100_000_000,
    }
    
    # 填充利润表数据
    data.income_statement = {
        '营业收入': 150_000_000,
        '营业成本': 100_000_000,
        '税金及附加': 1_500_000,
        '销售费用': 10_000_000,
        '管理费用': 8_000_000,
        '财务费用': 2_000_000,
        '营业利润': 28_500_000,
        '利润总额': 30_000_000,
        '所得税费用': 7_500_000,
        '净利润': 22_500_000,
    }
    
    # 填充现金流量表数据
    data.cash_flow = {
        '销售商品收到的现金': 140_000_000,
        '经营活动现金流': 25_000_000,
        '投资活动现金流': -15_000_000,
        '筹资活动现金流': -5_000_000,
    }
    
    print("\n公司信息：")
    print(f"  公司名称: {data.company_name}")
    print(f"  纳税人识别号: {data.tax_id}")
    print(f"  报表期间: {data.report_period}")
    print(f"  数据来源: {data.source_software}")
    
    print("\n资产负债表关键指标：")
    print(f"  资产总计: {data.balance_sheet.get('资产总计', 0):,.0f} 元")
    print(f"  负债合计: {data.balance_sheet.get('负债合计', 0):,.0f} 元")
    print(f"  所有者权益: {data.balance_sheet.get('所有者权益合计', 0):,.0f} 元")
    
    # 计算资产负债率
    debt_ratio = data.get_ratio('负债合计', '资产总计')
    if debt_ratio:
        print(f"  资产负债率: {debt_ratio*100:.2f}%")
    
    print("\n利润表关键指标：")
    print(f"  营业收入: {data.income_statement.get('营业收入', 0):,.0f} 元")
    print(f"  营业成本: {data.income_statement.get('营业成本', 0):,.0f} 元")
    print(f"  净利润: {data.income_statement.get('净利润', 0):,.0f} 元")
    
    # 计算净利率
    net_margin = data.get_ratio('净利润', '营业收入')
    if net_margin:
        print(f"  净利率: {net_margin*100:.2f}%")
    
    print("\n现金流量表关键指标：")
    print(f"  经营活动现金流: {data.cash_flow.get('经营活动现金流', 0):,.0f} 元")
    print(f"  投资活动现金流: {data.cash_flow.get('投资活动现金流', 0):,.0f} 元")
    print(f"  筹资活动现金流: {data.cash_flow.get('筹资活动现金流', 0):,.0f} 元")
    
    return data


def demo_strategy_integration():
    """演示与策略库的集成"""
    
    print("\n" + "=" * 70)
    print("演示4：文件解析 + 策略审查集成")
    print("=" * 70)
    
    from parsers.base_parser import FinancialData
    from strategies import StrategyManager
    
    # 创建模拟财务数据（解析后的结果）
    data = FinancialData(
        company_name="测试公司",
        report_period="2024年度"
    )
    
    # 模拟资产负债表（有问题）
    data.balance_sheet = {
        '货币资金': 30_000_000,
        '应收账款': 80_000_000,  # 应收过高
        '存货': 60_000_000,
        '流动资产合计': 180_000_000,
        '资产总计': 300_000_000,
        '短期借款': 100_000_000,
        '流动负债合计': 150_000_000,
        '负债合计': 180_000_000,
        '所有者权益合计': 120_000_000,
    }
    
    # 模拟利润表
    data.income_statement = {
        '营业收入': 200_000_000,
        '营业成本': 140_000_000,
        '销售费用': 15_000_000,
        '管理费用': 10_000_000,
        '财务费用': 8_000_000,
        '营业利润': 27_000_000,
        '净利润': 20_000_000,
    }
    
    # 转换为策略审查所需格式
    review_data = {
        'financial_statements': {
            'revenue': data.income_statement.get('营业收入', 0),
            'cost': data.income_statement.get('营业成本', 0),
            'profit': data.income_statement.get('净利润', 0),
            'inventory': data.balance_sheet.get('存货', 0),
            'accounts_receivable': data.balance_sheet.get('应收账款', 0),
            'total_assets': data.balance_sheet.get('资产总计', 0),
            'total_liabilities': data.balance_sheet.get('负债合计', 0),
            'owners_equity': data.balance_sheet.get('所有者权益合计', 0),
        }
    }
    
    # 加载策略
    manager = StrategyManager()
    manager.load_all_strategies()
    
    print("\n执行财务审查策略...\n")
    
    # 执行成本操纵识别策略
    result = manager.execute_strategy('cost_manipulation', review_data)
    
    print(f"策略执行状态: {result.status.upper()}")
    print(f"发现问题: {len(result.findings)} 个")
    print()
    
    for finding in result.findings:
        severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(finding['severity'], '⚪')
        print(f"{severity_emoji} [{finding['severity'].upper()}] {finding['type']}")
        print(f"   {finding['description']}")
        print()


def demo_data_export():
    """演示数据导出"""
    
    print("\n" + "=" * 70)
    print("演示5：数据导出格式")
    print("=" * 70)
    
    from parsers.base_parser import FinancialData
    import json
    
    data = FinancialData(
        company_name="示例公司",
        report_period="2024年",
        balance_sheet={'资产总计': 100000000, '负债合计': 50000000},
        income_statement={'营业收入': 80000000, '净利润': 10000000},
    )
    
    # 转换为字典
    data_dict = data.to_dict()
    
    print("\nJSON格式输出示例：\n")
    print(json.dumps(data_dict, indent=2, ensure_ascii=False))


def print_usage_guide():
    """打印使用指南"""
    
    print("\n" + "=" * 70)
    print("使用指南")
    print("=" * 70)
    
    guide = """
文件解析模块使用示例：

1. 基本文件解析
   from parsers import parse_file
   
   result = parse_file('/path/to/financial_report.xlsx')
   
   if result.success:
       data = result.data
       print(f"营业收入: {data.income_statement.get('营业收入')}")
   else:
       print(f"解析失败: {result.errors}")

2. 批量解析
   from parsers import parse_files
   
   files = ['report1.xlsx', 'report2.pdf', 'report3.csv']
   results = parse_files(files)
   
   for result in results:
       if result.success:
           print(f"{result.file_path}: 解析成功")

3. 使用解析器管理器
   from parsers import FileParserManager
   
   manager = FileParserManager()
   
   # 扫描目录
   results = manager.scan_and_parse('/data/financial_reports')
   
   # 合并数据
   merged_data = manager.merge_financial_data(results)

4. 识别文件类型
   from parsers.file_identifier import identify_file
   
   file_type, software_type = identify_file('report.xlsx')
   print(f"文件类型: {file_type.name}")
   print(f"软件类型: {software_type.name}")

支持的文件格式：
  - Excel (.xlsx, .xls)
  - Word (.docx)
  - PDF (.pdf)
  - CSV (.csv)
  - XML (.xml) - 金蝶特定格式

支持的财务软件：
  - 金蝶 (KIS, K3, EAS, 云星空)
  - 用友 (U8, NC, YonSuite, 畅捷通)
  - SAP (部分格式)
  - 通用格式
"""
    print(guide)


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("财务报表文件解析模块演示")
    print("=" * 70)
    print("\n本演示展示如何识别和解析各种财务文件格式。\n")
    
    try:
        # 演示1：文件识别
        input("按回车键开始演示1：文件识别...")
        demo_file_identification()
        
        # 演示2：解析器管理器
        input("\n按回车键开始演示2：解析器管理器...")
        demo_parser_manager()
        
        # 演示3：财务数据结构
        input("\n按回车键开始演示3：财务数据结构...")
        demo_mock_parsing()
        
        # 演示4：策略集成
        input("\n按回车键开始演示4：文件解析 + 策略审查...")
        demo_strategy_integration()
        
        # 演示5：数据导出
        input("\n按回车键开始演示5：数据导出格式...")
        demo_data_export()
        
        # 使用指南
        input("\n按回车键显示使用指南...")
        print_usage_guide()
        
        print("\n" + "=" * 70)
        print("演示完成！")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n演示已中断。")
    except Exception as e:
        print(f"\n演示出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
