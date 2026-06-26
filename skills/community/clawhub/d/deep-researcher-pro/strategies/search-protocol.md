# Search Protocol
# For: Deep Researcher v1
# Purpose: Define search angles, language rules, and verification protocol for deep research mode

***

## Search Protocol (Deep Research — All Modes)

| Item | Requirement |
|------|-------------|
| Searches | 3-5 from different angles |
| Full-text Fetches | top 3-5 results per search |
| Cross-verification | required for ALL claims |
| Contradiction hunting | actively seek opposing evidence |

***

## Search Angles (Always Use All 5)

1. **Direct/factual**: "[domain] overview status"
   → Aim: Establish baseline understanding from authoritative sources

2. **Critical/contrarian**: "[domain] problems challenges risks limitations"
   → Aim: Surface failure modes, dissenting views, and known issues

3. **Practitioner/insider**: "[domain] experience case study best practice"
   → Aim: Ground-level evidence from people who actually do the work

4. **Forward-looking**: "[domain] trends future predictions forecast"
   → Aim: Identify trajectory and momentum signals

5. **Cross-domain**: "[domain] vs [alternative] comparison"
   → Aim: Understand positioning, alternatives, and opportunity cost

***

## Multi-subject Search Strategy

When MODE ROUTING (SKILL.md) determines there are 2+ subjects, apply this protocol.
Mode (compare / compare-multi / brief-multi) is determined by semantic intent analysis in SKILL.md — not here.

**Core rule**: each subject is researched **independently** — do NOT conflate subjects into shared search queries until the COMPARE/SCORE step.

### Per-subject execution
For each subject S:
1. Run STEP 1 region detection independently for S
2. Determine S's language per the language assignment rules
3. Execute all 5 search angles using S's language
4. Record: `[HH:MM:SS] Subject: [S] → region: [R] → language: [L]`

### Comparative search (after all subjects collected)
- 2 subjects: one comparative search `[A] vs [B]`
- 3 subjects: one 3-way search `[A] vs [B] vs [C]`; add pairwise if needed
- 4+ subjects: pairwise for the most decision-relevant pairs only; skip low-value combinations

### Total search count
- N subjects × 5 angles + 1~N comparative searches
- For N > 4: consider reducing to 3 most relevant subjects to preserve depth over breadth

### Same-language subjects
When two subjects share a research language (e.g. Alibaba Cloud and Huawei Cloud, both → Chinese):
- Keep their searches **separate** — do not merge into one search
- Include the subject name in every keyword to maintain per-subject resolution:
  - ✅ "Alibaba Cloud 2025 market share" and "Huawei Cloud 2025 market share"
  - ❌ "Alibaba Cloud and Huawei Cloud 2025 market share"

### Research depth symmetry
Before moving to SCORE, verify each subject received equivalent research depth:
- [ ] All subjects have completed all 5 search angles
- [ ] Full-text fetch counts across subjects differ by no more than 2
- [ ] Comparative search executed
- [ ] If asymmetry exists, document in RESEARCH_LOG and note in output
- Never proceed to COMPARE/SCORE if any subject has fewer than 3 search angles completed

***

## Full-text Fetch Rules

### When to fetch full text
- Search snippets that contain a key claim used in CONSUS, DIVERGENCES, or FAILED_PATHS
- Search snippets with specific numbers or statistics
- Search snippets that contradict other findings (need to verify context)

### When NOT to fetch full text
- Search snippets that only confirm what is already well-established from 2+ other sources

### Fetch priority
1. Claims used in CONSENSUS (highest priority — these are treated as fact)
2. Claims used in DIVERGENCES (need full context for both sides)
3. Specific numbers cited (must have source)
4. Contradictory findings (need to understand context)

### When full-text fetch fails
If the source URL is inaccessible (403, 404, paywall, anti-scraping, timeout), follow these rules:
- Claims based solely on search snippets (where full-text fetch failed) must be:
  - **Downgraded by one evidence level** (HIGH→MEDIUM, MEDIUM→LOW)
  - **Annotated with**: `[full-text fetch failed — based on search snippet only]`
- **CONSENSUS claims must never rely on a failed-fetch source alone** — always find a fetchable alternative first. If no fetchable alternative exists, move the claim to DIVERGENCES or [UNKNOWN].
- Do NOT use training data or prior knowledge to fill in what the full text might have said
- In RESEARCH_LOG, record the failure: `[timestamp] Full text fetch FAILED: [URL] → [reason: 403/paywall/anti-scraping]`

***

## Cross-verification Rules

