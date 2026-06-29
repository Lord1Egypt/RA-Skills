---
name: copy-brain
description: Copy a public figure's thinking into a callable "thinking skill". For a given scenario, extract and replicate their **thinking style, mental models, reasoning, and decision logic** (rather than merely imitating their tone). Use when the user wants to "think like a certain public figure / create a skill based on their brain".
metadata:
   clawbot:
      requires:
         env:
         - TAVILY_API_KEY
         - SCRAPEBADGER_API_KEY
         - REDFOX_API_KEY
---

# copy-brain

Copy a **public figure** specified by the user into a **callable thinking skill**.

> **The core is not imitating tone, but replicating the "brain".** Tone and wording are only surface-level; what we truly want to capture is **how this person thinks, how they weigh trade-offs, and how they make decisions under uncertainty**. The final skill should enable the agent to **reason out the answer this person would likely give on a new problem using their thinking style**, rather than reusing things they have already said.
> **Path convention**: The directory containing this `SKILL.md` is the skill root directory (hereafter `<SKILL_DIR>`).
> All paths below are **relative to `<SKILL_DIR>`**. Before running any script, first `cd` into `<SKILL_DIR>` (the directory containing this SKILL.md); output/template paths are resolved relatively in the same way.

## Workflow

### Step 0 / 1: Check the output directory and determine the persona

1. List the `.md` files under `<SKILL_DIR>/output/` (ignore `.gitkeep`; ignore stray intermediate files like `.json`, see Step 4.1).
2. **If skill files already exist**: list them for the user and ask "Do you want to reuse one of the existing skills, or create a new persona skill?".
   - If they choose to reuse → read that file and complete the user's subsequent request based on it, then end this workflow.
3. **If the directory is empty**: directly ask "Whose thinking would you like to copy?".

Once you have the persona's name, do a lightweight confirmation: is the name unique (if there are namesakes, ask the user to add field/nationality), and determine a slug for the filename (pinyin or English, lowercase, hyphenated).

---

### Step 2: Check and explain the API Keys

This skill can use three data sources (**recommended but not required**; skip whichever is missing). Ask the user to configure the corresponding API Keys in their **computer's system environment variables** using the **variable names** in the table below:

| Service | Env Variable | Purpose | Sign Up |
|------|-----------|------|------|
| Tavily | `TAVILY_API_KEY` | Fallback search when the built-in search is poor (stale results / multilingual / poor matching); good at non-Chinese / non-China content | https://app.tavily.com |
| ScrapeBadger | `SCRAPEBADGER_API_KEY` | Fetch the persona's profile and posts on X (Twitter) | https://scrapebadger.com/dashboard |
| RedFox | `REDFOX_API_KEY` | Fetch Xiaohongshu and WeChat Official Account articles | https://redfox.hk/dashboard/keys |

Explain the table above to the user (purpose + recommended setup). How to configure (after setting, you must **reopen the terminal** for it to take effect):

```powershell
# Windows PowerShell (persist to user environment variables)
setx TAVILY_API_KEY "your_key"
setx SCRAPEBADGER_API_KEY "your_key"
setx REDFOX_API_KEY "your_key"
```

```bash
# macOS / Linux (add to ~/.zshrc or ~/.bashrc)
export TAVILY_API_KEY="your_key"
export SCRAPEBADGER_API_KEY="your_key"
export REDFOX_API_KEY="your_key"
```

Check the current configuration:

```bash
python scripts/check_keys.py
```

> If dependencies are missing, install first: `pip install -r requirements.txt` (run in `<SKILL_DIR>`)

- The script signals that a service is not configured with `EXIT_NO_KEY` (exit code 2) + a stderr message.
- Even if none of the three are configured, you can continue using just the agent's built-in web search + web extraction tools, only with narrower coverage. **Do not force the user to configure them**.
- The Tavily script only exposes 3 search parameters: `query` (required), `--search-depth` (optional, basic/advanced/fast/ultra-fast, default basic), `--time-range` (optional, day/week/month/year). For full text, use the built-in web extraction tool on the result URLs.

