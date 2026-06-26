---
name: digital-twin
description: >
  Build a psychologically grounded Digital Twin personality skill that makes an agent speak, think,
  decide, and adapt like a specific real person. Use this skill whenever the user asks to create a
  digital twin, personality clone, shadow persona, AI stand-in, or personality skill for a named
  person — including phrasings like "make an AI version of [name]", "clone [name]'s personality",
  "build a persona for [name]", "create a shadow skill for [name]", "train a twin on [name]", or
  "I want the agent to respond as [name]". Also use it when the user asks to update or refresh an
  existing personality skill with newer data. The twin is built by analyzing samples of the target
  person's own communication across four psychological and linguistic pillars; the output is an
  installable {name}_personality skill that matches their speech patterns, thinking style,
  decision-making, and audience-awareness. IMPORTANT: this skill does NOT connect to any data
  source itself and does NOT require, request, or store any API keys, tokens, or credentials. It
  sources its training data entirely from connections the user has ALREADY set up — any meeting/call
  transcript service (Fireflies, Otter, Fathom, Granola, Zoom, Teams, etc.), email, Slack, Teams
  chat, document stores, or other MCP connectors/skills the user controls. It is a consumer of
  whatever the user has connected, not an integration. This skill builds personality, voice, and
  judgment — not factual memory or recall. Pair it with a vector database for memory if full digital
  twin fidelity is needed.
---

# Digital Twin Skill — Personal AI Stand-In Builder

## Purpose

This skill analyzes samples of a person's own communication — meeting and call transcripts from any
service, sent emails, Slack/Teams or other chat messages, documents they authored, and any other
available source — across four psychological and linguistic pillars. From that analysis it produces
an installable **personality skill**: a structured persona document that makes Claude speak, think,
decide, and adapt to audiences the way that person actually does.

The output skill is named `{name}_personality` (e.g., `joes_personality`) and can be activated on
demand ("respond as if you were Joe") or set as a default persona for all communications.

**This skill builds personality, voice, and judgment — not factual memory.** It captures HOW someone
thinks and communicates, not WHAT they know or remember. For a full digital twin, pair the generated
personality skill with a vector database containing the person's domain knowledge and history.

---

## A Note on Data Access — Read This First

This skill **does not connect to any service and does not handle authentication.** It never requires,
requests, or stores API keys, tokens, or credentials of any kind. It relies entirely on data sources
the **user has already connected** — their own MCP connectors and skills, configured under their own
account with their own access scopes.

The agent running this skill should:

1. Check which connected sources are available to it (e.g., a transcript service, an email connector,
   a Slack/Teams connector, a document store) by inspecting available MCP servers/tools/skills.
2. Ask the user who to clone and which connected sources to draw from.
3. Pull the target person's communication samples **through those existing connections**.

If the user has no usable source connected, do not attempt to connect one. Instead, tell them to
install and configure an appropriate connector or skill first (pointing them to their platform's
skill/connector marketplace), then return. This skill is a consumer of connected sources, never the
integration itself.

---

## Prerequisites

Before starting, verify:

1. **At least one connected source of the target person's communication is available.** Acceptable
   sources include, in any combination: meeting/call transcripts from any transcript service, sent
   emails, chat messages (Slack, Teams, etc.), documents the person authored, or anything else
   containing a substantial volume of their own words. It is the user's responsibility to have these
   sources connected and working. The agent only needs to know *who* to clone and *from which
   sources* — it can inspect available MCP tools/connectors to see what is reachable, but it does
   not set anything up. If nothing usable is connected, stop and direct the user to connect a source
   first (see "A Note on Data Access" above).

2. **Sufficient content volume.** More of the person's own words produces a richer twin. Rough
   guidance, subject to availability:
   - **Transcripts:** 5 minimum recommended; 10+ across varied meeting types (1:1s, team meetings,
     leadership reviews, cross-functional calls) is dramatically better.
   - **Emails:** ideally ~50 sent emails with reasonable content per email.
   - **Chat (Slack/Teams/etc.):** ideally ~50 messages of substance.
   - **Documents and other sources:** anything the person authored can be leveraged.

   These are guidelines, not gates. Take whatever usable content is available across all sources. If
   the total content is minimal and no well-trained profile already exists, warn the user that the
   resulting profile will be shallow and may not capture audience adaptation or decision patterns
   well. A profile can always be updated later from additional sources — and refreshing it
   periodically is good practice, as it captures more of the person's range as the profile matures.

3. **The target person is identifiable in the sources.** Their name must appear as a speaker label,
   sender, or author so their contributions can be isolated. Ask the user to confirm the exact name
   as it appears in the source data if there is any ambiguity.

### Consent & Privacy

Before proceeding with any analysis, confirm the following with the user:

- **Target person consent**: The user should have the target person's knowledge and consent before
  building a personality profile of them. If the user is profiling themselves, this is implicit. If
  they are profiling someone else, remind them that they are responsible for obtaining that person's
  consent. Do not proceed until the user confirms consent.
