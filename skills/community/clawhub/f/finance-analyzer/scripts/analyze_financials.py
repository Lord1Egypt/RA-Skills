#!/usr/bin/env python3
"""
Financial Statement Analyzer
Reads Excel/CSV files containing financial statements (Income Statement,
Balance Sheet, Cash Flow Statement) and calculates key financial metrics.

Usage:
    python3 analyze_financials.py <file_path> [--sheet <sheet_name>] [--output <output_path>]

Arguments:
    file_path       Path to the Excel (.xlsx/.xls) or CSV (.csv) file
    --sheet         (Optional) Specific sheet name to analyze; if omitted, all sheets are analyzed
    --output        (Optional) Output file path for the analysis results (JSON format)

Output:
    Prints a JSON object containing:
    - parsed_data: Extracted financial data from each statement
    - metrics: Calculated financial metrics (ROE, ROA, gross_margin, net_margin, etc.)
    - warnings: Any issues encountered during parsing

Dependencies:
    pip install openpyxl pandas
"""

import argparse
import json
import os
import sys
import re

try:
    import pandas as pd
except ImportError:
    print(json.dumps({"error": "pandas is not installed. Run: pip install pandas openpyxl"}))
    sys.exit(1)


# ─── Keyword mappings for recognizing financial line items ───────────────────

# Income Statement (损益表 / 利润表) keywords
INCOME_STATEMENT_KEYWORDS = {
    "revenue": [
        "营业收入", "营业总收入", "主营业务收入", "revenue", "total revenue",
        "net revenue", "sales", "net sales", "turnover"
    ],
    "cost_of_revenue": [
        "营业成本", "主营业务成本", "营业总成本", "cost of revenue",
        "cost of goods sold", "cogs", "cost of sales"
    ],
    "gross_profit": [
        "毛利润", "毛利", "gross profit", "gross margin"
    ],
    "operating_income": [
        "营业利润", "operating income", "operating profit", "ebit"
    ],
    "total_profit": [
        "利润总额", "profit before tax", "income before tax",
        "earnings before tax", "pre-tax income"
    ],
    "income_tax": [
        "所得税费用", "所得税", "income tax", "tax expense",
        "provision for income tax"
    ],
    "net_income": [
        "净利润", "净利", "归属于母公司所有者的净利润", "net income",
        "net profit", "net earnings", "profit after tax"
    ],
    "operating_expense": [
        "营业费用", "销售费用", "管理费用", "研发费用",
        "operating expense", "selling expense", "admin expense",
        "r&d expense", "sg&a"
    ],
}

# Balance Sheet (资产负债表) keywords
BALANCE_SHEET_KEYWORDS = {
    "total_assets": [
        "资产总计", "资产合计", "总资产", "total assets"
    ],
    "total_liabilities": [
        "负债合计", "负债总计", "总负债", "total liabilities"
    ],
    "total_equity": [
        "所有者权益合计", "股东权益合计", "归属于母公司股东权益合计",
        "所有者权益（或股东权益）合计", "净资产",
        "total equity", "total shareholders equity",
        "stockholders equity", "total stockholders equity"
    ],
    "current_assets": [
        "流动资产合计", "流动资产", "total current assets", "current assets"
    ],
    "current_liabilities": [
        "流动负债合计", "流动负债", "total current liabilities",
        "current liabilities"
    ],
}

# Cash Flow Statement (现金流量表) keywords
CASH_FLOW_KEYWORDS = {
    "operating_cash_flow": [
        "经营活动产生的现金流量净额", "经营活动现金流量净额",
        "net cash from operating", "cash from operations",
        "operating cash flow", "net cash provided by operating"
    ],
    "investing_cash_flow": [
        "投资活动产生的现金流量净额", "投资活动现金流量净额",
        "net cash from investing", "investing cash flow",
        "net cash used in investing"
    ],
    "financing_cash_flow": [
        "筹资活动产生的现金流量净额", "筹资活动现金流量净额",
        "net cash from financing", "financing cash flow",
        "net cash used in financing"
    ],
}

# Sheet name detection keywords
SHEET_TYPE_KEYWORDS = {
    "income_statement": [
        "损益", "利润", "income", "profit", "loss", "p&l", "收益"
    ],
    "balance_sheet": [
        "资产负债", "balance", "财务状况", "资产"
    ],
    "cash_flow": [
        "现金流", "cash flow", "现金"
    ],
}


