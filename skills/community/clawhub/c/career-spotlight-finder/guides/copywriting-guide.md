# Copywriting Guide

This guide governs Step 4 of the Career Spotlight pipeline. Its purpose is voice transformation, not further analysis. The aggregated report (`~/.career-spotlight/report.md`) already contains all the content; this step reshapes it into copy that sounds like a real person talking about themselves with confidence.

---

## 1. Core Transformation

The report is analytical. The copy is personal. Every sentence must cross that bridge.

| Report Voice | Copy Voice |
|---|---|
| Third person ("The user demonstrated...") | First person ("I built...") |
| Comprehensive (every finding listed) | Cherry-picked for impact (only the best hits) |
| Structured listing (bullet after bullet) | Rhythmic with emphasis (vary length, lead with punch) |
| Objective and neutral | Confident and warm |

### How to apply this

- **Read the report first, then close it mentally.** Write as if you are the person explaining their work to someone they respect. Do not transcribe the report into first person; re-tell it.
- **Cut aggressively.** The report may surface 30 findings. The copy uses 8-15 of the best. If a bullet does not make someone lean in, it does not make the cut.
- **Vary sentence rhythm.** Three short sentences, then one longer one. A fragment for emphasis. Then a full thought. This keeps copy from sounding like a list someone put periods on.
- **Default to confident.** Replace hedging language ("helped to," "was involved in") with direct ownership ("designed," "led," "built"). If the report shows the person did the work, the copy should say so plainly.

### Before and after examples

**Bad (report voice pasted into first person):**
> I was responsible for the implementation of a microservices architecture that was adopted by the platform team, resulting in improvements to deployment frequency.

**Good (copy voice):**
> I broke a monolith into 12 microservices and cut deploy cycles from weekly to daily.

**Bad (hedging, no specifics):**
> I helped with various data pipeline improvements that contributed to better performance across the organization.

**Good (direct, concrete):**
> I redesigned the ingestion pipeline to handle 10TB/day -- a 4x throughput increase that eliminated the overnight processing backlog.

### Expert-first framing

- Lead with the report's **expert center**. The first impression should be "this person is clearly strong at X."
- Use supporting theme lines as **differentiators**, not as competing identities. The structure is still focused, but the differentiator must answer "why this person?" rather than reading like an afterthought.
- If the user's background spans adjacent directions, keep one credible center of gravity **without erasing the second strength that makes them memorable**.
- Never undercut the positioning with disclaimers such as "I'm not really an expert in X," "I'm not a pure specialist," or "I kind of do several things." The point of this step is to package the user's work into a confident, defensible expert story.

### Competitive wording and defensibility

- Default to **competitive mode**, not modest mode, for `resume-bullets.md` and `linkedin-summary.md`. These outputs should sound like a strong candidate competing in a crowded market.
- When several phrasings are all defensible, prefer the one with **higher signal, stronger market recognition, and more senior-feeling language**.
- It is acceptable to raise the level of abstraction by one step if that better captures the real value of the work:
  - "script" -> "workflow" or "pipeline"
  - "feature" -> "system capability"
  - "research" -> "algorithm design" or "method development"
  - "tool" -> "engineering workflow" or "platform layer" **only if the evidence supports it**
- Do **not** invent scale, ownership, leadership, production usage, or adoption. Competitive wording is allowed; fabricated claims are not.
- Use the **two-layer interview test**: if a hiring manager asked "what do you mean by that?" twice in a row, could the user still defend the wording with the underlying project? If not, the phrasing is too aggressive.

### Output register

Use different aggression levels for different outputs:

- **Resume bullets** — highest signal, most compressed, most prestige-oriented wording
- **LinkedIn summary** — polished and market-facing, still more elevated than conversational speech
- **Elevator pitch** — clear and memorable, moderately technical, less compressed
- **Casual intro** — simplest and least jargon-heavy; do not force prestige wording here

### Bridge profiles

When the report uses a bridge framing, the copy should preserve the combination as part of the selling point.

- Prefer **arc-first** writing when the combination itself is the story: "I started with X, that led me into Y, and what makes me different is that I can connect both to Z."
- Do not reduce the secondary line to a weak final clause if it is core to the user's distinctiveness.
- Keep the copy legible and focused, but allow the user to sound more interesting than a single narrow job-title label would allow.

---

## 2. Resume Bullets

### Selection

1. Read every theme line in the report, starting with the main theme.
2. Select 8-15 highlights total. Prioritize the main theme line -- it should have the most bullets.
3. For each highlight, ask: "Would a hiring manager pause on this?" If no, cut it.

### Format

Every bullet follows this structure:

