---
name: ai-capsule
description: Ranks your daily AI news feed by personal relevance — scores every article and surfaces the most useful ones first. To fetch X/Twitter posts, the daily run reads your local Chrome x.com cookies (via browser-cookie3, in-memory only) and calls the twitter-cli subprocess; it may auto-detect a local proxy on 127.0.0.1 to reach x.com, and writes reports/history/dedup state to your local data_dir. Sources include HuggingFace Papers, OpenAI, Anthropic, DeepMind, Simon Willison, GitHub Trending, HN, Reddit, and more, plus X/Twitter accounts.
version: 1.0.5
license: MIT
emoji: "📰"
homepage: https://github.com/WebPudge/ai-capsule
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - bash
---

# AI Capsule — Personal AI News Value Evaluator

Scores and ranks your daily AI news feed based on what you actually care about. Tell it your role and familiar areas — it scores every article against your profile and ranks them so the most relevant ones appear first. Nothing is filtered out: every article makes it into the digest, just in the right order. Sources include HuggingFace Papers, OpenAI, Anthropic, DeepMind, Simon Willison, GitHub Trending, HN, Reddit, and more (17 total), plus X/Twitter accounts.

**Trigger words:** run the full digest by saying `daily`, `daily mode`, `每日模式`, `每日摘要`, or `日报`. To avoid firing during ordinary conversation, the bare word `daily` only triggers as a short command — the message must start with a trigger word and contain little else (≤ ~6 words / ≤ 5 tokens after the trigger). `daily` appearing mid-sentence (e.g. "I read the daily news", "今天的 daily report 还没看") does NOT trigger the digest. When ambiguous, ask the user to confirm before fetching.

**First time:** run `bash $SKILL_DIR/scripts/setup-env.sh` once, then say `daily` — Claude will walk you through a short setup (role, familiar areas, output language).

## Initialization

> **First time only:** run `bash $SKILL_DIR/scripts/setup-env.sh` to set up the Python venv. Config is created on first run via guided setup.

On every run, resolve the skill directory, Python interpreter, and config path:

```bash
SKILL_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]:-$0}" 2>/dev/null || echo "$0")")" && pwd)
CONFIG_FILE="${AI_CAPSULE_CONFIG:-$HOME/.ai-capsule/config.yaml}"

# Prefer venv; fall back to system python3 for spawned/headless agents (OpenClaw, CI)
if [ -x "$SKILL_DIR/.venv/bin/python" ]; then
  PYTHON="$SKILL_DIR/.venv/bin/python"
else
  PYTHON="$(command -v python3 || command -v python)"
  echo "WARN: venv not found, using system Python ($PYTHON). Run: bash $SKILL_DIR/scripts/setup-env.sh"
fi

echo "SKILL_DIR: $SKILL_DIR"
echo "PYTHON: $PYTHON"
echo "CONFIG_FILE: $CONFIG_FILE"
cat "$CONFIG_FILE" 2>/dev/null || echo "initialized: false"
```

**If `initialized: false`** (or config file missing) → enter the guided setup flow (Step -1), otherwise jump to Step 0.

---

## User Configuration

**Config file:** `~/.ai-capsule/config.yaml` — lives outside the skill directory, survives updates.

**Override:** set env var `AI_CAPSULE_CONFIG=/path/to/config.yaml` to use a different file.

**Built-in identity profiles:**
- `engineer`: Is it actionable in a real engineering context?
- `pm`: Does it affect product direction, UX, or business decisions?
- `researcher`: Does it advance understanding of a technical principle?
- `learner`: Is this direction worth investing time to learn systematically?
- `founder`: Does it affect tech stack choices, product direction, or competitive positioning?

**Built-in purpose profiles (control scoring weights):**
- `learn`: D×0.35, N×0.25, R×0.2, U×0.1, WPS×0.1
- `solve`: U×0.45, R×0.3, D×0.1, N×0.1, WPS×0.05
- `scout`: W×0.25, P×0.2, N×0.2, S×0.15, R×0.15, U×0.05

---

## Usage

