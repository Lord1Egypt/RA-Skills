#!/usr/bin/env python3
"""
合同风险智能审查 - Contract Risk Reviewer
Main analysis script for PDF contract analysis.
"""

import sys
import json
import uuid
import os
import argparse
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

# ── 91Skillhub Token Verification ─────────────────────────────────────────────
VERIFY_URL = "https://api.yk-global.com/v1/verify"


def _map_prefix_to_tier(api_key: str) -> str:
    """Map API key prefix to tier name."""
    upper = api_key.upper() if api_key else ""
    if "-MAX" in upper:
        return "MAX"
    if "-ENT" in upper:
        return "MAX"
    if "-PRO" in upper:
        return "PRO"
    if "-STD" in upper:
        return "STD"
    if "-BSC" in upper:
        return "STD"
    if "-FREE" in upper:
        return "FREE"
    return "FREE"


def verify_token(api_key: str) -> dict:
    """
    Verify API key via 91Skillhub API.
    Returns dict with keys: valid (bool), tier (str), error (str, if failed).
    On network error, degrades to FREE tier gracefully.
    """
    if not api_key:
        return {"valid": False, "tier": "FREE", "error": "No API key provided"}

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success") and data.get("valid"):
                tier = _map_prefix_to_tier(api_key)
                return {"valid": True, "tier": tier}
            else:
                return {
                    "valid": False,
                    "tier": "FREE",
                    "error": data.get("error", "Key无效或已过期"),
                }
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            return {
                "valid": False,
                "tier": "FREE",
                "error": err_body.get("error", f"HTTP {e.code}"),
            }
        except Exception:
            return {"valid": False, "tier": "FREE", "error": f"HTTP {e.code}"}
    except Exception as e:
        # Network error — degrade to FREE, don't block user
        return {"valid": False, "tier": "FREE", "error": str(e)}


# ── PDF Text Extraction ──────────────────────────────────────────────────────

def extract_text_pymupdf(pdf_path: str) -> str:
    """Extract text using PyMuPDF (fitz)."""
    import fitz
    doc = fitz.open(pdf_path)
    pages_text = []
    for page in doc:
        text = page.get_text("text")
        if text:
            pages_text.append(text)
    return "\n".join(pages_text)


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Extract text using pdfplumber."""
    import pdfplumber
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t)
    return "\n".join(pages_text)


def extract_text_ocr(pdf_path: str, languages: str = "chi_sim+eng") -> str:
    """OCR for scanned/image PDFs using pytesseract + pdf2image."""
    import pytesseract
    from pdf2image import convert_from_path
    import numpy as np

    images = convert_from_path(pdf_path, dpi=200)
    ocr_texts = []
    for img in images:
        img_array = np.array(img)
        text = pytesseract.image_to_string(img_array, lang=languages)
        if text.strip():
            ocr_texts.append(text)
    return "\n".join(ocr_texts)


def extract_pdf_text(pdf_path: str) -> tuple[str, bool]:
    """
    Extract text from PDF, trying PyMuPDF → pdfplumber → OCR.
    Returns (text, was_ocr: bool).
    """
    text = ""
    used_ocr = False

    # Try PyMuPDF first
    try:
        text = extract_text_pymupdf(pdf_path)
    except Exception as e:
        print(f"[WARN] PyMuPDF extraction failed: {e}", file=sys.stderr)

    # Fallback to pdfplumber
    if not text or len(text.strip()) < 50:
        try:
            text2 = extract_text_pdfplumber(pdf_path)
            if text2 and len(text2.strip()) > len(text.strip()):
                text = text2
        except Exception as e:
            print(f"[WARN] pdfplumber extraction failed: {e}", file=sys.stderr)

    # Last resort: OCR
    if not text or len(text.strip()) < 50:
        print("[INFO] Low text yield, attempting OCR...", file=sys.stderr)
        try:
            text = extract_text_ocr(pdf_path)
            used_ocr = True
        except Exception as e:
            print(f"[WARN] OCR extraction failed: {e}", file=sys.stderr)

    return text, used_ocr


# ── Contract Type Detection & AI Analysis ───────────────────────────────────

def detect_contract_type_and_lang(text: str) -> tuple[str, str]:
    """Heuristic pre-check of contract type and language before sending to AI."""
    # Language detection
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in text.split() if w.isascii()])
    is_chinese = chinese_chars > 50
    is_english = english_words > 100

    if is_chinese and is_english:
        language = "Bilingual (中文+English)"
    elif is_chinese:
        language = "中文"
    else:
        language = "English"

    # Simple keyword-based pre-detection
    text_lower = text.lower()
    if any(k in text_lower for k in ["劳动合同", "聘用", "用人单位", "劳动者", "工资", "社会保险"]):
        contract_type = "劳动合同"
    elif any(k in text_lower for k in ["采购", "供应商", "货物", "供货", "采购方"]):
        contract_type = "采购合同"
    elif any(k in text_lower for k in ["销售", "买方", "出卖", "销售方", "产品"]):
        contract_type = "销售合同"
    elif any(k in text_lower for k in ["租赁", "承租", "出租", "租金", "房屋", "场地"]):
        contract_type = "租赁合同"
    elif any(k in text_lower for k in ["保密", "nda", "confidential", "机密", "商业秘密", "泄密"]):
        contract_type = "保密协议"
    else:
        contract_type = "其他"

    return contract_type, language


def build_analysis_prompt(text: str, contract_type: str, language: str, tier: str = "FREE") -> str:
    """Build the AI prompt for contract risk analysis."""

    truncated = text[-8000:] if len(text) > 8000 else text

    # Key terms table is only for STD and above
    key_terms_instruction = ""
    if tier in ("STD", "PRO", "MAX"):
        key_terms_instruction = '''
    "key_terms": {
      "parties": ["Party A", "Party B", ...],
      "contract_value": "amount if stated, otherwise 'Not specified'",
      "payment_terms": "payment conditions summary",
      "duration": "contract duration/term",
      "termination": "termination conditions",
      "breach_penalties": "breach of contract penalties",
      "dispute_resolution": "dispute resolution clause",
      "governing_law": "applicable law/jurisdiction"
    },
'''
    else:
        key_terms_instruction = '''
    "key_terms": null,  // Key terms table not available in FREE tier
'''

    prompt = f"""# Contract Risk Analysis