**Action verb** + **Object** + **Quantified result** (when numbers are available)

Examples:
- Architected a distributed event-processing system handling 2M events/hour across 4 regions
- Reduced CI/CD pipeline duration from 45 minutes to 8 minutes by parallelizing test stages
- Led a 6-person team through a zero-downtime migration from on-prem to AWS, completing 3 weeks ahead of schedule
- Designed an internal CLI tool adopted by 40+ engineers, eliminating 5 hours/week of manual deployment steps

### Grouping

Group bullets by theme line. Main theme line bullets come first, then supporting, then supplementary. Add a heading for each group using the theme line name.

Heading names should be market-legible and clearly distinct from each other. Do not use overlapping headings that sound like variants of the same bucket. For example, prefer:

- `Distributed RL Systems and Post-Training Infrastructure`
- `Applied Reinforcement Learning Algorithms`
- `AI-native Product Engineering`

over weaker pairings like:

- `Reinforcement Learning Systems`
- `Reinforcement Learning Research`

### Preferred verbs

Use these when they fit the situation accurately:
- Designed, Built, Led, Optimized, Deployed, Architected, Migrated, Automated, Reduced, Increased

When defensible, also consider stronger high-signal verbs such as:
- Engineered, Orchestrated, Directed, Spearheaded, Scaled, Reframed, Operationalized

### Verbs to avoid

Never use these -- they dilute ownership:
- Helped, Assisted, Participated, Was responsible for

If the report uses "helped" language, determine from context whether the person drove the work. If yes, use a direct verb. If the person genuinely played a supporting role, reframe to show the specific contribution ("Wrote the migration playbook used by 3 teams" rather than "Helped with the migration").

### When numbers are missing

Not every bullet needs a number. When quantified results are unavailable, substitute scope or outcome:
- **Scope:** "...serving 200K daily active users" or "...across 4 engineering teams"
- **Outcome:** "...eliminating a recurring production incident" or "...adopted as the team standard"

Do not invent numbers. Do not estimate. Use only what the report supports.

---

## 3. Elevator Pitch

### Constraints

- 80-120 words. No exceptions. Count them.
- Must sound natural when read aloud. Test by reading it to yourself. If you stumble, rewrite.
- Must be memorizable. Short sentences. No jargon. No acronyms unless they are universally understood (e.g., "API" is fine; "CQRS" is not).

### Formula

```
[Who I am] + [Main strength from main theme] + [One concrete proof point with numbers if possible] + [Differentiator from supporting theme]
```

For bridge profiles, this alternative formula often works better:

```
[Where I started] + [What that led me into] + [Current center of gravity] + [What makes me different]
```

### Example

> I'm a backend engineer who specializes in making systems scale without falling over. At my last company, I redesigned the data pipeline to handle a 4x traffic increase with no added infrastructure cost. What sets me apart is that I don't just build for performance -- I build for the team. Every system I ship comes with runbooks, dashboards, and a handoff plan so the on-call engineer at 2 AM isn't guessing.

(96 words. Spoken tone. Concrete proof point. Clear differentiator.)

### Common mistakes

- **Too abstract:** "I'm passionate about building scalable solutions that drive business value." This says nothing. Replace with a specific example.
- **Too long:** If it's over 120 words, something is filler. Find it and cut it.
- **Too jargon-heavy:** "I specialize in event-driven CQRS architectures with eventual consistency guarantees." Nobody memorizes this. Translate to human language.

---

## 4. LinkedIn Summary

### Constraints

- 150-300 words.
- Professional but not stiff. Write as if addressing a respected colleague, not a dissertation committee.
- Naturally embed industry keywords throughout. LinkedIn search matches on these terms, so they affect discoverability. Pull keywords from the report's Term Mapping Table.
- This is a market-facing surface. It should sound stronger and more polished than casual conversation, and it may use higher-signal terminology as long as every claim stays defensible.

### Structure

**Opening (1-2 sentences):** The positioning statement from the report. This is the hook. It should make someone want to keep reading.

**Body (2-3 short paragraphs):** Expand the main theme line and at least one supporting theme line. For each, include 1-2 concrete examples. Use the same direct, first-person voice as the resume bullets but in flowing prose rather than bullet format.

If the user is a bridge profile, the body should make the progression or combination explicit rather than treating the second strong line as a side note.

**Close (1-2 sentences):** What excites you or what you are looking for. This gives recruiters a reason to reach out and signals openness.

### Example opening

> I build backend systems that hold up under pressure. Over the past seven years, I've specialized in data-intensive platforms -- the kind where a bad design decision at the architecture layer costs you six figures in compute by Thursday.

