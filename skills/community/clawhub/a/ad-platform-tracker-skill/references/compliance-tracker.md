# Regulatory & Compliance Tracker

## Global Privacy Law Landscape (2025)

| Regulation | Region | Model | Key Requirement | Fine |
|---|---|---|---|---|
| GDPR | EU/EEA | Opt-in | Explicit consent before data collection | Up to €20M or 4% global revenue |
| UK GDPR | United Kingdom | Opt-in | Same as GDPR; UK-specific post-Brexit rules | Up to £17.5M or 4% global revenue |
| CCPA/CPRA | California, US | Opt-out | "Do Not Sell or Share" link required | Up to $7,500 per intentional violation |
| US State Laws | 19+ states as of 2025 | Varies | Patchwork of requirements; each state differs | Varies |
| EU AI Act | EU | N/A | AI-driven ad targeting new transparency rules | Tiered by risk level |

**Key 2025 milestone:** 19 distinct US state privacy laws took effect. Manual compliance is no longer feasible — automation and CMPs (Consent Management Platforms) required.

---

## Meta-Specific Compliance Requirements

### Tracking & Measurement
- **Pixel alone is insufficient** — must implement Conversions API (CAPI) alongside Pixel
- CAPI must be gated by user consent signals (fire only when consent granted)
- CAPI with consent mode: full data when opted in; privacy-preserving modeling when opted out
- Deduplication required: set `event_id` to prevent double-counting Pixel + CAPI events
- Privacy-Enhanced Match: hashes PII before sending to Meta

### Sensitive Categories — Active Restrictions

**Health & Wellness (US, EU, UK) — Effective January 2025**
- Mid/lower funnel events BLOCKED: Add to Cart, Purchase, Lead (for health-categorized sites)
- Must optimize on: Landing Page Views, Engagement, or TOF (top-of-funnel) events
- CAPI and server-side APIs: also restricted for blocked events
- Applies to: any site Meta categorizes as health-related (includes fitness, supplements, mental health)
- Work-arounds: Third-party analytics (Triple Whale, Northbeam) for BOF tracking; quiz/survey signals

**Financial Services (US) — Effective January 14, 2025**
- New mandatory Special Ad Category: "Financial Products and Services"
- Requires regulatory authorization proof (SEC registration for investments, etc.)
- Restricted targeting: Cannot use certain interest/behavioral data
- Key events like Purchase and Lead blocked for financial domains
- CAPI restricted for financial domains
- Ad copy must include: clear fees, terms, APRs; no misleading claims
- Landing pages: must load <3 seconds, display privacy policy + terms of service
- Cannot directly request sensitive info (bank account/routing numbers) in ads

**Political Advertising**
- "Paid for by" disclaimer required (verified)
- Tighter targeting restrictions; some behavioral data not available
- Stricter ad review process
- 2025 change: Updated political ad disclaimer requirements

**Housing, Employment, Credit (Special Ad Categories)**
- Demographic targeting restrictions (cannot target/exclude by age, gender, zip code)
- Must declare Special Ad Category before launching
- Reduced audience targeting options

**Lookalike Restrictions (Sept 2025)**
- Health and finance data cannot be used to seed lookalike audiences
- Impact: Custom audiences based on health-related site visitors restricted
- Action: Build first-party email/CRM-based seeds instead

### Custom Audience Compliance (from March 2025)
- Advertisers must certify first-party data complies with privacy and anti-discrimination guidelines
- Custom audience uploads require documentation of data source and consent
- Data with sensitive attributes (health terms, financial signals) is blocked from custom audiences

---

## Google Ads Compliance Requirements

### Privacy & Targeting
- Healthcare, financial services, political: restricted targeting options (same direction as Meta)
- Brand safety: mandatory for regulated industries; use DoubleVerify/IAS exclusion lists
- Placement reports: review Search Partner Network placements for brand safety

### Cookie & Tracking
- Google Consent Mode v2 required for EEA advertisers (2024 deadline — still enforce)
- First-party data (Customer Match) more important as third-party cookies erode
- Enhanced Conversions: hash PII before sending to Google for conversion matching

---

## Apple iOS & ATT (Ongoing)

- ATT (App Tracking Transparency) opt-in rate: ~30–40% globally (varies by app)
- Impact: Reduced signal for Meta web/app campaigns; still ongoing
- SKAdNetwork (SKAN): Apple's privacy-preserving attribution; limited data
- Response: Meta's CAPI + AEM fills some gaps; Google's first-party data stronger here

---

## Compliance Audit Checklist

### Meta Account Audit
- [ ] Pixel + CAPI dual setup implemented
- [ ] Consent signals flowing correctly to CAPI
- [ ] Events Manager shows correct data categorization (not flagged as sensitive)
- [ ] No PHI (Personal Health Information) in pixel events
- [ ] Custom audience upload documentation ready
- [ ] "Do Not Sell" opt-out mechanism on website (for US)
- [ ] Privacy policy URL active and accurate (required for Lead Ads)
- [ ] Special Ad Categories declared where required (financial, political, housing)
- [ ] Political ads have "Paid for by" disclaimer

### Google Ads Account Audit
- [ ] Google Consent Mode v2 implemented (EEA accounts)
- [ ] Enhanced Conversions set up for web
- [ ] Customer Match consent documented
- [ ] Brand Safety exclusion lists applied
- [ ] Healthcare/financial: placement exclusions for sensitive sites
- [ ] Remarketing lists: confirm users gave consent for tracking

---

## Risk Assessment by Vertical

| Vertical | Risk Level | Primary Concern | Key Action |
|---|---|---|---|
| Healthcare / Wellness | 🔴 Critical | Event blocking, HIPAA adjacent | Audit pixel, switch to TOF optimization |
| Financial Services | 🔴 Critical | New Special Ad Category, event blocking | Declare category, get authorization proof |
| Political | 🔴 Critical | Disclaimer, targeting restrictions | Verify "Paid for by," check targeting rules |
| Legal Services | 🟡 High | Special ad category potential | Monitor for reclassification |
| Real Estate | 🟡 High | Housing Special Ad Category | Use SAC, remove demographic targeting |
| E-commerce (general) | 🟢 Medium | CCPA opt-out, data minimization | Add "Do Not Sell" link, audit pixel |
| B2B / SaaS | 🟢 Low-Medium | GDPR consent for EU traffic | Consent Mode, first-party data strategy |

---

## Staying Current

- Meta Transparency Center: https://transparency.fb.com/ (policy changes)
- Meta Business Help: https://www.facebook.com/business/help (policy guides)
- Google Ads policies: https://support.google.com/adspolicy/
- IAPP (International Association of Privacy Professionals): https://iapp.org
- OneTrust / CookiePro blog: compliance tool vendors with up-to-date guides
