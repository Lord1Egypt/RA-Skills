"""
Action Suggestion Engine

Given a document type and extracted data, generates actionable
suggestions that an AI agent can present to the user or execute.

Each document type has:
- Primary action (most likely)
- Secondary actions
- Parameter extraction hints
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from .classify import (
        DOC_TYPE_INVOICE, DOC_TYPE_BUSINESS_CARD, DOC_TYPE_RECEIPT,
        DOC_TYPE_TABLE, DOC_TYPE_CONTRACT, DOC_TYPE_GENERAL,
        DOC_TYPE_ID_CARD, DOC_TYPE_PASSPORT, DOC_TYPE_BANK_STATEMENT,
        DOC_TYPE_DRIVER_LICENSE, DOC_TYPE_TAX_FORM,
        DOC_TYPE_FINANCIAL_REPORT, DOC_TYPE_MEETING_MINUTES,
        DOC_TYPE_RESUME, DOC_TYPE_TRAVEL_ITINERARY
    )
except ImportError:
    from classify import (
        DOC_TYPE_INVOICE, DOC_TYPE_BUSINESS_CARD, DOC_TYPE_RECEIPT,
        DOC_TYPE_TABLE, DOC_TYPE_CONTRACT, DOC_TYPE_GENERAL,
        DOC_TYPE_ID_CARD, DOC_TYPE_PASSPORT, DOC_TYPE_BANK_STATEMENT,
        DOC_TYPE_DRIVER_LICENSE, DOC_TYPE_TAX_FORM,
        DOC_TYPE_FINANCIAL_REPORT, DOC_TYPE_MEETING_MINUTES,
        DOC_TYPE_RESUME, DOC_TYPE_TRAVEL_ITINERARY
    )


# =============================================================================

@dataclass
class Action:
    name: str  # machine-friendly action identifier
    description: str  # human-readable description
    parameters: Dict[str, Any]  # extracted parameters from document
    confidence: float  # how sure we are that this is relevant


# =============================================================================
# Extractors (domain-specific structured data extraction)
# =============================================================================

def extract_money(text: str) -> Optional[str]:
    """Extract monetary amount from text."""
    patterns = [
        r"NT\$?\s*([\d,]+\.?\d*)",
        r"￥\s*([\d,]+\.?\d*)",
        r"¥\s*([\d,]+\.?\d*)",
        r"金額[:：]?\s*([\d,]+\.?\d*)",
        r"Total\s*[:：]?\s*\$?([\d,]+\.?\d*)",
        r"合計[:：]?\s*([\d,]+\.?\d*)",
        r"實付[:：]?\s*([\d,]+\.?\d*)",
        r"應付[:：]?\s*([\d,]+\.?\d*)",
        r"\$\s*([\d,]+\.?\d*)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m and m.lastindex >= 1:
            return m.group(1).replace(",", "")
    return None


def extract_date(text: str) -> Optional[str]:
    """Extract a date from text (basic heuristics)."""
    patterns = [
        r"發票日期[:：]?\s*(\d{4})[年.-/](\d{1,2})[月.-/](\d{1,2})[日]?",
        r"日期[:：]?\s*(\d{4})[年.-/](\d{1,2})[月.-/](\d{1,2})[日]?",
        r"Date\s*[:：]?\s*(\d{4})[/-](\d{1,2})[/-](\d{1,2})",
        r"(\d{4})[年.-/](\d{1,2})[月.-/](\d{1,2})[日]?",
        r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})",
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s*(\d{4})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            groups = m.groups()
            if len(groups) == 3:
                # Check if last group is year (4 digits) or first is
                if len(groups[0]) == 4:
                    return f"{groups[0]}-{groups[1].zfill(2)}-{groups[2].zfill(2)}"
                elif len(groups[2]) == 4:
                    return f"{groups[2]}-{groups[0].zfill(2)}-{groups[1].zfill(2)}"
            elif len(groups) == 2:
                # Month name format: "Mar 15, 2025"
                month_map = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                             "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
                # This branch needs the month name; skip for now
                pass
    return None


def extract_vendor(text: str) -> Optional[str]:
    """Extract vendor/merchant name from invoice/receipt."""
    patterns = [
        r"(?:賣方|卖方|Seller)[:：]?\s*([^\n\r]+)",
        r"(?:商店名稱|店名|Merchant)[:：]?\s*([^\n\r]+)",
        r"(?:公司名稱|Company)[:：]?\s*([^\n\r]+)",
        r"(?:供應商|Vendor)[:：]?\s*([^\n\r]+)",
        r"(?:開立|Issued by|From)[:：]?\s*([^\n\r]+)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m and m.lastindex >= 1:
            return m.group(1).strip()
    return None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number."""
    patterns = [
        r"電話[:：]?\s*([\d\-\+\(\)\s]{8,})",
        r"手机[:：]?\s*([\d\-\+\(\)\s]{8,})",
        r"Tel[:：]?\s*([\d\-\+\(\)\s]{8,})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m and m.lastindex >= 1:
            return m.group(1).strip()
    return None


def extract_email(text: str) -> Optional[str]:
    """Extract email address."""
    m = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    return m.group(0) if m else None


def extract_name(text: str) -> Optional[str]:
    """Extract person name from business card."""
    # Heuristic: look for a line with name-indicating patterns
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines:
        # Chinese name: 2-4 characters, maybe with a dot or space
        if re.match(r"^[\u4e00-\u9fa5]{2,4}", line):
            return line
        # English name: First Last pattern upper-lower case
        if re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+", line):
            return line
    return None


# =============================================================================
# Action Generators per Document Type
# =============================================================================

def suggest_invoice(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for invoice documents."""
    actions = []

    amount = extract_money(text)
    date = extract_date(text)
    vendor = extract_vendor(text)

    params = {}
    if amount:
        params["amount"] = amount
    if date:
        params["date"] = date
    if vendor:
        params["vendor"] = vendor

    actions.append(Action(
        name="create_expense",
        description="將此發票金額記入帳務系統",
        parameters=params,
        confidence=0.9 if amount else 0.5,
    ))

    actions.append(Action(
        name="archive",
        description="將此發票歸檔至文件庫",
        parameters={},
        confidence=0.95,
    ))

    if "稅" in text or "tax" in text.lower():
        actions.append(Action(
            name="tax_report",
            description="加入本期稅務報表",
            parameters={"tax_period": date or ""},
            confidence=0.7,
        ))

    return actions


def suggest_business_card(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for business card documents."""
    actions = []

    name = extract_name(text)
    phone = extract_phone(text)
    email = extract_email(text)

    params = {}
    if name:
        params["name"] = name
    if phone:
        params["phone"] = phone
    if email:
        params["email"] = email

    actions.append(Action(
        name="add_contact",
        description="新增通訊錄聯絡人",
        parameters=params,
        confidence=0.9 if (name and (phone or email)) else 0.6,
    ))

    # Could also save vCard file
    actions.append(Action(
        name="save_vcard",
        description="下載 vCard 檔案",
        parameters=params,
        confidence=0.8 if params else 0.4,
    ))

    return actions


def suggest_receipt(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for receipt documents."""
    actions = []

    amount = extract_money(text)
    merchant = extract_vendor(text)
    date = extract_date(text)

    params = {}
    if amount:
        params["amount"] = amount
    if merchant:
        params["merchant"] = merchant
    if date:
        params["date"] = date

    actions.append(Action(
        name="create_expense",
        description="記一筆支出",
        parameters=params,
        confidence=0.85 if amount else 0.5,
    ))

    actions.append(Action(
        name="split_bill",
        description="分帳計算（適合多人聚餐）",
        parameters={"total": amount or "", "merchant": merchant or ""},
        confidence=0.6,
    ))

    return actions


def suggest_table(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for tabular documents."""
    actions = []

    # Assume table data is in pruned_result; agent can extract
    actions.append(Action(
        name="export_csv",
        description="將表格匯出為 CSV",
        parameters={},
        confidence=0.95,
    ))

    actions.append(Action(
        name="analyze_data",
        description="分析表格數據（總和、平均、趨勢）",
        parameters={},
        confidence=0.8,
    ))

    return actions


def suggest_contract(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for contract documents."""
    actions = []

    actions.append(Action(
        name="summarize",
        description="生成合約重點摘要",
        parameters={},
        confidence=0.9,
    ))

    actions.append(Action(
        name="extract_dates",
        description="找出所有關鍵日期（簽署日、生效日、到期日）",
        parameters={},
        confidence=0.85,
    ))

    actions.append(Action(
        name="flag_obligations",
        description="標記義務條款與責任",
        parameters={},
        confidence=0.7,
    ))

    return actions


def suggest_general(text: str, metadata: Dict[str, Any]) -> List[Action]:
    """Suggest actions for general documents."""
    actions = []

    actions.append(Action(
        name="summarize",
        description="摘要此文件",
        parameters={},
        confidence=0.9,
    ))

    actions.append(Action(
        name="translate",
        description="翻為英文/中文",
        parameters={"target_lang": "en"},
        confidence=0.8,
    ))

    actions.append(Action(
        name="search_keywords",
        description="提取關鍵字與主題",
        parameters={},
        confidence=0.7,
    ))

    return actions


# =============================================================================
# New document type actions
# =============================================================================

def suggest_id_card(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    # Extract basic fields
    id_match = re.search(r"(?:身分證字號|ID No\.?)[:：]?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    name_match = re.search(r"姓名[:：]?\s*([^\n\r]+)", text, re.IGNORECASE)
    dob_match = re.search(r"出生日期[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2})", text)

    params = {}
    if id_match:
        params["id_number"] = id_match.group(1)
    if name_match:
        params["name"] = name_match.group(1).strip()
    if dob_match:
        params["date_of_birth"] = dob_match.group(1)

    actions.append(Action(
        name="extract_id_info",
        description="提取身份資訊",
        parameters=params,
        confidence=0.9 if params else 0.5,
    ))

    # Age verification if DOB known
    if dob_match:
        actions.append(Action(
            name="verify_age",
            description="檢查是否達法定年齡（需計算年龄）",
            parameters={"date_of_birth": params["date_of_birth"]},
            confidence=0.8,
        ))

    return actions


def suggest_passport(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    passport_match = re.search(r"(?:Passport No\.?)[:：]?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    name_match = re.search(r"Name[:：]?\s*([^\n\r]+)", text, re.IGNORECASE)
    nationality_match = re.search(r"Nationality[:：]?\s*([^\n\r]+)", text, re.IGNORECASE)
    expiry_match = re.search(r"Date of Expiry[:：]?\s*(\d{4}-\d{2}-\d{2})", text)

    params = {}
    if passport_match:
        params["passport_number"] = passport_match.group(1)
    if name_match:
        params["name"] = name_match.group(1).strip()
    if nationality_match:
        params["nationality"] = nationality_match.group(1).strip()
    if expiry_match:
        params["expiry_date"] = expiry_match.group(1)

    actions.append(Action(
        name="store_passport_info",
        description="安全儲存護照資訊（用於旅遊規劃）",
        parameters=params,
        confidence=0.9 if params else 0.5,
    ))

    if expiry_match:
        actions.append(Action(
            name="check_validity",
            description="確保護照仍在有效期內",
            parameters={"expiry_date": params["expiry_date"]},
            confidence=0.85,
        ))

    return actions


def suggest_bank_statement(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    # Basic heuristics
    balance_match = re.search(r"Current Balance[:：]?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
    account_match = re.search(r"Account(?: Number)?[:：]?\s*([\d\*]+)", text, re.IGNORECASE)
    period_match = re.search(r"Statement Period[:：]?\s*([^\n\r]+)", text, re.IGNORECASE)

    params = {}
    if balance_match and balance_match.lastindex >= 1:
        params["closing_balance"] = balance_match.group(1)
    if account_match and account_match.lastindex >= 1:
        params["account_number"] = account_match.group(1)
    if period_match and period_match.lastindex >= 1:
        params["statement_period"] = period_match.group(1).strip()

    actions.append(Action(
        name="categorize_transactions",
        description="將交易分類（食物、交通、帳單…）",
        parameters=params,
        confidence=0.9,
    ))

    if balance_match:
        actions.append(Action(
            name="highlight_large",
            description="列出大額交易",
            parameters={},
            confidence=0.8,
        ))

    actions.append(Action(
        name="generate_report",
        description="生成月度支出報告",
        parameters={},
        confidence=0.75,
    ))

    return actions


def suggest_driver_license(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    license_match = re.search(r"(?:driver'?s? license|駕照|License No\.?)[:：]?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    name_match = re.search(r"Name[:：]?\s*([^\n\r]+)", text, re.IGNORECASE)
    expiry_match = re.search(r"Expiry Date[:：]?\s*(\d{4}-\d{2}-\d{2})", text)

    params = {}
    if license_match and license_match.lastindex >= 1:
        params["license_number"] = license_match.group(1)
    if name_match and name_match.lastindex >= 1:
        params["name"] = name_match.group(1).strip()
    if expiry_match and expiry_match.lastindex >= 1:
        params["expiry_date"] = expiry_match.group(1)

    actions.append(Action(
        name="store_license_info",
        description="安全儲存駕照資訊",
        parameters=params,
        confidence=0.85 if params else 0.5,
    ))

    if expiry_match:
        actions.append(Action(
            name="check_expiry",
            description="檢查駕照是否已過期或即將過期",
            parameters={"expiry_date": params["expiry_date"]},
            confidence=0.9,
        ))

    return actions


def suggest_tax_form(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    year_match = re.search(r"(?:tax year|所得年度)[:：]?\s*(\d{3,4})", text, re.IGNORECASE)
    income_match = re.search(r"(?:總收入|Total Income|total income)[:：]?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)
    tax_match = re.search(r"(?:應納稅額|Tax Payable)[:：]?\s*([\d,]+\.?\d*)", text, re.IGNORECASE)

    params = {}
    if year_match and year_match.lastindex >= 1:
        params["tax_year"] = year_match.group(1)
    if income_match and income_match.lastindex >= 1:
        params["total_income"] = income_match.group(1)
    if tax_match and tax_match.lastindex >= 1:
        params["tax_payable"] = tax_match.group(1)

    actions.append(Action(
        name="summarize_tax",
        description="生成稅務摘要",
        parameters=params,
        confidence=0.9,
    ))

    actions.append(Action(
        name="check_errors",
        description="對比去年資料，檢查異常",
        parameters=params,
        confidence=0.75,
    ))

    actions.append(Action(
        name="suggest_deductions",
        description="列出可能遺漏的減免項目",
        parameters={},
        confidence=0.7,
    ))

    return actions


def suggest_financial_report(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    revenue_match = re.search(r"(?:營收|Revenue)[:：]?\s*\$?([\d,.]+M?)", text, re.IGNORECASE)
    net_match = re.search(r"(?:淨損|淨利|Net (?:Income|Loss))[:：]?\s*\$?([-\d,.]+M?)", text, re.IGNORECASE)
    params = {}
    if revenue_match:
        params["revenue"] = revenue_match.group(1)
    if net_match:
        params["net_income"] = net_match.group(1)

    actions.append(Action(name="summarize_financials", description="生成財務摘要", parameters=params, confidence=0.9))
    actions.append(Action(name="compare_periods", description="與前期比較", parameters={}, confidence=0.75))
    actions.append(Action(name="flag_risks", description="標記財務風險指標", parameters={}, confidence=0.7))
    return actions


def suggest_meeting_minutes(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    actions.append(Action(name="extract_action_items", description="提取待辦事項", parameters={}, confidence=0.9))
    actions.append(Action(name="create_calendar_events", description="建立日曆事件（會議、截止日）", parameters={}, confidence=0.7))
    actions.append(Action(name="send_summary", description="發送會議摘要給出席者", parameters={}, confidence=0.65))
    return actions


def suggest_resume(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    email_match = extract_email(text)
    phone_match = extract_phone(text)
    name_match = extract_name(text)
    params = {}
    if name_match:
        params["name"] = name_match
    if email_match:
        params["email"] = email_match
    if phone_match:
        params["phone"] = phone_match
    actions.append(Action(name="create_candidate_profile", description="建立候選人資料", parameters=params, confidence=0.85))
    actions.append(Action(name="match_jobs", description="比對職缺需求", parameters={}, confidence=0.6))
    actions.append(Action(name="extract_skills", description="列出技能與經驗摘要", parameters={}, confidence=0.8))
    return actions


def suggest_travel_itinerary(text: str, metadata: Dict[str, Any]) -> List[Action]:
    actions = []
    actions.append(Action(name="create_calendar_events", description="加入航班與住宿到日曆", parameters={}, confidence=0.85))
    actions.append(Action(name="set_reminders", description="設定出發前提醒", parameters={}, confidence=0.7))
    actions.append(Action(name="check_visa", description="檢查簽證需求", parameters={}, confidence=0.6))
    return actions


# =============================================================================
# Main Dispatcher
# =============================================================================

SUGGESTION_DISPATCH = {
    DOC_TYPE_INVOICE: suggest_invoice,
    DOC_TYPE_BUSINESS_CARD: suggest_business_card,
    DOC_TYPE_RECEIPT: suggest_receipt,
    DOC_TYPE_TABLE: suggest_table,
    DOC_TYPE_CONTRACT: suggest_contract,
    DOC_TYPE_ID_CARD: suggest_id_card,
    DOC_TYPE_PASSPORT: suggest_passport,
    DOC_TYPE_BANK_STATEMENT: suggest_bank_statement,
    DOC_TYPE_DRIVER_LICENSE: suggest_driver_license,
    DOC_TYPE_TAX_FORM: suggest_tax_form,
    DOC_TYPE_FINANCIAL_REPORT: suggest_financial_report,
    DOC_TYPE_MEETING_MINUTES: suggest_meeting_minutes,
    DOC_TYPE_RESUME: suggest_resume,
    DOC_TYPE_TRAVEL_ITINERARY: suggest_travel_itinerary,
    DOC_TYPE_GENERAL: suggest_general,
}


def suggest_actions(
    doc_type: str,
    text: str,
    metadata: Dict[str, Any],
    pruned_result: Any = None,
) -> List[Action]:
    """
    Generate suggested actions based on document type and content.

    Args:
        doc_type: Document type from classifier
        text: Full extracted text
        metadata: Additional document metadata (pages, language, etc.)
        pruned_result: Structured page-level data (can be used to refine suggestions)

    Returns:
        List of Action objects, sorted by confidence (high -> low)
    """
    if doc_type not in SUGGESTION_DISPATCH:
        doc_type = DOC_TYPE_GENERAL

    actions = SUGGESTION_DISPATCH[doc_type](text, metadata)
    return sorted(actions, key=lambda a: a.confidence, reverse=True)


# =============================================================================
# Serialization for Agent Consumption
# =============================================================================

def actions_to_dict(actions: List[Action]) -> List[Dict[str, Any]]:
    return [
        {
            "action": a.name,
            "description": a.description,
            "parameters": a.parameters,
            "confidence": a.confidence,
        }
        for a in actions
    ]


# For standalone testing
if __name__ == "__main__":
    import sys
    from pathlib import Path
    import json

    test_cases = [
        ("invoice", "發票號碼: AB12345678\n金額: NT$ 1,200\n賣方: 某某科技"),
        ("business_card", "姓名: 王大明\n電話: 0912-345-678\nEmail: test@example.com"),
        ("id_card", "身分證字號: A123456789\n姓名: 李四\n出生日期: 1990年01月01日"),
        ("passport", "Passport No: X1234567\nName: John Doe\nNationality: US"),
        ("bank_statement", "Account Number: ****1234\nStatement Period: 2025-03-01 to 2025-03-31\nCurrent Balance: $5,000"),
        ("tax_form", "Tax Year: 2024\nTotal Income: $120,000\nTax Payable: $15,000"),
    ]

    print("Testing action suggestions...\n")
    try:
        from .classify import classify
    except ImportError:
        from classify import classify
    for expected_type, sample in test_cases:
        result = classify(sample)
        print(f"[{expected_type}] detected as: {result.doc_type} (conf={result.confidence:.2f})")
        actions = suggest_actions(result.doc_type, sample, {})
        print(f"  Top action: {actions[0].name if actions else 'none'}")
        for a in actions:
            print(f"    - {a.name} ({a.confidence:.2f}): {a.description}")
        print()
