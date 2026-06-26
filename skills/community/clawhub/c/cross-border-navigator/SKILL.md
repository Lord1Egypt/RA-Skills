---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_126c9e245d0711f19299525400d9a7a1
    ReservedCode1: lH5mHoKm4szntsndPk/nMoXphzx4/U6PRXGmCEhFLoki/sWCWg79ii0+YBE5T0BQYMDyIzw3AGWKldH2rE1T0P7/WjQb8AWzrUf+8tFPjazfc+EI1aOimje4HGIR+trOxGtYdrSJg0qDTXDS8IBX3Of9r60zSjdYFM2AiiqddqZ5PPzhIN3VELB7Pvw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_126c9e245d0711f19299525400d9a7a1
    ReservedCode2: lH5mHoKm4szntsndPk/nMoXphzx4/U6PRXGmCEhFLoki/sWCWg79ii0+YBE5T0BQYMDyIzw3AGWKldH2rE1T0P7/WjQb8AWzrUf+8tFPjazfc+EI1aOimje4HGIR+trOxGtYdrSJg0qDTXDS8IBX3Of9r60zSjdYFM2AiiqddqZ5PPzhIN3VELB7Pvw=
---

# Cross-Border Business Navigator (跨境商业导航)

## Description
A global business intelligence skill that guides international market entry, cross-border operations, and multinational strategy. It provides comprehensive analysis of regulatory environments, cultural nuances, tax treaties, entry strategies, and geopolitical risks across 190+ countries. Designed for exporters, foreign investors, supply chain managers, international lawyers, and global business strategists who need actionable intelligence to navigate complex cross-border landscapes.

**Keywords**: international business, market entry, cross-border, trade, export, foreign investment, regulatory compliance, tax treaty, cultural intelligence, supply chain, sanctions, sanctions screening, localization

## Triggers
- "how to enter [country] market for [product/service]"
- "compare business environments in [country A] vs [country B]"
- "what are the regulatory requirements for [industry] in [region]"
- "cross-border M&A checklist for [target country]"
- "tax implications of setting up subsidiary in [country]"
- "cultural negotiation tips for [country]"
- "supply chain risks in [region]"
- "is [country] under any trade sanctions"
- "IP protection strategy for [country]"
- "best market entry mode for [sector] in [region]"

## Capabilities

### 1. Market Entry Intelligence
- **Country feasibility score**: Weighted multi-factor assessment (market size, growth, competition, ease of doing business, regulatory burden, cultural distance)
- **Entry mode recommendation**: Match 6 entry strategies (Direct Export, Licensing, Joint Venture, WOS, Strategic Alliance, M&A) to country + industry context with risk/control/investment tradeoff tables
- **Total cost of entry estimation**: Break down registration, legal, tax, office setup, staffing, compliance costs

### 2. Regulatory & Compliance Mapping
- **Sanctions screening**: Check against OFAC SDN List, EU Consolidated List, UN Security Council sanctions, and country-specific restricted parties
- **Export control classification**: Identify dual-use items, EAR/ITAR requirements (US), EU Dual-Use Regulation, Wassenaar Arrangement
- **Data protection requirements**: Map GDPR adequacy decisions, China PIPL, Japan APPI, Brazil LGPD, India DPDP Act — and cross-border data transfer mechanisms
- **Sector-specific regulations**: Financial services licensing, healthcare/medical device approval, food/drug safety, telecommunications, energy/mining

### 3. Cultural Intelligence & Negotiation
- **Hofstede dimensions**: Power distance, individualism, uncertainty avoidance, masculinity, long-term orientation, indulgence — with business implications
- **Negotiation playbooks**: Per-region negotiation style (direct vs indirect, relationship vs contract, individual vs collective decision-making)
- **Business etiquette**: Greetings, gift-giving, business card exchange, dining protocol, hierarchy expectations, meeting punctuality norms
- **Communication style**: High-context vs low-context, direct vs indirect feedback, silence interpretation

### 4. Tax & Financial Structure
- **Tax treaty network analysis**: Withholding tax rates on dividends/interest/royalties, permanent establishment thresholds
- **Transfer pricing**: Arm's length principle, documentation requirements per OECD BEPS Action 13
- **Currency & capital controls**: Repatriation restrictions, foreign exchange regulations, hedging recommendations
- **Incentive discovery**: Special economic zones, tax holidays, R&D credits, investment incentives by country

