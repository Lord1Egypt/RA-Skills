---
name: Audit Creator Tax Compliance & Generate Compliance Reports
description: "Audit income sources, expenses, and licensing agreements to identify tax deductions and compliance requirements. Use when the user needs quarterly tax reports, multi-country compliance flags, or equipment deduction strategies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SHEETS_API_KEY"],"bins":["jq","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📋"}}
---

## Overview

**Creator Tax & Compliance Auditor** analyzes your entire financial ecosystem to surface tax deductions you're missing and flag compliance risks before they become problems. Built specifically for content creators, software developers, digital entrepreneurs, and independent professionals earning across multiple jurisdictions.

This skill integrates with your financial tools (Google Sheets, Stripe, PayPal), content platforms (YouTube, Patreon, Substack), and accounting systems to automatically categorize income sources and expenses. It then generates actionable quarterly compliance reports that identify:

- **Tax deduction opportunities**: Software subscriptions, equipment depreciation, home office allocation, travel for content creation, professional development
- **Multi-country compliance risks**: VAT/GST requirements, withholding tax obligations, licensing restrictions by audience jurisdiction
- **Documentation gaps**: Missing receipts, incomplete expense logs, untracked licensing agreements
- **Quarterly filing deadlines**: Jurisdiction-specific estimated tax payments and reporting requirements

Integrates with: Google Sheets, Stripe, PayPal, Wave Accounting, WordPress, Notion, Slack (for alerts), GitHub (for developer expense tracking).

---

## Quick Start

Try these prompts immediately to see the skill in action:

```
Audit my income sources for Q4 2024. I earn from YouTube ads, Patreon subscribers, 
and freelance software development. Flag which income streams have multi-country 
tax implications and what documentation I need for IRS compliance.
```

```
Generate a tax deduction checklist for a software creator. I spend on Adobe Creative 
Suite ($600/year), AWS hosting ($150/month), home office (30% of $2000 rent), 
conference travel ($8000/year), and laptop upgrades ($2500). What can I legally 
deduct and what needs separate documentation?
```

```
Analyze my licensing risks. I create educational content on YouTube and Teachable, 
with audience in US (60%), UK (20%), Canada (15%), and Australia (5%). What 
licensing agreements, copyright notices, and data privacy requirements must I 
implement per jurisdiction? Flag any compliance gaps.
```

```
Generate my Q3 2024 creator compliance report. Here's my expense log [CSV paste]. 
Calculate estimated tax liability by jurisdiction, list deductions I've claimed, 
identify missing receipts, and give me a 30-day action plan to prepare for 
quarterly tax payment.
```

---

## Capabilities

### 1. Income Source Audit
**Automatically categorize and analyze all income streams:**

- Distinguishes between W-2 employment, 1099 contractor income, platform revenue sharing, and passive income
- Flags income sources subject to backup withholding (third-party payment processors)
- Calculates effective tax rate by source and identifies high-risk income streams
- Cross-references income sources against multi-country tax treaties
- Alerts on income thresholds triggering additional reporting requirements (e.g., $600 PayPal threshold for 1099-K)

**Usage Example:**
```
"I earn $5K/month from YouTube AdSense, $8K/month from Patreon (with international subscribers), 
and $12K/month from freelance Upwork contracts. Break down my tax obligations by source and 
tell me which income is subject to self-employment tax."
```

### 2. Expense Categorization & Deduction Maximization
**Smart expense analysis with deduction strategy:**

- Categorizes expenses using IRS Schedule C classifications (home office, supplies, equipment, professional services, travel)
- Flags equipment eligible for Section 179 expensing vs. depreciation schedules
- Calculates home office deduction using both simplified ($5/sq ft up to $300) and actual expense methods
- Identifies bundled expenses (e.g., software with personal use component) and proper allocation percentages
- Tracks meal, entertainment, and travel expenses with IRS substantiation requirements
- Warns about red-flag deductions that trigger audit patterns

**Usage Example:**
```
"I bought a $3000 laptop (50% business use), spent $2400 on Adobe Creative Suite, 
rented co-working space ($400/month), attended 3 conferences ($6000 total), and drove 
8000 business miles. What's my maximum legal deduction? What documentation do I need?"
```

### 3. Multi-Country Compliance Scanner
**Jurisdiction-specific requirements at a glance:**

- Maps audience geography against VAT/GST thresholds and registration requirements
- Identifies withholding tax obligations on international payments (W-8BEN forms, treaty requirements)
- Flags data privacy compliance needs (GDPR for EU audience, CCPA for California, LGPD for Brazil)
- Checks licensing and content rights restrictions by country
- Lists currency reporting requirements and FBAR filing thresholds
- Alerts on platform-specific compliance (e.g., YouTube monetization requirements, Patreon payment processor rules)

**Usage Example:**
```
"My Patreon has 200 supporters: 120 US, 40 UK, 25 Canada, 15 Australia. What tax forms 
do I need? Am I subject to VAT? What data privacy agreements must I have? Flag any 
licensing restrictions I should know about."
```

