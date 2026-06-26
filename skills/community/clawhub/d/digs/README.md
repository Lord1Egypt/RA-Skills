# Digs 🔭

> *The questions you're pursuing are part of how you think. Your agent should track them too.*

**Digs** is an open-source agent skill that turns your active research threads into a private, compounding intelligence layer — kept on your machine, owned by you.

## Philosophy

A dig is a question you're pursuing. Not knowledge you have — something you're figuring out. The difference matters: Digs is anchored by uncertainty, not facts. Each thread stays alive until it's resolved or abandoned, and the agent helps it compound over time.

Inspired by Andrej Karpathy's LLM-wiki pattern: the file isn't a dump of links. It's a persistent, maintained artifact — findings synthesised, contradictions flagged, open questions tracked. The agent is an active participant in the research, not just a retrieval layer.

No Notion. No bookmarks folder. Just files and your AI agent.

---

## What it does

- **Tracks research threads** — one markdown file per question you're figuring out
- **Logs findings** — synthesised insights, not link dumps, with contradictions flagged
- **Keeps open questions** — first-class objects that evolve as you learn
- **Surfaces connections** — links to your people, your books, and other threads
- **Compounds over time** — the agent maintains cross-references and nudges stale threads

```
digs/
  city-walkability.md
  attention-mechanisms.md
  remote-work-productivity.md
  closed/
    why-sourdough-rises.md
```

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/digs
curl -o ~/.claude/skills/digs/SKILL.md https://raw.githubusercontent.com/haah-ing/digs-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add haah-ing/digs-skill
```

Works with OpenClaw, Cursor, and any agent that supports the skills ecosystem.

### Hermes

```bash
hermes skills install digs
```

---

## Then just talk

```
"I keep wondering what actually makes a city walkable."
"I found this — Jan Gehl says pedestrian activity triples when setbacks reduce below 2m."
"What am I figuring out about urbanism right now?"
"That contradicts what I found last week about Walk Score."
"I think I figured it out — it's geometry, not destination density."
```

Each dig file looks like this:

```markdown
# What makes a city actually walkable?

- **Status:** active
- **Opened:** 12 Mar 2026
- **Tags:** #cities #urbanism #design

## Open questions

- What metrics actually correlate with walkability scores?
- ~~Is Walk Score a reliable proxy?~~ — no, it measures transit access
- Does walkability cause higher rents, or just correlate?

## Findings

12 Mar 2026: Gehl's research shows pedestrian activity increases 3× when building setbacks reduce below 2m. Geometry matters more than destination mix.

22 Mar 2026: Walk Score correlates with transit access, not human-scale design — these are separable.

## Sources

- [Cities for People — Jan Gehl](https://islandpress.org/books/cities-people)
- https://www.walkscore.com/methodology.shtml
```

---

## Works best with

Digs is part of a suite of personal intelligence skills:

- [**Peeps** 👥](https://github.com/haah-ing/peeps-skill) — your personal network. When someone has expertise matching an open dig, your agent surfaces them as a source.
- [**Pages** 📖](https://github.com/haah-ing/pages-skill) — your reading life. Books relevant to active digs get connected automatically.
- [**Haah** 🪩](https://github.com/haah-ing/haah-skill) — dispatch to your trusted circles. When you need external signal on a research question, Haah can ask your network.
- [**Nooks** 📍](https://github.com/haah-ing/nooks-skill) — your saved places. A coffee meeting at a nook can turn into a finding.
- [**Vibes** 🎧](https://github.com/haah-ing/vibes-skill) — albums, shows, podcasts, films, YouTube channels. Documentaries and podcasts can feed findings into your digs.

Install all six and your agent knows your people, your places, your reads, your culture, and your open questions.

---

## Contributing

The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Haah Inc*
