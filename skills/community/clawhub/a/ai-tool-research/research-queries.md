# Research Queries

Reusable search-query templates. Read during Step 3 of the parent SKILL.md.

**Always append a date filter**: `after:<since_date>` for web/Google, `since:<since_date>` for X.com, `pushed:>=<since_date>` / `updated:>=<since_date>` for GitHub.

---

## Universal query patterns (apply to every tool)

Substitute `<TOOL>` with the tool's canonical name.

### Web / Google

- `<TOOL> productivity workflow after:<since_date>`
- `<TOOL> use case case study after:<since_date>`
- `<TOOL> skill extension plugin after:<since_date>`
- `<TOOL> vs <competitor> 2026 after:<since_date>`
- `<TOOL> release notes changelog <current_month> 2026`
- `<TOOL> tutorial guide <persona> after:<since_date>`

### X.com / Twitter

- `<TOOL> since:<since_date> min_faves:50`
- `<TOOL> tip since:<since_date> min_retweets:20`
- `<TOOL> workflow since:<since_date>`
- `<TOOL> "ship" OR "built" since:<since_date> min_faves:100`
- `from:<known_power_user> <TOOL>`

### GitHub

- `<TOOL>-skills pushed:>=<since_date>`
- `<TOOL>-extensions pushed:>=<since_date>`
- `<TOOL>-plugins pushed:>=<since_date>`
- `<TOOL>-rules pushed:>=<since_date>`
- `<TOOL>-mcp pushed:>=<since_date>`
- `awesome-<TOOL> pushed:>=<since_date>`

### Reddit

- `site:reddit.com/r/<tool-sub> after:<since_date>`
- Relevant subs: `r/ClaudeAI`, `r/cursor`, `r/ChatGPTCoding`, `r/Bard`, `r/OpenAI`, `r/LocalLLaMA`, `r/PromptEngineering`

### YouTube (transcripts via search)

- `<TOOL> tutorial <persona> 2026`
- `<TOOL> tips tricks <current_month> 2026`

---

## Per-tool primary sources

Start every research run here before going broad.

### Claude

**Official / verified**:

