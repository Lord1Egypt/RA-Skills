# Data Sources Reference

## Source Reliability Matrix

| Source | Tier | Type | Key Required | Best For | Limitations |
|--------|------|------|-------------|---------|------------|
| ACLED | 1 | Field-verified events | Yes (free) | Armed conflict, protests, fatalities | Conflict-only; 1–3 day lag |
| UN OCHA / ReliefWeb | 1 | UN-curated reports | Appname (free) | Humanitarian, displacement | Slow publication; UN-centric framing |
| GDELT Doc API | 2 | Aggregated news | No | Volume/tone trends, multilingual | Automated; no editorial filter |
| Wire services (via GDELT) | 2 | AP, Reuters in GDELT results | No | Breaking news, verified quotes | Filtered through GDELT |
| ReliefWeb Flash Updates | 2 | UN field reports | Appname (free) | Rapid crisis updates | UN-centric framing |
| CIA World Factbook | 3 | Static reference | No | Background, demographics, history | Not live — can be years stale |
| Single-outlet coverage | 3 | Media | No | Local detail | Bias risk; unverified |
| Social/Telegram sourced | 3 | User-generated | No | Signals only — not standalone | High manipulation risk |

---

## Source Bias Matrix

All media outlets carry institutional perspectives shaped by ownership, funding, and political context. This matrix documents those perspectives without judging their legitimacy. Apply when evaluating GDELT article sources and when two sources contradict each other.

**Framing rule:** State-funded media from any country reflects that government's foreign policy positions. This is equally true for US, Russian, Chinese, Iranian, Gulf, and European state media. No state media is treated as more neutral than another by default.

| Source | Funding / Ownership | Editorial Perspective | Reliable For | Cross-Check Against |
|--------|--------------------|-----------------------|-------------|-------------------|
| Al Jazeera | Qatar state-funded | Reflects Qatari foreign policy; amplifies non-Gulf opposition movements | Arab world coverage, local-language depth | Saudi/UAE state media for balance |
| RT / Sputnik | Russian state-funded | Reflects Russian government foreign policy positions | Russian official positions, Russian domestic framing | Western wire services |
| Press TV | Iranian state-funded | Reflects Iranian government foreign policy positions | Iranian official positions, IRGC-aligned framing | Regional independent outlets |
| CGTN / Xinhua | Chinese state-funded | Reflects Chinese Communist Party foreign policy positions | Chinese official positions, Belt-and-Road framing | Regional independent outlets |
| BBC World Service | UK public-funded | Reflects UK editorial standards; significant international reach | Fact-checked reporting, broad geographic coverage | Local-language sources for on-ground detail |
| VOA / RFE-RL | US government-funded | Reflects US government foreign policy communications priorities | US official positions; coverage of countries with restricted press | Local sources and regional outlets |
| Saudi state media (SPA/Al Arabiya) | Saudi state-funded | Reflects Saudi government foreign policy positions | Saudi official positions, Gulf Cooperation Council framing | Al Jazeera, independent Arab outlets |
| UAE state media (WAM) | UAE state-funded | Reflects UAE government foreign policy positions | UAE official positions | Al Jazeera, independent outlets |
| Reuters / AP | Privately owned, commercial | Commercially incentivized toward broad factual reporting; Western editorial default | Breaking facts, verified quotes, wire-standard reporting | Local-language sources for context |
| Haaretz | Independent Israeli | Left-liberal Israeli perspective | Israeli civil society, domestic political dissent | Times of Israel, Palestinian outlets for balance |
| Times of Israel | Independent Israeli | Centrist-right Israeli perspective | Israeli security establishment framing | Haaretz, Palestinian outlets for balance |
| TRT World | Turkish state-funded | Reflects Turkish government foreign policy positions | Turkish official positions | Independent Turkish media (filtered) |
| Ethiopian state media | Ethiopian government-funded | Reflects Ethiopian government positions | Ethiopian official positions | UN OCHA, independent regional outlets |

**Application rule:** When two sources contradict each other, check their institutional perspectives. If the contradiction aligns with their known positions, the divergence itself is analytically meaningful — both versions may contain partial truth. Present both with attribution rather than selecting one.

---

## Narrative Divergence Scoring (NDS)

### Calculation Method

**Step 1:** Get GDELT tone for global coverage of topic
```
tone_global = GDELT timelinetone query (no sourcecountry filter)
```

**Step 2:** Get GDELT tone for coverage originating from within affected country
```
tone_local = GDELT timelinetone query with sourcecountry=COUNTRY_CODE
```

**Step 3:** Get volume for local vs global
```
vol_global = GDELT timelinevol (no filter)
vol_local = GDELT timelinevol with sourcecountry=COUNTRY_CODE
vol_ratio = vol_local / vol_global
expected_ratio = country_media_share  # rough estimate
vol_deviation = |vol_ratio - expected_ratio| * 10
```

**Step 4:** Calculate NDS
```
NDS = |tone_global - tone_local| + vol_deviation
```

### NDS Interpretation

