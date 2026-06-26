"""
税收优惠合规审查策略

审查企业享受的税收优惠政策是否符合条件，包括：
- 高新技术企业（15%税率）
- 小型微利企业优惠（实际税负5%）
- 研发费用加计扣除（100%/120%）
- 固定资产加速折旧/一次性扣除
- 区域性税收优惠（西部大开发、自贸区等）
- 政策时效性审查

注意：本策略基于截至2026年有效的税收政策，使用时请确认最新政策。
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_strategy import BaseStrategy, StrategyResult


class TaxPreferenceStrategy(BaseStrategy):
    """
    税收优惠合规审查策略
    
    审查要点：
    1. 优惠资质条件是否符合
    2. 备案/审批程序是否完备
    3. 优惠计算是否正确
    4. 政策时效性
    5. 业务实质是否符合优惠条件
    """
    
    name = "tax_preference"
    description = "税收优惠合规审查策略 - 审查税收优惠政策适用条件和计算准确性"
    version = "1.0.0"
    author = "财务审查系统"
    applicable_tax_types = ["企业所得税", "增值税"]
    required_data_fields = [
        "financial_statements",
        "company_info",
        "tax_preference_details"  # 税收优惠明细
    ]
    
    # 政策有效期（截止日期）
    POLICY_EXPIRATION = {
        'small_profit_2027': '2027-12-31',      # 小型微利优惠延长至2027年底
        'rd_expense_deduction': '2027-12-31',   # 研发费用加计扣除政策
        'one_time_deduction_500w': '2027-12-31', # 500万以下设备器具一次性扣除
        'high_tech': '长期有效',                  # 高新技术企业所得税优惠
        'western_development': '2030-12-31',    # 西部大开发政策
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.review_date = self.config.get('review_date', datetime.now().strftime('%Y-%m-%d'))
    
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行税收优惠合规审查
        
        Args:
            data: 包含:
                - financial_statements: 财务报表
                - company_info: 企业信息
                    - is_high_tech: 是否高新技术企业
                    - is_small_profit: 是否小型微利企业
                    - industry: 行业
                    - location: 注册地
                - tax_preference_details: 税收优惠明细
                    - preferences: 享受的优惠列表
                    - rd_expenses: 研发费用明细
                    - high_tech_certificate: 高新证书信息
        """
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        company_info = data.get('company_info', {})
        pref_details = data.get('tax_preference_details', {})
        
        # 1. 小型微利企业优惠审查
        self._check_small_profit_preference(result, fs, company_info, pref_details)
        
        # 2. 高新技术企业优惠审查
        self._check_high_tech_preference(result, fs, company_info, pref_details)
        
        # 3. 研发费用加计扣除审查
        self._check_rd_expense_deduction(result, fs, company_info, pref_details)
        
        # 4. 固定资产加速折旧/一次性扣除审查
        self._check_fixed_asset_preference(result, fs, pref_details)
        
        # 5. 区域性税收优惠审查
        self._check_regional_preference(result, company_info, pref_details)
        
        # 6. 政策时效性审查
        self._check_policy_expiration(result, pref_details)
        
        return result
    
    def _check_small_profit_preference(self, result: StrategyResult,
                                        fs: Dict, company_info: Dict, pref_details: Dict):
        """审查小型微利企业优惠"""
        
        is_small_profit = company_info.get('is_small_profit', False)
        preferences = pref_details.get('preferences', [])
        
        # 判断是否享受了小型微利优惠
        enjoyed_small_profit = any(
            p.get('type') == 'small_profit' for p in preferences
        )
        
        if not enjoyed_small_profit and not is_small_profit:
            return
        
        # 获取财务数据
        revenue = fs.get('revenue', 0)
        profit = fs.get('profit', 0)
        total_assets = fs.get('total_assets', 0)
        employee_count = company_info.get('employee_count', 0)
        
        # 小型微利企业条件（2023-2027年政策）
        # 从事国家非限制和禁止行业
        # 年度应纳税所得额不超过300万元
        # 从业人数不超过300人
        # 资产总额不超过5000万元
        
        conditions = {
            '应纳税所得额≤300万': profit <= 3_000_000,
            '从业人数≤300人': 0 < employee_count <= 300,
            '资产总额≤5000万': 0 < total_assets <= 50_000_000,
        }
        
        if enjoyed_small_profit or is_small_profit:
            unmet_conditions = [k for k, v in conditions.items() if not v]
            
            if unmet_conditions:
                result.add_finding(
                    finding_type='小型微利企业条件不符',
                    description=f'企业不符合小型微利企业条件：{"、".join(unmet_conditions)}，'
                               f'不应享受小型微利企业所得税优惠',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='财税〔2023〕12号、国家税务总局公告2023年第6号'
                )
                result.add_recommendation(
                    '如已按小型微利企业申报，需补缴企业所得税并加收滞纳金；'
                    '建议按25%税率重新计算应纳税额'
                )
            else:
                # 验证优惠计算是否正确
                # 2023-2027年政策：减按25%计入应纳税所得额，按20%税率缴纳（实际税负5%）
                expected_tax = profit * 0.25 * 0.20 if profit <= 3_000_000 else (
                    3_000_000 * 0.25 * 0.20 + (profit - 3_000_000) * 0.25
                )
                actual_tax = pref_details.get('actual_cit_paid', profit * 0.25)
                
                # 如果实际税负显著高于5%，可能未正确享受优惠
                if actual_tax > expected_tax * 1.5 and profit <= 3_000_000:
                    result.add_finding(
                        finding_type='小型微利优惠未充分享受',
                        description=f'企业符合小型微利条件，但所得税税负{actual_tax/profit*100:.1f}%'
                                   f'高于优惠后税负5%，可能未正确享受优惠',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='财税〔2023〕12号'
                    )
                    
                result.details['small_profit_expected_tax'] = expected_tax
        
        #  check if claiming preference when not qualified
        if enjoyed_small_profit and not is_small_profit:
            result.add_finding(
                finding_type='违规享受小型微利优惠',
                description='企业不符合小型微利企业条件但享受了税收优惠，涉嫌偷逃税款',
                severity='high',
                tax_type='企业所得税',
                regulation='税收征收管理法第六十三条'
            )
    
    def _check_high_tech_preference(self, result: StrategyResult,
                                     fs: Dict, company_info: Dict, pref_details: Dict):
        """审查高新技术企业优惠"""
        
        is_high_tech = company_info.get('is_high_tech', False)
        preferences = pref_details.get('preferences', [])
        
        enjoyed_high_tech = any(
            p.get('type') == 'high_tech' for p in preferences
        )
        
        if not enjoyed_high_tech and not is_high_tech:
            return
        
        # 高新技术企业认定条件
        # 1. 企业申请认定时须注册成立一年以上
        # 2. 拥有核心知识产权（发明专利、实用新型、软件著作权等）
        # 3. 技术领域属于《国家重点支持的高新技术领域》
        # 4. 科技人员占企业当年职工总数的比例不低于10%
        # 5. 研发费用占销售收入比例：收入≤5000万≥5%，5000万-2亿≥4%，2亿以上≥3%
        # 6. 高新技术产品（服务）收入占总收入≥60%
        # 7. 创新能力评价达标
        
        high_tech_info = pref_details.get('high_tech_certificate', {})
        
        if enjoyed_high_tech or is_high_tech:
            # 检查证书有效性
            cert_no = high_tech_info.get('certificate_no')
            issue_date = high_tech_info.get('issue_date')
            expiry_date = high_tech_info.get('expiry_date')
            
            if not cert_no:
                result.add_finding(
                    finding_type='高新资质证书缺失',
                    description='企业享受高新技术企业所得税优惠，但未能提供有效的高新技术企业证书',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='国科发火〔2016〕32号'
                )
            elif expiry_date:
                # 检查证书是否过期
                if expiry_date < self.review_date:
                    result.add_finding(
                        finding_type='高新资质证书过期',
                        description=f'高新技术企业证书已于{expiry_date}过期，'
                                   f'过期后不应继续享受15%优惠税率',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='国科发火〔2016〕32号'
                    )
                    result.add_recommendation(
                        '如证书已过期，应按规定补缴税款；'
                        '建议及时办理高新资质重新认定'
                    )
            
            # 检查研发费用占比
            revenue = fs.get('revenue', 0)
            rd_expense = fs.get('rd_expense', 0)
            
            if revenue > 0:
                rd_ratio = rd_expense / revenue
                
                # 根据收入规模确定比例要求
                if revenue <= 50_000_000:
                    required_ratio = 0.05
                elif revenue <= 200_000_000:
                    required_ratio = 0.04
                else:
                    required_ratio = 0.03
                
                if rd_ratio < required_ratio:
                    result.add_finding(
                        finding_type='高新资质研发费用占比不足',
                        description=f'研发费用占比{rd_ratio*100:.2f}%低于要求{required_ratio*100:.1f}%，'
                                   f'可能影响高新资质维持',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='国科发火〔2016〕32号 第十一条'
                    )
            
            # 检查高新技术产品收入占比
            high_tech_revenue = pref_details.get('high_tech_revenue', 0)
            if revenue > 0:
                high_tech_ratio = high_tech_revenue / revenue
                if high_tech_ratio < 0.60:
                    result.add_finding(
                        finding_type='高新技术产品收入占比不足',
                        description=f'高新技术产品收入占比{high_tech_ratio*100:.1f}%低于60%要求，'
                                   f'不符合高新技术企业认定条件',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='国科发火〔2016〕32号 第十一条'
                    )
            
            # 检查科技人员占比
            rd_personnel = company_info.get('rd_personnel_count', 0)
            total_employees = company_info.get('employee_count', 0)
            
            if total_employees > 0:
                rd_personnel_ratio = rd_personnel / total_employees
                if rd_personnel_ratio < 0.10:
                    result.add_finding(
                        finding_type='科技人员占比不足',
                        description=f'科技人员占比{rd_personnel_ratio*100:.1f}%低于10%要求',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='国科发火〔2016〕32号 第十一条'
                    )
    
    def _check_rd_expense_deduction(self, result: StrategyResult,
                                     fs: Dict, company_info: Dict, pref_details: Dict):
        """审查研发费用加计扣除"""
        
        rd_expenses = pref_details.get('rd_expenses', [])
        if not rd_expenses:
            return
        
        total_rd = sum(exp.get('amount', 0) for exp in rd_expenses)
        
        if total_rd == 0:
            return
        
        # 检查行业限制
        industry = company_info.get('industry', '')
        restricted_industries = [
            '烟草制造业',
            '住宿和餐饮业',
            '批发和零售业',
            '房地产业',
            '租赁和商务服务业',
            '娱乐业'
        ]
        
        if industry in restricted_industries:
            result.add_finding(
                finding_type='研发费用加计扣除行业限制',
                description=f'{industry}属于负面清单行业，不得享受研发费用加计扣除优惠',
                severity='high',
                amount=total_rd * 1.0,  # 一般企业加计100%
                tax_type='企业所得税',
                regulation='财税〔2015〕119号、财税〔2023〕7号'
            )
            return
        
        # 检查研发费用归集准确性
        for exp in rd_expenses:
            exp_type = exp.get('type', '')
            amount = exp.get('amount', 0)
            
            # 人员人工费用检查
            if exp_type == '人员人工':
                # 检查是否包含非研发人员工资
                if exp.get('includes_non_rd', False):
                    result.add_finding(
                        finding_type='研发费用归集不当',
                        description='研发费用中人员人工费用包含非研发人员工资，应予以剔除',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='国家税务总局公告2017年第40号'
                    )
            
            # 折旧费用检查
            if exp_type == '折旧费用':
                # 检查是否包含非研发用设备折旧
                if exp.get('includes_non_rd_equipment', False):
                    result.add_finding(
                        finding_type='研发费用归集不当',
                        description='研发费用中折旧费用包含非研发用设备折旧',
                        severity='medium',
                        tax_type='企业所得税',
                        regulation='国家税务总局公告2017年第40号'
                    )
        
        # 检查委托研发比例限制
        commissioned_rd = sum(
            exp.get('amount', 0) for exp in rd_expenses 
            if exp.get('type') == '委托研发'
        )
        
        if commissioned_rd > 0:
            commissioned_ratio = commissioned_rd / total_rd
            # 委托境内研发：按实际发生额80%计入；委托境外研发：不超过境内研发2/3
            if commissioned_ratio > 0.80:
                result.add_finding(
                    finding_type='委托研发费用占比过高',
                    description=f'委托研发费用占比{commissioned_ratio*100:.1f}%，'
                               f'需关注委托研发合同合规性及费用归集准确性',
                    severity='medium',
                    tax_type='企业所得税',
                    regulation='财税〔2015〕119号、财税〔2018〕64号'
                )
        
        # 检查加计扣除比例
        # 2023年起：一般企业100%，集成电路/工业母机企业120%
        is_ic_industry = company_info.get('is_ic_industry', False)
        is_machine_tool = company_info.get('is_machine_tool', False)
        
        deduction_rate = 1.20 if (is_ic_industry or is_machine_tool) else 1.00
        expected_deduction = total_rd * deduction_rate
        actual_deduction = pref_details.get('actual_rd_deduction', 0)
        
        if abs(actual_deduction - expected_deduction) > 1000:
            result.add_finding(
                finding_type='研发费用加计扣除计算有误',
                description=f'研发费用{total_rd:,.2f}元，按{deduction_rate*100:.0f}%加计扣除'
                           f'应为{expected_deduction:,.2f}元，'
                           f'但实际扣除{actual_deduction:,.2f}元，差异{abs(actual_deduction-expected_deduction):,.2f}元',
                severity='medium',
                tax_type='企业所得税',
                regulation='财政部 税务总局公告2023年第7号'
            )
        
        result.details['rd_expense_summary'] = {
            'total_rd': total_rd,
            'deduction_rate': deduction_rate,
            'expected_deduction': expected_deduction,
            'tax_saving': expected_deduction * 0.25
        }
    
    def _check_fixed_asset_preference(self, result: StrategyResult,
                                       fs: Dict, pref_details: Dict):
        """审查固定资产加速折旧/一次性扣除"""
        
        fixed_asset_prefs = pref_details.get('fixed_asset_preferences', [])
        if not fixed_asset_prefs:
            return
        
        for pref in fixed_asset_prefs:
            asset_type = pref.get('asset_type', '')
            asset_value = pref.get('value', 0)
            deduction_method = pref.get('deduction_method', '')  # 'one_time' or 'accelerated'
            
            # 500万以下设备器具一次性扣除（2018-2027年）
            if deduction_method == 'one_time':
                if asset_value > 5_000_000:
                    result.add_finding(
                        finding_type='一次性扣除金额超标',
                        description=f'单位价值{asset_value:,.2f}元的{asset_type}超过500万元限额，'
                                   f'不应适用一次性扣除政策',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='财税〔2023〕37号'
                    )
                
                # 检查资产类型限制
                excluded_types = ['房屋', '建筑物', '土地使用权']
                if any(excluded in asset_type for excluded in excluded_types):
                    result.add_finding(
                        finding_type='一次性扣除资产类型不符',
                        description=f'{asset_type}不属于设备器具范围，不得适用一次性扣除',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='财税〔2023〕37号'
                    )
            
            # 加速折旧检查
            if deduction_method == 'accelerated':
                depreciation_years = pref.get('depreciation_years', 0)
                standard_years = pref.get('standard_years', 0)
                
                if standard_years > 0:
                    min_years = standard_years * 0.6  # 不低于规定年限60%
                    if depreciation_years < min_years:
                        result.add_finding(
                            finding_type='加速折旧年限过短',
                            description=f'{asset_type}折旧年限{depreciation_years}年低于'
                                       f'规定年限{standard_years}年的60%（{min_years:.1f}年）',
                            severity='medium',
                            tax_type='企业所得税',
                            regulation='企业所得税法实施条例第九十八条'
                        )
    
    def _check_regional_preference(self, result: StrategyResult,
                                    company_info: Dict, pref_details: Dict):
        """审查区域性税收优惠"""
        
        location = company_info.get('location', '')
        industry = company_info.get('industry', '')
        preferences = pref_details.get('preferences', [])
        
        # 西部大开发政策（适用于西部地区鼓励类产业）
        western_regions = [
            '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', 
            '宁夏', '新疆', '内蒙古', '广西'
        ]
        
        enjoyed_western = any(
            p.get('type') == 'western_development' for p in preferences
        )
        
        if enjoyed_western:
            # 检查是否在西部地区
            is_in_west = any(region in location for region in western_regions)
            
            if not is_in_west:
                result.add_finding(
                    finding_type='违规享受西部大开发优惠',
                    description=f'企业注册地{location}不属于西部地区，'
                               f'不应享受西部大开发15%优惠税率',
                    severity='high',
                    tax_type='企业所得税',
                    regulation='财税〔2020〕23号'
                )
            else:
                # 检查是否属于鼓励类产业
                is_encouraged_industry = company_info.get('is_encouraged_industry', False)
                
                if not is_encouraged_industry:
                    result.add_finding(
                        finding_type='西部大开发产业目录不符',
                        description=f'{industry}不属于西部地区鼓励类产业目录，'
                                   f'不应享受西部大开发优惠',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='西部地区鼓励类产业目录（2020年本）'
                    )
                
                # 检查主营业务收入占比
                main_business_ratio = company_info.get('main_business_ratio', 0)
                if main_business_ratio < 0.60:
                    result.add_finding(
                        finding_type='西部大开发主营业务收入占比不足',
                        description=f'鼓励类产业主营业务收入占比{main_business_ratio*100:.1f}%低于60%要求',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='国家税务总局公告2018年第23号'
                    )
        
        # 海南自贸港优惠
        if '海南' in location:
            enjoyed_hainan = any(
                p.get('type') == 'hainan_ftz' for p in preferences
            )
            
            if enjoyed_hainan:
                # 检查是否在负面清单之外
                is_negative_list = company_info.get('is_negative_list_industry', False)
                
                if is_negative_list:
                    result.add_finding(
                        finding_type='海南自贸港负面清单行业',
                        description='企业所属行业属于海南自贸港负面清单，'
                                   f'不得享受15%优惠税率',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='财税〔2020〕31号'
                    )
    
    def _check_policy_expiration(self, result: StrategyResult, pref_details: Dict):
        """检查政策时效性"""
        
        preferences = pref_details.get('preferences', [])
        
        for pref in preferences:
            pref_type = pref.get('type', '')
            policy_expiry = None
            
            if pref_type == 'small_profit':
                policy_expiry = self.POLICY_EXPIRATION.get('small_profit_2027')
            elif pref_type == 'rd_expense_deduction':
                policy_expiry = self.POLICY_EXPIRATION.get('rd_expense_deduction')
            elif pref_type == 'one_time_deduction_500w':
                policy_expiry = self.POLICY_EXPIRATION.get('one_time_deduction_500w')
            elif pref_type == 'western_development':
                policy_expiry = self.POLICY_EXPIRATION.get('western_development')
            
            if policy_expiry and policy_expiry != '长期有效':
                if policy_expiry < self.review_date:
                    result.add_finding(
                        finding_type='税收优惠政策已过期',
                        description=f'{pref.get("name", pref_type)}政策已于{policy_expiry}到期，'
                                   f'请确认是否有延期政策',
                        severity='high',
                        tax_type='企业所得税',
                        regulation='税收政策时效性提醒'
                    )
                else:
                    # 政策即将到期提醒（6个月内）
                    from datetime import datetime, timedelta
                    expiry = datetime.strptime(policy_expiry, '%Y-%m-%d')
                    review = datetime.strptime(self.review_date, '%Y-%m-%d')
                    
                    if (expiry - review).days <= 180:
                        result.add_finding(
                            finding_type='税收优惠政策即将到期',
                            description=f'{pref.get("name", pref_type)}政策将于{policy_expiry}到期，'
                                       f'请关注政策延续情况',
                            severity='low',
                            tax_type='企业所得税',
                            regulation='税收政策时效性提醒'
                        )


__all__ = ['TaxPreferenceStrategy']