### 4. Quarterly Compliance Reporting
**Automated report generation with actionable next steps:**

- Calculates estimated tax liability and compares against previous quarter
- Generates filing deadline calendar (federal, state, local, and international)
- Lists missing documentation and receipt backup requirements
- Provides quarter-over-quarter income/expense trends with variance analysis
- Creates priority action items (e.g., "File 1040-ES by Jan 16", "Renew business license by March 31")
- Includes IRS risk assessment and audit probability flags

**Output includes:**
- Estimated tax payment amounts by jurisdiction
- Deduction summary with itemization
- Compliance checklist (passed/failed/action-required items)
- Documentation gaps with remediation steps
- 30/60/90-day action plan

### 5. Licensing & Agreement Risk Assessment
**Proactive identification of compliance gaps:**

- Analyzes content licensing agreements (YouTube Partner Program, Patreon, Substack, Stripe)
- Checks terms of service compliance for monetization and audience restrictions
- Identifies copyright/trademark risks (music licensing, image rights, trademark usage)
- Maps affiliate disclosures and FTC compliance (required for sponsored content)
- Validates age-gated content requirements and audience jurisdiction restrictions
- Flags cookie consent and analytics compliance (GDPR/CCPA)

---

## Configuration

### Environment Variables (Required)

```bash
# OpenAI API for expense categorization and report generation
export OPENAI_API_KEY="sk-..."

# Google Sheets for reading expense logs and income tracking
export GOOGLE_SHEETS_API_KEY="..."
export GOOGLE_SHEETS_ID="your-sheet-id"

# Optional: Direct accounting integrations
export STRIPE_API_KEY="sk_live_..."
export PAYPAL_CLIENT_ID="..."
export WAVE_ACCESS_TOKEN="..."
```

### Setup Instructions

1. **Create a Google Sheet** with these columns:
   - Date, Category (Income/Expense), Amount, Source/Vendor, Description, Tax Year, Jurisdiction

2. **Grant permissions** via Google Cloud Console for Sheets API access

3. **Provide historical data** (current year + previous 2 years for trend analysis)

4. **Configure jurisdiction list** (where you earn income or have audience):
   ```json
   {
     "jurisdictions": ["US", "UK", "CA", "AU"],
     "business_structure": "Sole Proprietor",
     "tax_year": 2024,
     "fiscal_year_end": "12/31"
   }
   ```

5. **Optional integrations**:
   - Connect Stripe/PayPal for automatic income import
   - Link Patreon/YouTube analytics for audience geographic breakdown
   - Sync Wave Accounting or QuickBooks for real-time expense data

---

## Example Outputs

### Quarterly Compliance Report (Excerpt)

```
═══════════════════════════════════════════════════════════════════
CREATOR TAX & COMPLIANCE REPORT — Q4 2024
═══════════════════════════════════════════════════════════════════

📊 INCOME SUMMARY
─────────────────────────────────────────────────────────────────
YouTube AdSense:              $18,240  (US only)
Patreon (global):             $32,000  (40% international)
Freelance/1099 (Upwork):       $48,000  (US + UK clients)
─────────────────────────────────────────────────────────────────
Total Gross Income:           $98,240

🚨 MULTI-COUNTRY TAX OBLIGATIONS
─────────────────────────────────────────────────────────────────
US (Self-Employment Tax):     $13,886 (15.3% on $90,600)
UK (Self-Assessment Income):   $4,800 (estimated, ~20% on £3800)
Canada (Provincial Tax):       $1,200 (estimated on CA resident subscribers)
Australia (Withholding):       $960 (30% on AU income over threshold)
─────────────────────────────────────────────────────────────────
Total Estimated Tax Liability: $20,846

💰 DEDUCTION ANALYSIS
─────────────────────────────────────────────────────────────────
Software Subscriptions:       $7,200  ✓ Fully deductible
Home Office (30%):            $7,200  ✓ IRS-approved (actual expense method)
Equipment (Section 179):      $3,500  ✓ Full first-year deduction
Conference Travel:            $8,000  ✓ Deductible (50% meals)
Internet/Utilities (30%):     $2,400  ✓ Home office allocation
Professional Development:     $1,200  ✓ Courses, books, certifications
─────────────────────────────────────────────────────────────────
Total Deductions:            $29,500
Taxable Income:              $68,740

⚠️ COMPLIANCE FLAGS
─────────────────────────────────────────────────────────────────
🔴 MISSING DOCUMENTATION: No receipts found for $2,340 in meals/entertainment
🟡 ACTION REQUIRED: File W-8BEN with PayPal for UK income (prevents 30% backup withholding)
🟡 ACTION REQUIRED: Add GDPR privacy notice to website (40% EU audience on Patreon)
✓ PASS: YouTube monetization compliant with content requirements
✓ PASS: Affiliate disclosures present on all sponsored content

📅 DEADLINE CALENDAR
─────────────────────────────────────────────────────────────────
Jan 15, 2025: File 1040-ES (Q1 estimated tax) — US Federal
Jan 31, 2025: File 1099-K from Stripe (if >$20K) — US Reporting
Feb 15, 2025: Submit Self-Assessment — UK Tax Authority
Mar 15, 2025: File 1040 (if eligible) — US Federal

🎯 30-DAY ACTION PLAN
─────────────────────────────────────────────────────────────────
Week 1: Gather missing meal/entertainment receipts; file W-8BEN with PayPal
Week 2: Update website privacy policy with GDPR language; add cookie consent
Week 3: Calculate Q1 estimated tax; file 1040-ES by Jan 15
Week 4: Prepare 2024 tax return documentation; schedule tax prep review
```

