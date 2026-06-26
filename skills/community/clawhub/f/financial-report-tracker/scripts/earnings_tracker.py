#!/usr/bin/env python3
"""
Financial Report Tracker - Automatically track tech company earnings reports and generate investment summaries

Usage:
    python earnings_tracker.py track <ticker>
    python earnings_tracker.py preview <ticker>
    python earnings_tracker.py review <ticker> --quarter <Q1/Q2/Q3/Q4>
"""

import sys
import io
import time
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import yfinance as yf
    import requests
except ImportError:
    print("❌ Missing dependencies. Please install: pip install yfinance requests pandas")
    sys.exit(1)


def create_ticker(symbol):
    """Create Ticker object and set user agent"""
    ticker = yf.Ticker(symbol)
    # Yahoo Finance may require a user agent
    try:
        import os
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        ticker._history_params['headers'] = headers
    except:
        pass
    return ticker


def get_with_retry(func, *args, max_retries=3, delay=2, **kwargs):
    """Fetch function with retry logic"""
    last_error = None
    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, dict) and 'error' not in result:
                return result
            elif isinstance(result, dict) and result.get('error') and 'Rate limited' not in str(result.get('error', '')):
                return result
            last_error = result.get('error', 'Unknown error')
        except Exception as e:
            last_error = str(e)
        
        if attempt < max_retries - 1:
            time.sleep(delay * (attempt + 1))
    
    return {'error': f'{last_error} (retried {max_retries} times)', 'symbol': args[0] if args else 'unknown'}


def get_earnings_calendar(symbol):
    """Get earnings calendar"""
    def _fetch():
        ticker = create_ticker(symbol)
        info = ticker.info
        
        # Try to get next earnings date
        next_earnings = info.get('earningsNextGrossProfit', None) or info.get('nextEarningsDate', None)
        
        # Get more details from calendar
        try:
            calendar = ticker.calendar
            if calendar is not None and not calendar.empty:
                if 'Earnings Date' in calendar.columns or 'Earnings Date' in calendar.index:
                    earnings_date = calendar.loc['Earnings Date'].values[0]
                    if hasattr(earnings_date, '__str__'):
                        next_earnings = str(earnings_date)
                    else:
                        next_earnings = str(earnings_date)
        except:
            pass
        
        return {
            'symbol': symbol,
            'next_earnings': next_earnings,
            'company_name': info.get('shortName', info.get('longName', 'N/A')),
            'market_cap': info.get('marketCap', None),
            'exchange': info.get('exchange', 'N/A'),
        }
    
    return get_with_retry(_fetch)


def get_earnings_estimate(symbol):
    """Get market expectations"""
    def _fetch():
        ticker = create_ticker(symbol)
        info = ticker.info
        
        # EPS estimates
        eps_estimate = info.get('forwardEps', None)  # Forward EPS
        eps_current = info.get('trailingEps', None)   # Actual EPS
        
        # Revenue estimates
        revenue_estimate = info.get('totalRevenue', None)
        
        # Analyst ratings
        analyst_rating = info.get('recommendationKey', 'N/A')
        target_price = info.get('targetMeanPrice', None)
        current_price = info.get('currentPrice', info.get('regularMarketPrice', None))
        
        # 52-week range
        week_52_high = info.get('fiftyTwoWeekHigh', None)
        week_52_low = info.get('fiftyTwoWeekLow', None)
        
        return {
            'symbol': symbol,
            'eps_estimate': eps_estimate,
            'eps_current': eps_current,
            'revenue': revenue_estimate,
            'analyst_rating': analyst_rating,
            'target_price': target_price,
            'current_price': current_price,
            'week_52_high': week_52_high,
            'week_52_low': week_52_low,
            'company_name': info.get('shortName', info.get('longName', 'N/A')),
        }
    
    return get_with_retry(_fetch)