- **Third-party data**: Sources may contain contributions from other people (other meeting
  participants, email recipients, chat counterparts). This skill extracts ONLY the target person's
  contributions for analysis. Other people's names appear only in metadata for audience
  categorization (determining relationship types). No personality analysis is performed on anyone
  but the target.
- **Data handling**: All analysis is performed in-session. This skill does not persist, export, or
  transmit raw source content anywhere. The only output is the generated personality skill
  containing derived behavioral patterns — not raw source content. The user's own connections handle
  all data access and are governed by whatever permissions and scopes the user configured on them.

---

## User Invocation Patterns

The user triggers this skill with a request like:

> "Use the digital twin skill to create a personality skill for John Doe from his last 10 meeting
> transcripts and his sent email."

The key parameters to extract from the user's request:

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| **Target person name** | Yes | — | "John Doe" |
| **Sources to draw from** | No | All connected sources with usable data | "transcripts and Slack" |
| **Volume per source** | No | Recent available (see Prerequisites) | "last 15 meetings", "~50 emails" |
| **Additional context** | No | — | "He's the VP of Engineering, tends to be very direct" |
| **Audience types to focus on** | No | Auto-detect | "Focus on his leadership meetings and 1:1s" |

If the user doesn't specify volume, pull a reasonable recent set from each available source. Inform
them: more content = longer processing time but richer personality capture. Each sample is analyzed
individually before compositing.

---

## Execution Workflow

### Phase 1: Source Retrieval

Pull the target person's communication samples **through the user's existing connections**. This
skill does not connect to sources directly and does not maintain its own vectorized memory of the
content — it calls the user's own MCP tools, connectors, and skills, which handle authentication and
access using the user's credentials and scopes.

1. For each connected source the user pointed you to, query for recent items where the target person
   is a participant, sender, or author (meetings, email threads, chat messages, documents). If a
   source returns an error or is unavailable, note it and continue with the others; if no source is
   reachable at all, stop and tell the user to check their connector/skill configuration.
2. For each item, extract ONLY the target person's contributions — their statements, responses,
   questions, reasoning, and authored text — preserving the surrounding context (who they were
   responding to, what was asked of them) but focusing analysis on their words. Do not retain or
   analyze other people's content beyond what's needed for audience categorization.
3. Tag each sample with metadata:
   - Source type (transcript / email / chat / document / other) and date
   - Title or topic
   - Other participants or recipients (to determine audience type)
   - Approximate share of the exchange that is the target person's own words
4. Categorize each sample by audience type for Pillar 4 analysis:
   - **Leadership/Upward**: Exchanges with their superiors or executive leadership
   - **Peer/Lateral**: Exchanges with colleagues at a similar level
   - **Direct Report/Downward**: Exchanges with people they manage
   - **Cross-Functional**: Exchanges with people from other departments
   - **External**: Client, vendor, partner, or investor exchanges
   - **Mixed**: Group settings with multiple relationship types

   For one-directional sources (e.g., an authored document or a broadcast message), categorize by
   intended audience where it can be inferred, and note that interactive dynamics won't be observable.

Store extracted contributions in a working structure organized by sample.

### Phase 2: Four-Pillar Analysis

Process EACH sample individually through all four pillars. This is critical — do not batch or
summarize samples before analysis. Each sample gets its own pillar scores and observations. The
composite comes AFTER individual analysis.

Read the detailed methodology for each pillar from the references directory:

- **Pillar 1 — Linguistic Profiling**: Read `references/pillar_1_linguistic.md`
- **Pillar 2 — Psychometric Profiling**: Read `references/pillar_2_psychometric.md`
- **Pillar 3 — Judgment & Decision Patterns**: Read `references/pillar_3_judgment.md`
- **Pillar 4 — Contextual Audience Profiling**: Read `references/pillar_4_audience.md`

Some dimensions (e.g., turn-taking, response latency, in-conversation acknowledgment) are only
observable in interactive sources like transcripts and chats. For one-directional sources like
emails and documents, analyze the dimensions that are present and skip the ones that aren't — do not
invent observations the source can't support.

For each sample, produce a structured analysis document covering all four pillars. Then proceed to
compositing.

### Phase 3: Composite Profile Generation

After all samples are individually analyzed:

**Pillar 1 — Linguistic Composite:**
- Merge all linguistic observations into a unified style guide
- Identify patterns that appear in 60%+ of samples as "core patterns"
- Note patterns that appear in fewer as "situational patterns" tied to specific contexts or source
  types (e.g., written email vs. spoken meeting)
- Resolve contradictions by weighting more recent samples slightly higher

**Pillar 2 — Psychometric Composite:**
- For each OCEAN dimension: average the per-sample scores to get a final score (1-100 scale)
- Calculate standard deviation — high deviation means the person's expression of that trait is
  context-dependent (note this)
