"""
税款比对分析策略

比对已纳税款统计表与财务报表数据，基于税法分析可能的少缴税款疑点。

此策略会进行以下比对分析：
1. 增值税：申报收入 vs 财务收入
2. 企业所得税：申报利润 vs 财务利润
3. 理论应纳税额计算与实缴税额比对
4. 税负率异常分析
"""
from typing import Dict, List, Any, Optional
from .base_strategy import BaseStrategy, StrategyResult


class TaxReconciliationStrategy(BaseStrategy):
    """
    税款比对分析策略
    
    通过比对财务报表数据和纳税申报数据，识别潜在的少缴税款风险。
    """
    
    name = "tax_reconciliation"
    description = "税款比对分析策略 - 比对已纳税款与财务报表，识别少缴税款疑点"
    version = "1.0.0"
    author = "财务审查系统"
    applicable_tax_types = ["增值税", "企业所得税"]
    required_data_fields = [
        "financial_statements",  # 财务报表数据
        "tax_returns"            # 纳税申报表数据
    ]
    
    # 默认税率配置
    default_vat_rate = 0.13  # 默认增值税率13%
    cit_rate = 0.25          # 企业所得税率25%
    small_profit_cit_rate = 0.20  # 小型微利企业优惠税率
    small_profit_effective_rate = 0.05  # 小型微利企业实际税负5%
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        # 从配置中读取参数，使用默认值
        self.vat_rate = self.config.get('vat_rate', self.default_vat_rate)
        self.industry_type = self.config.get('industry_type', 'general')  # general, manufacturing, service
        
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行税款比对分析
        
        Args:
            data: 包含以下字段:
                - financial_statements: 财务报表数据
                    - revenue: 营业收入
                    - cost: 营业成本
                    - profit: 利润总额
                    - salary: 工资薪金
                    - entertainment: 业务招待费
                    - welfare: 职工福利费
                    - advertising: 广告费
                    - donation: 公益性捐赠
                - tax_returns: 纳税申报数据
                    - vat_revenue: 增值税申报收入
                    - vat_paid: 实际缴纳增值税
                    - cit_income: 所得税申报收入
                    - cit_taxable_income: 应纳税所得额
                    - cit_paid: 实际缴纳企业所得税
                - company_info: 企业信息（可选）
                    - is_small_profit: 是否小型微利企业
                    
        Returns:
            StrategyResult: 分析结果
        """
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        tr = data.get('tax_returns', {})
        company_info = data.get('company_info', {})
        is_small_profit = company_info.get('is_small_profit', False)
        
        # ========== 1. 增值税比对分析 ==========
        self._analyze_vat_reconciliation(result, fs, tr)
        
        # ========== 2. 企业所得税比对分析 ==========
        self._analyze_cit_reconciliation(result, fs, tr, is_small_profit)
        
        # ========== 3. 税负率分析 ==========
        self._analyze_tax_burden_rate(result, fs, tr, is_small_profit)
        
        # ========== 4. 理论应纳税额测算 ==========
        self._calculate_theoretical_tax(result, fs, is_small_profit)
        
        return result
    
    def _analyze_vat_reconciliation(self, result: StrategyResult, 
                                     fs: Dict, tr: Dict):
        """分析增值税申报与财务数据的比对"""
        
        revenue = fs.get('revenue', 0)
        vat_revenue = tr.get('vat_revenue', 0)
        vat_paid = tr.get('vat_paid', 0)
        
        if revenue <= 0:
            return
        
        # 1.1 收入差异分析
        if vat_revenue > 0:
            revenue_diff = revenue - vat_revenue
            revenue_diff_pct = (revenue_diff / revenue) * 100 if revenue > 0 else 0
            
            # 财务收入大于增值税申报收入超过5%视为异常
            if revenue_diff_pct > 5:
                # 估算少缴增值税
                estimated_underpaid_vat = revenue_diff * self.vat_rate
                
                result.add_finding(
                    finding_type='增值税申报收入偏低',
                    description=f'财务报表收入({revenue:,.2f})高于增值税申报收入({vat_revenue:,.2f})，'
                               f'差异{revenue_diff_pct:.2f}%，可能少计增值税收入',
                    severity='high',
                    amount=estimated_underpaid_vat,
                    tax_type='增值税',
                    regulation='增值税暂行条例第十九条'
                )
                
                result.add_recommendation(
                    f'核实差异原因，如为未开票收入应及时申报，'
                    f'预计涉及少缴增值税约{estimated_underpaid_vat:,.2f}元'
                )
            
            # 1.2 销项税额比率分析
            if vat_paid > 0 and vat_revenue > 0:
                output_vat_ratio = vat_paid / vat_revenue
                
                # 销项税额/收入比率异常（偏离适用税率超过20%）
                expected_ratio = self.vat_rate
                if output_vat_ratio < expected_ratio * 0.8:
                    result.add_finding(
                        finding_type='销项税额比率异常偏低',
                        description=f'实际销项税负率{output_vat_ratio*100:.2f}%低于适用税率{expected_ratio*100:.1f}%，'
                                   f'可能存在应抵未抵进项或税率适用错误',
                        severity='medium',
                        tax_type='增值税',
                        regulation='增值税暂行条例第二条'
                    )
        
        # 1.3 无申报收入但有财务收入（严重异常）
        elif vat_revenue == 0 and revenue > 0:
            estimated_vat = revenue * self.vat_rate
            result.add_finding(
                finding_type='增值税零申报异常',
                description=f'财务报表收入{revenue:,.2f}元，但增值税申报收入为0，'
                           f'可能存在严重漏报，预计涉及增值税{estimated_vat:,.2f}元',
                severity='high',
                amount=estimated_vat,
                tax_type='增值税',
                regulation='税收征收管理法第六十三条'
            )
    
    def _analyze_cit_reconciliation(self, result: StrategyResult,
                                     fs: Dict, tr: Dict, is_small_profit: bool):
        """分析企业所得税申报与财务数据的比对"""
        
        profit = fs.get('profit', 0)
        cit_income = tr.get('cit_income', 0)
        cit_taxable_income = tr.get('cit_taxable_income', 0)
        cit_paid = tr.get('cit_paid', 0)
        
        if profit <= 0:
            return
        
        # 2.1 收入差异分析
        if cit_income > 0:
            income_diff = abs(profit - cit_income)  # 使用利润总额近似比较
            income_diff_pct = (income_diff / profit) * 100 if profit > 0 else 0
            
            if income_diff_pct > 10:
                result.add_finding(
                    finding_type='所得税申报收入差异',
                    description=f'财务利润总额({profit:,.2f})与所得税申报收入({cit_income:,.2f})'
                               f'差异{income_diff_pct:.2f}%，需核实差异原因',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='企业所得税法第五条'
                )
        
        # 2.2 应纳税所得额差异分析
        if cit_taxable_income > 0:
            # 正常情况应纳税所得额应略低于利润总额（纳税调整减少 > 纳税调整增加）
            # 或略高于利润总额（存在纳税调增项目）
            taxable_diff = cit_taxable_income - profit
            
            # 应纳税所得额大幅低于利润总额（可能过度调整）
            if taxable_diff < -profit * 0.3:  # 应纳税所得额比利润低30%以上
                result.add_finding(
                    finding_type='应纳税所得额异常偏低',
                    description=f'应纳税所得额({cit_taxable_income:,.2f})显著低于利润总额({profit:,.2f})，'
                               f'可能通过不当纳税调整减少应税所得',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='企业所得税法第十条、第十一条'
                )
        
        # 2.3 限额扣除项目测算
        self._check_deduction_limits(result, fs, is_small_profit)
        
        # 2.4 实际税负分析
        if cit_paid > 0 and profit > 0:
            actual_cit_rate = cit_paid / profit
            expected_rate = self.small_profit_effective_rate if is_small_profit else self.cit_rate
            
            # 实际税负显著低于预期
            if actual_cit_rate < expected_rate * 0.5:
                result.add_finding(
                    finding_type='企业所得税税负异常偏低',
                    description=f'实际所得税税负率{actual_cit_rate*100:.2f}%显著低于预期{expected_rate*100:.1f}%，'
                               f'可能存在少计收入或多计扣除',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='企业所得税法第二十八条'
                )
    
    def _check_deduction_limits(self, result: StrategyResult, fs: Dict, is_small_profit: bool):
        """检查限额扣除项目是否超标"""
        
        revenue = fs.get('revenue', 0)
        profit = fs.get('profit', 0)
        salary = fs.get('salary', 0)
        
        if salary <= 0:
            return
        
        adjustments = []
        
        # 职工福利费 14%
        welfare = fs.get('welfare', 0)
        welfare_limit = salary * 0.14
        if welfare > welfare_limit:
            excess = welfare - welfare_limit
            adjustments.append(('职工福利费', excess))
        
        # 职工教育经费 8%
        education = fs.get('education', 0)
        edu_limit = salary * 0.08
        if education > edu_limit:
            excess = education - edu_limit
            adjustments.append(('职工教育经费', excess))
        
        # 工会经费 2%
        union_fee = fs.get('union_fee', 0)
        union_limit = salary * 0.02
        if union_fee > union_limit:
            excess = union_fee - union_limit
            adjustments.append(('工会经费', excess))
        
        # 业务招待费 60%且不超过收入5‰
        entertainment = fs.get('entertainment', 0)
        if entertainment > 0 and revenue > 0:
            ent_limit = min(entertainment * 0.6, revenue * 0.005)
            if entertainment > ent_limit:
                excess = entertainment - ent_limit
                adjustments.append(('业务招待费', excess))
        
        # 广告费和业务宣传费 15%（一般企业）
        advertising = fs.get('advertising', 0)
        if advertising > 0 and revenue > 0:
            ad_limit = revenue * 0.15
            if advertising > ad_limit:
                excess = advertising - ad_limit
                adjustments.append(('广告费', excess))
        
        # 公益性捐赠 12%
        donation = fs.get('donation', 0)
        if donation > 0 and profit > 0:
            donation_limit = profit * 0.12
            if donation > donation_limit:
                excess = donation - donation_limit
                adjustments.append(('公益性捐赠', excess))
        
        # 汇总发现
        if adjustments:
            total_excess = sum(adj[1] for adj in adjustments)
            tax_rate = self.small_profit_effective_rate if is_small_profit else self.cit_rate
            estimated_tax_impact = total_excess * tax_rate
            
            adjustment_details = '，'.join([f"{name}超标{amount:,.2f}元" for name, amount in adjustments])
            
            result.add_finding(
                finding_type='限额扣除项目超标',
                description=f'发现{len(adjustments)}项扣除超标：{adjustment_details}，'
                           f'预计应调增应纳税所得额{total_excess:,.2f}元，'
                           f'涉及企业所得税{estimated_tax_impact:,.2f}元',
                severity='medium',
                amount=estimated_tax_impact,
                tax_type='企业所得税',
                regulation='企业所得税法实施条例第40-44条'
            )
            
            result.details['deduction_adjustments'] = adjustments
            result.details['total_adjustment'] = total_excess
    
    def _analyze_tax_burden_rate(self, result: StrategyResult,
                                  fs: Dict, tr: Dict, is_small_profit: bool):
        """分析税负率是否合理"""
        
        revenue = fs.get('revenue', 0)
        if revenue <= 0:
            return
        
        vat_paid = tr.get('vat_paid', 0)
        cit_paid = tr.get('cit_paid', 0)
        
        # 增值税税负率
        if vat_paid > 0:
            vat_burden_rate = vat_paid / revenue
            
            # 行业税负率参考（简化版，实际应分行业）
            industry_benchmark = {
                'general': 0.025,      # 一般行业约2.5%
                'manufacturing': 0.03,  # 制造业约3%
                'service': 0.02,        # 服务业约2%
                'retail': 0.015         # 零售业约1.5%
            }
            
            benchmark = industry_benchmark.get(self.industry_type, 0.025)
            
            if vat_burden_rate < benchmark * 0.5:
                result.add_finding(
                    finding_type='增值税税负率异常偏低',
                    description=f'增值税税负率{vat_burden_rate*100:.2f}%显著低于行业参考值{benchmark*100:.1f}%，'
                               f'可能存在进项抵扣异常或隐瞒收入',
                    severity='medium',
                    tax_type='增值税',
                    regulation='国家税务总局公告2019年第39号'
                )
        
        # 企业所得税贡献率
        if cit_paid > 0:
            cit_contribution_rate = cit_paid / revenue
            expected_contribution = 0.01 if is_small_profit else 0.015  # 小型微利约1%，一般企业约1.5%
            
            if cit_contribution_rate < expected_contribution * 0.3:
                result.add_finding(
                    finding_type='企业所得税贡献率异常偏低',
                    description=f'所得税贡献率{cit_contribution_rate*100:.2f}%显著偏低，'
                               f'可能存在虚增成本费用或少计收入',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='企业所得税法第六条'
                )
    
    def _calculate_theoretical_tax(self, result: StrategyResult,
                                    fs: Dict, is_small_profit: bool):
        """计算理论应纳税额，与实缴税额对比"""
        
        revenue = fs.get('revenue', 0)
        profit = fs.get('profit', 0)
        
        if revenue <= 0 or profit <= 0:
            return
        
        # 理论增值税（简化计算，不考虑进项）
        theoretical_vat = revenue * self.vat_rate
        
        # 理论企业所得税
        if is_small_profit:
            # 小型微利企业：应纳税所得额不超过300万部分减按25%计入，按20%税率
            theoretical_cit = profit * 0.25 * 0.20
        else:
            theoretical_cit = profit * self.cit_rate
        
        # 实际缴纳数据
        actual_vat = result.details.get('actual_vat_paid', 0)
        actual_cit = result.details.get('actual_cit_paid', 0)
        
        # 存储理论税额供后续分析
        result.details['theoretical_tax'] = {
            'vat': theoretical_vat,
            'cit': theoretical_cit,
            'total': theoretical_vat + theoretical_cit
        }
        
        result.add_recommendation(
            f'根据财务报表测算，理论增值税约{theoretical_vat:,.2f}元，'
            f'理论企业所得税约{theoretical_cit:,.2f}元，'
            f'建议与实际申报数据进行详细比对分析'
        )


# 导出策略类
__all__ = ['TaxReconciliationStrategy']
