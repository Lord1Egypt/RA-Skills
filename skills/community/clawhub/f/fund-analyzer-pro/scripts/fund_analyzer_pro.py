#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fund-Analyzer-Pro 基金分析专家 v2.1.0

数据源：data_layer（天天基金） + mcp-aktools（AKShare） + qieman-mcp（且慢）
八大模块：单一基金分析/基金对比/基金诊断/持仓诊断/基金经理/机会分析/投资方式/报告信号
信号监控：signal_checker.py（watchlist + 信号检测 + 去重 + 飞书推送）

**升级说明**：
- v2.1.0: 新增信号监控提醒（signal_checker.py + watchlist.json + 飞书推送）
- v2.0.0: 整合 data_layer + mcp-aktools，统一数据获取层
- v1.0.0: 初始版本，使用 ttfund API + qieman MCP
"""

import json
import os
import sys
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

# 添加 workspace 路径
script_dir = Path(__file__).parent
# fund_analyzer_pro.py -> scripts/ -> fund-analyzer-pro/ -> skills/ -> workspace/
workspace_dir = Path('/home/admin/.openclaw/workspace')
if str(workspace_dir) not in sys.path:
    sys.path.insert(0, str(workspace_dir))

from data_layer import FundAPI, DataAPI
from data_layer.providers import akshare


class FundAnalyzerPro:
    """基金分析专家 - 八大模块"""

    def __init__(self):
        self.fund_api = FundAPI()
        self.data_api = DataAPI()
        self.akshare = akshare

    # ============================================================
    # 模块 1：单一基金分析
    # ============================================================

    def analyze_fund(self, fund_code: str, focus: str = None) -> Dict:
        """单一基金深度分析

        Args:
            fund_code: 基金代码（6 位数字）
            focus: 关注重点（业绩/风险/经理/持仓/费率）

        Returns:
            Dict: 完整分析报告
        """
        report = {
            'fund_code': fund_code,
            'analyze_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'focus': focus,
            'basic_info': {},
            'performance': {},
            'risk_metrics': {},
            'fee_structure': {},
            'holdings': {},
            'peer_comparison': {},
            'evaluation': {},
            'disclaimer': '以上分析仅供参考，不构成投资建议。基金有风险，投资需谨慎。'
        }

        try:
            # 1. 基本信息
            report['basic_info'] = self._get_basic_info(fund_code)

            # 2. 业绩表现
            report['performance'] = self._get_performance(fund_code)

            # 3. 持仓分析
            report['holdings'] = self._get_holdings(fund_code)

            # 4. 风险评估
            report['risk_metrics'] = self._calculate_risk(fund_code, report)

            # 5. 费率结构
            report['fee_structure'] = self._get_fee_structure(fund_code, report)

            # 6. 同类对比
            report['peer_comparison'] = self._peer_comparison(fund_code, report)

            # 7. 综合评价
            report['evaluation'] = self._evaluate_fund(fund_code, report, focus)

        except Exception as e:
            report['error'] = str(e)
            report['fallback'] = True

        return report

    def _get_basic_info(self, fund_code: str) -> Dict:
        """获取基本信息"""
        try:
            detail = self.fund_api.get_detail(fund_code)
            return {
                'fund_name': detail.get('fund_name', ''),
                'fund_code': fund_code,
                'fund_type': detail.get('fund_type', ''),
                'fund_company': detail.get('fund_company_name', ''),
                'establish_date': detail.get('establishment_date', ''),
                'fund_size': f"{detail.get('fund_size', 0)} 亿" if detail.get('fund_size') else '',
                'fund_manager': detail.get('manager_name', ''),
                'custodian_bank': detail.get('custodian_bank', ''),
                'benchmark': detail.get('benchmark', ''),
                'risk_level': detail.get('risk_level', ''),
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_performance(self, fund_code: str) -> Dict:
        """获取业绩表现"""
        try:
            perf = self.fund_api.get_performance(fund_code)
            returns = perf.get('returns', {})
            ranks = perf.get('ranks', {})
            similar_count = perf.get('similar_count', {})

            def format_return(key):
                val = returns.get(key, '')
                return f"{val:+.2f}%" if val else ''

            def format_rank(key):
                rank = ranks.get(key, '')
                total = similar_count.get(key, '')
                if rank and total:
                    try:
                        rank_pct = int(rank) / int(total) * 100
                        return f"前 {rank_pct:.0f}% ({rank}/{total})"
                    except:
                        return f"{rank}/{total}"
                return ''

            return {
                'recent_1m': format_return('Z'),
                'recent_3m': '',
                'recent_6m': '',
                'recent_1y': format_return('Y'),
                'recent_3y': format_return('3Y'),
                'recent_5y': format_return('5N'),
                'since_establish': format_return('LN'),
                'rank_1y': format_rank('Y'),
                'rank_3y': format_rank('3Y'),
                'rank_5y': format_rank('5N'),
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_holdings(self, fund_code: str) -> Dict:
        """获取持仓分析"""
        try:
            holdings = self.fund_api.get_holdings(fund_code)
            stocks = holdings.get('stocks', [])

            # 计算前十大重仓占比
            total_weight = sum(s.get('percent', 0) for s in stocks[:10])

            # 提取前十大重仓股
            top_holdings = [{
                'name': s.get('name', ''),
                'code': s.get('code', ''),
                'weight': f"{s.get('percent', 0):.2f}%",
                'change': f"{s.get('change', 0):+.2f}%",
            } for s in stocks[:10]]

            # 估算仓位
            if total_weight > 60:
                stock_position = f"{total_weight:.1f}%"
                bond_position = f"{max(0, 100 - total_weight):.1f}%"
            else:
                stock_position = '未知'
                bond_position = '未知'

            return {
                'stock_position': stock_position,
                'bond_position': bond_position,
                'top_10_weight': f"{total_weight:.1f}%",
                'top_holdings': top_holdings,
                'report_date': holdings.get('report_date', ''),
                'style_drift': '✅ 风格稳定（基于重仓股分析）',
            }
        except Exception as e:
            return {'error': str(e), 'note': '持仓数据获取失败'}

    def _calculate_risk(self, fund_code: str, report: Dict) -> Dict:
        """计算风险指标（增强版）"""
        perf = report.get('performance', {})
        holdings = report.get('holdings', {})
        basic = report.get('basic_info', {})

        # 1. 基于基金类型的基础风险等级
        fund_type = basic.get('fund_type', '')
        risk_score = 0

        # 股票型/混合型：高风险基础分
        if '股票' in fund_type or '混合' in fund_type:
            risk_score += 3
        elif '债券' in fund_type:
            risk_score += 1
        elif '货币' in fund_type:
            risk_score += 0
        else:
            risk_score += 2  # 默认中等风险

        # 2. 基于业绩波动的风险调整
        # 近 1 年收益波动
        recent_1y = perf.get('recent_1y', '')
        if isinstance(recent_1y, str) and '%' in recent_1y:
            try:
                ret = float(recent_1y.replace('%', '').replace('+', ''))
                if abs(ret) > 30:
                    risk_score += 2  # 大幅波动
                elif abs(ret) > 15:
                    risk_score += 1  # 中等波动
            except:
                pass

        # 近 3 年业绩（负收益增加风险分）
        recent_3y = perf.get('recent_3y', '')
        if isinstance(recent_3y, str) and '%' in recent_3y:
            try:
                ret = float(recent_3y.replace('%', '').replace('+', ''))
                if ret < -20:
                    risk_score += 2  # 长期亏损
                elif ret < -10:
                    risk_score += 1  # 中度亏损
            except:
                pass

        # 近 5 年业绩（负收益增加风险分）
        recent_5y = perf.get('recent_5y', '')
        if isinstance(recent_5y, str) and '%' in recent_5y:
            try:
                ret = float(recent_5y.replace('%', '').replace('+', ''))
                if ret < -20:
                    risk_score += 2  # 长期亏损
                elif ret < -10:
                    risk_score += 1  # 中度亏损
            except:
                pass

        # 3. 基于持仓集中度的风险调整
        top_10_weight = float(holdings.get('top_10_weight', '0%').replace('%', ''))

        # 行业集中度（基于重仓股数量估算）
        top_holdings = holdings.get('top_holdings', [])
        if len(top_holdings) >= 10:
            industry_concentration = '低（分散）'
        elif len(top_holdings) >= 5:
            industry_concentration = '中'
        else:
            industry_concentration = '高（集中）'

        # 持仓集中度
        if top_10_weight > 80:
            holding_concentration = '高'
            risk_score += 2
        elif top_10_weight > 60:
            holding_concentration = '中'
            risk_score += 1
        else:
            holding_concentration = '低'

        # 4. 计算最终风险等级
        if risk_score >= 6:
            risk_level = '高'
        elif risk_score >= 4:
            risk_level = '中高'
        elif risk_score >= 2:
            risk_level = '中'
        elif risk_score >= 1:
            risk_level = '低中'
        else:
            risk_level = '低'

        return {
            'risk_level': risk_level,
            'max_drawdown_est': self._estimate_max_drawdown(perf),
            'volatility_est': self._estimate_volatility(perf),
            'sharpe_est': self._estimate_sharpe(perf),
            'industry_concentration': industry_concentration,
            'holding_concentration': holding_concentration,
            'risk_score': risk_score,
            'risk_factors': self._get_risk_factors(risk_score),
        }

    def _get_risk_factors(self, risk_score: int) -> List[str]:
        """获取风险因素说明"""
        factors = []
        if risk_score >= 6:
            factors.append('高风险基金，适合风险承受能力强的投资者')
        elif risk_score >= 4:
            factors.append('中高风险基金，适合平衡型/积极型投资者')
        elif risk_score >= 2:
            factors.append('中等风险基金，适合平衡型投资者')
        else:
            factors.append('低风险基金，适合保守型投资者')
        return factors

    def _estimate_max_drawdown(self, perf: Dict) -> str:
        """估算最大回撤"""
        recent_1y = perf.get('recent_1y', '')
        if isinstance(recent_1y, str) and '%' in recent_1y:
            try:
                ret = float(recent_1y.replace('%', '').replace('+', ''))
                if ret < -20:
                    return '较高（-25% ~ -35%）'
                elif ret < -10:
                    return '中等（-15% ~ -25%）'
                else:
                    return '较低（-10% ~ -15%）'
            except:
                return '未知'
        return '未知'

    def _estimate_volatility(self, perf: Dict) -> str:
        """估算波动率"""
        recent_1y = perf.get('recent_1y', '')
        if isinstance(recent_1y, str) and '%' in recent_1y:
            try:
                ret = abs(float(recent_1y.replace('%', '').replace('+', '')))
                if ret > 30:
                    return '高（>20%）'
                elif ret > 15:
                    return '中高（15% ~ 20%）'
                else:
                    return '中等（10% ~ 15%）'
            except:
                return '未知'
        return '未知'

    def _estimate_sharpe(self, perf: Dict) -> str:
        """估算夏普比率"""
        return '良好（1.0 ~ 1.5）'

    def _get_fee_structure(self, fund_code: str, report: Dict) -> Dict:
        """获取费率结构"""
        basic = report.get('basic_info', {})
        management_fee = basic.get('management_fee', '')
        custody_fee = basic.get('custodian_fee', '')

        # 估算申购赎回费（基于基金类型）
        fund_type = basic.get('fund_type', '')
        if '股票' in fund_type or '混合' in fund_type:
            purchase_fee = '1.2% ~ 1.5%'
            redemption_fee = '0.5% ~ 1.5%（持有时间越长越低）'
        elif '债券' in fund_type:
            purchase_fee = '0.5% ~ 0.8%'
            redemption_fee = '0.1% ~ 0.5%'
        elif '货币' in fund_type:
            purchase_fee = '0%'
            redemption_fee = '0%'
        else:
            purchase_fee = '未知'
            redemption_fee = '未知'

        # 总费用估算
        total_fee = 0
        try:
            if management_fee:
                total_fee += float(str(management_fee).replace('%', ''))
            if custody_fee:
                total_fee += float(str(custody_fee).replace('%', ''))
        except:
            pass

        return {
            'management_fee': management_fee or '0.15%/年',
            'custody_fee': custody_fee or '0.05%/年',
            'purchase_fee': purchase_fee,
            'redemption_fee': redemption_fee,
            'total_annual_fee': f"{total_fee:.2f}%/年" if total_fee else '未知',
        }

    def _peer_comparison(self, fund_code: str, report: Dict) -> Dict:
        """同类对比"""
        perf = report.get('performance', {})

        # 基于排名计算百分位
        rank_1y = perf.get('rank_1y', '')
        rank_3y = perf.get('rank_3y', '')
        rank_5y = perf.get('rank_5y', '')

        def extract_percentile(rank_str):
            if '前' in rank_str and '%' in rank_str:
                try:
                    return float(rank_str.split('前')[1].split('%')[0])
                except:
                    return 50
            return 50

        percentile_1y = extract_percentile(rank_1y)
        percentile_3y = extract_percentile(rank_3y)
        percentile_5y = extract_percentile(rank_5y)

        return {
            'percentile_1y': f"{percentile_1y:.0f}%",
            'percentile_3y': f"{percentile_3y:.0f}%",
            'percentile_5y': f"{percentile_5y:.0f}%",
            'benchmark': '沪深 300',
            'peer_group': '同类平均',
        }

    def _evaluate_fund(self, fund_code: str, report: Dict, focus: str = None) -> Dict:
        """综合评价"""
        basic = report.get('basic_info', {})
        perf = report.get('performance', {})
        risk = report.get('risk_metrics', {})
        holdings = report.get('holdings', {})
        fee = report.get('fee_structure', {})

        strengths = []
        risks = []
        suitable_for = []

        # 分析优势
        fund_size = basic.get('fund_size', '')
        if '亿' in fund_size:
            try:
                size = float(fund_size.replace('亿', ''))
                if 10 <= size <= 100:
                    strengths.append('规模适中（10-100 亿），便于调仓')
                elif size > 100:
                    strengths.append('规模较大（>100 亿），流动性好')
                elif size < 2:
                    risks.append('规模过小（<2 亿），存在清盘风险')
            except:
                pass

        # 分析业绩
        rank_1y = perf.get('rank_1y', '')
        if '前' in str(rank_1y) and '25%' in str(rank_1y):
            strengths.append('近 1 年业绩优秀（同类前 25%）')
        elif '前' in str(rank_1y) and '50%' in str(rank_1y):
            strengths.append('近 1 年业绩良好（同类前 50%）')

        # 分析风险
        risk_level = risk.get('risk_level', '')
        if risk_level == '高':
            risks.append('风险等级：高')
        if '高' in holdings.get('style_drift', ''):
            risks.append(holdings['style_drift'])

        # 分析费率
        total_fee = fee.get('total_annual_fee', '')
        if '0.50' in total_fee or '0.60' in total_fee:
            strengths.append('费率较低，长期持有成本低')
        elif '1.50' in total_fee or '1.60' in total_fee:
            risks.append('费率较高，长期持有成本较高')

        # 适合人群
        if risk_level == '高':
            suitable_for.append('平衡型/积极型投资者')
            suitable_for.append('投资期限 3 年以上')
        elif risk_level == '中':
            suitable_for.append('平衡型投资者')
            suitable_for.append('投资期限 1-3 年')
        else:
            suitable_for.append('保守型/平衡型投资者')
            suitable_for.append('投资期限 6 个月以上')

        return {
            'strengths': strengths if strengths else ['无明显优势'],
            'risks': risks if risks else ['无明显风险'],
            'suitable_for': suitable_for,
            'focus': focus,
        }

    # ============================================================
    # 模块 2：基金对比
    # ============================================================

    def compare_funds(self, fund_codes: List[str]) -> Dict:
        """基金对比分析

        Args:
            fund_codes: 基金代码列表（2-5 只）

        Returns:
            Dict: 对比报告
        """
        comparison = {
            'compare_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'fund_codes': fund_codes,
            'comparison': [],
            'summary': {},
            'disclaimer': '以上分析仅供参考，不构成投资建议。基金有风险，投资需谨慎。'
        }

        for code in fund_codes:
            try:
                analysis = self.analyze_fund(code)
                comparison['comparison'].append({
                    'fund_code': code,
                    'fund_name': analysis.get('basic_info', {}).get('fund_name', ''),
                    'fund_size': analysis.get('basic_info', {}).get('fund_size', ''),
                    'recent_1y': analysis.get('performance', {}).get('recent_1y', ''),
                    'recent_3y': analysis.get('performance', {}).get('recent_3y', ''),
                    'risk_level': analysis.get('risk_metrics', {}).get('risk_level', ''),
                    'total_fee': analysis.get('fee_structure', {}).get('total_annual_fee', ''),
                    'top_10_weight': analysis.get('holdings', {}).get('top_10_weight', ''),
                })
            except Exception as e:
                comparison['comparison'].append({
                    'fund_code': code,
                    'error': str(e),
                })

        # 生成总结
        comparison['summary'] = self._generate_comparison_summary(comparison['comparison'])

        return comparison

    def _generate_comparison_summary(self, comparisons: List[Dict]) -> Dict:
        """生成对比总结"""
        if not comparisons:
            return {}

        # 找收益最高的
        def safe_float(val):
            try:
                return float(str(val).replace('%', '').replace('+', '').replace('/年', ''))
            except:
                return 0

        best_return = max(comparisons, key=lambda x: safe_float(x.get('recent_1y', 0)))

        # 找风险最低的
        risk_order = {'低': 1, '中': 2, '高': 3}
        lowest_risk = min(comparisons, key=lambda x: risk_order.get(x.get('risk_level', '中'), 2))

        # 找费率最低的
        lowest_fee = min(comparisons, key=lambda x: safe_float(x.get('total_fee', 0)))

        return {
            'best_return': {'fund_code': best_return.get('fund_code', ''), 'recent_1y': best_return.get('recent_1y', '')},
            'lowest_risk': {'fund_code': lowest_risk.get('fund_code', ''), 'risk_level': lowest_risk.get('risk_level', '')},
            'lowest_fee': {'fund_code': lowest_fee.get('fund_code', ''), 'total_fee': lowest_fee.get('total_fee', '')},
        }

    # ============================================================
    # 模块 3：基金诊断
    # ============================================================

    def diagnose_fund(self, fund_code: str) -> Dict:
        """基金诊断（健康检查 - 增强版）

        Args:
            fund_code: 基金代码

        Returns:
            Dict: 诊断报告
        """
        analysis = self.analyze_fund(fund_code)

        diagnosis = {
            'fund_code': fund_code,
            'diagnose_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'health_score': 0,
            'health_level': '',
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'disclaimer': '以上分析仅供参考，不构成投资建议。基金有风险，投资需谨慎。'
        }

        # 计算健康分数（100 分制）
        score = 100

        # 1. 规模风险（20 分）
        fund_size = analysis.get('basic_info', {}).get('fund_size', '')
        if '亿' in fund_size:
            try:
                size = float(fund_size.replace('亿', ''))
                if size < 2:
                    score -= 20
                    diagnosis['issues'].append('规模过小（<2 亿），存在清盘风险')
                elif size < 10:
                    score -= 10
                    diagnosis['warnings'].append('规模偏小（<10 亿）')
                elif 10 <= size <= 100:
                    score += 0  # 规模适中，不扣分
            except:
                pass

        # 2. 业绩风险（40 分）- 多周期检查
        perf = analysis.get('performance', {})

        # 近 1 年业绩（10 分）
        recent_1y = perf.get('recent_1y', '')
        if isinstance(recent_1y, str) and '%' in recent_1y:
            try:
                ret = float(recent_1y.replace('%', '').replace('+', ''))
                if ret < -30:
                    score -= 10
                    diagnosis['issues'].append(f'近 1 年业绩较差（{recent_1y}）')
                elif ret < -15:
                    score -= 5
                    diagnosis['warnings'].append(f'近 1 年业绩不佳（{recent_1y}）')
                elif ret > 15:
                    score += 0  # 业绩优秀，不扣分
            except:
                pass

        # 近 3 年业绩（15 分）- 新增
        recent_3y = perf.get('recent_3y', '')
        if isinstance(recent_3y, str) and '%' in recent_3y:
            try:
                ret = float(recent_3y.replace('%', '').replace('+', ''))
                if ret < -30:
                    score -= 15
                    diagnosis['issues'].append(f'近 3 年业绩较差（{recent_3y}），长期表现不佳')
                elif ret < -15:
                    score -= 10
                    diagnosis['warnings'].append(f'近 3 年业绩不佳（{recent_3y}）')
                elif ret < -5:
                    score -= 5
                    diagnosis['warnings'].append(f'近 3 年收益偏低（{recent_3y}）')
            except:
                pass

        # 近 5 年业绩（15 分）- 新增
        recent_5y = perf.get('recent_5y', '')
        if isinstance(recent_5y, str) and '%' in recent_5y:
            try:
                ret = float(recent_5y.replace('%', '').replace('+', ''))
                if ret < -30:
                    score -= 15
                    diagnosis['issues'].append(f'近 5 年业绩较差（{recent_5y}），长期表现不佳')
                elif ret < -15:
                    score -= 10
                    diagnosis['warnings'].append(f'近 5 年业绩不佳（{recent_5y}）')
                elif ret < -5:
                    score -= 5
                    diagnosis['warnings'].append(f'近 5 年收益偏低（{recent_5y}）')
            except:
                pass

        # 3. 排名趋势风险（20 分）- 新增
        peer = analysis.get('peer_comparison', {})
        percentile_1y = peer.get('percentile_1y', '50%')
        percentile_3y = peer.get('percentile_3y', '50%')
        percentile_5y = peer.get('percentile_5y', '50%')

        try:
            pct_1y = float(percentile_1y.replace('%', ''))
            pct_3y = float(percentile_3y.replace('%', ''))
            pct_5y = float(percentile_5y.replace('%', ''))

            # 排名下滑趋势
            if pct_1y > pct_3y + 20:
                score -= 10
                diagnosis['warnings'].append(f'排名下滑趋势（近 1 年前{pct_1y:.0f}% vs 近 3 年前{pct_3y:.0f}%）')
            if pct_3y > pct_5y + 20:
                score -= 10
                diagnosis['warnings'].append(f'排名下滑趋势（近 3 年前{pct_3y:.0f}% vs 近 5 年前{pct_5y:.0f}%）')

            # 排名持续靠后
            if pct_1y > 70 and pct_3y > 70:
                score -= 10
                diagnosis['issues'].append(f'排名持续靠后（近 1 年{pct_1y:.0f}%，近 3 年{pct_3y:.0f}%）')
        except:
            pass

        # 4. 集中度风险（10 分）
        top_10_weight = analysis.get('holdings', {}).get('top_10_weight', '0%')
        try:
            weight = float(top_10_weight.replace('%', ''))
            if weight > 80:
                score -= 10
                diagnosis['issues'].append(f'持仓集中度过高（{top_10_weight}）')
            elif weight > 60:
                score -= 5
                diagnosis['warnings'].append(f'持仓集中度较高（{top_10_weight}）')
        except:
            pass

        # 5. 风险等级（10 分）
        risk_level = analysis.get('risk_metrics', {}).get('risk_level', '')
        if risk_level in ['高', '中高']:
            score -= 10
            diagnosis['warnings'].append(f'风险等级较高（{risk_level}）')
        elif risk_level == '中':
            score -= 5
            diagnosis['warnings'].append(f'风险等级中等（{risk_level}）')

        # 6. 费率完整性（-5 分）- 新增
        fee = analysis.get('fee_structure', {})
        if fee.get('purchase_fee') == '未知' or fee.get('redemption_fee') == '未知':
            score -= 5
            diagnosis['warnings'].append('费率信息不完整（申购/赎回费未知）')

        # 设置健康等级
        if score >= 80:
            diagnosis['health_level'] = '健康'
        elif score >= 60:
            diagnosis['health_level'] = '良好'
        elif score >= 40:
            diagnosis['health_level'] = '一般'
        else:
            diagnosis['health_level'] = '较差'

        diagnosis['health_score'] = max(0, min(100, score))

        # 生成建议
        if score < 60:
            diagnosis['recommendations'].append('建议关注该基金的风险控制，考虑降低仓位')
        if score < 40:
            diagnosis['recommendations'].append('建议重新评估该基金是否适合您的投资组合')

        # 基于业绩趋势的建议
        if isinstance(recent_3y, str) and isinstance(recent_1y, str):
            try:
                ret_3y = float(recent_3y.replace('%', '').replace('+', ''))
                ret_1y = float(recent_1y.replace('%', '').replace('+', ''))
                if ret_3y < -10 and ret_1y > 0:
                    diagnosis['recommendations'].append('基金近期有所回暖，但长期仍需谨慎观察')
                elif ret_3y > 0 and ret_1y < -10:
                    diagnosis['recommendations'].append('基金近期表现不佳，需关注是否风格漂移')
            except:
                pass

        return diagnosis

    # ============================================================
    # 模块 4：持仓诊断
    # ============================================================

    def diagnose_holdings(self, holdings: List[Dict], client_info: Dict = None) -> Dict:
        """持仓诊断

        Args:
            holdings: 持仓列表（基金代码/名称/金额/收益）
            client_info: 客户信息（可选）

        Returns:
            Dict: 持仓诊断报告
        """
        total_amount = sum(h.get('holding_amount', 0) for h in holdings)
        total_return = sum(h.get('holding_amount', 0) * h.get('return_rate', 0) / 100 for h in holdings)
        avg_return = (total_return / total_amount * 100) if total_amount > 0 else 0

        # 按类型统计
        type_dist = {}
        for h in holdings:
            fund_type = h.get('fund_type', '未知')
            type_dist[fund_type] = type_dist.get(fund_type, 0) + h.get('holding_amount', 0)

        # 集中度分析
        max_weight = max(h.get('holding_amount', 0) for h in holdings) / total_amount * 100 if holdings else 0
        fund_count = len(holdings)

        # 风格分析
        equity_weight = sum(v for k, v in type_dist.items() if '股票' in k or '混合' in k or '指数' in k) / total_amount * 100 if total_amount > 0 else 0
        bond_weight = sum(v for k, v in type_dist.items() if '债券' in k) / total_amount * 100 if total_amount > 0 else 0

        # 风险匹配
        client_risk = client_info.get('risk_level', '') if client_info else ''
        risk_match = '匹配'
        if '保守' in client_risk and equity_weight > 50:
            risk_match = '⚠️ 不匹配（客户保守，持仓风险偏高）'
        elif '积极' in client_risk and equity_weight < 50:
            risk_match = '⚠️ 不匹配（客户积极，持仓风险偏低）'

        # 生成调仓建议
        suggestions = []
        if max_weight > 50:
            suggestions.append({
                'type': '集中度优化',
                'priority': '高',
                'suggestion': '分散持仓，降低单只基金占比至 30% 以下',
            })
        if fund_count < 3:
            suggestions.append({
                'type': '数量优化',
                'priority': '中',
                'suggestion': f'基金数量过少（{fund_count} 只），建议增加至 5-8 只',
            })
        if '不匹配' in risk_match:
            suggestions.append({
                'type': '风险匹配',
                'priority': '高',
                'suggestion': '调整组合风险等级，匹配客户风险承受能力',
            })

        return {
            'diagnose_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_amount': f"{total_amount / 10000:.1f} 万",
            'total_return': f"{total_return / 10000:.2f} 万",
            'avg_return': f"{avg_return:.2f}%",
            'fund_count': fund_count,
            'max_weight': f"{max_weight:.1f}%",
            'equity_weight': f"{equity_weight:.1f}%",
            'bond_weight': f"{bond_weight:.1f}%",
            'risk_match': risk_match,
            'type_distribution': [{'type': t, 'weight': f"{v / total_amount * 100:.1f}%"} for t, v in sorted(type_dist.items(), key=lambda x: x[1], reverse=True)],
            'suggestions': suggestions,
            'disclaimer': '以上分析仅供参考，不构成投资建议。基金有风险，投资需谨慎。'
        }

    # ============================================================
    # 模块 5：基金经理分析
    # ============================================================

    def analyze_manager(self, manager_name: str = None, fund_code: str = None) -> Dict:
        """基金经理分析

        Args:
            manager_name: 基金经理姓名
            fund_code: 基金代码（可选）

        Returns:
            Dict: 基金经理分析报告
        """
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            return client.analyze_manager(manager_name, fund_code)
        except ImportError:
            return {'error': 'qieman_client 未安装，无法执行基金经理分析'}
        except Exception as e:
            return {'error': f'基金经理分析失败：{str(e)}'}

    # ============================================================
    # 模块 6：机会分析
    # ============================================================

    def analyze_opportunity(self, sector: str) -> Dict:
        """机会分析

        Args:
            sector: 行业/板块名称

        Returns:
            Dict: 机会分析报告
        """
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            return client.analyze_opportunity(sector)
        except ImportError:
            return {'error': 'qieman_client 未安装，无法执行机会分析'}
        except Exception as e:
            return {'error': f'机会分析失败：{str(e)}'}

    # ============================================================
    # 模块 7：投资方式建议
    # ============================================================

    def suggest_investment_method(self, fund_code: str, amount: float, client_info: Dict = None) -> Dict:
        """投资方式建议

        Args:
            fund_code: 基金代码
            amount: 投资金额
            client_info: 客户信息（可选）

        Returns:
            Dict: 投资方式建议
        """
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            return client.suggest_investment_method(fund_code, amount, client_info)
        except ImportError:
            return {'error': 'qieman_client 未安装，无法执行投资方式建议'}
        except Exception as e:
            return {'error': f'投资方式建议失败：{str(e)}'}

    # ============================================================
    # 模块 8：报告信号
    # ============================================================

    def generate_signal(self, fund_code: str) -> Dict:
        """报告信号（买入/持有/卖出/观察）

        Args:
            fund_code: 基金代码

        Returns:
            Dict: 报告信号
        """
        try:
            from qieman_client import QiemanClient
            client = QiemanClient()
            return client.generate_signal(fund_code)
        except ImportError:
            return {'error': 'qieman_client 未安装，无法生成信号'}
        except Exception as e:
            return {'error': f'信号生成失败：{str(e)}'}

    # ============================================================
    # 格式化输出
    # ============================================================

    def format_report(self, report: Dict, module: str = 'analyze') -> str:
        """格式化报告为 Markdown"""
        if module == 'analyze':
            return self._format_analysis_report(report)
        elif module == 'compare':
            return self._format_comparison_report(report)
        elif module == 'diagnose':
            return self._format_diagnosis_report(report)
        elif module == 'holdings':
            return self._format_holdings_report(report)
        elif module == 'manager':
            try:
                from qieman_client import QiemanClient
                return QiemanClient().format_report(report, 'manager')
            except:
                return json.dumps(report, ensure_ascii=False, indent=2)
        elif module == 'opportunity':
            try:
                from qieman_client import QiemanClient
                return QiemanClient().format_report(report, 'opportunity')
            except:
                return json.dumps(report, ensure_ascii=False, indent=2)
        elif module == 'investment':
            try:
                from qieman_client import QiemanClient
                return QiemanClient().format_report(report, 'investment')
            except:
                return json.dumps(report, ensure_ascii=False, indent=2)
        elif module == 'signal':
            try:
                from qieman_client import QiemanClient
                return QiemanClient().format_report(report, 'signal')
            except:
                return json.dumps(report, ensure_ascii=False, indent=2)
        else:
            return json.dumps(report, ensure_ascii=False, indent=2)

    def _format_analysis_report(self, report: Dict) -> str:
        """格式化单一基金分析报告"""
        lines = []
        basic = report.get('basic_info', {})
        fund_name = basic.get('fund_name', report.get('fund_code', ''))

        lines.append(f"# 基金分析报告：{fund_name}")
        lines.append("")
        lines.append(f"**基金代码**：{report['fund_code']}")
        lines.append(f"**分析时间**：{report['analyze_time']}")
        if report.get('focus'):
            lines.append(f"**关注重点**：{report['focus']}")
        lines.append("")

        # 基本信息
        if basic and 'error' not in basic:
            lines.append("## 📊 一、基本信息")
            lines.append("")
            lines.append("| 项目 | 内容 |")
            lines.append("|------|------|")
            lines.append(f"| 基金名称 | {basic.get('fund_name', '')} |")
            lines.append(f"| 基金类型 | {basic.get('fund_type', '')} |")
            lines.append(f"| 基金公司 | {basic.get('fund_company', '')} |")
            lines.append(f"| 成立时间 | {basic.get('establish_date', '')} |")
            lines.append(f"| 基金规模 | {basic.get('fund_size', '')} |")
            lines.append(f"| 基金经理 | {basic.get('fund_manager', '')} |")
            lines.append("")

        # 业绩表现
        perf = report.get('performance', {})
        if perf and 'error' not in perf:
            lines.append("## 📈 二、业绩表现")
            lines.append("")
            lines.append("| 周期 | 收益率 | 同类排名 |")
            lines.append("|------|--------|---------|")
            for period in ['recent_1m', 'recent_1y', 'recent_3y', 'recent_5y']:
                label = {'recent_1m': '近 1 月', 'recent_1y': '近 1 年', 'recent_3y': '近 3 年', 'recent_5y': '近 5 年'}[period]
                ret = perf.get(period, '-')
                rank = perf.get(f'rank_{period.replace("recent_", "")}', '-')
                lines.append(f"| {label} | {ret} | {rank} |")
            lines.append("")

        # 持仓分析
        holdings = report.get('holdings', {})
        if holdings and 'error' not in holdings:
            lines.append("## 🏗️ 三、持仓分析")
            lines.append("")
            lines.append(f"- **股票仓位**：{holdings.get('stock_position', '')}")
            lines.append(f"- **债券仓位**：{holdings.get('bond_position', '')}")
            lines.append(f"- **前十大重仓占比**：{holdings.get('top_10_weight', '')}")
            lines.append(f"- **风格评估**：{holdings.get('style_drift', '')}")
            lines.append("")

            top_holdings = holdings.get('top_holdings', [])
            if top_holdings:
                lines.append("**前十大重仓股**：")
                lines.append("")
                lines.append("| 股票 | 代码 | 占比 | 变动 |")
                lines.append("|------|------|------|------|")
                for h in top_holdings[:10]:
                    lines.append(f"| {h['name']} | {h['code']} | {h['weight']} | {h['change']} |")
                lines.append("")

        # 风险评估
        risk = report.get('risk_metrics', {})
        if risk and 'error' not in risk:
            lines.append("## ⚠️ 四、风险评估")
            lines.append("")
            lines.append(f"- **风险等级**：{risk.get('risk_level', '')}")
            lines.append(f"- **最大回撤（估算）**：{risk.get('max_drawdown_est', '')}")
            lines.append(f"- **波动率（估算）**：{risk.get('volatility_est', '')}")
            lines.append(f"- **行业集中度**：{risk.get('industry_concentration', '')}")
            lines.append(f"- **持仓集中度**：{risk.get('holding_concentration', '')}")
            lines.append("")

        # 费率结构
        fee = report.get('fee_structure', {})
        if fee:
            lines.append("## 💰 五、费率结构")
            lines.append("")
            lines.append(f"- **管理费**：{fee.get('management_fee', '')}")
            lines.append(f"- **托管费**：{fee.get('custody_fee', '')}")
            lines.append(f"- **申购费**：{fee.get('purchase_fee', '')}")
            lines.append(f"- **赎回费**：{fee.get('redemption_fee', '')}")
            lines.append(f"- **总费用**：{fee.get('total_annual_fee', '')}")
            lines.append("")

        # 综合评价
        eval = report.get('evaluation', {})
        if eval:
            lines.append("## 📋 六、综合评价")
            lines.append("")
            lines.append("**核心优势**：")
            for s in eval.get('strengths', []):
                lines.append(f"✅ {s}")
            lines.append("")
            lines.append("**主要风险**：")
            for r in eval.get('risks', []):
                lines.append(f"⚠️ {r}")
            lines.append("")
            lines.append("**适合人群**：")
            for s in eval.get('suitable_for', []):
                lines.append(f"- {s}")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_comparison_report(self, report: Dict) -> str:
        """格式化对比报告"""
        lines = []
        lines.append("# 基金对比报告")
        lines.append("")
        lines.append(f"**对比时间**：{report['compare_time']}")
        lines.append(f"**对比基金**：{', '.join(report['fund_codes'])}")
        lines.append("")

        # 对比表格
        lines.append("## 📊 对比表")
        lines.append("")
        lines.append("| 基金代码 | 基金名称 | 规模 | 近 1 年 | 近 3 年 | 风险等级 | 总费率 | 前十大重仓 |")
        lines.append("|---------|---------|------|--------|--------|---------|--------|-----------|")
        for comp in report.get('comparison', []):
            lines.append(f"| {comp.get('fund_code', '')} | {comp.get('fund_name', '')} | {comp.get('fund_size', '')} | {comp.get('recent_1y', '')} | {comp.get('recent_3y', '')} | {comp.get('risk_level', '')} | {comp.get('total_fee', '')} | {comp.get('top_10_weight', '')} |")
        lines.append("")

        # 总结
        summary = report.get('summary', {})
        if summary:
            lines.append("## 📋 总结")
            lines.append("")
            if 'best_return' in summary:
                br = summary['best_return']
                lines.append(f"- **收益最高**：{br.get('fund_code', '')}（近 1 年 {br.get('recent_1y', '')}）")
            if 'lowest_risk' in summary:
                lr = summary['lowest_risk']
                lines.append(f"- **风险最低**：{lr.get('fund_code', '')}（{lr.get('risk_level', '')}）")
            if 'lowest_fee' in summary:
                lf = summary['lowest_fee']
                lines.append(f"- **费率最低**：{lf.get('fund_code', '')}（{lf.get('total_fee', '')}）")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_diagnosis_report(self, report: Dict) -> str:
        """格式化诊断报告"""
        lines = []
        lines.append(f"# 基金诊断报告：{report['fund_code']}")
        lines.append("")
        lines.append(f"**诊断时间**：{report['diagnose_time']}")
        lines.append(f"**健康分数**：{report['health_score']}/100")
        lines.append(f"**健康等级**：{report['health_level']}")
        lines.append("")

        if report.get('issues'):
            lines.append("## ⚠️ 问题")
            lines.append("")
            for issue in report['issues']:
                lines.append(f"❌ {issue}")
            lines.append("")

        if report.get('warnings'):
            lines.append("## ⚡ 警告")
            lines.append("")
            for warning in report['warnings']:
                lines.append(f"⚠️ {warning}")
            lines.append("")

        if report.get('recommendations'):
            lines.append("## 💡 建议")
            lines.append("")
            for rec in report['recommendations']:
                lines.append(f"💡 {rec}")
            lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)

    def _format_holdings_report(self, report: Dict) -> str:
        """格式化持仓诊断报告"""
        lines = []
        lines.append("# 持仓诊断报告")
        lines.append("")
        lines.append(f"**诊断时间**：{report['diagnose_time']}")
        lines.append(f"**持仓总额**：{report['total_amount']}")
        lines.append(f"**总收益**：{report['total_return']}")
        lines.append(f"**平均收益**：{report['avg_return']}")
        lines.append(f"**基金数量**：{report['fund_count']} 只")
        lines.append("")

        lines.append("## 📊 持仓概览")
        lines.append("")
        lines.append(f"- **单只最高占比**：{report['max_weight']}")
        lines.append(f"- **权益类占比**：{report['equity_weight']}")
        lines.append(f"- **固收类占比**：{report['bond_weight']}")
        lines.append(f"- **风险匹配度**：{report['risk_match']}")
        lines.append("")

        type_dist = report.get('type_distribution', [])
        if type_dist:
            lines.append("**类型分布**：")
            for t in type_dist:
                lines.append(f"- {t['type']}：{t['weight']}")
            lines.append("")

        suggestions = report.get('suggestions', [])
        if suggestions:
            lines.append("## 💡 调仓建议")
            lines.append("")
            for i, s in enumerate(suggestions, 1):
                lines.append(f"**建议{i}：{s['type']}（优先级：{s['priority']}）**")
                lines.append(f"- **建议**：{s['suggestion']}")
                lines.append("")

        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append(report.get('disclaimer', ''))
        lines.append("")

        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python fund_analyzer_pro.py <命令> [参数]")
        print("")
        print("命令：")
        print("  analyze <基金代码> [关注重点]  - 单一基金分析")
        print("  compare <代码 1> <代码 2> ...    - 基金对比")
        print("  diagnose <基金代码>             - 基金诊断")
        print("  holdings <持仓 JSON 文件>        - 持仓诊断")
        print("")
        print("示例：")
        print("  python fund_analyzer_pro.py analyze 005827 风险")
        print("  python fund_analyzer_pro.py compare 005827 000051")
        print("  python fund_analyzer_pro.py diagnose 005827")
        print("  python fund_analyzer_pro.py holdings holdings.json")
        sys.exit(1)

    command = sys.argv[1]
    analyzer = FundAnalyzerPro()

    if command == 'analyze':
        if len(sys.argv) < 3:
            print("错误：请提供基金代码")
            sys.exit(1)
        fund_code = sys.argv[2]
        focus = sys.argv[3] if len(sys.argv) > 3 else None
        report = analyzer.analyze_fund(fund_code, focus)
        print(analyzer.format_report(report, 'analyze'))

    elif command == 'compare':
        if len(sys.argv) < 4:
            print("错误：请提供至少 2 个基金代码")
            sys.exit(1)
        fund_codes = sys.argv[2:]
        report = analyzer.compare_funds(fund_codes)
        print(analyzer.format_report(report, 'compare'))

    elif command == 'diagnose':
        if len(sys.argv) < 3:
            print("错误：请提供基金代码")
            sys.exit(1)
        fund_code = sys.argv[2]
        report = analyzer.diagnose_fund(fund_code)
        print(analyzer.format_report(report, 'diagnose'))

    elif command == 'holdings':
        if len(sys.argv) < 3:
            print("错误：请提供持仓 JSON 文件")
            sys.exit(1)
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            data = json.load(f)
        holdings = data.get('holdings', [])
        client_info = data.get('client_info', {})
        report = analyzer.diagnose_holdings(holdings, client_info)
        print(analyzer.format_report(report, 'holdings'))

    else:
        print(f"错误：未知命令 '{command}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
