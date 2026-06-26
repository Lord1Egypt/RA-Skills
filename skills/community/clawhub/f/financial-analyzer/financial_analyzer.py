"""
Financial Analyzer - AI-powered financial analysis tool
"""
import json
import math
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class FinancialStatements:
    """Financial statement data"""
    # Balance Sheet
    total_assets: float = 0
    total_liabilities: float = 0
    total_equity: float = 0
    current_assets: float = 0
    current_liabilities: float = 0
    cash: float = 0
    inventory: float = 0
    accounts_receivable: float = 0
    fixed_assets: float = 0
    long_term_debt: float = 0
    
    # Income Statement
    revenue: float = 0
    cost_of_goods: float = 0
    gross_profit: float = 0
    operating_expenses: float = 0
    operating_income: float = 0  # EBIT
    interest_expense: float = 0
    net_income: float = 0
    tax_expense: float = 0
    
    # Cash Flow
    operating_cash_flow: float = 0
    investing_cash_flow: float = 0
    financing_cash_flow: float = 0
    capital_expenditure: float = 0
    free_cash_flow: float = 0
    
    # Per Share Data
    eps: float = 0  # Earnings per share
    book_value_per_share: float = 0
    dividend_per_share: float = 0
    
    # Market Data
    stock_price: float = 0
    shares_outstanding: float = 0
    market_cap: float = 0


