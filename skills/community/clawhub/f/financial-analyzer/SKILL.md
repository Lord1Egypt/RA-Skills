---
name: financial-analyzer
description: AI-powered financial analysis assistant for financial statement analysis, ratio analysis, cash flow analysis, investment evaluation, and financial health assessment. Supports Chinese and international accounting standards. Essential tool for investors and analysts.
tags:
  - finance
  - analysis
  - investment
  - financial-statements
  - valuation
  - accounting
version: 1.0.0
author: chenq
---

# Financial Analyzer

AI-powered financial analysis and investment evaluation tool.

## Features

### 1. Financial Statement Analysis
- **Balance Sheet**: Assets, liabilities, equity analysis
- **Income Statement**: Revenue, expenses, profit analysis
- **Cash Flow Statement**: Operating, investing, financing
- **Statement of Changes**: Equity changes tracking

### 2. Ratio Analysis
- **Liquidity Ratios**: Current, quick, cash ratio
- **Solvency Ratios**: Debt, interest coverage, D/E
- **Profitability Ratios**: ROE, ROA, margins
- **Efficiency Ratios**: Turnover, asset utilization
- **Market Ratios**: P/E, P/B, PEG, dividend yield

### 3. Cash Flow Analysis
- **Operating Cash Flow**: Quality of earnings
- **Free Cash Flow**: Valuation and health
- **Cash Conversion**: Efficiency metrics
- **Burn Rate**: Startup sustainability

### 4. Investment Evaluation
- **DCF Valuation**: Discounted cash flow
- **Relative Valuation**: Peer comparison
- **Graham Number**: Value investing
- **Intrinsic Value**: Multiple methods

### 5. Risk Assessment
- **Altman Z-Score**: Bankruptcy prediction
- **Piotroski F-Score**: Financial health
- **Credit Risk**: Default probability
- **Operational Risk**: Business stability

## Installation

```bash
pip install numpy pandas
```

## Usage

### Basic Analysis

```python
from financial_analyzer import FinancialAnalyzer

analyzer = FinancialAnalyzer()

# Analyze a company
result = analyzer.analyze(
    company="茅台",
    statements={
        'balance_sheet': balance_data,
        'income_statement': income_data,
        'cash_flow': cash_flow_data
    }
)

print(result['summary'])
```

### Ratio Analysis

```python
# Calculate all ratios
ratios = analyzer.calculate_ratios(statements)

print(ratios['liquidity'])
# {
#     'current_ratio': 2.5,
#     'quick_ratio': 1.8,
#     'cash_ratio': 0.5
# }

print(ratios['profitability'])
# {
#     'roe': 0.28,
#     'roa': 0.18,
#     'gross_margin': 0.75,
#     'net_margin': 0.52
# }
```

### Valuation

```python
# DCF Valuation
dcf = analyzer.dcf_valuation(
    free_cash_flow=50e9,
    growth_rate=0.05,
    discount_rate=0.10,
    terminal_growth=0.03
)
print(f"Intrinsic Value: {dcf['enterprise_value']:,.0f}")

# Relative Valuation
relative = analyzer.relative_valuation(
    company="茅台",
    peers=["五粮液", "泸州老窖"],
    metrics={'pe': 35, 'pb': 8}
)
```

### Risk Assessment

```python
# Altman Z-Score (bankruptcy risk)
z_score = analyzer.altman_z_score(statements)
print(f"Z-Score: {z_score['score']:.2f}")
print(f"Risk Level: {z_score['risk_level']}")
# Z-Score: 5.2
# Risk Level: Safe (Z > 2.99)

# Piotroski F-Score (financial health)
f_score = analyzer.piotroski_f_score(statements)
print(f"F-Score: {f_score['score']}/9")
```

### Financial Health Check

```python
# Comprehensive health check
health = analyzer.health_check(statements)

print(health['overall_score'])  # 85/100
print(health['strengths'])
print(health['weaknesses'])
print(health['recommendations'])
```

## API Reference

### Statement Analysis
| Method | Description |
|--------|-------------|
| `analyze(company, statements)` | Full analysis |
| `analyze_balance_sheet(data)` | Balance sheet analysis |
| `analyze_income(data)` | Income statement analysis |
| `analyze_cash_flow(data)` | Cash flow analysis |

### Ratios
| Method | Description |
|--------|-------------|
| `calculate_ratios(statements)` | All ratios |
| `liquidity_ratios(data)` | Liquidity metrics |
| `solvency_ratios(data)` | Solvency metrics |
| `profitability_ratios(data)` | Profitability metrics |
| `efficiency_ratios(data)` | Efficiency metrics |

### Valuation
| Method | Description |
|--------|-------------|
| `dcf_valuation(...)` | DCF model |
| `relative_valuation(...)` | Peer comparison |
| `graham_number(...)` | Graham's formula |
| `earnings_power_value(...)` | EPV valuation |

