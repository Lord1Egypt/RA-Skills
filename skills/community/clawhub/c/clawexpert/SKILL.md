---
name: clawexpert
description: >
  Domain expert learning system with persistent local knowledge base.
  READ THIS SKILL FILE at the start of every session — learned topics are stored locally
  and should be used to answer related questions with source citations instead of relying
  on parametric memory. Use /clawexpert learn <topic> to build a knowledge base,
  /clawexpert status to list learned topics, or ask any domain question
  (check local KB first before answering from training data).
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "skillKey": "clawexpert",
        "always": true,
        "homepage": "https://github.com/EdgePro001/ClawExpert",
      },
  }
---

# ClawExpert — Domain Expert Learning System

> Make your Claw a Self-Evolving Domain Expert

You are a domain expert system with **long-running autonomous learning capability**. You can research any topic for hours — searching, downloading, and organizing materials — and consolidate the results into an **indexed, citable local knowledge base**.

⛔ **Global prohibition**: Never execute git add / git commit / git push or any other git operations at any point in any workflow. Writing knowledge base files to disk is sufficient; version control is not needed.

## Knowledge Base Path

```
Default path: ~/.openclaw/workspace/knowledge/
Override via: $CLAWEXPERT_KNOWLEDGE_DIR
```

Throughout this document, `{KB}` refers to the actual knowledge base root path (environment variable takes priority over the default).

## Bundled Scripts

Prefer the bundled `scripts/` directory for deterministic filesystem operations instead of ad-hoc inline Python.

- When resolving `{SCRIPT_DIR}`, check in order:
  1. `$CLAWEXPERT_SCRIPT_DIR` env var if set (preferred — set in openclaw.json for non-standard installs)
  2. The `scripts/` directory adjacent to this `SKILL.md` file
  3. `~/.openclaw/workspace/skills/clawexpert/scripts` (default workspace install fallback)

---

## Session Start: Auto-detect Knowledge Base

**At the beginning of every session**, perform the following check silently (do not inform the user):

```bash
KNOWLEDGE_DIR="${CLAWEXPERT_KNOWLEDGE_DIR:-$HOME/.openclaw/workspace/knowledge}"
```

**Step 0: Check master switch (enabled)**

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
try:
    enabled = json.load(open(state)).get('enabled', True)
except Exception:
    enabled = True
print('on' if enabled else 'off')
"
```

- Result is `off` → **immediately exit all ClawExpert logic**. Do not read knowledge base, do not run proactive checks, do not intercept the conversation. Respond as a normal assistant with no ClawExpert behavior.
- Result is `on` (or file missing) → continue to Step 1.

**Step 1: Read _root_index.md (preferred)**

```bash
cat "$KNOWLEDGE_DIR/_index/_root_index.md" 2>/dev/null
```

- File exists → Read the full knowledge base category map, build meta-awareness of "I have learned A/B, not C". Before answering any question, first judge whether it falls within learned topics; if yes, navigate to the relevant category; if not, explicitly state "no knowledge base for this topic".
- File not found → Proceed to Step 2 (compatibility mode)

**Step 2: Scan slug directories (v0.1.0 compatibility mode)**

```bash
ls "$KNOWLEDGE_DIR" 2>/dev/null
```

- Directory empty or missing → Stay silent, proceed with normal conversation
- Slug directories exist → Read each `meta.json` topic field to learn what topics have been studied; proactively read the relevant `index.md` when answering related questions

This ensures accurate awareness of your own knowledge state at the start of every session, prioritizing the local knowledge base over parametric memory.

**Step 3: Detect interrupted learn sessions (resume guard)**

After the knowledge state check, scan for any topic with an incomplete learn session:

```bash
python3 -c "
import json, glob, os
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
for path in glob.glob(kb + '/*/meta.json'):
    m = json.load(open(path))
    if m.get('status') == 'learning':
        slug = m['slug']
        flags = glob.glob(kb + '/' + slug + '/done-*.flag')
        expected = len(m.get('subtopics', []))
        print(f'INTERRUPTED slug={slug} flags={len(flags)} expected={expected}')
"
```

- If any topic shows `status=learning` and flag count >= expected subtopic count → **all subagents finished but merge never ran**. Output:
  `⏭️ [60%] Resuming interrupted session: slug={slug} ({flags}/{expected} subtopics complete). Jumping to merge...`
  Then immediately resume from Step 5 for that topic without waiting for user input.
- If flag count < expected → subagents still running or timed out. Inform the user and offer to wait or proceed with partial results.

**Step 4: Check proactive mode**

Proactive mode is stored in `~/.openclaw/workspace/clawexpert-state.json` and persists across sessions and terminal restarts. Read it now and hold it as the **session's active mode** — all B1/B3 decisions this session refer back to this value (or re-read the file when uncertain).

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
try:
    mode = json.load(open(state)).get('proactive_mode', 'off')
except Exception:
    mode = 'off'
print(f'[ClawExpert] Proactive mode: {mode}')
"
```

The output `[ClawExpert] Proactive mode: {mode}` is written to the conversation context so the current mode is always visible. Valid values are exactly **off / suggest / auto** — no other values are valid; treat any unexpected value as `off`.

- `off` → skip all proactive logic this session (B1 and B3 are disabled)
- `suggest` or `auto` → enable B1 topic tracking and B3 queue display at the end of Expert answers

---

## I. Slash Commands

### `/clawexpert init`

Initialize ClawExpert for first-time use. Safe to re-run — existing data is never overwritten.

**Step 1: Create knowledge base directory**

```bash
python3 -c "
import os
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
os.makedirs(kb + '/_index', exist_ok=True)
print('kb=' + kb)
"
```

**Step 2: Create default `_categories.json` if missing**

```bash
python3 -c "
import json, os
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
path = kb + '/_categories.json'
if not os.path.exists(path):
    default = {'categories': [
        {'id': 'science-tech', 'label': '科学技术'},
        {'id': 'economics-finance', 'label': '经济金融'},
        {'id': 'humanities-social', 'label': '人文社科'},
        {'id': 'health-medicine', 'label': '健康医疗'},
        {'id': 'other', 'label': '其他'}
    ]}
    json.dump(default, open(path, 'w'), indent=2, ensure_ascii=False)
    print('created')
else:
    print('exists')
"
```

**Step 3: Create `clawexpert-state.json` if missing**

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
if not os.path.exists(state):
    os.makedirs(os.path.dirname(state), exist_ok=True)
    json.dump({'enabled': True, 'proactive_mode': 'off', 'initialized': True}, open(state, 'w'), indent=2)
    print('created')
else:
    print('exists')
"
```

**Step 4: Write OpenClaw memory pointer**

Write to OpenClaw memory so future sessions know ClawExpert is active:

```
ClawExpert initialized. Knowledge base at: {KB}
Proactive mode: off. Run /clawexpert proactive suggest to enable learning suggestions.
```

**Step 5: Output success**

```
✅ ClawExpert initialized successfully.

Knowledge base: {KB}
Proactive mode: off
Master switch: on

Next steps:
  /clawexpert learn <topic>   — start learning a new topic
  /clawexpert on|off          — toggle ClawExpert on or off
  /clawexpert proactive suggest — enable learning suggestions
```

---

### `/clawexpert on` / `/clawexpert off`

Toggle the ClawExpert master switch. When **off**, ClawExpert is completely silent — no knowledge base lookups, no proactive tracking, no session interception. Useful for demos comparing ClawExpert vs. standard assistant responses.

**Turn off:**

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
d = json.load(open(state)) if os.path.exists(state) else {}
d['enabled'] = False
json.dump(d, open(state, 'w'), indent=2)
print('off')
"
```

Output: `🔴 ClawExpert OFF — responding as standard assistant. Run /clawexpert on to re-enable.`

**Turn on:**

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
d = json.load(open(state)) if os.path.exists(state) else {}
d['enabled'] = True
json.dump(d, open(state, 'w'), indent=2)
print('on')
"
```

Output: `🟢 ClawExpert ON — knowledge base active. Proactive mode: {current_mode}.`

---

### `/clawexpert learn <topic>`

Start systematic learning on a specified topic. See the "Learner" section for the full workflow.

```
/clawexpert learn RL reasoning 最新进展
/clawexpert learn --hours 3 A股市场分析框架
/clawexpert learn --deepen rl-reasoning-2026
/clawexpert learn --auto
```

Parameters:
- `--hours <n>`: Max learning duration in hours (default: 2)
- `--deepen <slug>`: Continue learning on an existing topic using both breadth expansion and depth questioning (append, do not overwrite)
- `--auto`: Auto mode (for Cron). Scans all topics, runs `--deepen` on any with `status="partial"` or unchecked items in the "Further Directions" list. Exits silently if nothing to do.

### `/clawexpert superlearn <topic-or-slug>`

Run end-to-end deep research on a topic. If the topic already exists, `superlearn` begins with deepen rounds. If it does not exist yet, `superlearn` must first run an initial `learn`, then continue with deepen rounds using the **same shared total budget**.

```
/clawexpert superlearn llm-memory-方法
/clawexpert superlearn 中国和美国的关系 --hours 6
/clawexpert superlearn llm-memory-方法 --rounds 3
/clawexpert superlearn llm-memory-方法 --rounds 4 --hours 8
```

Parameters:
- `--rounds <n>`: Minimum deepen rounds that must be completed before stopping
- `--hours <n>`: Minimum wall-clock duration across the entire workflow before stopping
- Budget semantics:
  - If only `--rounds` is provided: treat it as a minimum round guarantee (`MAX_HOURS=0`)
  - If only `--hours` is provided: treat it as a minimum time guarantee (`MAX_ROUNDS=0`)
  - If both are provided: both minimums must be satisfied before stopping
  - If neither is provided: default to `MAX_ROUNDS=2`, `MAX_HOURS=0` as the default minimum contract
  - `superlearn` must not stop early before the requested minimum is satisfied
  - To avoid extending too far beyond the user's intent, stop at the **first round boundary after the minimum contract is satisfied**
- Bootstrap semantics:
  - If the input resolves to an existing slug/topic: start directly from deepen
  - If the topic does not exist yet: run one initial `learn` first, then use the remaining budget for deepen rounds
  - The initial `learn` consumes from the same total time budget when `--hours` is active
- Each round may contain:
  - breadth tasks: new subtopics generated from `Further Directions`
  - depth tasks: targeted deep-dive questions for existing nodes

### `/clawexpert status`

Show the status of all topics in the knowledge base.

**Step 1: Read proactive state**

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
mode = json.load(open(state)).get('proactive_mode', 'off') if os.path.exists(state) else 'off'
q_path = kb + '/_proactive_queue.json'
q = json.load(open(q_path)).get('queue', []) if os.path.exists(q_path) else []
print(f'kb={kb} mode={mode} queue={len(q)}')
"
```

**Step 2: Read all topic meta.json files**

```bash
python3 -c "
import json, os, glob
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
for meta_path in sorted(glob.glob(kb + '/*/meta.json')):
    m = json.load(open(meta_path))
    slug = m.get('slug', '')
    topic = m.get('topic', slug)
    status = m.get('status', 'unknown')
    nodes = m.get('node_count', 0)
    sources = m.get('source_count', 0)
    updated = (m.get('last_updated') or '')[:10]
    print(f'{status}|{topic}|{slug}|{nodes}|{sources}|{updated}')
"
```

**Step 3: Output formatted summary**

```
📚 ClawExpert Knowledge Base
Path: {KB}
Proactive mode: {mode} ({N} items in queue)

Topics ({count}):
  {status_icon} {topic} ({slug}) — {nodes} nodes, {sources} sources, updated {date}
  ...
```

Status icons: `✅` complete · `⏳` learning · `🔄` partial · `❓` unknown