| NDS | Meaning | Action |
|-----|---------|--------|
| < 2 | Consistent narrative | No special flag |
| 2–5 | Moderate divergence | Note possible spin; flag which version lacks verification |
| 5–8 | Significant divergence | Flag as **NARRATIVE CONFLICT DETECTED** — present both versions |
| > 8 | Extreme divergence | Strong indicator of active information operation; treat all coverage with skepticism |

### Language Distribution Analysis

Run GDELT `timelinelang` mode and check:

```
IF local_language_volume >> 5x English_volume:
  → Regional story being underreported internationally
  → Check: is international media deliberately avoiding this topic?
  → Flag: "Coverage gap detected — story may be larger than international reporting suggests"

IF English_volume >> 5x local_language_volume:
  → International campaign amplifying local story
  → Check: who benefits from international attention?
  → Flag: "Externally amplified narrative — verify local ground truth"

IF volume spikes without corresponding ACLED events:
  → Possible coordinated inauthentic activity
  → Flag: "Volume anomaly — no verified event correlation"
```

---

## GDELT Doc API v2 — Full Reference

**Base URL:** `https://api.gdeltproject.org/api/v2/doc/doc`
**Rate limit:** 1 request per 5 seconds
**Search window:** Last 3 months (back to January 2017 minimum)
**Languages:** 65 (all machine-translated to English for search)

### Key Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `query` | string | Use quotes for phrases: `"civil war"` |
| `mode` | artlist, timelinevol, timelinetone, timelinelang, tonechart | |
| `maxrecords` | 1–250 | Default 75 |
| `format` | json, csv, html | |
| `startdatetime` | YYYYMMDDHHMMSS | |
| `enddatetime` | YYYYMMDDHHMMSS | |
| `sourcelang` | eng, ara, rus, tur, fas, etc. | ISO 639-1 |
| `sourcecountry` | US, IR, RU, TR, IL, etc. | ISO 3166-1 alpha-2 |
| `TIMELINESMOOTH` | 1–30 | Smoothing window for timeline modes |

### Mode Cheat Sheet

| Mode | Returns | Use When |
|------|---------|---------|
| `artlist` | Articles with title, URL, tone, date | Primary source retrieval |
| `timelinevol` | Volume over time | Detect coverage surges, anomalies |
| `timelinetone` | Tone over time | Escalation/de-escalation trend |
| `timelinelang` | Volume by language | Local vs global narrative gap |
| `tonechart` | Tone distribution histogram | Overall sentiment landscape |

### Query Examples

```bash
# Country + event type
?query="Sudan military" &mode=artlist&maxrecords=25&format=json

# Boolean — multiple terms
?query="Iran AND (sanctions OR nuclear)"&mode=timelinetone&format=json

# Narrow to source country (divergence analysis)
?query="Gaza ceasefire"&mode=timelinetone&sourcecountry=IL&format=json

# Time-bounded (last 72 hours)
?query="Yemen attack"&mode=artlist&startdatetime=YYYYMMDD000000&format=json

# Language distribution
?query="Ethiopia conflict"&mode=timelinelang&format=json
```

---

## ACLED API — Reference

**Base URL:** `https://api.acleddata.com/acled/read/`
**Registration:** acleddata.com — free, approved within 24h
**Coverage:** 1997–present, global, daily updates

### Recommended Query
```bash
GET https://api.acleddata.com/acled/read/?key=KEY&email=EMAIL\
&country=COUNTRY&limit=20\
&fields=event_date|event_type|sub_event_type|actor1|assoc_actor_1|actor2|assoc_actor_2|location|admin1|fatalities|notes|source|source_scale\
&format=json
```

### Event Types
`Battles` | `Explosions/Remote violence` | `Violence against civilians` | `Protests` | `Riots` | `Strategic developments`

---

## ReliefWeb API v2 — Reference

**Base URL:** `https://api.reliefweb.int/v2/`
**Appname:** Register at apidoc.reliefweb.int — use your domain

```bash
POST https://api.reliefweb.int/v2/reports?appname=YOUR_APP
{
  "query": {"value": "KEYWORD"},
  "filter": {"field": "country.name", "value": "COUNTRY"},
  "limit": 10,
  "sort": ["date:desc"],
  "fields": {"include": ["title","date","source","url","body"]}
}
```

---

## Fallback Chain

```
ACLED unavailable → GDELT artlist filtered to conflict keywords
ReliefWeb blocked → UN OCHA RSS: https://reliefweb.int/updates.rss
GDELT rate-limited → Wait 5s, retry once, then proceed with available data
All APIs fail → Use user-provided data; flag source limitation prominently
```

---

## Data Freshness

| Source | Update Frequency | Typical Lag |
|--------|-----------------|------------|
| GDELT | Every 15 minutes | ~15 min |
| ACLED | Daily | 1–3 days |
| ReliefWeb | As published | Hours–days |
| Crisis Group | Monthly | Up to 30 days |
| CIA Factbook | Annual | Months–years |

**Rule:** For events < 48h: GDELT is most current. For conflict data: ACLED is most accurate but lagged.
