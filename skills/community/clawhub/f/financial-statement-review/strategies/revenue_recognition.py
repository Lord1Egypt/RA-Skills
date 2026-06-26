"""
收入确认审查策略

基于 CAS 14 收入准则，审查收入确认的合规性，识别提前确认、延后确认或虚构收入的风险。
"""
from typing import Dict, Any
from .base_strategy import BaseStrategy, StrategyResult


class RevenueRecognitionStrategy(BaseStrategy):
    """
    收入确认审查策略
    
    审查要点：
    1. 收入确认时点是否符合五步法模型
    2. 是否存在提前确认收入
    3. 是否存在虚构收入（空转、关联交易）
    4. 完工百分比法应用是否恰当
    """
    
    name = "revenue_recognition"
    description = "收入确认审查策略 - 基于 CAS 14 审查收入确认合规性"
    version = "1.0.0"
    author = "财务审查系统"
    applicable_tax_types = ["增值税", "企业所得税"]
    required_data_fields = [
        "financial_statements",
        "revenue_details"
    ]
    
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行收入确认审查
        
        Args:
            data: 包含:
                - financial_statements: 财务报表
                - revenue_details: 收入明细
                    - monthly_revenue: 月度收入分布
                    - customer_concentration: 客户集中度
                    - related_party_revenue: 关联销售收入
                    - contract_terms: 主要合同条款
                    - completion_percentages: 完工百分比数据
        """
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        rd = data.get('revenue_details', {})
        
        revenue = fs.get('revenue', 0)
        
        # 1. 月度收入分布分析（识别年底突击确认）
        self._analyze_monthly_distribution(result, rd.get('monthly_revenue', []), revenue)
        
        # 2. 客户集中度分析（识别关联方交易）
        self._analyze_customer_concentration(result, rd.get('customer_concentration', {}), revenue)
        
        # 3. 收入与现金流匹配分析
        self._analyze_revenue_cash_flow_match(result, fs)
        
        # 4. 完工百分比法审查
        self._check_percentage_completion(result, rd.get('completion_data', {}))
        
        return result
    
    def _analyze_monthly_distribution(self, result: StrategyResult, 
                                       monthly_data: list, total_revenue: float):
        """分析月度收入分布，识别异常"""
        if not monthly_data or len(monthly_data) < 12:
            return
        
        # 计算Q4收入占比
        q4_revenue = sum(monthly_data[9:12])  # 10-12月
        q4_ratio = q4_revenue / total_revenue if total_revenue > 0 else 0
        
        # Q4占比超过40%视为异常
        if q4_ratio > 0.40:
            result.add_finding(
                finding_type='Q4收入占比过高',
                description=f'第四季度收入占比{q4_ratio*100:.1f}%，存在年底突击确认收入的风险',
                severity='medium',
                tax_type='企业所得税',
                regulation='CAS 14 - 收入确认时点'
            )
            result.add_recommendation('抽查第四季度大额收入合同，核实收入确认时点的合理性')
        
        # 12月收入占比分析
        dec_revenue = monthly_data[11] if len(monthly_data) > 11 else 0
        dec_ratio = dec_revenue / total_revenue if total_revenue > 0 else 0
        
        if dec_ratio > 0.20:
            result.add_finding(
                finding_type='12月收入占比过高',
                description=f'12月份收入占比{dec_ratio*100:.1f}%，需关注是否存在提前确认次年收入',
                severity='high',
                tax_type='企业所得税',
                regulation='CAS 14 - 收入确认时点'
            )
    
    def _analyze_customer_concentration(self, result: StrategyResult,
                                         customer_data: dict, total_revenue: float):
        """分析客户集中度"""
        if not customer_data:
            return
        
        # 前五大客户占比
        top5_revenue = customer_data.get('top5_revenue', 0)
        top5_ratio = top5_revenue / total_revenue if total_revenue > 0 else 0
        
        if top5_ratio > 0.50:
            result.add_finding(
                finding_type='客户集中度过高',
                description=f'前五大客户收入占比{top5_ratio*100:.1f}%，需关注主要客户稳定性和关联交易',
                severity='medium',
                tax_type='企业所得税',
                regulation='CAS 36 - 关联方披露'
            )
        
        # 关联方收入占比
        related_revenue = customer_data.get('related_party_revenue', 0)
        related_ratio = related_revenue / total_revenue if total_revenue > 0 else 0
        
        if related_ratio > 0.30:
            result.add_finding(
                finding_type='关联方收入占比高',
                description=f'关联方销售收入占比{related_ratio*100:.1f}%，需关注转让定价公允性',
                severity='high',
                tax_type='企业所得税',
                regulation='企业所得税法第六章 - 特别纳税调整'
            )
            result.add_recommendation('准备同期资料文档，证明关联交易定价公允性')
    
    def _analyze_revenue_cash_flow_match(self, result: StrategyResult, fs: dict):
        """分析收入与现金流的匹配性"""
        revenue = fs.get('revenue', 0)
        operating_cash_in = fs.get('operating_cash_in', 0)  # 销售商品收到的现金
        receivables = fs.get('accounts_receivable', 0)
        
        if revenue <= 0:
            return
        
        # 收入现金含量
        if operating_cash_in > 0:
            cash_content = operating_cash_in / revenue
            
            if cash_content < 0.70:
                result.add_finding(
                    finding_type='收入现金含量过低',
                    description=f'销售收现率仅{cash_content*100:.1f}%，大量收入未形成现金回流，'
                               f'需关注应收账款回收风险和收入真实性',
                    severity='high',
                    tax_type='增值税',
                    regulation='企业会计准则第30号 - 现金流量表'
                )
        
        # 应收账款增速超过收入增速
        revenue_growth = fs.get('revenue_growth', 0)
        receivable_growth = fs.get('receivable_growth', 0)
        
        if receivable_growth > revenue_growth + 0.20:  # 应收增速超收入增速20个百分点
            result.add_finding(
                finding_type='应收账款增速异常',
                description=f'应收账款增长率({receivable_growth*100:.1f}%)显著高于收入增长率({revenue_growth*100:.1f}%)，'
                           f'可能存在放宽信用政策刺激销售或虚构收入',
                severity='medium',
                tax_type='企业所得税',
                regulation='CAS 14 - 对价很可能收回'
            )
    
    def _check_percentage_completion(self, result: StrategyResult, completion_data: dict):
        """审查完工百分比法的应用"""
        if not completion_data:
            return
        
        # 检查完工进度估计方法
        estimation_method = completion_data.get('estimation_method', '')
        
        if estimation_method == 'cost':
            # 成本法需要关注实际成本与预算成本的合理性
            actual_cost = completion_data.get('actual_cost', 0)
            estimated_total_cost = completion_data.get('estimated_total_cost', 0)
            
            if estimated_total_cost > 0:
                cost_variance = (actual_cost - estimated_total_cost) / estimated_total_cost
                
                if abs(cost_variance) > 0.20:  # 成本偏差超过20%
                    result.add_finding(
                        finding_type='预算成本偏差过大',
                        description=f'实际成本与预算成本偏差{cost_variance*100:.1f}%，'
                                   f'完工百分比估计可能不准确',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='CAS 14 - 履约进度的计量'
                    )
        
        # 检查收入确认与结算的差异
        recognized_revenue = completion_data.get('recognized_revenue', 0)
        settled_revenue = completion_data.get('settled_revenue', 0)
        
        if recognized_revenue > 0:
            settlement_ratio = settled_revenue / recognized_revenue
            
            if settlement_ratio < 0.50:  # 已结算不足已确认收入的50%
                result.add_finding(
                    finding_type='已确认收入结算比例低',
                    description=f'已确认收入{recognized_revenue:,.2f}元，但已结算仅{settled_revenue:,.2f}元，'
                               f'结算比例{settlement_ratio*100:.1f}%，存在提前确认收入风险',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='CAS 14 - 时段法确认条件'
                )


__all__ = ['RevenueRecognitionStrategy']