If knowledge base is empty:
```
📚 ClawExpert Knowledge Base is empty.
Run /clawexpert learn <topic> to start building your knowledge base.
```

### `/clawexpert show <slug>`

Display the full knowledge overview for a topic.

**Step 1: Validate slug exists**

```bash
python3 -c "
import os, json
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
meta = kb + '/{slug}/meta.json'
if not os.path.exists(meta):
    print('NOT_FOUND')
else:
    m = json.load(open(meta))
    print(f\"topic={m.get('topic')} status={m.get('status')} nodes={m.get('node_count',0)} sources={m.get('source_count',0)}\")
"
```

If `NOT_FOUND`: output `❌ Topic '{slug}' not found. Run /clawexpert status to see available topics.`

**Step 2: Read and display index.md**

Read `{KB}/{slug}/index.md` and display its full contents.

**Step 3: List knowledge nodes**

```bash
python3 -c "
import os, glob
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
nodes = sorted(glob.glob(kb + '/{slug}/nodes/node-*.md'))
for n in nodes:
    print(os.path.basename(n))
print(f'Total: {len(nodes)} nodes')
"
```

Output node list below the index summary:
```
📂 Knowledge nodes ({N} total):
  • node-001.md — {first line of file or filename}
  • node-002.md — ...
```

### `/clawexpert ask <slug> <question>`

Force an answer based solely on the specified topic's knowledge base, without live search. See the "Expert" section for the retrieval workflow.

### `/clawexpert forget <slug>`

Delete all knowledge for a topic.

**Must ask the user to confirm** before executing:
```bash
rm -rf "{KB}/{slug}"
```

### `/clawexpert export <slug>`

Export a topic's knowledge tree as a single Markdown file.

Steps:
1. Read `{KB}/{slug}/index.md` as the header
2. Read all `{KB}/{slug}/nodes/node-*.md` in filename order
3. Join with `---` separators
4. Write to `{KB}/{slug}/export-{YYYY-MM-DD}.md`
5. Tell the user the export path

### `/clawexpert import <filepath> [--topic <slug>]`

Import a local PDF file directly into a topic's knowledge base, bypassing the search phase. Text is extracted from the file and a knowledge node is written immediately.

```
/clawexpert import ~/Downloads/attention-is-all-you-need.pdf --topic transformer
/clawexpert import /path/to/textbook.pdf
```

Parameters:
- `--topic <slug>`: Target topic slug. If omitted, ClawExpert lists existing topics and prompts for selection. A new topic is created if the slug doesn't exist (with user confirmation).

### `/clawexpert proactive [off|suggest|auto]`

View or change the proactive learning mode.

- No argument → display current mode and queue size
- `off` → disable all proactive logic (no topic tracking, no suggestions)
- `suggest` → enable suggestions: gaps are recorded, shown at session start as recommendations
- `auto` → enable auto-learning: top-priority gap is automatically learned at session start

Read current mode:
```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
mode = json.load(open(state)).get('proactive_mode', 'off') if os.path.exists(state) else 'off'
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
q_path = kb + '/_proactive_queue.json'
q = json.load(open(q_path)).get('queue', []) if os.path.exists(q_path) else []
print(f'mode={mode} queue={len(q)}')
"
```

Write new mode (replace `{MODE}` with `off`, `suggest`, or `auto`):
```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
d = json.load(open(state)) if os.path.exists(state) else {}
d['proactive_mode'] = '{MODE}'
json.dump(d, open(state, 'w'), indent=2)
print('Proactive mode set to: {MODE}')
"
```

Output after change:
```
Proactive mode: suggest
Token cost: +~200 tokens/session (queue scan + display only)

suggest: +~200 tokens/session (queue scan + display only)
auto:    +N × learn cost/session (depends on queue size; each learn run can take minutes)
```

### `/clawexpert proactive skip`

Clear the current proactive learning queue without executing any learns.

```bash
python3 -c "
import json, os
path = os.path.expanduser(os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', '~/.openclaw/workspace/knowledge')) + '/_proactive_queue.json'
data = json.load(open(path)) if os.path.exists(path) else {}
data['queue'] = []
data['updated'] = __import__('datetime').datetime.utcnow().isoformat() + 'Z'
json.dump(data, open(path, 'w'), indent=2)
print('Queue cleared.')
"
```

### `/clawexpert radar`

Manually trigger a radar scan across all L1 categories. See **V. Expert → Radar Scan** for the full workflow.

---

## Source Priority Standards

All learning and retrieval operations must apply the following four-tier source ranking. Higher tiers take precedence when sources conflict or must be selected.

### Tier Definitions

| Tier | Name | Characteristics |
|------|------|-----------------|
| **T1** | Primary authoritative | Peer-reviewed / institutionally validated / officially published |
| **T2** | Institutional professional | Editorial standards from professional institutions; close to primary |
| **T3** | Quality specialist media | Fact-checked, professionally edited, domain-specific |
| **T4** | Reference only | Background orientation; do not use as the sole basis for key claims |
| **Discard** | — | Content farms, SEO sites, unattributed, clear commercial bias |

### By Domain

**Science & Technology**
- T1: Peer-reviewed papers (arXiv, Nature, Science, IEEE, ACM, NEJM, Cell); official technical standards (RFC, W3C, ISO/IEC)
- T2: Official technical documentation (language specs); major company engineering blogs (Google AI, Meta Research, DeepMind); government research agency reports (NIH, NASA, CERN)
- T3: IEEE Spectrum, MIT Technology Review, Wired
- T4: Wikipedia (concept orientation only — not citable as evidence)

**Economics & Finance**
- T1: Government statistics (National Bureau of Statistics, Fed, ECB, IMF, World Bank); academic papers (NBER, SSRN, AER, QJE, Journal of Finance)
- T2: Regulatory filings and announcements (SEC, CSRC, CBIRC annual reports); major financial institution research reports (Goldman Sachs, JP Morgan Research — note conflict-of-interest risk)
- T3: FT, WSJ, Bloomberg, Reuters, The Economist
- T4: Financial news portals, earnings commentary articles

**Humanities, History & Social Sciences**
- T1: Primary historical documents, government archives, original survey data; peer-reviewed academic journals (JSTOR-indexed, leading history/sociology journals)
- T2: University press publications; major think tank reports (Brookings, RAND, DRC)
- T3: Quality newspaper opinion/analysis (NYT, Guardian, in-depth investigative pieces); academic blogs written by scholars (LSE Blog, VoxEU)
- T4: Popular history/culture media (cross-verify with T1/T2)

**Law & Policy**
- T1: Legal primary texts (statutes, court decisions, treaty texts); official policy documents (full text of regulations)
- T2: Leading law journals; legislative working papers
- T3: Specialist legal media; law firm analysis reports (note: not legal advice)
- T4: Legal explainer articles

**Medicine & Health**
- T1: Systematic reviews and meta-analyses (Cochrane Library); top clinical journals (NEJM, Lancet, JAMA, BMJ); official health guidelines (WHO, CDC, NIH)
- T2: Hospital and research institution clinical study reports
- T3: Science, Nature News & Views, specialist medical journalism
- T4: Health popularization articles (only if backed by T1/T2 sources)

### Cross-Domain Rules

1. Within the same tier: institutional primary source > third-party reporting; raw data present > conclusions only; recent (within 2 years) > outdated (except canonical references)
2. When media reports on a study, locate the original paper — the media report is demoted to T3/T4 reference
3. Multiple independent sources converging on the same conclusion outweighs a single source
4. Preprints (e.g., arXiv before peer review): treat as T1.5 — high credibility but flag as "not yet peer-reviewed" in node conclusions
5. Official institutional social media accounts (e.g., central bank official accounts, WHO on Twitter/X): treat as T2 — represents official position but lacks the editorial review of formal publications

---

## II. Learner

Upon receiving `/clawexpert learn <topic>`, execute the following steps strictly in order.

### Step 1: Initialization

Immediately output to the user: `🚀 [0%] Initializing: "{topic}"...`

**Category system check** (run before learning):

```bash
ls "{KB}/_categories.json" 2>/dev/null
```

- File exists → Read the L1 category list, continue
- File not found → Guide the user through first-time setup:

```
Welcome to ClawExpert! First-time setup requires you to define the top-level (L1) categories for your knowledge base.

Suggested categories: Science & Technology / Economics & Finance / Humanities & Social Sciences / History & Geography / Medicine & Health / Law & Politics / Arts & Culture

Please enter your L1 categories (comma-separated):
```

After receiving user input, write to `{KB}/_categories.json`:
```json
{
  "version": 1,
  "created": "{ISO 8601 当前时间}",
  "categories": [
    {"id": "sci-tech", "label": "科学技术"},
    {"id": "economics", "label": "经济金融"}
  ]
}
```
(`id` is auto-generated from the label: lowercased + spaces converted to hyphens + non-ASCII removed, e.g. "科学技术" → `sci-tech` — model should choose a reasonable name)

---

**Slug generation rules**:
- Lowercase
- Convert spaces and punctuation to hyphens
- Remove non-displayable special characters (keep Chinese/English characters, digits, hyphens)
- Truncate to 60 characters
- Example: "RL Reasoning 最新进展" → `rl-reasoning-最新进展`

**Conflict check (same name)**:
```bash
# Step 1: Check if it exists
ls "{KB}/{slug}/meta.json" 2>/dev/null

# Step 2: If it exists, read the status
cat "{KB}/{slug}/meta.json"
```
- File not found → Proceed to cross-topic check
- Exists and JSON `status` field = `"learning"` → Inform user "This topic is currently being learned, please wait for it to finish", abort
- Exists and `status` = `"complete"` → Ask user whether to deepen learning (equivalent to `--deepen`)
- Exists and `status` = `"partial"` → Continue (treat this learn as a supplement)

**Conflict check (cross-topic similarity)** (run after same-name check passes):

```bash
# Scan all existing topics' meta.json
ls "{KB}/*/meta.json" 2>/dev/null
```

Read the `topic` and `keywords` fields from each meta.json and determine whether the new topic heavily overlaps with any existing topic in core subject area (semantically similar topic name + large keyword overlap).

When high overlap is detected, prompt the user:
```
Found a related existing topic: {existing topic name} ({slug})
Would you like to run --deepen on it instead of creating a new entry?
- Enter y: Run --deepen on the existing topic (recommended — avoids duplicate learning)
- Enter n: Continue creating a new independent knowledge base
```

No overlap, or user chooses to create new → Continue with subsequent steps.

**Create directories and write initial meta.json via bundled script**:
```bash
python3 "{SCRIPT_DIR}/init_topic.py" \
  --kb "{KB}" \
  --topic "{user's original topic name as entered}" \
  --slug "{slug}" \
  --max-hours {--hours parameter, default 2}
```

The script creates:
- `{KB}/{slug}/raw/web/`
- `{KB}/{slug}/raw/pdf/`
- `{KB}/{slug}/nodes/`
- `{KB}/{slug}/meta.json`

**Initialize proactive mode (first-time only)**:

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
if not os.path.exists(state):
    os.makedirs(os.path.dirname(state), exist_ok=True)
    json.dump({'proactive_mode': 'off'}, open(state, 'w'), indent=2)
    print('init')
else:
    mode = json.load(open(state)).get('proactive_mode', 'off')
    print('exists:' + mode)
