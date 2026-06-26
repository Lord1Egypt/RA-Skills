"""
Document Type Classifier

Detects document type from extracted text using heuristics,
keywords, and layout patterns.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

# =============================================================================
# Document Type Definitions
# =============================================================================

DOC_TYPE_INVOICE = "invoice"
DOC_TYPE_BUSINESS_CARD = "business_card"
DOC_TYPE_RECEIPT = "receipt"
DOC_TYPE_TABLE = "table"
DOC_TYPE_CONTRACT = "contract"
DOC_TYPE_ID_CARD = "id_card"
DOC_TYPE_PASSPORT = "passport"
DOC_TYPE_BANK_STATEMENT = "bank_statement"
DOC_TYPE_DRIVER_LICENSE = "driver_license"
DOC_TYPE_TAX_FORM = "tax_form"
DOC_TYPE_FINANCIAL_REPORT = "financial_report"
DOC_TYPE_MEETING_MINUTES = "meeting_minutes"
DOC_TYPE_RESUME = "resume"
DOC_TYPE_TRAVEL_ITINERARY = "travel_itinerary"
DOC_TYPE_GENERAL = "general"


# =============================================================================
# Pattern Matchers
# =============================================================================

def match_invoice(text: str) -> float:
    """
    Invoice patterns:
    - Keywords: 發票、發票號碼、統一編號、稅額、金額、發票日期
    - Layout: table with totals, tax labels
    """
    patterns = [
        r"發票|發票號碼|發票日期",
        r"統一編號|稅額|銷售額",
        r"金額|NT\$|新台幣|Total|Amount",
        r"買受人|卖方|seller|buyer",
        r"品項|項目|desc(?:ription)?",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_business_card(text: str) -> float:
    """
    Business card patterns:
    - Name + phone + email in proximity
    - Job title, company name
    - Address blocks
    """
    patterns = [
        r"姓名|姓名[:：]|[A-Z][a-z]+ [A-Z][a-z]+",  # English name pattern
        r"(?:Tel|電話|Phone)[:：]?\s*[\d\-\+\(\)]+",
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        r"地址|Addr(?:ess)?|Company",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_receipt(text: str) -> float:
    """
    Receipt patterns:
    - Merchant name, transaction ID, total paid
    - Keywords: 收據、收銀、小計、折扣、實付
    """
    patterns = [
        r"收據|收銀|收據號碼|Receipt No\.",
        r"Merchant|商店|商號",
        r"小計|折扣|實付|Total|Paid",
        r"交易日期|Time|DateTime",
        r"付款方式|Payment",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_table(text: str) -> float:
    """
    Table pattern:
    - Grid characters: |, -, +, tabular alignment
    - Header row with multiple columns
    - Repeated separators
    - Must have multiple lines to be considered a table (avoid single-line false positives)
    """
    lines = [l for l in text.split("\n") if l.strip()]
    if len(lines) < 3:
        return 0.0  # not enough lines for a table
    table_like = sum(1 for line in lines if "|" in line or "\t" in line or line.count(" ") > 5)
    score = table_like / len(lines)
    return min(score * 1.2, 1.0)  # slight boost


def match_contract(text: str) -> float:
    """
    Contract patterns:
    - Terms like 合約、contract、agreement、條款
    - Signatures, dates, parties
    - Clauses numbering (第1條、Article 1)
    """
    patterns = [
        r"合約|合約條款|Contract|Agreement",
        r"甲方|乙方|Party A|Party B",
        r"第[一二三四五六七八九十\d]+條|Article \d+",
        r"簽署|簽名|Signature|Signed",
        r"生效日|有效期限|Date of Effect",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_id_card(text: str) -> float:
    """
    ID Card patterns (Chinese / Taiwanese):
    - 身分證字號、身份證、ID No.
    - 出生日期、出生地
    - 姓名、性別、發照日期
    """
    patterns = [
        r"身分證字號|身份證|ID No\.|Identification",
        r"出生日期|Date of Birth|出生地",
        r"姓名|Name",
        r"性別|Sex|Gender",
        r"發照日期|Issue Date|有效期",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_passport(text: str) -> float:
    """
    Passport patterns:
    - Passport No., 護照號碼
    - 國籍、Nationality
    - Date of issue/expiry
    """
    patterns = [
        r"(?:Passport No|護照號碼)[.:：]?" ,
        r"National(?:ity)?|國籍",
        r"Date of Issue|签发日期|發照日期",
        r"Date of Expiry|有效期至|到期日",
        r"Place of Birth|出生地",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_bank_statement(text: str) -> float:
    """
    Bank statement patterns:
    - Account number, statement period, balance
    - Banks keywords: 銀行、銀行對帳單、Statement
    """
    patterns = [
        r"account(?: number)?|帳戶號碼|銀行帳號",
        r"statement period|帳單期間|週期",
        r"balance|余额|結餘|Current Balance",
        r"银行|Bank|Financial Institution",
        r"transaction|交易明細|交易紀錄",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_driver_license(text: str) -> float:
    """
    Driver license patterns:
    - License number, class, expiry
    - Name, address, date of birth
    """
    patterns = [
        r"driver'?s? license|駕駛執照|駕照",
        r"license class|類別|Class [A-Z]",
        r"expir(?:y|ation)|到期日|失效日期",
        r"address|地址|住址",
        r"date of birth|出生日期",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_tax_form(text: str) -> float:
    """
    Tax form patterns (e.g., 綜合所得稅申報書):
    - Tax year, taxpayer ID, income, deductions
    """
    patterns = [
        r"tax year|所得年度|申报年度",
        r"taxpayer|納稅人識別編號|身分證字號",
        r"income|所得|收入",
        r"deduction|扣除額|免稅額",
        r"tax payable|應納稅額",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_financial_report(text: str) -> float:
    """
    Financial report / analysis patterns:
    - Quarterly/annual reports, earnings, revenue, net income
    - SEC filings language, stock analysis
    """
    patterns = [
        r"財務報告|財報|Financial Report|Annual Report",
        r"營收|Revenue|Net Income|淨損|淨利|EPS",
        r"資產負債|Balance Sheet|Cash Flow|現金流",
        r"每股|股價|市值|Market Cap|股數",
        r"毛利率|營業利益|Operating Income|EBITDA",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_meeting_minutes(text: str) -> float:
    """
    Meeting minutes patterns:
    - Attendees, agenda, action items, decisions
    """
    patterns = [
        r"會議記錄|會議紀要|Meeting Minutes|Minutes of",
        r"出席|Attendees|Participants|與會",
        r"決議|Resolution|Action Items|待辦事項",
        r"會議時間|Date.*Time|下次會議|Next Meeting",
        r"主席|Chair|Moderator|主持人",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_resume(text: str) -> float:
    """
    Resume / CV patterns:
    - Education, experience, skills, contact
    """
    patterns = [
        r"履歷|簡歷|Resume|Curriculum Vitae|CV",
        r"學歷|Education|Degree|University|大學",
        r"工作經歷|Work Experience|Employment|任職",
        r"技能|Skills|Competenc|專長",
        r"Email.*Phone|電話.*信箱|Contact|聯繫方式",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


def match_travel_itinerary(text: str) -> float:
    """
    Travel itinerary patterns:
    - Flight, hotel, dates, destinations
    """
    patterns = [
        r"行程|Itinerary|Travel Plan|旅遊",
        r"航班|Flight|航班號|Departure|Arrival",
        r"酒店|Hotel|住宿|Check-in|Check-out",
        r"目的地|Destination|出發|Arrival",
        r"護照|Passport|簽證|Visa|機票",
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return min(matches / len(patterns), 1.0)


# =============================================================================
# Main Classifier
# =============================================================================

@dataclass
class ClassificationResult:
    doc_type: str
    confidence: float
    scores: Dict[str, float]


def classify(text: str) -> ClassificationResult:
    """
    Classify document type from extracted text.

    Args:
        text: Full OCR-extracted text

    Returns:
        ClassificationResult with type, confidence, and all scores
    """
    scores = {
        DOC_TYPE_INVOICE: match_invoice(text),
        DOC_TYPE_BUSINESS_CARD: match_business_card(text),
        DOC_TYPE_RECEIPT: match_receipt(text),
        DOC_TYPE_TABLE: match_table(text),
        DOC_TYPE_CONTRACT: match_contract(text),
        DOC_TYPE_ID_CARD: match_id_card(text),
        DOC_TYPE_PASSPORT: match_passport(text),
        DOC_TYPE_BANK_STATEMENT: match_bank_statement(text),
        DOC_TYPE_DRIVER_LICENSE: match_driver_license(text),
        DOC_TYPE_TAX_FORM: match_tax_form(text),
        DOC_TYPE_FINANCIAL_REPORT: match_financial_report(text),
        DOC_TYPE_MEETING_MINUTES: match_meeting_minutes(text),
        DOC_TYPE_RESUME: match_resume(text),
        DOC_TYPE_TRAVEL_ITINERARY: match_travel_itinerary(text),
    }

    best_type = max(scores, key=scores.get)
    confidence = scores[best_type]

    # If none match strongly, default to general
    if confidence < 0.3:
        best_type = DOC_TYPE_GENERAL
        confidence = 1.0  # general is fallback

    return ClassificationResult(
        doc_type=best_type,
        confidence=confidence,
        scores=scores,
    )


# Simple test
if __name__ == "__main__":
    test_texts = {
        "invoice": "發票號碼: AB12345678\n統一編號: 12345678\n金額: NT$ 1,200\n發票日期: 2025年03月15日",
        "business_card": "姓名: 王大明\n電話: 0912-345-678\nEmail: test@example.com",
        "receipt": "收據號碼: R20250315001\n商店: 7-ELEVEN\n實付: 85元",
        "contract": "合約甲方: 某某公司\n第1條\n簽署人: 張三",
        "id_card": "身分證字號: A123456789\n姓名: 李四\n出生日期: 1990年01月01日",
        "financial_report": "財務報告 2024\n營收: 1.812M\n淨損: -54.709M\n毛利率: -94.8%",
        "meeting_minutes": "會議記錄\n出席: 王經理、李主管\n決議: 通過Q2預算\n下次會議: 2025-04-01",
        "resume": "王大明\nEmail: wang@test.com Phone: 0912-345-678\n學歷: 台灣大學資訊工程系\n工作經歷: 軟體工程師 3年\n技能: Python, JavaScript",
        "travel_itinerary": "旅遊行程\n航班: BR851 台北-東京 08:00\n酒店: Hilton Tokyo Check-in: 2025-04-01\n目的地: 東京",
        "general": "這是一個普通文件內容。",
    }

    for name, text in test_texts.items():
        result = classify(text)
        print(f"[{name}] detected: {result.doc_type} (conf: {result.confidence:.2f})")
        print(f"  scores: {result.scores}")
        print()
