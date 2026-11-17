---
name: b2b-lead-research-agent
description: Build a qualified US B2B prospect list from public business sources - define your ICP, research target companies, score and deduplicate accounts, and draft personalized multi-touch outreach that a human reviews and sends. Consent-based research, CAN-SPAM and TCPA aware, no spam and no scraped personal data.
version: 1.0.5
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    envVars:
      - name: APOLLO_API_KEY
        required: false
        description: Optional. Licensed US company and contact data provider.
      - name: HUNTER_API_KEY
        required: false
        description: Optional. Email pattern and deliverability checks for business emails.
      - name: BRAVE_SEARCH_API_KEY
        required: false
        description: Optional. Web search API for company research.
      - name: TAVILY_API_KEY
        required: false
        description: Optional. Research and extraction API for company pages.
    emoji: "\u1F50D"
    homepage: https://github.com/rapidworker1
---

# B2B Lead Research Agent

**Turn "we should find more accounts like these" into a ranked, verified,
ready-to-work US prospect list** - and outreach copy that survives a spam filter
and a compliance review.

Use this skill when someone asks for:

- a target account list for a US B2B product or service
- company research: what a company does, who they sell to, recent triggers
- lead scoring, tiering, deduplication, and list hygiene
- ICP (ideal customer profile) definition from scratch
- cold email and LinkedIn outreach copy for US buyers
- territory/account planning, account selection, "why this account" briefs
- cleaning an existing list before sending

---

## Operating principles (non-negotiable)

1. **Company-level research from public business sources.** Official company
   websites, press releases, public filings, public registries, public job
   postings, public directory listings the company chose to publish.
2. **Business contact details published for business use.** A company contact
   page, a press contact, a business role address. Not scraped personal
   accounts, not leaked databases, not breach dumps, not bought lists.
3. **Human in the loop.** Research and drafting are automated. **Sending is
   manual** - the operator opens the draft, checks it, and sends it.
4. **One-to-one by default.** Bulk blast to a purchased list is out of scope.
5. **Opt-out always wins.** One click, forever, no questions asked.
6. **Respect the source.** No bypassing logins, no scraping behind a paywall or
   a blocklist, no ignoring robots.txt, no rate-limit evasion.

If a request needs any of these, say no to the request and offer the
compliant path instead.

---

## Workflow

1. **Define the ICP.** `templates/icp-worksheet.md` - firmographics, triggers,
   disqualifiers, and the two questions a rep must be able to answer.
2. **Discover accounts.** Public sources only, see
   `references/research-playbook.md`.
3. **Research each account.** One-page dossier: what they sell, who they sell
   to, size, funding/stock/leadership signals, a trigger, and one credible
   reason to contact them now.
4. **Normalize and score.** `scripts/lead_sheet.py` dedupes and tiers the list.
5. **Draft outreach.** `templates/outreach-sequence.md` - 4-touch, US business
   email, one clear ask, easy to say yes to.
6. **Compliance check.** `scripts/compliance_check.py` on every draft.
7. **Hand off for human review.** Delivered as a sheet + drafts, never as
   "send this to 5,000 people".

## Quickstart

**Score and tier a list:**

```bash
python3 scripts/lead_sheet.py \
  --accounts accounts.csv \
  --icp icp.json \
  --out scored.csv
```

`accounts.csv` needs `company,domain,employees,industry,state,country,notes`.
The script normalizes domains, removes duplicates, applies the ICP weights,
tiers accounts A/B/C, and prints a summary.

**Lint outreach drafts before sending:**

```bash
python3 scripts/compliance_check.py --drafts outreach/ --out compliance.json
```

It checks each draft for the CAN-SPAM elements (real from address, physical
postal address, working unsubscribe, non-deceptive subject line), plus
required statements, and reports a pass/fail per message.

---

## Output contract

Every research run delivers four artifacts:

| Artifact | Contents |
| --- | --- |
| **Scored sheet** | Company, domain, tier, score, size, industry, location, trigger, source URL, date researched |
| **Account dossiers** | One page per Tier A/B account: what they do, why they fit, the trigger, the hook, the ask |
| **Outreach drafts** | 4-touch sequence per Tier A account, each with a personalization note explaining the line used |
| **Compliance report** | Pass/fail per draft, plus the opt-out list and suppression notes |

Nothing else. No "complete contact database", no unverified email lists.

## Research standards for US accounts

