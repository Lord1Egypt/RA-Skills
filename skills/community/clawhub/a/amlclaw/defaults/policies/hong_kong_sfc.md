# Hong Kong SFC — AML/CFT Compliance Policy for Virtual Asset Service Providers

## 1. Jurisdiction & Regulatory Framework

This policy applies to Virtual Asset Service Providers (VASPs) and Licensed Virtual Asset Trading Platforms (VATPs) operating under the Hong Kong Securities and Futures Commission (SFC) regulatory framework.

**Applicable regulations:**
- **Anti-Money Laundering and Counter-Terrorist Financing Ordinance (AMLO)** — Cap. 615
- **SFC AML/CFT Guidelines** — Guidelines for Licensed Corporations and SFC-Licensed VATPs
- **SFC AML Guideline Sections 4.1.9, 5.10, 12.7, 12.11, 12.14, 12.15.2** — Key provisions for VA screening
- **FATF 40 Recommendations** (2023 update) — International AML/CFT standards
- **FATF VA/VASP Guidance** (2021) — Virtual asset-specific guidance
- **FATF Recommendation 16** — Travel Rule for wire transfers / VA transfers
- **OFAC SDN List** — US Office of Foreign Assets Control Specially Designated Nationals
- **UN Consolidated Sanctions List** — United Nations Security Council sanctions

## 2. Customer Due Diligence (CDD)

### 2.1 Standard CDD (AMLO Schedule 2, SFC AML Guideline 4.1)
- Verify identity of all customers before establishing business relationships
- CDD required for occasional transactions ≥ HKD 8,000 (~USD 1,025)
- Identify and verify beneficial owners (>25% ownership threshold)
- Understand nature and purpose of business relationship
- Ongoing monitoring of transactions and updating of customer information
- **Unhosted wallet threshold**: Full KYC/CDD verification for single transactions > USD 1,000 (~HKD 7,800) per rule `HK-SFC-CDD-HIGH-001`

### 2.2 Enhanced Due Diligence (EDD) (SFC AML Guideline 12.15.2)
EDD is required when:
- Higher ML/TF risk identified through institutional risk assessment
- Customer is a PEP or associated with a PEP
- Transactions linked to FATF high-risk or grey-listed jurisdictions
- Complex or unusually large transactions with no apparent economic purpose
- Blockchain analytics show Sanctions/Terrorism exposure at Hop 4-5 — per rule `HK-SFC-DEP-HIGH-001`
- Any exposure (>0%) to Cybercrime or Obfuscation — per rule `HK-SFC-DEP-HIGH-002` (zero-tolerance)
- Gambling/High-Risk Entities exposure >30% AND >USD 1,000 — per rule `HK-SFC-DEP-HIGH-003`
- Target address self-tagged as Cybercrime or Obfuscation — per rules `HK-SFC-DEP-SELF-HIGH-001`, `HK-SFC-WDR-SELF-HIGH-001`

EDD procedures include:
- Senior management approval for relationship continuation
- Additional source of funds / source of wealth documentation
- Increased frequency and depth of transaction monitoring
- Detailed record keeping of risk assessment rationale

## 3. Blockchain-Specific Risk Indicators

Risk categories based on TrustIn KYA label taxonomy, calibrated for SFC requirements:

| Risk Tier | Primary Categories | SFC-Specific Notes |
|-----------|-------------------|-------------------|
| **Severe** | Sanctions, Terrorism Financing, Public Freezing Action, Illicit Markets, Other Financial Crimes | Zero tolerance. Immediate freeze and JFIU report. |
| **High** | Cybercrime, Obfuscation | **SFC mandates zero-tolerance** for Mixers/Darknet — any exposure (>0%) triggers Reject (`HK-SFC-DEP-HIGH-002`) |
| **High** | Gambling, High-Risk Entities | Threshold-based: >30% exposure AND >USD 1,000 |
| **Medium** | Other Entities (select) | Black/Grey Industry, MEV Bots/Arbitrage, Spam |
| **Low / Whitelist** | Exchanges & DeFi, Other Entities | CEX, TradFi — whitelist stop rule (`HK-SFC-WHL-001`) |

**Key SFC distinction**: Hong Kong applies **zero-tolerance for Cybercrime and Obfuscation** (Mixers, Privacy Wallets, Privacy Tokens). Any exposure >0% triggers rejection, regardless of amount or hop distance. This is stricter than Singapore's threshold-based approach.

## 4. Screening Procedures by Scenario

