# Singapore MAS — AML/CFT Compliance Policy for Digital Payment Token Services

## 1. Jurisdiction & Regulatory Framework

This policy applies to Digital Payment Token (DPT) service providers licensed under the Payment Services Act 2019 (PS Act) in Singapore, regulated by the Monetary Authority of Singapore (MAS).

**Applicable regulations:**
- **MAS Notice PSN02** — Prevention of Money Laundering and Countering the Financing of Terrorism for DPT Services
- **MAS Notice PSN08** — Technology Risk Management
- **FATF 40 Recommendations** (2023 update) — International AML/CFT standards
- **FATF VA/VASP Guidance** (2021) — Virtual asset-specific guidance
- **FATF Recommendation 16** — Travel Rule for wire transfers / VA transfers
- **OFAC SDN List** — US Office of Foreign Assets Control Specially Designated Nationals
- **UN Consolidated Sanctions List** — United Nations Security Council sanctions
- **FATF High-Risk Jurisdictions** — Countries with strategic AML/CFT deficiencies

## 2. Customer Due Diligence (CDD)

### 2.1 Standard CDD (MAS Notice PSN02 Section 6)
- Verify identity of all customers before establishing a business relationship
- Obtain beneficial ownership information for legal entities (>25% ownership threshold)
- Understand the purpose and intended nature of the business relationship
- Perform ongoing due diligence including transaction monitoring
- **Occasional transaction threshold**: Full KYC/CDD required for single transactions > SGD 4,700 (~USD 3,500) per rule `SG-DPT-TX-002`

### 2.2 Enhanced Due Diligence (EDD) (MAS Notice PSN02 Section 6)
EDD is required when:
- Customer or counterparty is from a FATF grey/black-listed jurisdiction
- Transaction involves a Politically Exposed Person (PEP) or their associates
- Unusual or complex transaction patterns detected without apparent economic purpose
- Blockchain analytics reveal connections to high-risk entities (Cybercrime, Obfuscation, Gambling, High-Risk Entities) — per rules `SG-DPT-DEP-HIGH-002`, `SG-DPT-WDR-HIGH-002`
- Far-distance (Hop 4-5) exposure to Sanctions or Terrorism Financing — per rules `SG-DPT-DEP-HIGH-001`, `SG-DPT-WDR-HIGH-001`
- Target address self-tagged as Cybercrime or Obfuscation — per rules `SG-DPT-DEP-SELF-HIGH-001`, `SG-DPT-WDR-SELF-HIGH-001`

EDD procedures include:
- Senior management approval for relationship continuation
- Additional source of funds / source of wealth documentation
- Increased frequency of transaction monitoring
- More detailed record keeping of rationale for proceeding

## 3. Blockchain-Specific Risk Indicators

Risk categories are based on TrustIn KYA label taxonomy:

| Risk Tier | Primary Categories | Examples |
|-----------|-------------------|----------|
| **Severe** | Sanctions, Terrorism Financing, Public Freezing Action, Illicit Markets, Other Financial Crimes | Sanctioned Entity, Terrorist Organization, Law Enforcement Freeze, Human Trafficking, Suspected Money Laundering |
| **High** | Cybercrime, Obfuscation, Gambling, High-Risk Entities | Hacker/Thief, Ransomware, Phishing, Ponzi, Pig Butchering, Mixers, Privacy Wallet, Unlicensed Gambling, Sanctioned CEX |
| **Medium** | Other Entities (select) | Black/Grey Industry, MEV Bots/Arbitrage, Spam |
| **Low / Whitelist** | Exchanges & DeFi, Other Entities | CEX, TradFi, DeFi Protocol, Stablecoin, Mining Pools |

**Whitelist stop rule** (`SG-DPT-WHL-001`): Graph traversal stops at known compliant CEX or TradFi institutions to prevent false positives from deep-chain analysis.

## 4. Screening Procedures by Scenario

