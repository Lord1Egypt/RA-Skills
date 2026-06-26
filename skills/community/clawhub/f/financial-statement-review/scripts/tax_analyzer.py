"""
税务分析模块 - 分析税务合规性，识别税务风险
"""
from typing import Dict, List, Optional
from data_loader import load_tax_risk_indicators, get_high_risk_indicators


class TaxAnalyzer:
    """税务分析器"""
    
    def __init__(self):
        self.risks = []
        self.suggestions = []
    
    def analyze_vat_compliance(self, financial_data: Dict[str, float],
                                vat_return: Optional[Dict[str, float]] = None) -> Dict[str, any]:
        """
        分析增值税合规性
        
        Args:
            financial_data: 财务数据
            vat_return: 增值税申报表数据
            
        Returns:
            分析结果
        """
        results = {
            'risks': [],
            'suggestions': [],
            'checks': []
        }
        
        revenue = financial_data.get('营业收入', 0)
        
        # 收入与增值税申报差异
        if vat_return and revenue > 0:
            vat_revenue = vat_return.get('应税销售额', 0)
            if vat_revenue < revenue * 0.9:  # 允许一定误差
                diff_pct = (revenue - vat_revenue) / revenue * 100
                results['risks'].append({
                    'type': '增值税申报收入差异',
                    'description': f'财务报表收入({revenue:,.2f})与增值税申报收入({vat_revenue:,.2f})差异{diff_pct:.1f}%',
                    'severity': '高',
                    'tax_type': '增值税'
                })
            
            results['checks'].append({
                'item': '收入申报一致性',
                'status': '已检查',
                'result': '存在差异' if vat_revenue < revenue * 0.9 else '一致'
            })
        
        # 销项税额比率检查
        if vat_return:
            output_vat = vat_return.get('销项税额', 0)
            if revenue > 0 and output_vat > 0:
                vat_ratio = output_vat / revenue
                # 一般货物销售税率13%，服务6%，混合销售应在6%-13%之间
                if vat_ratio > 0.15:  # 超过最高税率
                    results['risks'].append({
                        'type': '销项税额异常',
                        'description': f'销项税额占收入比例{vat_ratio*100:.1f}%超过正常范围',
                        'severity': '中',
                        'tax_type': '增值税'
                    })
        
        return results
    
    def analyze_cit_compliance(self, financial_data: Dict[str, float],
                                cit_return: Optional[Dict[str, float]] = None) -> Dict[str, any]:
        """
        分析企业所得税合规性
        
        Args:
            financial_data: 财务数据
            cit_return: 企业所得税申报表数据
            
        Returns:
            分析结果
        """
        results = {
            'risks': [],
            'suggestions': [],
            'checks': [],
            'adjustments': []
        }
        
        profit = financial_data.get('利润总额', 0)
        revenue = financial_data.get('营业收入', 0)
        
        # 收入与所得税申报差异
        if cit_return and revenue > 0:
            cit_revenue = cit_return.get('营业收入', 0)
            if abs(cit_revenue - revenue) > revenue * 0.05:
                results['risks'].append({
                    'type': '所得税申报收入差异',
                    'description': f'财务报表收入与所得税申报收入差异超过5%',
                    'severity': '高',
                    'tax_type': '企业所得税'
                })
        
        # 限额扣除项目检查
        if financial_data.get('工资薪金', 0) > 0:
            salary = financial_data['工资薪金']
            
            # 职工福利费14%
            welfare = financial_data.get('职工福利费', 0)
            welfare_limit = salary * 0.14
            if welfare > welfare_limit:
                excess = welfare - welfare_limit
                results['adjustments'].append({
                    'item': '职工福利费超标',
                    'book_amount': welfare,
                    'limit_amount': welfare_limit,
                    'excess_amount': excess,
                    'tax_impact': excess * 0.25
                })
            
            # 职工教育经费8%
            education = financial_data.get('职工教育经费', 0)
            edu_limit = salary * 0.08
            if education > edu_limit:
                excess = education - edu_limit
                results['adjustments'].append({
                    'item': '职工教育经费超标',
                    'book_amount': education,
                    'limit_amount': edu_limit,
                    'excess_amount': excess,
                    'tax_impact': excess * 0.25
                })
            
            # 业务招待费60%且不超过收入5‰
            entertainment = financial_data.get('业务招待费', 0)
            ent_limit1 = entertainment * 0.6
            ent_limit2 = revenue * 0.005
            ent_limit = min(ent_limit1, ent_limit2)
            if entertainment > ent_limit:
                excess = entertainment - ent_limit
                results['adjustments'].append({
                    'item': '业务招待费超标',
                    'book_amount': entertainment,
                    'limit_amount': ent_limit,
                    'excess_amount': excess,
                    'tax_impact': excess * 0.25
                })
        
        # 广告费和业务宣传费15%
        if revenue > 0:
            advertising = financial_data.get('广告费和业务宣传费', 0)
            ad_limit = revenue * 0.15
            if advertising > ad_limit:
                excess = advertising - ad_limit
                results['adjustments'].append({
                    'item': '广告费超标',
                    'book_amount': advertising,
                    'limit_amount': ad_limit,
                    'excess_amount': excess,
                    'tax_impact': excess * 0.25
                })
        
        # 公益性捐赠12%
        if profit > 0:
            donation = financial_data.get('公益性捐赠支出', 0)
            donation_limit = profit * 0.12
            if donation > donation_limit:
                excess = donation - donation_limit
                results['adjustments'].append({
                    'item': '公益性捐赠超标',
                    'book_amount': donation,
                    'limit_amount': donation_limit,
                    'excess_amount': excess,
                    'tax_impact': excess * 0.25
                })
        
        # 汇总纳税调整影响
        if results['adjustments']:
            total_impact = sum(adj['tax_impact'] for adj in results['adjustments'])
            results['risks'].append({
                'type': '限额扣除项目超标',
                'description': f'发现{len(results["adjustments"])}项超标，预计增加所得税费用{total_impact:,.2f}元',
                'severity': '中',
                'tax_type': '企业所得税'
            })
        
        return results
    
    def analyze_related_party_transactions(self, transactions: List[Dict]) -> Dict[str, any]:
        """
        分析关联交易税务风险
        
        Args:
            transactions: 关联交易明细列表
            
        Returns:
            分析结果
        """
        results = {
            'risks': [],
            'suggestions': [],
            'summary': {}
        }
        
        total_rp_sales = 0
        total_rp_purchases = 0
        
        for trans in transactions:
            amount = trans.get('金额', 0)
            trans_type = trans.get('类型', '')
            
            if '销售' in trans_type:
                total_rp_sales += amount
            elif '采购' in trans_type:
                total_rp_purchases += amount
        
        results['summary'] = {
            '关联销售收入': total_rp_sales,
            '关联采购金额': total_rp_purchases,
            '关联交易笔数': len(transactions)
        }
        
        # 关联交易占比检查
        if total_rp_sales > 0 or total_rp_purchases > 0:
            results['risks'].append({
                'type': '关联交易风险',
                'description': f'存在关联交易（销售{total_rp_sales:,.2f}，采购{total_rp_purchases:,.2f}），需关注转让定价合规性',
                'severity': '中',
                'tax_type': '企业所得税'
            })
            
            results['suggestions'].append({
                'type': '转让定价文档',
                'content': '建议准备同期资料文档（本地文档、主体文档），证明关联交易定价公允性'
            })
        
        return results
    
    def generate_tax_risk_report(self, all_results: Dict[str, any]) -> str:
        """
        生成税务风险报告
        
        Args:
            all_results: 各税种分析结果汇总
            
        Returns:
            税务风险报告文本
        """
        report = []
        report.append("=" * 70)
        report.append("税务合规性审查报告")
        report.append("=" * 70)
        
        # 风险汇总
        all_risks = []
        for result in all_results.values():
            if isinstance(result, dict):
                all_risks.extend(result.get('risks', []))
        
        high_risks = [r for r in all_risks if r.get('severity') == '高']
        medium_risks = [r for r in all_risks if r.get('severity') == '中']
        
        report.append(f"\n一、风险概览")
        report.append(f"  发现高风险事项：{len(high_risks)}项")
        report.append(f"  发现中风险事项：{len(medium_risks)}项")
        
        if high_risks:
            report.append(f"\n二、高风险事项详述")
            for i, risk in enumerate(high_risks, 1):
                report.append(f"  {i}. [{risk['tax_type']}] {risk['type']}")
                report.append(f"     描述：{risk['description']}")
        
        if medium_risks:
            report.append(f"\n三、中风险事项")
            for i, risk in enumerate(medium_risks, 1):
                report.append(f"  {i}. [{risk['tax_type']}] {risk['type']}")
                report.append(f"     描述：{risk['description']}")
        
        # 纳税调整汇总
        all_adjustments = []
        for result in all_results.values():
            if isinstance(result, dict):
                all_adjustments.extend(result.get('adjustments', []))
        
        if all_adjustments:
            report.append(f"\n四、建议纳税调整")
            total_tax_impact = 0
            for adj in all_adjustments:
                report.append(f"  - {adj['item']}")
                report.append(f"    账面金额：{adj['book_amount']:,.2f}")
                report.append(f"    扣除限额：{adj['limit_amount']:,.2f}")
                report.append(f"    超标金额：{adj['excess_amount']:,.2f}")
                report.append(f"    所得税影响：{adj['tax_impact']:,.2f}")
                total_tax_impact += adj['tax_impact']
            report.append(f"\n  预计增加所得税费用合计：{total_tax_impact:,.2f}元")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


if __name__ == '__main__':
    # 测试税务分析器
    analyzer = TaxAnalyzer()
    
    # 示例财务数据
    financial_data = {
        '营业收入': 10000000,
        '利润总额': 2000000,
        '工资薪金': 2000000,
        '职工福利费': 350000,  # 超过14%限额
        '业务招待费': 200000
    }
    
    result = analyzer.analyze_cit_compliance(financial_data)
    print("企业所得税分析结果：")
    print(f"  发现调整事项：{len(result['adjustments'])}项")
    for adj in result['adjustments']:
        print(f"    - {adj['item']}: 超标{adj['excess_amount']:,.2f}元")