### Minimum source count by evidence level
- HIGH: must have 2+ independent authoritative sources
- MEDIUM: at least 1 authoritative source + 1 supporting source
- LOW: single source is acceptable but must be marked

### What counts as "independent"
- Two articles from different outlets (not republishing the same wire)
- A report + a practitioner account
- A primary source + secondary analysis

### What does NOT count as independent
- Same article republished on multiple platforms
- Two articles citing the same single original source
- A summary and its original (count as 1)

### Contradiction handling
If two sources directly contradict on a factual claim:
1. Note the contradiction in DIVERGENCES
2. Do not pick a side unless a third source breaks the tie
3. If no tie-breaker exists, mark as [CONTESTED] with both sources

***

## Search Language and Region

### Region detection (always run at STEP 1)
- Detect the domain region from the query topic itself — do NOT wait for an explicit --region flag
- Examples: "日本SaaS市場" → region=Japan, "mercado logístico alemán" → region=Germany
- If the topic is inherently global (e.g. "AI Agent frameworks"), region = global, no local-language requirement

### Language assignment rules (hard rules)
| Condition | Angles 1–2 (mandatory) | Angles 3–5 |
|-----------|------------------------|------------|
| region = global | User query language or English | User query language or English |
| region = China/Taiwan/HK | Chinese (中文) | Chinese or English |
| region = Japan | Japanese (日本語) | English or Japanese |
| region = Korea | Korean (한국어) | English or Korean |
| region = Germany/Austria | German (Deutsch) | English or German |
| region = France | French (Français) | English or French |
| region = Indonesia/Malaysia | Bahasa Indonesia/Melayu | English or local |
| region = Thailand | Thai (ภาษาไทย) | English or Thai |
| region = Vietnam | Vietnamese (Tiếng Việt) | English or Vietnamese |
| region = Arabic-speaking | Arabic (العربية) | English or Arabic |
| region = Russia/CIS | Russian (Русский) | English or Russian |
| region = Spain/Latin America | Spanish (Español) | English or Spanish |
| region = other single country | Official local language of that country (see fallback inference below) | English or local |

### Fallback language inference (when region is not in the table above)
When the detected region does not match any explicit entry in the language assignment table,
**do not default to English** — instead, run this inference sequence:

**Step A — Infer from the query itself**
- Does the query contain non-ASCII words that identify a language?
  - Greek letters (α, β, γ…) → ελληνικά
  - Arabic script (ا, ب, ت…) → العربية
  - Cyrillic (А, Б, В…) → Русский (or relevant CIS language)
  - Thai script → ภาษาไทย
  - Devanagari (अ, आ…) → हिन्दी / local South Asian language
- Does the query contain a country name or demonym that implies a language?
  - "Greek / Ελληνικά / Grèce / Grecia" → ελληνικά
  - "Polish / Polska / polskie" → Polski
  - "Dutch / Netherlands / Holland" → Nederlands
  - "Swedish / Sverige" → Svenska
  - "Norwegian / Norge" → Norsk
  - "Finnish / Suomi" → Suomi
  - "Czech / Česká" → Čeština
  - "Portuguese / Portugal / Brasil" → Português
  - "Italian / Italia" → Italiano
  - "Turkish / Türkiye" → Türkçe
  - "Hebrew / Israel" → עברית
  - "Hindi / India (non-regional)" → हिन्दी or English (India is multilingual)
  - "Swahili / Kenya / Tanzania" → Kiswahili
  - "Malay / Malaysia / Brunei" → Bahasa Melayu

**Step B — Look at the domain context**
- If the topic is a government policy, legal regulation, or official standard:
  → The official language of that government is almost always the right language
  → Example: "Norwegian oil regulations" → Norsk (Bokmål), even though English is also official in some contexts
- If the topic involves a specific sub-national region within a multi-language country:
  → Use that region's dominant local language, NOT the national default language
  → Example (India): Tamil Nadu policy → Tamil (தமிழ்); Kerala policy → Malayalam (മലയാളം); Maharashtra → Marathi (मराठी); NOT Hindi
  → Example (Spain): Catalonia policy → Catalan (Català); Basque Country → Euskara; NOT just Spanish
  → Example (China): generally 中文; Hong Kong context → Traditional Chinese or Cantonese-influenced writing
- If the topic is an international standard applied locally:
  → Use the country's official language for local implementation details
  → Use English for the international standard itself

**Step C — When inference is genuinely ambiguous**
- If after Steps A and B the language is still unclear (e.g. India with many regional languages, or a topic cutting across multiple regions):
  1. Use English as angle 1, and the most probable local language as angle 2
  2. Record the ambiguity in RESEARCH_LOG: `[HH:MM:SS] Language inference ambiguous for region [X] → Used [languages] → Reason: [why uncertain]`
  3. Do NOT silently default to English-only — the ambiguity must be documented