### Risk
| Method | Description |
|--------|-------------|
| `altman_z_score(statements)` | Bankruptcy risk |
| `piotroski_f_score(statements)` | Financial health |
| `credit_risk_score(statements)` | Credit assessment |
| `operational_risk(statements)` | Business risk |

### Reports
| Method | Description |
|--------|-------------|
| `generate_report(analysis)` | Full report |
| `summary_report(analysis)` | Summary |
| `peer_comparison(company, peers)` | Compare with peers |

## Key Ratios

### Liquidity
| Ratio | Formula | Good Range |
|-------|---------|------------|
| Current Ratio | Current Assets / Current Liabilities | 1.5 - 3.0 |
| Quick Ratio | (CA - Inventory) / CL | 1.0 - 2.0 |
| Cash Ratio | Cash / CL | 0.2 - 0.5 |

### Profitability
| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| ROE | Net Income / Equity | Higher is better |
| ROA | Net Income / Assets | Higher is better |
| Gross Margin | Gross Profit / Revenue | Industry dependent |
| Net Margin | Net Income / Revenue | Higher is better |

### Leverage
| Ratio | Formula | Good Range |
|-------|---------|------------|
| Debt/Equity | Total Debt / Equity | < 2.0 |
| Interest Coverage | EBIT / Interest | > 3.0 |
| Debt/Assets | Total Debt / Assets | < 0.6 |

### Efficiency
| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Asset Turnover | Revenue / Assets | Higher is better |
| Inventory Turnover | COGS / Inventory | Industry dependent |
| Receivables Turnover | Revenue / Receivables | Higher is better |

## Valuation Models

### DCF Model
```python
{
    'method': 'dcf',
    'steps': [
        'Project free cash flows',
        'Calculate terminal value',
        'Discount to present value',
        'Subtract debt, add cash'
    ],
    'inputs': {
        'fcf': 'Free cash flow',
        'growth_rate': 'Expected growth',
        'wacc': 'Weighted average cost of capital',
        'terminal_growth': 'Long-term growth'
    }
}
```

### Graham Number
```python
graham_number = sqrt(22.5 * EPS * Book_Value_Per_Share)
```

## Risk Models

### Altman Z-Score
```
Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5

X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Market Value Equity / Total Liabilities
X5 = Sales / Total Assets

Interpretation:
Z > 2.99: Safe Zone
1.81 < Z < 2.99: Grey Zone
Z < 1.81: Distress Zone
```

### Piotroski F-Score
```
9 criteria, 1 point each:
1. Positive ROA
2. Positive Operating Cash Flow
3. ROA improving
4. OCF > Net Income
5. Lower debt ratio
6. Higher current ratio
7. No share dilution
8. Higher gross margin
9. Higher asset turnover

Score interpretation:
8-9: Strong
6-7: Good
4-5: Average
0-3: Weak
```

## Example: Full Analysis

```python
from financial_analyzer import FinancialAnalyzer

analyzer = FinancialAnalyzer()

# Company financial data
statements = {
    'balance_sheet': {
        'total_assets': 200e9,
        'total_liabilities': 50e9,
        'current_assets': 80e9,
        'current_liabilities': 30e9,
        'cash': 40e9,
        'inventory': 10e9,
        'equity': 150e9
    },
    'income_statement': {
        'revenue': 100e9,
        'cost_of_goods': 25e9,
        'operating_expenses': 10e9,
        'net_income': 50e9,
        'ebit': 60e9
    },
    'cash_flow': {
        'operating_cf': 55e9,
        'investing_cf': -15e9,
        'financing_cf': -10e9,
        'free_cash_flow': 40e9
    }
}

# Run full analysis
result = analyzer.analyze("Example Corp", statements)

print(f"ROE: {result['ratios']['profitability']['roe']:.1%}")
print(f"Z-Score: {result['risk']['z_score']:.2f}")
print(f"Health Score: {result['health_score']}/100")
```

## Chinese Accounting Standards

Supports both:
- **CAS** (Chinese Accounting Standards)
- **IFRS** (International Financial Reporting Standards)
- **GAAP** (US Generally Accepted Accounting Principles)

## Use Cases

- **Investment Analysis**: Evaluate investment opportunities
- **Credit Analysis**: Assess creditworthiness
- **Due Diligence**: M&A analysis
- **Performance Tracking**: Monitor company health
- **Screening**: Filter investment candidates

## Best Practices

1. Use multiple ratios together
2. Compare with industry peers
3. Analyze trends over time
4. Consider qualitative factors
5. Understand accounting policies

## Future Capabilities

- Real-time data integration
- AI-powered insights
- Automated report generation
- Multi-company comparison
- Industry benchmarking
