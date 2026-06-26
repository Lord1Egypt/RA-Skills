---

name: digs
description: Active research intelligence — track questions you're pursuing, log findings as they arrive, and close the loop when you figure it out. One markdown file per research thread in digs/. Use when opening a new inquiry, logging a finding, or asking "what am I figuring out about X?"
metadata:
  openclaw:
    emoji: "🔭"
    os: ["linux", "darwin", "win32"]
  hermes:
tags: ["research", "questions", "thinking"]

---

# 🔭 Digs — active research intelligence

**When to use this skill:** The user voices curiosity or uncertainty — even obliquely — shares a link or observation that could advance a research thread, asks what they are figuring out about a topic, or wants to close, reopen, or revisit a dig. You don't need the user to say "open a dig." If they're wondering about something, that's the signal. Act on it.

**You must:**

- Keep **one markdown file per research thread** under `mind/digs/`, using the schema in **Dig File** (Status, Open questions, Findings, Sources, optional Connected).
- **Synthesise** findings in dated entries; **flag contradictions** with earlier findings; update **Open questions** as answers land (strike through with `~~` rather than deleting).
- **Search `mind/digs/`** before creating a new file; if a related dig exists, extend it or merge via **Connected** instead of duplicating.
Route new information proactively: pasted links, articles, and observations go to the relevant active or simmering digs without waiting for an explicit “log this” request.
Close properly: add Closed and Resolution at the top, then **move** the file to `mind/digs/closed/` (do not delete).

**Do not:** See **What NOT to Suggest** — e.g. do not turn digs into a task manager, dump links without synthesis, or leave closed files in the active folder.

---

## Data

**Base path** is workspace root or document root folder. On first use, create it: `mkdir -p mind/digs/`. Digs uses a `mind/digs/` folder in your workspace.

Files live in `mind/digs/`. One file per research thread.

```
mind/
└── digs/
    ├── digsconfig.yml
    ├── city-walkability.md
    ├── attention-mechanisms.md
    └── remote-work-productivity.md
```

**Filenames:** short kebab-case slug of what you're figuring out — `city-walkability.md`, not `research-on-city-walkability-question.md`. If the question is sharp the slug writes itself.

### Dataset Config

`digsconfig.yml` lives inside the `mind/digs/` directory. Read it at the start of any session involving this skill.

```yaml
images: no (by default no, ask if you human want to feach images for concepts, warn that it is token expensive)
```

---

## Dig File

```markdown
# What makes a city actually walkable?

Status: active
Opened: 12 Mar 2026
Tags: #cities #urbanism #design #housing
Inmage: optional image illustrating the concept, sotred in `../assets/good-long-slug`
Connected: [[why-singapore-feels-different]], [[remote-work-and-density]]

## Open questions

- What metrics actually correlate with walkability scores?
- Is Walk Score a reliable proxy or marketing?
- Does walkability cause higher rents, or just correlate?

## Findings

12 Mar 2026: Jan Gehl's research shows pedestrian activity increases 3× when building setbacks reduce below 2m. Suggests physical geometry matters more than destination mix. Source: [Cities for People](https://islandpress.org/books/cities-people)

15 Mar 2026: Singapore HDB estates score high on Walk Score but feel sterile — the metric misses thermal comfort and shade. The algorithm optimises for distance, not experience. Personal observation.

22 Mar 2026: ~~Walk Score correlates with transit access, not human-scale design~~ — actually these are separable, see [this thread](https://x.com/...). Still unclear.

## Sources

- [Cities for People — Jan Gehl](https://islandpress.org/books/cities-people)
- https://www.walkscore.com/methodology.shtml
- [[marco-tabini]] — works in urban planning (link only if Peeps is installed)
```

**Field guidance:**

