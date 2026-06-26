# Lead Sourcing Reference

Complete guide to defining your ICP, finding qualified leads, and importing clean data into your tracking sheet.

---

## ICP Definition Worksheet

Answer all six questions before sourcing a single lead. Vague ICPs produce vague results.

**1. What role feels the pain your offer solves?**
- Be specific: not "marketing person" but "Head of Growth" or "VP of Sales"
- Include seniority: decision-maker, influencer, or end-user?
- Example: *Director of Marketing at companies with an active sales team*

**2. What company size/stage is most likely to buy?**
- Headcount ranges: 1–10, 11–50, 51–200, 201–1000, 1000+
- Stage signals: bootstrapped, seed, Series A/B, enterprise
- Example: *10–50 employees, bootstrapped or seed-stage*

**3. What industry or vertical do you have the strongest proof in?**
- Lead with your best vertical first. Expand later.
- Example: *B2B SaaS, specifically productivity or sales tools*

**4. What geography are you targeting?**
- Start narrow: one country, then expand
- Consider timezone for reply timing
- Example: *US + Canada, English-speaking markets*

**5. What signals indicate they're ready to buy now?**
- Hiring signals: posting for SDR, BDR, outbound sales roles
- Funding signals: raised seed/Series A in last 6 months
- Tool signals: switched CRM, new product launch
- Example: *Currently hiring SDRs or BDRs (shows outbound intent)*

**6. What disqualifies a company immediately?**
- Too small (can't afford), too large (wrong buyer), wrong industry, competitor
- Example: *Fewer than 5 employees, or enterprise (500+ headcount)*

### Completed ICP Statement Template

> **Target:** [Role] at [Company Size] [Industry] companies in [Geography], showing [signal if applicable].
> **Disqualify if:** [exclusion criteria]

**Example:**
> **Target:** Head of Sales or VP Sales at 10–50 person B2B SaaS startups in the US, currently hiring SDRs.
> **Disqualify if:** fewer than 10 employees, non-software companies, or enterprises with 200+ headcount.

---

## Apollo.io Filter Guide

Apollo is the primary free-tier lead source. 75 verified export credits per month.

### Account setup
1. Sign up at apollo.io — free tier, no credit card required
2. Verify your email
3. Install the Chrome extension (optional — useful for LinkedIn enrichment)

### Building your search filter

Navigate to **Search → People**. Apply filters in this order:

| Filter | Setting | Notes |
|--------|---------|-------|
| **Job Titles** | Exact titles from your ICP | Use variations: "VP Sales," "Head of Sales," "Sales Director" |
| **Seniority** | Director, VP, C-Level | Match your ICP buyer level |
| **# Employees** | 10–50 (or your range) | "Company Headcount" filter |
| **Industry** | Software, SaaS, Technology | Use Apollo's predefined categories |
| **Location** | United States, Canada | "Person Location" not "Company Location" |
| **Email Status** | Verified | Filters to confirmed emails only — critical for deliverability |

### Exporting leads

1. Apply all filters. Review count (aim for 200–500 results minimum before exporting 75).
2. Click **Export → Export to CSV**
3. Select fields: First Name, Last Name, Email, Title, Company, Company Size, LinkedIn URL
4. Free tier: 75 exports/month. Use them on your best-filtered list.

### Saving your search

Save each filter set as a named search. Rotate filters monthly to get fresh leads from different segments.

---

## Hunter.io Domain Search

Use Hunter.io for two purposes: finding emails by domain, and verifying emails from other sources.

### Finding emails for a specific company

1. Go to hunter.io → Domain Search
2. Enter the company's domain (e.g., `acme.com`)
3. Hunter returns all known emails at that domain + confidence score
4. Filter to your target role using the department/title filters
5. Free tier: 25 searches/month

### Bulk email verification

If you have a list of emails from LinkedIn or other sources without verification:
1. Go to hunter.io → Email Verifier
2. Paste email addresses (or upload CSV)
3. Hunter returns: Valid, Risky, Invalid
4. Keep only Valid. Delete Invalid. Use Risky sparingly (manually review first).

### Integration with Google Sheets

Hunter has a Google Sheets add-on:
1. Install: Extensions → Add-ons → Get add-ons → search "Hunter"
2. Authenticate with your Hunter account
3. Use `=HUNTER_VERIFY(A2)` to check emails in bulk from your sheet

---

## LinkedIn Manual Sourcing (No Sales Navigator)

Manual LinkedIn sourcing is slow but free and unlimited. Use it to supplement Apollo exports.

### Search method

1. Use LinkedIn's standard People search
2. Apply filters: Location, Current Company Size (rough), Industry
3. Title keyword search: "VP Sales" OR "Head of Sales" OR "Sales Director"
4. Work through search results page by page (LinkedIn caps free users at ~100 results per search)

### Finding email from LinkedIn profile

Options (in order of reliability):
- **Apollo Chrome Extension** — install on Chrome, visit profile, extension surfaces email if known
- **Hunter Chrome Extension** — same as above
- **Contact info section** — some people list email directly on their profile
- **Company website pattern** — if company uses firstname@company.com pattern, extrapolate

### Recording your leads

Create a Google Sheet with columns:
`First Name | Last Name | Email | Title | Company | LinkedIn URL | Source | Email Status | Notes`

Fill manually as you find contacts. Mark Email Status as "unverified" until confirmed.

---

## Lead Scoring Rubric

When you have more leads than export credits, prioritize using this rubric. Higher score = export first.

| Signal | Points |
|--------|--------|
| Recent funding (last 6 months) | +3 |
| Actively hiring for your target role | +2 |
| Recent product launch or major announcement | +2 |
| Tech stack match (using relevant tool) | +1 |
| LinkedIn activity in last 30 days | +1 |
| Company in your strongest vertical | +1 |
| No clear signal | 0 |
| Competitor (known) | Disqualify |

Score each lead. Export highest scores first.

---

## Batch Import Checklist

Run every batch through this checklist before loading into your tracking sheet.

**Step 1: Verify**
- [ ] All emails have "Verified" or "Valid" status (Apollo or Hunter)
- [ ] No emails sourced more than 6 months ago (stale data)

**Step 2: Deduplicate**
- [ ] Cross-reference against your existing Leads tab (remove duplicates)
- [ ] Cross-reference against your Suppression tab (remove all suppressed emails)
- [ ] Remove anyone you've contacted in the last 90 days

**Step 3: Clean**
- [ ] Remove catch-all mailboxes: info@, hello@, contact@, admin@, support@
- [ ] Remove role-based addresses unless the role is your target (e.g., sales@ if targeting sales leaders)
- [ ] Check for obvious test data (test@, example.com)
- [ ] Verify company names are populated (blank company = low personalization potential)

**Step 4: Import**
- [ ] Set Status column to "new" for all new rows
- [ ] Set Source column (Apollo, Hunter, LinkedIn, etc.)
- [ ] Leave Notes blank (fill during outreach)
- [ ] Confirm row count matches your expected import

**Step 5: Confirm**
- [ ] New leads show in Leads tab with Status = "new"
- [ ] No overlap with Suppression tab
- [ ] Total lead count updated in your Stats tab
