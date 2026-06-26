"""
财务报表分析模块 - 分析报表数据，识别异常和风险
"""
from typing import Dict, List, Tuple, Optional
import re


class FinancialStatementAnalyzer:
    """财务报表分析器"""
    
    def __init__(self):
        self.warnings = []
        self.risks = []
    
    def analyze_balance_sheet(self, data: Dict[str, float]) -> Dict[str, any]:
        """
        分析资产负债表
        
        Args:
            data: 资产负债表数据，包含各项科目金额
            
        Returns:
            分析结果字典
        """
        results = {
            'warnings': [],
            'risks': [],
            'ratios': {}
        }
        
        # 计算关键指标
        total_assets = data.get('资产总计', 0)
        total_liabilities = data.get('负债合计', 0)
        total_equity = data.get('所有者权益合计', 0)
        current_assets = data.get('流动资产合计', 0)
        current_liabilities = data.get('流动负债合计', 0)
        inventory = data.get('存货', 0)
        accounts_receivable = data.get('应收账款', 0)
        cash = data.get('货币资金', 0)
        
        # 验证勾稽关系
        if abs(total_assets - total_liabilities - total_equity) > 0.01:
            results['risks'].append({
                'type': '勾稽关系错误',
                'description': '资产总计 ≠ 负债合计 + 所有者权益合计',
                'severity': '高'
            })
        
        # 计算财务比率
        if current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            quick_ratio = (current_assets - inventory) / current_liabilities
            results['ratios']['流动比率'] = round(current_ratio, 2)
            results['ratios']['速动比率'] = round(quick_ratio, 2)
            
            if current_ratio < 1:
                results['risks'].append({
                    'type': '短期偿债风险',
                    'description': f'流动比率{current_ratio:.2f}低于1，可能存在短期偿债压力',
                    'severity': '高'
                })
            elif current_ratio > 3:
                results['warnings'].append({
                    'type': '资金利用效率',
                    'description': f'流动比率{current_ratio:.2f}过高，资金利用效率可能不足',
                    'severity': '低'
                })
        
        if total_assets > 0:
            debt_ratio = total_liabilities / total_assets
            results['ratios']['资产负债率'] = round(debt_ratio * 100, 2)
            
            if debt_ratio > 0.7:
                results['risks'].append({
                    'type': '财务杠杆过高',
                    'description': f'资产负债率{debt_ratio*100:.1f}%超过70%，财务风险较高',
                    'severity': '高'
                })
        
        # 异常指标检查
        if total_assets > 0:
            # 货币资金占比
            cash_ratio = cash / total_assets
            if cash_ratio > 0.5:
                results['warnings'].append({
                    'type': '资金闲置',
                    'description': f'货币资金占比{cash_ratio*100:.1f}%较高，可能存在资金闲置或受限',
                    'severity': '中'
                })
            
            # 应收账款占比
            ar_ratio = accounts_receivable / total_assets
            if ar_ratio > 0.3:
                results['warnings'].append({
                    'type': '应收账款占比高',
                    'description': f'应收账款占比{ar_ratio*100:.1f}%较高，关注回款风险',
                    'severity': '中'
                })
            
            # 存货占比
            inv_ratio = inventory / total_assets
            if inv_ratio > 0.3:
                results['warnings'].append({
                    'type': '存货占比高',
                    'description': f'存货占比{inv_ratio*100:.1f}%较高，关注跌价风险',
                    'severity': '中'
                })
        
        return results
    
    def analyze_income_statement(self, data: Dict[str, float], 
                                  prev_data: Optional[Dict[str, float]] = None) -> Dict[str, any]:
        """
        分析利润表
        
        Args:
            data: 当期利润表数据
            prev_data: 上期利润表数据（用于趋势分析）
            
        Returns:
            分析结果字典
        """
        results = {
            'warnings': [],
            'risks': [],
            'ratios': {},
            'trends': {}
        }
        
        revenue = data.get('营业收入', 0)
        cost = data.get('营业成本', 0)
        profit = data.get('净利润', 0)
        operating_profit = data.get('营业利润', 0)
        
        # 计算毛利率
        if revenue > 0:
            gross_margin = (revenue - cost) / revenue
            results['ratios']['毛利率'] = round(gross_margin * 100, 2)
            
            net_margin = profit / revenue
            results['ratios']['净利率'] = round(net_margin * 100, 2)
            
            if gross_margin < 0:
                results['risks'].append({
                    'type': '毛利为负',
                    'description': f'毛利率为{gross_margin*100:.1f}%，主营业务可能出现亏损',
                    'severity': '高'
                })
            elif gross_margin > 0.8:
                results['warnings'].append({
                    'type': '毛利率异常高',
                    'description': f'毛利率{gross_margin*100:.1f}%异常高，需核实收入成本确认是否准确',
                    'severity': '中'
                })
        
        # 利润结构分析
        if operating_profit != 0 and profit != 0:
            op_ratio = operating_profit / profit
            if op_ratio < 0.5 and profit > 0:
                results['warnings'].append({
                    'type': '利润结构异常',
                    'description': '营业利润占净利润比例低，非经常性损益占比高',
                    'severity': '中'
                })
        
        # 趋势分析
        if prev_data and prev_data.get('营业收入', 0) > 0:
            prev_revenue = prev_data['营业收入']
            revenue_growth = (revenue - prev_revenue) / prev_revenue
            results['trends']['收入增长率'] = round(revenue_growth * 100, 2)
            
            if revenue_growth > 0.5:
                results['warnings'].append({
                    'type': '收入增长异常',
                    'description': f'收入同比增长{revenue_growth*100:.1f}%，需核实增长真实性',
                    'severity': '中'
                })
            elif revenue_growth < -0.3:
                results['risks'].append({
                    'type': '收入大幅下滑',
                    'description': f'收入同比下降{abs(revenue_growth)*100:.1f}%，经营状况恶化',
                    'severity': '高'
                })
        
        return results
    
    def analyze_cash_flow(self, data: Dict[str, float],
                         income_data: Optional[Dict[str, float]] = None) -> Dict[str, any]:
        """
        分析现金流量表
        
        Args:
            data: 现金流量表数据
            income_data: 利润表数据（用于对比分析）
            
        Returns:
            分析结果字典
        """
        results = {
            'warnings': [],
            'risks': [],
            'analysis': {}
        }
        
        operating_cf = data.get('经营活动现金流量净额', 0)
        investing_cf = data.get('投资活动现金流量净额', 0)
        financing_cf = data.get('筹资活动现金流量净额', 0)
        
        # 现金流结构分析
        if operating_cf < 0:
            results['risks'].append({
                'type': '经营现金流为负',
                'description': '经营活动现金流量净额为负，主营业务盈利能力存疑',
                'severity': '高'
            })
        
        # 净利润与经营现金流对比
        if income_data:
            profit = income_data.get('净利润', 0)
            if profit != 0:
                cf_profit_ratio = operating_cf / profit
                results['analysis']['经营现金流/净利润'] = round(cf_profit_ratio, 2)
                
                if cf_profit_ratio < 0.5 and profit > 0:
                    results['risks'].append({
                        'type': '盈利质量差',
                        'description': f'经营现金流/净利润={cf_profit_ratio:.2f}，盈利质量较差，可能存在大量赊销',
                        'severity': '高'
                    })
        
        # 资金链风险
        if operating_cf < 0 and financing_cf < 0:
            results['risks'].append({
                'type': '资金链风险',
                'description': '经营和筹资活动现金流均为负，存在资金链断裂风险',
                'severity': '高'
            })
        
        return results
    
    def cross_statement_analysis(self, balance_sheet: Dict[str, float],
                                  income_statement: Dict[str, float],
                                  cash_flow: Dict[str, float]) -> Dict[str, any]:
        """
        跨报表勾稽关系分析
        
        Args:
            balance_sheet: 资产负债表数据
            income_statement: 利润表数据
            cash_flow: 现金流量表数据
            
        Returns:
            分析结果字典
        """
        results = {
            'warnings': [],
            'risks': [],
            'reconciliation': {}
        }
        
        # 收入与现金流勾稽
        revenue = income_statement.get('营业收入', 0)
        operating_cf_in = cash_flow.get('销售商品、提供劳务收到的现金', 0)
        
        if revenue > 0:
            cash_content = operating_cf_in / revenue
            results['reconciliation']['收入现金含量'] = round(cash_content * 100, 2)
            
            if cash_content < 0.8:
                results['warnings'].append({
                    'type': '收入现金含量低',
                    'description': f'销售收现率{cash_content*100:.1f}%较低，关注应收账款回收',
                    'severity': '中'
                })
        
        # 货币资金与现金流量表勾稽
        cash_begin = balance_sheet.get('货币资金_期初', 0)
        cash_end = balance_sheet.get('货币资金_期末', 0)
        cf_net = cash_flow.get('现金及现金等价物净增加额', 0)
        
        expected_change = cash_end - cash_begin
        if abs(expected_change - cf_net) > 0.01:
            results['risks'].append({
                'type': '货币资金勾稽异常',
                'description': f'货币资金变动({expected_change:.2f})与现金流量表净增加额({cf_net:.2f})不匹配',
                'severity': '高'
            })
        
        return results
    
    def generate_summary(self, all_results: Dict[str, any]) -> str:
        """
        生成分析摘要
        
        Args:
            all_results: 各报表分析结果汇总
            
        Returns:
            分析摘要文本
        """
        summary = []
        summary.append("=" * 60)
        summary.append("财务报表分析摘要")
        summary.append("=" * 60)
        
        # 统计风险数量
        high_risks = 0
        medium_risks = 0
        low_risks = 0
        
        for result in all_results.values():
            if isinstance(result, dict):
                for risk in result.get('risks', []):
                    if risk.get('severity') == '高':
                        high_risks += 1
                    elif risk.get('severity') == '中':
                        medium_risks += 1
                for warning in result.get('warnings', []):
                    if warning.get('severity') == '低':
                        low_risks += 1
        
        summary.append(f"\n风险统计：")
        summary.append(f"  - 高风险事项：{high_risks}项")
        summary.append(f"  - 中风险事项：{medium_risks}项")
        summary.append(f"  - 低风险事项（提示）：{low_risks}项")
        
        if high_risks > 0:
            summary.append("\n【高风险事项】")
            for name, result in all_results.items():
                if isinstance(result, dict):
                    for risk in result.get('risks', []):
                        if risk.get('severity') == '高':
                            summary.append(f"  [{name}] {risk['type']}: {risk['description']}")
        
        summary.append("\n" + "=" * 60)
        return "\n".join(summary)


if __name__ == '__main__':
    # 测试分析器
    analyzer = FinancialStatementAnalyzer()
    
    # 示例资产负债表数据
    bs_data = {
        '资产总计': 10000000,
        '负债合计': 6000000,
        '所有者权益合计': 4000000,
        '流动资产合计': 5000000,
        '流动负债合计': 4000000,
        '存货': 2000000,
        '应收账款': 2500000,
        '货币资金': 800000
    }
    
    result = analyzer.analyze_balance_sheet(bs_data)
    print("资产负债表分析结果：")
    print(f"  财务比率: {result['ratios']}")
    print(f"  风险: {len(result['risks'])}项")
    print(f"  提示: {len(result['warnings'])}项")
