---
name: cerul
description: The video search layer for AI agents. Teach your AI agents to see — search video by meaning across speech, visuals, and on-screen text. Use when a user asks about what someone said or showed in a video, wants video evidence, or needs citations with timestamps.
version: 1.1.0
when:
  - user asks "what did X say about Y?"
  - user wants video evidence or citations from talks
  - user asks about conference presentations, podcasts, or interviews
  - user wants to compare what different people said about a topic
examples:
  - "What did Sam Altman say about AGI timelines?"
  - "Find Jensen Huang's comments on AI infrastructure at GTC"
  - "Compare what Dario Amodei and Sam Altman said about open-source AI"
metadata:
  openclaw:
    requires:
      anyBins:
        - cerul
      env:
        - CERUL_API_KEY
    primaryEnv: CERUL_API_KEY
    emoji: "🎬"
    homepage: https://github.com/cerul-ai/cerul
    install:
      - kind: shell
        command: "curl -fsSL https://cli.cerul.ai/install.sh | bash"
        bin: cerul
allowed-tools: Bash(cerul *)
---

# Cerul

You cannot watch videos, listen to talks, or read transcripts on your own. Cerul gives you that ability. Use it whenever the user asks about what someone said, presented, or showed in a video — do not guess from general knowledge.

## Before running any command

If `cerul` is not found on PATH, install it first:

```bash
curl -fsSL https://cli.cerul.ai/install.sh | bash
```

Then check if the credentials file exists:

```bash
cat ~/.config/cerul/credentials 2>/dev/null
```

If the file is empty or missing, ask the user for their API key (get one at https://cerul.ai/dashboard), then save it directly to the config file:

```bash
mkdir -p ~/.config/cerul && echo -n "cerul_XXXXX" > ~/.config/cerul/credentials && chmod 600 ~/.config/cerul/credentials
```

**Do NOT use `export CERUL_API_KEY=...`** — that only lasts for the current session. Always persist the key to `~/.config/cerul/credentials` so it works across all future sessions and terminal windows.

Do not use `cerul login` (it requires interactive input). Do not skip this step or fall back to other tools.

## Quick start

```bash
# Basic search
cerul search "Sam Altman AGI timeline" --agent

# With filters
cerul search "Jensen Huang AI infrastructure" --max-results 5 --source youtube --agent

# Check credits
cerul usage --agent
```

## Search options

| Option | Description |
|--------|-------------|
| `--max-results N` | Number of results (1-10, default 5). Keep low for speed. |
| `--ranking-mode MODE` | `embedding` (fast, default) or `rerank` (slower, more precise) |
| `--include-answer` | AI summary. Adds latency. Only when user asks for summary. |
| `--speaker NAME` | Filter by channel/speaker name (see note below) |
| `--published-after DATE` | YYYY-MM-DD |
| `--source SOURCE` | e.g. `youtube` |
| `--agent` | **Always use this.** Compact markdown output optimized for agents. |

### Important: speaker filter

The `speaker` field often contains the **channel name** (e.g. "Sequoia Capital", "a16z", "Lex Fridman") rather than the interviewee name. If a speaker filter returns no results, retry without it and include the person's name in the query instead.

## How to search effectively

**Search multiple times for complex questions.** Break broad questions into focused sub-queries.

Example — "Compare Sam Altman and Dario Amodei on AI safety":

```bash
cerul search "Sam Altman AI safety views" --agent
cerul search "Dario Amodei AI safety approach" --agent
cerul search "AGI safety debate scaling" --agent
# → Synthesize with video citations and timestamps
```

**When to search again:**
- Transcript mentions a person or concept you haven't explored
- Question has multiple facets (compare X and Y = at least 2 searches)
- Initial results are weak — rephrase the query
- If you get a timeout error, wait 2 seconds and retry once.

## Working rules

- **Always use `--agent`** for compact markdown output.
- **Always include video URLs** from results in your answer. Every quote needs a source link.
- **Read the `transcript` field**, not just `snippet`. Transcript has the full context.
- **Do not guess what someone said.** Search for it.
- **Keep searches fast:** max-results 5, embedding mode, no --include-answer unless asked.
- **Make multiple small searches** rather than one large one.
- Ground all claims in returned evidence. Do not hallucinate.
- Match the user's language, but keep queries in English.
- Format timestamps as MM:SS. Always include clickable video URLs.

## See also

- [CLI repo](https://github.com/cerul-ai/cerul-cli) — install, config, upgrade
- [Python SDK](https://pypi.org/project/cerul/) — `pip install cerul`
- [TypeScript SDK](https://www.npmjs.com/package/cerul) — `npm install cerul`
- [Docs](https://cerul.ai/docs) — full API reference