## Contract Type: {contract_type}
## Language: {language}

## Contract Text:
{truncated}

---

Please analyze this contract and return a structured JSON report:

{{
  "summary": "200-word-or-less summary of the contract's core content in the contract's language",
  "contract_type": "{contract_type}",
  "language": "{language}",
{key_terms_instruction}
  "risk_report": [
    {{
      "level": "HIGH",    // HIGH / MEDIUM / LOW
      "category": "payment | termination | liability | confidentiality | compliance | other",
      "title": "Risk title (brief, in Chinese or English matching the contract language)",
      "description": "Detailed risk description",
      "clause_reference": "Which clause/section this risk comes from, or 'Not specified'",
      "recommendation": "What the user should do about this risk"
    }}
  ],
  "overall_score": 1-10,   // Risk score: 1=very low risk, 10=very high risk
  "overall_assessment": "Brief overall risk assessment paragraph"
}}

IMPORTANT:
- Be strict and thorough — do not minimize real risks
- HIGH risks involve significant financial loss, legal liability, or irreversible consequences
- MEDIUM risks involve moderate exposure or unclear terms
- LOW risks are minor issues, technical violations, or overly broad clauses
- If no risks found, return empty risk_report array []
- Respond ONLY with valid JSON — no markdown code blocks, no explanation outside the JSON
"""
    return prompt


def call_ai_analysis(prompt: str, model: str = "minimax/MiniMax-M2") -> dict:
    """Call AI via OpenAI-compatible API."""
    import os

    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_API_BASE", "https://api.minimax.chat/v1")

    if not api_key:
        # Fallback: try direct OpenAI
        api_key = os.environ.get("OPENAI_API_KEY_FALLBACK", "")
        base_url = os.environ.get("OPENAI_API_BASE_FALLBACK", "https://api.openai.com/v1")

    if not api_key:
        return {"error": "No API key configured. Set OPENAI_API_KEY or OPENAI_API_KEY_FALLBACK environment variable."}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=4000
        )
        content = response.choices[0].message.content.strip()
        # Strip markdown code blocks if present
        if content.startswith("```"):
            lines = content.splitlines()
            content = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        return json.loads(content)
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}


# ── Report Rendering ──────────────────────────────────────────────────────────

def render_report(analysis: dict, contract_type: str, language: str,
                  word_count: int, used_ocr: bool, tier: str) -> str:
    """Render the analysis result as a formatted markdown report."""

    score = analysis.get("overall_score", "?")
    score_label = "低" if score <= 3 else ("中" if score <= 6 else "高")
    summary = analysis.get("summary", "_未提供摘要_")
    key_terms = analysis.get("key_terms")
    risks = analysis.get("risk_report", [])

    high = [r for r in risks if r.get("level") == "HIGH"]
    med  = [r for r in risks if r.get("level") == "MEDIUM"]
    low  = [r for r in risks if r.get("level") == "LOW"]

    lines = []
    lines.append("## 📄 合同风险审查报告\n")
    lines.append(f"**合同类型：** {contract_type}")
    lines.append(f"**合同语言：** {language}")
    lines.append(f"**整体风险评分：** {score}/10 — {score_label}风险")
    if used_ocr:
        lines.append(f"**文本提取：** OCR（扫描件）")
    else:
        lines.append(f"**文本提取：** 直接提取")
    lines.append("\n---\n")

    # Summary
    lines.append("### 📋 文本摘要\n")
    lines.append(f"{summary}\n")
    lines.append("\n---\n")

    # Key terms table — only for STD+
    if tier in ("STD", "PRO", "MAX") and key_terms:
        lines.append("### 🔑 关键条款\n")
        lines.append("| 条款 | 内容 |")
        lines.append("|------|------|")
        terms_map = [
            ("当事人", "parties", lambda v: ", ".join(v) if isinstance(v, list) else v),
            ("合同金额", "contract_value", lambda v: v),
            ("付款条件", "payment_terms", lambda v: v),
            ("合同期限", "duration", lambda v: v),
            ("解除条款", "termination", lambda v: v),
            ("违约责任", "breach_penalties", lambda v: v),
            ("争议解决", "dispute_resolution", lambda v: v),
            ("适用法律", "governing_law", lambda v: v),
        ]
        for label, key, fmt in terms_map:
            val = key_terms.get(key, "未明确")
            lines.append(f"| {label} | {fmt(val)} |")
        lines.append("\n---\n")
    elif tier in ("STD", "PRO", "MAX"):
        lines.append("### 🔑 关键条款\n")
        lines.append("_未能提取关键条款（合同文本不足）_\n")
        lines.append("\n---\n")

    # Risk list
    lines.append("### ⚠️ 风险点列表\n")

    if high:
        lines.append(f"#### 🔴 高风险 ({len(high)}项)\n")
        for i, r in enumerate(high, 1):
            lines.append(f"{i}. **{r.get('title', '未命名风险')}**")
            lines.append(f"   - 类别：{r.get('category', 'other')}")
            lines.append(f"   - 条款来源：{r.get('clause_reference', '未明确')}")
            lines.append(f"   - 风险描述：{r.get('description', '')}")
            lines.append(f"   - 建议措施：{r.get('recommendation', '')}\n")
    else:
        lines.append("#### 🔴 高风险 (0项) — 未发现高风险点\n\n")

    if med:
        lines.append(f"#### 🟠 中风险 ({len(med)}项)\n")
        for i, r in enumerate(med, 1):
            lines.append(f"{i}. **{r.get('title', '未命名风险')}**")
            lines.append(f"   - 类别：{r.get('category', 'other')}")
            lines.append(f"   - 条款来源：{r.get('clause_reference', '未明确')}")
            lines.append(f"   - 风险描述：{r.get('description', '')}")
            lines.append(f"   - 建议措施：{r.get('recommendation', '')}\n")
    else:
        lines.append("#### 🟠 中风险 (0项)\n\n")

    if low:
        lines.append(f"#### 🟡 低风险 ({len(low)}项)\n")
        for i, r in enumerate(low, 1):
            lines.append(f"{i}. **{r.get('title', '未命名风险')}**")
            lines.append(f"   - 类别：{r.get('category', 'other')}")
            lines.append(f"   - 条款来源：{r.get('clause_reference', '未明确')}")
            lines.append(f"   - 风险描述：{r.get('description', '')}")
            lines.append(f"   - 建议措施：{r.get('recommendation', '')}\n")
    else:
        lines.append("#### 🟡 低风险 (0项)\n\n")

    lines.append("---\n")
    lines.append("⚠️ **免责声明：** 本报告仅供参考，不构成法律建议。如有法律疑问，请咨询专业律师。\n")
    lines.append("\n---\n")
    lines.append("### 📊 统计信息\n")
    lines.append(f"- 合同文本字数：约{word_count}字")
    lines.append(f"- 检测到风险：{len(risks)}项（🔴高{len(high)} / 🟠中{len(med)} / 🟡低{len(low)}）")
    lines.append(f"- 分析时间：2026-04-20")
    if tier != "FREE":
        lines.append(f"- 当前套餐：{tier}")

    return "\n".join(lines)


# ── Excel Export ──────────────────────────────────────────────────────────────

def export_csv(report_path: str, analysis: dict, contract_type: str, language: str):
    """Export risk report as CSV for STD+ tiers."""
    import csv

    csv_path = report_path.replace("_report.md", "_risks.csv")
    risks = analysis.get("risk_report", [])

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["风险等级", "类别", "风险标题", "风险描述", "条款来源", "建议措施", "合同类型", "语言"])
        for r in risks:
            writer.writerow([
                r.get("level", ""),
                r.get("category", ""),
                r.get("title", ""),
                r.get("description", ""),
                r.get("clause_reference", ""),
                r.get("recommendation", ""),
                contract_type,
                language
            ])
    return csv_path


# ── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Contract Risk Reviewer")
    parser.add_argument("--pdf", required=True, help="Path to the contract PDF file")
    parser.add_argument("--tier", default="FREE", choices=["FREE", "STD", "PRO", "MAX"],
                        help="Subscription tier (default: FREE)")
    parser.add_argument("--api-key", default="", 
                        help="91Skillhub API key for automatic tier verification")
    parser.add_argument("--model", default="minimax/MiniMax-M2",
                        help="AI model to use")
    parser.add_argument("--output", default=None,
                        help="Output report path (default: /tmp/contracts/<uuid>_report.md)")
    parser.add_argument("--export-csv", action="store_true",
                        help="Also export CSV (STD+ tier)")
    args = parser.parse_args()

    pdf_path = args.pdf
    # Verify token if api_key provided; degrade to FREE on failure
    if args.api_key:
        verify_result = verify_token(args.api_key)
        if verify_result["valid"]:
            tier = verify_result["tier"]
        else:
            tier = "FREE"
        print(f"[INFO] Token verified: valid={verify_result['valid']}, tier={tier}", file=sys.stderr)
    else:
        tier = args.tier

    # Ensure temp dir exists
    os.makedirs("/tmp/contracts", exist_ok=True)

    # Determine output path
    if args.output:
        report_path = args.output
    else:
        file_uuid = str(uuid.uuid4())[:8]
        report_path = f"/tmp/contracts/{file_uuid}_report.md"

    print(f"[INFO] Processing: {pdf_path}", file=sys.stderr)
    print(f"[INFO] Tier: {tier}", file=sys.stderr)

    # Step 1: Extract text
    print("[INFO] Extracting text from PDF...", file=sys.stderr)
    text, used_ocr = extract_pdf_text(pdf_path)
    word_count = len(text)
    print(f"[INFO] Extracted {word_count} characters (OCR used: {used_ocr})", file=sys.stderr)

    if word_count < 50:
        print("[ERROR] Could not extract sufficient text from PDF.", file=sys.stderr)
        print("[HINT] The PDF may be a scanned image. Please provide a text-based PDF or contact support.", file=sys.stderr)
        print(json.dumps({"error": "text_extraction_failed", "characters_extracted": word_count}))
        sys.exit(1)

    # Step 2: Detect type and language
    contract_type, language = detect_contract_type_and_lang(text)
    print(f"[INFO] Detected: type={contract_type}, language={language}", file=sys.stderr)

    # Step 3: Build prompt and call AI
    print("[INFO] Calling AI for risk analysis...", file=sys.stderr)
    prompt = build_analysis_prompt(text, contract_type, language, tier)
    analysis = call_ai_analysis(prompt, args.model)

    if "error" in analysis:
        print(json.dumps(analysis))
        sys.exit(1)

    # Step 4: Render report
    report_md = render_report(analysis, contract_type, language, word_count, used_ocr, tier)

    # Save report
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[INFO] Report saved to: {report_path}", file=sys.stderr)

    # Step 5: Export CSV if requested (STD+)
    csv_path = None
    if args.export_csv and tier in ("STD", "PRO", "MAX"):
        csv_path = export_csv(report_path, analysis, contract_type, language)
        print(f"[INFO] CSV exported to: {csv_path}", file=sys.stderr)

    # Output JSON summary to stdout for programmatic use
    result = {
        "status": "success",
        "report_path": report_path,
        "csv_path": csv_path,
        "contract_type": contract_type,
        "language": language,
        "word_count": word_count,
        "used_ocr": used_ocr,
        "overall_score": analysis.get("overall_score"),
        "risk_count": {
            "total": len(analysis.get("risk_report", [])),
            "high": len([r for r in analysis.get("risk_report", []) if r.get("level") == "HIGH"]),
            "medium": len([r for r in analysis.get("risk_report", []) if r.get("level") == "MEDIUM"]),
            "low": len([r for r in analysis.get("risk_report", []) if r.get("level") == "LOW"]),
        },
        "tier": tier,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
