# UN Consolidated Sanctions List

**Source**: United Nations Security Council
**Type**: Consolidated Sanctions Reference
**Update Frequency**: As resolutions are adopted

---

## Overview

The UN Security Council Consolidated List includes all individuals and entities subject to sanctions measures imposed by the Security Council. This list is the foundation for many national sanctions regimes.

---

## Key Sanctions Regimes Relevant to Virtual Assets

### 1. DPRK (North Korea) Sanctions

**Resolution**: UNSCR 1718 (2006) and subsequent resolutions

**Relevance to Crypto**:
- DPRK-linked actors actively use cryptocurrency for sanctions evasion
- Lazarus Group and related APT actors
- Crypto exchange hacks attributed to DPRK

**Key Designations**:
- Lazarus Group
- Reconnaissance General Bureau (RGB)
- Various front companies and individuals

### 2. Iran Sanctions

**Resolution**: UNSCR 1737 (2006) and subsequent resolutions

**Relevance to Crypto**:
- Iranian entities using crypto to evade financial sanctions
- Mining operations to generate foreign currency
- Cross-border payments via virtual assets

### 3. Terrorism-Related Sanctions

**Resolution**: UNSCR 1267 (1999) - Al-Qaida/ISIL (Da'esh)

**Relevance to Crypto**:
- Terrorist financing via cryptocurrency donations
- Use of privacy coins and mixers
- Cross-border fund transfers

---

## How to Access UN Sanctions Data

### Official Sources

1. **UN Security Council Consolidated List**
   - URL: https://www.un.org/securitycouncil/content/un-sc-consolidated-list
   - Format: XML, PDF
   - Updates: Real-time

2. **Sanctions List Search**
   - URL: https://scsanctions.un.org/search/
   - Interactive search tool

### Data Fields Available

| Field | Description |
|-------|-------------|
| Reference Number | Unique identifier |
| Name | Full name/entity name |
| Aliases | Known aliases |
| Date of Birth | For individuals |
| Nationality | Country of origin |
| Address | Known addresses |
| Passport/ID | Document numbers |
| Listing Date | When added to list |
| Narrative | Reason for listing |

---

## Integration with AML Systems

### Screening Requirements

1. **Customer Screening**
   - Screen all customers against UN list
   - Real-time or batch screening
   - Fuzzy matching for name variations

2. **Transaction Screening**
   - Screen counterparties
   - Screen wallet addresses (where linked to sanctioned entities)
   - Geographic screening

### Best Practices

1. **Data Updates**
   - Subscribe to UN sanctions updates
   - Implement automated list updates
   - Document update procedures

2. **Match Handling**
   - Clear escalation procedures
   - Documentation requirements
   - Regulatory reporting

3. **Record Keeping**
   - Retain screening records
   - Document false positive dispositions
   - Audit trail maintenance

---

## Crypto-Specific Designations

### OFAC Designated Crypto Addresses

Note: While UN does not directly designate crypto addresses, OFAC (US) has designated specific addresses linked to UN-sanctioned entities:

- Lazarus Group wallet addresses
- Tornado Cash smart contracts
- Various mixer services

### Cross-Reference Requirements

For comprehensive sanctions screening in crypto:
1. UN Consolidated List
2. OFAC SDN List (includes crypto addresses)
3. EU Consolidated List
4. National sanctions lists (as applicable)

---

## Regulatory Expectations

### FATF Guidance

- Targeted Financial Sanctions (TFS) must cover VAs/VASPs
- Real-time screening for high-risk transactions
- Ability to freeze assets without delay

### Jurisdictional Requirements

| Jurisdiction | Requirement |
|--------------|-------------|
| Singapore | MAS requires UN + Singapore lists |
| Dubai | VARA requires UN + UAE lists |
| Hong Kong | SFC requires UN + HK lists |

---

## Resources

- **UN SC Consolidated List**: https://www.un.org/securitycouncil/content/un-sc-consolidated-list
- **UN Sanctions App**: https://www.un.org/securitycouncil/content/un-sc-consolidated-list-app
- **FATF TFS Guidance**: https://www.fatf-gafi.org/

---

**Note**: This document provides an overview for compliance reference. Always consult official UN sources for the authoritative and current sanctions list.
