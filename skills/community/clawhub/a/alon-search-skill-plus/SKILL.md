---
name: alon-search-skill-plus
description: Search agent skills across trusted directories, ClawHub, and GitHub adaptation candidates with explicit ranking and safety filters.
version: 0.1.4
model: sonnet
---

# Search Skill Plus

Enhanced skill search with additional sources including ClawHub and GitHub repositories that can be adapted into Skills.

## When to Use

When users describe a need and want to find an existing Skill to solve it.

Examples:
- "Is there a skill that can auto-generate changelogs?"
- "Find me a skill for frontend design"
- "I need a skill that can automate browser actions"
- "Search Toolify-related skills"

## Data Sources (by trust level)

### Tier 1 - Official / High Trust (show first)
| Source | URL | Notes |
|--------|-----|-------|
| anthropics/skills | github.com/anthropics/skills | Official examples, most reliable |
| ComposioHQ/awesome-claude-skills | github.com/ComposioHQ/awesome-claude-skills | Hand-picked, 12k+ stars |

### Tier 2 - Community Curated (secondary)
| Source | URL | Notes |
|--------|-----|-------|
| travisvn/awesome-claude-skills | github.com/travisvn/awesome-claude-skills | Community curated, 21k+ stars |
| skills.sh | skills.sh | Vercel's official directory |

### Tier 3 - Aggregators (use with caution)
| Source | URL | Notes | Security Warning |
|--------|-----|-------|------------------|
| skillsmp.com | skillsmp.com | Auto-scraped, requires extra filtering | - |
| ClawHub | clawhub.ai | OpenClaw-style skill registry | ⚠️ Known malicious skill attacks (RCE via fake CLI tools) |

### Tier 4 - GitHub Extended Discovery (reference / adaptation candidates)
| Source | URL | Notes | Output Label |
|--------|-----|-------|--------------|
| GitHub topic search | github.com/topics/claude-code / topics/claude-skill | Finds standalone skill repos not listed in curated directories | `Standalone Skill Repo` |
| GitHub code search | github.com/search | Finds repos containing `SKILL.md`, `plugin.json`, or skill-like workflows | `Standalone Skill Repo` |
| GitHub general repos | github.com | Finds tools/scripts that can be wrapped as a skill with light changes | `Adaptable GitHub Repo` |

## Search Process

### Step 1: Parse User Intent

Extract from user description:
- Core functionality keywords (e.g., changelog, browser, frontend)
- Use case (e.g., development, testing, design)
- Special requirements (e.g., language support, specific framework)

### Step 1.5: Derive Controlled Search Keywords

This skill is **not** a free-form semantic search engine. It should derive a small, controlled keyword set from user intent.

**Keyword budget rules:**
- Limit the search plan to `1-2` primary keywords
- If expansion is needed, add at most `1-2` extra keywords
- The limit applies to keyword generation, **not** the number of search sources
- Reuse the same keyword set across the allowed sources
- If results remain weak after the controlled expansion, report that results are limited instead of continuing to drift

**When expansion is allowed:**
- Start with the primary keyword set only
- Expand only if the first-pass search yields fewer than `3` high-relevance results
- `High relevance` means the result clearly matches the user's requested function or scenario, not just a loose topical overlap
- If the first pass already yields `3+` high-relevance results, do **not** expand
- After expansion, stop once the search yields `3-5` high-relevance results or enough material for a useful ranked answer
- If expansion still does not produce at least `2` high-relevance results, explicitly report that results are limited

**Mode A: User describes a scenario**
- Convert the scenario into `1-2` high-signal functional keywords
- Add `1` platform/domain keyword only when the scenario clearly depends on one
- Prefer concise action words over vague nouns

Examples:
- "I want a skill to turn meeting recordings into structured notes"
  - Primary keywords: `transcribe`, `summarize`
- "I need something to help publish Markdown to WeChat"
  - Primary keywords: `publish`, `formatter`
  - Optional platform keyword: `wechat`

**Mode B: User already gives keywords**
- Preserve the user's original keywords first
- Expand only when the original search returns too few relevant results
- Add at most `1-2` close variants, such as:
  - near-synonyms
  - higher-level functional terms
  - common implementation terms

