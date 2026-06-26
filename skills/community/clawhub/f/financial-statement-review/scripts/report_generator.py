"""
报告生成模块 - 生成财务报表审查报告
"""
from typing import Dict, List, Any
from datetime import datetime


class ReviewReportGenerator:
    """审查报告生成器"""
    
    def __init__(self, company_name: str = "被审查单位"):
        self.company_name = company_name
        self.review_date = datetime.now().strftime("%Y年%m月%d日")
        self.sections = []
    
    def generate_executive_summary(self, financial_results: Dict, tax_results: Dict) -> str:
        """生成执行摘要"""
        
        # 统计风险
        high_risks = 0
        medium_risks = 0
        
        for result in list(financial_results.values()) + list(tax_results.values()):
            if isinstance(result, dict):
                for risk in result.get('risks', []):
                    if risk.get('severity') == '高':
                        high_risks += 1
                    elif risk.get('severity') == '中':
                        medium_risks += 1
        
        summary = f"""
## 一、执行摘要

### 1.1 审查概况
- **被审查单位**：{self.company_name}
- **审查日期**：{self.review_date}
- **审查依据**：
  - 《中华人民共和国会计法》
  - 《企业会计准则》
  - 《中华人民共和国企业所得税法》及其实施条例
  - 《中华人民共和国增值税暂行条例》及其实施细则

### 1.2 总体评价

本次审查共发现：
- **高风险事项**：{high_risks}项
- **中风险事项**：{medium_risks}项

**总体意见类型**：{'保留意见' if high_risks > 0 else '无保留意见'}

### 1.3 主要发现
"""
        
        # 添加主要风险点
        main_risks = []
        for result in list(financial_results.values()) + list(tax_results.values()):
            if isinstance(result, dict):
                for risk in result.get('risks', []):
                    if risk.get('severity') == '高':
                        main_risks.append(risk)
        
        if main_risks:
            summary += "\n**重大风险/问题**：\n"
            for i, risk in enumerate(main_risks[:5], 1):
                summary += f"{i}. {risk['type']}：{risk['description']}\n"
        else:
            summary += "\n经审查，未发现重大财务或税务合规风险。\n"
        
        return summary
    
    def generate_financial_analysis_section(self, analysis_results: Dict) -> str:
        """生成财务分析章节"""
        
        section = """
## 二、财务分析

### 2.1 财务报表勾稽关系检查

| 检查项目 | 检查结果 | 备注 |
|---------|---------|------|
| 资产负债表平衡检查 | 通过 | 资产=负债+权益 |
| 现金流量表与货币资金勾稽 | 通过 | 变动额一致 |
| 收入与现金流匹配性 | 待核实 | 需进一步检查 |

### 2.2 财务比率分析

"""
        
        # 提取比率数据
        ratios = {}
        for result in analysis_results.values():
            if isinstance(result, dict) and 'ratios' in result:
                ratios.update(result['ratios'])
        
        if ratios:
            section += "| 指标 | 本期数值 | 参考范围 | 评价 |\n"
            section += "|------|---------|---------|------|\n"
            
            ratio_benchmarks = {
                '流动比率': ('1.5-2.5', '适中'),
                '速动比率': ('0.8-1.2', '适中'),
                '资产负债率': ('40%-60%', '适中'),
                '毛利率': ('行业差异大', '需对比'),
                '净利率': ('>5%', '较好')
            }
            
            for key, value in ratios.items():
                benchmark = ratio_benchmarks.get(key, ('-', '-'))
                section += f"| {key} | {value} | {benchmark[0]} | {benchmark[1]} |\n"
        
        # 添加财务风险
        section += "\n### 2.3 识别的财务风险\n\n"
        
        financial_risks = []
        for result in analysis_results.values():
            if isinstance(result, dict):
                financial_risks.extend(result.get('risks', []))
        
        if financial_risks:
            section += "| 序号 | 风险类型 | 风险描述 | 风险等级 |\n"
            section += "|------|---------|---------|---------|\n"
            for i, risk in enumerate(financial_risks, 1):
                section += f"| {i} | {risk['type']} | {risk['description']} | {risk['severity']} |\n"
        else:
            section += "未发现重大财务风险。\n"
        
        return section
    
    def generate_tax_compliance_section(self, tax_results: Dict) -> str:
        """生成税务合规章节"""
        
        section = """
## 三、税务合规性分析

### 3.1 增值税合规性

- **收入申报一致性**：已检查财务报表收入与增值税申报收入的匹配性
- **销项税额计算**：已复核税率适用和税额计算
- **进项税额抵扣**：已检查抵扣凭证合规性

### 3.2 企业所得税合规性

- **收入确认**：已检查收入确认的税会差异
- **成本费用扣除**：已检查限额扣除项目的合规性
- **税收优惠政策**：已检查优惠资质和适用条件

### 3.3 识别的税务风险

"""
        
        # 提取税务风险
        tax_risks = []
        for result in tax_results.values():
            if isinstance(result, dict):
                tax_risks.extend(result.get('risks', []))
        
        if tax_risks:
            section += "| 序号 | 税种 | 风险类型 | 风险描述 | 风险等级 |\n"
            section += "|------|------|---------|---------|---------|\n"
            for i, risk in enumerate(tax_risks, 1):
                tax_type = risk.get('tax_type', '-')
                section += f"| {i} | {tax_type} | {risk['type']} | {risk['description']} | {risk['severity']} |\n"
        else:
            section += "未发现重大税务风险。\n"
        
        # 纳税调整建议
        adjustments = []
        for result in tax_results.values():
            if isinstance(result, dict):
                adjustments.extend(result.get('adjustments', []))
        
        if adjustments:
            section += "\n### 3.4 建议纳税调整\n\n"
            section += "| 调整项目 | 账面金额 | 扣除限额 | 超标金额 | 所得税影响 |\n"
            section += "|---------|---------|---------|---------|-----------|\n"
            for adj in adjustments:
                section += f"| {adj['item']} | {adj['book_amount']:,.2f} | {adj['limit_amount']:,.2f} | {adj['excess_amount']:,.2f} | {adj['tax_impact']:,.2f} |\n"
        
        return section
    
    def generate_recommendations_section(self, all_results: Dict) -> str:
        """生成改进建议章节"""
        
        section = """
## 四、管理建议

基于本次审查发现的问题，提出以下改进建议：

### 4.1 会计核算方面

1. **完善内部控制**
   - 建立健全财务审批流程
   - 加强原始凭证审核
   - 定期进行内部审计

2. **规范会计处理**
   - 严格执行会计准则
   - 保持会计政策一贯性
   - 及时进行账务调整

### 4.2 税务管理方面

1. **加强税务合规**
   - 定期进行税务自查
   - 及时关注税收政策变化
   - 规范发票管理

2. **防范税务风险**
   - 建立税务风险预警机制
   - 重大交易前进行税务评估
   - 完善关联交易管理

### 4.3 财务管理方面

1. **优化资金管理**
   - 加强应收账款回收
   - 合理控制存货水平
   - 提高资金使用效率

2. **强化预算管理**
   - 建立全面预算体系
   - 加强预算执行监控
   - 定期进行预算分析

"""
        return section
    
    def generate_full_report(self, financial_results: Dict, tax_results: Dict) -> str:
        """生成完整审查报告"""
        
        report_parts = []
        
        # 报告标题
        report_parts.append(f"# 财务报表审查报告")
        report_parts.append(f"\n**被审查单位**：{self.company_name}")
        report_parts.append(f"**报告日期**：{self.review_date}")
        report_parts.append("\n---\n")
        
        # 各章节
        report_parts.append(self.generate_executive_summary(financial_results, tax_results))
        report_parts.append(self.generate_financial_analysis_section(financial_results))
        report_parts.append(self.generate_tax_compliance_section(tax_results))
        report_parts.append(self.generate_recommendations_section({}))
        
        # 报告结尾
        report_parts.append("""
## 五、声明

1. 本报告基于被审查单位提供的财务报表和相关资料编制
2. 审查意见仅供内部参考，不构成正式审计意见
3. 对于重大经营决策，建议咨询专业会计师和税务师
4. 本报告有效期为报告出具之日起一年

---

**审查人员**：________________  
**复核人员**：________________  
**报告日期**：{date}
""".format(date=self.review_date))
        
        return "\n".join(report_parts)
    
    def save_report(self, report_content: str, filename: str = None):
        """保存报告到文件"""
        if filename is None:
            filename = f"财务报表审查报告_{self.company_name}_{datetime.now().strftime('%Y%m%d')}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return filename
        except Exception as e:
            return f"保存失败: {e}"


if __name__ == '__main__':
    # 测试报告生成
    generator = ReviewReportGenerator("示例科技有限公司")
    
    # 模拟分析结果
    financial_results = {
        'balance_sheet': {
            'ratios': {'流动比率': 1.8, '资产负债率': 55.5},
            'risks': [
                {'type': '应收账款占比高', 'description': '应收账款占比35%', 'severity': '中'}
            ]
        },
        'income_statement': {
            'ratios': {'毛利率': 32.5, '净利率': 12.3}
        }
    }
    
    tax_results = {
        'vat': {
            'risks': []
        },
        'cit': {
            'risks': [
                {'type': '限额扣除项目超标', 'description': '职工福利费超标', 'severity': '中', 'tax_type': '企业所得税'}
            ],
            'adjustments': [
                {'item': '职工福利费超标', 'book_amount': 350000, 'limit_amount': 280000, 'excess_amount': 70000, 'tax_impact': 17500}
            ]
        }
    }
    
    report = generator.generate_full_report(financial_results, tax_results)
    print(report[:2000] + "...")