### 4.1 Deposit Screening
**Inflow analysis** (where did the funds come from?):
- **Hop 1 (direct)**: Sanctions/Terrorism/Illicit → **Freeze** (`SG-DPT-DEP-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism/Illicit → **Freeze** (`SG-DPT-DEP-SEVERE-002`)
- **Hop 4-5 (far)**: Sanctions/Terrorism/Illicit → **EDD** (`SG-DPT-DEP-HIGH-001`)
- **Threshold**: Cybercrime/Obfuscation/Gambling/High-Risk >10% AND >USD 50 → **EDD** (`SG-DPT-DEP-HIGH-002`)
- **Threshold**: Grey Industry/Spam >30% AND >USD 1,000 → **Review** (`SG-DPT-DEP-MED-001`)

**Outflow history** (where has this address previously sent funds?):
- **Hop 1 (direct)**: Funded Sanctions/Terrorism → **Freeze** (`SG-DPT-DEP-OUT-SEVERE-001`)
- **Hop 2-3 (indirect)**: Funded Sanctions/Terrorism → **EDD** (`SG-DPT-DEP-OUT-HIGH-001`)

**Self-tag** (is the address itself flagged?):
- Sanctions/Terrorism/Illicit tag → **Freeze** (`SG-DPT-DEP-SELF-SEVERE-001`)
- Cybercrime/Obfuscation tag → **EDD** (`SG-DPT-DEP-SELF-HIGH-001`)

### 4.2 Withdrawal Screening
**Outflow analysis** (where are the funds going?):
- **Hop 1 (direct)**: Sanctions/Terrorism destination → **Freeze** (`SG-DPT-WDR-SEVERE-001`)
- **Hop 2-3 (near)**: Sanctions/Terrorism destination → **Freeze** (`SG-DPT-WDR-SEVERE-002`)
- **Hop 4-5 (far)**: Sanctions/Terrorism destination → **EDD** (`SG-DPT-WDR-HIGH-001`)
- **Threshold**: Cybercrime/Obfuscation/Gambling >10% AND >USD 50 → **EDD** (`SG-DPT-WDR-HIGH-002`)

**Self-tag gate** (is the withdrawing address flagged?):
- Sanctions/Terrorism/Illicit → **Freeze** (`SG-DPT-WDR-SELF-SEVERE-001`)
- Cybercrime/Obfuscation → **EDD** (`SG-DPT-WDR-SELF-HIGH-001`)

### 4.3 Onboarding Screening
- Run deposit self-tag and inflow checks against the customer's submitted addresses
- Severe → reject onboarding, file STR
- High → proceed only with EDD and senior management approval
- Low/Medium → approve with standard monitoring

## 5. Risk Rating Matrix

| Risk Level | Action | Operational Response |
|------------|--------|---------------------|
| **Severe** | Freeze | Immediate asset freeze. Escalate to MLRO. File STR with STRO within 15 business days. No tipping off. |
| **High** | EDD | Enhanced due diligence. Senior compliance officer review within 48 hours. Obtain additional SOF/SOW documentation. |
| **Medium** | Review / Flag | Compliance officer review within 24 hours. Document rationale. Increased monitoring frequency. |
| **Low** | Allow | Standard processing. Routine monitoring. |

## 6. Suspicious Transaction Reporting (STR)

- **Reporting authority**: Suspicious Transaction Reporting Office (STRO), Commercial Affairs Department, Singapore Police Force
- **Filing deadline**: Within **15 business days** of forming suspicion (MAS Notice PSN02 Section 8)
- **Filing method**: Via STRO Online Notices and Reporting (SONAR) platform
- **Tipping off prohibition**: Strictly prohibited to disclose STR filing to the subject or any third party
- **Record keeping**: Maintain copies of all STRs and supporting documentation for minimum 5 years
- **Threshold for mandatory reporting**: Any transaction where there is reasonable ground to suspect ML/TF, regardless of amount

## 7. Record Keeping Requirements

Per MAS Notice PSN02:
- **CDD records**: Minimum **5 years** after termination of business relationship
- **Transaction records**: Minimum **5 years** from date of transaction
- **Screening reports**: Retain all graph data, risk paths, and screening decisions for 5 years
- **STR records**: Maintain filing records and supporting evidence for 5 years
- **Ruleset versioning**: Archive all rule configuration changes with timestamps for audit trail

## 8. Travel Rule Compliance (FATF Recommendation 16)

Per rule `SG-DPT-TX-001`:
- **Threshold**: Single VA transfer > USD 1,000 (~SGD 1,350) triggers Travel Rule obligations
- **Required originator information**: Name, account number (wallet address), physical address / national ID / date of birth
- **Required beneficiary information**: Name, account number (wallet address)
- **Counterparty VASP verification**: Verify the receiving institution is licensed/registered
- **Unhosted wallet transfers**: Require proof of ownership and enhanced CDD for transfers above threshold

## 9. Sanctions Screening Requirements

### 9.1 Lists to Screen Against
- **OFAC SDN List** — Specially Designated Nationals and Blocked Persons
- **OFAC Sectoral Sanctions** — Sectoral Sanctions Identifications List
- **UN Consolidated Sanctions List** — UN Security Council consolidated list
- **FATF High-Risk Jurisdictions** — Countries under increased monitoring or call for action
- **MAS Targeted Financial Sanctions** — Domestic designations under Terrorism (Suppression of Financing) Act and UN Act

### 9.2 Screening Procedures
- Screen all customers and counterparties at onboarding
- Re-screen full portfolio within **24 hours** of any sanctions list update
- Blockchain address screening via TrustIn KYA API for entity-level sanctions tags
- Fuzzy name matching for customer identity vs. sanctions lists (minimum 85% match threshold)

## 10. Ongoing Monitoring

### 10.1 Transaction Monitoring
- **Real-time**: All deposits and withdrawals screened before processing
- **Structuring detection**: Daily cumulative deposit alerts > USD 3,000 (`SG-DPT-TX-003`)
- **Periodic re-screening**: Monthly full portfolio re-screening for ongoing risk changes
- **Event-driven**: Immediate re-screening on sanctions list updates or material risk profile changes

### 10.2 Risk Re-Assessment
- Annual review of all customer risk ratings
- Quarterly review for high-risk customers
- Address risk labels change over time — an address clean at onboarding may be flagged later
- Update CDD records when material changes are identified

## 11. Escalation Procedures

1. **Automated flag** → Compliance officer review within **24 hours**
2. **EDD trigger** → Senior compliance officer review within **48 hours**
3. **Freeze trigger** → Immediate escalation to Money Laundering Reporting Officer (MLRO), asset freeze enforced, STR filed with STRO within 15 business days
4. **Regulatory reporting** → Annual compliance report to MAS
5. **Board reporting** → Quarterly AML/CFT effectiveness report to senior management

## 12. Rule-to-Regulation Traceability

| Rule ID | Regulation Reference |
|---------|---------------------|
| SG-DPT-DEP-SEVERE-001 | MAS Notice PSN02 Section 6 & OFAC SDN Direct Contact |
| SG-DPT-DEP-SEVERE-002 | MAS Notice PSN02 & TrustIn SG DPT Guide Section 1.A |
| SG-DPT-DEP-HIGH-001 | MAS Notice PSN02 & Pollution Decay Principle (OFAC) |
| SG-DPT-DEP-HIGH-002 | TrustIn KYA Pro SG DPT Guide Section 1.B & 2.2 |
| SG-DPT-DEP-MED-001 | TrustIn KYA Pro SG DPT Guide Section 1.C & 2.2 |
| SG-DPT-DEP-OUT-SEVERE-001 | MAS Notice PSN02 & OFAC Indirect Benefits Prohibition |
| SG-DPT-DEP-OUT-HIGH-001 | MAS Notice PSN02 & OFAC Indirect Benefits Prohibition |
| SG-DPT-DEP-SELF-SEVERE-001 | MAS Notice PSN02 Section 6 & FATF Recommendation 10 |
| SG-DPT-DEP-SELF-HIGH-001 | MAS Notice PSN02 Section 6 (CDD/Ongoing CDD) |
| SG-DPT-WHL-001 | TrustIn KYA Pro SG DPT Guide Section 2.1 |
| SG-DPT-WDR-SEVERE-001 | MAS Notice PSN02 Section 8 (STR) & FATF Recommendation 20 |
| SG-DPT-WDR-SEVERE-002 | MAS Notice PSN02 Section 8 & TrustIn SG DPT Guide |
| SG-DPT-WDR-HIGH-001 | MAS Notice PSN02 & Pollution Decay Principle |
| SG-DPT-WDR-HIGH-002 | MAS Notice PSN02 Section 6 (EDD) & TrustIn SG DPT Guide |
| SG-DPT-WDR-SELF-SEVERE-001 | MAS Notice PSN02 Section 6 & 8 (Ongoing CDD + STR) |
| SG-DPT-WDR-SELF-HIGH-001 | MAS Notice PSN02 Section 6 (Ongoing CDD) |
| SG-DPT-TX-001 | TrustIn KYA Pro SG DPT Guide Section 2.3 (Travel Rule) |
| SG-DPT-TX-002 | TrustIn KYA Pro SG DPT Guide Section 2.3 (CDD Threshold) |
| SG-DPT-TX-003 | TrustIn KYA Pro SG DPT Guide Section 2.3 (Structuring) |