### Example close

> I'm currently exploring roles where I can pair deep systems work with early-stage product decisions. If your team is solving hard infrastructure problems and shipping fast, I'd like to hear about it.

### Keyword embedding

Do not dump a keyword list at the bottom. Instead, weave terms naturally:
- **Bad:** "Skills: Python, Kafka, AWS, Terraform, Kubernetes, CI/CD, microservices"
- **Good:** "I've spent the last three years building event-driven pipelines on Kafka and AWS, with Terraform managing the infrastructure and Kubernetes keeping it portable."

When several terms are all accurate, prefer the term a hiring manager is more likely to recognize as high-value. The goal is not to sound inflated; it is to avoid underselling strong work with flat wording.

---

## 5. Casual Intro

### Constraints

- 2-3 sentences. Maximum.
- Zero jargon. A non-technical family member should understand it.
- Must end with a conversational hook -- something that invites a follow-up question.

### Formula

```
[What I do in plain terms] + [What makes it interesting] + [Conversational hook that invites follow-up]
```

### Example

> I build the behind-the-scenes systems that keep apps running when millions of people use them at the same time. The fun part is figuring out how to make them faster and cheaper without anyone noticing a thing. Right now I'm working on a problem where we have to process a full day's worth of data in under ten minutes -- it's like a puzzle with very expensive wrong answers.

### How to test it

Read it aloud to an imaginary person at a dinner party. If they would say "oh, interesting -- how does that work?" you succeeded. If they would nod politely and change the subject, rewrite.

### Common mistakes

- **Accidentally technical:** "I work on distributed systems" -- most people do not know what this means. Say "I build the behind-the-scenes systems that keep apps running smoothly."
- **Too vague:** "I work in tech" -- this invites zero follow-up. Be specific about what makes your work interesting.
- **No hook:** Without the conversational thread-pull at the end, the intro is a dead end. Always close with something that makes the listener curious.

---

## 6. Privacy

### Default behavior

Always generalize company names and proprietary project details unless the user has explicitly said otherwise.

| Real Detail | Generalized Version |
|---|---|
| Stripe | a major fintech company |
| Walmart | a Fortune 500 retailer |
| Project Nightingale (internal codename) | an internal platform migration |
| 23M users (if the number is identifiable) | millions of users |

### Rules

1. **Company names:** Replace with descriptive phrases: "a Series B healthtech startup," "a top-3 cloud provider," "a Fortune 500 retailer."
2. **Internal project names:** Replace with functional descriptions: "a real-time fraud detection system," "an internal developer productivity platform."
3. **Metrics that could identify a company:** Generalize the scale: "millions of daily transactions" instead of "4.2M daily transactions" if that number is publicly traceable to one company.
4. **If user explicitly approves real names:** Use them. Note in the copy file frontmatter: `privacy: user-approved-real-names`.
5. **When in doubt:** Generalize. It is always safer to be vague about employers and specific about your own contributions.

---

## 7. Output

### Files to write

Write four separate files to `~/.career-spotlight/copies/`:

| File | Content |
|---|---|
| `resume-bullets.md` | Resume bullets (Section 2) |
| `elevator-pitch.md` | Elevator pitch (Section 3) |
| `linkedin-summary.md` | LinkedIn summary (Section 4) |
| `casual-intro.md` | Casual intro (Section 5) |

Each file should use the corresponding section of `templates/copywriting-variants.md` as its format reference.

### Archiving

Before writing any new copy file, check if the file already exists in `~/.career-spotlight/copies/`. If it does:

1. Move it to `~/.career-spotlight/history/`.
2. Rename it with a full timestamp: `[original-name]-YYYY-MM-DDTHH-MM-SS.md`.
   - Example: `resume-bullets.md` becomes `resume-bullets-2026-03-23T14-30-00.md`.
3. Use the current time at the moment of archiving. Do not reuse timestamps from previous runs.

Archive all existing copy files before writing any new ones. This ensures the full previous set is preserved as a unit.

### File format

Each copy file should include a brief YAML frontmatter block:

```yaml
---
generated: YYYY-MM-DDTHH:MM:SS
source_report: ~/.career-spotlight/report.md
privacy: generalized  # or "user-approved-real-names"
---
```

Followed by the copy content itself, formatted in clean Markdown.

### Final check

After writing all four files, re-read each one and verify:
- Resume bullets: 8-15 bullets, action-verb format, grouped by theme
- Elevator pitch: 80-120 words, sounds natural aloud
- LinkedIn summary: 150-300 words, keywords embedded naturally, has opening/body/close
- Casual intro: 2-3 sentences, no jargon, ends with a hook