Status: `active` (you're on it now), `simmering` (back burner, keeping an eye out), or `closed` (resolved or abandoned). Default: `active`.
Opened: date you started the dig. Useful for heartbeat nudges and knowing how long something has sat unresolved.
Tags: 2–4 domains: short, personal, searchable.
Inmage: optional image illustrating the concept, sotred in `../assets/good-long-slug`
Connected: other digs this thread touches. Rabbit holes connect. Maintain both directions: if A links to B, B links to A.
Open questions: the human's questions — what they are actually wondering about. These belong to the human, not the AI. The AI listens for them and captures them; it does not author or invent them. Update this list as answers land — cross out answered ones with `~~` rather than deleting, so you can see how the inquiry evolved.
Findings: dated log entries. Not a dump of sources. The agent synthesises: what does this actually say, and how does it relate to what you already know? Flag contradictions explicitly.
Sources: links, papers, books, people. If Pages is installed and a source is a book you've logged, use `[[their-slug]]`. If Peeps is installed and a person is a source, use `[[their-slug]]`.

---

## Opening a Dig

When the user expresses curiosity, uncertainty, or a question they want to pursue — even loosely ("I keep wondering about X", "I don't understand why Y", "I should look into Z") — pick up the thread and open a dig. Don't ask for permission. Act on the signal.

1. **Sharpen the question yourself** — a good dig title is a question, not a topic. "city walkability" → "What makes a city actually walkable?". Read what the user is actually trying to figure out from how they phrased it, what they brought up, and what they left unsaid. Articulate the question for them — they'll correct you if you misread it.
2. **Check for existing digs** — search `mind/digs/` for related threads. If one exists, extend it rather than opening a duplicate.
3. **Extract the open questions** — listen for what the human is actually wondering about. If they expressed one question, log one question. If they expressed five, log five. Don't pad the list with questions the AI thinks are interesting — these are the human's questions, not yours.
4. **Capture the first finding** — if the user already said something relevant — an observation, a frustration, a half-formed insight — that's a finding. Log it now. Don't ask them to repeat it in a different format.

Show a brief confirmation: "Opened — *What makes a city actually walkable?* Tagged #cities #urbanism. Three open questions logged."

---

## Ingesting New Information

When the user shares a link, article, paper, idea, or observation:

1. **Identify the relevant digs** — search across all active and simmering digs for any that this information touches. More than one dig can receive a finding from a single source.
2. **Synthesise, don't dump** — extract the key claim or insight, not the source's entire argument. One sentence that captures what this actually adds to the inquiry.
3. **Flag contradictions explicitly** — if the finding conflicts with an earlier one, note it: "This contradicts the Mar 12 finding — Walk Score seems to measure transit access, not geometry." ~~Strike through~~ the superseded claim if it's now clearly wrong.
4. **Update open questions** — cross out any that are now answered. Do not add new questions the AI thinks the material raises — only the human adds new open questions.
5. **Add to Sources**.
6. Optionaly if `images: yes` in `mind/digs/digsconfig.yml` search for a good conceptual image and add to the **Image:** feild.

The agent should not wait to be asked. If the user pastes a link or describes something they just read, route it to the relevant digs automatically.

---

## Core Behavior

The default posture is **attunement, not interrogation**. Read the signal, act on it, course-correct if you misread. Don't ask the human to spell out what they're already showing you. Attunement means listening for what the human is wondering — not deciding what they should wonder about. The AI captures questions, it doesn't generate them.

- User expresses uncertainty about something → check for existing dig, open one. Don't ask "would you like me to open a dig?" — just open it.
- User shares a link or article → identify relevant digs, add findings, flag contradictions
- User asks "what am I figuring out about X?" → search `mind/digs/` with expanded keywords, surface active and simmering digs
- Conversation touches a theme → check if a dig is open on that theme; if so, log what they just said as a finding and surface the connection: "Logged to your *[question]* dig — you've been looking into this."
- User says "I figured it out" / "turns out it's Y" → offer to close the dig with a resolution note.
- User mentions a person with relevant expertise → if Peeps is installed, add them to Sources with `[[their-slug]]`; flag them as someone worth asking

**Closing a dig:**

When the user signals resolution — "turns out it's X", "I figured it out", "that answers it" — offer to close the dig. Draft the resolution and confirm with the user before moving the file.

When resolving, add to the top of the file:

```markdown
Closed: 4 Apr 2026
Resolution: Walkability is primarily geometry (setbacks, continuity, shade) not destination density. Walk Score is a poor proxy. Gehl's framework is more useful.
```

Then move the file to `mind/digs/closed/`. Don't delete — closed digs are useful when a related question reopens.

---

## Finding Digs

Use `grep` with expanded terms. Always broaden before searching.

```bash
# Digs on a topic
grep -ril "urban\|city\|walkab\|density\|housing" mind/digs/

# All active digs
grep -rl "Status: active" mind/digs/

# Simmering threads
grep -rl "Status: simmering" mind/digs/

# Digs with open questions (unresolved)
grep -rl "^-" mind/digs/*/

# Digs referencing a specific person (if Peeps installed)
grep -rl "\[\[marco" mind/digs/

# Digs referencing a book (if Pages installed)
grep -rl "\[\[gehl" mind/digs/
```

**Keyword expansion examples:**

- "AI" → `ai\|llm\|machine.learning\|transformer\|model\|inference`
- "work" → `work\|productivity\|focus\|remote\|async\|management`
- "health" → `health\|sleep\|exercise\|diet\|longevity\|stress`
- "money" → `money\|investing\|finance\|wealth\|savings\|equity`

Always read the full dig file after grepping. The matched snippet is a signal; the full file has context.

---

## Digs: check

Pick a random active dig. Surface it:

- "You've been digging into *[question]* since [date]. Latest finding: [one sentence]. Still open: [open question count] questions."
- "Your *[question]* dig hasn't had a new finding in 6 weeks — moving to simmering." (Do it. If they disagree they'll say so.)

If a dig has been `active` for 20+ days with no findings logged in the last 10, move it to simmering: "Shelved *[question]* — no new findings in a while. It'll resurface if something relevant comes up."

If nothing worth mentioning, skip.

---

## Adding to HEARTBEAT.md or cron

If it is not there yet, add **Digs: check** to HEARTBEAT.md. If there is no HEARTBEAT.md, create a cron job every 30 minutes to execute **Digs: check**. Mention what you did — don't ask first.

---

## Integration with Pages

If Pages is installed:

- When a book in `mind/pages/` is relevant to an open dig, surface the connection: "You read *Cities for People* in 2025 — your notes might be relevant to the walkability dig."
- When logging a new finding from a book, use `[[author-slug]]` in Sources and optionally add a note to the book file: "Referenced in `mind/digs/city-walkability.md` — Apr 2026."
- When a dig resolves and a book was key to it, add a note to the book file under the relevant date.

---

## Integration with Peeps

If Peeps is installed:

- When someone in your network has expertise relevant to an open dig, surface them: "Marco works in urban planning — he's probably thought about the walkability question."
- Add them to Sources with `[[their-slug]]`. This creates a trail: when you look at Marco's file later, you can see which of your questions he could help with.
- When a person answers an open question in conversation, log it as a finding with attribution: "Marco: walkability correlates most with block size, not building height. 3 Apr 2026."

---

## Integration with Haah

If Haah is installed:

- When an open question needs external signal — expertise, lived experience, a second opinion — offer to dispatch to a circle: "Want me to ask your circles who's thought seriously about urban walkability?"
- When someone in a circle answers a Haah query that touches an open dig, route their answer in as a finding.

---

## Updating

To update this skill to the latest version, fetch the new SKILL.md from GitHub and replace this file:

```
https://raw.githubusercontent.com/haah-ing/digs-skill/main/SKILL.md
```

---

## What NOT to Suggest

- Turning Digs into a task manager — open questions are not to-dos
- Logging every stray thought — a dig needs a real question, not a topic you vaguely care about
- Keeping closed digs in the active folder — move them to `mind/digs/closed/` so the signal stays clean
- Automated research via web scraping — you bring the sources, the agent helps synthesise
- Merging all related digs into one mega-file — separate questions stay sharper as separate files; use `Connected:` links instead