def get_earnings_review(symbol, quarter=None):
    """Get earnings review"""
    def _fetch():
        ticker = create_ticker(symbol)
        info = ticker.info
        
        # Get historical earnings data
        try:
            financials = ticker.financials
            earnings = ticker.earnings
            quarterly_financials = ticker.quarterly_financials
            
            # Get key metrics
            revenue = None
            net_income = None
            gross_margin = None
            
            if not financials.empty:
                latest = financials.iloc[:, 0] if len(financials.columns) > 0 else None
                if latest is not None:
                    revenue = latest.get('Total Revenue', None)
                    net_income = latest.get('Net Income', None)
                    gross_profit = latest.get('Gross Profit', None)
                    if revenue and gross_profit:
                        gross_margin = (gross_profit / revenue) * 100
        except:
            pass
        
        # Profitability metrics
        profit_margin = info.get('profitMargins', None)
        operating_margin = info.get('operatingMargins', None)
        roe = info.get('returnOnEquity', None)
        
        # Growth metrics
        revenue_growth = info.get('revenueGrowth', None)
        earnings_growth = info.get('earningsGrowth', None)
        
        # Valuation metrics
        pe_ratio = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)
        
        # Management guidance
        guidance = info.get('earningsQuarterlyGrowth', None)
        
        return {
            'symbol': symbol,
            'company_name': info.get('shortName', info.get('longName', 'N/A')),
            'revenue': revenue,
            'net_income': net_income,
            'gross_margin': gross_margin,
            'profit_margin': profit_margin,
            'operating_margin': operating_margin,
            'roe': roe,
            'revenue_growth': revenue_growth,
            'earnings_growth': earnings_growth,
            'pe_ratio': pe_ratio,
            'forward_pe': forward_pe,
            'guidance': guidance,
            'analyst_count': info.get('numberOfAnalystOpinions', None),
            'target_price': info.get('targetMeanPrice', None),
            'current_price': info.get('currentPrice', info.get('regularMarketPrice', None)),
            'debt_to_equity': info.get('debtToEquity', None),
            'current_ratio': info.get('currentRatio', None),
        }
    
    return get_with_retry(_fetch)


def format_track_report(data):
    """Format tracking report"""
    output = []
    output.append("# 📊 Financial Report Tracker Report")
    output.append(f"\n**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    if 'error' in data:
        output.append(f"❌ Data retrieval failed: {data['error']}")
        output.append("")
        output.append("💡 **Tip**: The Yahoo Finance API has request limits. Try again later or test with a different ticker symbol.")
        return "\n".join(output)
    
    output.append(f"## 📅 Earnings Calendar - {data.get('company_name', data['symbol'])} ({data['symbol']})")
    output.append("")
    
    next_earnings = data.get('next_earnings', 'Data Unavailable')
    output.append(f"| Item | Data |")
    output.append(f"|------|------|")
    output.append(f"| Next Earnings Date | {next_earnings} |")
    output.append(f"| Exchange | {data.get('exchange', 'N/A')} |")
    
    if data.get('market_cap'):
        market_cap = data['market_cap']
        if market_cap >= 1e12:
            market_cap_str = f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            market_cap_str = f"${market_cap/1e9:.2f}B"
        else:
            market_cap_str = f"${market_cap/1e6:.2f}M"
        output.append(f"| Market Cap | {market_cap_str} |")
    
    return "\n".join(output)


def format_preview_report(data):
    """Format preview report"""
    output = []
    output.append("# 📊 Earnings Preview Analysis")
    output.append(f"\n**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    if 'error' in data:
        output.append(f"❌ Data retrieval failed: {data['error']}")
        output.append("")
        output.append("💡 **Tip**: The Yahoo Finance API has request limits. Try again later or test with a different ticker symbol.")
        return "\n".join(output)
    
    company_name = data.get('company_name', data['symbol'])
    output.append(f"## 🔍 Market Expectations - {company_name} ({data['symbol']})")
    output.append("")
    
    # Trend determination function
    def trend(val, compare_val=None):
        if val is None:
            return "→"
        if compare_val:
            if val > compare_val:
                return "↑"
            elif val < compare_val:
                return "↓"
        return "→"
    
    # Rating function
    def rating(val, threshold_high=0.5, threshold_low=0.1):
        if val is None:
            return "⭐⭐⭐"
        if val >= threshold_high:
            return "⭐⭐⭐⭐⭐"
        elif val >= threshold_low:
            return "⭐⭐⭐⭐"
        else:
            return "⭐⭐⭐"
    
    output.append("## Data Overview")
    output.append("")
    output.append("| Metric | Value | Trend | Rating |")
    output.append("|--------|-------|-------|--------|")
    
    # EPS
    eps_str = f"${data.get('eps_estimate', 'Data Unavailable'):.2f}" if data.get('eps_estimate') else "Data Unavailable"
    eps_rating = "⭐⭐⭐⭐" if data.get('eps_estimate') else "⭐⭐⭐"
    output.append(f"| Expected EPS | {eps_str} | {trend(data.get('eps_estimate'))} | {eps_rating} |")
    
    # Current EPS
    eps_current_str = f"${data.get('eps_current', 'Data Unavailable'):.2f}" if data.get('eps_current') else "Data Unavailable"
    output.append(f"| Current EPS | {eps_current_str} | {trend(data.get('eps_current'), data.get('eps_estimate'))} | {rating(data.get('eps_current'))} |")
    
    # Revenue
    revenue = data.get('revenue', None)
    if revenue:
        if revenue >= 1e12:
            revenue_str = f"${revenue/1e12:.2f}T"
        else:
            revenue_str = f"${revenue/1e9:.2f}B"
    else:
        revenue_str = "Data Unavailable"
    output.append(f"| Revenue | {revenue_str} | {trend(revenue)} | {rating(revenue, 1e12, 1e11)} |")
    
    # Target price vs. Current price
    target = data.get('target_price', None)
    current = data.get('current_price', None)
    if target and current:
        upside = ((target - current) / current) * 100
        price_str = f"${current:.2f} → ${target:.2f} ({upside:+.1f}%)"
        price_rating = "⭐⭐⭐⭐" if upside > 20 else "⭐⭐⭐"
    else:
        price_str = "Data Unavailable"
        price_rating = "⭐⭐⭐"
    output.append(f"| Target/Current Price | {price_str} | → | {price_rating} |")
    
    # 52-week range
    high_52 = data.get('week_52_high', None)
    low_52 = data.get('week_52_low', None)
    if high_52 and low_52:
        range_str = f"${low_52:.2f} - ${high_52:.2f}"
    else:
        range_str = "Data Unavailable"
    output.append(f"| 52-Week Range | {range_str} | → | ⭐⭐⭐ |")
    
    # Analyst rating
    analyst = data.get('analyst_rating', 'N/A')
    rating_map = {
        'strongBuy': 'Strong Buy ⭐⭐⭐⭐⭐',
        'buy': 'Buy ⭐⭐⭐⭐',
        'hold': 'Hold ⭐⭐⭐',
        'underweight': 'Underweight ⭐⭐',
        'sell': 'Sell ⭐',
    }
    analyst_display = rating_map.get(analyst, analyst)
    output.append(f"| Analyst Rating | {analyst_display} | → | ⭐⭐⭐⭐ |")
    
    return "\n".join(output)


def format_review_report(data):
    """Format earnings review"""
    output = []
    output.append("# 📊 Earnings Review Report")
    output.append(f"\n**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    if 'error' in data:
        output.append(f"❌ Data retrieval failed: {data['error']}")
        output.append("")
        output.append("💡 **Tip**: The Yahoo Finance API has request limits. Try again later or test with a different ticker symbol.")
        return "\n".join(output)
    
    company_name = data.get('company_name', data['symbol'])
    output.append(f"## 📈 Earnings Review - {company_name} ({data['symbol']})")
    output.append("")
    
    # Key Findings
    output.append("## Key Findings")
    output.append("")
    
    findings = []
    
    # Revenue analysis
    revenue = data.get('revenue', None)
    if revenue:
        if revenue >= 1e12:
            findings.append(f"Revenue reached ${revenue/1e12:.2f}T, leading industry position")
        elif revenue >= 1e9:
            findings.append(f"Revenue reached ${revenue/1e9:.2f}B, significant market presence")
    
    # Gross margin analysis
    gross_margin = data.get('gross_margin', None)
    if gross_margin:
        if gross_margin >= 50:
            findings.append(f"Gross margin {gross_margin:.1f}%, strong pricing power and solid moat")
        elif gross_margin >= 30:
            findings.append(f"Gross margin {gross_margin:.1f}%, healthy profitability")
        else:
            findings.append(f"Gross margin {gross_margin:.1f}%, facing significant competitive pressure")
    
    # Net profit margin analysis
    profit_margin = data.get('profit_margin', None)
    if profit_margin:
        profit_pct = profit_margin * 100
        if profit_pct >= 20:
            findings.append(f"Net profit margin {profit_pct:.1f}%, strong profitability")
        elif profit_pct >= 10:
            findings.append(f"Net profit margin {profit_pct:.1f}%, normal profitability level")
        else:
            findings.append(f"Net profit margin {profit_pct:.1f}%, limited profit potential")
    
    # Revenue growth
    revenue_growth = data.get('revenue_growth', None)
    if revenue_growth:
        growth_pct = revenue_growth * 100
        if growth_pct >= 20:
            findings.append(f"Revenue YoY growth {growth_pct:.1f}%, strong growth momentum")
        elif growth_pct >= 0:
            findings.append(f"Revenue YoY growth {growth_pct:.1f}%, maintaining growth")
        else:
            findings.append(f"Revenue YoY decline {abs(growth_pct):.1f}%, requires attention")
    
    # Valuation analysis
    pe = data.get('pe_ratio', None)
    forward_pe = data.get('forward_pe', None)
    if pe and forward_pe:
        if pe < forward_pe:
            findings.append(f"PE {pe:.1f}x, expected future earnings improvement, valuation likely to moderate")
        else:
            findings.append(f"PE {pe:.1f}x, current valuation is relatively high")
    
    for i, finding in enumerate(findings[:5], 1):
        output.append(f"{i}. {finding}")
    
    if not findings:
        output.append("Incomplete data retrieved. Please verify the ticker symbol is correct.")
    
    output.append("")
    output.append("## Detailed Data")
    output.append("")
    output.append("| Metric | Value | Trend | Rating |")
    output.append("|--------|-------|-------|--------|")
    
    # Revenue
    if revenue:
        if revenue >= 1e12:
            revenue_str = f"${revenue/1e12:.2f}T"
        else:
            revenue_str = f"${revenue/1e9:.2f}B"
    else:
        revenue_str = "Data Unavailable"
    output.append(f"| Revenue | {revenue_str} | {'↑' if revenue_growth and revenue_growth > 0 else '↓'} | ⭐⭐⭐⭐ |")
    
    # Net Income
    net_income = data.get('net_income', None)
    if net_income:
        ni_str = f"${net_income/1e9:.2f}B" if net_income >= 1e9 else f"${net_income/1e6:.2f}M"
    else:
        ni_str = "Data Unavailable"
    output.append(f"| Net Income | {ni_str} | → | ⭐⭐⭐⭐ |")
    
    # Gross Margin
    gm_str = f"{gross_margin:.1f}%" if gross_margin else "Data Unavailable"
    gm_rating = "⭐⭐⭐⭐⭐" if gross_margin and gross_margin >= 50 else "⭐⭐⭐⭐" if gross_margin and gross_margin >= 30 else "⭐⭐⭐"
    output.append(f"| Gross Margin | {gm_str} | → | {gm_rating} |")
    
    # Net Profit Margin
    pm_str = f"{profit_margin*100:.1f}%" if profit_margin else "Data Unavailable"
    pm_rating = "⭐⭐⭐⭐⭐" if profit_margin and profit_margin >= 0.2 else "⭐⭐⭐⭐" if profit_margin and profit_margin >= 0.1 else "⭐⭐⭐"
    output.append(f"| Net Profit Margin | {pm_str} | → | {pm_rating} |")
    
    # ROE
    roe = data.get('roe', None)
    roe_str = f"{roe*100:.1f}%" if roe else "Data Unavailable"
    roe_rating = "⭐⭐⭐⭐⭐" if roe and roe >= 0.2 else "⭐⭐⭐⭐" if roe and roe >= 0.1 else "⭐⭐⭐"
    output.append(f"| Return on Equity (ROE) | {roe_str} | → | {roe_rating} |")
    
    # PE
    pe_str = f"{pe:.1f}x" if pe else "Data Unavailable"
    pe_rating = "⭐⭐⭐⭐" if pe and pe < 25 else "⭐⭐⭐" if pe and pe < 40 else "⭐⭐"
    output.append(f"| P/E Ratio | {pe_str} | → | {pe_rating} |")
    
    # Target Price
    target = data.get('target_price', None)
    current = data.get('current_price', None)
    if target and current:
        upside = ((target - current) / current) * 100
        price_str = f"${current:.2f} → ${target:.2f} ({upside:+.1f}%)"
    else:
        price_str = "Data Unavailable"
    output.append(f"| Target/Current Price | {price_str} | → | ⭐⭐⭐⭐ |")
    
    # Actionable Recommendations
    output.append("")
    output.append("## Actionable Recommendations")
    output.append("")
    output.append("| Priority | Recommendation | Expected Outcome |")
    output.append("|----------|----------------|------------------|")
    
    actions = []
    
    # Valuation-based recommendations
    if pe and pe < 20:
        actions.append(("🟢 Low", "Valuation at historical lows, consider accumulating on dips", "Ample margin of safety"))
    elif pe and pe > 50:
        actions.append(("🔴 High", "Elevated valuation, wait for pullback opportunity", "Avoid chasing highs"))
    
    # Growth-based recommendations
    if revenue_growth and revenue_growth > 0.15:
        actions.append(("🟡 Medium", "Strong growth, suitable for growth-oriented allocation", "Long-term holding returns promising"))
    
    # Margin-based recommendations
    if profit_margin and profit_margin > 0.2:
        actions.append(("🟢 Low", "Strong profitability, abundant cash flow", "Outstanding risk resilience"))
    elif profit_margin and profit_margin < 0.05:
        actions.append(("🔴 High", "Profitability under pressure, monitor cost control", "Requires close tracking of recovery"))
    
    if not actions:
        actions.append(("🟡 Medium", "Fundamental data complete; recommend comprehensive assessment with industry trends", "Prudent decision making"))
    
    for action in actions[:4]:
        output.append(f"| {action[0]} | {action[1]} | {action[2]} |")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Financial Report Tracker - Automatically track tech company earnings reports')
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')
    
    # track command
    track_parser = subparsers.add_parser('track', help='Track earnings release dates')
    track_parser.add_argument('symbol', help='Ticker symbol, e.g., AAPL')
    
    # preview command
    preview_parser = subparsers.add_parser('preview', help='Earnings preview analysis')
    preview_parser.add_argument('symbol', help='Ticker symbol, e.g., AAPL')
    
    # review command
    review_parser = subparsers.add_parser('review', help='Earnings review')
    review_parser.add_argument('symbol', help='Ticker symbol, e.g., AAPL')
    review_parser.add_argument('--quarter', '-q', help='Specify quarter, e.g., Q1', default=None)
    
    args = parser.parse_args()
    
    if args.command == 'track':
        data = get_earnings_calendar(args.symbol.upper())
        print(format_track_report(data))
    elif args.command == 'preview':
        data = get_earnings_estimate(args.symbol.upper())
        print(format_preview_report(data))
    elif args.command == 'review':
        data = get_earnings_review(args.symbol.upper(), args.quarter)
        print(format_review_report(data))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()