**Step D — Validate the choice**
Before executing angle 1, confirm: "Does my search keyword read like a native speaker would write it, or does it look like a translation?" If the latter, reformulate before searching.

### Multi-language and supranational regions (hard rules)
For regions with no single dominant official language:

| Region type | Angles 1–2 language rule |
|-------------|--------------------------|
| EU-wide policy (Schengen, GDPR, subsidies, directives) | English + French (EU's two primary working languages) |
| Schengen Area (multi-country context) | English + French, OR English + language of the primary member state in context |
| Belgium | Dutch if Flemish context; French if Walloon/federal context |
| Switzerland | German (primary); French if western-Swiss context |
| Canada | English; French if Quebec-specific context |
| International organizations (IMO, UN, WTO, World Bank, OECD) | English (primary working language) |
| Other multi-language regions | English + official language of the most contextually relevant country |

**Document language choice**: For any multi-language or supranational region, always record in RESEARCH_LOG:
`[HH:MM:SS] Region detected: [region] → Multi-language region → Language selected: [language(s)] → Rationale: [why]`
Never default to English-only for a multi-language region without documenting the rationale.

### Multi-country region language allocation (hard rules)
When the topic covers **multiple countries that each have their own mapped language**
(e.g. "Southeast Asia major countries", "Central America", "Nordic countries", "Gulf states"):

**Allocation rule**:
1. Identify the 2–3 most contextually relevant countries for the specific topic
   (prioritize by: explicit mention in query > policy importance > market size > alphabetical)
2. Assign those countries' mapped languages to angles 1–3 (one language per angle)
3. Use English for angles 4–5 (regional overview sources, international reports)
4. Record in RESEARCH_LOG:
   `[HH:MM:SS] Region: [multi-country] → Countries prioritized: [A, B, C] → Angle languages: [lang1, lang2, lang3, EN, EN] → Rationale: [why this priority]`

**Examples**:

| Topic | Countries prioritized | Angles 1–3 | Angles 4–5 |
|-------|----------------------|------------|------------|
| Southeast Asia e-commerce | Indonesia, Vietnam, Thailand | Bahasa Indonesia, Tiếng Việt, ภาษาไทย | English |
| Southeast Asia labor law | Indonesia, Philippines, Thailand | Bahasa Indonesia, English (PH official), ภาษาไทย | English |
| Central America agriculture policy | Mexico, Guatemala, Honduras | Español (add country name to differentiate) | English |
| Nordic welfare systems | Sweden, Denmark, Norway | Svenska, Dansk, Norsk | English |
| Gulf states infrastructure | UAE, Saudi Arabia, Qatar | العربية (UAE context), العربية (SA context), English | English |

**When all countries in the region share a language** (e.g. all Central American countries → Spanish,
all Arabic Gulf states → Arabic):
→ Use the shared language for angles 1–2, differentiated by country-specific keywords
→ Use English for angle 3 onward

### Region and language inference
Region and research language are always inferred from the query topic itself — no explicit instruction needed.
Follow the language assignment table and fallback inference rules below.
If the user mentions a specific region or language in their query (e.g. "focus on the EU market", "search in Japanese"),
treat that as a strong hint and apply accordingly.

### Enforcement
- **Record the actual language used** for each angle in RESEARCH_LOG
- **Do NOT substitute English for a required local-language search** — English may only be used for angles 3–5 when region is non-global
- If the search engine does not return local-language results for the required language, note this in RESEARCH_LOG and try a reformulated local-language query before falling back to English

***

## Search Quality Checklist

Before moving from STEP 2 (COLLECT) to STEP 3 (SCORE), verify:
- [ ] 3-5 searches completed (covering all 5 angles)
- [ ] Top 3-5 results fetched for full text
- [ ] All claims have source references
- [ ] No claim relies solely on a search snippet without full-text verification (or is downgraded per full-text fetch failure rules)
- [ ] Contradictory findings identified and noted
- [ ] All full-text fetch failures are recorded and affected claims downgraded
- [ ] If --mode=compare, both subjects received equal search coverage (symmetry checkpoint passed)
- [ ] If information is scarce (< 3 valid sources total), mark domain as "information-scarce" per SKILL.md rules
- [ ] **If region ≠ global: Angles 1 and 2 were executed in the official local language** (check RESEARCH_LOG — each angle entry must show the actual language used)
- [ ] **If region ≠ global: At least 2 local-language sources appear in the SOURCES table**
