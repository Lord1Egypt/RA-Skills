# OFAC Virtual Currency Sanctions Compliance Guidance

**Purpose**: U.S. sanctions compliance requirements for virtual currency transactions
**Key Assumptions**: Applies to U.S. persons and entities under OFAC jurisdiction
**Usage Patterns**: Sanctions screening; SDN list checking; compliance program design

---

## Overview

- **Authority**: Office of Foreign Assets Control (OFAC), U.S. Department of the Treasury
- **Legal Basis**: International Emergency Economic Powers Act (IEEPA); Trading with the Enemy Act (TWEA)
- **Applies to**: U.S. persons, entities, and foreign persons engaging with U.S. financial system
- **Source**: https://ofac.treasury.gov/faqs/topic/1626

---

## Part 1 - Definitions

### Virtual Currency

| Term | Definition |
|------|------------|
| **Digital Currency** | Sovereign cryptocurrency, virtual currency (non-fiat), and digital representation of fiat currency |
| **Virtual Currency** | Digital representation of value that functions as medium of exchange, unit of account, or store of value without government backing |
| **Digital Currency Address** | Alphanumeric identifier associated with wallet that can receive transfers |
| **Hosted Wallet Provider** | Business that creates and stores wallets for customers |

### Persons Subject to OFAC

- U.S. citizens and permanent residents (anywhere in world)
- Entities organized under U.S. law
- Persons physically present in the U.S.
- Foreign branches of U.S. entities
- Foreign persons dealing with U.S. origin goods/services

---

## Part 2 - Compliance Obligations

### Core Requirements

All persons subject to OFAC jurisdiction must:

| Obligation | Description |
|------------|-------------|
| **Screen transactions** | Check against SDN List and other sanctions lists |
| **Block property** | Freeze assets of designated persons |
| **Avoid dealings** | Refrain from unauthorized transactions with sanctioned entities |
| **Report blocked property** | Report within 10 business days, then annually |

### Equal Application

OFAC sanctions apply equally regardless of:
- Transaction type (fiat vs. virtual currency)
- Technology used
- Location of parties (if U.S. nexus exists)

### Risk-Based Compliance Programs

Organizations should develop:
- Tailored compliance programs appropriate to business model
- Screening procedures for virtual currency transactions
- Training for staff handling virtual currency
- Escalation procedures for potential matches

---

## Part 3 - SDN List and Digital Currencies

### Digital Currency Addresses on SDN List

OFAC designates specific wallet addresses using structured format:
- Format: "Digital Currency Address - [Currency Code]"
- Example: "Digital Currency Address - XBT" (Bitcoin)
- Example: "Digital Currency Address - ETH" (Ethereum)

### Searching the SDN List

| Method | Description |
|--------|-------------|
| **Sanctions List Search Tool** | Official OFAC search interface |
| **ID # Field** | Use for exact address matches |
| **Downloadable Files** | XML, CSV, PDF formats available |
| **API Access** | For automated screening |

### Designated Entities (Examples)

| Entity/Address Type | Examples |
|---------------------|----------|
| **Ransomware operators** | Addresses used in ransomware attacks |
| **Darknet markets** | Addresses associated with illegal marketplaces |
| **Sanctioned exchanges** | Garantex, Suex, Chatex |
| **State actors** | DPRK-affiliated addresses, Iranian addresses |

---

## Part 4 - Blocking and Reporting

### Blocking Requirements

When virtual currency belonging to SDN is identified:

| Action | Requirement |
|--------|-------------|
| **Deny access** | Prevent all parties from accessing blocked assets |
| **Segregate** | Separate blocked assets from other holdings |
| **Document** | Maintain records of blocking action |
| **Preserve** | Do not transfer, convert, or dispose of assets |

### Reporting Requirements

| Report Type | Deadline | Method |
|-------------|----------|--------|
| **Initial blocking report** | 10 business days | OFAC online portal |
| **Annual report** | By September 30 annually | OFAC online portal |
| **Rejected transaction report** | 10 business days | OFAC online portal |

### Unblocking Process

Customers may request unblocking through:
1. OFAC online application portal
2. Specific license request
3. Demonstrate case of mistaken identity
4. Await delisting of underlying designation

---

