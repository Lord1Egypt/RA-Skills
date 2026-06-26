# Nevada C-Corp — State Reference

## Governing Law
Nevada Revised Statutes (NRS) Chapter 78 — Private Corporations

## Filing

### Where to File
- **Online:** [Nevada SilverFlume](https://www.nvsilverflume.gov/home)
- **Agency:** Nevada Secretary of State

### SilverFlume Step-by-Step (Battle-Tested March 2026)

**Phase 1: Account + Articles**
1. Create account at nvsilverflume.gov (use company email)
2. Dashboard → Business Formations → Domestic Entity Formation
3. Select "Articles of Incorporation - Domestic Corporation"
4. **Name:** Enter exact legal name including suffix (e.g., "Acme Corp, Inc.")
5. **Registered Agent:** Select "entity" type, enter full RA name, pick exact match, verify it shows as **"commercial"** registered agent
6. **Stock Value:** Enter authorized shares, par value, and classes per your Articles
7. **Officer Information:** Add directors and officers. **IMPORTANT: The dropdown only has President, Director, Secretary, Treasurer — NO CEO or Chairman option.** Map CEO → President. Chairman → Director. The Organizational Resolutions govern actual titles.
8. **Business Information:** Select appropriate industry codes
9. **Signature:** Sign as incorporator
10. **Supporting Documentation:** Upload signed Registered Agent Acceptance form (must have both RA signature and entity signature)
11. Submit — goes into checkout cart

**Phase 2: Initial List (Required — auto-added to cart)**
1. The Initial List of Officers/Directors is automatically queued after Articles
2. **Business License Exemption:** Select "No" (unless nonprofit or specific financial institution under NRS 76)
3. **Publicly Traded:** Select "No" for private corps
4. **Officers:** Add each person with their title. You'll need separate entries if one person holds multiple titles (e.g., add Alice Johnson as Director, then again as Secretary, then again as Treasurer)
5. **Addresses:** Can use registered agent address for all officers (keeps personal addresses private)
6. **Sign** as President (or principal officer)
7. Review and submit to cart

**Phase 3: Checkout + Payment**
1. Both filings appear in cart together
2. Pay by credit card (2.5% processing fee added by payment processor) or trust account (no fee)
3. After payment: documents available in Documents tab (may take hours if server issues)
4. Download and save: Filed Articles, Initial List, State Business License
5. Note your **NV Business ID** (Entity Number)

**Known Issues:**
- SilverFlume has intermittent server outages — if you get a 500 error or "failed to commit," your payment likely went through. Check email for confirmation and contact support@nvsilverflume.gov with your confirmation number.
- Documents may not appear immediately in the Documents tab after payment — give it up to 24 hours.
- The system sometimes shows "$0.00" for total paid even though your card was charged — the payment receipt PDF is your proof.

### Filing Fees (Updated March 2026)
| Item | Cost | When |
|------|------|------|
| Articles of Incorporation | $75 | At filing |
| Initial List of Officers/Directors | $150 | Within 30 days (bundled at filing) |
| State Business License | $500 | Bundled with Initial List |
| CC Processing Fee | 2.5% | If paying by credit card |
| Registered Agent (annual) | ~$100-150 | Annual |
| EIN | Free | After incorporation |
| **Total to incorporate** | **~$725-775 + CC fee** | |

### Annual Requirements
| Item | Cost | When |
|------|------|------|
| Annual List of Officers/Directors | ~$150 | Anniversary of incorporation |
| Business License Renewal | ~$500 | Anniversary of incorporation |
| Registered Agent | ~$100-150 | Annual |
| **Annual Total** | **~$750-800** | |

## EIN (Employer Identification Number)

### Online Application (Fastest)
- **URL:** https://sa.www4.irs.gov/modiein/individual/index.jsp
- Takes 5 minutes, EIN issued instantly
- **REQUIRES SSN or ITIN** of the responsible party
- Select: Corporation → Started a new business
- Enter: legal name, Nevada, date of incorporation, responsible party SSN

### Non-US Founders (No SSN/ITIN)
If the incorporator or CEO does not have a US SSN or ITIN:
- **Option 1 (recommended):** Have a US-based officer (e.g., CFO, Treasurer) apply as the responsible party using their SSN. This is standard practice — whoever applies becomes the "responsible party" on IRS records.
- **Option 2:** Call IRS international line at 267-941-1099 (Mon-Fri 6AM-11PM ET, not toll-free). They can process without SSN.
- **Option 3:** File Form SS-4 by fax to 855-641-6935. Takes ~4 business days.

**After getting EIN:** The responsible party can be changed later via Form 8822-B if needed.

## 83(b) Elections (CRITICAL for Stock-for-Services)

If issuing stock in exchange for services (common in startups), **every stockholder should file an 83(b) election within 30 days of stock issuance.** This is irrevocable and time-sensitive.

### Why It Matters
- **Without 83(b):** Stockholder is taxed on the fair market value of shares as they vest (could be millions if company grows)
- **With 83(b):** Stockholder is taxed on value at time of issuance (par value = essentially $0 for new companies)
- **Missing the 30-day deadline is irreversible** — no extensions, no exceptions

### Filing Process
1. Complete the 83(b) election form (see template in assets/)
2. Sign and date
3. Mail original to IRS Service Center via **certified mail, return receipt requested** (proof of timely filing)
4. Give copy to company Secretary
5. Keep copy for personal records
6. Attach copy to personal tax return for the year of issuance

### IRS Service Center Addresses
File at the IRS Service Center where the stockholder files their individual return:
- California: Fresno, CA 93888-0002
- Texas: Austin, TX 73301-0002
- Others: https://www.irs.gov/filing/where-to-file-addresses

## Key Nevada Advantages
- No state corporate income tax
- No franchise tax
- Strong director/officer liability protections (NRS 78.138)
- No requirement to disclose shareholders in public filings
- Broad indemnification allowed (NRS 78.7502)
- Shares can be issued for services rendered (NRS 78.211)

## Stock Rules
- **Consideration:** Cash, services, personal property, real estate, or any combination (NRS 78.211)
- **Par value:** Can be any amount, including fractional cents
- **No minimum capital** required to incorporate
- **Treasury shares:** Allowed under NRS 78.267
- **Vesting:** Standard for startups: 4-year vesting, 1-year cliff. Implemented via Restricted Stock Purchase Agreements (RSPAs). Unvested shares subject to repurchase at par value upon termination.

## Required Documents
1. Articles of Incorporation (filed with SOS)
2. Registered Agent Acceptance form (filed with Articles — needs both RA and entity signatures)
3. Initial List of Officers/Directors (filed within 30 days)
4. Bylaws (internal, not filed)
5. Organizational Resolutions (internal)
6. Stock Ledger (internal, must be maintained per NRS 78.105)
7. 83(b) Election forms (filed by each stockholder with IRS)
8. Restricted Stock Purchase Agreements (internal, signed by each stockholder)

## Post-Incorporation Deadlines
- **Immediately:** File Initial List + Business License at SilverFlume (bundled with Articles checkout)
- **Within 30 days of stock issuance:** All stockholders file 83(b) elections with IRS (CRITICAL)
- **After EIN obtained:** Open corporate bank account
- **If operating outside NV:** File for foreign qualification in operating state(s)

## Foreign Qualification
If the corporation operates in another state (e.g., Florida, Texas), it must register as a foreign corporation in that state. Typically requires:
- Certificate of Good Standing from Nevada
- Foreign qualification filing in target state
- Additional registered agent in that state
- Additional annual fees in that state

## Recommended Registered Agents
- **Northwest Registered Agent** — ~$125/yr, includes mail scanning, business address, fast response on acceptance forms
- **Nevada Registered Agent LLC** — ~$50/yr, NV-only, no-frills
- **ZenBusiness (Incfile)** — Free first year with formation, $119/yr renewal
