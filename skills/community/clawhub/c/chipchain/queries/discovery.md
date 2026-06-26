# Unknown Supplier Discovery Workflow

> Step 1: Define the search target | Step 2: Search by material (2a-2g) | Step 3: Collect and deduplicate | Step 4: The delta is the discovery | Step 5: Update the investigation | When to use this workflow

**Question pattern:** "Who else makes X?" / "Are there suppliers we're missing?" /
"Find companies in segment Y that aren't in our database."

This workflow inverts the normal investigation flow. Instead of starting with a
company name and verifying it, you start with a material or technology and search
databases that are organized by WHAT, not WHO. Every company name that comes back
gets checked against the entity files. The ones that aren't listed are the discoveries.

## Step 1: Define the search target

Pick the identifiers you have for the material/technology. The more you have, the
more databases you can query.

| Identifier | Example | Where to find it |
|---|---|---|
| Material name (EN) | Photoacid generator | Chemistry knowledge |
| Material name (native script) | 光酸発生剤 (JA), 광산발생제 (KR), 光酸产生剂 (CN) | Lexicon files |
| CAS number | 89452-37-9 (triphenylsulfonium triflate) | chemistry/precursor-chains.md, PubChem |
| CPC/IPC patent class | G03F 7/004 | academia/patents-guide.md, Google Patents |
| HS code | 2904, 3707 | trade/hs-codes.md |
| SEMICON product category | "Photoresist Materials" | semi.org exhibitor directory |

If you only have the material name, start there. You can discover the CAS, CPC,
and HS codes during the search.

## Step 2: Search by material, not by company

Run these searches in parallel. Each one returns company names you might not know.

### 2a. Chemical registration databases

Search by CAS number. These are registries where companies must register to
manufacture or import a chemical. The database gives you the companies.

```
# ECHA (EU) — search by CAS, returns all registered manufacturers/importers
WebSearch: site:echa.europa.eu "[CAS number]"
→ Look for "Registration" tab → "Registrants" list

# K-REACH (Korea) — Korean chemical registration
WebSearch: "[CAS number]" site:kreachportal.me OR "K-REACH" "[material name KR]" 등록
→ Registered manufacturers/importers in Korea

# EPA CDR (US) — Chemical Data Reporting
WebSearch: "[CAS number]" site:epa.gov "chemical data reporting"
→ US manufacturers and importers

# CSCL (Japan) — Chemical Substances Control Law
WebSearch: "[CAS number]" 化審法 製造者
→ Japanese manufacturers
```

### 2b. Patent landscape by technology class

Search CPC/IPC codes with NO assignee filter. Every assignee is a potential player.

```
# Google Patents — broad landscape
CPC:[code] published:2020-2025
→ Sort by "most recent" → list all unique assignees
→ Filter out universities (unless co-assigned with a company)

# Lens.org — better for aggregating assignees
classification_cpc:[code] AND year_published:[2020 TO 2025]
→ Use "Assignee" facet to see all companies

# Country-specific patent offices for deeper coverage
KIPRIS: [Korean material term] in title/abstract, no assignee filter
J-PlatPat: [Japanese material term], classification [code]
CNIPA: [Chinese material term], IPC [code]
```

### 2c. SEMICON exhibitor directories

SEMI.org maintains categorized lists for every SEMICON show. Browse by product
category, not by company name.

```
WebSearch: site:semi.org "SEMICON [Japan/Korea/China/West]" exhibitor "[product category]"
WebSearch: "SEMICON [show]" exhibitor list "[material or equipment type]"
→ Every company in the category is a potential supplier
→ Pay attention to small/unknown exhibitors, not the big names you already know
```

### 2d. Filing keyword search (reverse direction)

Instead of searching one company's filing, search ALL filings for the material.

```
# Korean (DART full-text)
WebSearch: "[material name KR]" site:dart.fss.or.kr
→ Returns filings from ANY company that mentions this material

# Japanese (EDINET via web)
WebSearch: "[material name JA]" 有価証券報告書 事業の内容
→ Companies that describe this material in their business section

# Chinese (cninfo full-text)
WebSearch: "[material name CN]" site:cninfo.com.cn 招股说明书
→ IPO prospectuses mentioning this material in product descriptions

# Taiwan (MOPS)
WebSearch: "[material name TW]" 年報 主要產品
→ Annual reports listing this as a product
```

### 2e. Trade data gaps

Query Comtrade for bilateral flows at the HS code level. Compare the flow volume
to what known suppliers could account for.

```
# UN Comtrade
HS [code], reporter=[importing country], partner=all, year=2023-2025
→ If total imports = $100M but known suppliers account for only $60M,
   the $40M gap suggests unknown suppliers

# Look for unexpected origin countries
→ If you only know Japanese and Korean suppliers but see $15M from Germany,
   there's a German supplier you haven't identified
```

### 2f. Competitor sections in annual reports

Known companies list their competitors in their own filings.

```
# Japanese
WebSearch: "[known company JA]" 有価証券報告書 "競合" OR "競争"
→ Look for 競合先, 競争環境, 競合他社

# Korean
WebSearch: "[known company KR]" 사업보고서 "경쟁" OR "경쟁사"
→ Look for 경쟁현황, 경쟁업체

# Chinese
WebSearch: "[known company CN]" 年报 "竞争" OR "竞争对手"
→ Look for 竞争格局, 主要竞争对手

# Chinese — Taiwan
WebSearch: "[known company TW]" 年報 "競爭"
→ Look for 競爭對手, 競爭概況
```