def normalize(text):
    """Normalize text for matching: lowercase, strip whitespace and punctuation."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    text = re.sub(r'[（）()：:、，,\s]+', ' ', text)
    text = text.strip()
    return text


def detect_sheet_type(sheet_name):
    """Detect the type of financial statement from sheet name."""
    name = normalize(sheet_name)
    for stmt_type, keywords in SHEET_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in name:
                return stmt_type
    return "unknown"


def _extract_row_value(row):
    """Extract the last numeric value from a row (most recent period)."""
    for col_idx in range(len(row) - 1, 0, -1):
        val = row.iloc[col_idx]
        if pd.notna(val):
            try:
                return float(val)
            except (ValueError, TypeError):
                continue
    return None


def find_value(df, keywords_list):
    """
    Search a DataFrame for a row matching any of the keywords,
    then return the numeric value from that row.
    Prioritizes exact matches over substring matches to avoid
    e.g. "资产合计" matching "流动资产合计" before "资产总计".
    """
    # First pass: exact match (normalized cell text == keyword)
    for idx, row in df.iterrows():
        first_col_val = normalize(str(row.iloc[0]) if pd.notna(row.iloc[0]) else "")
        second_col_val = ""
        if len(row) > 1:
            second_col_val = normalize(str(row.iloc[1]) if pd.notna(row.iloc[1]) else "")

        for kw in keywords_list:
            kw_norm = normalize(kw)
            if kw_norm == first_col_val or kw_norm == second_col_val:
                val = _extract_row_value(row)
                if val is not None:
                    return val

    # Second pass: substring match (fallback)
    for idx, row in df.iterrows():
        first_col_val = normalize(str(row.iloc[0]) if pd.notna(row.iloc[0]) else "")
        second_col_val = ""
        if len(row) > 1:
            second_col_val = normalize(str(row.iloc[1]) if pd.notna(row.iloc[1]) else "")

        for kw in keywords_list:
            kw_norm = normalize(kw)
            if kw_norm in first_col_val or kw_norm in second_col_val:
                val = _extract_row_value(row)
                if val is not None:
                    return val

    return None


def parse_statement(df, keywords_map):
    """Parse a financial statement DataFrame using keyword mappings."""
    result = {}
    for field, keywords in keywords_map.items():
        value = find_value(df, keywords)
        if value is not None:
            result[field] = value
    return result


def read_file(file_path, sheet_name=None):
    """Read an Excel or CSV file and return DataFrames keyed by sheet name."""
    ext = os.path.splitext(file_path)[1].lower()
    sheets = {}

    if ext == '.csv':
        df = pd.read_csv(file_path, header=None)
        name = sheet_name if sheet_name else "Sheet1"
        sheets[name] = df
    elif ext in ('.xlsx', '.xls'):
        xls = pd.ExcelFile(file_path)
        target_sheets = [sheet_name] if sheet_name else xls.sheet_names
        for sn in target_sheets:
            if sn in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sn, header=None)
                sheets[sn] = df
            else:
                print(json.dumps({"error": f"Sheet '{sn}' not found. Available: {xls.sheet_names}"}))
                sys.exit(1)
    else:
        print(json.dumps({"error": f"Unsupported file format: {ext}. Use .xlsx, .xls, or .csv"}))
        sys.exit(1)

    return sheets


def calculate_metrics(income_data, balance_data, cash_flow_data):
    """Calculate financial metrics from parsed statement data."""
    metrics = {}
    warnings = []

    net_income = income_data.get("net_income")
    revenue = income_data.get("revenue")
    cost_of_revenue = income_data.get("cost_of_revenue")
    gross_profit = income_data.get("gross_profit")
    total_assets = balance_data.get("total_assets")
    total_equity = balance_data.get("total_equity")
    current_assets = balance_data.get("current_assets")
    current_liabilities = balance_data.get("current_liabilities")

    # ROE = Net Income / Total Equity
    if net_income is not None and total_equity is not None and total_equity != 0:
        metrics["ROE"] = {
            "value": round(net_income / total_equity * 100, 2),
            "unit": "%",
            "formula": "净利润 / 股东权益 × 100%",
            "components": {"net_income": net_income, "total_equity": total_equity}
        }
    else:
        warnings.append("无法计算 ROE：缺少净利润或股东权益数据")

    # ROA = Net Income / Total Assets
    if net_income is not None and total_assets is not None and total_assets != 0:
        metrics["ROA"] = {
            "value": round(net_income / total_assets * 100, 2),
            "unit": "%",
            "formula": "净利润 / 总资产 × 100%",
            "components": {"net_income": net_income, "total_assets": total_assets}
        }
    else:
        warnings.append("无法计算 ROA：缺少净利润或总资产数据")

    # Gross Margin = Gross Profit / Revenue (or calculated from revenue - COGS)
    if gross_profit is None and revenue is not None and cost_of_revenue is not None:
        gross_profit = revenue - cost_of_revenue
    if gross_profit is not None and revenue is not None and revenue != 0:
        metrics["gross_margin"] = {
            "value": round(gross_profit / revenue * 100, 2),
            "unit": "%",
            "formula": "毛利润 / 营业收入 × 100%",
            "components": {"gross_profit": gross_profit, "revenue": revenue}
        }
    else:
        warnings.append("无法计算毛利率：缺少毛利润或营业收入数据")

    # Net Margin = Net Income / Revenue
    if net_income is not None and revenue is not None and revenue != 0:
        metrics["net_margin"] = {
            "value": round(net_income / revenue * 100, 2),
            "unit": "%",
            "formula": "净利润 / 营业收入 × 100%",
            "components": {"net_income": net_income, "revenue": revenue}
        }
    else:
        warnings.append("无法计算净利率：缺少净利润或营业收入数据")

    # Current Ratio = Current Assets / Current Liabilities
    if current_assets is not None and current_liabilities is not None and current_liabilities != 0:
        metrics["current_ratio"] = {
            "value": round(current_assets / current_liabilities, 2),
            "unit": "倍",
            "formula": "流动资产 / 流动负债",
            "components": {"current_assets": current_assets, "current_liabilities": current_liabilities}
        }

    # Debt-to-Asset Ratio
    total_liabilities = balance_data.get("total_liabilities")
    if total_liabilities is not None and total_assets is not None and total_assets != 0:
        metrics["debt_to_asset_ratio"] = {
            "value": round(total_liabilities / total_assets * 100, 2),
            "unit": "%",
            "formula": "总负债 / 总资产 × 100%",
            "components": {"total_liabilities": total_liabilities, "total_assets": total_assets}
        }

    # Operating Cash Flow info
    if cash_flow_data.get("operating_cash_flow") is not None:
        metrics["operating_cash_flow"] = {
            "value": cash_flow_data["operating_cash_flow"],
            "unit": "元",
            "formula": "经营活动产生的现金流量净额"
        }

    return metrics, warnings


def main():
    parser = argparse.ArgumentParser(description="Financial Statement Analyzer")
    parser.add_argument("file_path", help="Path to Excel or CSV file")
    parser.add_argument("--sheet", help="Specific sheet name to analyze", default=None)
    parser.add_argument("--output", help="Output file path (JSON)", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(json.dumps({"error": f"File not found: {args.file_path}"}))
        sys.exit(1)

    # Read file
    sheets = read_file(args.file_path, args.sheet)

    # Parse each sheet
    income_data = {}
    balance_data = {}
    cash_flow_data = {}
    parsed_sheets = {}

    for sheet_name, df in sheets.items():
        sheet_type = detect_sheet_type(sheet_name)

        if sheet_type == "income_statement":
            income_data = parse_statement(df, INCOME_STATEMENT_KEYWORDS)
            parsed_sheets[sheet_name] = {"type": "income_statement", "data": income_data}
        elif sheet_type == "balance_sheet":
            balance_data = parse_statement(df, BALANCE_SHEET_KEYWORDS)
            parsed_sheets[sheet_name] = {"type": "balance_sheet", "data": balance_data}
        elif sheet_type == "cash_flow":
            cash_flow_data = parse_statement(df, CASH_FLOW_KEYWORDS)
            parsed_sheets[sheet_name] = {"type": "cash_flow", "data": cash_flow_data}
        else:
            # Try to auto-detect by content
            trial_income = parse_statement(df, INCOME_STATEMENT_KEYWORDS)
            trial_balance = parse_statement(df, BALANCE_SHEET_KEYWORDS)
            trial_cash = parse_statement(df, CASH_FLOW_KEYWORDS)

            # Use the one with the most matches
            scores = {
                "income_statement": len(trial_income),
                "balance_sheet": len(trial_balance),
                "cash_flow": len(trial_cash),
            }
            best = max(scores, key=scores.get)

            if scores[best] > 0:
                if best == "income_statement":
                    income_data.update(trial_income)
                    parsed_sheets[sheet_name] = {"type": "income_statement", "data": trial_income}
                elif best == "balance_sheet":
                    balance_data.update(trial_balance)
                    parsed_sheets[sheet_name] = {"type": "balance_sheet", "data": trial_balance}
                elif best == "cash_flow":
                    cash_flow_data.update(trial_cash)
                    parsed_sheets[sheet_name] = {"type": "cash_flow", "data": trial_cash}
            else:
                parsed_sheets[sheet_name] = {"type": "unknown", "data": {}}

    # If only one sheet (e.g., CSV), try to extract all data from it
    if len(sheets) == 1:
        single_df = list(sheets.values())[0]
        if not income_data:
            income_data = parse_statement(single_df, INCOME_STATEMENT_KEYWORDS)
        if not balance_data:
            balance_data = parse_statement(single_df, BALANCE_SHEET_KEYWORDS)
        if not cash_flow_data:
            cash_flow_data = parse_statement(single_df, CASH_FLOW_KEYWORDS)

    # Calculate metrics
    metrics, warnings = calculate_metrics(income_data, balance_data, cash_flow_data)

    # Build result
    result = {
        "file": args.file_path,
        "sheets_analyzed": list(parsed_sheets.keys()),
        "parsed_data": {
            "income_statement": income_data,
            "balance_sheet": balance_data,
            "cash_flow": cash_flow_data,
        },
        "metrics": metrics,
        "warnings": warnings,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Results saved to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
