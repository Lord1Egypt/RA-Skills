"""
Broker statement parser. Extract trades and balances from local text PDFs. Do not generate official tax filings.

Supports: 华泰(HTSC), 富途(Futu), 盈透(IBKR), 辉立(Phillip)
"""
import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import pdfplumber
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Install the pinned packages listed in requirements.txt before running this script."
    ) from exc


class BrokerDetector:
    """Auto-detect broker from PDF content."""

    PATTERNS = {
        "htsc": {
            "name": "华泰金融控股（香港）有限公司",
            "name_en": "Huatai Financial Holdings (Hong Kong) Co., Limited",
            "country": "HK",
            "keywords": ["华泰金融控股", "HTSC", "htsc.com", "B01829"],
        },
        "futu": {
            "name": "富途证券国际（香港）有限公司",
            "name_en": "Futu Securities International (Hong Kong) Limited",
            "country": "HK",
            "keywords": ["富途证券", "Futu Securities", "futuhk", "futunn"],
        },
        "ibkr": {
            "name": "盈透证券",
            "name_en": "Interactive Brokers LLC",
            "country": "US",
            "keywords": ["Interactive Brokers", "IBKR", "盈透"],
        },
        "phillip": {
            "name": "辉立证券（香港）有限公司",
            "name_en": "Phillip Securities (Hong Kong) Limited",
            "country": "HK",
            "keywords": ["辉立证券", "Phillip Securities", "phillip.com"],
        },
    }

    @classmethod
    def detect(cls, text):
        scores = {}
        for broker_id, info in cls.PATTERNS.items():
            score = sum(1 for kw in info["keywords"] if kw.lower() in text.lower())
            if score > 0:
                scores[broker_id] = score
        if scores:
            best = max(scores, key=scores.get)
            return best, cls.PATTERNS[best]
        return None, None