- **Source every fact.** Store the URL and the date researched for each claim.
- **One page per account.** If it does not fit on a page, it is not research.
- **Find the trigger.** A hiring spree, a new VP of Sales, a funding round, a new product line, an expansion, a compliance deadline, a competitor change, a tech-stack change. No trigger, no email.
- **Write the personalization note.** The draft must say which line came from which fact. If you cannot point to it, cut the line.
- **Prefer recent, public, specific.** The newest press release beats the About page.

## Sources that work for US company research

| Source | What you get | Notes |
| --- | --- | --- |
| Company website + newsroom | Product, customers, leadership, pricing, US address | Primary source, always cite |
| Press release wire (Business Wire, PR Newswire public pages) | Funding, launches, events with dates | Public pages, read-only |
| SEC EDGAR | Public company financials, filings, S-1s, 8-Ks | Free, authoritative, see `references/enrichment-sources.md` |
| State Secretary of State registries | Legal entity, registered agent, status | Public, per state |
| Public job postings | Growth signals, tech stack, team shape | Public careers pages |
| SAM.gov / state procurement portals | Government and public-sector buyers | Public |
| Conference exhibitor lists | Who's actively buying in your category | Public PDFs and pages |
| Licensed providers (Apollo, ZoomInfo, Clay, HubSpot Breeze, LinkedIn Sales Navigator) | Bulk firmographics and business contacts | Licensed use, respect their terms |

## Guardrails (hard rules)

- **No scraped personal data.** No personal social profiles, no personal email
  guessing outside a company's published pattern, no data broker dumps, no
  breach or dump data, no "gmail + firstname.lastname" on private individuals.
- **No mass automated sending.** This skill never sends. Volume stays low
  enough that each message can be read by a human first.
- **No deceptive subjects.** No fake "Re:", no fake "Fwd:", no
  `FW:` padding, no misleading sender name, no look-alike domains.
- **No bought or scraped lists.** Business contacts from a company's own
  published channels, or from a provider the company is licensed to use.
- **No fake personalization.** Never claim a fact you did not verify, never
  invent a mutual connection.
- **No scraping against a site's terms or robots.txt.** No rate-limit evasion,
  no credential reuse, no circumvention of paywalls.
- **Opt-out suppression is permanent.** Keep a suppression list and check it
  before every send.

## Compliance essentials (US)

Full detail in `references/us-compliance.md`. The short version:

- **CAN-SPAM (commercial email):** truthful headers, non-deceptive subject,
  identify the message as an ad where required, physical postal address,
  working unsubscribe, honor unsubscribe within 10 business days.
- **TCPA (SMS and calls):** prior express written consent for marketing texts
  and automated calls. Do not treat a form fill as consent for texts unless it
  said so.
- **State laws:** California, Colorado, Virginia, Connecticut, Utah and others
  require opt-in rather than opt-out for some categories. Opt in everywhere
  unless counsel says otherwise.
- **Platform rules:** LinkedIn and major inboxes treat unsolicited automation
  as abuse and can ban the sending domain. Slow, low-volume, personalized.

## Files in this bundle

```
references/
  us-compliance.md        CAN-SPAM, TCPA, state laws, suppression list rules
  research-playbook.md    ICP definition, discovery, triggers, qualification
  enrichment-sources.md   Public and licensed US company data sources
templates/
  icp-worksheet.md        ICP definition sheet
  company-dossier.md      One-page account brief
  outreach-sequence.md    4-touch US outreach sequence
scripts/
  lead_sheet.py           Normalize, dedupe, ICP-score, tier a list
  compliance_check.py     CAN-SPAM / required-statement linter for drafts
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Low response rate | Weak trigger, not weak copy - fix the account selection |
| Contacts bounce | Verify the pattern against the company's published contact |
| Filters reject | Run `compliance_check.py`, slow the volume, fix the auth setup |
| Too few accounts | Loosen firmographics, not the disqualifiers |

## Related

- [`ai-creative-studio`](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) — turn each account's trigger into a hook, an ad, and a landing page.
- [`ai-trading`](https://clawhub.ai/rapidworker1/skills/ai-trading) — research public competitors of a target account before you pitch.
- **[Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite)** — one Windows kit that sets up research, content and outbound workflows side by side. The desktop app is a separate download from the publisher's GitHub release, with a published SHA-256 so you can check the file before you unpack it; no skill bundle carries an installer.

---

*Research and drafts only. Nothing in this skill sends anything, and nothing in
it bypasses a platform's rules. Sending stays a human decision, and it stays
compliant.*