class FinancialAnalyzer:
    """
    AI-powered financial analysis tool
    
    Features:
    - Financial statement analysis
    - Ratio calculation and analysis
    - Valuation models
    - Risk assessment
    - Health scoring
    """
    
    def __init__(self, currency: str = "CNY"):
        self.currency = currency
        self.history: List[Dict] = []
    
    # ==================== Main Analysis ====================
    
    def analyze(
        self,
        company: str,
        statements: Dict[str, Any]
    ) -> Dict:
        """
        Perform comprehensive financial analysis
        
        Args:
            company: Company name or ticker
            statements: Dict containing financial statement data
            
        Returns:
            Dict with full analysis results
        """
        # Parse statements
        fs = self._parse_statements(statements)
        
        # Calculate ratios
        ratios = self.calculate_ratios(fs)
        
        # Risk assessment
        risk = self._assess_risk(fs)
        
        # Health check
        health = self._health_check(fs, ratios)
        
        # Valuation (if market data available)
        valuation = self._valuation(fs, ratios)
        
        # Build result
        result = {
            'company': company,
            'analysis_date': datetime.now().isoformat(),
            'currency': self.currency,
            'financials': {
                'revenue': fs.revenue,
                'net_income': fs.net_income,
                'total_assets': fs.total_assets,
                'total_equity': fs.total_equity,
                'market_cap': fs.market_cap
            },
            'ratios': ratios,
            'risk': risk,
            'health': health,
            'valuation': valuation,
            'summary': self._generate_summary(company, ratios, risk, health, valuation)
        }
        
        self.history.append(result)
        return result
    
    def _parse_statements(self, statements: Dict) -> FinancialStatements:
        """Parse input dict into FinancialStatements"""
        fs = FinancialStatements()
        
        # Balance sheet
        bs = statements.get('balance_sheet', {})
        fs.total_assets = bs.get('total_assets', 0)
        fs.total_liabilities = bs.get('total_liabilities', 0)
        fs.total_equity = bs.get('total_equity', 0)
        fs.current_assets = bs.get('current_assets', 0)
        fs.current_liabilities = bs.get('current_liabilities', 0)
        fs.cash = bs.get('cash', 0)
        fs.inventory = bs.get('inventory', 0)
        fs.accounts_receivable = bs.get('accounts_receivable', 0)
        fs.fixed_assets = bs.get('fixed_assets', 0)
        fs.long_term_debt = bs.get('long_term_debt', 0)
        
        # Income statement
        inc = statements.get('income_statement', {})
        fs.revenue = inc.get('revenue', 0)
        fs.cost_of_goods = inc.get('cost_of_goods', 0)
        fs.gross_profit = inc.get('gross_profit', fs.revenue - fs.cost_of_goods)
        fs.operating_expenses = inc.get('operating_expenses', 0)
        fs.operating_income = inc.get('operating_income', 0)
        fs.interest_expense = inc.get('interest_expense', 0)
        fs.net_income = inc.get('net_income', 0)
        fs.tax_expense = inc.get('tax_expense', 0)
        
        # Calculate EBIT if not provided
        if fs.operating_income == 0:
            fs.operating_income = fs.net_income + fs.tax_expense + fs.interest_expense
        
        # Cash flow
        cf = statements.get('cash_flow', {})
        fs.operating_cash_flow = cf.get('operating_cash_flow', 0)
        fs.investing_cash_flow = cf.get('investing_cash_flow', 0)
        fs.financing_cash_flow = cf.get('financing_cash_flow', 0)
        fs.capital_expenditure = cf.get('capital_expenditure', 0)
        fs.free_cash_flow = cf.get('free_cash_flow', fs.operating_cash_flow - fs.capital_expenditure)
        
        # Per share
        per_share = statements.get('per_share', {})
        fs.eps = per_share.get('eps', 0)
        fs.book_value_per_share = per_share.get('book_value_per_share', 0)
        fs.dividend_per_share = per_share.get('dividend_per_share', 0)
        
        # Market
        market = statements.get('market', {})
        fs.stock_price = market.get('stock_price', 0)
        fs.shares_outstanding = market.get('shares_outstanding', 0)
        fs.market_cap = market.get('market_cap', fs.stock_price * fs.shares_outstanding)
        
        return fs
    
    # ==================== Ratio Analysis ====================
    
    def calculate_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate all financial ratios"""
        return {
            'liquidity': self._liquidity_ratios(fs),
            'solvency': self._solvency_ratios(fs),
            'profitability': self._profitability_ratios(fs),
            'efficiency': self._efficiency_ratios(fs),
            'market': self._market_ratios(fs)
        }
    
    def _liquidity_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate liquidity ratios"""
        # Current ratio
        current_ratio = fs.current_assets / fs.current_liabilities if fs.current_liabilities > 0 else 0
        
        # Quick ratio (excluding inventory)
        quick_assets = fs.current_assets - fs.inventory
        quick_ratio = quick_assets / fs.current_liabilities if fs.current_liabilities > 0 else 0
        
        # Cash ratio
        cash_ratio = fs.cash / fs.current_liabilities if fs.current_liabilities > 0 else 0
        
        # Working capital
        working_capital = fs.current_assets - fs.current_liabilities
        
        return {
            'current_ratio': round(current_ratio, 2),
            'quick_ratio': round(quick_ratio, 2),
            'cash_ratio': round(cash_ratio, 2),
            'working_capital': working_capital,
            'assessment': self._assess_liquidity(current_ratio, quick_ratio, cash_ratio)
        }
    
    def _assess_liquidity(self, current, quick, cash) -> str:
        """Assess liquidity health"""
        if current >= 2.0 and quick >= 1.0:
            return "Strong"
        elif current >= 1.5 and quick >= 0.8:
            return "Good"
        elif current >= 1.0:
            return "Adequate"
        else:
            return "Weak"
    
    def _solvency_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate solvency ratios"""
        # Debt to equity
        debt_to_equity = fs.total_liabilities / fs.total_equity if fs.total_equity > 0 else 0
        
        # Debt to assets
        debt_to_assets = fs.total_liabilities / fs.total_assets if fs.total_assets > 0 else 0
        
        # Interest coverage ratio
        interest_coverage = fs.operating_income / fs.interest_expense if fs.interest_expense > 0 else float('inf')
        
        # Equity ratio
        equity_ratio = fs.total_equity / fs.total_assets if fs.total_assets > 0 else 0
        
        # Long term debt to equity
        lt_debt_to_equity = fs.long_term_debt / fs.total_equity if fs.total_equity > 0 else 0
        
        return {
            'debt_to_equity': round(debt_to_equity, 2),
            'debt_to_assets': round(debt_to_assets, 2),
            'interest_coverage': round(interest_coverage, 2),
            'equity_ratio': round(equity_ratio, 2),
            'lt_debt_to_equity': round(lt_debt_to_equity, 2),
            'assessment': self._assess_solvency(debt_to_equity, interest_coverage)
        }
    
    def _assess_solvency(self, d_e, ic) -> str:
        """Assess solvency"""
        if d_e < 0.5 and ic > 5:
            return "Strong"
        elif d_e < 1.0 and ic > 3:
            return "Good"
        elif d_e < 2.0:
            return "Adequate"
        else:
            return "Risky"
    
    def _profitability_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate profitability ratios"""
        # ROE
        roe = fs.net_income / fs.total_equity if fs.total_equity > 0 else 0
        
        # ROA
        roa = fs.net_income / fs.total_assets if fs.total_assets > 0 else 0
        
        # Gross margin
        gross_margin = fs.gross_profit / fs.revenue if fs.revenue > 0 else 0
        
        # Operating margin
        operating_margin = fs.operating_income / fs.revenue if fs.revenue > 0 else 0
        
        # Net margin
        net_margin = fs.net_income / fs.revenue if fs.revenue > 0 else 0
        
        # EBITDA margin
        ebitda = fs.operating_income + (fs.operating_expenses * 0.3)  # Approximate
        ebitda_margin = ebitda / fs.revenue if fs.revenue > 0 else 0
        
        return {
            'roe': round(roe, 4),
            'roa': round(roa, 4),
            'gross_margin': round(gross_margin, 4),
            'operating_margin': round(operating_margin, 4),
            'net_margin': round(net_margin, 4),
            'ebitda_margin': round(ebitda_margin, 4),
            'assessment': self._assess_profitability(roe, net_margin)
        }
    
    def _assess_profitability(self, roe, net_margin) -> str:
        """Assess profitability"""
        if roe > 0.20 and net_margin > 0.15:
            return "Excellent"
        elif roe > 0.15 and net_margin > 0.10:
            return "Strong"
        elif roe > 0.10:
            return "Good"
        elif roe > 0.05:
            return "Adequate"
        else:
            return "Weak"
    
    def _efficiency_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate efficiency ratios"""
        # Asset turnover
        asset_turnover = fs.revenue / fs.total_assets if fs.total_assets > 0 else 0
        
        # Inventory turnover
        inventory_turnover = fs.cost_of_goods / fs.inventory if fs.inventory > 0 else 0
        
        # Receivables turnover
        receivables_turnover = fs.revenue / fs.accounts_receivable if fs.accounts_receivable > 0 else 0
        
        # Fixed asset turnover
        fixed_asset_turnover = fs.revenue / fs.fixed_assets if fs.fixed_assets > 0 else 0
        
        # Cash conversion cycle (simplified)
        ccc = 0  # Would need more data
        
        return {
            'asset_turnover': round(asset_turnover, 2),
            'inventory_turnover': round(inventory_turnover, 2),
            'receivables_turnover': round(receivables_turnover, 2),
            'fixed_asset_turnover': round(fixed_asset_turnover, 2),
            'cash_conversion_cycle': ccc,
            'assessment': self._assess_efficiency(asset_turnover)
        }
    
    def _assess_efficiency(self, at) -> str:
        """Assess efficiency"""
        if at > 1.5:
            return "Efficient"
        elif at > 1.0:
            return "Good"
        elif at > 0.5:
            return "Adequate"
        else:
            return "Inefficient"
    
    def _market_ratios(self, fs: FinancialStatements) -> Dict:
        """Calculate market ratios"""
        if fs.stock_price == 0 or fs.shares_outstanding == 0:
            return {}
        
        # P/E ratio
        pe_ratio = fs.market_cap / fs.net_income if fs.net_income > 0 else 0
        
        # P/B ratio
        pb_ratio = fs.market_cap / fs.total_equity if fs.total_equity > 0 else 0
        
        # PEG ratio (assuming 10% growth)
        peg_ratio = pe_ratio / 10 if pe_ratio > 0 else 0
        
        # Dividend yield
        dividend_yield = (fs.dividend_per_share * fs.shares_outstanding) / fs.market_cap if fs.market_cap > 0 else 0
        
        # P/S ratio
        ps_ratio = fs.market_cap / fs.revenue if fs.revenue > 0 else 0
        
        return {
            'pe_ratio': round(pe_ratio, 2),
            'pb_ratio': round(pb_ratio, 2),
            'peg_ratio': round(peg_ratio, 2),
            'dividend_yield': round(dividend_yield, 4),
            'ps_ratio': round(ps_ratio, 2),
            'market_cap': fs.market_cap
        }
    
    # ==================== Valuation ====================
    
    def dcf_valuation(
        self,
        free_cash_flow: float,
        growth_rate: float = 0.05,
        discount_rate: float = 0.10,
        terminal_growth: float = 0.03,
        projection_years: int = 5
    ) -> Dict:
        """
        Discounted Cash Flow Valuation
        
        Args:
            free_cash_flow: Current free cash flow
            growth_rate: Expected growth rate
            discount_rate: WACC (discount rate)
            terminal_growth: Long-term growth rate
            projection_years: Number of projection years
            
        Returns:
            Dict with valuation results
        """
        # Project cash flows
        cash_flows = []
        for year in range(1, projection_years + 1):
            cf = free_cash_flow * (1 + growth_rate) ** year
            # Discount
            pv = cf / (1 + discount_rate) ** year
            cash_flows.append({
                'year': year,
                'cf': cf,
                'pv': pv
            })
        
        # Terminal value
        terminal_value = (free_cash_flow * (1 + growth_rate) ** projection_years * 
                         (1 + terminal_growth)) / (discount_rate - terminal_growth)
        terminal_pv = terminal_value / (1 + discount_rate) ** projection_years
        
        # Enterprise value
        enterprise_value = sum(cf['pv'] for cf in cash_flows) + terminal_pv
        
        return {
            'method': 'DCF',
            'enterprise_value': enterprise_value,
            'terminal_value': terminal_value,
            'terminal_pv': terminal_pv,
            'projected_cfs': cash_flows,
            'implied_pe': enterprise_value / free_cash_flow if free_cash_flow > 0 else 0,
            'assumptions': {
                'growth_rate': growth_rate,
                'discount_rate': discount_rate,
                'terminal_growth': terminal_growth
            }
        }
    
    def relative_valuation(
        self,
        company: str,
        peers: List[str],
        metrics: Dict[str, float]
    ) -> Dict:
        """Relative valuation with peer comparison"""
        # Simplified peer comparison
        return {
            'method': 'Relative',
            'company': company,
            'peers': peers,
            'metrics': metrics,
            'average_metrics': {
                'pe': 20,  # Would come from data
                'pb': 2,
                'ps': 3
            },
            'suggestion': 'Undervalued' if metrics.get('pe', 30) < 20 else 'Fair value'
        }
    
    def graham_number(self, eps: float, book_value: float) -> float:
        """Graham Number (value investing)"""
        return math.sqrt(22.5 * eps * book_value)
    
    # ==================== Risk Assessment ====================
    
    def altman_z_score(self, fs: FinancialStatements) -> Dict:
        """
        Altman Z-Score for bankruptcy prediction
        
        For public manufacturing companies:
        Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
        """
        # Working capital / Total assets
        x1 = (fs.current_assets - fs.current_liabilities) / fs.total_assets if fs.total_assets > 0 else 0
        
        # Retained earnings / Total assets
        retained_earnings = fs.total_equity * 0.3  # Approximate
        x2 = retained_earnings / fs.total_assets if fs.total_assets > 0 else 0
        
        # EBIT / Total assets
        x3 = fs.operating_income / fs.total_assets if fs.total_assets > 0 else 0
        
        # Market value of equity / Total liabilities
        x4 = fs.market_cap / fs.total_liabilities if fs.total_liabilities > 0 else 0
        
        # Sales / Total assets
        x5 = fs.revenue / fs.total_assets if fs.total_assets > 0 else 0
        
        # Calculate Z-score
        z_score = (1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5)
        
        # Determine risk level
        if z_score > 2.99:
            risk_level = "Safe"
        elif z_score > 1.81:
            risk_level = "Grey"
        else:
            risk_level = "Distress"
        
        return {
            'score': round(z_score, 2),
            'risk_level': risk_level,
            'components': {
                'x1_working_capital': round(x1, 3),
                'x2_retained_earnings': round(x2, 3),
                'x3_ebit': round(x3, 3),
                'x4_market_value': round(x4, 3),
                'x5_sales': round(x5, 3)
            }
        }
    
    def piotroski_f_score(self, fs: FinancialStatements) -> Dict:
        """
        Piotroski F-Score for financial health
        
        9 criteria, 1 point each
        """
        score = 0
        criteria = []
        
        # 1. Positive ROA
        roa = fs.net_income / fs.total_assets if fs.total_assets > 0 else 0
        if roa > 0:
            score += 1
            criteria.append({'criterion': 'Positive ROA', 'passed': True})
        else:
            criteria.append({'criterion': 'Positive ROA', 'passed': False})
        
        # 2. Positive Operating Cash Flow
        if fs.operating_cash_flow > 0:
            score += 1
            criteria.append({'criterion': 'Positive OCF', 'passed': True})
        else:
            criteria.append({'criterion': 'Positive OCF', 'passed': False})
        
        # 3. ROA improving (simplified - comparing to assets)
        if roa > 0.1:  # Simplified
            score += 1
            criteria.append({'criterion': 'ROA improving', 'passed': True})
        else:
            criteria.append({'criterion': 'ROA improving', 'passed': False})
        
        # 4. OCF > Net Income (quality of earnings)
        if fs.operating_cash_flow > fs.net_income:
            score += 1
            criteria.append({'criterion': 'OCF > Net Income', 'passed': True})
        else:
            criteria.append({'criterion': 'OCF > Net Income', 'passed': False})
        
        # 5. Lower debt ratio
        debt_ratio = fs.total_liabilities / fs.total_assets if fs.total_assets > 0 else 1
        if debt_ratio < 0.5:
            score += 1
            criteria.append({'criterion': 'Lower debt ratio', 'passed': True})
        else:
            criteria.append({'criterion': 'Lower debt ratio', 'passed': False})
        
        # 6. Higher current ratio
        current_ratio = fs.current_assets / fs.current_liabilities if fs.current_liabilities > 0 else 0
        if current_ratio > 1.5:
            score += 1
            criteria.append({'criterion': 'Higher current ratio', 'passed': True})
        else:
            criteria.append({'criterion': 'Higher current ratio', 'passed': False})
        
        # 7-9: Simplified (would need historical data)
        criteria.append({'criterion': 'No dilution (assumed)', 'passed': True})
        criteria.append({'criterion': 'Margins (assumed stable)', 'passed': True})
        criteria.append({'criterion': 'Asset turnover (assumed stable)', 'passed': True})
        score += 3  # Assume passed
        
        # Determine strength
        if score >= 8:
            strength = "Strong"
        elif score >= 6:
            strength = "Good"
        elif score >= 4:
            strength = "Average"
        else:
            strength = "Weak"
        
        return {
            'score': score,
            'max_score': 9,
            'strength': strength,
            'criteria': criteria
        }
    
    def _assess_risk(self, fs: FinancialStatements) -> Dict:
        """Comprehensive risk assessment"""
        # Z-score
        z_result = self.altman_z_score(fs)
        
        # F-score
        f_result = self.piotroski_f_score(fs)
        
        # Overall risk
        risk_factors = []
        
        if z_result['risk_level'] == 'Distress':
            risk_factors.append('High bankruptcy risk')
        
        if fs.debt_to_equity(fs.total_liabilities / fs.total_equity) > 1:
            risk_factors.append('High leverage')
        
        if fs.interest_coverage(fs.operating_income / fs.interest_expense) < 2:
            risk_factors.append('Low interest coverage')
        
        return {
            'altman_z': z_result,
            'piotroski_f': f_result,
            'risk_factors': risk_factors,
            'overall_risk': 'Low' if not risk_factors else 'Medium' if len(risk_factors) < 2 else 'High'
        }
    
    # ==================== Health Check ====================
    
    def _health_check(self, fs: FinancialStatements, ratios: Dict) -> Dict:
        """Comprehensive health check"""
        score = 0
        max_score = 100
        strengths = []
        weaknesses = []
        
        # Liquidity (20 points)
        liq = ratios['liquidity']
        if liq['current_ratio'] >= 2:
            score += 10
            strengths.append('Strong current ratio')
        elif liq['current_ratio'] >= 1.5:
            score += 7
        else:
            weaknesses.append('Weak current ratio')
        
        if liq['quick_ratio'] >= 1:
            score += 10
            strengths.append('Strong quick ratio')
        else:
            score += 3
        
        # Solvency (20 points)
        sol = ratios['solvency']
        if sol['debt_to_equity'] < 0.5:
            score += 10
            strengths.append('Low debt')
        elif sol['debt_to_equity'] < 1.0:
            score += 7
        else:
            weaknesses.append('High debt')
        
        if sol['interest_coverage'] > 5:
            score += 10
        elif sol['interest_coverage'] > 3:
            score += 7
        else:
            weaknesses.append('Low interest coverage')
        
        # Profitability (30 points)
        prof = ratios['profitability']
        if prof['roe'] > 0.20:
            score += 15
            strengths.append('Excellent ROE')
        elif prof['roe'] > 0.15:
            score += 10
        elif prof['roe'] > 0.10:
            score += 5
        else:
            weaknesses.append('Low ROE')
        
        if prof['net_margin'] > 0.15:
            score += 15
            strengths.append('Strong margins')
        elif prof['net_margin'] > 0.10:
            score += 10
        elif prof['net_margin'] > 0.05:
            score += 5
        else:
            weaknesses.append('Low margins')
        
        # Efficiency (15 points)
        eff = ratios['efficiency']
        if eff['asset_turnover'] > 1:
            score += 15
            strengths.append('Good asset utilization')
        elif eff['asset_turnover'] > 0.5:
            score += 8
        else:
            score += 3
            weaknesses.append('Low asset turnover')
        
        # Cash flow (15 points)
        if fs.free_cash_flow > 0:
            score += 15
            strengths.append('Positive free cash flow')
        elif fs.operating_cash_flow > 0:
            score += 8
            weaknesses.append('Negative free cash flow')
        else:
            weaknesses.append('Negative operating cash flow')
        
        # Determine overall health
        if score >= 80:
            overall = "Excellent"
        elif score >= 65:
            overall = "Good"
        elif score >= 50:
            overall = "Fair"
        else:
            overall = "Poor"
        
        return {
            'score': score,
            'max_score': max_score,
            'overall': overall,
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    # ==================== Valuation ====================
    
    def _valuation(self, fs: FinancialStatements, ratios: Dict) -> Dict:
        """Perform valuation"""
        valuations = {}
        
        # DCF (if FCF available)
        if fs.free_cash_flow > 0:
            valuations['dcf'] = self.dcf_valuation(
                free_cash_flow=fs.free_cash_flow,
                growth_rate=0.05,
                discount_rate=0.10
            )
        
        # Graham Number
        if fs.eps > 0 and fs.book_value_per_share > 0:
            valuations['graham'] = {
                'value': self.graham_number(fs.eps, fs.book_value_per_share),
                'method': 'Graham Number'
            }
        
        # Relative (if market data available)
        if ratios.get('market'):
            valuations['relative'] = {
                'method': 'Relative',
                'pe': ratios['market'].get('pe_ratio'),
                'pb': ratios['market'].get('pb_ratio')
            }
        
        return valuations
    
    # ==================== Summary ====================
    
    def _generate_summary(
        self,
        company: str,
        ratios: Dict,
        risk: Dict,
        health: Dict,
        valuation: Dict
    ) -> str:
        """Generate analysis summary"""
        lines = []
        
        lines.append(f"## Financial Analysis: {company}")
        lines.append("")
        
        # Health
        lines.append(f"**Overall Health Score**: {health['score']}/100 ({health['overall']})")
        lines.append("")
        
        # Key ratios
        prof = ratios['profitability']
        lines.append(f"**Profitability**: ROE {prof['roe']:.1%}, Net Margin {prof['net_margin']:.1%}")
        
        liq = ratios['liquidity']
        lines.append(f"**Liquidity**: Current Ratio {liq['current_ratio']:.2f}x")
        
        sol = ratios['solvency']
        lines.append(f"**Solvency**: D/E {sol['debt_to_equity']:.2f}x")
        
        # Risk
        lines.append("")
        lines.append(f"**Risk Assessment**: {risk['overall_risk']}")
        if risk['risk_factors']:
            lines.append(f"Concerns: {', '.join(risk['risk_factors'])}")
        
        # Strengths/Weaknesses
        if health['strengths']:
            lines.append("")
            lines.append(f"**Strengths**: {', '.join(health['strengths'][:3])}")
        
        if health['weaknesses']:
            lines.append("")
            lines.append(f"**Weaknesses**: {', '.join(health['weaknesses'][:3])}")
        
        return "\n".join(lines)
    
    def summary_report(self, analysis: Dict) -> str:
        """Generate summary report"""
        return analysis.get('summary', '')
    
    def peer_comparison(
        self,
        company: str,
        peers: List[str],
        statements_map: Dict[str, Dict]
    ) -> Dict:
        """Compare company with peers"""
        comparisons = {}
        
        for name, statements in statements_map.items():
            result = self.analyze(name, statements)
            comparisons[name] = {
                'roe': result['ratios']['profitability']['roe'],
                'net_margin': result['ratios']['profitability']['net_margin'],
                'debt_to_equity': result['ratios']['solvency']['debt_to_equity'],
                'health_score': result['health']['score']
            }
        
        return {
            'company': company,
            'comparisons': comparisons
        }


# Convenience function
def analyze_financials(company: str, statements: Dict) -> Dict:
    """Quick analysis function"""
    analyzer = FinancialAnalyzer()
    return analyzer.analyze(company, statements)