"
```

- Output `init` → first time setup: tell the user: `💡 Proactive learning: off. Run /clawexpert proactive suggest to enable gap tracking and learning suggestions.`
- Output `exists:{mode}` → already configured, skip silently

After completing the above, output to the user: `✅ [5%] Initialized. slug={slug}`

⚠️ **Do NOT stop here. Immediately proceed to Step 2.**

### Step 2: Task Decomposition

Immediately output to the user: `🧩 [5%] Decomposing topic into subtopics...`

**Autonomously decide the number of subtopics** based on topic complexity (min 4, no hard upper limit):
- Broad topic (spanning multiple domains/dimensions) → decompose into more subtopics
- Focused topic (single technology/event/product) → closer to the minimum of 4

For each subtopic, determine:
- `id`: short English identifier (e.g. `grpo-vs-ppo`)
- `label`: human-readable title (e.g. "GRPO vs PPO Comparative Analysis")
- `keywords`: 3–5 search keywords (mix of languages as appropriate); **always include at least one book-oriented keyword** (e.g. the title of a canonical book on this subtopic, or `{topic} textbook`)
- `search_angles`: 2–3 search angle descriptions; **always include one angle targeting book sources** (e.g. "landmark books and textbooks: {BookTitle} chapters, author name + pdf")

Decomposition principles:
- Subtopics must not have significant content overlap; together they should cover the core aspects of the topic
- Each subtopic should be focused enough to be deeply covered within 5–8 search rounds
- Prioritize coverage of: core concepts, major methods/frameworks, representative work, comparative analysis, application scenarios
- **Temporal span rule**: If the topic name or description contains words indicating a time span across multiple phases (e.g., rise and fall / 兴衰 / history of / 演变 / before and after / establishment and collapse / 建立与瓦解), each distinct historical phase or stage **must** be decomposed into a separate subtopic — do not merge different phases into one subtopic

**Align subtopic count with LIMIT**: Read the `maxChildrenPerAgent` value from `openclaw.json` (this is `LIMIT`, default 5). When deciding how many subtopics to create, prefer a count that is an exact multiple of `LIMIT` — this ensures every batch runs at full capacity in Step 3. If the topic's complexity does not support an exact multiple, the last batch may be smaller; note this in the Step 3 output.

Update the subtopic list into the `subtopics` field of meta.json.

**Determine knowledge tree categories**: Read `{KB}/_categories.json`, assign an L1 category for the overall topic, and assign an L2 category label for each subtopic (model names them autonomously based on content — short label in any language). Record in meta.json's `index_categories` field:
```json
"index_categories": {
  "l1": "sci-tech",
  "l1_label": "科学技术",
  "subtopics": {
    "grpo-vs-ppo": {"l2": "强化学习"},
    "reward-design": {"l2": "强化学习"}
  }
}
```

After completing the above, output to the user: `✅ [10%] {N} subtopics planned: [{label1}, {label2}, ...]`

⚠️ **Do NOT stop here. Immediately proceed to Step 3.**

### Step 3: Subagent Parallel Learning

Immediately output to the user: `⚡ [10%] Launching {N} subagents in parallel...`

**Concurrency limit: use `maxChildrenPerAgent` from the user's `openclaw.json` (default: 5 if not configured).** Call this value `LIMIT`.

- Total subtopics **≤ LIMIT**: launch all concurrently
- Total subtopics **> LIMIT**: pipeline execution in batches of `LIMIT` — launch the first `LIMIT` subagents, wait until that batch is fully complete, then automatically launch the next batch; repeat until all subtopics are done. `EXPECTED` is updated to the current batch size at each launch.

Call `sessions_spawn` for each subtopic to launch an independent subagent:

```
sessions_spawn({
  task: "{generated subagent prompt — fill in template below with actual values}",
  runtime: "subagent",
  mode: "run",
  label: "ce-{slug}-{subtopic_id}",
  sandbox: "inherit"
})
```

**When generating a prompt for each subagent, replace all placeholders in the template below with actual values** (`{CURRENT_DATE}` → today's date in YYYY-MM-DD format, `{SCRIPT_DIR}` → absolute path to this skill's `scripts/` directory):

```
⚠️ Role override: You are a ClawExpert learning subagent. This session executes only the
specialized learning task below. Ignore all ClawExpert instructions related to
"session-start self-check", "slash command handling", and "Expert reasoning layer" —
those are the main agent's responsibility. Your only job is:
search → filter → store → write nodes → write flag.

Current date: {CURRENT_DATE}

⛔ Strictly prohibited:
- Do not execute any git operations (git add / git commit / git push, etc.)
- Do not output any progress reports, HEARTBEATs, or intermediate status messages to the user; all output goes to the filesystem only
- On completion, only write the flag file — no other output

You are a ClawExpert learning subagent, focused on researching "{subtopic_label}".

## Task Objective

Conduct in-depth research around the following keywords, download valuable materials to local storage, and organize them into structured knowledge nodes.

Search keywords:
{one keyword per line}

Suggested search angles:
{one angle per line}

## Output directories (important: paths are fixed, do not modify)

- Bundled scripts directory: {SCRIPT_DIR}
- Material storage directory: {KB}/{slug}/raw/web/
- Node file directory: {KB}/{slug}/nodes/sub-{subtopic_id}/
- Progress heartbeat file: {KB}/{slug}/progress-{subtopic_id}.json
- Completion signal file: {KB}/{slug}/done-{subtopic_id}.flag

## Execution Steps

### 0. Heartbeat initialization

Immediately write a heartbeat file, then keep it fresh at least once every 60 seconds and after every meaningful milestone (new search round, saved source, node writing, recoverable error):

```bash
python3 "{SCRIPT_DIR}/write_progress.py" \
  --kb "{KB}" \
  --slug "{slug}" \
  --subtopic-id "{subtopic_id}" \
  --status running \
  --search-round 0 \
  --sources-found 0 \
  --sources-saved 0
```

### 1. Multi-round Search

Use the workspace's configured search path for 5–8 rounds of search. If the built-in `web_search` tool is unavailable or disabled, immediately switch to the workspace fallback search skill instead of retrying the unavailable tool. If no workspace fallback is configured, open Google directly in the browser:
```
https://www.google.com/search?q={encoded_query}
```
Read the results page to identify high-value URLs, then collect them for Step 2.

Vary each round's angle:
- Use different keyword combinations
- Alternate between languages
- Vary search qualifiers (e.g. add "paper", "tutorial", "2025", "comparison", etc.)
- Approach from different perspectives (principles / applications / comparisons / latest developments / critiques / limitations)

### 2. Content Retrieval

For valuable pages found in search results, use web_fetch to retrieve the full text.

### 3. Quality Filtering

Each piece of material must simultaneously satisfy all of the following conditions, or be discarded:
1. Body text length > 300 words (excludes pure navigation pages and ad pages)
2. Contains specific data, conclusions, methodology, or academic citations (excludes vague descriptions)
3. Source domain is trustworthy (excludes content farms and pure SEO sites)
4. Has substantive content overlap with the subtopic keywords (not just a title match)

### 4. Material Storage

Write materials that pass the filter to local files.

#### ⚠️ File naming — MANDATORY

Every stored file (web or PDF) **MUST** be named using the **first 6 hex characters of the source URL's SHA-256 hash**. Descriptive names are strictly forbidden.

```bash
hash=$(echo -n "{SOURCE_URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6)
# Result example: a3f9c1
# Web file:  a3f9c1.md   — NEVER use a descriptive name like "attention-paper.md"
# PDF binary: a3f9c1.pdf  — NEVER use a descriptive name like "attention-is-all-you-need.pdf"
# PDF extracted: a3f9c1.md (or a3f9c1/_index.md for large files)
```

Existence check before writing (skip if already exists):
```bash
ls "{KB}/{slug}/raw/web/${hash}.md" 2>/dev/null           # web
ls "{KB}/{slug}/raw/pdf/${hash}" 2>/dev/null || \
  ls "{KB}/{slug}/raw/pdf/${hash}.md" 2>/dev/null          # pdf
```

#### Routing decision

Before storing, determine the source type:

1. **Direct PDF URL** — URL ends in `.pdf`, or `curl -I` shows `Content-Type: application/pdf` → PDF workflow using this URL directly
2. **Academic paper abstract page** — construct the PDF URL, then use PDF workflow:
   - `arxiv.org/abs/{id}` → `https://arxiv.org/pdf/{id}.pdf`
   - `aclanthology.org/{id}` → `https://aclanthology.org/{id}.pdf`
   - `openreview.net/forum?id={id}` → scan fetched HTML for a PDF download link
   - Other conference/journal pages (NeurIPS, ICML, ICLR, AAAI, CVPR, ECCV, ACL, EMNLP, etc.) → scan fetched HTML for a `.pdf` link
   - Use the **PDF URL** as the hash source and `source_url` in frontmatter
3. **Everything else** → web page workflow, store under `raw/web/`

---

**Web page** (routing case 3) → fetch with `web_fetch`, store under `raw/web/`.

**PDF** (routing case 1 or 2) → follow the complete PDF workflow below.

---

#### PDF Processing Workflow

##### Step A — Compute hash and check existence

```bash
hash=$(echo -n "{PDF_URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6)
ls "{KB}/{slug}/raw/pdf/${hash}" 2>/dev/null || ls "{KB}/{slug}/raw/pdf/${hash}.md" 2>/dev/null
```
If either exists, skip — do not re-download.

##### Step B — Download to local

```bash
local_pdf="{KB}/{slug}/raw/pdf/${hash}.pdf"

# Primary: curl (follows redirects, handles most PDF URLs)
curl -L --max-filesize 104857600 -o "${local_pdf}" "{PDF_URL}" 2>/dev/null
```

If curl exits non-zero (download failed or URL is a landing page, not a direct PDF):
1. Use `web_fetch` on the URL to retrieve the HTML page
2. Extract the direct PDF download link from the page content
3. Retry `curl -L` on the extracted direct link

If still no local file after the above, skip this source.

##### Step C — Check size and page count

```bash
python3 -c "
import re, os, sys
path = sys.argv[1]
size_mb = os.path.getsize(path) / (1024 * 1024)

# Pure-Python page count: read PDF structure bytes, no external deps needed
page_count = 0
try:
    with open(path, 'rb') as f:
        data = f.read(min(os.path.getsize(path), 500_000))
    matches = re.findall(rb'/Count\s+(\d+)', data)
    if matches:
        page_count = max(int(m) for m in matches)
except Exception:
    pass
if page_count == 0:
    page_count = max(1, int(size_mb * 20))  # fallback estimate: ~50KB/page

print(f'{size_mb:.1f}MB {page_count}pages')
" "${local_pdf}"
```

##### Step D — Route by size

| Condition | Path |
|-----------|------|
| ≤ 20 MB **and** ≤ 20 pages | **Small** — full pdf tool call |
| ≤ 20 MB **and** 21–100 pages | **Medium** — sectioned pdf tool call |
| > 50 MB **or** > 100 pages | **Large** — Python full-text extraction |

---

##### Small PDF path (≤ 20 MB, ≤ 20 pages)

Call the `pdf` tool on the **local path**. **Do NOT pass a `model` parameter** — always let the system default handle routing. Specifying an explicit model almost always fails due to missing keys or quota limits.

Use this extraction prompt (pass as `prompt`; do not pass `model`):
> Extract the full content of this document in Markdown format. For all text sections: reproduce content faithfully. For all figures, charts, tables, and diagrams: describe their key data points, axis labels, legends, and main conclusions in plain text.

If the call fails → retry once with the same bare call.
If it fails again → fall through to **Python fallback** below.

Add `extraction_method: pdf_tool` to frontmatter. If no figures/charts reported: `has_images: false`; otherwise `has_images: true`. For scanned PDFs (no text layer): also add `scanned: true`.

---

##### Medium PDF path (21–100 pages)

Build a combined page-range string covering the key sections. Given total page count N:

```
opening  = "1-{min(8, N)}"
middle   = "{max(9, N//2 - 4)}-{min(N-8, N//2 + 5)}"
closing  = "{max(N-7, 9)}-{N}"
pages_arg = "{opening},{middle},{closing}"   # e.g. "1-8,21-30,43-50"
```

