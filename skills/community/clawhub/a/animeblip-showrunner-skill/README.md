# Animeblip Showrunner — AI video creation skill

Turn a one-line idea into a complete **multi-scene story video** — screenplay → consistent
characters → consistent elements (locations/props) → scene images → scene videos → final
cut — in 900+ art styles, as **short videos, films, or episodic series**. This skill lets
**any AI agent** (Claude Code, Cursor, Gemini CLI, Codex, OpenClaw, …) drive
[Animeblip](https://animeblip.com)'s production pipeline end-to-end, so it can create
**high-quality video content at scale** — autonomously, episode after episode.

> Keywords: AI video generation · text-to-video · image-to-video · anime · vertical
> micro-drama · storyboard · multi-scene story video · consistent characters · episodic
> series · faceless video automation · AI showrunner.

**How it works:** Animeblip's backend agent owns the full creative pipeline but has **no
built-in reviewer**. This skill is that reviewer/producer: you send the brief, **poll**
`query_session` on a cadence, critique the screenplay, and fix failures with **targeted
single-scene** edits (never full regen), keeping spend bounded.

> You manage and review by polling and sending messages — there is no managed loop, YOU
> (the agent) drive. The Animeblip agent does the creative generation.

## Install

```bash
npx skills add animeblip-ai/animeblip-showrunner-skill
```

[`skills`](https://github.com/vercel-labs/skills) is Vercel Labs' cross-platform skill
installer — it works with Claude Code, Gemini CLI, Codex, Cursor and 40+ other agents.
Install into a specific agent with `-a`:

```bash
npx skills add animeblip-ai/animeblip-showrunner-skill -a claude-code
```

This drops the skill into `~/.claude/skills/animeblip-showrunner-skill/` (pulled from the public
GitHub repo). Or install from a local checkout:

```bash
git clone https://github.com/animeblip-ai/animeblip-showrunner-skill.git \
  ~/.claude/skills/animeblip-showrunner-skill
```

## Setup

```bash
export ANIMEBLIP_API_KEY="ab_…"                            # your Animeblip API key — create one at studio.animeblip.com → API Keys
export ANIMEBLIP_BASE_URL="https://studio.animeblip.com"   # optional — defaults to prod
```

`ANIMEBLIP_BASE_URL` defaults to `https://studio.animeblip.com` and rarely needs changing.
Python 3 stdlib only — no dependencies to install.

## Usage

Once installed, just describe what you want in your agent — it triggers the skill and
drives Animeblip for you:

```
Make a vertical anime micro-drama: a wronged heiress returns with the power to expose
liars — produce the complete final video.
```

The agent then: `create_project.py` → `send_message.py` (your brief) → poll
`query_session.py` → triage any failures / answer any questions → deliver the final video
link. To produce a whole series, it loops `create_episode.py` per episode. See
[SKILL.md](./SKILL.md) for the full flow.

The skill uses **one fixed art style** (the Anime6 preset) for every story — the agent does
not pick styles. To use a different art style, change it on the website (the storyboard
editor); there's no `--style` to set here.

## Layout

```
animeblip-showrunner-skill/
├── SKILL.md                  # canonical entry (commands, flow, triage, rules)
├── CLAUDE.md                 # maintainer guidance (conventions for editing this skill)
├── README.md                 # this file
├── LICENSE                   # MIT
├── skill-card.md             # one-screen command quick-reference
├── scripts/
│   ├── _common.py            # shared REST client + auth
│   ├── create_project.py       # new story (ep1 of a new series)
│   ├── send_message.py       # send a message verbatim (full brief or one scoped step)
│   ├── query_session.py      # one status snapshot (the poll channel)
│   ├── get_project_state.py  # scenes + characters[]/elements[] read (the review channel)
│   ├── create_episode.py     # next episode in the same series
│   └── list_projects.py      # list projects (series) + their episodes — find one to resume
└── docs/
    ├── triage-rules.md       # failure classification + Chinese-prompt mitigation
    └── cost-model-and-caps.md# what costs money + how to keep spend bounded
```

Call the per-op script directly, e.g. `python3 scripts/create_project.py …`. `--dry-run`
works on every command, in any position.

## Flow (instruction-driven — no mode flag)

End-to-end vs step-by-step is decided by **what message you send**, driven by the user's
request — not a flag. See [SKILL.md](./SKILL.md) for the full flow.

- **Default — end-to-end (one shot):** `create_project.py` → `send_message.py` with the full
  brief *plus* an end-to-end line → poll `query_session.py` → deliver. While polling: triage
  any `failures[]` (one targeted fix), answer any new `messages[]` the agent left, else keep
  polling.
- **Per-step (review between steps):** `send_message.py "Write the screenplay only, then stop."`
  → poll `query_session.py` → read `get_project_state.py` (the review channel — scenes +
  characters[]/elements[]) → critique → send the next scoped step → repeat through characters →
  images → videos → final cut.
- **Manual review:** same per-step cycle, but surface the `get_project_state.py` snapshot to a
  human and stop until they say continue.

Chain episodes with `create_episode.py --from S`.

## Rules

- The Animeblip agent has **no web search** — research facts yourself before the brief.
- **One run per story at a time** (`409` = busy → wait, retry).
- Keep spend bounded — stop after ~2 retries per shot / ~6 fix-sends per episode and surface
  to the human rather than burning credits; if the user asked for a sign-off, don't skip it.
- Do not full-regen to fix one shot — name the scene.

See **SKILL.md** for the canonical command reference and **docs/** for one page per
concept.

## Links

- Animeblip — https://animeblip.com
- Create your API key — https://studio.animeblip.com (→ API Keys)

## License

[MIT](LICENSE)