---

### Step 3: Search background → determine scenario

1. **First use the agent's built-in web search** to do a **quick background check** on the persona (identity, field, notable achievements, active platforms). If the built-in results are poor (stale / multilingual / poor matching), use Tavily as a fallback:

```bash
python scripts/tavily_search.py "{persona} bio background"
# When you need higher relevance or a time window:
python scripts/tavily_search.py "{persona} bio background" --search-depth advanced --time-range year
```

2. Summarize the quick-check highlights to the user in 2-4 sentences, then **ask about the scenario**: "In which scenario would you like to think/decide using this persona's **thinking style**?" and offer a few candidate examples (tailored to the persona's traits), emphasizing **thinking and judgment** rather than tone.

After the user confirms the scenario, record `scenario` and its slug.

---

### Step 4: Deep search → draft → confirm → save

**4.1 Collect deeply and broadly** (multiple angles, multiple keywords). **Prioritize first-hand original platform sources**—as long as a Key is configured, use the scripts below as much as possible, treating the persona's own posts/notes/articles as the primary corpus; supplement general background/commentary with the built-in search (Tavily fallback when poor):
Every script supports `-h` to view its parameters.

```bash
# ① First-hand platform sources (primary)—X platform (persona is active on X and ScrapeBadger is configured)
python scripts/scrapebadger.py profile {x_username}
python scripts/scrapebadger.py tweets {x_username} --pages 3
# You can also precisely search their tweets by topic (advanced operators):
python scripts/scrapebadger.py search "from:{x_username} {scenario_keywords}" --type Latest --pages 2

# ① First-hand platform sources (primary)—Xiaohongshu / WeChat Official Accounts (Chinese personas, RedFox configured)
python scripts/redfox_xhs.py search "{persona}" --pages 2
python scripts/redfox_gzh.py search "{persona} {scenario_keywords}" --sort _4 --pages 2
# After a hit, use detail / work to pull the full text of a single piece to get the complete reasoning:
python scripts/redfox_xhs.py detail --id {workId}
python scripts/redfox_gzh.py work {workUuid}

# ② General background, views, controversies, recent developments—built-in search first, Tavily fallback when poor
python scripts/tavily_search.py "{persona} {scenario_keywords}" --search-depth advanced
python scripts/tavily_search.py "{persona} views quotes interview" --time-range year
```

Every fact/view/piece of reasoning must keep a **source link**; especially preserve original excerpts that reveal "**why he thinks this way**".

- **Read the full text**: both the built-in search and Tavily return summaries/snippets; to read the full text, use the agent's built-in web extraction tool on the result URLs. If a platform post fetched by a script only has a summary, use `redfox_*.py detail/work` or extract the original link to get the full text.
- **Do not save intermediate JSON to disk**: the scripts print JSON to the terminal stdout by default, and the agent can just read the terminal output. **Do not** use `--out`, and **do not** save `.json` or other intermediate collection files under `output/`. `output/` only holds the final persona skill `.md` (see 4.3). If you accidentally generate a `.json` under `output/` or an `output/output/` subdirectory, delete it after saving the `.md`.

**4.2 Generate the draft**: apply the structure of `<SKILL_DIR>/templates/persona_skill_template.md`, filling it in for the chosen scenario. **Present the draft to the user for preview**, explain the data sources and collection time, and proactively point out areas that are uncertain / lack evidence.
**4.3 Save after confirmation**: once the user agrees, save to:

```
<SKILL_DIR>/output/{people_name_slug}-{scenario_slug}.md
```

After saving, tell the user the file path and note: this file is itself a persona skill with frontmatter and can be reused.

## Quality and Ethics Requirements
- Factual claims need sources; distinguish between "facts" and "stylistic simulation". Do not fabricate quotes or falsify data.
- Do not use this to impersonate the actual person for fraud, defamation, or misleading purposes; do not include private/non-public information.
- Search with the utmost rigor. If the information found is insufficient to copy the public figure's thinking, stop generating the draft and inform the user.
