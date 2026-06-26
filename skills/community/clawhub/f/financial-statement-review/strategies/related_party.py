"""
关联交易审查策略

审查关联方交易的合规性，特别关注：
- 关联方借款/贷款（资本弱化、利息扣除限制）
- 关联方资金占用
- 通过利息变相逃避税费
- 关联交易定价公允性
- 关联方担保
- 向关联方发放福利

法规依据：
- 《企业所得税法》第六章 特别纳税调整
- 《特别纳税调整实施办法（试行）》（国税发〔2009〕2号）
- 《关于完善关联申报和同期资料管理有关事项的公告》（2016年第42号）
- 《资本弱化税收管理》（财税〔2008〕121号）
"""
from typing import Dict, List, Any, Optional
from .base_strategy import BaseStrategy, StrategyResult


class RelatedPartyTransactionStrategy(BaseStrategy):
    """
    关联交易审查策略
    
    审查要点：
    1. 关联方借款与资本弱化（债资比2:1或5:1）
    2. 关联方利息支出税前扣除限制
    3. 关联方资金占用与隐性利润分配
    4. 关联交易转让定价公允性
    5. 关联方担保的税务处理
    6. 向关联方发放福利的税务处理
    7. 同期资料准备义务
    """
    
    name = "related_party"
    description = "关联交易审查策略 - 审查关联方交易的税务合规性和转让定价公允性"
    version = "1.0.0"
    author = "财务审查系统"
    applicable_tax_types = ["企业所得税", "增值税"]
    required_data_fields = [
        "financial_statements",
        "related_party_transactions",  # 关联交易明细
        "company_info"
    ]
    
    # 资本弱化债资比标准
    DEBT_EQUITY_RATIO = 2.0  # 一般企业2:1
    DEBT_EQUITY_RATIO_FINANCIAL = 5.0  # 金融企业5:1
    
    # 关联方认定标准
    RP_THRESHOLD_OWNERSHIP = 0.25  # 股权控制25%
    RP_THRESHOLD_LOAN = 0.50  # 借贷资金占实收资本50%
    RP_THRESHOLD_GUARANTEE = 0.10  # 10%以上担保
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.safe_harbor_rate_min = self.config.get('safe_harbor_rate_min', 0.0435)  # 基准利率下限
        self.safe_harbor_rate_max = self.config.get('safe_harbor_rate_max', 0.15)   # 基准利率上限
    
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行关联交易审查
        
        Args:
            data: 包含:
                - financial_statements: 财务报表
                - related_party_transactions: 关联交易明细
                    - borrowings: 关联方借款
                    - lendings: 关联方贷款
                    - sales: 关联方销售
                    - purchases: 关联方采购
                    - guarantees: 关联方担保
                    - services: 关联方服务
                - company_info: 企业信息
                    - is_financial_enterprise: 是否金融企业
        """
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        rp_data = data.get('related_party_transactions', {})
        company_info = data.get('company_info', {})
        
        # 1. 资本弱化审查（关联方借款）
        self._check_capital_thinning(result, fs, rp_data, company_info)
        
        # 2. 关联方利息审查
        self._check_related_party_interest(result, fs, rp_data, company_info)
        
        # 3. 关联方资金占用审查
        self._check_fund_occupation(result, fs, rp_data)
        
        # 4. 关联交易定价审查
        self._check_transfer_pricing(result, fs, rp_data)
        
        # 5. 关联方担保审查
        self._check_related_guarantees(result, rp_data)
        
        # 6. 向关联方发放福利审查
        self._check_welfare_to_related_parties(result, rp_data)
        
        # 7. 同期资料准备义务审查
        self._check_documentation_obligations(result, fs, rp_data)
        
        return result
    
    def _check_capital_thinning(self, result: StrategyResult,
                                 fs: Dict, rp_data: Dict, company_info: Dict):
        """审查资本弱化（债资比）"""
        
        borrowings = rp_data.get('borrowings', [])
        if not borrowings:
            return
        
        equity = fs.get('owners_equity', 0)
        if equity <= 0:
            result.add_finding(
                finding_type='所有者权益异常',
                description='所有者权益为零或负数，无法计算债资比，资本弱化风险极高',
                severity='high',
                tax_type='企业所得税',
                regulation='财税〔2008〕121号'
            )
            return
        
        # 计算关联方债权性投资
        related_debt = sum(
            loan.get('principal', 0) for loan in borrowings
            if loan.get('is_related_party', True)
        )
        
        if related_debt <= 0:
            return
        
        # 计算债资比
        debt_equity_ratio = related_debt / equity
        
        # 确定标准债资比
        is_financial = company_info.get('is_financial_enterprise', False)
        standard_ratio = self.DEBT_EQUITY_RATIO_FINANCIAL if is_financial else self.DEBT_EQUITY_RATIO
        
        if debt_equity_ratio > standard_ratio:
            # 计算不得扣除的利息支出
            total_rp_interest = sum(
                loan.get('annual_interest', 0) for loan in borrowings
                if loan.get('is_related_party', True)
            )
            
            # 不得扣除利息 = 年度实际支付的全部关联方利息 × (1 - 标准比例/实际债资比例)
            non_deductible_interest = total_rp_interest * (1 - standard_ratio / debt_equity_ratio)
            tax_impact = non_deductible_interest * 0.25
            
            result.add_finding(
                finding_type='资本弱化-债资比超标',
                description=f'关联方债资比{debt_equity_ratio:.2f}:1超过标准{standard_ratio:.0f}:1，'
                           f'关联方债务{related_debt:,.2f}元，所有者权益{equity:,.2f}元，'
                           f'不得扣除利息支出约{non_deductible_interest:,.2f}元',
                severity='high',
                amount=tax_impact,
                tax_type='企业所得税',
                regulation='财税〔2008〕121号、国税发〔2009〕2号'
            )
            result.add_recommendation(
                f'应调增应纳税所得额{non_deductible_interest:,.2f}元，补缴企业所得税约{tax_impact:,.2f}元；'
                f'建议通过增资方式降低债资比，或准备资本弱化特殊事项文档'
            )
        
        result.details['debt_equity_ratio'] = debt_equity_ratio
        result.details['standard_ratio'] = standard_ratio
        result.details['related_party_debt'] = related_debt
    
    def _check_related_party_interest(self, result: StrategyResult,
                                       fs: Dict, rp_data: Dict, company_info: Dict):
        """审查关联方利息支出"""
        
        borrowings = rp_data.get('borrowings', [])
        if not borrowings:
            return
        
        for loan in borrowings:
            if not loan.get('is_related_party', False):
                continue
            
            lender = loan.get('lender_name', '关联方')
            principal = loan.get('principal', 0)
            annual_interest = loan.get('annual_interest', 0)
            interest_rate = loan.get('interest_rate', 0)
            
            if principal <= 0:
                continue
            
            # 计算实际利率
            actual_rate = annual_interest / principal if principal > 0 else 0
            
            # 检查利率是否异常
            if actual_rate > self.safe_harbor_rate_max:
                excess_rate = actual_rate - self.safe_harbor_rate_max
                excess_interest = principal * excess_rate
                tax_impact = excess_interest * 0.25
                
                result.add_finding(
                    finding_type='关联方借款利率过高',
                    description=f'向{lender}借款利率{actual_rate*100:.2f}%超过合理区间上限'
                               f'{self.safe_harbor_rate_max*100:.2f}%，'
                               f'超额利息{excess_interest:,.2f}元不得税前扣除',
                    severity='high',
                    amount=tax_impact,
                    tax_type='企业所得税',
                    regulation='企业所得税法第四十六条、实施条例第三十八条'
                )
                result.add_recommendation(
                    f'准备转让定价文档证明利率合理性，或按合理利率调整，'
                    f'预计调增应纳税所得额{excess_interest:,.2f}元'
                )
            
            elif actual_rate < self.safe_harbor_rate_min * 0.5:
                # 利率过低可能涉及隐性利润分配
                result.add_finding(
                    finding_type='关联方借款利率过低',
                    description=f'向{lender}借款利率{actual_rate*100:.2f}%显著低于市场水平，'
                               f'可能涉及隐性利润分配或转移定价',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='企业所得税法第六章-特别纳税调整'
                )
            
            # 检查非银行关联方借款利息凭证
            lender_type = loan.get('lender_type', '')
            if lender_type != '银行' and annual_interest > 0:
                has_invoice = loan.get('has_invoice', False)
                if not has_invoice:
                    result.add_finding(
                        finding_type='关联方利息支出凭证不合规',
                        description=f'向{lender}支付利息{annual_interest:,.2f}元未取得合法有效凭证',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='企业所得税法第八条、发票管理办法'
                    )
                
                # 非金融企业向非金融企业借款，需证明利率合理性
                has_rate_documentation = loan.get('has_rate_documentation', False)
                if not has_rate_documentation and actual_rate > 0:
                    result.add_finding(
                        finding_type='非金融机构借款利率合理性证明缺失',
                        description=f'向非金融企业{lender}借款，未提供利率合理性证明文件',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='企业所得税法实施条例第三十八条'
                    )
            
            # 检查股东出资是否到位（出资不到位情况下借款利息不得扣除）
            capital_paid = company_info.get('capital_paid', 0)
            capital_subscribed = company_info.get('capital_subscribed', 0)
            
            if capital_paid < capital_subscribed:
                unpaid_ratio = (capital_subscribed - capital_paid) / capital_subscribed
                non_deductible_portion = unpaid_ratio
                
                result.add_finding(
                    finding_type='股东出资不到位-借款利息受限',
                    description=f'股东认缴出资{capital_subscribed:,.2f}元，实缴{capital_paid:,.2f}元，'
                               f'未缴足比例{unpaid_ratio*100:.1f}%，'
                               f'对应比例借款利息不得税前扣除',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='国税函〔2009〕312号'
                )
    
    def _check_fund_occupation(self, result: StrategyResult,
                                fs: Dict, rp_data: Dict):
        """审查关联方资金占用"""
        
        # 检查其他应收款中的关联方往来
        other_receivables_rp = rp_data.get('other_receivables_related', [])
        
        for item in other_receivables_rp:
            counterparty = item.get('counterparty', '关联方')
            amount = item.get('amount', 0)
            duration_months = item.get('duration_months', 0)
            is_charging_interest = item.get('is_charging_interest', False)
            
            if amount <= 0:
                continue
            
            # 大额资金占用
            if amount > 10_000_000:  # 超过1000万
                result.add_finding(
                    finding_type='大额关联方资金占用',
                    description=f'关联方{counterparty}占用资金{amount:,.2f}元，'
                               f'账龄{duration_months}个月，'
                               f'{'已' if is_charging_interest else '未'}收取利息',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='税收征收管理法第三十六条'
                )
            
            # 长期资金占用（超过1年）
            if duration_months > 12:
                # 计算应计利息（按同期同类贷款利率）
                assumed_rate = 0.05  # 假设年利率5%
                due_interest = amount * assumed_rate * (duration_months / 12)
                
                if not is_charging_interest:
                    result.add_finding(
                        finding_type='关联方资金占用未收利息',
                        description=f'关联方{counterparty}长期占用资金{amount:,.2f}元'
                                   f'（{duration_months}个月）未收取利息，'
                                   f'按市场利率估算应收利息约{due_interest:,.2f}元，'
                                   f'可能涉及隐性利润分配',
                        severity='high',
                        amount=due_interest * 0.25,
                        tax_type='企业所得税',
                        regulation='企业所得税法第四十一条、特别纳税调整实施办法'
                    )
                    result.add_recommendation(
                        f'关联方资金占用应按独立交易原则收取利息，'
                        f'建议补计利息收入{due_interest:,.2f}元，'
                        f'或准备特殊事项文档证明无需调整'
                    )
        
        # 检查预付款项中的异常（可能存在变相资金占用）
        prepayments_rp = rp_data.get('prepayments_related', [])
        total_prepayment_rp = sum(p.get('amount', 0) for p in prepayments_rp)
        
        if total_prepayment_rp > 5_000_000:
            result.add_finding(
                finding_type='大额预付关联方款项',
                description=f'预付关联方款项合计{total_prepayment_rp:,.2f}元，'
                           f'需关注是否存在变相资金占用',
                severity='medium',
                tax_type='企业所得税',
                regulation='特别纳税调整实施办法'
            )
        
        # 检查是否存在通过关联方进行资金回流（虚增收入）
        receivables_rp = rp_data.get('accounts_receivable_related', [])
        total_ar_rp = sum(ar.get('amount', 0) for ar in receivables_rp)
        
        revenue = fs.get('revenue', 0)
        if revenue > 0:
            ar_rp_ratio = total_ar_rp / revenue
            if ar_rp_ratio > 0.20:  # 关联方应收占收入超过20%
                result.add_finding(
                    finding_type='关联方应收账款占比过高',
                    description=f'关联方应收账款{total_ar_rp:,.2f}元占收入比例{ar_rp_ratio*100:.1f}%，'
                               f'可能存在通过关联交易虚增收入或资金回流',
                    severity='high',
                    tax_type='增值税',
                    regulation='增值税暂行条例第七条'
                )
    
    def _check_transfer_pricing(self, result: StrategyResult,
                                 fs: Dict, rp_data: Dict):
        """审查关联交易定价公允性"""
        
        # 关联方销售
        sales = rp_data.get('sales', [])
        purchases = rp_data.get('purchases', [])
        
        # 分析关联方销售毛利率 vs 非关联方销售毛利率
        rp_sales_amount = sum(s.get('amount', 0) for s in sales)
        rp_sales_cost = sum(s.get('cost', 0) for s in sales)
        
        total_revenue = fs.get('revenue', 0)
        total_cost = fs.get('cost', 0)
        
        if rp_sales_amount > 0 and total_revenue > rp_sales_amount:
            # 计算关联方销售毛利率
            rp_gross_margin = (rp_sales_amount - rp_sales_cost) / rp_sales_amount if rp_sales_amount > 0 else 0
            
            # 计算非关联方销售毛利率
            non_rp_revenue = total_revenue - rp_sales_amount
            non_rp_cost = total_cost - rp_sales_cost
            non_rp_gross_margin = (non_rp_revenue - non_rp_cost) / non_rp_revenue if non_rp_revenue > 0 else 0
            
            # 毛利率差异分析
            if non_rp_gross_margin > 0:
                margin_diff = rp_gross_margin - non_rp_gross_margin
                
                if margin_diff < -0.10:  # 关联方销售毛利率低10个百分点以上
                    potential_transfer = rp_sales_amount * abs(margin_diff)
                    tax_impact = potential_transfer * 0.25
                    
                    result.add_finding(
                        finding_type='关联交易定价偏低',
                        description=f'关联方销售毛利率{rp_gross_margin*100:.1f}%显著低于'
                                   f'非关联方{non_rp_gross_margin*100:.1f}%，差异{margin_diff*100:.1f}个百分点，'
                                   f'可能存在转让定价不当，潜在利润转移{potential_transfer:,.2f}元',
                        severity='high',
                        amount=tax_impact,
                        tax_type='企业所得税',
                        regulation='企业所得税法第四十一条、特别纳税调整实施办法'
                    )
                    result.add_recommendation(
                        f'建议准备同期资料-本地文档，使用可比非受控价格法或交易净利润法'
                        f'证明定价合理性，或进行特别纳税调整补缴税款约{tax_impact:,.2f}元'
                    )
        
        # 关联方采购
        if purchases:
            rp_purchase_amount = sum(p.get('amount', 0) for p in purchases)
            
            # 检查采购价格是否高于市场价格
            for purchase in purchases:
                supplier = purchase.get('supplier', '关联方')
                unit_price = purchase.get('unit_price', 0)
                market_price = purchase.get('market_price', 0)
                quantity = purchase.get('quantity', 0)
                
                if market_price > 0 and unit_price > market_price * 1.10:  # 高于市价10%
                    excess_price = (unit_price - market_price) * quantity
                    tax_impact = excess_price * 0.25
                    
                    result.add_finding(
                        finding_type='关联交易采购定价偏高',
                        description=f'向{supplier}采购单价{unit_price:.2f}元高于市场价{market_price:.2f}元，'
                                   f'溢价{(unit_price/market_price-1)*100:.1f}%，涉及金额{excess_price:,.2f}元',
                        severity='high',
                        amount=tax_impact,
                        tax_type='企业所得税',
                        regulation='企业所得税法第四十一条'
                    )
        
        # 关联交易金额阈值检查（同期资料准备义务）
        total_rp_amount = rp_sales_amount + sum(p.get('amount', 0) for p in purchases)
        
        if total_rp_amount > 200_000_000:  # 2亿元
            result.add_finding(
                finding_type='关联交易金额达到同期资料准备标准',
                description=f'关联交易金额{total_rp_amount:,.2f}元超过2亿元，'
                           f'应准备本地文档',
                severity='medium',
                tax_type='企业所得税',
                regulation='国家税务总局公告2016年第42号'
            )
    
    def _check_related_guarantees(self, result: StrategyResult, rp_data: Dict):
        """审查关联方担保"""
        
        guarantees = rp_data.get('guarantees', [])
        if not guarantees:
            return
        
        for guarantee in guarantees:
            guaranteed_party = guarantee.get('guaranteed_party', '关联方')
            guarantee_amount = guarantee.get('amount', 0)
            guarantee_type = guarantee.get('type', '')  # 'provide' or 'receive'
            
            if guarantee_type == 'provide':  # 为关联方提供担保
                # 检查是否收取担保费
                has_guarantee_fee = guarantee.get('has_guarantee_fee', False)
                guarantee_fee = guarantee.get('guarantee_fee', 0)
                
                if not has_guarantee_fee and guarantee_amount > 10_000_000:
                    # 估算合理担保费（按担保金额0.5%-2%）
                    estimated_fee_rate = 0.01
                    estimated_annual_fee = guarantee_amount * estimated_fee_rate
                    
                    result.add_finding(
                        finding_type='关联方担保未收取担保费',
                        description=f'为{guaranteed_party}提供担保{guarantee_amount:,.2f}元'
                                   f'未收取担保费，按市场费率{estimated_fee_rate*100:.1f}%估算，'
                                   f'年应收担保费约{estimated_annual_fee:,.2f}元',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='企业所得税法第四十一条'
                    )
                    result.add_recommendation(
                        f'为关联方提供担保应按独立交易原则收取担保费，'
                        f'建议补计担保费收入或准备转让定价文档'
                    )
                
                # 检查担保是否实际履行（形成损失）
                if guarantee.get('was_performed', False):
                    loss_amount = guarantee.get('loss_amount', 0)
                    if loss_amount > 0:
                        result.add_finding(
                            finding_type='关联方担保实际履行形成损失',
                            description=f'为{guaranteed_party}提供的担保已实际履行，'
                                       f'形成损失{loss_amount:,.2f}元，'
                                       f'需关注税前扣除合规性',
                            severity='high',
                            tax_type='企业所得税',
                            regulation='企业资产损失所得税税前扣除管理办法'
                        )
    
    def _check_welfare_to_related_parties(self, result: StrategyResult, rp_data: Dict):
        """审查向关联方发放福利"""
        
        welfare_transactions = rp_data.get('welfare_to_related_parties', [])
        if not welfare_transactions:
            return
        
        for trans in welfare_transactions:
            recipient = trans.get('recipient', '关联方')
            welfare_type = trans.get('type', '')  # 'goods', 'services', 'discount'
            value = trans.get('value', 0)
            is_charged = trans.get('is_charged', False)
            
            if value <= 0:
                continue
            
            if not is_charged:
                result.add_finding(
                    finding_type='向关联方提供福利未收费',
                    description=f'向{recipient}提供{welfare_type}价值{value:,.2f}元未收取费用，'
                               f'应视同销售处理',
                    severity='high',
                    amount=value * 0.13 + value * 0.25,  # 增值税+企业所得税
                    tax_type='增值税/企业所得税',
                    regulation='增值税暂行条例实施细则第四条、企业所得税法实施条例第二十五条'
                )
                result.add_recommendation(
                    f'向关联方无偿提供货物、服务应视同销售缴纳增值税和企业所得税，'
                    f'建议补提销项税额并按公允价值确认收入'
                )
            else:
                # 检查收费是否公允
                charged_amount = trans.get('charged_amount', 0)
                if charged_amount < value * 0.9:  # 低于公允价值90%
                    shortfall = value - charged_amount
                    result.add_finding(
                        finding_type='向关联方提供福利定价偏低',
                        description=f'向{recipient}提供{welfare_type}公允价值{value:,.2f}元，'
                                   f'仅收费{charged_amount:,.2f}元，差额{shortfall:,.2f}元',
                        severity='medium',
                        amount=shortfall * 0.13 + shortfall * 0.25,
                        tax_type='增值税/企业所得税',
                        regulation='增值税暂行条例第七条、企业所得税法第四十一条'
                    )
    
    def _check_documentation_obligations(self, result: StrategyResult,
                                          fs: Dict, rp_data: Dict):
        """审查同期资料准备义务"""
        
        # 判断是否达到同期资料准备门槛
        rp_sales = sum(s.get('amount', 0) for s in rp_data.get('sales', []))
        rp_purchases = sum(p.get('amount', 0) for p in rp_data.get('purchases', []))
        total_rp = rp_sales + rp_purchases
        
        revenue = fs.get('revenue', 0)
        total_assets = fs.get('total_assets', 0)
        
        documentation_required = []
        
        # 本地文档门槛
        if total_rp > 200_000_000:  # 2亿元
            documentation_required.append('本地文档（关联交易超2亿元）')
        
        # 主体文档门槛
        if revenue > 5_500_000_000:  # 55亿元
            documentation_required.append('主体文档（年度营收超55亿元）')
        
        # 特殊事项文档
        # 成本分摊协议
        if rp_data.get('cost_sharing_agreements', []):
            documentation_required.append('特殊事项文档-成本分摊协议')
        
        # 资本弱化
        borrowings = rp_data.get('borrowings', [])
        related_debt = sum(
            loan.get('principal', 0) for loan in borrowings
            if loan.get('is_related_party', True)
        )
        equity = fs.get('owners_equity', 0)
        if equity > 0 and related_debt / equity > self.DEBT_EQUITY_RATIO:
            documentation_required.append('特殊事项文档-资本弱化')
        
        if documentation_required:
            result.add_finding(
                finding_type='同期资料准备义务',
                description=f'企业达到同期资料准备标准，需准备：{"、".join(documentation_required)}',
                severity='medium',
                tax_type='企业所得税',
                regulation='国家税务总局公告2016年第42号'
            )
            result.add_recommendation(
                '应在关联交易发生年度次年6月30日前准备完毕同期资料，'
                '并自税务机关要求之日起30日内提供'
            )


__all__ = ['RelatedPartyTransactionStrategy']