### 4.1 Deposit Screening
**Inflow analysis** (where did the funds come from?):
- **Hop 1 (direct)**: Sanctions/Terrorism/Illicit → **Freeze** (`HK-SFC-DEP-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism/Illicit → **Freeze** (`HK-SFC-DEP-SEVERE-002`)
- **Hop 4-5 (far)**: Sanctions/Terrorism/Illicit → **EDD** (`HK-SFC-DEP-HIGH-001`)
- **Zero-tolerance**: Any Cybercrime/Obfuscation exposure >0% → **Reject** (`HK-SFC-DEP-HIGH-002`)
- **Threshold**: Gambling/High-Risk >30% AND >USD 1,000 → **EDD** (`HK-SFC-DEP-HIGH-003`)

**Outflow history** (where has this address previously sent funds?):
- **Hop 1 (direct)**: Funded Sanctions/Terrorism → **Freeze** (`HK-SFC-DEP-OUT-SEVERE-001`)
- **Hop 2-3 (indirect)**: Funded Sanctions/Terrorism → **EDD** (`HK-SFC-DEP-OUT-HIGH-001`)

**Self-tag** (is the address itself flagged?):
- Sanctions/Terrorism/Illicit tag → **Freeze** (`HK-SFC-DEP-SELF-SEVERE-001`)
- Cybercrime/Obfuscation tag → **EDD** (`HK-SFC-DEP-SELF-HIGH-001`)

### 4.2 Withdrawal Screening
**Outflow analysis** (where are the funds going?):
- **Hop 1 (direct)**: Sanctions/Terrorism destination → **Freeze** (`HK-SFC-WDR-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism destination → **Freeze** (`HK-SFC-WDR-SEVERE-002`)
- **Threshold**: Cybercrime/Obfuscation/Gambling >10% AND >USD 100 → **EDD** (`HK-SFC-WDR-HIGH-001`)

**Self-tag gate** (is the withdrawing address flagged?):
- Sanctions/Terrorism/Illicit → **Freeze** (`HK-SFC-WDR-SELF-SEVERE-001`)
- Cybercrime/Obfuscation → **EDD** (`HK-SFC-WDR-SELF-HIGH-001`)

### 4.3 Onboarding Screening
- Run deposit self-tag and inflow checks against submitted customer addresses
- Severe → reject onboarding, file STR with JFIU
- High → proceed only with EDD and senior management approval
- Low/Medium → approve with standard monitoring tier

## 5. Risk Rating Matrix

| Risk Level | Action | Operational Response |
|------------|--------|---------------------|
| **Severe** | Freeze | Immediate asset freeze. Escalate to MLRO. File STR with JFIU as soon as reasonably practicable. No tipping off. |
| **High** | EDD / Reject | Enhanced due diligence or reject (for zero-tolerance categories). Compliance Officer review within 48 hours. |
| **Medium** | Review / Flag | Compliance team review within 24 hours. Document rationale. Increase monitoring frequency. |
| **Low** | Allow | Standard processing. Routine monitoring. |

## 6. Suspicious Transaction Reporting (STR)

- **Reporting authority**: Joint Financial Intelligence Unit (JFIU), jointly operated by Hong Kong Police Force and Customs & Excise Department
- **Filing deadline**: As soon as **reasonably practicable** after forming suspicion (AMLO Section 25A)
- **Filing method**: Via JFIU electronic submission portal
- **Tipping off prohibition**: Criminal offence under AMLO Section 25A(4) — strictly prohibited
- **Predicate offences**: Dealing with property known or believed to represent proceeds of an indictable offence (OSCO Section 25) or terrorist property (UNATMO Section 14)
- **Record keeping**: Maintain copies of all STRs and supporting documentation for minimum 6 years
- **Defence STR**: Filing provides a statutory defence against ML/TF charges for the reporting institution

## 7. Record Keeping Requirements

Per AMLO Schedule 2 and SFC AML Guidelines:
- **CDD records**: Minimum **6 years** after termination of business relationship
- **Transaction records**: Minimum **6 years** from date of transaction
- **Screening reports**: Retain all graph data, risk paths, and screening decisions for 6 years
- **STR records**: Maintain filing records and supporting evidence for 6 years
- **Ruleset versioning**: Archive all rule configuration changes with timestamps for audit trail
- **Unhosted wallet assessments**: Retain proof of ownership documentation for 6 years

## 8. Travel Rule Compliance (FATF Recommendation 16, SFC AML Guideline 12.11 & 12.14)

Per rule `HK-SFC-TX-001`:
- **Threshold**: VA transfers > USD 1,000 (~HKD 7,800) trigger Travel Rule and unhosted wallet proof requirements
- **Required originator information**: Name, account number (wallet address), unique transaction reference
- **Required beneficiary information**: Name, account number (wallet address)
- **Counterparty VASP verification**: Verify receiving institution is SFC-licensed or equivalent foreign-regulated
- **Unhosted wallet transfers**: Require proof of ownership (signed message or micro-transaction verification) per SFC Guideline 12.14
- **Threshold for CDD**: Single transaction > USD 1,000 triggers full KYC verification (`HK-SFC-CDD-HIGH-001`)

## 9. Sanctions Screening Requirements

### 9.1 Lists to Screen Against
- **OFAC SDN List** — Specially Designated Nationals and Blocked Persons
- **UN Consolidated Sanctions List** — UN Security Council consolidated list
- **FATF High-Risk Jurisdictions** — Countries under increased monitoring or call for action
- **Hong Kong Designated Lists** — Under United Nations Sanctions Ordinance (Cap. 537) and United Nations (Anti-Terrorism Measures) Ordinance (Cap. 575)
- **PRC sanctions lists** — Where applicable to HK-regulated entities

### 9.2 Screening Procedures
- Screen all customers and counterparties at onboarding and ongoing
- Re-screen full portfolio within **24 hours** of any sanctions list update
- Blockchain address screening via TrustIn KYA API for entity-level sanctions tags
- Name screening with fuzzy matching (minimum 85% match threshold)
- Cross-reference wallet clusters against known sanctioned entity addresses

## 10. Ongoing Monitoring

### 10.1 Transaction Monitoring
- **Real-time**: All deposits and withdrawals screened before processing
- **Structuring detection**: Daily cumulative alerts > USD 10,000 to prevent HKD 8,000 Travel Rule evasion (`HK-SFC-TX-002`)
- **Periodic re-screening**: Quarterly for high-risk customers, annually for standard
- **Event-driven**: Immediate re-screening on sanctions list updates or customer behaviour changes

### 10.2 Risk Re-Assessment
- Quarterly risk reassessment for high-risk customers
- Annual risk reassessment for standard customers
- Addresses may acquire new risk labels over time — ongoing CDD must account for evolving threat intelligence
- Update CDD records when material changes are identified

## 11. Escalation Procedures

1. **Automated flag** → Compliance team review within **24 hours**
2. **EDD trigger** → Compliance Officer review within **48 hours**
3. **Freeze trigger** → Immediate escalation to MLRO, asset freeze enforced, STR filed with JFIU as soon as reasonably practicable
4. **Regulatory reporting** → Quarterly compliance report to SFC, annual AML return
5. **Board reporting** → Quarterly AML/CFT effectiveness report to senior management

## 12. Rule-to-Regulation Traceability

| Rule ID | Regulation Reference |
|---------|---------------------|
| HK-SFC-DEP-SEVERE-001 | SFC AML Guideline 4.1.9 & 12.7 & OFAC SDN Direct Contact |
| HK-SFC-DEP-SEVERE-002 | SFC AML Guideline 4.1.9 & 12.7 |
| HK-SFC-DEP-HIGH-001 | SFC AML Guideline 12.15.2 & Pollution Decay Principle |
| HK-SFC-DEP-HIGH-002 | SFC AML Guideline 12.15.2 (Zero-tolerance Cybercrime/Obfuscation) |
| HK-SFC-DEP-HIGH-003 | TrustIn HK VATP Guide Section 2.1 |
| HK-SFC-DEP-OUT-SEVERE-001 | SFC AML Guideline 4.1.9 & OFAC Indirect Benefits Prohibition |
| HK-SFC-DEP-OUT-HIGH-001 | SFC AML Guideline 12.15.2 & OFAC Indirect Benefits |
| HK-SFC-DEP-SELF-SEVERE-001 | SFC AML Guideline 4.1.9 & FATF Recommendation 10 |
| HK-SFC-DEP-SELF-HIGH-001 | SFC AML Guideline 12.15.2 (CDD/Ongoing CDD) |
| HK-SFC-WHL-001 | TrustIn HK VATP Guide Section 2.1 |
| HK-SFC-WDR-SEVERE-001 | SFC AML Guideline 4.1.9 & 12.7 (Outflow Hop 1) |
| HK-SFC-WDR-SEVERE-002 | SFC AML Guideline 4.1.9 & 12.7 (Outflow Hop 2-3) |
| HK-SFC-WDR-HIGH-001 | SFC AML Guideline 12.15.2 (Outflow EDD) |
| HK-SFC-WDR-SELF-SEVERE-001 | SFC AML Guideline 4.1.9 & 12.7 (Ongoing CDD) |
| HK-SFC-WDR-SELF-HIGH-001 | SFC AML Guideline 12.15.2 (Ongoing CDD) |
| HK-SFC-TX-001 | SFC AML Guideline 12.11 & 12.14 (Travel Rule) |
| HK-SFC-CDD-HIGH-001 | SFC AML Guideline 12.11 (CDD for unhosted wallets) |
| HK-SFC-TX-002 | SFC AML Guideline 5.10 (Structuring) |
