"""
成本费用操纵识别策略

识别通过成本费用进行利润操纵的行为，包括：
- 少结转成本调节毛利率
- 费用资本化
- 利用会计估计调节利润（折旧、坏账）
"""
from typing import Dict, Any
from .base_strategy import BaseStrategy, StrategyResult


class CostManipulationStrategy(BaseStrategy):
    """
    成本费用操纵识别策略
    
    审查要点：
    1. 毛利率异常波动
    2. 存货周转天数异常
    3. 费用率异常变化
    4. 资本性支出突增
    """
    
    name = "cost_manipulation"
    description = "成本费用操纵识别策略 - 识别通过成本费用调节利润的行为"
    version = "1.0.0"
    author = "财务审查系统"
    applicable_tax_types = ["企业所得税"]
    required_data_fields = ["financial_statements"]
    
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行成本费用操纵识别
        
        Args:
            data: 包含:
                - financial_statements: 财务报表
                    - revenue, cost, inventory, etc.
                - historical_data: 历史数据（用于趋势分析）
                - industry_benchmarks: 行业参考数据
        """
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        historical = data.get('historical_data', {})
        industry = data.get('industry_benchmarks', {})
        
        # 1. 毛利率异常分析
        self._analyze_gross_margin(result, fs, historical, industry)
        
        # 2. 存货周转分析
        self._analyze_inventory_turnover(result, fs, historical)
        
        # 3. 费用率分析
        self._analyze_expense_ratio(result, fs, historical)
        
        # 4. 资本性支出分析
        self._analyze_capex(result, fs, historical)
        
        return result
    
    def _analyze_gross_margin(self, result: StrategyResult, fs: dict, 
                               historical: dict, industry: dict):
        """分析毛利率异常"""
        revenue = fs.get('revenue', 0)
        cost = fs.get('cost', 0)
        
        if revenue <= 0:
            return
        
        gross_margin = (revenue - cost) / revenue
        
        # 与上期比较
        prev_margin = historical.get('gross_margin', 0)
        if prev_margin > 0:
            margin_change = gross_margin - prev_margin
            
            # 毛利率异常上升
            if margin_change > 0.05:  # 上升超过5个百分点
                result.add_finding(
                    finding_type='毛利率异常上升',
                    description=f'毛利率从{prev_margin*100:.1f}%上升至{gross_margin*100:.1f}%，'
                               f'上升{margin_change*100:.1f}个百分点，需关注是否存在少结转成本',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='CAS 1 - 存货成本结转'
                )
                result.add_recommendation('执行存货计价测试，检查成本结转完整性')
        
        # 与行业对比
        industry_margin = industry.get('average_gross_margin', 0)
        if industry_margin > 0:
            if gross_margin > industry_margin * 1.3:  # 高于行业30%
                result.add_finding(
                    finding_type='毛利率显著高于行业',
                    description=f'毛利率{gross_margin*100:.1f}%显著高于行业均值{industry_margin*100:.1f}%，'
                               f'可能存在少计成本或虚增收入',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='企业会计准则第30号'
                )
            elif gross_margin < industry_margin * 0.7:  # 低于行业30%
                result.add_finding(
                    finding_type='毛利率显著低于行业',
                    description=f'毛利率{gross_margin*100:.1f}%显著低于行业均值{industry_margin*100:.1f}%，'
                               f'需关注持续经营能力',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='CAS 1 - 存货减值'
                )
        
        # 毛利率异常高（超过50%的一般行业）
        if gross_margin > 0.50 and industry.get('high_margin_industry', False) == False:
            result.add_finding(
                finding_type='毛利率异常高',
                description=f'毛利率高达{gross_margin*100:.1f}%，需核实收入成本确认准确性',
                severity='medium',
                tax_type='企业所得税',
                regulation='企业会计准则第14号'
            )
    
    def _analyze_inventory_turnover(self, result: StrategyResult, fs: dict, historical: dict):
        """分析存货周转异常"""
        revenue = fs.get('revenue', 0)
        cost = fs.get('cost', 0)
        inventory = fs.get('inventory', 0)
        
        if cost <= 0 or inventory <= 0:
            return
        
        # 计算存货周转天数
        inventory_turnover = cost / inventory
        inventory_days = 365 / inventory_turnover if inventory_turnover > 0 else 0
        
        # 与上期比较
        prev_days = historical.get('inventory_days', 0)
        if prev_days > 0:
            days_change = inventory_days - prev_days
            
            if days_change > prev_days * 0.30:  # 周转天数增加超过30%
                result.add_finding(
                    finding_type='存货周转天数异常延长',
                    description=f'存货周转天数从{prev_days:.0f}天延长至{inventory_days:.0f}天，'
                               f'可能存在滞销存货未计提减值或成本结转不及时',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='CAS 1 - 存货减值；CAS 14 - 成本结转'
                )
                result.add_recommendation('执行存货监盘和跌价准备测试')
        
        # 存货与收入配比分析
        if revenue > 0:
            inventory_to_revenue = inventory / revenue
            
            if inventory_to_revenue > 0.30:  # 存货超过收入的30%
                result.add_finding(
                    finding_type='存货占比异常',
                    description=f'存货余额占收入比例达{inventory_to_revenue*100:.1f}%，'
                               f'资金占用严重，需关注跌价风险',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='CAS 1 - 存货可变现净值'
                )
    
    def _analyze_expense_ratio(self, result: StrategyResult, fs: dict, historical: dict):
        """分析费用率异常"""
        revenue = fs.get('revenue', 0)
        period_expenses = fs.get('period_expenses', 0)
        
        if revenue <= 0:
            return
        
        expense_ratio = period_expenses / revenue
        
        # 与上期比较
        prev_ratio = historical.get('expense_ratio', 0)
        if prev_ratio > 0:
            ratio_change = expense_ratio - prev_ratio
            
            # 费用率异常下降
            if ratio_change < -0.03:  # 下降超过3个百分点
                result.add_finding(
                    finding_type='费用率异常下降',
                    description=f'费用率从{prev_ratio*100:.1f}%下降至{expense_ratio*100:.1f}%，'
                               f'可能存在费用资本化或推迟确认费用',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='CAS 4 - 固定资产；CAS 6 - 无形资产'
                )
                result.add_recommendation('检查资本性支出与收益性支出的划分')
        
        # 分析各项费用明细
        # 研发费用
        rd_expense = fs.get('rd_expense', 0)
        if rd_expense > 0 and revenue > 0:
            rd_ratio = rd_expense / revenue
            
            if rd_ratio > 0.10:  # 研发占比超过10%
                result.add_finding(
                    finding_type='研发费用占比高',
                    description=f'研发费用占比{rd_ratio*100:.1f}%，需关注研发费用资本化条件',
                    severity='low',
                    tax_type='企业所得税',
                    regulation='CAS 6 - 研发费用资本化'
                )
    
    def _analyze_capex(self, result: StrategyResult, fs: dict, historical: dict):
        """分析资本性支出异常"""
        capex = fs.get('capital_expenditure', 0)  # 资本性支出
        revenue = fs.get('revenue', 0)
        
        if revenue <= 0:
            return
        
        capex_ratio = capex / revenue
        
        # 与上期比较
        prev_capex = historical.get('capital_expenditure', 0)
        if prev_capex > 0:
            growth = (capex - prev_capex) / prev_capex
            
            if growth > 1.0:  # 增长超过100%
                result.add_finding(
                    finding_type='资本性支出异常增长',
                    description=f'资本性支出同比增长{growth*100:.0f}%，'
                               f'需关注是否存在费用资本化',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='CAS 4 - 固定资产确认条件'
                )
                result.add_recommendation('抽查大额资本性支出项目，核实是否符合资本化条件')
        
        # 在建工程长期挂账
        construction_in_progress = fs.get('construction_in_progress', 0)
        if construction_in_progress > 0:
            cip_age = fs.get('cip_age_months', 0)  # 在建工程账龄（月）
            
            if cip_age > 24:  # 超过2年未转固
                result.add_finding(
                    finding_type='在建工程长期挂账',
                    description=f'在建工程余额{construction_in_progress:,.2f}元，账龄{cip_age:.0f}个月，'
                               f'可能存在推迟转固少提折旧',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='CAS 4 - 固定资产达到预定可使用状态'
                )


__all__ = ['CostManipulationStrategy']