class HTSCParser:
    """Parser for 华泰(HTSC) Hong Kong daily/monthly statements."""

    @staticmethod
    def parse(text):
        data = {
            "client_name": None,
            "account_number": None,
            "account_type": None,
            "address": None,
            "statement_date": None,
            "currencies": {},
            "holdings": [],
            "total_value_hkd": None,
            "transactions": [],
            "fees": {},
        }

        lines = text.split("\n")

        # --- Client name and account ---
        for line in lines:
            # Pattern: "张三 (0123456789) 客户户口 : 0123456789"
            m = re.search(r"(\S+)\s*\((\d+)\).*客户户口\s*:\s*(\d+)", line)
            if m:
                data["client_name"] = m.group(1)
                data["account_number"] = m.group(3)
            # Account type
            if "户口类别" in line:
                m = re.search(r"户口类别\s*:\s*(.+?)\s", line)
                if m:
                    data["account_type"] = m.group(1)
            # Address
            if "區" in line or "市" in line or "省" in line:
                if not data["address"] and "省" not in line:
                    continue
                if re.search(r"[\u4e00-\u9fff]{2,}(?:省|市|區|镇|路|號|号|座)", line):
                    if not re.search(r"(?:皇后|中心|大道|Tel|电话|傳真)", line):
                        data["address"] = line.strip()

        # --- Address: collect multi-line ---
        addr_lines = []
        capture = False
        for line in lines:
            if re.search(r"[\u4e00-\u9fff]{2,}省[\u4e00-\u9fff]{2,}市", line):
                capture = True
            if capture:
                if re.search(r"(?:客户主任|列印|户口类别)", line):
                    break
                clean = line.strip()
                if clean and not re.search(r"(?:皇后|中心|大道|Tel|电话|傳真|^$)", clean):
                    addr_lines.append(clean)
        if addr_lines:
            data["address"] = "".join(addr_lines)

        # --- Statement date ---
        for line in lines:
            m = re.search(r"列印于\s*(\d{4}-\d{2}-\d{2})", line)
            if m:
                data["statement_date"] = m.group(1)
                break
            m = re.search(r"日结单\s*\((\d{4}-\d{2}-\d{2})\)", line)
            if m:
                data["statement_date"] = m.group(1)
                break

        # --- Portfolio total value ---
        for line in lines:
            m = re.search(r"投资组合总值\s*HKD\s*([\d,]+\.?\d*)", line)
            if m:
                data["total_value_hkd"] = float(m.group(1).replace(",", ""))

        # --- Portfolio summary ---
        for line in lines:
            # HKD line
            m = re.search(
                r"HKD\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d\-,]+\.?\d*)\s+"
                r"([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+"
                r"([\d,]+\.?\d*)\s+([\d,.]+)\s+([\d,]+\.?\d*)", line
            )
            if m:
                cash = float(m.group(1).replace(",", ""))
                net = float(m.group(3).replace(",", "").replace("-", ""))
                stocks = float(m.group(4).replace(",", ""))
                fund = float(m.group(6).replace(",", ""))
                total = float(m.group(8).replace(",", ""))
                data["currencies"]["HKD"] = {
                    "cash": cash, "net_balance": net,
                    "stocks_value": stocks, "fund_value": fund,
                    "total": total, "exchange_rate": float(m.group(9).replace(",", "")),
                }
            # USD line
            m = re.search(
                r"USD\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d\-,]+\.?\d*)\s+"
                r"([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+"
                r"([\d,]+\.?\d*)\s+([\d,.]+)\s+([\d,]+\.?\d*)", line
            )
            if m:
                cash = float(m.group(1).replace(",", ""))
                net = float(m.group(3).replace(",", "").replace("-", ""))
                stocks = float(m.group(4).replace(",", ""))
                fund = float(m.group(6).replace(",", ""))
                total = float(m.group(8).replace(",", ""))
                data["currencies"]["USD"] = {
                    "cash": cash, "net_balance": net,
                    "stocks_value": stocks, "fund_value": fund,
                    "total": total, "exchange_rate": float(m.group(9).replace(",", "")),
                }

        # --- Holdings ---
        in_holdings = False
        current_section = None
        for line in lines:
            if "持货结存" in line:
                in_holdings = True
                continue
            if in_holdings:
                # Section header: e.g. "HK - HONG KONG STOCK (HKD)" or "FUND - FUND (USD)"
                m = re.match(r"(FUND|HK|US)\s*-\s*(.+?)\s*\((\w+)\)", line)
                if m:
                    current_section = m.group(3)
                    continue
                # Stop conditions
                if any(kw in line for kw in ["预告", "股票借贷", "利息", "待交收", "成交单据", "融资", "重要提示"]):
                    in_holdings = False
                    continue
                # Holding line: "CODE  NAME  QTY...  PRICE  VALUE..."
                # Look for known stock patterns
                # HK stock: "00401 万嘉集团 200 200 0 200 0.166 33.20 0 0.00 0.00"
                # US stock: "AAPL 苹果 10 10 0 10 180.95 1,809.50 60 1,085.70 0.00"
                # Fund: "HK0000846540 ChinaAMC Select... 1,120.95 1,121.59..."
                parts = line.split()
                if len(parts) >= 6:
                    # Try to detect if this is a holding line
                    code = parts[0]
                    # Fund pattern
                    if re.match(r"[A-Z]{2}\d{8,}", code):
                        try:
                            qty_idx = None
                            price_idx = None
                            val_idx = None
                            for i, p in enumerate(parts):
                                if re.match(r"^[\d,]+\.?\d*$", p) and qty_idx is None:
                                    qty_idx = i
                                elif re.match(r"^[\d,]+\.?\d*$", p) and price_idx is None and i > qty_idx:
                                    # Check if likely a price (less digits after decimal or looks like a price)
                                    if "." in p and len(p.split(".")[1]) <= 4:
                                        price_idx = i
                                        break
                            if qty_idx and price_idx:
                                name = " ".join(parts[1:qty_idx])
                                market_value = float(parts[price_idx + 1].replace(",", ""))
                                data["holdings"].append({
                                    "code": code,
                                    "name": name,
                                    "currency": current_section or "HKD",
                                    "type": "fund",
                                    "market_value": market_value,
                                })
                        except (ValueError, IndexError):
                            pass
                    # US stock: "AAPL 苹果 10 10 0 10 180.95 1,809.50 60 1,085.70 0.00"
                    elif re.match(r"^[A-Z]{1,5}$", code):
                        try:
                            # Find numeric value that looks like market value
                            numbers_in_line = []
                            for p in parts:
                                try:
                                    v = float(p.replace(",", ""))
                                    numbers_in_line.append(v)
                                except ValueError:
                                    pass
                            if len(numbers_in_line) >= 2:
                                market_value = numbers_in_line[-3]  # Usually the market value
                                data["holdings"].append({
                                    "code": code,
                                    "name": parts[1] if len(parts) > 1 else "",
                                    "currency": current_section or "USD",
                                    "type": "stock",
                                    "market_value": market_value,
                                })
                        except (ValueError, IndexError):
                            pass
                    # HK stock: "00401 万嘉集团 200 200 0 200 0.166 33.20 0 0.00 0.00"
                    elif re.match(r"^\d{5}$", code):
                        try:
                            numbers_in_line = []
                            for p in parts:
                                try:
                                    v = float(p.replace(",", ""))
                                    numbers_in_line.append(v)
                                except ValueError:
                                    pass
                            if len(numbers_in_line) >= 2:
                                market_value = numbers_in_line[-3]
                                data["holdings"].append({
                                    "code": code,
                                    "name": parts[1] if len(parts) > 1 else "",
                                    "currency": current_section or "HKD",
                                    "type": "stock",
                                    "market_value": market_value,
                                })
                        except (ValueError, IndexError):
                            pass

        # --- Transactions from 户口变动 ---
        in_movements = False
        in_trade_confirm = False
        for i, line in enumerate(lines):
            # Track which section we're in
            if "户口变动" in line:
                in_movements = True
                in_trade_confirm = False
                continue
            if "成交单据" in line:
                in_trade_confirm = True
                in_movements = False
                continue
            if in_movements and any(kw in line for kw in ["持货结存", "待交收", "利息", "预告", "股票借贷", "重要提示", "融资"]):
                in_movements = False
                continue
            if in_trade_confirm and any(kw in line for kw in ["户口变动", "持货结存", "利息", "预告"]):
                in_trade_confirm = False
                continue

            # ---- Parse 户口变动 format ----
            if in_movements:
                m = re.search(
                    r"(\d{10})\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})\s+买卖交易\s+"
                    r"(买入|卖出)(开仓|平仓)\s+(.+?)\s+@?\s*([\d,.]+)\s*"
                    r"\(?(\d[\d,]*)\)?\s+\(?([\d,\-]+\.?\d*)\)?\s+\(?([\d,\-]+\.?\d*)\)?",
                    line
                )
                if m:
                    ref_no = m.group(1)
                    settlement_date = m.group(2)
                    trade_date = m.group(3)
                    direction = m.group(4)
                    open_close = m.group(5)
                    product = m.group(6).strip().rstrip(":")
                    price = float(m.group(7).replace(",", ""))
                    qty = int(m.group(8).replace(",", ""))
                    amount = float(m.group(9).replace(",", ""))
                    data["transactions"].append({
                        "ref_no": ref_no,
                        "settlement_date": settlement_date,
                        "trade_date": trade_date,
                        "direction": direction,
                        "open_close": open_close,
                        "product": product,
                        "price": price,
                        "quantity": qty,
                        "amount": amount,
                    })
                continue

            # ---- Parse 成交单据 format ----
            if in_trade_confirm:
                # Match header line: "0006261313 2023-06-02 卖出 BAC:US USD 28.855 (200)CLEARING..."
                m = re.search(
                    r"(\d{10})\s+(\d{4}-\d{2}-\d{2})\s+(买入|卖出)\s+"
                    r"([A-Z]+):?(?:US|HK)?\s+(HKD|USD|CNH|JPY)\s+"
                    r"([\d,.]+)\s+\(?(\d[\d,]*)\)?",
                    line
                )
                if m:
                    ref_no = m.group(1)
                    trade_date = m.group(2)
                    direction = m.group(3)
                    product = m.group(4)
                    ccy = m.group(5)
                    price = float(m.group(6).replace(",", ""))
                    qty = int(m.group(7).replace(",", ""))
                    # Look for net amount in following lines
                    net_amount = None
                    for j in range(i+1, min(i+8, len(lines))):
                        nm = re.search(r"净金额\s+\(?([\d,\-]+\.?\d*)\)?", lines[j])
                        if nm:
                            net_amount = float(nm.group(1).replace(",", ""))
                            break
                    data["transactions"].append({
                        "ref_no": ref_no,
                        "trade_date": trade_date,
                        "direction": direction,
                        "product": product,
                        "currency": ccy,
                        "price": price,
                        "quantity": qty,
                        "net_amount": net_amount,
                    })
                continue
        for line in lines:
            m = re.search(r"(?:融资计息|利息).*?([\d,]+\.?\d*)\s*<(\d+)%>", line)
            if m:
                data["fees"]["margin_interest"] = float(m.group(1).replace(",", ""))

        return data


def parse_statement(pdf_path):
    """Main entry: parse any supported broker PDF."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"

    broker_id, broker_info = BrokerDetector.detect(full_text)
    if not broker_id:
        return {"error": "Unsupported broker", "text_preview": full_text[:500]}

    if broker_id == "htsc":
        data = HTSCParser.parse(full_text)
    else:
        return {"error": f"Parser for {broker_info['name']} not yet implemented"}

    data["broker_id"] = broker_id
    data["broker"] = broker_info
    return data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse a local broker PDF into JSON.")
    parser.add_argument("pdf")
    args = parser.parse_args()
    print(json.dumps(parse_statement(args.pdf), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