- **Single article**: paste title + body directly
- **Batch**: paste a JSON array `[{"id":"1","title":"...","content":"..."},...]`
- **URL**: paste a link starting with `http` or `https`
- **Daily**: say "daily" or "daily mode"
- **Reconfigure**: say "reconfigure" → Claude resets `initialized: false` and walks through setup again

---

## Execution Steps

### Step -1: Guided Setup (first run only)

Runs when `initialized: false` or config file is missing.

**Question 1 — Your role**
> What role do you primarily take when consuming AI news?
- A) Application engineer / full-stack engineer → engineer
- B) AI researcher / ML engineer → researcher
- C) Product manager / founder → pm or founder
- D) Student / self-learner → learner
- E) Other (describe freely)

**Question 2 — Your familiar areas**
> e.g. LLM application development, RAG, Agent frameworks, model fine-tuning…

**Question 3 — Your primary purpose**
- A) Follow the technical frontier (learn)
- B) Solve concrete problems at work (solve)
- C) Scan market trends (scout)
- D) Context-dependent (default: learn)

**Question 4 — What you don't want to see**
> e.g. pure marketing fluff, trend analysis with no code…

**Question 5 — Output language**
> What language should card text, value analysis, and scoring reasons be written in?
- A) Chinese / 中文 (default)
- B) English
- C) Other (describe freely, e.g. "日本語")

> Proper nouns (model names, framework names, GitHub repo names) always stay in their original form.

**Question 6 — Data directory**
> Where should daily reports, history, and dedup files be stored?
- A) ~/.ai-capsule/data (default — survives skill updates)
- B) Custom path (describe freely)

After collecting answers, write the config:
```bash
mkdir -p ~/.ai-capsule
cat > "${AI_CAPSULE_CONFIG:-$HOME/.ai-capsule/config.yaml}" << 'EOF'
initialized: true
identity: [user description]
role_desc: [user description]
familiar_areas:
  - [area 1]
default_identity: [engineer/pm/researcher/learner/founder]
default_purpose: [learn/solve/scout]
output_language: zh  # zh = Chinese / en = English / other language name
data_dir: ~/.ai-capsule/data
EOF
```

---

### Step 0: Mode Detection

- Input starts with `http(s)://` → **URL mode**
- Input starts with `[` and looks like a JSON array → **Batch mode**
- Input contains an explicit multi-word trigger — `daily mode`, `每日模式`, `每日摘要`, or `日报` — → **Daily mode** (matches anywhere in the message)
- Bare `daily` → **Daily mode** only if it is a short command: the message **starts with** `daily` and has ≤ 5 tokens after it (roughly ≤ 6 words total). `daily` mid-sentence (e.g. "I read the daily news", "今天的 daily report 还没看") does NOT trigger.
- Ambiguous → ask the user to confirm before fetching

### Step 1: Content Retrieval

**Fetch tool mapping** — use whichever tool your agent runtime provides:

| Runtime | Tool |
|---------|------|
| Claude Code | `WebFetch` |
| Codex / shell agents | `Bash: curl <url>` + python parse |
| Tavily agents | `tavily_extract` |
| Fallback | Ask user to paste content |

**URL mode:** Fetch and extract main text. For WeChat links, ask user to paste manually.

**Batch mode:** Parse JSON, extract `title` and `content`/`text` fields, score each article.

**Daily mode:** Read and execute `$SKILL_DIR/sections/daily-mode.md`.

**Single article mode:** Go directly to Step 2.

### Step 2: Dedup Check

Dedup file: `{data_dir}/dedup-titles.txt` (one title per line).

**Daily mode**: handled centrally in `sections/daily-mode.md` Step 3 — never judge manually.

**Single / URL / Batch mode**:

```bash
grep -Fx "article title" "$(
  "$PYTHON" -c "
import os, pathlib, yaml
cfg = yaml.safe_load(open(os.environ.get('AI_CAPSULE_CONFIG', str(pathlib.Path.home()/'.ai-capsule/config.yaml'))))
print(cfg.get('data_dir','~/.ai-capsule/data').replace('~', str(pathlib.Path.home())))
")/dedup-titles.txt"
```

If output is non-empty, skip and say: `"This article has already been scored (title: XXX)."`

