# Contract Risk Reviewer · 合同风险智能审查

**Trigger Keywords / 触发词：** 合同审查、合同风险、合同分析、合同检查、合同审核、contract review、contract risk

**When to use / 何时使用：**
- User uploads a contract PDF and wants AI-powered risk analysis
- User asks to review/audit/check a contract for risks
- User provides a contract and asks for a structured risk report
- User mentions "合同审查"、"合同风险"、"合同分析"

---

## What this skill does

上传合同 PDF → AI 分析 → 输出结构化风险报告（文本摘要 + 关键条款表格 + 风险点列表）

---

## Workflow

### Step 1 — Receive Contract File

The user uploads a PDF file. Download it to `/tmp/contracts/` using the appropriate tool:

- If the file comes as a Feishu message attachment → use `feishu_im_bot_image` or `feishu_im_user_fetch_resource` with `type=file`
- If the file is a local path → copy or note the path directly
- If the file is a URL → use `web_crawl` or fetch

Store the file in `/tmp/contracts/<uuid>.pdf`.

### Step 2 — Extract Text from PDF

Try in order:

1. **PyMuPDF (fitz)** — best for text-based PDFs:
   ```python
   import fitz
   doc = fitz.open(pdf_path)
   text = "\n".join(page.get_text() for page in doc)
   ```

2. **pdfplumber** — good for tables:
   ```python
   import pdfplumber
   with pdfplumber.open(pdf_path) as pdf:
       text = "\n".join(page.extract_text() or "" for page in pdf.pages)
   ```

3. **OCR (pytesseract)** — for scanned/image PDFs:
   - Convert PDF pages to images with `pdf2image` or `PyMuPDF` render
   - Run pytesseract with language packs (chi_sim + eng)
   - Fallback to Chinese + English bilingual OCR

If text extraction fails completely or yields < 50 characters, inform the user that the PDF may be a scanned image requiring OCR, and offer to process with OCR.

### Step 3 — Auto-Detect Contract Type

Use the AI model to classify the contract type from extracted text:

- 劳动合同 (Labor/Employment Contract)
- 采购合同 (Purchase/Procurement Contract)
- 销售合同 (Sales Contract)
- 租赁合同 (Lease/Rental Contract)
- 保密协议 (NDA/Confidentiality Agreement)
- 其他 (Other)

Also detect language: 中文 / English / Bilingual.

### Step 4 — AI Risk Analysis

Build a structured prompt for the AI model. Use `model` parameter from user's session or default to `minimax/MiniMax-M2`.

**Prompt Structure:**

```
# Contract Risk Analysis

## Contract Type: [detected type]
## Language: [Chinese / English / Bilingual]

## Contract Text:
[extracted text, truncated to last 8000 characters if too long]

---

Please analyze this contract and return a structured JSON report:

{
  "summary": "200-word-or-less summary of the contract's core content",
  "contract_type": "detected contract type",
  "language": "detected language",
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
  "risk_report": [
    {
      "level": "HIGH",    // HIGH / MEDIUM / LOW
      "category": "payment/termination/liability/confidentiality/other",
      "title": "Risk title",
      "description": "Detailed risk description",
      "clause_reference": "Which clause/section this risk comes from",
      "recommendation": "What the user should do about this risk"
    }
  ],
  "overall_score": 1-10,   // Risk score: 1=very low risk, 10=very high risk
  "overall_assessment": "Brief overall risk assessment paragraph"
}

IMPORTANT:
- Be strict and thorough — do not minimize real risks
- Classify risks as HIGH only if they involve significant financial loss, legal liability, or irreversible consequences
- If no risks found, return empty risk_report array
- This is NOT legal advice — include a disclaimer in the response to the user
```

### Step 5 — Format and Deliver Results

Render the results as a well-formatted markdown report:

```
## 📄 合同风险审查报告

**合同类型：** [类型]
**语言：** [语言]
**整体风险评分：** [X/10] — [低/中/高]

---

### 📋 文本摘要

[200字以内摘要]

---

### 🔑 关键条款

| 条款 | 内容 |
|------|------|
| 当事人 | ... |
| 合同金额 | ... |
| 付款条件 | ... |
| 合同期限 | ... |
| 违约责任 | ... |
| 解除条款 | ... |
| 争议解决 | ... |
| 适用法律 | ... |

---

### ⚠️ 风险点列表

#### 🔴 高风险 (X项)

1. **[风险标题]**
   - 条款来源：第X条
   - 风险描述：...
   - 建议措施：...

#### 🟠 中风险 (X项)

...

#### 🟡 低风险 (X项)

...

---

⚠️ **免责声明：** 本报告仅供参考，不构成法律建议。如有法律疑问，请咨询专业律师。

---

📊 **统计数据**
- 文本字数：X字
- 检测到风险：X项（高X / 中X / 低X）
- 合同语言：中文/英文
- 分析时间：YYYY-MM-DD HH:mm
```

### Step 6 — Save & Export

- Save the full report as `/tmp/contracts/<uuid>_report.md`
- If user requests Excel export (STD plan or above), generate a simple CSV/Excel format
- Send the report to the user via the current channel (Feishu message or direct display)

---

## Tiered Features

| Feature | FREE | STD (¥9.9) | PRO (¥29) | MAX (¥69) |
|---------|------|-----------|-----------|-----------|
| Monthly limit | 3 contracts | 30 contracts | 200 contracts | Unlimited |
| Contract types | Other only | All 6 types | All 6 types | All 6 types |
| Summary + Risk list | ✅ | ✅ | ✅ | ✅ |
| Key terms table | ❌ | ✅ | ✅ | ✅ |
| Excel report export | ❌ | ✅ | ✅ | ✅ |
| Batch processing | ❌ | ❌ | ✅ | ✅ |
| Risk comparison | ❌ | ❌ | ✅ | ✅ |
| API priority | ❌ | ❌ | ❌ | ✅ |

For FREE tier: skip the key terms table, only deliver summary + risk list.

---

## Token Validation

Check the user's token prefix in their session context or configuration:

- Token starting with `CONTRACT-MAX` → full access
- `CONTRACT-PRO` → PRO features
- `CONTRACT-STD` → STD features
- `CONTRACT-FREE` or none → FREE tier

If monthly limit is exceeded, inform the user and suggest upgrading.

---

## Error Handling

| Error | Handling |
|-------|----------|
| PDF extraction yields < 50 chars | Offer OCR processing; if OCR also fails, report failure and suggest providing a text-based PDF |
| AI analysis fails | Return error message; suggest retrying |
| Unsupported file type | Inform user only PDF is supported |
| Token validation missing | Default to FREE tier |

---

## File Requirements

- All uploaded PDFs stored in `/tmp/contracts/` (auto-cleanup optional)
- Reports saved in same directory with `_report.md` suffix
- Do NOT store contract text long-term; clean up after report is delivered

---

## Tech Stack

- **PDF Text:** `PyMuPDF` (fitz) + `pdfplumber`
- **OCR:** `pytesseract` + `pdf2image` (with `chi_sim+eng` language packs)
- **AI Analysis:** OpenAI-compatible API via `openai` Python package
- **Report Export:** `csv` module for Excel CSV format

---

## Skill Metadata

- **Slug:** `contract-risk-reviewer`
- **Name:** 合同风险智能审查 (Contract Risk Reviewer)
- **Platform:** ClawHub (clawhub.ai) + 腾讯Skillhub
- **Entry:** `scripts/analyze_contract.py`
- **Dependencies:** `fitz`, `pdfplumber`, `pytesseract`, `pdf2image`, `openai`

> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
