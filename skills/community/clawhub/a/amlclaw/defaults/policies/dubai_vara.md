# Dubai VARA — AML/CFT Compliance Policy for Virtual Asset Service Providers

## 1. Jurisdiction & Regulatory Framework

This policy applies to Virtual Asset Service Providers (VASPs) licensed by the Dubai Virtual Assets Regulatory Authority (VARA) under the Dubai Virtual Assets Regulation Law.

**Applicable regulations:**
- **VARA Compliance and Risk Management Rules** — Virtual Asset regulatory framework (Rulebook Sections 3, 4)
- **UAE Federal Decree-Law No. 20 of 2018** — Anti-Money Laundering and Combating the Financing of Terrorism
- **UAE Cabinet Decision No. 10 of 2019** — Implementing regulations for Federal AML Law
- **UAE Executive Office of Anti-Money Laundering and Counter Terrorism Financing (EOCN)** — National coordination
- **FATF 40 Recommendations** (2023 update) — International AML/CFT standards
- **FATF VA/VASP Guidance** (2021) — Virtual asset-specific guidance
- **FATF Recommendation 16** — Travel Rule for wire transfers / VA transfers
- **OFAC SDN List** — US Office of Foreign Assets Control Specially Designated Nationals
- **UN Consolidated Sanctions List** — United Nations Security Council sanctions
- **UAE Local Sanctions List** — Domestic designations under Federal AML Law

## 2. Customer Due Diligence (CDD)

### 2.1 Standard CDD (VARA Rulebook Section 3.1, UAE Federal AML Law)
- Verify identity of all customers before establishing a business relationship using reliable, independent sources
- Identify Ultimate Beneficial Owners (UBOs) with >25% ownership or control
- Assess purpose and intended nature of virtual asset activities
- Continuous due diligence with risk-based approach
- **Transaction threshold**: Full KYC/CDD required for single transactions > AED 3,500 (~USD 950) per rule `UAE-VARA-CDD-HIGH-001`

### 2.2 Enhanced Due Diligence (EDD) (VARA Rulebook Section 3.1)
EDD is required when:
- Customer from high-risk jurisdiction per FATF or UAE National Risk Assessment
- Transaction involves PEPs, their family members, or close associates
- Transactions above AED 55,000 (~USD 15,000) without clear economic rationale
- Complex or unusual transaction patterns
- Blockchain analytics reveal Sanctions/Terrorism exposure at Hop 4-5 — per rule `UAE-VARA-DEP-HIGH-001`
- Any exposure (>0%) to Obfuscation (Mixers, Privacy Tokens) — per rule `UAE-VARA-DEP-HIGH-002` (zero-tolerance, VARA prohibition)
- Cybercrime/Gambling/High-Risk exposure >10% AND >USD 100 — per rule `UAE-VARA-DEP-HIGH-003`
- Target address self-tagged as Cybercrime or Obfuscation — per rules `UAE-VARA-DEP-SELF-HIGH-001`, `UAE-VARA-WDR-SELF-HIGH-001`

EDD procedures include:
- MLRO approval for relationship continuation
- Additional source of funds / source of wealth documentation
- Increased frequency and depth of transaction monitoring
- Detailed rationale documentation for proceeding

## 3. Blockchain-Specific Risk Indicators

Risk categories based on TrustIn KYA label taxonomy, calibrated for VARA requirements:

| Risk Tier | Primary Categories | VARA-Specific Notes |
|-----------|-------------------|-------------------|
| **Severe** | Sanctions, Terrorism Financing, Public Freezing Action, Illicit Markets, Other Financial Crimes | Zero tolerance. Immediate freeze and FIU report. |
| **High** | Obfuscation | **VARA explicitly prohibits anonymity-enhanced crypto** — any exposure (>0%) triggers Reject (`UAE-VARA-DEP-HIGH-002`) |
| **High** | Cybercrime, Gambling, High-Risk Entities | Threshold-based: >10% exposure AND >USD 100 |
| **Medium** | Other Entities (select) | Black/Grey Industry, MEV Bots/Arbitrage, Spam |
| **Low / Whitelist** | Exchanges & DeFi, Other Entities | CEX, TradFi — whitelist stop rule (`UAE-VARA-WHL-001`) |

**Key VARA distinction**: Dubai applies **zero-tolerance for Obfuscation** (Mixers, Privacy Wallets, Privacy Tokens). VARA explicitly prohibits anonymity-enhanced crypto assets. Any exposure >0% triggers deposit rejection. Additionally, VARA has a **lower CDD threshold** (AED 3,500 / ~USD 950) compared to Singapore and Hong Kong.

## 4. Screening Procedures by Scenario