### Step 3: Scoring

Read `default_identity`, `default_purpose`, and `output_language` (default: `zh`) from `$CONFIG_FILE`.

Scoring framework: see `$SKILL_DIR/sections/scoring.md` (Read the file before every run).

Runtime mode switches:
- "learn" / "学习" → PURPOSE = learn
- "solve" / "解决问题" → PURPOSE = solve
- "scout" / "找灵感" → PURPOSE = scout
- "pm perspective" / "engineer perspective" / etc. → switch IDENTITY

**Always output the score_json block first:**

```
<score_json>
{
  "title": "article title",
  "source": "hf | openai | anthropic | hn | reddit | github | producthunt | blog | unknown",
  "url": "taken directly from pending.json or fetch result — never construct from title",
  "identity": "engineer",
  "purpose": "learn",
  "R": 8, "U": 7, "N": 6, "D": 8,
  "W": 5, "P": 6, "S": 4,
  "total": 7.2,
  "F": 9,
  "final_score": 7.2,
  "action": "READ",
  "summary": "article entity + core value",
  "reasons": {
    "R": "specific relevance reason",
    "U": "specific utility reason",
    "N": "specific novelty reason",
    "D": "specific depth reason",
    "W": "specific wow reason",
    "P": "specific perspective reason",
    "S": "specific cross-domain reason"
  }
}
</score_json>
```

`F`: Personal Fit (0–10), assessed against `familiar_areas` and `dislikes` in config.
`final_score = total × (0.7 + 0.3 × F/10)` — sorting only, never displayed.
`action`: `TRY` (runnable code/tool) / `READ` (deep content) / `SCAN` (brief/low score).

### Step 4: Display Output

Output format: see `$SKILL_DIR/sections/output-format.md` (Read the file before every run).

**Language rule**: all card text follows `output_language`. Always keep in original form: article titles, technical terms, model/framework names, GitHub repo names, URLs, Action tags (TRY/READ/SCAN).

**Batch / Daily mode**: output detailed cards only, sorted high-to-low by score — no summary table.

### Step 5: Append Records

Append to `{data_dir}/history.jsonl` (with timestamp) and `{data_dir}/dedup-titles.txt`.

---

## Data Source Management

Source configs: `$SKILL_DIR/sources/{industry}.yaml`

**View sources:**
```bash
"$PYTHON" "$SKILL_DIR/sources_extract.py" --markdown --industry ai
```

**Add a source:**
```bash
bash $SKILL_DIR/scripts/add-source.sh --industry ai --type rss     --name "Name" --url https://example.com/feed
bash $SKILL_DIR/scripts/add-source.sh --industry ai --type webfetch --name "Name" --url https://example.com --note "hint"
bash $SKILL_DIR/scripts/add-source.sh --industry ai --type tavily  --name "Name" --query "search terms" --domains "reddit.com"
bash $SKILL_DIR/scripts/add-source.sh --industry ai --type twitter --name "Name" --accounts "handle1,handle2"
```

**Source schema:**
```yaml
# RSS — fetched automatically by fetch.py
- name: Source Name
  type: rss
  url: https://...
  limit: 5
  handler: huggingface    # optional: huggingface | hacker_news

# URL fetch — agent fetches in daily Step 2
- name: Source Name
  type: webfetch
  url: https://...        # use YYYY/M/D placeholder for date-based URLs
  limit: 5
  note: "hint for the agent"

# Tavily search — agent searches in daily Step 2
- name: Source Name
  type: tavily
  query: "search terms"
  include_domains:
    - reddit.com
  time_range: day         # day | week | month
  limit: 5

# X/Twitter — fetched automatically by fetch.py (requires Chrome login)
- name: X/Twitter
  type: twitter
  accounts:
    - handle1
    - handle2
  limit: 5
```

**New industry:** create `$SKILL_DIR/sources/{industry}.yaml` using `ai.yaml` as template.

---

Source: [github.com/WebPudge/ai-capsule](https://github.com/WebPudge/ai-capsule) · [Feedback / Bug report → Issues](https://github.com/WebPudge/ai-capsule/issues/new)