### 2g. Academic literature by material

Search Google Scholar for the material/technology without filtering by company.
Author affiliations reveal who's active.

```
Google Scholar: "[material name]" AND (semiconductor OR "advanced node" OR fab)
Google Scholar: "[material name JA/KR/CN]" 半導体
→ Collect ALL author affiliations
→ Filter: which affiliations are companies vs universities?
```

#### How to interpret Google Scholar results

Author affiliations are the signal, but they need interpretation:

**Company affiliation = direct commercial signal.**
An author at "Toyo Gosei Co., Ltd." or "東洋合成工業 開発部" is doing commercial
R&D. This company is active in the space.

**University-only affiliation = academic, not supply chain (usually).**
But check for two exceptions:
- **Co-authors from a company you don't recognize.** A paper with authors from
  "Seoul National University" AND "XYZ Chemical Co." means XYZ is funding or
  collaborating on that research. XYZ is your discovery lead.
- **CAS institute spinoffs (China).** An author at 中科院化学研究所 (CAS Institute
  of Chemistry) working on photoresist may be connected to a startup. Search
  for the lead author's name + 创业 (startup) or 公司 (company).

**Division names matter.**
"Samsung SDI R&D Center" working on PAGs is different from "Samsung Electronics
Semiconductor Division." The division tells you how close to production they are.

**Publication frequency = investment signal.**
One paper 5 years ago = explored and moved on. 10+ papers over 3 years = active
investment. Look at the trend, not just the count.

**Conference proceedings vs journal articles.**
SPIE Advanced Lithography, IEDM, VLSI Symposium are industry-facing. Papers there
signal commercial intent. A paper in Journal of Organic Chemistry is academic.
Companies presenting at SPIE are closer to production.

**Funding acknowledgments (bottom of the paper).**
"This work was supported by [Company X]" or "funded by [grant from Company Y]"
is a supplier signal even when Company X isn't an author. Always check the
acknowledgments section.

**Known university-industry pairings (from academia/universities.md):**
- Korea: SKKU co-publications often signal Samsung involvement. KAIST + company
  co-authors are direct.
- Japan: Tohoku + equipment company = TEL/Kioxia ecosystem. University of Tokyo +
  materials company = likely commercial collaboration.
- Taiwan: NYCU (formerly NCTU) = TSMC pipeline. NTU + ITRI = government-backed R&D.
- China: Tsinghua, Zhejiang, Fudan + company = often Big Fund ecosystem companies.

## Step 3: Collect and deduplicate

Build a table of every company name found across all searches:

```
| Company Name | Found Via | Already in Entity Files? | Notes |
|---|---|---|---|
| [Company A] | ECHA registration | YES (entities/japan.md) | Known |
| [Company B] | Patent CPC search | NO | DISCOVERY — investigate |
| [Company C] | SEMICON exhibitor | NO | DISCOVERY — investigate |
| [Company D] | Competitor section of [Known Company] filing | NO | DISCOVERY |
| [Company E] | Google Scholar co-authorship | NO | Pre-commercial? |
| [Company F] | Trade data gap (Germany) | UNKNOWN | Country not in entity files |
```

## Step 4: The delta is the discovery

Filter the table to companies NOT in entity files. These are your findings.

For each discovery:
- Run the [reverse-lookup workflow](reverse-lookup.md) to establish what they
  actually do
- Search in their native language for press coverage, filings, patents
- Determine: are they a current commercial supplier, a pre-commercial R&D player,
  or a historical player that exited the market?

## Step 5: Update the investigation

Report discoveries in the standard format:

```markdown
## Unknown Supplier Discovery Results

### Search Coverage
| Method | Query Used | Companies Found | New (not in entity files) |
|---|---|---|---|
| ECHA CAS lookup | [CAS] | 8 | 2 |
| Patent CPC landscape | [code] | 15 | 4 |
| SEMICON exhibitors | [category] | 12 | 1 |
| DART keyword search | [material KR] | 3 | 1 |
| Google Scholar | [material] | 6 (company affiliations) | 2 |
| Comtrade gap analysis | HS [code] | 1 unexpected origin country | 1 |

### Source Registry
[1] ECHA registration — https://echa.europa.eu/...
    Evidence: "Company B registered as manufacturer of [CAS number]"
[2] Google Patents, CPC G03F 7/004 — https://patents.google.com/...
    Evidence: "8 patents filed 2022-2025, assignee: Company C (深圳)"
[3] Google Scholar — https://scholar.google.com/...
    Evidence: "co-authors from Company D R&D division + [University]"

### Discoveries
- Company B (Germany) registered as [CAS] manufacturer [1]
  → Not in entity files, investigate via reverse-lookup
- Company C (China) filed 8 patents since 2022 [2]
  → Not in entity files, possible emerging player
- Company D appears in 3 papers with [University] co-authors [3]
  → Possible pre-commercial player, funding acknowledgment mentions Company D

### What We Searched But Found No New Players
[List of methods that only returned known companies — this is also a finding.
If every method returns the same 3-4 companies, that's evidence of real concentration.]
```

## When to use this workflow

- After any supplier-ID investigation where findings match the entity files too
  closely (you may just be confirming your own database, not doing research)
- When the user asks "who else?" or "are there alternatives?"
- When a bottleneck analysis claims only 2-3 suppliers exist globally (verify by
  searching for others)
- When the counterfactual check suggests "what if a supplier exists that I haven't
  found?"
- Proactively, any time you feel too confident about a concentration claim
