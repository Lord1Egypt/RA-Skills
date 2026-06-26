#!/usr/bin/env python3
"""
风险指标计算模块

实现21个财务风险指标的评分逻辑，每个指标0-3分：
- 0分：无风险
- 1分：轻微风险（接近阈值）
- 2分：中等风险（达到阈值）
- 3分：严重风险（显著超出阈值）
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RiskCalculator:
    """风险指标计算器"""

    # 评分阈值定义
    THRESHOLDS = {
        # 资产真实性风险
        'cash_debt_paradox': {'cash_ratio': 0.15, 'debt_ratio': 0.30},
        'receivables_anomaly': {'growth_ratio': 1.5, 'receivables_ratio': 0.30},
        'inventory_anomaly': {'growth_ratio': 1.5, 'turnover_decline': 0.20},
        'prepayments_surge': {'ratio': 0.05, 'growth': 0.50},
        'other_receivables_high': {'ratio': 0.05},
        'construction_suspended': {'ratio': 0.10, 'years': 3},
        
        # 利润质量风险
        'cash_profit_divergence': {'ratio': 0.5, 'years': 3},
        'gross_margin_anomaly': {'above_industry': 0.10, 'absolute_high': 0.50},
        'sales_expense_anomaly': {'below_industry': 0.5},
        'abnormal_non_recurring': {'ratio': 0.30},
        'asset_impairment_bath': {'ratio': 0.50},
        
        # 关联交易风险
        'related_transaction_high': {'ratio': 0.30},
        'related_fund_flows': {'ratio': 0.50},
        'related_guarantees': {'ratio': 0.50},
        
        # 资本结构风险
        'goodwill_high': {'ratio': 0.30},
        'debt_ratio_high': {'ratio': 0.70},
        'short_term_liquidity': {'pressure_ratio': 3.0, 'current_ratio': 1.0},
        'dual_debt_high': {'short_ratio': 0.30, 'long_ratio': 0.20},
        
        # 审计治理风险
        'auditor_changes': {'count': 2, 'years': 5},
        'non_standard_opinion': {'types': ['2', '3', '4', '5']},
        'executive_departures': {'count': 2, 'years': 3},
    }

    def __init__(self, financial_data: Dict[str, pd.DataFrame]):
        """
        初始化风险计算器

        Args:
            financial_data: 包含 balance, income, cashflow, fina_indicator, audit 等数据
        """
        self.balance = financial_data.get('balance', pd.DataFrame())
        self.income = financial_data.get('income', pd.DataFrame())
        self.cashflow = financial_data.get('cashflow', pd.DataFrame())
        self.fina_indicator = financial_data.get('fina_indicator', pd.DataFrame())
        self.audit = financial_data.get('audit', pd.DataFrame())
        self.stock_info = financial_data.get('stock_info', {})
        
        logger.info(f"✅ 风险计算器初始化完成")
        logger.info(f"   资产负债表: {len(self.balance)} 条")
        logger.info(f"   利润表: {len(self.income)} 条")
        logger.info(f"   现金流量表: {len(self.cashflow)} 条")
        logger.info(f"   财务指标: {len(self.fina_indicator)} 条")

    def calculate_all_indicators(self) -> Dict[str, Dict]:
        """
        计算所有21个风险指标

        Returns:
            Dict: 每个指标的计算结果 {indicator_name: {score, value, trend, details}}
        """
        logger.info("=" * 60)
        logger.info("📊 开始计算21个风险指标...")
        logger.info("=" * 60)
        
        results = {}
        
        # === 资产真实性风险 (6个) ===
        logger.info("\n【资产真实性风险】")
        results['cash_debt_paradox'] = self.calc_cash_debt_paradox()
        results['receivables_anomaly'] = self.calc_receivables_anomaly()
        results['inventory_anomaly'] = self.calc_inventory_anomaly()
        results['prepayments_surge'] = self.calc_prepayments_surge()
        results['other_receivables_high'] = self.calc_other_receivables_high()
        results['construction_suspended'] = self.calc_construction_suspended()
        
        # === 利润质量风险 (5个) ===
        logger.info("\n【利润质量风险】")
        results['cash_profit_divergence'] = self.calc_cash_profit_divergence()
        results['gross_margin_anomaly'] = self.calc_gross_margin_anomaly()
        results['sales_expense_anomaly'] = self.calc_sales_expense_anomaly()
        results['abnormal_non_recurring'] = self.calc_abnormal_non_recurring()
        results['asset_impairment_bath'] = self.calc_asset_impairment_bath()
        
        # === 关联交易风险 (3个) ===
        logger.info("\n【关联交易风险】")
        results['related_transaction_high'] = self.calc_related_transaction_high()
        results['related_fund_flows'] = self.calc_related_fund_flows()
        results['related_guarantees'] = self.calc_related_guarantees()
        
        # === 资本结构风险 (4个) ===
        logger.info("\n【资本结构风险】")
        results['goodwill_high'] = self.calc_goodwill_high()
        results['debt_ratio_high'] = self.calc_debt_ratio_high()
        results['short_term_liquidity'] = self.calc_short_term_liquidity()
        results['dual_debt_high'] = self.calc_dual_debt_high()
        
        # === 审计治理风险 (3个) ===
        logger.info("\n【审计治理风险】")
        results['auditor_changes'] = self.calc_auditor_changes()
        results['non_standard_opinion'] = self.calc_non_standard_opinion()
        results['executive_departures'] = self.calc_executive_departures()
        
        # 计算总分
        total_score = sum(r['score'] for r in results.values())
        severity = self._determine_severity(total_score)
        
        logger.info("\n" + "=" * 60)
        logger.info(f"📊 风险计算完成")
        logger.info(f"   总分: {total_score} 分")
        logger.info(f"   严重程度: {severity}")
        logger.info("=" * 60)
        
        results['_summary'] = {
            'total_score': total_score,
            'severity': severity,
            'indicator_count': len(results) - 1,
            'critical_count': sum(1 for r in results.values() if r.get('score', 0) == 3),
            'high_count': sum(1 for r in results.values() if r.get('score', 0) == 2),
            'moderate_count': sum(1 for r in results.values() if r.get('score', 0) == 1),
            'low_count': sum(1 for r in results.values() if r.get('score', 0) == 0),
        }
        
        return results

    def _determine_severity(self, total_score: int) -> str:
        """判断整体严重程度"""
        if total_score >= 31:
            return "🔴 Critical"
        elif total_score >= 16:
            return "🟠 High"
        elif total_score >= 6:
            return "🟡 Moderate"
        else:
            return "🟢 Low"

    def _analyze_trend(self, values: List[float]) -> str:
        """
        分析历史趋势

        Args:
            values: 历史值列表（按时间升序）

        Returns:
            str: 趋势描述
        """
        if not values or len(values) < 2:
            return "数据不足"
        
        # 计算变化趋势
        first_half = values[:len(values)//2] if len(values) >= 4 else values[:1]
        second_half = values[len(values)//2:] if len(values) >= 4 else values[1:]
        
        avg_first = np.mean(first_half)
        avg_second = np.mean(second_half)
        
        if avg_first == 0:
            return "无法判断"
        
        change_pct = (avg_second - avg_first) / abs(avg_first) * 100
        
        if change_pct > 30:
            return "📈 显著上升"
        elif change_pct > 10:
            return "↗️ 温和上升"
        elif change_pct < -30:
            return "📉 显著下降"
        elif change_pct < -10:
            return "↘️ 温和下降"
        else:
            return "➡️ 相对稳定"

    def _score_from_deviation(self, value: float, threshold: float, direction: str = 'above') -> int:
        """
        根据偏离阈值程度评分

        Args:
            value: 实际值
            threshold: 阈值
            direction: 'above' 越高越危险, 'below' 越低越危险

        Returns:
            int: 0-3分
        """
        if direction == 'above':
            if value >= threshold * 1.5:
                return 3
            elif value >= threshold:
                return 2
            elif value >= threshold * 0.8:
                return 1
            else:
                return 0
        else:  # below
            if value <= threshold * 0.5:
                return 3
            elif value <= threshold:
                return 2
            elif value <= threshold * 1.2:
                return 1
            else:
                return 0

    # ========== 资产真实性风险 ==========

    def calc_cash_debt_paradox(self) -> Dict:
        """
        1. 存贷双高检测

        检测标准：
        - 货币资金/总资产 > 15%
        - 有息负债/总资产 > 30%
        - 两者同时满足2年以上
        """
        logger.info("  [1] 存贷双高检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        results = []
        for _, row in self.balance.iterrows():
            try:
                monetary_cap = row.get('monetary_cap', 0) or 0
                total_assets = row.get('total_assets', 0) or 1
                short_loan = row.get('short_loan', 0) or 0
                long_loan = row.get('long_loan', 0) or 0
                bonds_payable = row.get('bonds_payable', 0) or 0
                
                cash_ratio = monetary_cap / total_assets if total_assets > 0 else 0
                debt_ratio = (short_loan + long_loan + bonds_payable) / total_assets if total_assets > 0 else 0
                
                paradox_ratio = cash_ratio * debt_ratio  # 乘积衡量双高程度
                
                results.append({
                    'end_date': row.get('end_date'),
                    'cash_ratio': cash_ratio,
                    'debt_ratio': debt_ratio,
                    'paradox_ratio': paradox_ratio,
                })
            except Exception as e:
                logger.warning(f"      计算异常: {e}")
                continue
        
        if not results:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
        
        # 统计双高年份
        threshold = self.THRESHOLDS['cash_debt_paradox']
        dual_high_years = sum(1 for r in results 
                             if r['cash_ratio'] > threshold['cash_ratio'] 
                             and r['debt_ratio'] > threshold['debt_ratio'])
        
        # 最新值
        latest = results[-1]
        avg_paradox = np.mean([r['paradox_ratio'] for r in results])
        
        # 评分逻辑
        if dual_high_years >= 3:
            score = 3
        elif dual_high_years >= 2:
            score = 2
        elif dual_high_years >= 1:
            score = 1
        else:
            score = 0
        
        trend = self._analyze_trend([r['paradox_ratio'] for r in results])
        
        logger.info(f"      最新现金占比: {latest['cash_ratio']*100:.1f}%")
        logger.info(f"      最新有息负债占比: {latest['debt_ratio']*100:.1f}%")
        logger.info(f"      双高年份: {dual_high_years} 年")
        logger.info(f"      ⚠️ 评分: {score} 分")
        
        return {
            'score': score,
            'value': latest['paradox_ratio'],
            'trend': trend,
            'details': {
                'cash_ratio_latest': latest['cash_ratio'],
                'debt_ratio_latest': latest['debt_ratio'],
                'dual_high_years': dual_high_years,
                'avg_paradox_ratio': avg_paradox,
                'threshold_cash': threshold['cash_ratio'],
                'threshold_debt': threshold['debt_ratio'],
            }
        }

    def calc_receivables_anomaly(self) -> Dict:
        """
        2. 应收账款畸高检测

        检测标准：
        - 应收账款增速 > 收入增速 × 1.5 连续3年
        - 或应收账款/收入 > 30% 且上升
        """
        logger.info("  [2] 应收账款畸高检测...")
        
        if self.balance.empty or self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '财务数据缺失'}}
        
        # 合并数据（按年度）
        try:
            balance_sorted = self.balance.sort_values('end_date')
            income_sorted = self.income.sort_values('end_date')
            
            results = []
            for i in range(1, len(balance_sorted)):
                try:
                    curr_balance = balance_sorted.iloc[i]
                    prev_balance = balance_sorted.iloc[i-1]
                    
                    # 找对应年度的income
                    curr_income = income_sorted[income_sorted['end_date'] == curr_balance['end_date']]
                    prev_income = income_sorted[income_sorted['end_date'] == prev_balance['end_date']]
                    
                    if curr_income.empty or prev_income.empty:
                        continue
                    
                    curr_receiv = curr_balance.get('accounts_receiv', 0) or 0
                    prev_receiv = prev_balance.get('accounts_receiv', 0) or 1
                    curr_revenue = curr_income.iloc[0].get('revenue', 0) or 0
                    prev_revenue = prev_income.iloc[0].get('revenue', 0) or 1
                    
                    # 增速计算
                    receiv_growth = (curr_receiv - prev_receiv) / abs(prev_receiv) if prev_receiv != 0 else 0
                    revenue_growth = (curr_revenue - prev_revenue) / abs(prev_revenue) if prev_revenue != 0 else 0
                    
                    # 增速比率
                    growth_ratio = abs(receiv_growth / revenue_growth) if revenue_growth != 0 else 0
                    
                    # 应收账款占比
                    receiv_ratio = curr_receiv / curr_revenue if curr_revenue > 0 else 0
                    
                    results.append({
                        'end_date': curr_balance.get('end_date'),
                        'receiv_growth': receiv_growth,
                        'revenue_growth': revenue_growth,
                        'growth_ratio': growth_ratio,
                        'receiv_ratio': receiv_ratio,
                    })
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效对比数据'}}
            
            # 统计异常年份
            threshold = self.THRESHOLDS['receivables_anomaly']
            
            # 增速异常年数
            growth_abnormal_years = sum(1 for r in results 
                                       if r['growth_ratio'] > threshold['growth_ratio'])
            
            # 占比异常年数
            ratio_abnormal_years = sum(1 for r in results 
                                      if r['receiv_ratio'] > threshold['receivables_ratio'])
            
            latest = results[-1]
            
            # 评分
            if growth_abnormal_years >= 3:
                score = 3
            elif growth_abnormal_years >= 2 or ratio_abnormal_years >= 3:
                score = 2
            elif growth_abnormal_years >= 1 or ratio_abnormal_years >= 2:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['receiv_ratio'] for r in results])
            
            logger.info(f"      最新应收账款增速: {latest['receiv_growth']*100:.1f}%")
            logger.info(f"      最新收入增速: {latest['revenue_growth']*100:.1f}%")
            logger.info(f"      增速异常年份: {growth_abnormal_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['growth_ratio'],
                'trend': trend,
                'details': {
                    'receiv_growth_latest': latest['receiv_growth'],
                    'revenue_growth_latest': latest['revenue_growth'],
                    'growth_ratio_latest': latest['growth_ratio'],
                    'receiv_ratio_latest': latest['receiv_ratio'],
                    'growth_abnormal_years': growth_abnormal_years,
                    'ratio_abnormal_years': ratio_abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_inventory_anomaly(self) -> Dict:
        """
        3. 存货异常检测

        检测标准：
        - 存货增速 > 成本增速 × 1.5 连续2年
        - 或存货周转率显著下降
        """
        logger.info("  [3] 存货异常检测...")
        
        if self.balance.empty or self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '财务数据缺失'}}
        
        try:
            balance_sorted = self.balance.sort_values('end_date')
            income_sorted = self.income.sort_values('end_date')
            
            results = []
            turnover_results = []
            
            for i in range(1, len(balance_sorted)):
                try:
                    curr_balance = balance_sorted.iloc[i]
                    prev_balance = balance_sorted.iloc[i-1]
                    
                    curr_income = income_sorted[income_sorted['end_date'] == curr_balance['end_date']]
                    prev_income = income_sorted[income_sorted['end_date'] == prev_balance['end_date']]
                    
                    if curr_income.empty or prev_income.empty:
                        continue
                    
                    curr_inventory = curr_balance.get('inventory', 0) or 0
                    prev_inventory = prev_balance.get('inventory', 0) or 1
                    curr_cost = curr_income.iloc[0].get('oper_cost', 0) or 0
                    prev_cost = prev_income.iloc[0].get('oper_cost', 0) or 1
                    
                    # 增速计算
                    inv_growth = (curr_inventory - prev_inventory) / abs(prev_inventory) if prev_inventory != 0 else 0
                    cost_growth = (curr_cost - prev_cost) / abs(prev_cost) if prev_cost != 0 else 0
                    
                    # 增速比率
                    growth_ratio = abs(inv_growth / cost_growth) if cost_growth != 0 else 0
                    
                    results.append({
                        'end_date': curr_balance.get('end_date'),
                        'inv_growth': inv_growth,
                        'cost_growth': cost_growth,
                        'growth_ratio': growth_ratio,
                        'inventory': curr_inventory,
                        'cost': curr_cost,
                    })
                    
                    # 存货周转率（使用平均值）
                    avg_inventory = (curr_inventory + prev_inventory) / 2
                    turnover = curr_cost / avg_inventory if avg_inventory > 0 else 0
                    turnover_results.append({
                        'end_date': curr_balance.get('end_date'),
                        'turnover': turnover,
                    })
                    
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['inventory_anomaly']
            
            # 增速异常年数
            growth_abnormal_years = sum(1 for r in results 
                                       if r['growth_ratio'] > threshold['growth_ratio'])
            
            # 周转率趋势分析
            if len(turnover_results) >= 2:
                turnover_values = [r['turnover'] for r in turnover_results]
                avg_first = np.mean(turnover_values[:len(turnover_values)//2])
                avg_last = np.mean(turnover_values[len(turnover_values)//2:])
                
                turnover_decline_pct = (avg_first - avg_last) / avg_first if avg_first > 0 else 0
                turnover_declining = turnover_decline_pct > threshold['turnover_decline']
            else:
                turnover_declining = False
                turnover_decline_pct = 0
            
            latest = results[-1]
            
            # 评分
            if growth_abnormal_years >= 3 and turnover_declining:
                score = 3
            elif growth_abnormal_years >= 2 or turnover_declining:
                score = 2
            elif growth_abnormal_years >= 1:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['inventory'] for r in results if r['inventory'] > 0])
            
            logger.info(f"      最新存货增速: {latest['inv_growth']*100:.1f}%")
            logger.info(f"      最新成本增速: {latest['cost_growth']*100:.1f}%")
            logger.info(f"      增速异常年份: {growth_abnormal_years} 年")
            logger.info(f"      周转率下降: {turnover_decline_pct*100:.1f}%")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['growth_ratio'],
                'trend': trend,
                'details': {
                    'inv_growth_latest': latest['inv_growth'],
                    'cost_growth_latest': latest['cost_growth'],
                    'growth_ratio_latest': latest['growth_ratio'],
                    'growth_abnormal_years': growth_abnormal_years,
                    'turnover_decline_pct': turnover_decline_pct,
                    'turnover_declining': turnover_declining,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_prepayments_surge(self) -> Dict:
        """
        4. 预付账款激增检测

        检测标准：
        - 预付账款/总资产 > 5%
        - 预付账款增速 > 50% 无合理商业理由
        """
        logger.info("  [4] 预付账款激增检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            balance_sorted = self.balance.sort_values('end_date')
            
            results = []
            for i in range(1, len(balance_sorted)):
                try:
                    curr = balance_sorted.iloc[i]
                    prev = balance_sorted.iloc[i-1]
                    
                    adv_payment = curr.get('adv_payment', 0) or 0
                    total_assets = curr.get('total_assets', 0) or 1
                    prev_adv_payment = prev.get('adv_payment', 0) or 1
                    
                    # 预付账款占比
                    ratio = adv_payment / total_assets if total_assets > 0 else 0
                    
                    # 预付账款增速
                    growth = (adv_payment - prev_adv_payment) / abs(prev_adv_payment) if prev_adv_payment != 0 else 0
                    
                    results.append({
                        'end_date': curr.get('end_date'),
                        'adv_payment': adv_payment,
                        'ratio': ratio,
                        'growth': growth,
                    })
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['prepayments_surge']
            
            # 占比异常年数
            ratio_abnormal_years = sum(1 for r in results if r['ratio'] > threshold['ratio'])
            
            # 增速异常年数
            growth_abnormal_years = sum(1 for r in results if abs(r['growth']) > threshold['growth'])
            
            latest = results[-1]
            
            # 评分
            if ratio_abnormal_years >= 2 and growth_abnormal_years >= 2:
                score = 3
            elif ratio_abnormal_years >= 1 and growth_abnormal_years >= 1:
                score = 2
            elif ratio_abnormal_years >= 1 or growth_abnormal_years >= 1:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['adv_payment'] for r in results])
            
            logger.info(f"      最新预付账款占比: {latest['ratio']*100:.1f}%")
            logger.info(f"      最新预付账款增速: {latest['growth']*100:.1f}%")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'adv_payment_latest': latest['adv_payment'],
                    'ratio_latest': latest['ratio'],
                    'growth_latest': latest['growth'],
                    'ratio_abnormal_years': ratio_abnormal_years,
                    'growth_abnormal_years': growth_abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_other_receivables_high(self) -> Dict:
        """
        5. 其他应收款高企检测

        检测标准：
        - 其他应收款 > 净资产 × 5%
        """
        logger.info("  [5] 其他应收款高企检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            results = []
            for _, row in self.balance.iterrows():
                try:
                    other_receiv = row.get('other_receiv', 0) or 0
                    total_equity = row.get('total_hldr_equity', 0) or 1
                    
                    ratio = other_receiv / total_equity if total_equity > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'other_receiv': other_receiv,
                        'total_equity': total_equity,
                        'ratio': ratio,
                    })
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['other_receivables_high']
            
            # 异常年数
            abnormal_years = sum(1 for r in results if r['ratio'] > threshold['ratio'])
            
            latest = results[-1]
            
            # 评分
            score = self._score_from_deviation(latest['ratio'], threshold['ratio'], 'above')
            
            # 如果持续多年异常，加1分
            if abnormal_years >= 3 and score > 0:
                score = min(score + 1, 3)
            
            trend = self._analyze_trend([r['ratio'] for r in results])
            
            logger.info(f"      最新其他应收款/净资产: {latest['ratio']*100:.1f}%")
            logger.info(f"      异常年份: {abnormal_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'other_receiv_latest': latest['other_receiv'],
                    'ratio_latest': latest['ratio'],
                    'abnormal_years': abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_construction_suspended(self) -> Dict:
        """
        6. 在建工程悬案检测

        检测标准：
        - 在建工程/总资产 > 10%
        - 或在建工程超过3年未转固
        """
        logger.info("  [6] 在建工程悬案检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            results = []
            for _, row in self.balance.iterrows():
                try:
                    const_in_prog = row.get('const_in_prog', 0) or 0
                    total_assets = row.get('total_assets', 0) or 1
                    fixed_assets = row.get('fixed_assets', 0) or 0
                    
                    ratio = const_in_prog / total_assets if total_assets > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'const_in_prog': const_in_prog,
                        'total_assets': total_assets,
                        'fixed_assets': fixed_assets,
                        'ratio': ratio,
                    })
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['construction_suspended']
            
            # 占比异常年数
            ratio_abnormal_years = sum(1 for r in results if r['ratio'] > threshold['ratio'])
            
            # 检查是否持续高企（未转固）
            recent_high = sum(1 for r in results[-threshold['years']:] if r['ratio'] > threshold['ratio'] * 0.5)
            sustained_high = recent_high >= threshold['years']
            
            latest = results[-1]
            
            # 评分
            if ratio_abnormal_years >= threshold['years'] and sustained_high:
                score = 3
            elif ratio_abnormal_years >= 2:
                score = 2
            elif ratio_abnormal_years >= 1:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['ratio'] for r in results])
            
            logger.info(f"      最新在建工程/总资产: {latest['ratio']*100:.1f}%")
            logger.info(f"      比例异常年份: {ratio_abnormal_years} 年")
            logger.info(f"      是否持续高企: {sustained_high}")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'const_in_prog_latest': latest['const_in_prog'],
                    'ratio_latest': latest['ratio'],
                    'ratio_abnormal_years': ratio_abnormal_years,
                    'sustained_high': sustained_high,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    # ========== 利润质量风险 ==========

    def calc_cash_profit_divergence(self) -> Dict:
        """
        7. 净现比背离检测

        检测标准：
        - 净利润为正但经营现金流为负连续3年
        - 或净现比 < 0.5 持续
        """
        logger.info("  [7] 净现比背离检测...")
        
        if self.income.empty or self.cashflow.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '财务数据缺失'}}
        
        try:
            income_sorted = self.income.sort_values('end_date')
            cashflow_sorted = self.cashflow.sort_values('end_date')
            
            results = []
            for _, income_row in income_sorted.iterrows():
                try:
                    # 找对应的现金流量数据
                    cashflow_match = cashflow_sorted[cashflow_sorted['end_date'] == income_row['end_date']]
                    
                    if cashflow_match.empty:
                        continue
                    
                    net_profit = income_row.get('net_profit', 0) or 0
                    oper_cashflow = cashflow_match.iloc[0].get('net_cash_flows_oper_act', 0) or 0
                    
                    # 净现比
                    cash_profit_ratio = oper_cashflow / net_profit if net_profit != 0 else 0
                    
                    # 检查背离情况
                    divergence = net_profit > 0 and oper_cashflow < 0
                    
                    results.append({
                        'end_date': income_row.get('end_date'),
                        'net_profit': net_profit,
                        'oper_cashflow': oper_cashflow,
                        'cash_profit_ratio': cash_profit_ratio,
                        'divergence': divergence,
                    })
                except Exception as e:
                    logger.warning(f"      计算异常: {e}")
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['cash_profit_divergence']
            
            # 统计背离年数
            divergence_years = sum(1 for r in results if r['divergence'])
            
            # 低净现比年数
            low_ratio_years = sum(1 for r in results 
                                 if r['cash_profit_ratio'] < threshold['ratio'] 
                                 and r['net_profit'] > 0)
            
            latest = results[-1]
            
            # 评分
            if divergence_years >= threshold['years']:
                score = 3
            elif divergence_years >= 2 or low_ratio_years >= 3:
                score = 2
            elif divergence_years >= 1 or low_ratio_years >= 2:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['cash_profit_ratio'] for r in results])
            
            logger.info(f"      最新净利润: {latest['net_profit']/1e8:.2f} 亿元")
            logger.info(f"      最新经营现金流: {latest['oper_cashflow']/1e8:.2f} 亿元")
            logger.info(f"      最新净现比: {latest['cash_profit_ratio']:.2f}")
            logger.info(f"      背离年份: {divergence_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['cash_profit_ratio'],
                'trend': trend,
                'details': {
                    'net_profit_latest': latest['net_profit'],
                    'oper_cashflow_latest': latest['oper_cashflow'],
                    'cash_profit_ratio_latest': latest['cash_profit_ratio'],
                    'divergence_years': divergence_years,
                    'low_ratio_years': low_ratio_years,
                    'divergence_latest': latest['divergence'],
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_gross_margin_anomaly(self) -> Dict:
        """
        8. 毛利率异常检测

        检测标准：
        - 毛利率 > 行业中位数 + 10个百分点
        - 或毛利率持续高于50%（竞争行业）
        """
        logger.info("  [8] 毛利率异常检测...")
        
        if self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '利润表数据缺失'}}
        
        try:
            # 尝试使用fina_indicator中的毛利率
            if not self.fina_indicator.empty:
                results = []
                for _, row in self.fina_indicator.iterrows():
                    try:
                        gm = row.get('grossprofit_margin', 0) or 0
                        if gm > 0:
                            results.append({
                                'end_date': row.get('end_date'),
                                'gross_margin': gm / 100,  # 转换为比例
                            })
                    except Exception as e:
                        continue
            else:
                # 从income计算
                results = []
                for _, row in self.income.iterrows():
                    try:
                        revenue = row.get('revenue', 0) or 0
                        cost = row.get('oper_cost', 0) or 0
                        
                        gross_margin = (revenue - cost) / revenue if revenue > 0 else 0
                        
                        results.append({
                            'end_date': row.get('end_date'),
                            'gross_margin': gross_margin,
                        })
                    except Exception as e:
                        continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['gross_margin_anomaly']
            
            # 异常高毛利年数
            absolute_high_years = sum(1 for r in results 
                                     if r['gross_margin'] > threshold['absolute_high'])
            
            latest = results[-1]
            avg_gm = np.mean([r['gross_margin'] for r in results])
            
            # 检查趋势
            gm_trend = self._analyze_trend([r['gross_margin'] for r in results])
            
            # 评分（暂时不做行业对比，因为没有行业数据）
            if absolute_high_years >= 3:
                score = 2  # 持续高毛利需要行业对比验证
            elif absolute_high_years >= 1:
                score = 1
            else:
                score = 0
            
            logger.info(f"      最新毛利率: {latest['gross_margin']*100:.1f}%")
            logger.info(f"      平均毛利率: {avg_gm*100:.1f}%")
            logger.info(f"      异常高毛利年份: {absolute_high_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分 (需行业对比验证)")
            
            return {
                'score': score,
                'value': latest['gross_margin'],
                'trend': gm_trend,
                'details': {
                    'gross_margin_latest': latest['gross_margin'],
                    'avg_gross_margin': avg_gm,
                    'absolute_high_years': absolute_high_years,
                    'note': '需行业对比验证',
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_sales_expense_anomaly(self) -> Dict:
        """
        9. 销售费用率异常检测

        检测标准：
        - 销售费用率 < 行业中位数 × 0.5
        """
        logger.info("  [9] 销售费用率异常检测...")
        
        if self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '利润表数据缺失'}}
        
        try:
            results = []
            for _, row in self.income.iterrows():
                try:
                    sell_exp = row.get('sell_exp', 0) or 0
                    revenue = row.get('revenue', 0) or 1
                    
                    sales_expense_ratio = sell_exp / revenue if revenue > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'sell_exp': sell_exp,
                        'revenue': revenue,
                        'ratio': sales_expense_ratio,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['sales_expense_anomaly']
            
            latest = results[-1]
            avg_ratio = np.mean([r['ratio'] for r in results])
            
            # 检查趋势（费用率下降）
            ratio_trend = self._analyze_trend([r['ratio'] for r in results])
            
            # 评分（暂时不做行业对比）
            # 如果费用率极低（<1%）或快速下降，给予关注
            if latest['ratio'] < 0.01 and latest['revenue'] > 1e9:  # 收入超1亿但销售费用率<1%
                score = 2
            elif latest['ratio'] < 0.02:
                score = 1
            else:
                score = 0
            
            logger.info(f"      最新销售费用率: {latest['ratio']*100:.1f}%")
            logger.info(f"      平均销售费用率: {avg_ratio*100:.1f}%")
            logger.info(f"      ⚠️ 评分: {score} 分 (需行业对比验证)")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': ratio_trend,
                'details': {
                    'sell_exp_latest': latest['sell_exp'],
                    'ratio_latest': latest['ratio'],
                    'avg_ratio': avg_ratio,
                    'note': '需行业对比验证',
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_abnormal_non_recurring(self) -> Dict:
        """
        10. 异常非经常性损益检测

        检测标准：
        - 非经常性损益 > 净利润 × 30%
        """
        logger.info("  [10] 异常非经常性损益检测...")
        
        if self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '利润表数据缺失'}}
        
        try:
            results = []
            for _, row in self.income.iterrows():
                try:
                    net_profit = row.get('net_profit', 0) or 0
                    invest_income = row.get('invest_income', 0) or 0
                    asset_disposal_income = row.get('asset_disposal_income', 0) or 0
                    
                    # 估算非经常性损益（投资收益+资产处置收益）
                    # 实际数据需要从附注获取，这里用代理指标
                    non_recurring_est = abs(invest_income) + abs(asset_disposal_income)
                    
                    # 占净利润比例
                    non_recurring_ratio = non_recurring_est / abs(net_profit) if net_profit != 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'net_profit': net_profit,
                        'non_recurring_est': non_recurring_est,
                        'ratio': non_recurring_ratio,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['abnormal_non_recurring']
            
            # 异常年数
            abnormal_years = sum(1 for r in results if r['ratio'] > threshold['ratio'])
            
            latest = results[-1]
            
            # 评分
            score = self._score_from_deviation(latest['ratio'], threshold['ratio'], 'above')
            
            # 如果持续异常，提升评分
            if abnormal_years >= 3 and score > 0:
                score = min(score + 1, 3)
            
            trend = self._analyze_trend([r['ratio'] for r in results])
            
            logger.info(f"      最新非经常性损益估算: {latest['non_recurring_est']/1e8:.2f} 亿元")
            logger.info(f"      最新净利润: {latest['net_profit']/1e8:.2f} 亿元")
            logger.info(f"      最新非经常性占比: {latest['ratio']*100:.1f}%")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'non_recurring_est_latest': latest['non_recurring_est'],
                    'net_profit_latest': latest['net_profit'],
                    'ratio_latest': latest['ratio'],
                    'abnormal_years': abnormal_years,
                    'note': '估算值，需从附注核实',
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_asset_impairment_bath(self) -> Dict:
        """
        11. 资产减值洗大澡检测

        检测标准：
        - 单年度资产减值损失 > 净利润 × 50%
        """
        logger.info("  [11] 资产减值洗大澡检测...")
        
        if self.income.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '利润表数据缺失'}}
        
        try:
            results = []
            for _, row in self.income.iterrows():
                try:
                    net_profit = row.get('net_profit', 0) or 0
                    impair_loss = row.get('asset_impair_loss', 0) or 0
                    
                    # 减值占净利润比例
                    impair_ratio = abs(impair_loss) / abs(net_profit) if net_profit != 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'net_profit': net_profit,
                        'impair_loss': impair_loss,
                        'ratio': impair_ratio,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['asset_impairment_bath']
            
            # 检测洗大澡（单年度大幅减值）
            bath_years = [r for r in results if r['ratio'] > threshold['ratio']]
            
            latest = results[-1]
            
            # 评分
            if len(bath_years) >= 2:
                score = 3  # 多次洗大澡
            elif len(bath_years) >= 1:
                # 检查是否是最近一年
                if bath_years[0]['end_date'] == latest['end_date']:
                    score = 2
                else:
                    score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['impair_loss'] for r in results])
            
            logger.info(f"      最新资产减值损失: {latest['impair_loss']/1e8:.2f} 亿元")
            logger.info(f"      减值占净利润比例: {latest['ratio']*100:.1f}%")
            logger.info(f"      洗大澡年份: {len(bath_years)} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'impair_loss_latest': latest['impair_loss'],
                    'ratio_latest': latest['ratio'],
                    'bath_years_count': len(bath_years),
                    'bath_years': [r['end_date'] for r in bath_years],
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    # ========== 关联交易风险 ==========

    def calc_related_transaction_high(self) -> Dict:
        """
        12. 关联交易占比高检测

        检测标准：
        - 关联采购/销售 > 30%
        
        注：Tushare无直接关联交易数据，需从附注获取
        """
        logger.info("  [12] 关联交易占比高检测...")
        
        # 由于数据源限制，返回提示信息
        logger.warning("      ⚠️ Tushare无关联交易数据，需从财报附注手动获取")
        
        return {
            'score': 0,
            'value': 0,
            'trend': '数据缺失',
            'details': {
                'error': 'Tushare无关联交易数据',
                'note': '需从财报附注"关联交易"章节获取以下信息：',
                'items': [
                    '关联采购金额 / 总采购金额',
                    '关联销售金额 / 营业收入',
                    '关联方应收账款占比',
                    '关联方应付账款占比',
                ],
                'threshold': self.THRESHOLDS['related_transaction_high']['ratio'],
            }
        }

    def calc_related_fund_flows(self) -> Dict:
        """
        13. 关联方资金往来频繁检测

        检测标准：
        - 关联方在其他应收/应付中占比 > 50%
        
        注：需要附注数据
        """
        logger.info("  [13] 关联方资金往来检测...")
        
        logger.warning("      ⚠️ 需从财报附注获取关联方资金往来明细")
        
        return {
            'score': 0,
            'value': 0,
            'trend': '数据缺失',
            'details': {
                'error': '需附注数据',
                'note': '需从财报附注"关联方资金往来"章节获取',
                'items': [
                    '关联方其他应收款金额',
                    '关联方其他应付款金额',
                    '关联方借款/贷款金额',
                ],
                'threshold': self.THRESHOLDS['related_fund_flows']['ratio'],
            }
        }

    def calc_related_guarantees(self) -> Dict:
        """
        14. 关联担保过多检测

        检测标准：
        - 对外担保 > 净资产 × 50%
        """
        logger.info("  [14] 关联担保过多检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            # 检查是否有对外担保字段
            results = []
            for _, row in self.balance.iterrows():
                try:
                    external_guarantee = row.get('external_guarantee', 0) or 0
                    total_equity = row.get('total_hldr_equity', 0) or 1
                    
                    # Tushare资产负债表通常无担保字段
                    # 但如果有，计算占比
                    ratio = external_guarantee / total_equity if total_equity > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'external_guarantee': external_guarantee,
                        'total_equity': total_equity,
                        'ratio': ratio,
                    })
                except Exception as e:
                    continue
            
            threshold = self.THRESHOLDS['related_guarantees']
            
            # 如果数据缺失，返回提示
            if all(r['external_guarantee'] == 0 for r in results):
                logger.warning("      ⚠️ 资产负债表无担保数据，需从公告/附注获取")
                return {
                    'score': 0,
                    'value': 0,
                    'trend': '数据缺失',
                    'details': {
                        'error': '资产负债表无担保字段',
                        'note': '需从公司公告"对外担保"章节或年报附注获取',
                        'threshold': threshold['ratio'],
                    }
                }
            
            latest = results[-1]
            
            # 评分
            score = self._score_from_deviation(latest['ratio'], threshold['ratio'], 'above')
            
            trend = self._analyze_trend([r['ratio'] for r in results])
            
            logger.info(f"      最新对外担保/净资产: {latest['ratio']*100:.1f}%")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'external_guarantee_latest': latest['external_guarantee'],
                    'ratio_latest': latest['ratio'],
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    # ========== 资本结构风险 ==========

    def calc_goodwill_high(self) -> Dict:
        """
        15. 商誉占比过高检测

        检测标准：
        - 商誉 > 净资产 × 30%
        """
        logger.info("  [15] 商誉占比过高检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            results = []
            for _, row in self.balance.iterrows():
                try:
                    goodwill = row.get('goodwill', 0) or 0
                    total_equity = row.get('total_hldr_equity', 0) or 1
                    
                    ratio = goodwill / total_equity if total_equity > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'goodwill': goodwill,
                        'total_equity': total_equity,
                        'ratio': ratio,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['goodwill_high']
            
            # 异常年数
            abnormal_years = sum(1 for r in results if r['ratio'] > threshold['ratio'])
            
            latest = results[-1]
            
            # 评分
            score = self._score_from_deviation(latest['ratio'], threshold['ratio'], 'above')
            
            # 如果商誉持续高企，提升风险
            if abnormal_years >= 3 and score > 0:
                score = min(score + 1, 3)
            
            trend = self._analyze_trend([r['goodwill'] for r in results])
            
            logger.info(f"      最新商誉: {latest['goodwill']/1e8:.2f} 亿元")
            logger.info(f"      最新商誉/净资产: {latest['ratio']*100:.1f}%")
            logger.info(f"      异常年份: {abnormal_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['ratio'],
                'trend': trend,
                'details': {
                    'goodwill_latest': latest['goodwill'],
                    'ratio_latest': latest['ratio'],
                    'abnormal_years': abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_debt_ratio_high(self) -> Dict:
        """
        16. 资产负债率畸高检测

        检测标准：
        - 资产负债率 > 70% 且持续上升
        """
        logger.info("  [16] 资产负债率畸高检测...")
        
        if self.fina_indicator.empty and self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '财务数据缺失'}}
        
        try:
            results = []
            
            # 优先使用fina_indicator中的资产负债率
            if not self.fina_indicator.empty:
                for _, row in self.fina_indicator.iterrows():
                    try:
                        debt_ratio = row.get('debt_to_assets', 0) or 0
                        if debt_ratio > 0:
                            results.append({
                                'end_date': row.get('end_date'),
                                'debt_ratio': debt_ratio / 100,  # 转换为比例
                            })
                    except Exception as e:
                        continue
            else:
                # 从资产负债表计算
                for _, row in self.balance.iterrows():
                    try:
                        total_liab = row.get('total_liab', 0) or 0
                        total_assets = row.get('total_assets', 0) or 1
                        
                        debt_ratio = total_liab / total_assets if total_assets > 0 else 0
                        
                        results.append({
                            'end_date': row.get('end_date'),
                            'debt_ratio': debt_ratio,
                        })
                    except Exception as e:
                        continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['debt_ratio_high']
            
            # 异常年数
            abnormal_years = sum(1 for r in results if r['debt_ratio'] > threshold['ratio'])
            
            latest = results[-1]
            
            # 检查趋势
            debt_trend = self._analyze_trend([r['debt_ratio'] for r in results])
            
            # 评分
            score = self._score_from_deviation(latest['debt_ratio'], threshold['ratio'], 'above')
            
            # 如果持续上升且已高企，提升风险
            if '上升' in debt_trend and score > 0:
                score = min(score + 1, 3)
            
            logger.info(f"      最新资产负债率: {latest['debt_ratio']*100:.1f}%")
            logger.info(f"      异常年份: {abnormal_years} 年")
            logger.info(f"      趋势: {debt_trend}")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['debt_ratio'],
                'trend': debt_trend,
                'details': {
                    'debt_ratio_latest': latest['debt_ratio'],
                    'abnormal_years': abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_short_term_liquidity(self) -> Dict:
        """
        17. 短期偿债压力检测

        检测标准：
        - 短期借款/货币资金 > 3
        - 或流动比率 < 1.0 持续
        """
        logger.info("  [17] 短期偿债压力检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            results = []
            current_ratio_results = []
            
            for _, row in self.balance.iterrows():
                try:
                    short_loan = row.get('short_loan', 0) or 0
                    monetary_cap = row.get('monetary_cap', 0) or 1
                    current_assets = row.get('current_assets', 0) or 0
                    current_liab = row.get('current_liab', 0) or 1
                    
                    # 短期借款/现金
                    pressure_ratio = short_loan / monetary_cap if monetary_cap > 0 else 0
                    
                    # 流动比率
                    current_ratio = current_assets / current_liab if current_liab > 0 else 0
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'short_loan': short_loan,
                        'monetary_cap': monetary_cap,
                        'pressure_ratio': pressure_ratio,
                    })
                    
                    current_ratio_results.append({
                        'end_date': row.get('end_date'),
                        'current_ratio': current_ratio,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['short_term_liquidity']
            
            # 压力异常年数
            pressure_abnormal_years = sum(1 for r in results 
                                          if r['pressure_ratio'] > threshold['pressure_ratio'])
            
            # 流动比率异常年数
            current_ratio_abnormal_years = sum(1 for r in current_ratio_results 
                                               if r['current_ratio'] < threshold['current_ratio'])
            
            latest = results[-1]
            latest_cr = current_ratio_results[-1]
            
            # 评分
            if pressure_abnormal_years >= 2 and current_ratio_abnormal_years >= 2:
                score = 3
            elif pressure_abnormal_years >= 1 and current_ratio_abnormal_years >= 1:
                score = 2
            elif pressure_abnormal_years >= 1 or current_ratio_abnormal_years >= 2:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['pressure_ratio'] for r in results])
            
            logger.info(f"      最新短期借款/现金: {latest['pressure_ratio']:.2f}")
            logger.info(f"      最新流动比率: {latest_cr['current_ratio']:.2f}")
            logger.info(f"      压力异常年份: {pressure_abnormal_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['pressure_ratio'],
                'trend': trend,
                'details': {
                    'pressure_ratio_latest': latest['pressure_ratio'],
                    'current_ratio_latest': latest_cr['current_ratio'],
                    'pressure_abnormal_years': pressure_abnormal_years,
                    'current_ratio_abnormal_years': current_ratio_abnormal_years,
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_dual_debt_high(self) -> Dict:
        """
        18. 长短期借款双高检测

        检测标准：
        - 短期借款 > 30% 资产
        - 长期借款 > 20% 资产
        """
        logger.info("  [18] 长短期借款双高检测...")
        
        if self.balance.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '资产负债表数据缺失'}}
        
        try:
            results = []
            for _, row in self.balance.iterrows():
                try:
                    short_loan = row.get('short_loan', 0) or 0
                    long_loan = row.get('long_loan', 0) or 0
                    total_assets = row.get('total_assets', 0) or 1
                    monetary_cap = row.get('monetary_cap', 0) or 0
                    
                    short_ratio = short_loan / total_assets if total_assets > 0 else 0
                    long_ratio = long_loan / total_assets if total_assets > 0 else 0
                    
                    # 检查现金是否紧张
                    cash_strained = monetary_cap < (short_loan + long_loan) * 0.3
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'short_ratio': short_ratio,
                        'long_ratio': long_ratio,
                        'cash_strained': cash_strained,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['dual_debt_high']
            
            # 双高年数
            dual_high_years = sum(1 for r in results 
                                 if r['short_ratio'] > threshold['short_ratio']
                                 and r['long_ratio'] > threshold['long_ratio'])
            
            # 双高+现金紧张年数
            severe_years = sum(1 for r in results 
                              if r['short_ratio'] > threshold['short_ratio']
                              and r['long_ratio'] > threshold['long_ratio']
                              and r['cash_strained'])
            
            latest = results[-1]
            
            # 评分
            if severe_years >= 2:
                score = 3
            elif dual_high_years >= 2:
                score = 2
            elif dual_high_years >= 1:
                score = 1
            else:
                score = 0
            
            trend = self._analyze_trend([r['short_ratio'] + r['long_ratio'] for r in results])
            
            logger.info(f"      最新短期借款占比: {latest['short_ratio']*100:.1f}%")
            logger.info(f"      最新长期借款占比: {latest['long_ratio']*100:.1f}%")
            logger.info(f"      双高年份: {dual_high_years} 年")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': latest['short_ratio'] + latest['long_ratio'],
                'trend': trend,
                'details': {
                    'short_ratio_latest': latest['short_ratio'],
                    'long_ratio_latest': latest['long_ratio'],
                    'dual_high_years': dual_high_years,
                    'cash_strained': latest['cash_strained'],
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    # ========== 审计治理风险 ==========

    def calc_auditor_changes(self) -> Dict:
        """
        19. 频繁更换审计机构检测

        检测标准：
        - 5年内更换审计机构 ≥ 2次
        """
        logger.info("  [19] 频繁更换审计机构检测...")
        
        if self.audit.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '审计数据缺失'}}
        
        try:
            audit_sorted = self.audit.sort_values('end_date')
            
            # 获取审计机构变更记录
            auditors = []
            for _, row in audit_sorted.iterrows():
                try:
                    auditor = row.get('audit_agency', '')
                    if auditor:
                        auditors.append({
                            'end_date': row.get('end_date'),
                            'auditor': auditor,
                        })
                except Exception as e:
                    continue
            
            if len(auditors) < 2:
                return {'score': 0, 'value': 0, 'trend': '数据不足', 
                        'details': {'error': '审计数据不足'}}
            
            # 统计变更次数
            changes = 0
            change_dates = []
            for i in range(1, len(auditors)):
                if auditors[i]['auditor'] != auditors[i-1]['auditor']:
                    changes += 1
                    change_dates.append(auditors[i]['end_date'])
            
            threshold = self.THRESHOLDS['auditor_changes']
            
            # 评分
            if changes >= threshold['count']:
                score = 3
            elif changes >= 1:
                score = 1
            else:
                score = 0
            
            logger.info(f"      审计机构变更次数: {changes} 次")
            logger.info(f"      变更年份: {change_dates}")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': changes,
                'trend': '无法判断',
                'details': {
                    'change_count': changes,
                    'change_dates': change_dates,
                    'auditors': [a['auditor'] for a in auditors[-5:]],  # 最近5年审计机构
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def calc_non_standard_opinion(self) -> Dict:
        """
        20. 静标审计意见检测

        检测标准：
        - 审计意见为非标准无保留意见
        """
        logger.info("  [20] 静标审计意见检测...")
        
        if self.audit.empty:
            return {'score': 0, 'value': 0, 'trend': '数据缺失', 'details': {'error': '审计数据缺失'}}
        
        try:
            audit_sorted = self.audit.sort_values('end_date')
            
            results = []
            for _, row in audit_sorted.iterrows():
                try:
                    audit_result = row.get('audit_result', '')
                    
                    results.append({
                        'end_date': row.get('end_date'),
                        'audit_result': audit_result,
                    })
                except Exception as e:
                    continue
            
            if not results:
                return {'score': 0, 'value': 0, 'trend': '数据缺失', 
                        'details': {'error': '无有效数据'}}
            
            threshold = self.THRESHOLDS['non_standard_opinion']
            
            # 审计意见类型判断
            # Tushare审计意见编码: 1=标准无保留, 2=无保留带强调, 3=保留, 4=否定, 5=无法表示
            latest = results[-1]
            
            # 检查是否有非标意见
            non_standard_found = any(r['audit_result'] in threshold['types'] for r in results)
            
            # 最新审计意见评分
            if latest['audit_result'] in ['4', '5']:  # 否定/无法表示
                score = 3
            elif latest['audit_result'] == '3':  # 保留意见
                score = 2
            elif latest['audit_result'] == '2':  # 带强调事项
                score = 1
            else:
                score = 0
            
            # 历史上有非标意见，增加风险提示
            if non_standard_found and score == 0:
                score = 1  # 历史有非标，即使现在是标准也值得关注
            
            logger.info(f"      最新审计意见: {latest['audit_result']}")
            logger.info(f"      历史非标意见: {non_standard_found}")
            logger.info(f"      ⚠️ 评分: {score} 分")
            
            return {
                'score': score,
                'value': int(latest['audit_result']),
                'trend': '无法判断',
                'details': {
                    'audit_result_latest': latest['audit_result'],
                    'audit_result_desc': self._get_audit_opinion_desc(latest['audit_result']),
                    'non_standard_found': non_standard_found,
                    'audit_history': [r['audit_result'] for r in results[-5:]],
                }
            }
        except Exception as e:
            logger.error(f"      计算失败: {e}")
            return {'score': 0, 'value': 0, 'trend': '计算异常', 'details': {'error': str(e)}}

    def _get_audit_opinion_desc(self, code: str) -> str:
        """获取审计意见描述"""
        mapping = {
            '1': '标准无保留意见',
            '2': '无保留意见带强调事项',
            '3': '保留意见',
            '4': '否定意见',
            '5': '无法表示意见',
        }
        return mapping.get(code, '未知类型')

    def calc_executive_departures(self) -> Dict:
        """
        21. 高管频繁离职检测

        检测标准：
        - CFO/董秘在3年内更换 ≥ 2次
        
        注：需要高管变动数据，Tushare有stk_managers接口
        """
        logger.info("  [21] 高管频繁离职检测...")
        
        # Tushare stk_managers接口需要额外调用
        # 这里返回提示，需要从数据获取器补充
        logger.warning("      ⚠️ 需从stk_managers接口获取高管变动数据")
        
        return {
            'score': 0,
            'value': 0,
            'trend': '数据缺失',
            'details': {
                'error': '需高管变动数据',
                'note': '需调用Tushare stk_managers接口获取',
                'items': [
                    'CFO姓名及变动记录',
                    '董秘姓名及变动记录',
                    '高管离职公告',
                ],
                'threshold_count': self.THRESHOLDS['executive_departures']['count'],
                'threshold_years': self.THRESHOLDS['executive_departures']['years'],
            }
        }


if __name__ == "__main__":
    # 测试用例
    print("=" * 60)
    print("风险指标计算器测试")
    print("=" * 60)
    
    # 创建模拟数据
    import pandas as pd
    
    mock_balance = pd.DataFrame([
        {'end_date': '20221231', 'monetary_cap': 1e9, 'total_assets': 10e9, 
         'short_loan': 3e9, 'long_loan': 2e9, 'accounts_receiv': 2e9,
         'inventory': 1.5e9, 'goodwill': 1e9, 'total_hldr_equity': 3e9,
         'total_liab': 7e9, 'current_assets': 4e9, 'current_liab': 3.5e9},
        {'end_date': '20231231', 'monetary_cap': 1.2e9, 'total_assets': 11e9,
         'short_loan': 3.5e9, 'long_loan': 2.5e9, 'accounts_receiv': 2.5e9,
         'inventory': 2e9, 'goodwill': 1.2e9, 'total_hldr_equity': 3.3e9,
         'total_liab': 7.7e9, 'current_assets': 4.5e9, 'current_liab': 4e9},
    ])
    
    mock_income = pd.DataFrame([
        {'end_date': '20221231', 'revenue': 8e9, 'oper_cost': 6e9, 'net_profit': 0.5e9,
         'sell_exp': 0.3e9, 'asset_impair_loss': 0.1e9},
        {'end_date': '20231231', 'revenue': 9e9, 'oper_cost': 7e9, 'net_profit': 0.6e9,
         'sell_exp': 0.35e9, 'asset_impair_loss': 0.3e9},
    ])
    
    mock_cashflow = pd.DataFrame([
        {'end_date': '20221231', 'net_cash_flows_oper_act': 0.3e9},
        {'end_date': '20231231', 'net_cash_flows_oper_act': 0.2e9},
    ])
    
    mock_data = {
        'balance': mock_balance,
        'income': mock_income,
        'cashflow': mock_cashflow,
        'fina_indicator': pd.DataFrame(),
        'audit': pd.DataFrame(),
    }
    
    calculator = RiskCalculator(mock_data)
    results = calculator.calculate_all_indicators()
    
    print("\n测试结果:")
    for key, value in results.items():
        if key != '_summary':
            print(f"{key}: {value['score']} 分")
    
    print("\n总结:")
    print(results['_summary'])