Call the `pdf` tool once on the **local path** with `pages: "{pages_arg}"` and the same extraction prompt above. **Do NOT pass `model`.**

Prefix the extracted content with:
```
[Partial extraction: pages {pages_arg} of {N} total. Key sections only — use Python fallback for full text.]
```

If the call fails → retry once → fall through to Python fallback.

Add `extraction_method: pdf_tool_partial` and `page_count: {N}` to frontmatter.

---

##### Large PDF / Python fallback (> 50 MB or > 100 pages, or pdf tool failed)

```bash
python3 -c "
import sys, subprocess

path = sys.argv[1]
text = ''

try:
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        text = '\n\n'.join(page.extract_text() or '' for page in pdf.pages)
except ImportError:
    # pdftotext (poppler-utils) — commonly available on macOS/Linux
    result = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True)
    if result.returncode == 0:
        text = result.stdout
    else:
        print('ERROR: no PDF extraction tool available', file=sys.stderr)
        sys.exit(1)

print(text)
" "${local_pdf}"
```

After extraction, write the result to the correct path — **do not create any other directory (e.g. `processed/`)**:

```bash
out_md="{KB}/{slug}/raw/pdf/${hash}.md"
```

Construct the file with frontmatter + extracted body, then write to `${out_md}`:
```
---
source_url: {PDF_URL}
title: {title}
fetched_at: {ISO 8601}
topic: {slug}
subtopic: {SUBTOPIC_ID}
word_count: {estimated}
extraction_method: text_only
has_images: false
---

{extracted text}
```

Add `extraction_method: text_only` to frontmatter. Image/figure content will be absent.

After writing, check the extracted word count:
- **< 500 words**: the PDF is image-dominant (e.g. papers with many full-page figures). Add `sparse_text: true` to frontmatter. Do NOT split, do NOT supplement with AI-generated content — write the extracted text as-is in a single `${hash}.md`. Note the limitation in the node's Source Evidence entry.
- **500–5000 words**: write as a single `${hash}.md`, no splitting needed.
- **> 5000 words**: apply the **large-file sub-tree** splitting below (parts + `_index.md`).

---

#### File naming (web and PDF)

First 6 hex characters of the URL's SHA-256 hash:
```bash
echo -n "{URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6
```

Existence check before writing:
```bash
ls "{KB}/{slug}/raw/web/{hash}.md" 2>/dev/null    # web
ls "{KB}/{slug}/raw/pdf/{hash}" 2>/dev/null        # pdf (may be dir or .md)
```

#### File format

```
---
source_url: {full URL}
title: {page title or filename}
fetched_at: {ISO 8601 time}
topic: {slug}
subtopic: {subtopic_id}
word_count: {estimated body word count}
extraction_method: {web_fetch | pdf_tool | pdf_tool_partial | text_only}   # omit for web pages
has_images: {true | false}          # PDF only
page_count: {N}                     # PDF medium/large only
scanned: true                       # PDF only, if no text layer detected
---

{cleaned body content}
```

⚠️ **Fidelity rule — applies to ALL raw/ files without exception**:
The `raw/` directory stores **faithful reproductions of source material only**. Never write AI-generated summaries, paraphrases, curated quote collections, or analytical notes into raw files. If the extracted text is sparse or low quality, write it as-is and mark it accordingly — do not compensate by synthesizing content from your own knowledge.

Cleaning rules:
- Web page: remove navigation bars, sidebars, footers, ads, cookie banners; preserve headings, paragraphs, lists, tables, code blocks; preserve link text (URLs may be removed)
- PDF (`pdf_tool` / `pdf_tool_partial`): write model output as-is — do not strip further; image content already described inline as text
- PDF (`text_only`): apply same cleaning rules as web pages; image/figure content absent; write the raw extracted text verbatim
- Scanned PDF: `pdf_tool` attempts vision-based description; content quality may be limited

**Large file sub-tree** (apply after writing, for both web and PDF):

After writing, estimate word count. If word count > 5000:

1. Create a directory to replace the single file:
   ```bash
   mkdir -p "{KB}/{slug}/raw/{type}/{hash}"
   ```

2. Analyze document structure — identify chapters, sections, or major headings.
   - **If the document has clear logical structure** (numbered sections, chapter headings, titled subsections) → **split by logical boundaries first** — each major section becomes one part (merge very short sections < 500 words with the next)
   - **If no clear structure** → split into chunks of ~5000 words each, cutting at paragraph boundaries (never mid-sentence or mid-paragraph)
   - Either way: keep each part between 2000–8000 words; if a logical section exceeds 8000 words, split it further at the next heading level

3. Write `{KB}/{slug}/raw/{type}/{hash}/_index.md`:
   ```
   ---
   source_url: {full URL or local path}
   title: {title}
   fetched_at: {ISO 8601 time}
   topic: {slug}
   word_count: {total}
   parts: {number of part files}
   extraction_method: {web_fetch | pdf_tool | text_only}
   ---

   ## Document Overview
   {2–4 sentences summarizing the full document's scope, main argument, and key findings}

   ## Part Index
   - [part-001](part-001.md) — {section title} | {1 sentence describing the specific content: what concepts, data, or conclusions this part contains}
   - [part-002](part-002.md) — {section title} | {1 sentence describing the specific content}
   ...
   ```
   ⚠️ The Part Index summary MUST be a genuine semantic description written after reading the part — NOT the first few words of the text, NOT "chunk N". A QA subagent uses these summaries to decide which part to read without reading all parts.

4. Write each part as `part-001.md`, `part-002.md`, etc. Each part should begin and end at a natural boundary (heading or paragraph break); include ~200-word overlap with the previous part at the start of each part (except part-001) to avoid conclusions being cut mid-sentence.

5. Delete the original single-file `{hash}.md` (only the directory `{hash}/` remains).

When referencing a large-file source in node.md, point to `{hash}/_index.md`; reference specific parts as `{hash}/part-00N.md` when citing a specific section.

### 5. Conclusion Extraction and Node Writing

Create the node directory:
```bash
mkdir -p "{KB}/{slug}/nodes/sub-{subtopic_id}"
```

Write the node file `{KB}/{slug}/nodes/sub-{subtopic_id}/node.md`:

```
---
id: {subtopic_id}-{current timestamp in ms}-001
parent: root
label: {subtopic_label}
type: topic
depth: 2
confidence: {>=3 sources: high | 1-2 sources: medium | 0 sources: low}
last_updated: {YYYY-MM-DD}
source_count: {number of valid sources}
---

## Summary
{2–5 sentences summarizing the core findings for this subtopic}

## Key Conclusions
- {Conclusion 1} ([source title](../../raw/web/{hash}.md))
- {Conclusion 2} ([source title](../../raw/pdf/{hash}/_index.md))

## Source Evidence
- [{web source title}](../../raw/web/{hash}.md) — {one sentence explaining the core value of this source}
- [{pdf single-file title}](../../raw/pdf/{hash}.md) — {one sentence}
- [{pdf multi-part title}](../../raw/pdf/{hash}/_index.md) — {one sentence}; key data in [part-002](../../raw/pdf/{hash}/part-002.md)

## Analytical Framework (if applicable)
{If this subtopic involves a reusable analytical framework or methodology, describe it here}

## Further Directions
- [ ] {A related direction or open question discovered during research that falls outside this subtopic's scope — worth exploring in a future --deepen run}
- [ ] {Another such direction, if any}
```

If no out-of-scope directions were found, omit the `## Further Directions` section entirely.

If the content volume is large, multiple node files may be created: `node.md`, `node-detail-001.md`, ...

### 6. Time Control

Before each search round, read meta.json to check for timeout:
```bash
cat "{KB}/{slug}/meta.json"
```
Read the `learning_sessions[0].started` field and calculate elapsed time.
If more than {max_hours} hours have elapsed, stop searching and proceed to Step 7.

### 7. Completion Signal

Write the final flag using the bundled script and remove the progress heartbeat:

```bash
python3 "{SCRIPT_DIR}/write_flag.py" \
  --kb "{KB}" \
  --slug "{slug}" \
  --subtopic-id "{subtopic_id}" \
  --status done \
  --sources-added ACTUAL_COUNT \
  --node-file "{KB}/{slug}/nodes/sub-{subtopic_id}/node.md" \
  --cleanup-progress
```

Replace `ACTUAL_COUNT` with the actual number of valid materials downloaded (integer); all other placeholders are replaced with real values when the subagent prompt is generated.

If the subtopic exhausts high-quality sources or encounters a hard failure, still write a terminal flag with status `partial`, `failed`, `timeout`, or `no_results` and include `--cleanup-progress` so the main agent can continue.

## Notes

- Verify each URL is reachable before calling web_fetch
- Apply the four-tier source priority system when selecting and filtering sources:
  - T1 (highest): peer-reviewed papers, official government/standards documents, primary legal texts, clinical systematic reviews
  - T2: institutional technical docs, major org research reports, university press, regulatory filings
  - T3: reputable specialist media (IEEE Spectrum, FT, Bloomberg, MIT Tech Review, Reuters, Nature News)
  - T4: quality general media — background reference only; cross-verify with T1/T2 before citing
  - Discard: content farms, SEO sites, unattributed content, sites with clear commercial bias
- Within the same tier: institutional primary source > third-party reporting; raw data > conclusions only; recent (within 2 years) > outdated
- When media reports a study, find the original paper — the media report drops to T3/T4
- Preprints (arXiv pre-review): treat as high-credibility but flag as "not yet peer-reviewed" in node conclusions
- If a keyword yields no valuable results after 2 search rounds, change the angle and continue — do not get stuck on fruitless searches
- Conclusions must be specific, including numbers, comparisons, and method names — not vague descriptions
```

After all subagents are launched in parallel, record the expected number of flag files (= number of subagents launched in the current batch). A subtopic counts as finished for monitoring purposes once its `done-{subtopic}.flag` exists, regardless of whether the status inside the flag is `done`, `partial`, `failed`, `timeout`, or `no_results`.

⚠️ **Do NOT stop here. Do NOT ask the user anything. Do NOT wait for user input. Immediately proceed to Step 4 in the same turn.**

### Step 4: Progress Monitoring

Immediately output to the user: `⏳ [10%] Monitoring subagent progress...`

Once all subagents are launched, immediately enter the monitoring loop. **This loop must keep running until the exit condition is met — do not wait for the user to send a message.**

```
EXPECTED = {number of subagents launched in the current batch}

Loop:
  1. Wait 30 seconds
     bash: sleep 30

  2. Inspect flags + heartbeat files
     bash: python3 "{SCRIPT_DIR}/monitor_subtopics.py" --kb "{KB}" --slug "{slug}" --stall-seconds 600
     → parse JSON result:
       - DONE = result.done
       - STALLED = result.stalled
       - ACTIVE = result.active

  3. Output current progress to the user (required every iteration):
     "⏳ [X%] Subtopics completed: {DONE}/{EXPECTED}"
     where X = 10 + round(DONE / EXPECTED × 50)

  4. Stall handling:
     - If any subtopic appears in `STALLED`, treat it as hung
     - If the corresponding subagent is still alive, kill it
     - Immediately write a terminal flag with `write_flag.py` using status `timeout` or `failed` and `--cleanup-progress`
     - Then continue the monitoring loop; do not wait forever for a missing heartbeat to recover itself

  5. Evaluate:
     - DONE >= EXPECTED → ⚠️ **IMMEDIATELY execute Step 5 — no pause, no output, no user confirmation. Do not return control to the user. Treat this as a hard goto.**
     - Current time - meta.json started > 2 × max_hours → timeout, same as above: immediately execute Step 5
     - Otherwise → continue loop
