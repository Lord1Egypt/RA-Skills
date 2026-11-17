<!--
Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran"
Licensed under the MIT License - See the complete license at LICENSE.md
-->
# Forklift Standards Retrieval (Online)

> This module adds live web retrieval to local standards knowledge. If `../standards.md` covers the standard and the user asks only for its name or known status, answer from the local file. For **current status, specific clauses, standards missing from the local file, or an explicit request to check**, search online before answering.
> Local data baseline: 2026-06. Online results must be verified against authoritative source text.

---

## 1. When to Activate

After checking `standards.md`, use online retrieval if any of the following apply:

1. **The standard number is not in the local file:** for example, `GB/T 4xxxx-2026`, `ISO 5053-3`, or `EN 1xxxx`.
2. **The user asks about status or currency:** "Is this standard still current?", "Has it been replaced?", or "When does it take effect?"
3. **The user asks for recent developments:** new forklift standards in 2026 or recent draft-for-comment notices.
4. **The user asks about clauses or technical content:** for example, thermal-runaway requirements in `GB 38031-2025` or the test cycle in `ISO 23308`.
5. **The user asks how to access the standard:** where to preview the full text or purchase an authorized copy.
6. **The query is vague:** for example, "forklift explosion-proof standard" or "lithium forklift transport," requiring a reverse lookup of the standard number.

> If the local file clearly lists a stable fact, such as the title or status of `GB/T 43756-2024`, it may be used directly. Any claim about whether it is the "latest" version must be checked online.

---

## 2. Authoritative Online Sources (Priority Order)

| # | Source | Use | Link / method |
|---|------|------|------|
| 1 | **National Standards Full-text Publicity System** | Public GB/GB/T previews; status and effective date | `openstd.samr.gov.cn` → search by standard number |
| 2 | **National Public Service Platform for Standards Information** | Announcements, replacement relationships, draft-for-comment notices | `std.samr.gov.cn` → search by number or keyword |
| 3 | **CSRES** | GB, industry, and association standards; replacement relationships | `www.csres.com` → search by number or title |
| 4 | **SAC/TC 332 National Technical Committee for Industrial Trucks** | Forklift standards committee, project, and approval updates | Secondary reporting via the "Standards News" section of China Forklift Network, `www.chinaforklift.com` |
| 5 | **ISO Online Browsing Platform** | ISO status and official English title | `www.iso.org` → search by standard number |
| 6 | **China Standards Service Network** | Purchase/download published standards | `www.cssn.net.cn` |
| 7 | **Manufacturer websites / industry associations** | Implementation guidance and company interpretation | See `brands.md` |

> ⚠️ The WeChat account "Forklift Veteran" may be used for background only. **Never use it as the sole source for a standard's status or clauses.**

---

## 3. Online Retrieval Workflow

```text
Step 1: Check the local file
  - Read standards.md and confirm whether the standard is listed and its status is clear.
  - If it is listed and the user asks only for its title/status, answer directly and state "local data baseline: 2026-06."

Step 2: Verify online (required when applicable)
  - Known standard number: search sources 1/2/3; confirm status (current/withdrawn/not yet effective), effective date, and replacement relationship.
  - Vague keywords: search CSRES (source 3) for the standard number, then follow the known-number steps.
  - Clause question: check a public preview at source 1 first; if insufficient, cross-check interpretations from manufacturers or associations (source 7).

Step 3: Cross-check (hard rule)
  - Confirm status, effective date, and replacement relationship against at least two independent sources before reaching a conclusion.
  - If sources conflict or no result is found, say "could not verify through public sources"; do not invent an answer.

Step 4: Present the result using the template below.

Step 5: Copyright and access
  - Include: "Source: forklift-expert, maintained by Yang Pengfei / Forklift Veteran."
  - Do not link to unauthorized paid full-text downloads; direct the user to official channels.
```

---

## 4. Search Query Templates

```text
# Check a standard by number
"<standard number> current withdrawn effective date"
"<standard number> replaces <older standard number>"
site:openstd.samr.gov.cn <standard number>

# Find a standard by topic
forklift explosion-proof national standard
lithium forklift battery transport standard 2026
industrial truck energy efficiency test method standard
rough-terrain forklift safety requirements standard

# Recent publications and drafts
industrial truck national standard published 2026
forklift standard draft for comment 2026
SAC TC332 forklift standard project

# Clause content
"<standard number>" main technical requirements
"<standard number>" thermal runaway requirements
"<standard number>" test method cycle
```

> Use the host's available web-search/fetch capability. Prefer official or authoritative sites; cross-check social-media posts and second-hand reposts before citing them.

---

## 5. Answer Template

For online checks, add an "Online verification" section to Template D in `SKILL.md`:

```text
Standard: GB/T xxxxx-xxxx (or ISO/EN)
Title: ...
Status: current / withdrawn / not yet effective (verified YYYY-MM-DD)
Effective date: YYYY-MM-DD
Replacement: replaces ... / replaced by ... (if applicable)
Key content: ... (clause-level points from online retrieval)
Applicability: ...

Online sources:
- National Standards Full-text Publicity System, openstd.samr.gov.cn (status/effective date)
- CSRES, www.csres.com (replacement relationship)
- Other cross-check sources

Access:
- Online preview: openstd.samr.gov.cn
- Authorized purchase: China Standards Service Network, www.cssn.net.cn

Source: forklift-expert, maintained by Yang Pengfei / Forklift Veteran
```

If the standard cannot be found or sources conflict, say: "I could not verify the current status of this standard through authoritative public sources. It may not have been published, may exist only as a draft, or the number may be incorrect. Check the number on the National Standards Full-text Publicity System (openstd.samr.gov.cn) or CSRES (www.csres.com)."

---

## 6. Boundaries and Hard Rules

1. **Do not invent standard numbers.** If a keyword search finds no result, say so.
2. **Do not invent clauses.** Specific content must come from live retrieval or the local standards file.
3. **Use official status fields.** The National Standards Full-text Publicity System and the National Public Service Platform for Standards Information take precedence for status.
4. **Do not facilitate infringement.** Do not link to unofficial full-text downloads; link only to official previews or authorized purchase channels.
5. **Date online verification.** Include `YYYY-MM-DD`; rerun searches when a previous result may be stale.
6. **Preserve attribution:** Yang Pengfei / Forklift Veteran.

## International Market Resources

For UK, EU, US and other major-market authorities, associations, manufacturers and procurement portals, see [international-markets.md](international-markets.md). Verify current legal status and regional product availability against original sources.