- Composite the conflict style, risk tolerance, and communication priority assessments using
  majority-vote across samples
- Write the psychometric narrative summary (see Pillar 2 reference for format)

**Pillar 3 — Judgment Composite:**
- Merge all decision pattern observations into a unified decision pattern library
- Build the stance map from consistent positions observed across 2+ samples
- Document reasoning chains with representative examples
- Flag any stances that shifted over time (evolution of thinking)

**Pillar 4 — Audience Composite:**
- For each audience category with sufficient data (2+ samples), produce a distinct communication
  profile
- If an audience category has only 1 sample, mark it as "preliminary — low confidence"
- Identify the person's default/baseline mode (most common audience type)

### Phase 4: Personality Skill Assembly

Using the composite profiles, generate the installable personality skill. The skill uses the
template in `references/personality_skill_template.md` and is output as a complete skill directory:

```
{name}_personality/
├── SKILL.md          (the personality skill itself)
└── references/
    ├── linguistic_profile.md
    ├── psychometric_profile.md
    ├── decision_patterns.md
    └── audience_profiles.md
```

The generated SKILL.md must include:

1. **Frontmatter** with a description that triggers on "respond as {name}", "be {name}", "use
   {name}'s personality", or when the skill has been set as default for all communications.
2. **Response Generation Pipeline** — the step-by-step instruction set telling Claude how to process
   any incoming message through the personality:
   - Step 1: Identify the audience context (who is being spoken to, what's the relationship)
   - Step 2: Select the matching audience communication profile
   - Step 3: Match the question/topic to a decision pattern category if applicable
   - Step 4: Check the stance map for any pre-existing positions on the topic
   - Step 5: Generate the response content using the judgment profile and psychometric tendencies
   - Step 6: Pass the draft through the linguistic filter with the correct audience mode
   - Step 7: Final check — does this read like {name} wrote it, to this specific person?
3. **Quick-reference persona card** at the top of SKILL.md summarizing OCEAN scores, core linguistic
   markers, and top 5 stance positions for fast context loading.
4. **Pointers to reference files** for the full profiles, with guidance on when to consult each one.

### Phase 5: Installation and Delivery

1. Package the personality skill directory.
2. Present it to the user with a summary:
   - OCEAN scores with brief interpretation
   - Top linguistic markers identified
   - Number of decision patterns captured
   - Audience profiles generated (and confidence level for each)
   - Which sources fed the build, and any caveats or gaps (e.g., "No external meeting data was
     available, so client-facing behavior is not captured" or "Built from email only — spoken
     conversational dynamics are not represented")
3. Explain how to use it:
   - Install the skill in their agent's skill directory
   - To always use it: set it as a default skill in the agent's configuration
   - To use on-demand: say "respond as if you were {name}" or "use {name}'s personality"
4. Remind them the profile can be regenerated anytime if the shadow drifts from how the person
   currently communicates — just rerun with fresh samples from any source.

---

## Important Processing Notes

- **One sample at a time.** Each sample must be fully analyzed through all four pillars before moving
  to the next. This is slower but produces dramatically better results, because cross-sample patterns
  emerge from individual analysis, not from pre-summarized mush.
- **More content takes longer.** Set expectations with the user. A 10-sample build may take
  significant processing time; a 20-sample build will take roughly twice as long.
- **Mix sources where possible.** A twin built from transcripts plus email plus chat captures both
  spoken and written voice and adapts across more contexts than one built from a single source type.
- **User-provided context helps.** If the user says "He's the CTO and tends to be very data-driven,"
  that context helps calibrate the analysis — especially for audience categorization and
  understanding the person's position in the org hierarchy.
- **This is personality, not memory.** The skill captures HOW someone thinks and communicates, not
  WHAT they know. For a full digital twin, pair with a vector database of their domain knowledge and
  conversation history.

---

## Rerun / Update Protocol

Profiles should be refreshed periodically as the person evolves and as more of their communication
becomes available. If the user asks to update an existing personality skill:

1. Pull new samples through the user's existing connections (user specifies sources and how many).
2. Run the full four-pillar analysis on the new samples.
3. Blend with the existing profile, weighting new data at 60% and existing at 40% (recency bias —
   people evolve).
4. Regenerate the skill with the updated composite.
5. Note what changed in the update summary.

---

## Reference Files

| File | When to Read | Purpose |
|------|-------------|---------|
| `references/pillar_1_linguistic.md` | Phase 2, for each sample | Full linguistic analysis methodology |
| `references/pillar_2_psychometric.md` | Phase 2, for each sample | OCEAN scoring rubric and psychometric assessment method |
| `references/pillar_3_judgment.md` | Phase 2, for each sample | Decision pattern extraction and stance mapping method |
| `references/pillar_4_audience.md` | Phase 2, for each sample | Audience-adaptive communication profiling method |
| `references/personality_skill_template.md` | Phase 4 | Template for the generated personality skill |