- [anthropic.com/news](https://anthropic.com/news) — product announcements
- [docs.claude.com](https://docs.claude.com) — feature docs
- [github.com/anthropics/skills](https://github.com/anthropics/skills) — official skill marketplace
- [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
- [github.com/anthropics/courses](https://github.com/anthropics/courses)
- [support.anthropic.com](https://support.anthropic.com)

**Curation**:

- [github.com/obra/superpowers](https://github.com/obra/superpowers) — the cross-tool SDLC skill pack
- [github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [github.com/travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [github.com/BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
- `gh skill` package manager

**X.com handles to monitor**:

- @AnthropicAI, @alexalbert__ (DevRel), @jxnlco, @swyx, @simonw

---

### Cursor

**Official / verified**:

- [cursor.com](https://cursor.com) — homepage, changelog, forum
- [forum.cursor.com](https://forum.cursor.com)
- [docs.cursor.com](https://docs.cursor.com)
- [github.com/getcursor/cursor](https://github.com/getcursor/cursor)
- [cursor.directory](https://cursor.directory) — rules/plugins/MCP directory

**Curation**:

- [github.com/PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
- [github.com/cursor/plugins](https://github.com/cursor/plugins)
- [ai-rules.dev](https://ai-rules.dev)

**X.com handles**:

- @cursor_ai, @amanrsanger, @srush_nlp, @mckaywrigley, @ericzakariasson

---

### Codex (OpenAI)

**Official / verified**:

- [openai.com/codex](https://openai.com/codex)
- [github.com/openai/codex](https://github.com/openai/codex)
- [github.com/openai/skills](https://github.com/openai/skills) — curated + experimental skills
- [platform.openai.com/docs](https://platform.openai.com/docs)
- [github.com/openai/codex-plugins](https://github.com/openai/codex-plugins)

**Curation**:

- [github.com/openai-cookbook](https://github.com/openai/openai-cookbook)
- TokRepo curated Codex write-ups
- The Prompt Shelf

**X.com handles**:

- @OpenAIDevs, @sama, @kevinweil, @npew, @stevenheidel

---

### Gemini (Google)

**Official / verified**:

- [ai.google.dev](https://ai.google.dev)
- [gemini.google.com](https://gemini.google.com)
- [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
- [github.com/gemini-cli-extensions](https://github.com/gemini-cli-extensions) — official extensions org
- [aistudio.google.com](https://aistudio.google.com)
- [developers.googleblog.com](https://developers.googleblog.com)
- [notebooklm.google.com](https://notebooklm.google.com)

**Curation**:

- [github.com/Piebald-AI/awesome-gemini-cli-extensions](https://github.com/Piebald-AI/awesome-gemini-cli-extensions)
- [geminicli.com/extensions](https://geminicli.com/extensions)

**X.com handles**:

- @GoogleDeepMind, @Google, @demishassabis, @OriolVinyalsML, @lmthang

---

### OpenClaw

**Official / verified**:

- [openclaw.ai](https://openclaw.ai) / [openclaw.im](https://openclaw.im)
- [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- [github.com/openclaw/clawhub](https://github.com/openclaw/clawhub) — the registry
- [clawhub.ai](https://clawhub.ai) — registry web UI
- [discord.gg/clawd](https://discord.gg/clawd)

**Curation**:

- [github.com/VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 5,400+ filtered / 13,729+ total
- [clawskills.sh](https://clawskills.sh)
- [crewclaw.com](https://crewclaw.com) — visual agent generator
- [openclawplaybook.ai](https://www.openclawplaybook.ai)

**X.com handles**:

- @steipete (creator — Peter Steinberger), @openclaw

---

## Per-persona source specializations

Run these in addition to the tool-primary sources when researching a specific persona.

### PhD / research

- [arxiv-sanity.com](https://arxiv-sanity.com)
- [paperswithcode.com](https://paperswithcode.com)
- r/MachineLearning, r/AskAcademia
- LaTeX Stack Exchange

### Solopreneur

- [indiehackers.com](https://indiehackers.com)
- [latentspace.com](https://latentspace.com) (Substack)
- r/indiehackers, r/SaaS, r/Entrepreneur

### Marketer / AEO / SEO

- [searchengineland.com](https://searchengineland.com)
- [hubspot.com/marketing](https://hubspot.com/marketing)
- r/SEO, r/marketing

### Designer

- [figma.com/community](https://figma.com/community)
- [dribbble.com](https://dribbble.com)
- [uxdesign.cc](https://uxdesign.cc)
- r/UXDesign, r/UI_Design

### Video / creator

- [tubefilter.com](https://tubefilter.com)
- [colinandsamir.com](https://colinandsamir.com)
- r/NewTubers, r/podcasting

### Developer

- [news.ycombinator.com](https://news.ycombinator.com) — sort by past month
- [dev.to](https://dev.to)
- [thenewstack.io](https://thenewstack.io)
- [pragmaticengineer.com](https://pragmaticengineer.com)
- Changelog podcast

### PKM / student

- [forum.obsidian.md](https://forum.obsidian.md)
- r/ObsidianMD, r/Zettelkasten, r/GetStudying
- [buildingasecondbrain.com](https://buildingasecondbrain.com)

### Sales / finance / ops

- [salesforce.com/blog](https://salesforce.com/blog)
- [hubspot.com/blog](https://hubspot.com/blog)
- r/sales, r/smallbusiness, r/accounting

---

## Search query checklist per run

For each tool, at minimum:

```text
- [ ] Vendor changelog / release notes for research window
- [ ] Official GitHub org — new repos or pushes > since_date
- [ ] Awesome-list — diff since last run
- [ ] X.com — 5+ power-user handles + generic tool query
- [ ] Reddit — top posts past month in the tool's sub
- [ ] HN — search "<TOOL>" past month
- [ ] dev.to — past-month tag filter
- [ ] Two persona-specialized sources relevant to the current research angle
```

If time-limited, prioritize: **vendor changelog → official GitHub → awesome-list → X.com power users**. Everything else is secondary.

---

## Dealing with stale / broken results

If a canonical URL 404s during verification:

1. Try the Wayback Machine for the most recent live capture
2. Search for the canonical name + author to see if the repo moved
3. If it genuinely disappeared, mark the entry 🔴 Unverified or remove it from the new version of the file; add a line to the "Changes since last run" section noting the removal

If a primary source (e.g., an awesome-list) hasn't been updated in the research window, still check it — absence of updates is itself a signal worth noting.

---

## Known power-user handles (X.com) — cross-tool

Worth monitoring regardless of which tool is being researched:

- @simonw — Simon Willison (LLM tools generalist)
- @swyx — Shawn Wang (AI engineering)
- @levelsio — Pieter Levels (solopreneur + vibe coding)
- @mckaywrigley — McKay Wrigley (agentic coding)
- @steipete — Peter Steinberger (OpenClaw creator)
- @jxnlco — Jason Liu (AI engineering)
- @svpino — Santiago Valdarrama (ML engineering)
- @rauchg — Guillermo Rauch (Vercel + AI UX)
- @_philschmid — Philipp Schmid (Google DeepMind)
- @karpathy — Andrej Karpathy (AI foundations)
- @charliermarsh — Charlie Marsh (Astral / Python + AI)