### 4.1 Deposit Screening
**Inflow analysis** (where did the funds come from?):
- **Hop 1 (direct)**: Sanctions/Terrorism/Illicit → **Freeze** (`UAE-VARA-DEP-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism/Illicit → **Freeze** (`UAE-VARA-DEP-SEVERE-002`)
- **Hop 4-5 (far)**: Sanctions/Terrorism/Illicit → **EDD** (`UAE-VARA-DEP-HIGH-001`)
- **Zero-tolerance**: Any Obfuscation exposure >0% → **Reject** (`UAE-VARA-DEP-HIGH-002`)
- **Threshold**: Cybercrime/Gambling/High-Risk >10% AND >USD 100 → **EDD** (`UAE-VARA-DEP-HIGH-003`)

**Outflow history** (where has this address previously sent funds?):
- **Hop 1 (direct)**: Funded Sanctions/Terrorism → **Freeze** (`UAE-VARA-DEP-OUT-SEVERE-001`)
- **Hop 2-3 (indirect)**: Funded Sanctions/Terrorism → **EDD** (`UAE-VARA-DEP-OUT-HIGH-001`)

**Self-tag** (is the address itself flagged?):
- Sanctions/Terrorism/Illicit tag → **Freeze** (`UAE-VARA-DEP-SELF-SEVERE-001`)
- Cybercrime/Obfuscation tag → **EDD** (`UAE-VARA-DEP-SELF-HIGH-001`)

### 4.2 Withdrawal Screening
**Outflow analysis** (where are the funds going?):
- **Hop 1 (direct)**: Sanctions/Terrorism destination → **Freeze** (`UAE-VARA-WDR-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism destination → **Freeze** (`UAE-VARA-WDR-SEVERE-002`)
- **Hop 4-5 (far)**: Sanctions/Terrorism destination → **EDD** (`UAE-VARA-WDR-HIGH-001`)
- **Threshold**: Cybercrime/Obfuscation/Gambling >10% AND >USD 100 → **EDD** (`UAE-VARA-WDR-HIGH-002`)

**Self-tag gate** (is the withdrawing address flagged?):
- Sanctions/Terrorism/Illicit → **Freeze** (`UAE-VARA-WDR-SELF-SEVERE-001`)
- Cybercrime/Obfuscation → **EDD** (`UAE-VARA-WDR-SELF-HIGH-001`)

### 4.3 Onboarding Screening
- Run deposit self-tag and inflow checks against submitted customer addresses
- Severe → reject onboarding, file SAR with FIU
- High → proceed only with EDD and MLRO approval
- Low/Medium → approve with standard monitoring

## 5. Risk Rating Matrix

| Risk Level | Action | Operational Response |
|------------|--------|---------------------|
| **Severe** | Freeze | Immediate asset freeze. Escalate to MLRO. File SAR with UAE FIU within 30 calendar days. No tipping off. |
| **High** | EDD / Reject | Enhanced due diligence or reject (for prohibited categories). Compliance Officer review within 48 hours. |
| **Medium** | Review / Flag | Compliance analyst review within 24 hours. Document rationale. Increase monitoring frequency. |
| **Low** | Allow | Standard processing. Routine monitoring. |

## 6. Suspicious Activity Reporting (SAR)

- **Reporting authority**: UAE Financial Intelligence Unit (FIU)
- **Filing method**: Via **goAML** electronic portal
- **Filing deadline**: Within **30 calendar days** of forming suspicion (UAE Federal AML Law)
- **Tipping off prohibition**: Criminal offence — strictly prohibited to disclose SAR filing to the subject
- **Threshold**: Any transaction where there is reasonable ground to suspect ML/TF, regardless of amount
- **Record keeping**: Maintain copies of all SARs and supporting documentation for minimum 5 years (8 years for high-risk)
- **VARA notification**: Material compliance breaches must be reported to VARA within 5 business days

## 7. Record Keeping Requirements

Per UAE Federal AML Law and VARA Rulebook:
- **CDD records**: Minimum **5 years** after termination of business relationship (**8 years** for high-risk customers)
- **Transaction records**: Minimum **5 years** from date of transaction
- **Screening reports**: Retain all graph data, risk paths, and screening decisions for 5 years
- **SAR records**: Maintain filing records and supporting evidence for 5 years (8 years for high-risk)
- **Ruleset versioning**: Archive all rule configuration changes with timestamps for audit trail
- **VARA compliance records**: Quarterly metrics submissions retained for 5 years

## 8. Travel Rule Compliance (FATF Recommendation 16, UAE Federal AML Law)

Per rule `UAE-VARA-TX-001`:
- **Threshold**: VA transfers > AED 3,500 (~USD 950) trigger Travel Rule and mandatory CDD
- **Required originator information**: Name, account number (wallet address), Emirates ID / passport number, physical address
- **Required beneficiary information**: Name, account number (wallet address)
- **Counterparty VASP verification**: Verify receiving institution is VARA-licensed or equivalent foreign-regulated
- **Cross-border transfers**: Additional originator/beneficiary information required for all cross-border VA transfers above threshold
- **Unhosted wallet transfers**: Require proof of ownership and enhanced CDD

## 9. Sanctions Screening Requirements

### 9.1 Lists to Screen Against
- **OFAC SDN List** — Specially Designated Nationals and Blocked Persons
- **UN Consolidated Sanctions List** — UN Security Council consolidated list
- **FATF High-Risk Jurisdictions** — Countries under increased monitoring or call for action
- **UAE Local Sanctions List** — Domestic designations under Federal AML Law and EOCN directives
- **UAE Targeted Financial Sanctions (TFS)** — Terrorism and proliferation financing designations
- **Arab League sanctions** — Regional sanctions where applicable

### 9.2 Screening Procedures
- Screen all customers and counterparties at onboarding and ongoing
- Re-screen full portfolio within **24 hours** of any sanctions list update (OFAC, UN, UAE local)
- Blockchain address screening via TrustIn KYA API for entity-level sanctions tags
- Name screening with fuzzy matching (minimum 85% match threshold)
- UAE-specific: Screen against EOCN domestic terrorist designation lists

## 10. Ongoing Monitoring

### 10.1 Transaction Monitoring
- **Real-time**: All deposits and withdrawals screened before settlement
- **Structuring detection**: Daily cumulative alerts > USD 950 to prevent AED 3,500 threshold evasion (`UAE-VARA-TX-002`)
- **Periodic re-screening**: Semi-annual full portfolio re-screening for all customers
- **Event-driven**: Immediate re-screening on sanctions list updates or risk escalation
- **VARA reporting**: Quarterly compliance metrics submission

### 10.2 Risk Re-Assessment
- Semi-annual portfolio re-screening for all customers
- Quarterly for high-risk customers
- Addresses may acquire new risk labels over time — ongoing CDD must account for evolving threat intelligence
- Update CDD records when material changes are identified

## 11. Escalation Procedures

1. **Automated flag** → Compliance analyst review within **24 hours**
2. **EDD trigger** → Compliance Officer review within **48 hours**
3. **Freeze trigger** → Immediate MLRO escalation, asset freeze enforced, SAR filed via goAML within 30 calendar days
4. **VARA notification** → Report material compliance breaches to VARA within **5 business days**
5. **Annual review** → Board-level AML/CFT effectiveness review
6. **Regulatory audit** → Maintain readiness for VARA on-site inspections

## 12. Rule-to-Regulation Traceability

| Rule ID | Regulation Reference |
|---------|---------------------|
| UAE-VARA-DEP-SEVERE-001 | UAE Federal AML Law & VARA Rulebook Section 3.1 & OFAC SDN |
| UAE-VARA-DEP-SEVERE-002 | UAE EOCN & VARA Compliance Guidelines 2.1 |
| UAE-VARA-DEP-HIGH-001 | UAE EOCN & Pollution Decay Principle |
| UAE-VARA-DEP-HIGH-002 | VARA Prohibited Activities (Anonymity-Enhanced Crypto) |
| UAE-VARA-DEP-HIGH-003 | TrustIn UAE VARA Guide 2.3 |
| UAE-VARA-DEP-OUT-SEVERE-001 | UAE Federal AML Law & OFAC Indirect Benefits Prohibition |
| UAE-VARA-DEP-OUT-HIGH-001 | UAE Federal AML Law & OFAC Indirect Benefits |
| UAE-VARA-DEP-SELF-SEVERE-001 | UAE Federal AML Law & VARA Rulebook Section 3.1 & FATF Rec 10 |
| UAE-VARA-DEP-SELF-HIGH-001 | VARA Rulebook Section 3.1 (EDD/Ongoing CDD) |
| UAE-VARA-WHL-001 | TrustIn UAE VARA Guide Section 2.1 |
| UAE-VARA-WDR-SEVERE-001 | UAE Federal AML Law & VARA Rulebook Section 4 (STR) |
| UAE-VARA-WDR-SEVERE-002 | UAE Federal AML Law & VARA Rulebook Section 4 (Hop 2-3) |
| UAE-VARA-WDR-HIGH-001 | UAE EOCN & Pollution Decay Principle |
| UAE-VARA-WDR-HIGH-002 | VARA Rulebook Section 3.1 (EDD on Outflow) |
| UAE-VARA-WDR-SELF-SEVERE-001 | UAE Federal AML Law & VARA Rulebook Section 4 (Ongoing CDD) |
| UAE-VARA-WDR-SELF-HIGH-001 | VARA Rulebook Section 3.1 (Ongoing CDD) |
| UAE-VARA-TX-001 | UAE Federal AML Threshold (AED 3,500) |
| UAE-VARA-CDD-HIGH-001 | UAE Federal AML Threshold & VARA CDD Requirements |
| UAE-VARA-TX-002 | TrustIn UAE VARA Guide 3 (Structuring) |