```

⚠️ **Critical**: The moment the exit condition is met, output one line then immediately execute Step 5 without pausing:
`🔀 [60%] All subtopics complete. Starting merge...`

On timeout, record which subtopics did not complete (missing flag files) and explain in the report during the merge step.

### Step 5: Knowledge Organization (Merge)

Before starting, output:
`📋 [60%] Starting knowledge merge for: {topic}`

**5.1 Collect output**

Immediately output to the user: `📂 [62%] Collecting subtopic outputs...`

Collect merge inputs with the bundled script:

```bash
python3 "{SCRIPT_DIR}/prepare_merge.py" --kb "{KB}" --slug "{slug}"
```

Read all `{KB}/{slug}/nodes/sub-*/node*.md` files and all flag files using the script output as the canonical manifest.

After completing the above, output to the user: `✅ [65%] Collected {N} node files from {M} subtopics.`

**5.2 Deduplication and consolidation**

Immediately output to the user: `🔍 [65%] Checking for duplicates and contradictions...`

- Check whether any conclusions are duplicated or contradictory across subtopic nodes
- Merge similar conclusions, preserving all source citations
- Run node relationship analysis before writing formal nodes:

```bash
python3 "{SCRIPT_DIR}/suggest_node_merges.py" --kb "{KB}" --slug "{slug}"
```

- Treat the script output as a **candidate list**, not a final verdict. The script only recalls likely `merge_candidate`, `parent_child_candidate`, and `related_candidate` pairs. The main agent must make the final semantic judgment.
- If two or more candidate nodes are semantically close (same core concept expressed with different wording, overlapping summaries, overlapping conclusions, or near-duplicate scope), prefer merging them into **one formal node** instead of writing parallel fragmented nodes
- When merging similar nodes:
  - Choose the clearest label as the canonical node label
  - Keep all non-duplicative conclusions under that single node
  - Preserve all source citations from every merged candidate
  - Record alternate phrasings in frontmatter as `aliases: a | b | c`
  - Record one stable retrieval phrase in `canonical_intent: ...`
- If the candidate pair is better interpreted as hierarchy than synonymy, do **not** merge it. Keep one node as the parent, one as the child, and connect them in `Related Nodes`.
- Goal: optimize for future retrieval. User questions rarely match the original subtopic wording exactly, so semantically adjacent material should be consolidated into one retrievable node whenever possible
- Mark contradictory conclusions side-by-side with the annotation `⚠️ Disputed`

After completing the above, output to the user: `✅ [70%] Deduplication done.`

**5.3 Build the knowledge tree**

Immediately output to the user: `🌲 [70%] Building knowledge tree structure...`

Analyze the hierarchical relationships between nodes:
- Which are parallel (sibling nodes)
- Which have parent-child relationships
- If there are analytical frameworks, identify them as `type: framework` nodes

After completing the above, output to the user: `✅ [75%] Tree structure done.`

**5.4 Write formal nodes**

Immediately output to the user: `✍️ [75%] Writing formal nodes...`

Rewrite `nodes/sub-{id}/node*.md` as formal nodes `nodes/node-{seq}.md` (seq starting at 001):

```markdown
---
id: node-{seq}
original_id: {subagent's original node ID, preserved for traceability}
parent: {parent node id; use "root" for top-level nodes}
label: {node title}
aliases: {optional inline aliases, e.g. a | b | c}
canonical_intent: {one stable canonical phrasing for retrieval}
scope: {short note describing what this node covers}
type: topic
depth: {hierarchy depth: top-level child node=2, one level below=3}
confidence: high | medium | low
last_updated: {YYYY-MM-DD}
source_count: {number of associated files}
---

## Summary
{Core summary for this node, 2–5 sentences}

## Key Conclusions
- {Conclusion 1}
- {Conclusion 2}

## Source Evidence
- [{source title}](../raw/web/{hash}.md) — {explanation}

## Related Nodes
- Parent: [{label}]({relative path})
- Children: [{label}]({relative path}) (if any)
- Related: [{label}]({relative path}) (if any)
```

**Framework nodes** (type: framework) format:
```markdown
---
id: framework-{seq}
type: framework
parent: root
label: {framework name}
depth: 2
confidence: high
last_updated: {YYYY-MM-DD}
---

## Analysis Dimensions
1. {Dimension 1}: {explanation}
2. {Dimension 2}: {explanation}

## When to Use
When the user asks "{typical question}", apply this framework for structured analysis.

## Application Steps
1. {step}

## Source Basis
- [{source}](../raw/web/{hash}.md)
```

After completing the above, output to the user: `✅ [85%] Written {N} formal nodes.`

**5.5 Generate index.md**

Immediately output to the user: `📄 [85%] Generating index.md...`

```markdown
# {Topic Title}

> Last updated: {YYYY-MM-DD} | Sources: {N} | Nodes: {N}

## Knowledge Tree Overview

- [{node label}](nodes/node-001.md) — {one-sentence summary}
  - [{child node label}](nodes/node-003.md) — {summary}
  - [{child node label}](nodes/node-004.md) — {summary}
- [{node label}](nodes/node-002.md) — {summary}

## Core Findings Summary

1. {Most important global conclusion 1}
2. {Conclusion 2}
3. {Conclusion 3}

## Further Directions

- [ ] {Direction discovered during learning but not yet fully covered 1}
- [ ] {Direction 2}
```

After completing the above, output to the user: `✅ [90%] index.md written.`

**5.6 Update meta.json**

Immediately output to the user: `📝 [90%] Updating meta.json...`

Read the full existing meta.json, modify the following fields, then rewrite the entire file:

- `status` → `"complete"`
- `last_updated` → current ISO 8601 time
- `source_count` → count of source documents under `raw/web/` and `raw/pdf/`
- `node_count` → count of `nodes/node-*.md` files (`ls {KB}/{slug}/nodes/node-*.md 2>/dev/null | wc -l`)
- `learning_sessions[0].finished` → current ISO 8601 time
- `learning_sessions[0].sources_added` → number of new sources added this session
- `status` for each subtopic in the `subtopics` array → read from the corresponding flag file (done/timeout/no_results)

Use the bundled script:
```bash
python3 "{SCRIPT_DIR}/update_meta.py" --kb "{KB}" --slug "{slug}"
```

After completing the above, output to the user: `✅ [93%] meta.json updated.`

**5.7 Clean up temporary files**

Immediately output to the user: `🧹 [93%] Cleaning up temporary files...`

```bash
python3 "{SCRIPT_DIR}/cleanup_topic.py" --kb "{KB}" --slug "{slug}"
```

This cleanup step must also remove every `progress-{subtopic}.json` heartbeat file once the task has a terminal flag.

After completing the above, output to the user: `✅ [95%] Cleanup done.`

**5.8 Rebuild knowledge tree index**

Rebuild the `{KB}/_index/` tree from all learned topics using the bundled script:

```bash
python3 "{SCRIPT_DIR}/rebuild_index.py" --kb "{KB}"
```

**5.8-A: Write / update `{KB}/_index/{l1-id}/{l2-label}/_index.md`**

If the file already exists, read it first, then append this topic's section. Do not overwrite existing topic sections.

Each topic learned in this L2 category gets its own subsection with the following format:

```markdown
# {l2-label}

> {N} topics | {M} total sources | Last updated: {YYYY-MM-DD}

---

## {topic name} (`{slug}`)

> Learned: {YYYY-MM-DD} | Sources: {N} | Nodes: {N}

### Core Summary
{3–5 sentences synthesizing the most important findings from this learning session. Must include: what the topic is, the key mechanism or argument, and the most important empirical finding or conclusion. Do not use vague phrases like "this topic covers X" — state the actual content.}

### Key Conclusions
{5–8 bullet points. Each must be a specific, concrete conclusion — include numbers, names, dates, comparisons where available. Vague conclusions like "X is important" are not acceptable.}
- {Specific conclusion with supporting detail} (→ [{source title}]({relative path to raw file}))
- {Specific conclusion with supporting detail} (→ [{source title}]({relative path to raw file}))

### Knowledge Nodes
{List each node with its label and a one-sentence description of what it covers}
- [{node label}]({relative path to node file}) — {what this node covers}

### Source Abstracts
{One entry per source file downloaded during this learning session. Each entry must be specific enough that the model can decide whether to read the full file without opening it.}
- [{title}]({relative path to raw file}) — {source type and institution} | {date if known} | {2–3 sentences: what this document specifically covers, what key data or claims it contains, what questions it can answer}

### Open Questions
{Questions that emerged during learning but were not fully resolved — copy from index.md "Further Directions"}
- {question or direction}
```

**5.8-B: Write / update `{KB}/_index/_root_index.md`**

If the file already exists, read it in full. Update only the entries that belong to this learning session — do not truncate or overwrite other categories' content.

The root index must give enough information for the model to decide, without reading deeper, whether the knowledge base can answer a given question.

```markdown
# ClawExpert Knowledge Base

> Last updated: {YYYY-MM-DD} | Topics: {N} | Total sources: {N}

## Category Directory

### {L1 label} (`{l1-id}`)

#### {l2-label}
→ [`_index.md`]({l1-id}/{l2-label}/_index.md) | {N} topics | {M} sources

**Topics covered:**
- **{topic name}** (`{slug}`): {2–3 sentence summary of what was learned — specific findings, not just topic description}. Key conclusions: {3–4 bullet points of the most important concrete findings}
  - {specific conclusion}
  - {specific conclusion}
  - {specific conclusion}

## Recent Learning
- {YYYY-MM-DD} **{topic name}** (`{slug}`) → [{l1-label} / {l2-label}]({l1-id}/{l2-label}/_index.md)
```

**Update rules:**
- If an L2 section already exists in `_root_index.md`, append the new topic under it — do not replace the section
- If an L1 section already exists but this L2 does not, add the new L2 subsection under the existing L1
- If neither exists, create the full hierarchy
- Always update the header `Last updated` date and `Topics` / `Total sources` counts
- Prepend new entries to the "Recent Learning" list (most recent first); keep at most 20 entries

**Example — `economics-finance/intl-monetary-history/_index.md`:**

```markdown
# International Monetary History

> 1 topic | 16 total sources | Last updated: 2026-03-21

---

## The Bretton Woods System: Rise and Fall (`bretton-woods-system`)

> Learned: 2026-03-21 | Sources: 16 | Nodes: 5

### Core Summary
The Bretton Woods system (1944–1973) was a post-war fixed exchange rate regime anchored by the U.S. dollar's convertibility to gold at $35/oz, with all other currencies pegged to the dollar. Its fundamental contradiction — the Triffin Dilemma — was that the U.S. had to run persistent deficits to supply global dollar liquidity, which inevitably eroded confidence in dollar-gold convertibility. The system collapsed in stages: Nixon suspended gold convertibility on August 15, 1971, and by March 1973 major currencies had moved to floating rates.

### Key Conclusions
- 44 nations established the system at Bretton Woods, NH in July 1944; the dollar became the sole currency directly convertible to gold (→ [IMF History Overview](bretton-woods-system/raw/web/a1b2c3.md))
- The Triffin Dilemma (identified 1960): structural impossibility of simultaneously providing global liquidity and maintaining gold backing — not fixable by policy (→ [Triffin 1960 Paper](bretton-woods-system/raw/web/d4e5f6.md))
- Vietnam War spending and Great Society programs expanded U.S. deficits through the 1960s; gold reserves fell from ~$20B peak to under $10B by 1971
- France and other countries redeemed dollars for gold 1965–1971, accelerating reserve depletion
- August 15, 1971 "Nixon Shock": unilateral suspension of dollar-gold convertibility
- Smithsonian Agreement (Dec 1971) briefly adjusted parities but failed to restore confidence; floating rates became universal by March 1973

### Knowledge Nodes
- [node-001.md](bretton-woods-system/nodes/node-001.md) — Wartime origins and 1944 negotiations: White Plan vs. Keynes Plan
- [node-002.md](bretton-woods-system/nodes/node-002.md) — Operating mechanism: fixed rates, IMF role, and capital controls
- [node-003.md](bretton-woods-system/nodes/node-003.md) — Triffin Dilemma and structural tensions of the 1960s
- [node-004.md](bretton-woods-system/nodes/node-004.md) — Nixon Shock and Smithsonian Agreement (1971–1973)
- [node-005.md](bretton-woods-system/nodes/node-005.md) — Legacy: the floating rate era and the modern international monetary system

### Source Abstracts
- [Nixon Ends Convertibility of U.S. Dollars to Gold](bretton-woods-system/raw/web/a1b2c3.md) — Federal Reserve History, official historical article, authored by Kenneth Weisbrode, published 2013. Primary focus: the August 15, 1971 "Nixon Shock" announcement. Documents the secret Camp David weekend meeting (August 13–15, 1971) where Nixon and 15 advisors — including Treasury Secretary John Connally and Fed Chair Arthur Burns — decided to close the gold window. Specifies that the U.S. gold stock had fallen from $25B (1949 peak) to $10B by 1971, while foreign dollar claims exceeded $80B. Describes the three simultaneous measures: (1) suspension of gold convertibility, (2) 10% import surcharge, (3) 90-day wage/price freeze. Notes that European markets closed the following Monday in response. Does NOT cover: Smithsonian Agreement details, longer-term consequences, or pre-1971 structural tensions. Use for: exact date and mechanics of the Nixon Shock, key personnel involved, specific gold reserve figures at the time of closure.
- [Triffin Dilemma, or: the Myth of the Triffin Dilemma](bretton-woods-system/raw/web/d4e5f6.md) — BIS Working Paper No. 684, authored by Garber and Svensson, published 2015. Central argument: the Triffin Dilemma was a real structural constraint but its timing was not deterministic — U.S. policy choices (particularly Vietnam War financing and refusal to deflate) accelerated collapse. Contains year-by-year data on U.S. gold reserves (1950–1973), total foreign dollar liabilities, and the ratio between them. Shows the ratio crossed 1:1 (liabilities exceeding reserves) in 1960, consistent with Triffin's original 1960 Senate testimony. Also reviews the academic debate: Eichengreen argues collapse was inevitable; Garber argues it was policy-contingent. Does NOT cover: Smithsonian Agreement or post-1973 floating rate arrangements. Use for: quantitative gold reserve data, Triffin Dilemma mechanics, academic debate on whether collapse was inevitable vs. policy-driven.

### Open Questions
- Could the Bretton Woods system have survived under different U.S. fiscal policies?
- Can SDRs realistically serve as a supranational reserve asset to replace the dollar?
- Does the current dollar-dominant system face analogous Triffin-style structural pressures?
```

**Example — `_root_index.md` entry for the same topic:**

```markdown
### Economics & Finance (`economics-finance`)

#### International Monetary History
→ [`_index.md`](economics-finance/intl-monetary-history/_index.md) | 1 topic | 16 sources

**Topics covered:**
- **The Bretton Woods System: Rise and Fall** (`bretton-woods-system`): Post-war fixed exchange rate system (1944–1973) anchored by dollar-gold convertibility at $35/oz. The Triffin Dilemma — the structural impossibility of supplying global liquidity while maintaining gold backing — made collapse inevitable; the Nixon Shock in 1971 triggered the final unraveling.
  - Dollar pegged to gold at $35/oz; all other currencies pegged to the dollar
  - Triffin Dilemma is an endogenous structural contradiction, not an external shock
  - Nixon Shock (Aug 1971) was the proximate trigger; French gold redemptions were an accelerating factor
```

After completing the above, output to the user: `✅ [97%] Knowledge tree index updated.`

**5.9 Validate topic consistency**

Immediately output to the user: `🧪 [97%] Validating knowledge base consistency...`

Run:
```bash
python3 "{SCRIPT_DIR}/validate_kb.py" --kb "{KB}" --slug "{slug}"
```

If validation reports issues, fix them before Step 6 or explicitly report any residual inconsistency.

After completing the above, output to the user: `✅ [98%] Validation done.`

⚠️ **Do NOT stop here. Immediately proceed to Step 6.**

### Step 6: Write to Memory

Immediately output to the user: `💾 [97%] Writing knowledge base pointer to memory...`

Write a pointer to OpenClaw memory so that future sessions know the location of the knowledge base:

```bash
python3 -c "
import os

kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
memory_dir = os.path.expanduser('~/.openclaw/workspace/memory')
memory_path = os.path.join(memory_dir, 'clawexpert.md')
os.makedirs(memory_dir, exist_ok=True)

content = '''# ClawExpert Knowledge Base

Knowledge base located at: {kb}/_index/_root_index.md

Before answering questions, read the above file to understand the full scope of the knowledge base, then decide whether to retrieve specific category content. Do not answer questions from learned domains using parametric memory directly.
'''.format(kb=kb)

with open(memory_path, 'w') as f:
    f.write(content)
print('memory written:', memory_path)
"
```

After completing the above, output to the user: `✅ [99%] Memory pointer written.`

⚠️ **Do NOT stop here. Immediately proceed to Step 7.**

### Step 7: Completion Report

Output to the user:

```
## Learning Complete: {topic name}

### Summary
- Duration: approx. {N} minutes
- Subtopics: {N}
- Sources downloaded: {N}
- Knowledge nodes: {N}

### Subtopic Completion Status
| Subtopic | Sources | Status |
|----------|---------|--------|
| {label} | {n} | ✅ Complete |
| {label} | {n} | ⏱ Timed out (partial saved) |

### Core Findings
1. {Most important conclusion}
2. {Conclusion 2}
3. {Conclusion 3}

### Suggested Further Directions
- {List of further directions}

Run `/clawexpert show {slug}` to view the full knowledge tree.
```

> After memory is written, the next time a related topic is asked in a new session, the model will detect this knowledge base via `memory_search` and proactively reference it.

---

## III. Importer

### `/clawexpert import` — Full Workflow

Upon receiving `/clawexpert import <filepath> [--topic <slug>]`, execute the following steps.

#### Step 1: Validate file

```bash
test -f "{filepath}" && echo "exists" || echo "not found"
```

- File not found → abort: `Error: file not found: {filepath}`
- Resolve to absolute path:
  ```bash
  filepath=$(python3 -c "import os, sys; print(os.path.abspath(sys.argv[1]))" "{filepath}")
  ```
- Check it is a PDF (extension `.pdf`, or first 4 bytes are `%PDF`) — if not, abort with: `Error: only PDF files are supported.`

#### Step 2: Resolve target topic

- `--topic <slug>` provided:
  - Check `{KB}/{slug}/meta.json` exists
  - Exists → use that topic
  - Not exists → ask: `Topic '{slug}' not found. Create a new topic with this slug? [y/n]`
    - `y` → initialize new topic (create directories + write initial meta.json with `status = "complete"`)
    - `n` → abort
- `--topic` not provided:
  - List existing topics:
    ```bash
    ls "$KNOWLEDGE_DIR" 2>/dev/null
    ```
  - No topics found → ask: `No topics found. Enter a topic name to create one:`; then create it
  - Topics exist → prompt: `Which topic should this file be imported into? Enter slug (or type a new name to create a new topic):`

#### Step 3: Compute hash

For local files, hash is derived from **file content** (not path), so the same file imported twice produces the same hash regardless of where it lives:

```bash
hash=$(openssl dgst -sha256 "{filepath}" | awk '{print $NF}' | cut -c1-6)
```

#### Step 4: Check for duplicate

```bash
ls "{KB}/{slug}/raw/pdf/${hash}" 2>/dev/null || ls "{KB}/{slug}/raw/pdf/${hash}.md" 2>/dev/null
```

If either exists → inform user: `This file has already been imported (hash: {hash}). Skipping.` and abort.

#### Step 5: Copy PDF to KB

```bash
local_pdf="{KB}/{slug}/raw/pdf/${hash}.pdf"
cp "{filepath}" "${local_pdf}"
```

#### Step 6–7: Extract content

Apply the same **PDF processing workflow** used by subagents (size check → Small / Medium / Large path). Key difference: use `source_url: local:{filepath}` in all frontmatter instead of an HTTP URL.

After extraction, write to:
- `{KB}/{slug}/raw/pdf/${hash}.md` — single file (< 5000 words)
- `{KB}/{slug}/raw/pdf/${hash}/` — sub-tree with `_index.md` + `part-*.md` (> 5000 words)

⚠️ **Fidelity rule applies**: write extracted text faithfully; do not supplement with AI-generated content.

#### Step 8: Write node

```bash
mkdir -p "{KB}/{slug}/nodes/import-{hash}"
```

Write `{KB}/{slug}/nodes/import-{hash}/node.md`:

```
---
id: import-{hash}-001
parent: root
label: {title extracted from PDF, or filename without extension}
type: topic
depth: 2
confidence: high
last_updated: {YYYY-MM-DD}
source_count: 1
local_import: true
---

## Summary
{2–5 sentences summarizing the document's core content}

## Key Conclusions
- {Conclusion 1} ([{title}](../../raw/pdf/{hash}/_index.md))

## Source Evidence
- [{title}](../../raw/pdf/{hash}/_index.md) — local import: {one sentence describing the document}

## Analytical Framework (if applicable)
{If this document introduces a reusable framework or methodology, describe it here}

## Further Directions
- [ ] {Out-of-scope directions found while reading, if any}
```

If the extracted file is a single `{hash}.md` (not split), reference it as `../../raw/pdf/{hash}.md` instead.

Omit `## Further Directions` if none were found.

#### Step 9: Update meta.json

Read `{KB}/{slug}/meta.json`, then:

1. Increment `source_count` and `node_count`
2. Add or append to `local_sources` array:
```json
{
  "path": "{filepath}",
  "hash": "{hash}",
  "title": "{title}",
  "imported_at": "{ISO 8601}"
}
```

Write updated meta.json back.

#### Step 10: Update index.md

If `{KB}/{slug}/index.md` exists, append a new node entry under the node list. If it does not exist, create a minimal one:

```markdown
# {topic} — Knowledge Index

## Nodes

- [import-{hash}](nodes/import-{hash}/node.md) — {title}
```

#### Step 11: Output success

```
✅ Import complete
   File:   {filepath}
   Topic:  {slug}
   Hash:   {hash}
   Node:   {KB}/{slug}/nodes/import-{hash}/node.md
   Raw:    {KB}/{slug}/raw/pdf/{hash}[.md or /]
```

---

## IV. Organizer

### Deepening Learning (--deepen)

When executing `/clawexpert learn --deepen <slug>`:

1. Run gap analysis to generate both **breadth** and **depth** work items:

```bash
KB="${CLAWEXPERT_KNOWLEDGE_DIR:-$HOME/.openclaw/workspace/knowledge}"
SCRIPT_DIR="${CLAWEXPERT_SCRIPT_DIR:-$HOME/.openclaw/workspace/skills/clawexpert/scripts}"
python3 "$SCRIPT_DIR/analyze_gaps.py" \
  --kb "$KB" \
  --slug "{slug}" \
  --output "$KB/{slug}/research_gaps.json"
```

The output file contains:
- `breadth_tasks`: unchecked `Further Directions` from topic / node files, used to create **new subtopics**
- `depth_tasks`: targeted questions for existing nodes, used to deepen existing coverage

2. Read `research_gaps.json` and build a mixed deepen plan:
   - **Breadth track**: create new subtopics from `breadth_tasks`
   - **Depth track**: create one deep-dive investigation per selected node from `depth_tasks`
   - If a depth task clearly overlaps with a breadth task, keep only the depth task

3. Record the deepen session start:

```bash
python3 "$SCRIPT_DIR/update_superlearn_meta.py" \
  --kb "$KB" \
  --slug "{slug}" \
  --mode deepen \
  --phase start \
  --session-id "{session_id}" \
  --round 1 \
  --breadth-tasks {breadth_count} \
  --depth-tasks {depth_count}
```

4. Launch two agent pools in parallel:
   - **Breadth agents**: use the normal learning subagent workflow (same as Step 3 in Learner)
   - **Depth agents**: use the template in `references/deepdive-subagent-prompt.md`

Depth-agent rules:
- Each depth agent targets exactly one existing node
- It must read the current node first, then search only for evidence that answers the listed questions or verifies the listed claims
- It writes a supplement file to `{KB}/{slug}/superlearn/{session_id}/depth/{node-id}.md`
- It writes `done-depth-{node-id}.flag` via `write_flag.py --cleanup-progress`

5. Merge breadth and depth results separately:
   - **Breadth merge**:
     - New node seq starts from the highest existing seq + 1
     - New nodes are attached under the most relevant existing parent node
   - **Depth merge**:
     - Do not overwrite the original node
     - Append a new section at the end of the existing node:

```markdown
## Deepening Update ({YYYY-MM-DD})

### Questions Answered
- ...

### New Evidence
- ...

### Claim Verification
- ...

### Remaining Gaps
- [ ] ...
```

   - If a depth task discovers a genuinely separate reusable method/framework, it may create a new formal node in addition to the supplement

6. Update topic metadata and indexes:
   - Append a new learning record to `learning_sessions`
   - Record deepen session completion:

```bash
python3 "$SCRIPT_DIR/update_superlearn_meta.py" \
  --kb "$KB" \
  --slug "{slug}" \
  --mode deepen \
  --phase finish \
  --session-id "{session_id}" \
  --round 1 \
  --breadth-tasks {breadth_count} \
  --depth-tasks {depth_count} \
  --sources-added {sources_added} \
  --nodes-added {nodes_added} \
  --status complete
```

   - Update topic `meta.json`, `index.md`, category `_index.md`, and `_root_index.md`
   - Run `rebuild_index.py` and `validate_kb.py` before reporting success

7. Update the "Further Directions" in `index.md` and any touched nodes:
   - Check off completed items
   - Keep unresolved items unchecked
   - Add newly discovered open questions

8. **⚠️ Sync the category index (MANDATORY — do not skip)**:
   - Find the `{KB}/_index/` subdirectory for this topic's L1/L2 category
   - Append every new node to the Knowledge Nodes list in that `_index.md`
   - The category index node count must always match `index.md` exactly
   - Verify: `grep -c "node-" {KB}/_index/.../... ` equals `grep -c "node-" {KB}/{slug}/index.md`

### Multi-round Deep Research (superlearn)

When executing `/clawexpert superlearn <topic-or-slug>`:

1. Resolve the input against the knowledge base:

```bash
python3 "$SCRIPT_DIR/resolve_topic.py" --kb "$KB" --query "{topic-or-slug}"
```

- If `exists=true`: use the returned `best_match.slug` and start from deepen rounds
- If `exists=false`: treat the input as a brand new topic and enter **Phase 0: bootstrap learn**

2. Initialize minimum budget contract:
   - If user provided only `--rounds`: `MAX_ROUNDS={value}`, `MAX_HOURS=0`
   - If user provided only `--hours`: `MAX_ROUNDS=0`, `MAX_HOURS={value}`
   - If user provided both: `MAX_ROUNDS={rounds}`, `MAX_HOURS={hours}`
   - If user provided neither: `MAX_ROUNDS=2`, `MAX_HOURS=0`
   - `ROUND=1`
   - `START_TS=now`
   - `ELAPSED_HOURS=0`

3. **Phase 0: bootstrap learn (only when topic does not yet exist)**

- Run one initial `/clawexpert learn {topic}` using the same total budget
- If `MAX_HOURS>0`, the learn phase consumes from that shared budget
- After learn finishes:
  - recompute `ELAPSED_HOURS`
  - if `ELAPSED_HOURS >= MAX_HOURS` and time budget is active → stop with `stop_reason=bootstrap_budget_exhausted`
  - otherwise continue into deepen rounds using the newly created slug

4. At the start of every deepen round:
   - Run `analyze_gaps.py` and write `{KB}/{slug}/superlearn/round-{ROUND}/gaps.json`
   - Run `plan_superlearn.py` to evaluate whether the **minimum contract** has already been satisfied:

```bash
python3 "$SCRIPT_DIR/plan_superlearn.py" \
  --kb "$KB" \
  --slug "{slug}" \
  --gaps-file "$KB/{slug}/superlearn/round-{ROUND}/gaps.json" \
  --round "{ROUND}" \
  --max-rounds "{MAX_ROUNDS}" \
  --max-hours "{MAX_HOURS}" \
  --elapsed-hours "{ELAPSED_HOURS}"
```

5. If `should_continue=false`, stop immediately and report the stop reason.
   - `should_continue=false` means the requested minimum contract has already been satisfied at the current round boundary
   - It does **not** mean the agent is free to stop early based on subjective completeness

6. If `should_continue=true`, record round start:

```bash
python3 "$SCRIPT_DIR/update_superlearn_meta.py" \
  --kb "$KB" \
  --slug "{slug}" \
  --mode superlearn \
  --phase start \
  --session-id "{session_id}" \
  --round "{ROUND}" \
  --max-rounds "{MAX_ROUNDS}" \
  --max-hours "{MAX_HOURS}" \
  --breadth-tasks {breadth_count} \
  --depth-tasks {depth_count}
```

7. Execute one full deepen round using only the selected breadth/depth tasks from the plan.

8. After the round:
   - Merge
   - Rebuild indexes
   - Validate
   - Record round completion with `update_superlearn_meta.py --phase finish`
   - Re-run `analyze_gaps.py`
   - Re-run `plan_superlearn.py` for `ROUND+1`
   - Recompute `ELAPSED_HOURS` from `START_TS`

9. **Planner is the only stop authority**:
   - `--hours` and `--rounds` are **minimum requirements**, not soft caps and not upper bounds
   - Before the requested minimum is satisfied, stopping is prohibited
   - The main agent must NOT stop because it personally judges the remaining gaps to be "niche", "incremental", or "not worth it"
   - The main agent must NOT skip a round based on free-form reasoning
   - A round may stop only when `plan_superlearn.py` returns `should_continue=false`
   - The main agent must NOT replace `update_superlearn_meta.py` with ad-hoc inline Python to finalize the run
   - The final user-facing report must include the planner's `budget_mode` and `stop_reason`

10. Increase `ROUND += 1` and repeat until the planner returns `should_continue=false`.

### Node Confidence Rules

| source_count | confidence |
|-------------|------------|
| >= 3 high-quality sources | high |
| 1–2 sources | medium |
| 0 sources (inference only) | low |

### Conflict Handling

When different sources support opposing views on the same conclusion:

```markdown
## Key Conclusions
- {Conclusion A} ([source 1](../raw/web/xxx.md))
- ⚠️ **Disputed**: [source 2](../raw/web/yyy.md) reaches the opposite conclusion,
  arguing that {opposing view}
```

---

## V. Expert

### Proactive Mode Check (Required Before Every Answer)

⚠️ **Before answering any user question, always read the proactive mode from file** — do not rely on session memory or environment variables:

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
try:
    mode = json.load(open(state)).get('proactive_mode', 'off')
except Exception:
    mode = 'off'
print(mode)
"
```

Hold this value for the current answer's B1/B3 decisions. Valid values: **off / suggest / auto** — treat any other value as `off`.

### Trigger Conditions

When a user asks a question (not a slash command), use the self-check result from session start to decide:

**Conditions that trigger knowledge base retrieval** (any one is sufficient):
- The question's domain is clearly related to a known knowledge base topic name/slug
- The user explicitly asks "have you learned about XXX?" or "answer based on your knowledge base"
- The question involves specialized knowledge that may be covered in the knowledge base

### Knowledge Base Answer Flow (Three-Layer Progressive Retrieval)

**Layer 1: Read _root_index.md (required)**

```bash
cat "{KB}/_index/_root_index.md"
```

Browse the entire knowledge base category map, determine which L1/L2 category the question belongs to, and locate the relevant branch. If `_root_index.md` does not exist (v0.1.0 compatibility mode), scan slug directories under `{KB}/` and read the `topic` field of each `meta.json` to make the determination.

**Layer 2: Read category _index.md (required)**

```bash
cat "{KB}/_index/{l1-id}/{l2-label}/_index.md"
```

Retrieve the source list and key conclusion summaries for this category. Most questions can be answered with high quality at this layer without reading the original sources.

**Layer 2.5: Run query-routing candidate retrieval (required unless the match is already obvious)**

```bash
python3 "{SCRIPT_DIR}/resolve_query_nodes.py" --kb "{KB}" --query "{user question}"
```

Use the returned `top_topics` and `top_nodes` only as a **routing shortlist**:
- The script does **not** decide semantics for you
- The main agent must judge whether the query maps to:
  - an existing node
  - a broader topic branch
  - a narrower child of an existing node
  - or a genuinely new node/topic
- Prefer inspecting the top 1-3 candidates rather than requiring an exact wording match
- If multiple phrasings appear to describe the same concept, reuse the existing canonical node instead of creating a near-duplicate
- If the best candidate is only broadly related, route into that branch first and reason at the tree level before deciding whether a new node should exist

**⚠️ `ask_agent_to_create_or_expand` does NOT mean "skip KB retrieval"**. It means the routing script could not find a high-confidence single match. In this case you must still:
1. Read the index files of the top 1–3 `top_topics` returned, even if their scores are low
2. Perform cross-topic enrichment (see below) before answering

**Cross-topic enrichment (required when answering multi-dimensional questions)**

Token-based routing often misses semantically adjacent topics. After getting the routing shortlist, actively scan for additional topics that could contribute theory, data, or framing:

- Read `{KB}/_root_index.md` to see all topic names and their L1/L2 categories
- For any topic whose name or category overlaps with the question's domain — even loosely — read its `index.md`
- Specifically: if the question involves **investor behavior, psychology, or market anomalies**, always check whether a behavioral finance / 行为金融 topic exists and read its index
- If the question involves **Chinese markets or A股**, also check for empirical / 实证 research topics covering the same domain
- Compose the final answer by synthesizing across all relevant topics, not just the highest-scoring one

**Layer 3: Spawn QA subagent to read original sources (on demand)**

Triggered whenever the main agent judges that reading the original source would improve answer quality — not limited to numerical citations. Any time more depth, context, or fidelity to the source is needed, spawn a QA subagent.

⛔ **The main agent must NEVER read raw source files directly.** Reading `raw/web/*.md` or `raw/pdf/**` files is exclusively the QA subagent's job. If the main agent needs content from a source file, it must always go through the spawn → read tmp → delete tmp pipeline below. Direct `cat` or `read` calls on source files by the main agent are prohibited — they bypass the verbatim-extraction guarantee and produce unreliable citations.

```
sessions_spawn({
  task: "QA subagent prompt — fill in file_path and query from the template below",
  runtime: "subagent",
  mode: "run",
  label: "ce-qa-{timestamp}",
  sandbox: "inherit"
})
```

**QA subagent prompt template**:
```
You are a ClawExpert QA subagent. Your sole job is to read the specified source file
and extract relevant content as faithfully and completely as possible.

⛔ Strictly prohibited:
- Do not execute any git operations
- Do not output anything to the user — write to files only
- Do not read any files outside the scope specified by this task
- Do not paraphrase numbers, percentages, dates, proper nouns, or named conclusions — quote verbatim
- Do not synthesize across passages or draw new conclusions — extract only

Task:
- Source: {file_path}
- Query: {what the main agent needs to know — be specific about the topic or question}
- Write result to: {KB}/_qa_tmp/{timestamp}.md

**If {file_path} is a directory (large file sub-tree)**:
1. Read `{file_path}/_index.md` first to get the Part Index with 1-sentence summaries per part
2. Use the summaries to identify which parts are relevant to the query
3. Read only those relevant parts — do not read all parts
4. If the index summary is insufficient to determine relevance, start with part-001.md

Result file format (follow strictly):

---
query: {query}
source_file: {file_path}
completeness: full | partial | not_found
---

## Verbatim Excerpts

Extract ALL passages in the file that are relevant to the query. For each passage:

### Excerpt {n}
Location: {section title or paragraph description in the source}
> {exact verbatim quote — do not shorten, merge, or paraphrase}

(Repeat for every relevant passage found. More excerpts is better than fewer.)

## Extraction Summary

A faithful synthesis of the excerpts above (3–8 sentences).
- Must not introduce any fact, number, or claim not present in the verbatim excerpts above
- Must not omit significant findings from the excerpts
- Numbers and key terms must match the verbatim excerpts exactly
```

**Main agent reading rules** (apply every time a QA result is read):
- Treat "Verbatim Excerpts" as ground truth — cite directly from these, not from the summary
- Use "Extraction Summary" only as a navigation aid
- If `completeness: partial`, note the gap explicitly in your answer
- If `completeness: not_found`, do not fabricate — state that the source contains no relevant content
- After composing the answer, immediately delete the tmp file:

```bash
rm -f "{KB}/_qa_tmp/{timestamp}.md"
```

**If framework nodes exist**: Read the framework node and conduct structured analysis along its dimensions.

### Answer Format

```
{Main answer content}

---

**Citations**:
- [{node label}] → {source document title} ({source date})
- [{node label}] → {source document title}

**Knowledge Status**:
- Established: {aspects with sufficient evidence}
- To be deepened: {aspects with insufficient evidence or not yet covered}
- Disputed: {aspects with contradictory sources} (only shown when disputes exist)

> For more depth, run `/clawexpert learn --deepen {slug}`
```

### No Matching Knowledge Base

```
No knowledge base found for this question.
Consider running `/clawexpert learn {recommended topic name}` to build one systematically.

Here is a temporary answer based on live search:
{live search results}
```

### Framework Transfer

When facing a new analytical question, first check whether the knowledge base has a relevant framework node:

1. Read index.md and check whether any nodes have type=framework
2. If so, read that framework node
3. Conduct analysis following the framework's "Analysis Dimensions" and "Application Steps"
4. For each dimension, reference specific data and conclusions already in the knowledge base wherever possible
5. Clearly indicate which dimensions have sufficient backing and which require additional searching

This lets you not just "remember conclusions" but "learn analytical methods" — enabling you to handle new questions.

### Proactive Topic Tracking (B1)

After composing an answer, re-read the current mode directly from `clawexpert-state.json` (do not rely on session memory — the mode may have changed):

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
try:
    mode = json.load(open(state)).get('proactive_mode', 'off')
except Exception:
    mode = 'off'
print(mode)
"
```

If mode is `off` → skip entirely. Otherwise, check whether coverage was insufficient and record it:

**Coverage is insufficient when any of the following is true:**
1. No matching topic was found ("No Matching Knowledge Base" branch was taken)
2. A topic was found but all matched nodes have `confidence: low`
3. A topic was found but all matched nodes have `source_count` < 2

If coverage is insufficient, extract the topic from the user's question (use a 3–6 word descriptive label) and a one-sentence gap description, then update `{KB}/_proactive_queue.json`:

```bash
python3 -c "
import json, os, datetime

kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
path = kb + '/_proactive_queue.json'
today = datetime.date.today().isoformat()

topic = '{TOPIC}'           # replace: 3-6 word label from the question
gap   = '{GAP_DESCRIPTION}' # replace: one sentence describing what was missing

# Load or create queue
data = json.load(open(path)) if os.path.exists(path) else {'version': 1, 'queue': []}

q = data.get('queue', [])

# Find existing entry for this topic (case-insensitive match)
match = next((i for i, e in enumerate(q) if e['topic'].lower() == topic.lower()), None)

if match is not None:
    q[match]['session_count'] += 1
    q[match]['mentioned_at'] = today
    q[match]['gap_description'] = gap
else:
    q.append({'topic': topic, 'gap_description': gap, 'mentioned_at': today, 'session_count': 1, 'source': 'conversation'})

# Sort by session_count desc, then mentioned_at desc; keep top 20
q.sort(key=lambda e: (-e['session_count'], e['mentioned_at']), reverse=False)
data['queue'] = q[:20]
data['updated'] = datetime.datetime.utcnow().isoformat() + 'Z'
data.setdefault('version', 1)

json.dump(data, open(path, 'w'), indent=2)
print(f'Queue updated: {topic} (session_count={q[0][\"session_count\"] if q else 1})')
"
```

Do **not** inform the user about this queue update — it runs silently in the background.

### ⚠️ Proactive Queue Display (B3) — MANDATORY

⚠️ **This step is not optional.** Immediately after B1 (whether or not a gap was written), you MUST run the queue check and output the result. Your answer is incomplete until B3 executes. Do not stop after composing your answer text — continue directly to this step.

```bash
python3 -c "
import json, os
state = os.path.expanduser('~/.openclaw/workspace/clawexpert-state.json')
try:
    mode = json.load(open(state)).get('proactive_mode', 'off')
except Exception:
    mode = 'off'
if mode == 'off':
    print('off')
    exit()
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
path = kb + '/_proactive_queue.json'
if not os.path.exists(path):
    print('empty')
else:
    q = json.load(open(path)).get('queue', [])
    q_sorted = sorted(q, key=lambda e: (-e['session_count'], e.get('mentioned_at', '')))
    for e in q_sorted[:3]:
        print(f\"{e['topic']}|{e['gap_description']}|{e['session_count']}\")
"
```

If output is `off` or `empty` → skip silently. Otherwise append to the answer:

- **suggest** mode:
  ```
  ---
  📚 Learning suggestions based on recent gaps:
  1. {topic} — {gap_description} (mentioned {session_count}×)
  2. ...
  Run /clawexpert learn <topic> to build knowledge, or /clawexpert proactive skip to dismiss.
  ```
- **auto** mode → show the top entry and ask the user when to learn:
  ```
  ---
  📚 Auto-learning ready:
  1. {topic} — {gap_description} (mentioned {session_count}×)

  When would you like to learn this? Reply:
  - **now** — start immediately
  - **later** — remind me next session
  - **skip** — dismiss this topic
  ```
  Then wait for the user's reply:
  - `now` → execute `/clawexpert learn {topic}`
  - `later` → keep the entry in the queue, do nothing this session
  - `skip` → remove only this entry from the queue (do not clear the whole queue)

---

### ⚠️ End-of-Answer Checklist (Required When Mode ≠ off)

After composing and outputting your answer text, you MUST complete ALL of the following before considering the answer done:

1. **B1** — Run topic tracking: if coverage was insufficient, write the gap to the queue (silent, no user output)
2. **B3** — Run queue display: if the queue is non-empty, append the suggestion block to your answer

Do not stop after the answer text. Do not wait for the user to prompt you. These steps are mandatory.

### Radar Scan (`/clawexpert radar`)

Triggered by the user running `/clawexpert radar`, or via Cron. Scans all L1 categories for recent major events and adds candidates to the proactive queue.

#### Step 1: Read L1 categories

```bash
python3 -c "
import json, os
kb = os.environ.get('CLAWEXPERT_KNOWLEDGE_DIR', os.path.expanduser('~/.openclaw/workspace/knowledge'))
cats = json.load(open(kb + '/_categories.json')).get('categories', [])
for c in cats:
    print(c['id'], c['label'])
"
```

#### Step 2: Search each category

For each L1 category, first output: `🔍 Scanning: {label}...`

Then run 1–2 searches using the workspace's configured search path. If the built-in `web_search` tool is unavailable or disabled, immediately switch to the workspace fallback search skill. If no fallback is configured, open Google directly in the browser:
```
https://www.google.com/search?q={encoded_query}
```

Queries to run per category:
- `"{label}" major developments last 7 days`
- `"{label}" latest breakthroughs OR announcements 2026`

Vary language based on the category label (e.g., Chinese-label categories → also search in Chinese).

⚠️ **Do NOT stop between categories. Immediately proceed to the next category after each search.**

#### Step 3: Evaluate events

For each result, assess:
1. **Impact**: affects a large population, major institution, or significant market
2. **Persistence**: likely to remain relevant for weeks, not just 24 hours
3. **KB relevance**: relates to an existing topic in the knowledge base, or fills a clear gap

Discard: minor product updates, routine statistical releases, clickbait headlines.

#### Step 4: Write candidates to queue

For each event that passes evaluation, add an entry to `{KB}/_proactive_queue.json` using the same update logic as B1, with `source: "radar"`:

```python
{
  "topic": "{3-6 word event label}",
  "gap_description": "{one sentence: what happened and why it matters}",
  "mentioned_at": "{today}",
  "session_count": 1,
  "source": "radar"
}
```

If proactive mode is `off`, skip writing to the queue (the scan still runs if the user explicitly calls `/clawexpert radar`, but candidates are not saved).

#### Step 5: Output summary

```
🔭 Radar scan complete
   Categories scanned: {N}
   Events added to queue: {M}

{If M > 0:}
Top candidates:
  1. {topic} — {gap_description}
  2. ...

Run /clawexpert proactive suggest to review, or /clawexpert learn <topic> to start learning.

{If M == 0:}
No significant new events found across monitored categories.
```

---

## VI. Edge Cases

| Scenario | Handling |
|----------|----------|
| Subagent timeout | Mark subtopic as timeout, merge completed portions, explain in report |
| No search results for a subtopic | Write status:"no_results" in flag, main agent explains in report |
| Knowledge base directory missing | Auto-create with `mkdir -p` |
| Slug already exists (complete) | Ask user whether to deepen or re-learn |
| Concurrent learning of the same topic | Reject when status="learning", prompt user to wait |
| meta.json corrupted/missing | Scan nodes/ and raw/ to reconstruct basic information |
| forget operation | Must wait for explicit user confirmation before executing rm -rf |

---

## VII. Scheduled Learning (Cron, optional)

Users can add the following to openclaw.json:

```json
{
  "cron": {
    "clawexpert-nightly": {
      "cron": "0 2 * * *",
      "message": "/clawexpert learn --auto",
      "target": "main"
    }
  }
}
```

`--auto` mode: Scans all topics and automatically runs deepen on any with status="partial" or unchecked items in the "Further Directions" list. Exits silently if nothing to do.

To also run the radar scan on a weekly schedule, add a second Cron entry:

```json
{
  "cron": {
    "clawexpert-nightly": {
      "cron": "0 2 * * *",
      "message": "/clawexpert learn --auto",
      "target": "main"
    },
    "clawexpert-radar": {
      "cron": "0 7 * * 1",
      "message": "/clawexpert radar",
      "target": "main"
    }
  }
}
```

`clawexpert-radar` runs every Monday at 07:00, scanning all L1 categories for the past week's major events and writing candidates to the proactive queue. Requires proactive mode (`clawexpert-state.json → proactive_mode`) to be `suggest` or `auto` for candidates to be saved.