Examples:
- User keyword: `subtitle`
  - Expansion: `transcribe`
- User keyword: `wechat`
  - Expansion: `publish`, `formatter`

**Expansion priority (used only when needed):**
- Prefer functional keywords
  - `transcribe`
  - `summarize`
  - `browser`
  - `commit`
  - `translate`
  - `scrape`
  - `deploy`
- Then platform/domain keywords when clearly required
  - `wechat`
  - `github`
  - `youtube`
  - `reddit`
  - `obsidian`
- Then implementation keywords if still needed
  - `cli`
  - `workflow`
  - `formatter`
  - `adapter`
  - `wrapper`
- Avoid vague generic words unless the user explicitly uses them
  - `tool`
  - `automation`
  - `agent`
  - `helper`
  - `assistant`

**Do NOT:**
- Expand across multiple dimensions at once unless evidence is strong
- Turn one user request into a long keyword list
- Add generic terms by default
- Pretend keyword expansion is the same as semantic retrieval

### Step 2: Multi-Source Search

**IMPORTANT: Prioritize the known 6 sources first. GitHub may be used as an extended source, but only for GitHub-hosted repositories. Do NOT search the general internet beyond the listed sites plus GitHub.**

Search by priority:

```
1. Search Tier 1 (official/high trust) first
2. If fewer than 5 results, continue to Tier 2
3. If still insufficient, search Tier 3 with strict filtering
4. If still insufficient, search Tier 4 on GitHub for:
   - standalone skill repositories
   - repositories containing `SKILL.md`
   - repositories that are not skills yet but are strong adaptation candidates
5. If still nothing found, tell user honestly
```

Before searching, briefly record the keyword plan internally:
- `Primary keywords`
- `Expanded keywords` if any
- `Why expansion was needed` if any

Recommended search flow:
1. Run the first pass with primary keywords only
2. Judge whether there are at least `3` high-relevance results across the trusted sources searched so far
3. Only then decide whether controlled keyword expansion is justified
4. Run at most one expansion round
5. If results are still sparse, stop and report limited coverage instead of continuing to broaden the query

Allowed search queries (use `site:` to restrict):
```
site:github.com/anthropics/skills {keywords}
site:github.com/ComposioHQ/awesome-claude-skills {keywords}
site:github.com/travisvn/awesome-claude-skills {keywords}
site:skills.sh {keywords}
site:skillsmp.com {keywords}
site:clawhub.ai {keywords}
site:github.com "SKILL.md" {keywords}
site:github.com "claude skill" {keywords}
site:github.com "plugin.json" {keywords}
site:github.com {keywords} ("automation" OR "cli" OR "workflow")
```

Search methods:
- GitHub repos: Use `site:github.com/{repo}` to restrict search scope
- GitHub extended discovery: Use GitHub search/topic pages only, then inspect repo metadata manually
- skills.sh: WebFetch to scrape search results from skills.sh only
- skillsmp.com: WebFetch with additional verification
- ClawHub: WebFetch clawhub.ai with strict security review

**Result sufficiency rules:**
- `0-1` high-relevance results: clearly insufficient, expansion is allowed
- `2` high-relevance results: borderline; expansion is allowed only if the results do not cover the user's scenario well
- `3-5` high-relevance results: sufficient; stop expanding
- `6+` high-relevance results: more than enough; rank and filter instead of expanding

**Do NOT:**
- Search the entire web
- Use broad queries without `site:` restriction
- Include results from unknown non-GitHub sources
- Present ordinary GitHub code as a ready-to-install skill unless it actually includes skill packaging

### Step 3: Quality Filtering (Critical)

**Must filter out the following:**

| Filter Condition | Reason |
|------------------|--------|
| GitHub stars < 10 | Not community verified |
| Last update > 6 months ago | Possibly abandoned |
| No `SKILL.md` file | Not a standard skill package |
| README too sparse | Quality concerns |
| Contains suspicious code patterns | Security risk |

