---
name: embodied-ai-news
description: "Aggregates publicly available Embodied AI and Robotics news from curated sources (robotics media, arXiv, company blogs). Delivers structured briefings on humanoid robots, foundation models, hardware, deployments, and funding with direct links to original articles. Optional module surfaces hot GitHub open-source repos relevant to embodied AI (policies, sim, data, benchmarks)."
homepage: https://github.com/HeXavi8/skills
---

# Embodied AI News Briefing

> Aggregates the latest Embodied AI & Robotics news from curated sources and delivers concise summaries with direct links. Covers the full stack: algorithms, hardware, simulation, deployment, funding, policy, and the China ecosystem.

## When to Use This Skill

Activate this skill when the user:

- Asks for embodied AI news, robot news, or humanoid robot updates
- Requests a daily/weekly/monthly robotics briefing
- Mentions wanting to know what's happening in embodied AI / robotics
- Asks about specific companies: Tesla Optimus, Figure, Unitree, AGIBOT, Boston Dynamics, etc.
- Asks about specific technologies: VLA models, diffusion policy, sim-to-real, dexterous manipulation
- Wants a summary of recent robotics research papers
- Asks about robotics funding, deployments, or supply chain
- Asks about simulation platforms, benchmarks, or datasets
- Asks for **GitHub 热门仓库**、**具身智能开源项目**、**star 最多的机器人代码库**，或 wants a **repo leaderboard / open-source radar**
- Asks about robotics policy, safety standards, or export controls
- Requests a monthly trend report or competitive analysis
- Says: "给我今天的具身智能资讯" (Give me today's embodied AI news)
- Says: "机器人行业有什么新动态" (What's new in the robot industry)
- Says: "最近有什么人形机器人的消息" (Any recent humanoid robot news)
- Says: "这个月的具身智能趋势报告" (This month's embodied AI trend report)
- Says: "embodied AI updates", "robot learning news", "humanoid robot news"

### Trigger Keywords

**English**: `embodied AI`, `humanoid robot`, `robot news`, `robotics update`, `robot learning`, `VLA model`, `diffusion policy`, `dexterous manipulation`, `sim-to-real`, `robot deployment`, `robotics funding`, `Figure AI`, `Tesla Optimus`, `Unitree`, `AGIBOT`, `Boston Dynamics`, `1X`, `Physical Intelligence`, `Skild AI`, `robot hand`, `quadruped robot`, `Isaac Sim`, `world model robot`, `robot benchmark`, `robot safety`, `robot regulation`, `monthly robot report`

**Chinese**: `具身智能`, `人形机器人`, `机器人资讯`, `灵巧操作`, `仿真到真实`, `机器人部署`, `宇树`, `智元`, `优必选`, `银河通用`, `傅利叶`, `机器人融资`, `灵巧手`, `四足机器人`, `机器人大模型`, `机器人月报`, `机器人安全`, `机器人政策`, `GitHub 热门`, `开源仓库`, `机器人开源`

---

## Reference Files

This skill relies on **6** companion reference files. Always consult them during execution:

```
📁 references/
├── 📰 news_sources.md        — WHERE to find information (tiered source list)
├── 🔍 search_queries.md     — HOW to search (query templates & recipes)
├── 📝 output_templates.md   — WHAT format to output (6+ template variants)
├── 📊 taxonomy.md           — SHARED LANGUAGE (categories, keywords, company list)
├── ⭐ github_repos.md       — GitHub hot repos module (discovery, ranking, output schema)
└── 🧭 workflow.md           — WHEN and in what ORDER to execute (SOP for daily/weekly/monthly)
```

| File                  | When to Consult                                                                         |
| --------------------- | --------------------------------------------------------------------------------------- |
| `news_sources.md`     | Phase 1 — choosing which sites to fetch; selecting tier-appropriate sources             |
| `search_queries.md`   | Phase 1 — building search queries; selecting recipe by briefing type                    |
| `taxonomy.md`         | Phase 3 — classifying stories; Phase 1 — looking up company aliases & tech terms        |
| `output_templates.md` | Phase 5 — rendering final output; selecting template by user request                    |
| `github_repos.md`     | Phase 1 & 5 — when user wants GitHub 热门开源; weekly/monthly open-source momentum       |
| `workflow.md`         | All Phases — orchestrating the end-to-end workflow; time budgeting; monthly maintenance |

### File Interconnection Map

```
┌─────────────────┐      ┌────────────────────┐     ┌───────────────┐     ┌──────────────────┐
│  search_queries │────▶ │  news_sources      │────▶│  Classify &   │────▶│ output_templates │
│  (discover)     │      │  (browse & verify) │     │  Prioritize   │     │   (generate)     │
└─────────────────┘      └────────────────────┘     └───────────────┘     └──────────────────┘
                                    ▲                        ▲
                                    │                        │
                                    └────── taxonomy.md ─────┘
                                         (shared vocabulary)

Optional GitHub module:
  search_queries (Recipe F) ──▶ github_repos.md ──▶ output_templates (⭐ GitHub section)
```

---

## Execution Workflow

### Phase 0: Determine Briefing Type & Time Scope

**Before any tool calls**, ask the user (if not already clear):

1. **Briefing Type**: Daily / Weekly / Monthly / Custom Topic?
2. **Time Scope**: Last 24 hours / Last 7 days / Last 30 days / Custom date range?
3. **Output Format**: Standard / Brief / Thread / Markdown Report / Presentation / Custom?
4. **Focus Area** (optional): All categories / Specific category (e.g., only hardware, only China ecosystem)?
5. **GitHub 开源模块** (optional): Include **hot embodied-AI repos** section? (Default: **Yes** for weekly/monthly if user asked for “完整/含开源”; **No** for daily unless requested.)

**Default if user doesn't specify**:

- Type: Daily
- Scope: Last 24 hours
- Format: Standard
- Focus: All categories
- GitHub module: **Off** for daily; **Off** for weekly/monthly unless user implies open-source / GitHub / 技术栈雷达

**Map to workflow.md**:

- Daily → `workflow.md` Section "Daily Workflow"
- Weekly → `workflow.md` Section "Weekly Workflow"
- Monthly → `workflow.md` Section "Monthly Workflow"

---

### Phase 1: Information Gathering

Consult `workflow.md` for the appropriate recipe, then execute the corresponding steps from `search_queries.md` and `news_sources.md`.

#### Step 1.1: Execute Search Queries

**Tool**: `WebSearch` (or equivalent web search tool)

**Source**: `search_queries.md` → Select the appropriate recipe:

- Daily Briefing → Recipe A (5 queries)
- Weekly Roundup → Recipe B (8 queries)
- Monthly Deep Dive → Recipe C (12 queries)
- Custom Topic → Recipe D + user-specified filters

**Parameters**:

- `return_format`: markdown
- `with_images_summary`: false
- `timeout`: 20 seconds per source
- Fetch only from publicly accessible sources listed in `news_sources.md`

**Output**: A list of 20–50 URLs with headlines and snippets.

---

#### Step 1.2: Fetch Tier 1 Sources Directly

**Tool**: `mcp__web_reader__webReader`

**Source**: `news_sources.md` → Tier 1 section

Directly fetch the homepage or RSS feed of:

- The Robot Report
- IEEE Spectrum — Robotics
- TechCrunch — Robotics
- Robotics Business Review
- (Add others based on briefing type)

**Parameters**:

- `url`: [homepage URL from news_sources.md]
- `return_format`: markdown
- `with_images_summary`: false
- Process only URLs from verified sources in `news_sources.md`

**Output**: Recent headlines (last 24h / 7d / 30d based on scope).

---

#### Step 1.3: Fetch arXiv Papers

**Tool**: `mcp__arxiv__readURL` (if available) or `WebSearch` with arXiv-specific queries

**Source**: `search_queries.md` → Section "6. Academic Research (arXiv)"

Execute 2–3 arXiv queries:

```
cat:cs.RO AND ("embodied AI" OR "robot learning" OR "VLA") submittedDate:[today - 7d TO today]
```

**Output**: 5–10 recent papers with abstracts.

---

#### Step 1.4: Fetch Company Blogs & Official Announcements

**Tool**: `mcp__web_reader__webReader`

**Source**: `news_sources.md` → Tier 2 (Company Blogs) + Tier 4 (China Ecosystem)

Fetch from:

- Figure AI Blog
- Physical Intelligence Blog
- Tesla AI Blog
- Unitree Blog (Chinese + English)
- AGIBOT WeChat Official Account (if accessible)
- (Add others based on focus area)

**Fetch constraints**:

- Only process URLs from search results and sources listed in `news_sources.md`
- Skip content requiring authentication
- Timeout: 15 seconds per URL

**Output**: Recent announcements (last 7d / 30d based on scope).

---

#### Step 1.5: GitHub — Hot Embodied AI Repos (Optional)

**When**: User requested the GitHub module (Phase 0), or weekly/monthly briefing explicitly includes open-source radar.

**Tools**: `WebSearch`, `WebFetch` (or equivalent) — **no** GitHub token required; use public pages only.

**Source**: `github_repos.md` (full procedure) + `search_queries.md` → **Section 10.5** + **Recipe F**

**Procedure** (summary):

1. Run **Recipe F** queries; collect **12–20** candidates.
2. Filter with **`github_repos.md` → Relevance Filter**; verify each shortlisted repo URL.
3. Rank per **`github_repos.md` → Rank (“热门” definition)**; output **5–8** repos.
4. Do **not** invent star counts; use verified values or “see repo page”.

**Output**: Structured rows ready for **`output_templates.md` → GitHub 热门开源** section; deduplicate against stories already covered in Foundation Models / Simulation sections.

---

### Phase 2: Content Extraction & Deduplication

For each fetched URL:

1. **Extract**:
   - Headline
   - Publication date
   - Source name
   - Summary (first 2–3 paragraphs or abstract)
   - Key entities: companies, models, hardware platforms (use `taxonomy.md` for reference)

2. **Deduplicate**:
   - If multiple sources cover the same story, keep the one with the most detail
   - Merge information if they provide complementary details

3. **Discard**:
   - Stories older than the time scope
   - Irrelevant content (use `search_queries.md` Section 1.4 "Noise Exclusion Filter")
   - Duplicate announcements

**Output**: A deduplicated list of 15–30 stories with extracted metadata.

---

### Phase 3: Classification & Prioritization

Consult `taxonomy.md` to classify each story.

#### Step 3.1: Assign Primary Category

Use `taxonomy.md` → Section "1. News Category Taxonomy"

Assign each story to **exactly one** primary category:

- 🔥 Major Announcements
- 🧠 Foundation Models & Algorithms
- 🦾 Hardware & Platforms
- 🌐 Simulation & Infrastructure
- 🏭 Deployments & Commercial
- 💰 Funding, M&A & Business
- 🌍 Policy, Safety & Ethics
- 🇨🇳 China Ecosystem

**Rules** (from `taxonomy.md` → "Category Assignment Rules"):

- **Major Announcements**: Only for top-impact stories (new paradigm, >$500M funding, first-ever deployment milestone)
- **China Ecosystem**: Use when the story's primary significance is about the Chinese market/ecosystem
- **Cross-cutting stories**: Assign primary + up to 2 secondary tags

---

#### Step 3.2: Assign Priority Level

Use `taxonomy.md` → Section "3. Priority Scoring System"

Calculate priority score (0–100) based on:

- **Impact** (0–40 points): Paradigm shift / Major milestone / Incremental improvement
- **Timeliness** (0–20 points): Breaking news / Recent (1–3 days) / Older
- **Source Authority** (0–20 points): Tier 1 / Tier 2 / Tier 3
- **Relevance** (0–20 points): Core embodied AI / Adjacent / Tangential

**Priority Levels**:

- **P0 (90–100)**: Must-read, above-the-fold
- **P1 (70–89)**: Important, include in main body
- **P2 (50–69)**: Notable, include if space allows
- **P3 (<50)**: Optional, move to "Other News" section or omit

---

#### Step 3.3: Sort Stories

Within each category, sort by:

1. Priority score (descending)
2. Publication date (most recent first)

---

### Phase 4: Content Synthesis

For each story, generate:

1. **One-sentence summary**: Capture the core news in <20 words
2. **Key points** (2–4 bullet points): Extract the most important details
3. **Metadata fields** (based on category):
   - For **Foundation Models**: Model Type, Embodiment, Open Source, Impact
   - For **Hardware**: Hardware Type, Company, Specs, Impact
   - For **Deployments**: Deployment Scale, Industry Vertical, Performance Metrics, Impact
   - For **Funding**: Amount, Lead Investor, Valuation, Use of Funds
   - (See `output_templates.md` for full metadata schema per category)

4. **Impact statement**: Why this matters for the embodied AI field (1–2 sentences)

**Tone & Style**:

- **Objective**: Present facts without hype or editorial opinion
- **Concise**: Favor clarity over completeness
- **Technical**: Use domain-specific terminology from `taxonomy.md`
- **Neutral**: Treat all companies, countries, and technologies equally

---

### Phase 5: Output Generation

Consult `output_templates.md` to select the appropriate template.

#### Step 5.1: Select Template

Based on user request (from Phase 0):

| User Request          | Template to Use            |
| --------------------- | -------------------------- |
| "Daily briefing"      | Standard Format            |
| "Quick summary"       | Brief Format               |
| "Twitter thread"      | Thread Format              |
| "Markdown report"     | Markdown Report Format     |
| "Presentation slides" | Presentation Format        |
| "Custom"              | Adapt from Standard Format |

---

#### Step 5.2: Render Output

Fill in the selected template with:

- **Header**: Date, source count, time scope
- **Category sections**: Ordered by priority (🔥 Major Announcements first)
- **Story blocks**: Headline, summary, key points, metadata, source link
- **GitHub 热门开源** (if Step 1.5 ran): Place **before** Key Takeaways / Daily Pulse per `output_templates.md`
- **Footer**: Methodology note, source attribution

**Quality checks**:

- All links are valid and correctly formatted
- All metadata fields are filled (use "N/A" if not applicable)
- No duplicate stories
- Stories are sorted by priority within each category
- Total output length is appropriate for briefing type:
  - Daily: 1,500–2,500 words
  - Weekly: 3,000–5,000 words
  - Monthly: 5,000–10,000 words

---

#### Step 5.3: Add Contextual Notes (Optional)

If the user requested analysis or trends, append:

- **Trend Spotlight**: 2–3 emerging patterns observed this period
- **Company Momentum**: Which companies/labs are most active
- **Technology Shifts**: Notable changes in technical approaches
- **Geographic Insights**: Regional differences (e.g., US vs China ecosystem)

Use `taxonomy.md` → Section "5. Trend Analysis Framework" for guidance.

---

### Phase 6: Delivery & Follow-up

1. **Deliver the briefing** in the selected format
2. **Offer follow-up options**:
   - "Would you like me to deep-dive into any specific story?"
   - "Should I track these companies/topics for your next briefing?"
   - "Would you like a comparison with last week/month's trends?"

---

## Special Workflows

### Custom Topic Deep-Dive

If user asks about a specific topic (e.g., "What's new with dexterous hands?"):

1. **Consult** `taxonomy.md` → Section "2. Technology & Product Taxonomy" → Find relevant subcategories
2. **Build custom queries** using `search_queries.md` → Recipe D (Custom Topic)
3. **Fetch** from all tiers in `news_sources.md` that cover this topic
4. **Output** using the "Deep-Dive Format" from `output_templates.md`

---

### Company-Specific Briefing

If user asks about a specific company (e.g., "What's Figure AI been up to?"):

1. **Consult** `taxonomy.md` → Section "4. Company & Organization Directory" → Find company profile
2. **Build queries** targeting:
   - Company blog
   - News mentions
   - arXiv papers by company researchers
   - Funding announcements
3. **Output** using the "Company Spotlight Format" from `output_templates.md`

---

### China Ecosystem Focus

If user asks specifically about China (e.g., "中国人形机器人有什么进展?"):

1. **Prioritize** `news_sources.md` → Tier 4 (China Ecosystem)
2. **Use** `search_queries.md` → Section "8. China Ecosystem"
3. **Consult** `taxonomy.md` → Section "4.3 China Ecosystem Companies"
4. **Output** in Chinese or bilingual format (ask user preference)

---

### GitHub Open-Source Radar Only

If the user **only** wants a **GitHub 热门仓库** snapshot (no full news briefing):

1. **Skip** or minimize Steps 1.1–1.4; run **`github_repos.md`** procedure end-to-end with **Recipe F**
2. **Output** using **`output_templates.md`** → **⭐ GitHub** section (Standard or Brief) plus a short **methodology** footnote
3. **Language**: Match user language; keep repo names in original spelling

---

## Operational Guidelines

### Operating Scope

This skill operates in **read-only mode**:

- Fetches content from public sources listed in reference files
- Synthesizes and presents information to the user
- Does not modify, post, or interact with external systems
- Does not perform actions on behalf of the user unless explicitly requested (e.g., "add this to my calendar")

#### Self-Modification Guard

- The agent must **never** silently modify the skill's own reference files (`news_sources.md`, `search_queries.md`, `github_repos.md`, `output_templates.md`, `workflow.md`, `taxonomy.md`)
- All proposed changes to these files must be presented as a **Maintenance Proposal** with a diff, and only applied after explicit user approval — see `workflow.md` → Part B
- User-facing reports and maintenance edits must remain separate; briefings never trigger file modifications

### Information Freshness

- **Daily briefing**: Prioritize stories from the last 24 hours
- **Weekly briefing**: Include stories from the last 7 days, but highlight the most recent
- **Monthly briefing**: Cover the full 30 days, but organize by week or theme

### Source Diversity

Aim for a balanced mix:

- 40% from Tier 1 (core industry media)
- 30% from Tier 2 (company blogs & official sources)
- 20% from Tier 3 (academic & research)
- 10% from Tier 4 (China ecosystem, if relevant)

### Quality over Quantity

- Better to have 15 high-quality, well-summarized stories than 50 shallow headlines
- If a story lacks detail or verification, mark it as "Unconfirmed" or omit it

### Handling Uncertainty

- If a story's details are unclear, state: "Details are limited; awaiting official confirmation"
- If sources conflict, present both versions: "Source A reports X, while Source B reports Y"
- Never fabricate details to fill gaps

### Language Handling

- If user asks in Chinese, output in Chinese (but keep company/model names in English)
- If user asks in English, output in English
- For bilingual users, offer: "Would you like this in English, Chinese, or bilingual?"

---

## Error Handling

### If a source is unreachable:

- Skip it and note in the footer: "Note: [Source Name] was unavailable at the time of this briefing"

### If search returns no results:

- Broaden the query or try alternative keywords from `taxonomy.md`
- If still no results, inform the user: "No recent news found for [topic] in the specified time range"

### If classification is ambiguous:

- Default to the most specific applicable category
- Add a secondary tag if the story spans multiple domains

### If output exceeds length limits:

- Prioritize P0 and P1 stories
- Move P2 and P3 stories to a "Quick Hits" section with one-line summaries
- Offer to generate a separate deep-dive on omitted topics

---

## Maintenance & Updates

### Monthly (consult `workflow.md` → "Monthly Workflow"):

- Review `taxonomy.md` for new companies, models, or terminology
- **Propose** updates to `news_sources.md` if new authoritative sources emerge
- **Propose** refinements to `search_queries.md` based on what queries yielded the best results
- **Propose** updates to `github_repos.md` anchor list and Recipe F queries

**⚠️ All reference file changes require explicit user approval.** The agent generates a Maintenance Proposal (see `workflow.md` → Part B) and presents it as a diff. Do not write to any reference file without user confirmation.

### Quarterly:

- Audit the priority scoring system — are P0 stories truly the most impactful?
- Review output templates — do they match user preferences?

---

## Example Invocations

### Example 1: Daily Briefing

**User**: "Give me today's embodied AI news"

**Agent**:

1. Determines: Daily briefing, last 24h, Standard format, All categories
2. Executes Recipe A from `search_queries.md` (5 queries)
3. Fetches Tier 1 sources from `news_sources.md`
4. Classifies using `taxonomy.md`
5. Outputs using Standard Format from `output_templates.md`

---

### Example 2: Weekly Roundup

**User**: "What happened in robotics this week?"

**Agent**:

1. Determines: Weekly briefing, last 7 days, Standard format, All categories
2. Executes Recipe B from `search_queries.md` (8 queries)
3. Fetches Tier 1 + Tier 2 sources
4. Prioritizes P0 and P1 stories
5. Outputs using Standard Format with "Trend Spotlight" section

---

### Example 3: Custom Topic

**User**: "What's new with VLA models?"

**Agent**:

1. Determines: Custom topic, last 7 days, Deep-Dive format
2. Consults `taxonomy.md` → "Vision-Language-Action (VLA) Models"
3. Builds custom queries from `search_queries.md` Section 2.1
4. Fetches from Tier 1 + Tier 3 (arXiv)
5. Outputs using Deep-Dive Format

---

### Example 4: Company Spotlight

**User**: "What's Unitree been up to?"

**Agent**:

1. Determines: Company-specific, last 30 days, Company Spotlight format
2. Consults `taxonomy.md` → Company profile for Unitree
3. Fetches Unitree blog + news mentions + arXiv papers
4. Outputs using Company Spotlight Format from `output_templates.md`

---

### Example 5: China Ecosystem

**User**: "中国人形机器人有什么进展?"

**Agent**:

1. Determines: China focus, last 7 days, Standard format, Chinese output
2. Prioritizes `news_sources.md` Tier 4 sources
3. Uses `search_queries.md` Section 8 (China Ecosystem)
4. Outputs in Chinese using Standard Format

---

### Example 6: GitHub Hot Repos Add-on

**User**: "今天的具身智能资讯里加上 GitHub 最热门的相关开源仓库"

**Agent**:

1. Enables GitHub module for this run; keeps daily scope if user asked “今天”
2. Executes **Recipe F** from `search_queries.md` and follows **`github_repos.md`** (verify URLs, no fake stars)
3. Inserts **`## ⭐ GitHub 热门开源（具身智能相关）`** from `output_templates.md` **before** Key Takeaways
4. Shortlists **5–8** repos with category tags and canonical `https://github.com/owner/repo` links

---

## Summary

This skill orchestrates a multi-phase workflow:

1. **Determine** briefing type & scope (including optional GitHub module)
2. **Gather** information from curated sources using structured queries
3. **Classify** stories using a shared taxonomy
4. **Prioritize** based on impact, timeliness, and relevance
5. **Synthesize** concise summaries with metadata
6. **Output** in the user's preferred format (with optional **GitHub 热门开源** section)

**Key success factors**:

- Always consult the **6** reference files at the appropriate workflow stage
- Maintain objectivity and source attribution
- Prioritize quality and relevance over quantity
- Adapt to user preferences (language, format, focus area)