### 5. Risk Assessment Framework
Score across 5 categories (HIGH / MEDIUM / LOW severity):
| Risk Category | Factors |
|---|---|
| Regulatory & Compliance | Sanctions, export controls, data localization, anti-corruption |
| Currency & Financial | FX volatility, capital controls, inflation, sovereign default |
| Political & Geopolitical | Regime stability, sanctions, expropriation, civil unrest |
| Cultural & Operational | Communication barriers, negotiation mismatch, talent localization |
| IP & Technology | IP protection adequacy, tech transfer requirements, cybersecurity |

### 6. Output Formats

**Market Entry Report Structure**:
1. **Executive Recommendation** (1-paragraph go/no-go with rationale)
2. **Country Profile** (GDP, population, ease of doing business rank, key indices)
3. **Market Opportunity** (sector size, growth rate, competitive landscape)
4. **Entry Strategy** (recommended mode with justification, timeline, cost estimate)
5. **Regulatory Roadmap** (step-by-step: registration, licensing, permits, timeline)
6. **Tax & Financial Architecture** (optimal holding structure, treaty benefits, effective tax rate)
7. **Cultural Playbook** (negotiation tips, communication style, key do's and don'ts)
8. **Risk Matrix** (5-category heatmap with mitigation strategies)
9. **Action Plan** (90-day, 6-month, 1-year milestones)

## Workflow

```
User Query
    ↓
[Step 1] Identify target country/region + business sector + objective
    ↓
[Step 2] Parallel web_search: (a) sanctions check, (b) regulatory landscape, (c) market data
    ↓
[Step 3] web_fetch authoritative sources: government portals, World Bank, tax authority sites
    ↓
[Step 4] Cultural analysis: Hofstede dimensions, business etiquette research
    ↓
[Step 5] Risk scoring across 5 categories with evidence
    ↓
[Step 6] Entry strategy recommendation with cost/benefit/timeline
    ↓
[Step 7] Generate structured report with actionable roadmap
    ↓
Final Output: Market entry report + risk matrix + 90-day action plan
```

## Usage Guidelines
1. **Sanctions-first**: Always check sanctions/compliance as step 2 — before any market opportunity analysis
2. **Currency of information**: Flag regulatory data older than 12 months as potentially outdated; regulations change frequently
3. **No legal advice disclaimer**: Explicitly state that the output is business intelligence, not legal advice; recommend consulting qualified local counsel for binding decisions
4. **Dual perspectives**: When significant political or trade tensions exist between the user's home country and the target country, present risks from both sides
5. **Language**: Match response language to user; use local terminology where relevant (e.g., "GmbH" not "LLC" for Germany)

## Examples

**Query**: "We are a SaaS company in Singapore looking to expand to Germany. What should we know?"

**Response Structure**:
1. Executive recommendation: Germany viable; GDPR compliance is #1 gate; recommend phased entry via representative office → GmbH subsidiary
2. Country profile + SaaS market data (€XXB market, XX% CAGR)
3. Recommended entry: Representative office (6 months) → GmbH subsidiary (register with Handelsregister, minimum €25K share capital)
4. Regulatory roadmap: GDPR compliance checklist, DPA appointment, EU AI Act implications for SaaS, Impressum requirements
5. Tax: Singapore-Germany DTA — withholding tax rates, GmbH corporate tax ~30%, VAT 19% (reverse charge for B2B SaaS)
6. Cultural playbook: German directness in negotiations, formal titles (Herr/Frau Doktor), punctuality, written contracts over verbal agreements, decision by consensus in Mittelstand companies
7. Risk matrix: GDPR fines (HIGH), works council requirements for hiring (MEDIUM), FX EUR/SGD volatility (LOW)
8. 90-day action plan: Engage German data protection lawyer, begin GDPR gap analysis, identify local sales lead, register trademark with DPMA

## References
- `references/global_business_data.json`: Regional frameworks, risk categories, entry strategies, tax treaty networks, regulatory bodies for all major economies
*（内容由AI生成，仅供参考）*