## Part 5 - Enforcement

### Recent Enforcement Actions

| Entity | Date | Action | Amount |
|--------|------|--------|--------|
| **Garantex** | August 2025 | Re-designation | N/A (asset freeze) |
| **Grinex** | August 2025 | Designation | N/A (asset freeze) |
| **Tornado Cash** | August 2022 | Designation | $7+ billion processed |
| **Blender.io** | May 2022 | Designation | First mixer sanctioned |

### Penalty Framework

| Violation Type | Civil Penalty | Criminal Penalty |
|----------------|---------------|------------------|
| **Willful violation** | Up to $1M per violation | Up to 20 years imprisonment |
| **Non-willful violation** | Up to $250K per violation | N/A |
| **Corporate violation** | Greater of $250K or twice transaction value | Corporate criminal liability |

### Mitigating Factors

OFAC considers:
- Existence of compliance program
- Voluntary self-disclosure
- Cooperation with investigation
- Remedial measures taken

---

## Part 6 - Specific Sanctions Programs

### Iran

| Prohibition | Scope |
|-------------|-------|
| **Financial transactions** | Nearly all transactions prohibited |
| **Virtual currency** | Included in comprehensive sanctions |
| **Secondary sanctions** | Foreign persons may face sanctions for Iran dealings |

### DPRK (North Korea)

| Prohibition | Scope |
|-------------|-------|
| **All transactions** | Comprehensive embargo |
| **Virtual currency** | Known to use crypto for sanctions evasion |
| **Cyber operations** | State-sponsored hacking linked to crypto theft |

### Russia

| Prohibition | Scope |
|-------------|-------|
| **Financial sector** | Broad restrictions on financial institutions |
| **Oligarchs** | Individual designations with crypto holdings |
| **Specific exchanges** | Garantex and successors designated |

### Ransomware-Related

| Focus | Description |
|-------|-------------|
| **Addresses** | Wallet addresses used in ransomware payments |
| **Operators** | Individuals operating ransomware schemes |
| **Facilitators** | Exchanges and mixers facilitating payments |

---

## Part 7 - Compliance Best Practices

### Screening Implementation

1. **Real-time screening**: Screen transactions before processing
2. **Batch screening**: Regular rescreening of customer base
3. **Address format handling**: Account for different address formats
4. **Fuzzy matching**: Consider variations and aliases

### Transaction Monitoring

| Indicator | Risk Level |
|-----------|------------|
| **Direct SDN address** | Critical - Block immediately |
| **One-hop from SDN** | High - Enhanced review |
| **Mixer/tumbler use** | High - Investigate source |
| **High-risk jurisdiction** | Elevated - Apply EDD |

### Documentation

Maintain records of:
- All screening results
- False positive resolutions
- Blocking actions and reports
- Compliance program updates

---

## Part 8 - Technical Considerations

### Blockchain Analysis

| Capability | Purpose |
|------------|---------|
| **Address clustering** | Identify related addresses |
| **Transaction tracing** | Follow fund flows |
| **Risk scoring** | Assess address risk levels |
| **Pattern detection** | Identify evasion techniques |

### API Integration

OFAC provides:
- Sanctions List Search API
- Downloadable list files (updated daily)
- Structured data formats

### Multi-Chain Considerations

| Chain | OFAC Designations |
|-------|-------------------|
| **Bitcoin (XBT)** | Yes - addresses designated |
| **Ethereum (ETH)** | Yes - addresses and smart contracts |
| **Other chains** | Emerging - TRON, BSC addresses appearing |

---

## Referenced Regulations

| Regulation | Description |
|------------|-------------|
| 31 CFR Part 501 | OFAC administrative procedures |
| 31 CFR Part 560 | Iranian Transactions and Sanctions Regulations |
| 31 CFR Part 510 | North Korea Sanctions Regulations |
| 31 CFR Part 589 | Ukraine-Related Sanctions Regulations |
| EO 13694 | Blocking Property of Certain Persons Engaging in Significant Malicious Cyber-Enabled Activities |

---

## Relevance to TrustIn Reports

- Address screening against OFAC SDN list
- Transaction risk scoring based on sanctions exposure
- Compliance evidence for regulated entity customers
- Cross-reference with on-chain analysis findings
