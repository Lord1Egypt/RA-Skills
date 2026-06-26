#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务分析报告生成工具
根据解析的财务数据生成完整的分析报告
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """分析报告生成器"""
    
    def __init__(self, data: Dict):
        self.data = data
        self.company_name = data.get('company_info', {}).get('company_name', '未知公司')
        self.stock_code = data.get('company_info', {}).get('stock_code', '')
        self.report_period = data.get('company_info', {}).get('report_period', '')
        self.metrics = data.get('financial_metrics', {})
        
    def generate_report(self) -> str:
        """生成完整的分析报告"""
        report_sections = [
            self._generate_header(),
            self._generate_summary(),
            self._generate_profitability_analysis(),
            self._generate_solvency_analysis(),
            self._generate_operation_analysis(),
            self._generate_risk_assessment(),
            self._generate_conclusion(),
            self._generate_disclaimer(),
        ]
        
        return '\n\n'.join(report_sections)
    
    def _generate_header(self) -> str:
        """生成报告标题"""
        return f"""# 📊 {self.company_name} ({self.stock_code}) {self.report_period} 财务分析报告

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**数据来源**: 公司年度报告  
**免责声明**: 本报告仅供参考，不构成投资建议

---
"""
    
    def _generate_summary(self) -> str:
        """生成执行摘要"""
        summary = f"""## 一、执行摘要

### 1.1 公司概况
- **公司名称**: {self.company_name}
- **股票代码**: {self.stock_code}
- **报告期**: {self.report_period}年度

### 1.2 核心财务指标

"""
        
        # 添加关键指标表格
        summary += "| 指标类别 | 指标名称 | 数值 | 评价 |\n"
        summary += "|----------|----------|------|------|\n"
        
        # 盈利能力
        if '营业收入' in self.metrics:
            value = self._format_value(self.metrics['营业收入'])
            summary += f"| 盈利能力 | 营业收入 | {value} | - |\n"
        
        if '净利润' in self.metrics:
            value = self._format_value(self.metrics['净利润'])
            summary += f"| 盈利能力 | 净利润 | {value} | - |\n"
        
        if 'ROE' in self.metrics:
            value = self.metrics['ROE']['value']
            evaluation = self._evaluate_roe(value)
            summary += f"| 盈利能力 | ROE | {value}% | {evaluation} |\n"
        
        # 偿债能力
        if '资产负债率' in self.metrics:
            value = self.metrics['资产负债率']['value']
            evaluation = self._evaluate_debt_ratio(value)
            summary += f"| 偿债能力 | 资产负债率 | {value}% | {evaluation} |\n"
        
        if '流动比率' in self.metrics:
            value = self.metrics['流动比率']['value']
            evaluation = self._evaluate_current_ratio(value)
            summary += f"| 偿债能力 | 流动比率 | {value} | {evaluation} |\n"
        
        return summary
    
    def _generate_profitability_analysis(self) -> str:
        """生成盈利能力分析"""
        analysis = """## 二、盈利能力分析

### 2.1 核心指标

"""
        
        if 'ROE' in self.metrics:
            roe = self.metrics['ROE']['value']
            analysis += f"**ROE (净资产收益率)**: {roe}%\n\n"
            analysis += self._analyze_roe(roe)
        
        if '营业收入' in self.metrics and '净利润' in self.metrics:
            revenue = self.metrics['营业收入']['value']
            profit = self.metrics['净利润']['value']
            net_margin = (profit / revenue) * 100 if revenue > 0 else 0
            analysis += f"\n**净利率**: {net_margin:.2f}%\n\n"
            analysis += self._analyze_net_margin(net_margin)
        
        return analysis
    
    def _generate_solvency_analysis(self) -> str:
        """生成偿债能力分析"""
        analysis = """## 三、偿债能力分析

### 3.1 资本结构

"""
        
        if '资产负债率' in self.metrics:
            debt_ratio = self.metrics['资产负债率']['value']
            analysis += f"**资产负债率**: {debt_ratio}%\n\n"
            analysis += self._analyze_debt_ratio(debt_ratio)
        
        if '流动比率' in self.metrics:
            current_ratio = self.metrics['流动比率']['value']
            analysis += f"\n**流动比率**: {current_ratio}\n\n"
            analysis += self._analyze_current_ratio(current_ratio)
        
        return analysis
    
    def _generate_operation_analysis(self) -> str:
        """生成运营能力分析"""
        analysis = """## 四、运营能力分析

"""
        
        if '总资产周转率' in self.metrics:
            turnover = self.metrics['总资产周转率']['value']
            analysis += f"**总资产周转率**: {turnover}\n\n"
            analysis += "该指标反映企业资产运营效率。\n"
        else:
            analysis += "报告中未找到详细的运营能力指标数据。\n"
        
        return analysis
    
    def _generate_risk_assessment(self) -> str:
        """生成风险评估"""
        risks = []
        
        if '资产负债率' in self.metrics:
            debt_ratio = self.metrics['资产负债率']['value']
            if debt_ratio > 70:
                risks.append(f"- **财务杠杆较高**: 资产负债率达{debt_ratio}%，需关注偿债压力")
        
        if '流动比率' in self.metrics:
            current_ratio = self.metrics['流动比率']['value']
            if current_ratio < 1.5:
                risks.append(f"- **短期偿债能力**: 流动比率为{current_ratio}，低于理想水平")
        
        assessment = """## 五、风险提示

"""
        
        if risks:
            assessment += "### 5.1 财务风险\n\n"
            assessment += "\n".join(risks)
        else:
            assessment += "基于现有数据，未发现明显的财务风险信号。\n"
        
        assessment += """

### 5.2 其他风险
- 本报告基于历史财务数据，不反映未来表现
- 行业政策变化可能影响公司经营
- 市场波动风险
"""
        
        return assessment
    
    def _generate_conclusion(self) -> str:
        """生成综合评价"""
        return """## 六、综合评价

### 6.1 优势
- 公司财务数据完整，信息披露规范
- 具备基本的盈利能力

### 6.2 关注点
- 建议持续关注公司的资产负债结构
- 关注行业发展趋势对公司业绩的影响

### 6.3 免责声明
本报告仅供参考学习使用，不构成任何投资建议。投资者应独立做出投资决策，自行承担投资风险。
"""
    
    def _generate_disclaimer(self) -> str:
        """生成免责声明"""
        return """---

## ⚠️ 重要声明

1. **数据来源**: 本报告数据来源于公司公开披露的财务报告
2. **分析局限**: 自动提取可能存在误差，关键数据请以官方披露为准
3. **投资风险**: 股市有风险，投资需谨慎
4. **建议**: 建议投资者结合多方面信息，必要时咨询专业投资顾问

---

*报告生成时间: {}*  
*本报告由AI自动生成*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    def _format_value(self, metric: Dict) -> str:
        """格式化数值显示"""
        value = metric['value']
        unit = metric.get('unit', '')
        
        if unit == '亿元':
            return f"{value/100000000:.2f}亿元"
        elif unit == '万元':
            return f"{value/10000:.2f}万元"
        elif unit == '%':
            return f"{value}%"
        elif value > 100000000:
            return f"{value/100000000:.2f}亿元"
        elif value > 10000:
            return f"{value/10000:.2f}万元"
        else:
            return f"{value:.2f}"
    
    def _evaluate_roe(self, roe: float) -> str:
        """评价ROE水平"""
        if roe >= 20:
            return "优秀"
        elif roe >= 15:
            return "良好"
        elif roe >= 10:
            return "一般"
        else:
            return "较低"
    
    def _evaluate_debt_ratio(self, ratio: float) -> str:
        """评价资产负债率"""
        if ratio <= 40:
            return "保守"
        elif ratio <= 60:
            return "适中"
        elif ratio <= 70:
            return "偏高"
        else:
            return "较高(金融行业常见)"
    
    def _evaluate_current_ratio(self, ratio: float) -> str:
        """评价流动比率"""
        if ratio >= 2:
            return "优秀"
        elif ratio >= 1.5:
            return "良好"
        elif ratio >= 1:
            return "正常"
        else:
            return "偏低"
    
    def _analyze_roe(self, roe: float) -> str:
        """分析ROE"""
        if roe >= 15:
            return "ROE处于较好水平，说明公司为股东创造价值的能力较强。"
        elif roe >= 10:
            return "ROE处于一般水平，具备基本的盈利能力。"
        else:
            return "ROE相对较低，需关注公司盈利能力的持续性。"
    
    def _analyze_net_margin(self, margin: float) -> str:
        """分析净利率"""
        if margin >= 20:
            return "净利率较高，说明公司具备较强的定价能力和成本控制能力。"
        elif margin >= 10:
            return "净利率处于正常水平。"
        else:
            return "净利率相对较低，需关注成本控制和收入增长。"
    
    def _analyze_debt_ratio(self, ratio: float) -> str:
        """分析资产负债率"""
        if ratio <= 60:
            return "资产负债率处于合理区间，财务结构相对稳健。"
        elif ratio <= 70:
            return "资产负债率偏高，需关注偿债能力。"
        else:
            return "资产负债率较高，这在金融行业较为常见，但需关注流动性风险。"
    
    def _analyze_current_ratio(self, ratio: float) -> str:
        """分析流动比率"""
        if ratio >= 1.5:
            return "流动比率良好，短期偿债能力较强。"
        elif ratio >= 1:
            return "流动比率正常，具备基本的短期偿债能力。"
        else:
            return "流动比率偏低，需关注短期流动性风险。"


def generate_report_from_file(data_path: str, output_path: str = None) -> str:
    """
    从数据文件生成报告
    
    Args:
        data_path: 解析后的数据文件路径(.json)
        output_path: 报告输出路径(.md)
        
    Returns:
        str: 生成的报告内容
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    generator = ReportGenerator(data)
    report = generator.generate_report()
    
    # 保存报告
    if output_path is None:
        output_path = Path(data_path).stem + "_report.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <解析后的数据文件路径>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        print(f"正在生成报告: {data_file}")
        report_path = generate_report_from_file(data_file, output_file)
        
        print(f"[OK] 报告生成完成")
        print(f"  输出文件: {report_path}")
        
    except Exception as e:
        print(f"[ERROR] 报告生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