### Deduction Opportunity Summary

```
TOP DEDUCTION OPPORTUNITIES YOU'RE MISSING:
─────────────────────────────────────────────────────────────────
1. Equipment Upgrade Cycle: $5,200 in camera/laptop purchases can be 
   Section 179 expensed (full deduction year 1) instead of depreciated 
   over 5 years. Potential tax savings: $1,560 (assuming 30% tax bracket).

2. Home Office Expansion: Currently claiming 200 sq ft at $5/sq ft 
   simplified rate ($1,000). If you measure actual office space at 400 
   sq ft (30% of 1,300 sq ft home), you can claim $7,200 using actual 
   expense method (30% of $24,000 annual rent/utilities/insurance). 
   Potential tax savings: $1,860.

3. Vehicle Mileage: You claimed 3,200 business miles. If your business 
   use is 40% (estimated from calendar review), you should claim 8,000 
   miles @ $0.67/mile = $5,360 deduction (vs. $2,144 currently claimed). 
   Additional tax savings: $950.
```

---

## Tips & Best Practices

### Income Tracking
- **Automate integrations**: Connect Stripe, PayPal, Patreon APIs to avoid manual data entry and reduce categorization errors
- **Weekly reconciliation**: Spend 15 minutes every Sunday reviewing new income/expenses to catch errors early
- **Separate business accounts**: Use dedicated bank/PayPal accounts for business income to simplify audit trails

### Expense Documentation
- **"Shoebox to spreadsheet" strategy**: Photograph all receipts, tag with date/category, store in Google Photos with automatic upload to expense sheet
- **Mileage tracking**: Use automatic tracking apps (Stride Health, MileIQ) rather than manual logs—IRS prefers contemporaneous records
- **Invoicing discipline**: Always get written invoices for contractor expenses; email confirmations count but receipts are stronger

### Multi-Country Compliance
- **Audience analytics review**: Monthly breakdown by country (YouTube Analytics, Patreon Dashboard) informs tax exposure
- **Tax treaty research**: US has treaties with 60+ countries that may reduce withholding rates (vs. 30% default)
- **Quarterly currency conversion tracking**: If earning in GBP/CAD/AUD, document exchange rates on transaction dates for FBAR reporting

### Red Flags to Avoid
- **Home office deduction percentage mismatch**: IRS flags claims >50% unless your entire home is business-dedicated
- **Meal/entertainment without business purpose documentation**: "Client dinner" alone isn't enough—write names, dates, business discussed
- **Hobby loss scrutiny**: Revenue under $50K with multi-year losses may be challenged as hobby vs. business activity

### Tax Form Mastery
- **Schedule C filers**: Self-employment income reported here; keep Part II (expenses) organized by category
- **1099-K threshold**: PayPal/Stripe issue 1099-K if you gross >$20K in credit card payments; this is reported to IRS automatically
- **W-8BEN requirement**: File with international payment processors to prevent 30% backup withholding on non-US earnings

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Not a substitute for professional tax counsel**: This skill provides analytical recommendations only. Tax laws vary by individual circumstances, business structure, and jurisdiction. Always consult a CPA or tax attorney before filing.

❌ **Cannot file tax returns**: This skill generates reports and guidance; you or your tax professional must file Form 1040, Schedule C, state returns, and international forms.

❌ **Does not provide legal advice on licensing**: Content licensing and copyright risks are complex and jurisdiction-specific. We flag potential issues but recommend consulting an IP attorney.

❌ **Limited to financial data you provide**: Analysis is only as accurate as your input data. If expense categorization is missing or incorrect, deduction calculations will be unreliable.

❌ **Does not monitor ongoing compliance**: This is a point-in-time audit. You must repeat quarterly to catch new compliance risks.

### Important Limitations

- **Exchange rate volatility**: Multi-currency reporting uses rates on transaction dates, but foreign tax authority requirements may differ
- **Audit probability scores**: These are statistical estimates based on IRS audit patterns, not predictions of your specific risk
- **Jurisdictional rules change**: Tax laws update annually (sometimes mid-year). This skill reflects 2024/2025 rules; verify current requirements before filing
- **Business structure assumptions**: Calculations assume sole proprietor status. S-Corp, LLC, or C-Corp filers need custom analysis

### Compliance Statement

By using this skill, you acknowledge:
1. You will independently verify all recommendations with a tax professional
2. You