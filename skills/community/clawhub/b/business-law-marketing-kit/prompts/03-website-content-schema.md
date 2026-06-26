# Prompt 3: Website Content & Schema
## Business Law & Contracts — Nevada Compliance Version

**Use this prompt to generate:** Practice area pages, attorney bio, FAQ content, and JSON-LD schema markup for Nevada business law and contracts attorneys.

---

## PROMPT

```
You are a Nevada business law website content specialist. Generate compliant website content and schema markup for the following firm:

FIRM NAME: [Firm Name]
LEAD ATTORNEY: [Attorney Name], NV Bar No. [Number], [Year licensed]
LOCATION: [City, NV — address]
PHONE: [Phone number]
WEBSITE: [URL]
PRACTICE AREAS: [Select from: Business Formation, Contract Law, Employment Agreements, Non-Competes, Commercial Litigation, Business Acquisitions, Startup Law, Commercial Leases, IP Protection]
FLAT FEE MENU: [List any flat-fee services with pricing — triggers RPC 1.5 scope disclosure]
BAR ADMISSIONS: Nevada State Bar No. [Number] | [Any other bars]
LINKEDIN: [URL]

GENERATE:

---

SECTION A: PRACTICE AREA PAGES

Generate full content for 4 practice area pages (750–1,000 words each):

PAGE 1: Nevada LLC & Business Formation

H1: Nevada Business Formation Attorney — LLC, Corporation & Entity Setup
Meta description (155 chars): [Nevada business formation attorney. LLC, S-Corp, C-Corp entity setup in Las Vegas and Clark County. Fee agreement in writing. This is an advertisement.]

CONTENT REQUIREMENTS:
- Explain Nevada LLC (NRS Chapter 86): advantages (no state income tax on pass-through entities, no franchise tax, strong charging order protection under NRS 86.401), honest limitations (Nevada Modified Business Tax on payrolls over $50K/quarter, annual list $150, registered agent required)
- S-Corp election: IRS Form 2553, limitations on number/type of shareholders, Nevada implications
- C-Corp: Nevada Corporation (NRS Chapter 78), appropriate for VC-backed startups, Delaware comparison (note Delaware Court of Chancery advantage for VC-backed companies — do NOT falsely claim Nevada is always superior)
- Series LLC (NRS 86.296): what it is, appropriate uses, HONEST caveat that asset protection between series is not tested in federal bankruptcy and may not be recognized in all states where the LLC does business
- Operating agreement importance: why it's more important than the formation documents
- Flat fee pricing table: MUST disclose what's included and what's not (state filing fees $75–$425, registered agent $50–$200/year, annual list $150, county business license ~$200)
- Written fee agreement: note that RPC 1.5(b) requires written fee agreement provided before or promptly after engagement begins

COMPLIANCE GATES:
[ ] No "bulletproof asset protection" language
[ ] Nevada Modified Business Tax disclosed for payrolls over $50K/quarter
[ ] Annual list and registered agent costs disclosed
[ ] Delaware C-Corp advantage for VC-backed startups accurately acknowledged
[ ] Series LLC limitations honestly described
[ ] "This is an advertisement." at page footer
[ ] No "Nevada's top business formation attorney" (specialization claim)

---

PAGE 2: Contract Drafting & Review

H1: Nevada Contract Attorney — Drafting, Review & Commercial Agreements
Meta description (155 chars): [Nevada contract attorney. Business contract drafting and review in Las Vegas. Non-compete compliance with Nevada's 2021 reform. This is an advertisement.]

CONTENT REQUIREMENTS:
- What business contract review covers: contract language analysis, indemnification and liability caps, governing law and dispute resolution, ambiguous terms, missing protections
- Common contract types in Nevada business: vendor agreements, service agreements, commercial leases, joint ventures, asset purchase agreements, NDA/confidentiality
- Non-compete agreements: FULL NRS 613.195 disclosure section
  - Void for hourly employees (NRS 613.195(4))
  - Nevada choice-of-law required for Nevada employees
  - Must protect a legitimate business interest
  - Reasonable in scope (geographic area, duration, restricted activities)
  - 2021 reform: liquidated damages provision alternative
  - Cannot be used as general "non-compete with the world" clauses
  - Nevada courts scrutinize — enforce with caution
- Employment agreements: offer letters vs. employment contracts, at-will presumption in Nevada (NRS 613.010), executive agreements, bonus/equity provisions
- Online templates vs. attorney drafting: factual comparison — templates are not legal advice, do not protect attorney-client privilege, do not account for Nevada-specific requirements
- Written scope and fee disclosure: scope of review will be set forth in engagement letter before work begins

COMPLIANCE GATES:
[ ] Non-compete hourly employee prohibition disclosed (NRS 613.195(4))
[ ] Nevada choice-of-law requirement for Nevada employees disclosed
[ ] No "ironclad" or "enforceable anywhere" non-compete promises
[ ] Contract enforceability characterized as fact-specific, not guaranteed
[ ] "This is an advertisement." at page footer
[ ] Flat fee scope disclosed if applicable

---

PAGE 3: Commercial Litigation & Business Disputes

H1: Nevada Business Dispute Attorney — Commercial Litigation & Contract Claims
Meta description (155 chars): [Nevada business dispute attorney. Commercial litigation, breach of contract, and business claims in Las Vegas. This is an advertisement.]

CONTENT REQUIREMENTS:
- Types of business disputes handled: breach of contract, partnership disputes, vendor disputes, non-compete enforcement, commercial lease disputes, business acquisition disputes, shareholder disputes
- Nevada District Court (Eighth Judicial District) and Nevada Supreme Court: what business litigants should know
- Alternative dispute resolution in Nevada: mediation under NRS 38.010 et seq., arbitration (AAA Commercial Rules), Nevada's mandatory mediation requirement in some commercial cases
- What to bring to a business dispute consultation: contract documents, correspondence, financial records, timeline of events
- Business dispute assessment process: case evaluation, remedies available (damages, injunctive relief, specific performance), litigation vs. ADR recommendation
- HONEST litigation characterization: outcomes depend on facts, evidence, judicial assignment, and applicable law — no outcome guarantees
- Litigation timeline: what to expect in Clark County business litigation (initial filing, discovery, motion practice, trial or settlement)

COMPLIANCE GATES:
[ ] No "we'll win your business case" language
[ ] No "we'll recover your money" promises
[ ] Litigation outcomes described as fact-dependent
[ ] ADR alternatives honestly presented as potentially faster/cheaper
[ ] "This is an advertisement." at page footer
[ ] No case result statistics without atypical-result FTC disclaimers

---

PAGE 4: Startup Law & Business Capital

H1: Nevada Startup Attorney — Business Formation, Founder Agreements & Investor Compliance
Meta description (155 chars): [Nevada startup attorney. Business formation, founder agreements, and Reg D investor compliance in Las Vegas. This is an advertisement.]

CONTENT REQUIREMENTS:
- Nevada startup ecosystem: Las Vegas Innovation District, tech and hospitality-tech startups, Nevada Gaming Control Board licensing for tech companies in gaming-adjacent spaces
- Startup legal checklist: entity formation, IP assignment (founders assign all IP to company before funding), vesting schedule for equity, employment agreements, NDA for all parties, SAFE notes vs. priced rounds
- Raising money from investors: FULL SEC Reg D disclosure
  - Federal securities law applies to all investment offerings regardless of state
  - Rule 506(b): up to 35 non-accredited investors, no general solicitation, Form D filing required
  - Rule 506(c): accredited investors only, general solicitation permitted (LinkedIn posts, email blasts OK), mandatory accredited investor verification
  - Form D: must be filed within 15 days of first sale
  - Nevada intrastate exemption (NRS 90.530(11)): narrow — all purchasers must be Nevada residents; does NOT exempt from federal law when out-of-state purchasers are involved
  - Regulation Crowdfunding (Reg CF): up to $5M/year, registered crowdfunding portal required, Form C filing
- Equity-for-fees (startup attorney engagement): if firm offers equity arrangements, FULL RPC 1.8(a) disclosure:
  - Transaction disclosed in writing and fair to client
  - Client advised to seek independent counsel
  - Written informed consent required
  - This is a material business transaction with the client — not a simple fee alternative

COMPLIANCE GATES:
[ ] Reg D (Rule 506(b) and 506(c)) accurately described
[ ] Nevada intrastate exemption accurately scoped (not a Reg D substitute)
[ ] RPC 1.8(a) equity-for-fees process fully disclosed if applicable
[ ] No "we'll help you raise $X" outcome promises
[ ] No "guaranteed Reg D compliance" language
[ ] "This is an advertisement." at page footer

---

SECTION B: ATTORNEY BIO

Generate a 400-word attorney bio for [Attorney Name] that:
- Opens with professional credential statement (NV Bar No. [Number], licensed [Year])
- Describes practice focus: business law, contracts, and [specific areas]
- Includes any Nevada-relevant credentials or bar section memberships (Nevada State Bar Business Law Section, Las Vegas Metro Chamber of Commerce, SCORE Las Vegas mentor if applicable)
- COMPLIANCE: No "best," "top," "premier," or "specialist" designations without Nevada State Bar certification backing
- COMPLIANCE: No case result claims without FTC atypical-result disclaimer
- Closes with: "[Attorney Name] is licensed to practice law in Nevada (NV Bar No. [Number]). This biography is for informational purposes only. Past results do not guarantee future outcomes. Attorney advertising."

---

SECTION C: FAQ SCHEMA CONTENT

Generate 8 Q&A pairs for FAQ schema (answering the questions Nevada business owners actually search for):

Q1: How much does it cost to form an LLC in Nevada?
A: [Accurate answer: Attorney fees vary by firm (get a written fee agreement before engaging). State filing fees: $75 online or $425 for 24-hour expedited filing. Annual list fee: $150/year. Registered agent: $50–$200/year. Clark County business license: approximately $200. Nevada Modified Business Tax applies to payrolls over $50,000 per quarter. Total first-year cost for a simple Nevada LLC typically ranges from $500–$1,500+ depending on attorney fees, service speed, and county business license. Contact [Firm Name] for a specific fee quote — fee agreement provided in writing before work begins. This is an advertisement.]

Q2: Are non-compete agreements enforceable in Nevada?
A: [Accurate answer referencing NRS 613.195: Non-competes are unenforceable for hourly employees (NRS 613.195(4)). For other employees, enforceability depends on: (1) valuable consideration, (2) legitimate business interest, (3) reasonable scope (geographic area, duration, restricted activity), and (4) Nevada choice-of-law clause for Nevada employees. Nevada courts scrutinize non-competes. The 2021 reform (AB 136) significantly changed Nevada non-compete law — consult a Nevada attorney for your specific situation. This is an advertisement.]

Q3: What is a Series LLC in Nevada?
A: [Accurate answer: Nevada allows Series LLCs (NRS 86.296) where separate cells can have distinct assets, members, and liabilities. Potential use cases include real estate investors holding multiple properties. Important limitation: the liability shield between series is untested in federal bankruptcy court and may not be recognized in other states where the LLC does business. Series LLCs require careful drafting and maintenance to preserve the liability separation. Consult a Nevada attorney about whether a Series LLC is appropriate for your specific situation. This is an advertisement.]

Q4: What is the Nevada Modified Business Tax?
A: [Accurate answer: The Nevada Modified Business Tax (NRS 363B) applies to employers with taxable wages exceeding $50,000 per quarter. The rate is 1.378% on wages above the threshold for most businesses (financial institutions: 2.0%). Nevada LLCs and corporations with significant payroll may owe this tax. It is separate from personal income tax (Nevada has no state income tax on individuals or pass-through business income). Consult a CPA and business attorney to understand your Nevada tax obligations. This is an advertisement.]

Q5: What does a business attorney do in a contract dispute?
A: [Accurate answer: A Nevada business attorney helps evaluate the contract terms, assess the strength of your position, negotiate with the opposing party, and — if resolution fails — pursue or defend litigation or arbitration. What an attorney cannot do: guarantee the outcome of a dispute. Results depend on the specific contract language, the facts of the dispute, applicable Nevada law, and the forum (court or arbitration). Early involvement (before a dispute escalates) typically provides more options. This is an advertisement.]

Q6: What is the difference between Rule 506(b) and Rule 506(c) for Nevada businesses raising investment?
A: [Accurate answer: Both are Reg D exemptions from SEC registration for private offerings. Rule 506(b): no general solicitation (cannot advertise the offering publicly), up to 35 non-accredited investors allowed (all must receive disclosure), unlimited accredited investors. Rule 506(c): general solicitation permitted (LinkedIn, email blasts OK), but ALL investors must be accredited and the company must take reasonable steps to verify accredited status. Both require Form D filing within 15 days of first sale. Consult a securities attorney before offering securities to investors — Nevada law alone does not exempt you from federal requirements. This is an advertisement.]

Q7: Do I need a lawyer to form an LLC in Nevada?
A: [Balanced answer: Nevada law does not require an attorney to form an LLC — you can file directly with the Nevada Secretary of State. Online services (LegalZoom, Incfile, Northwest) provide document preparation. However, document preparation services are not attorneys and cannot give legal advice, draft a legally sound operating agreement, advise on entity selection based on your specific situation, or represent you if a dispute arises. Attorney-client privilege protects communications with your attorney — not communications with a document preparation service. Whether to engage an attorney depends on the complexity of your business structure and goals. This is an advertisement.]

Q8: What is RPC 1.5 and how does it affect attorney fees?
A: [Audience-appropriate answer: Nevada RPC 1.5(b) requires that a business attorney communicate the basis or rate of fees to you in writing before or promptly after beginning representation. This means you should receive a written fee agreement (also called an engagement letter) before your attorney starts work on your matter. The fee agreement should describe: what services are included, the fee amount or rate, any services that are excluded, and billing and payment terms. If a business attorney does not provide a written fee agreement, ask for one. This is an advertisement.]

---

SECTION D: JSON-LD SCHEMA MARKUP

Generate JSON-LD schema for:

1. LocalBusiness / LegalService schema:
```json
{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "name": "[Firm Name]",
  "description": "[150-char description — no outcome promises, no specialization claims]",
  "url": "[Website URL]",
  "telephone": "[Phone]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "NV",
    "postalCode": "[Zip]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Lat]",
    "longitude": "[Long]"
  },
  "openingHours": "[Mo-Fr 09:00-17:00]",
  "priceRange": "$$",
  "areaServed": ["Las Vegas", "Henderson", "North Las Vegas", "Clark County", "Nevada"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Business Law Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Nevada LLC Formation"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Business Contract Review"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Commercial Litigation"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Employment Agreements"}}
    ]
  }
}
```

2. FAQPage schema (using Q&A pairs from Section C):
[Generate FAQPage JSON-LD using the 8 Q&A pairs from Section C. Each Q&A as an acceptedAnswer.]

3. Person schema for attorney bio:
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[Attorney Name]",
  "jobTitle": "Attorney at Law",
  "worksFor": {"@type": "Organization", "name": "[Firm Name]"},
  "alumniOf": [{"@type": "EducationalOrganization", "name": "[Law School]"}],
  "knowsAbout": ["Nevada Business Law", "Contract Law", "LLC Formation", "Commercial Litigation"],
  "sameAs": ["[LinkedIn URL]", "[Nevada State Bar profile URL]"]
}
```

COMPLIANCE NOTE: Schema markup is machine-readable metadata. It does not appear as visible text on the page but is indexed by search engines. Outcome claims in schema (e.g., "we win business cases") create the same RPC 7.1 exposure as visible page content. Schema descriptions must comply with the same standards as all attorney advertising.
```

---

## Output Format
- Practice area pages: full page content, H1, meta description, compliance gate checklist
- Attorney bio: complete 400-word bio
- FAQ: 8 complete Q&A pairs
- JSON-LD: three schema blocks, ready to paste into site header
- All outputs include inline compliance markers [GATE: PASS] or [GATE: FLAG — reason]