**Extended GitHub rules:**
- Repos with `SKILL.md` can be recommended as `Standalone Skill Repo`
- Repos without `SKILL.md` may still be shown as `Adaptable GitHub Repo` only if:
  - the core functionality is highly relevant
  - setup is simple and local-first
  - converting it into a skill appears low effort
  - the repo is not abandoned
- Never mix these two categories together without labeling the difference clearly

**Security checks:**
- Requests sensitive permissions (e.g., ~/.ssh, env variables)
- External network requests to unknown domains
- Contains eval() or dynamic code execution
- Modifies system files
- **ClawHub specific**: Check for fake CLI tools, suspicious install scripts
- **GitHub adaptable repos**: Review install scripts, shell wrappers, binary downloads, and postinstall hooks before suggesting adaptation

### Step 4: Rank Results

Scoring formula:
```
Score = Source Weight × 0.35 + Stars Weight × 0.25 + Recency Weight × 0.2 + Relevance × 0.1 + Packaging Weight × 0.1

Source weights:
- Tier 1: 1.0
- Tier 2: 0.7
- Tier 3: 0.4 (skillsmp.com), 0.3 (ClawHub - lower due to security concerns)
- Tier 4 standalone skill repo: 0.55
- Tier 4 adaptable GitHub repo: 0.35

Packaging weights:
- Has `SKILL.md`: 1.0
- Has skill-like manifest/instructions only: 0.6
- Requires light adaptation into a skill: 0.3
```

### Step 5: Format Output

Return Top 5-10 results:

```markdown
## Found X relevant Skills

Search keywords used: `keyword-a`, `keyword-b`

### Recommended
1. **[skill-name](github-url)** - Source: anthropics/skills
   - Function: xxx
   - Stars: xxx | Last updated: xxx
   - Install: `/plugin marketplace add xxx`

### Worth considering
2. **[skill-name](github-url)** - Source: ComposioHQ
   ...

### From Tier 3 (review carefully before use)
- [skill-name](url) - Source: ClawHub ⚠️
  - Note: Review code before installation

### Adaptable GitHub Repos
- [repo-name](github-url) - Type: Adaptable GitHub Repo
  - Function: xxx
  - Stars: xxx | Last updated: xxx
  - Skill readiness: Low / Medium / High
  - Adaptation idea: Wrap existing CLI/script with `SKILL.md` and a thin workflow
```

When GitHub extended results are used, split the output into:
- `Ready to use Skills`
- `Adaptable GitHub Repos`

Do not merge them into a single ranked list without labels.
If keyword expansion was used, say so explicitly in one short line.

## Example

**User**: Is there a skill that helps write commit messages?

**Search process**:
1. Extract keywords: commit, message, git
2. Search Tier 1: Found git-commit-assistant in anthropics/skills
3. Search Tier 2: Found semantic-commit in ComposioHQ
4. Filter: Exclude results with stars < 10
5. Rank: Official sources first

**Output**:
```
## Found 3 relevant Skills

### Recommended
1. **git-commit-assistant** - Source: anthropics/skills (official)
   - Function: Generate semantic commit messages
   - Install: `/plugin marketplace add anthropics/claude-code`

2. **semantic-commit** - Source: ComposioHQ
   - Function: Follow conventional commits spec
   - Stars: 890 | Last updated: 2 weeks ago
```

## Important Notes

1. **Never recommend unverified Skills** - Better to recommend fewer than to recommend risky ones
2. **Stay cautious with Tier 3 sources** - Results from skillsmp.com and ClawHub must be double-checked
3. **ClawHub security warning** - Snyk discovered malicious skills on ClawHub.ai that use fake CLI tools for RCE. Always:
   - Review skill source code before installation
   - Check for suspicious network requests
   - Verify the skill author's credibility
   - Avoid skills that require running untrusted install scripts
4. **If nothing suitable is found** - Tell the user honestly, suggest using skill-from-github or skill-from-notebook to create their own
5. **GitHub repo results are reference candidates first** - They are not automatic endorsements or guaranteed plug-and-play Skills
6. **Always show GitHub star count for GitHub-hosted results** - Stars are a useful but imperfect trust signal
7. **Security concerns** - Clearly inform users of risks, let them decide

## About Alon

Public skill from Alon's real daily workflows.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh
