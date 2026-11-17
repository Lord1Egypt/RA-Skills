---
name: chatmosp-literature-search
description: |
  Academic literature searcher of the chatMOSP system. When MOSP_database lacks
  matching parameters, searches open-access journals (Nature Communications,
  Science Advances, PNAS, etc.) and other academic resources to extract MSR/KMC
  parameters (surface energy, adsorption energy, interaction matrix, etc.).
  Triggers: parameter-builder detects missing key parameters and the user chooses
  literature search for completion.
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-literature-search

## 1. Core Responsibilities

1. Journal search: access 3 priority layers
2. Article retrieval: 3 stages (abstract → main text → SI)
3. Parameter extraction: extract E_ads, w, gamma from tables
4. Parameter validation: completeness + reasonability + consistency
5. Return scored result to parameter-builder

## 2. Input Contract

| Field | Required | Example |
|-------|----------|---------|
| Metal element | Yes | Pd, Pt, Au, Cu, Ni |
| Gas system | Yes | CO+O₂, H₂+CO₂, CO+H₂ |
| Temperature range | No | 300-500K |
| Pressure range | No | 1-10 atm |

## 3. Output Contract

Return parameter table (JSON), containing:

| Field | Description |
|-------|-------------|
| Surface energy | γ (eV/Å²) for each facet (100, 110, 111) |
| Adsorption energy | E_ads (eV) for each facet + each gas |
| Interaction matrix | w (eV) for CO-CO, CO-O, O-O |
| Parameter source | DOI, article title, authors |
| Completeness score | 1-10 |

> **⚠️ Literature search does NOT return gas entropy.** parameter-builder MUST recalculate it using the §3.1 formula after receiving the result.

## 4. Workflow

```
Input (metal + gas)
  → Journal search (3 priority layers)
  → Article retrieval (3 stages: abstract → main text → SI)
  → Parameter extraction (pdftotext + keyword search)
  → Parameter validation (completeness, reasonability, consistency)
  → Output (parameter table with score)
```

## 5. Journal Search Priority

### Layer 1: Top journals (priority, but may be inaccessible)

- Science, Nature, JACS, Angewandte Chemie, PRL, JCP
- Strategy: DOI resolution → abstract → main text → SI
- API limit or CAPTCHA → **immediately skip to Layer 2**

### Layer 2: Fully open-access journals (**recommended**)

- **Nature Communications**
- **Science Advances**
- **PNAS**
- **ACS Central Science**
- **Chemical Science**

Advantages: completely free, high quality, complete SI

### Layer 3: Preprint platforms (last resort)

- arXiv, ChemRxiv, bioRxiv
- Note: not peer-reviewed, parameters may be inaccurate, requires user confirmation

## 6. Tool Selection

### 6.1 Prefer the currently available interactive browser/web tool

- ✅ Supports JS rendering
- ✅ Supports login state
- ✅ Supports interactive operations
- ✅ Better suited for journal sites

### 6.2 Do NOT use `web_fetch`

- ❌ Journal sites often have restrictions (403, CAPTCHA)
- ❌ Cannot execute JS
- ❌ Cannot get dynamically loaded content

### 6.3 Fallback

If the current environment has no browser, web-search, PDF, or file-reading
tool available, do not pretend that literature retrieval was completed. Ask the
user to provide the paper, DOI, SI file, or parameter values directly.

## 7. Detailed Literature Retrieval Process

### Step 1: Build search keywords

**✅ Correct format** (MUST use):

```
"keyword1" AND "keyword2" AND "keyword3"
```

**Examples**:

- Cu cluster in CO oxidation → `"Cu" AND "CO oxidation"`
- Pd cluster in CO oxidation → `"Pd" AND "CO oxidation"`
- Pt cluster in H₂ → `"Pt" AND "H2"`

**❌ Incorrect format** (DO NOT use):

```
Pd CO oxidation
```

Space-separated format is treated as one keyword, returning inaccurate results.

### Step 2: Access journal site

- Use the currently available browser/web tool to enter journal search page
- Input keywords
- Default sort: relevance

### Step 3: Get top 10 results

- Only check top 10 (highest relevance)
- Output title, DOI, abstract (optional)

### Step 4: Initial screening (by title)

Screening criteria:

1. Reaction atmosphere match (must be target reaction: CO oxidation, WGSR, etc.)
2. Metal system match (must be target metal: Pd, Pt, Cu, etc.; exclude alloys)

Output filtered list + screening reason for each

### Step 5: User interaction

Choose next step:

1. Carefully check all filtered articles
2. Carefully check one specific article (user-specified)
3. Switch to another journal

### Step 6: Detailed article check

**6.1**: Check main text

- Confirm metal match
- Confirm reaction atmosphere match
- Look for parameter tables

**6.2**: No parameters → download SI

- Parameters only exist in text and tables, **NOT** in images
- Download SI PDF: `si_{first_author}_{year}.pdf`
- Same author, same year, multiple: `si_smith_2023a.pdf` / `b` / `c`

**6.3**: Check SI

- Search keywords: Table, Supplementary Table, S1, S2
- Extract parameter tables

### Step 7: Parameter extraction

**7.1**: Download SI via the currently available browser/web tool

**7.2**: Convert PDF to text

```bash
pdftotext si_{author}_{year}.pdf si_{author}_{year}.txt
```

**7.3**: Search parameter table keywords

- Table S, Supplementary Table
- adsorption energy, E_ads, binding energy
- surface energy, γ, surface tension
- interaction parameter, interaction matrix

**7.4**: Use `read` tool to read text, locate parameter tables

**7.5**: Extract values from tables, note unit conversions

**7.6**: Validate parameters

- Within reasonable range
- Follow physical laws
- Consistent

### Step 8: Show parameters to user

```
📊 Parameters extracted from literature:

【Article Information】
- Title: {title}
- DOI: {doi}
- Journal: {journal}

【Parameter Table】
- Surface energy: {values}
- Adsorption energy: {values}
- Interaction matrix: {values}

【Completeness Score】
- Score: {score}/10
- Description: {description}

Please select:
1. ✅ Use these parameters → pass to parameter-builder
2. ❌ Reject, continue searching
3. ❌ Cancel task
```

## 8. Article Retrieval 3 Stages

| Stage | Purpose | Search content |
|-------|---------|----------------|
| 1. Abstract | Confirm relevance | Metal, reaction, research type |
| 2. Main text | Find parameter tables | Methods, Results, Tables, Figures |
| 3. SI | Complete parameters | Supplementary Tables, Methods, Data |

> ⚠️ **IMPORTANT**: Main text not mentioning parameters does NOT mean SI lacks them. If article relevance is high, still download SI to check.

## 9. MSR Required Data Checklist

### Basic parameters

- ✅ Metal element, temperature, pressure
- ✅ Cluster radius, gas species, gas partial pressures

### Surface parameters (per facet)

- ✅ Surface energy γ (eV/Å²): (100), (110), (111), (211), (311), etc.

### Adsorption parameters (per facet + per gas)

- ✅ Adsorption energy E_ads (eV): e.g., CO on Pd(111), O₂ on Pd(100)

### Interaction parameters

- ✅ w matrix (eV): CO-CO, CO-O, O-O

### Gas parameters

- ✅ Gas entropy (eV/K): can be calculated via formula (T-dependent) or extracted

> ⚠️ Literature search does NOT return gas entropy; parameter-builder MUST auto-calculate

## 10. Completeness Scoring

### Per-parameter score

| Parameter type | Score | Description |
|----------------|-------|-------------|
| Surface energy | 2 points | At least (100), (110), (111) three facets |
| Adsorption energy | 3 points | Each gas on each facet |
| Interaction matrix | 3 points | CO-CO, CO-O, O-O |
| Parameter source | 1 point | DOI, title, author |
| Parameter reasonability | 1 point | Within reasonable range, physically plausible |

### Score level action

| Score | Level | Action |
|-------|-------|--------|
| 9-10 | Complete | Use directly |
| 7-8 | Mostly complete | User confirms missing, then use |
| 5-6 | Partial | Supplement missing |
| 3-4 | Incomplete | Use similar metal as reference |
| 1-2 | Very incomplete | Not recommended |

> ⚠️ **Gas entropy is NOT in this scoring.** Regardless of score, parameter-builder MUST recalculate gas entropy per formula.

## 11. Timeout & Fallback

### 11.1 Timeout

- Total time limit: 5 minutes
- Per-article limit: 2 minutes
- On timeout: stop immediately, return found parameters (even if incomplete)

### 11.2 Fallback

After 5 articles without complete parameters:

```
⚠️ I have searched 5 articles but could not find complete parameters.
- Surface energy: ✅ found
- Adsorption energy: ❌ not found
- Interaction matrix: ❌ not found

Suggestions:
1. Use similar metal as reference
2. Provide known parameter source (DOI or title)
3. Use default/test parameters
```

### 11.3 One journal failure prompt

```
⚠️ No parameters found in top 10 articles of {Journal}

Please select:
1. Switch journal
2. Cancel task (if all journals exhausted, suggest changing system or user-providing params)
```

## 12. Lessons Learned

- **Lesson 1: Keyword selection**
  - Start with broad keywords (`"Pd" AND "CO oxidation"`)
  - Then filter with specific (`"adsorption energy"`)
  - Search topics, not just parameter names
- **Lesson 2: DOI priority**
  - Prefer known DOI or title
  - Direct DOI access
  - Don't rely solely on keyword search
- **Lesson 3: Multi-platform search**
  - Don't limit to single journal
  - Prefer open access
- **Lesson 4: Don't waste time on inaccessible resources**
  - API limit or CAPTCHA → immediately skip to next layer
  - Prioritize open access
- **Lesson 5: Main text not mentioning parameters ≠ SI lacks them**
  - If article is highly relevant, still download SI
  - SI typically has complete parameter tables

## 13. Cross-Skill Handoff

- **Called by**: parameter-builder when key parameters missing + user chooses lit search
- **Calls tools**: available browser/web/PDF/file-reading tools in the current environment
- **Returns to parameter-builder**: parameter table with score

## 14. Dependencies

- **chatmosp-parameter-builder** — caller
- **Browser/web tool** — journal site access, SI download
- **pdftotext** — PDF to text
- **read** — read text files

## 15. File Structure

```
chatmosp-literature-search/
├── SKILL.md       # Chinese reference
└── SKILL_cn.md    # This file (English)
```

## 16. Practical Example

```
User: show me the Pd cluster under atmosphere of CO and O2

1. Extract need: metal=Pd, gases=[CO, O₂]
2. Check MOSP_database: no match
3. parameter-builder prompts with 4 options → user chooses literature search (open access)
4. Launch this skill:
   - Platform: Nature Communications
   - Keywords: `"Pd" AND "CO oxidation" AND "adsorption energy"`
   - Tool: currently available browser/web tool
5. Find relevant article, confirm DOI
6. Download SI → save to literature/
7. pdftotext → search "Supplementary Table" → extract parameters
8. Validate: completeness score
9. Display result + annotate missing
10. User confirms → pass to parameter-builder to assemble input.json

Key points:
- Always start with open-access journals
- Literature search does NOT return gas entropy; parameter-builder MUST recalculate
- Interaction parameters may be in KMC format; need MSR/KMC format conversion (see parameter-builder §9)
```
## ChatMOSP Companion Skills

This skill is part of the ChatMOSP skill set. For complete functionality, install the companion ChatMOSP skills from ClawHub when they are missing:

- chatmosp-input-coordinator
- chatmosp-parameter-builder
- chatmosp-msr-generator
- chatmosp-kmc-simulator
- chatmosp-literature-search
- chatmosp-file-organizer

If a required companion skill is unavailable, ask the user to install the missing ChatMOSP skill from ClawHub before continuing. Use the GitHub repository only as a fallback.
