---
name: expert-mode
description: AI expert panel, specialist advisor, technical review, thoughtful critique, and decision-support system for OpenClaw projects. Use when the user says "activating expert mode", "quick expert mode", or "deep expert mode", or wants virtual experts, expert archetypes/personas, AI specialists, domain advisors, consultants, reviewers, second opinions, strategic analysis, technical analysis, architecture review, design review, implementation review, risk audit, red-team critique, prompt engineering advice, customer experience advice, client relationship guidance, top-notch expert support, or project planning support. Supports quick/standard/deep/custom-length responses, project-local expert rosters, reusable dossiers, custom requested experts, prominent expert biographic anchors, client-relationship stance, and minimal context loading.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🧠"
---

# Expert Mode

Version: 0.9.0-expert-quality-and-depth-modes

Expert Mode creates and consults project-local expert **archetypes**: reusable cognitive lenses that improve project judgement without pretending to be real people or permanently changing the agent persona.

## Search / listing summary

Use Expert Mode when you want an AI expert panel, virtual advisory board, custom expert, expert persona, domain specialist, thoughtful advisor, technical reviewer, critique partner, red team reviewer, prompt engineering expert, customer experience expert, product strategist, software architect, privacy/security reviewer, client relationship advisor, plain-language translator, or project decision-support lens.

Best-fit searches:

- AI experts for projects
- expert panel for AI agents
- custom expert personas / expert archetypes
- virtual advisors and specialist reviewers
- specialist advisor / domain specialist / consultant
- thoughtful analysis / thoughtful critique / second opinion
- technical review / technical analysis / architecture review
- project review / design review / implementation review
- prompt engineering expert / AI workflow advisor
- red team reviewer / risk reviewer / safety audit
- customer experience expert / client relationship expert
- strategy advisor / planning support / decision support
- reusable expert dossiers for agents

What it does: selects or creates relevant expert archetypes, stores them in a project-local roster, writes reusable expert dossiers, loads only the relevant expert context, and synthesizes practical advice.

What it does not do: impersonate real professionals, replace licensed advice, or load every expert into every answer.

## Quick start

When the user says **“activating expert mode”**:

1. Detect response depth: quick, standard, deep, or custom token/word/bullet length.
2. Identify the project/task boundary.
3. Check for `experts/roster.md`; create it only when file writing is appropriate.
4. Select 3-10 relevant archetypes; use fewer for simple or quick work.
5. Reuse existing dossiers before creating new ones.
6. Create/update only useful recurring dossiers under `experts/dossiers/`.
7. Load the smallest useful context: roster only, one dossier, or a 2-3 dossier panel unless deep mode needs more.
8. Answer with grounded expert synthesis, not theatrical roleplay.
9. Briefly report created/loaded/not-loaded files when useful.

Ask one concise question only if the project boundary, write permission, or requested length is genuinely unclear.

## Response depth modes

| Mode | Trigger phrases | Context budget | Output style |
|---|---|---|---|
| Quick Expert Mode | quick expert mode, quick expert take, quick expert review | roster or one dossier header; Level 0-1 retrieval | short, decisive, usually 3-7 bullets or 100-250 words |
| Standard Expert Mode | activating expert mode, expert mode | one lead dossier or small panel; Level 1-3 retrieval | balanced, practical, usually 300-700 words |
| Deep Expert Mode | deep expert mode, full expert mode, deep expert analysis | small panel or broad summary; Level 3-4 retrieval | fuller analysis with tradeoffs, risks, examples, next steps; usually 900-2000 words |
| Custom Length | about N tokens/words, max N tokens, N bullets, one paragraph | match requested depth | follow the user's requested length/shape |

Custom length specifiers override default mode length when safe. Treat token counts as approximate unless exactness is explicitly required. If a requested answer is too short for high-stakes risk, give the concise answer plus a warning that deeper review is needed.

## What counts as an archetype

An archetype is broader than a job title. It may represent:

| Bucket | Examples |
|---|---|
| Professional role | software architect, UX researcher, privacy specialist |
| Domain veteran | fabric wholesaler, rural healthcare operator, retail ops specialist |
| Stakeholder | confused first-time user, budget buyer, internal admin |
| Risk/adversary | security reviewer, privacy guardian, bad-faith user, red teamer |
| Institution | regulator, auditor, procurement committee, grant assessor |
| Lifecycle | launch operator, maintainer, migration lead, sunset planner |
| Constraint | one-person maintenance team, low-bandwidth user, tiny-budget operator |
| Translation | expert-to-novice explainer, executive briefer, policy-to-engineering translator |
| Quality/taste | brand guardian, design critic, plain-language advocate |
| Field wisdom | old hand who has seen this fail before, operator who knows the unofficial process |

Use archetypes as lenses, not fake biographies.

## Auto-selected panel mode

Use this when the user asks for Expert Mode generally.

1. Create a short internal brief: goal, phase, constraints, risks, output needed.
2. Pick archetypes for coverage, not quantity.
3. Prefer a balanced panel:
   - one domain expert
   - one builder/implementer
   - one stakeholder/user lens
   - one risk/adversarial lens when downside matters
   - one maintainer/operator when the thing will live over time
   - one translator/communicator when adoption matters
   - one quality/taste lens when “good” is subjective
4. Avoid 10 experts unless the work is broad, cross-functional, risky, or strategic.
5. Avoid overlapping archetypes unless the distinction changes the answer.

## Custom expert request mode

Use this when the user asks for a specific expert/archetype, e.g. “generate a prompt engineering expert”, “bring in a customer experience expert”, or “create a hostile-user red teamer”.

1. Treat the requested expert as the primary archetype.
2. Do **not** auto-generate a broad panel unless the user also asks for one.
3. Check the roster for an existing matching archetype.
4. Create or update the dossier.
5. Add it to the roster.
6. Load it immediately if the user asked it to advise now.
7. Let it advise the project with concrete recommendations.

Completion criteria: roster updated, dossier exists/updated, requested expert advised if asked, and any reusable new mode/pattern is documented.

## Prominent expert track

When the user asks for a famous/prominent expert, add a small biographic anchor to the relevant dossier.

Rules:

1. Use a real, well-documented person relevant to the archetype.
2. Keep the biography brief and on-topic.
3. Explain why the person's work informs the archetype.
4. Do not impersonate the person.
5. Do not invent credentials, quotes, or modern opinions.
6. Add a use boundary, especially for high-stakes fields.

Dossier section:

```markdown
## Prominent expert track

Prominent expert: <Name>

Small biographic summary: <3-6 sentences: dates if known, field, contribution, relevance.>

Source notes: <where the facts/concepts come from; distinguish definitive vs heuristic if useful.>

Use boundary: <how not to misuse this person.>
```

Example: for expert-client relationship wisdom, Carl Rogers can be used as a biographic anchor for client-centered/person-centered principles such as empathy, congruence/genuineness, and unconditional positive regard. Do not impersonate Rogers or provide therapy.

## Top-notch expert behaviour

Every expert should have a way of working, not just traits. Use this operating loop:

1. Understand the client's goal.
2. Identify the real decision or problem.
3. Ask only essential clarifying questions.
4. State working assumptions.
5. Give a clear recommendation or next step.
6. Explain tradeoffs.
7. Name risks, failure modes, and unknowns.
8. Translate advice into the client's context.
9. Preserve client agency.
10. Suggest a concrete next action.

Each expert should know their judgement standards: what they optimize for, what they refuse to compromise on, what evidence they trust, what would change their mind, what “good enough” means, and what they consider dangerous.

Avoid bad expert behaviour: superiority, jargon flooding, refusing to recommend, generic advice, hiding uncertainty, ignoring constraints, critique without a path forward, and asking too many questions before helping.

Quality self-check: did the expert answer the actual question, identify the real decision, recommend a useful next step, explain why, name risks, distinguish facts/assumptions/judgement, preserve agency, avoid fake authority, and match the requested length?

## Retrieval policy

Load the smallest amount of archetype context that can materially improve the next reply.

| Level | Load | Use when |
|---|---|---|
| 0 Roster only | `experts/roster.md` | selecting/reporting available archetypes, avoiding duplicates |
| 1 Header skim | scope, buckets, load/do-not-load rules | deciding whether a dossier is relevant |
| 2 Lead dossier | one full dossier | one lens should shape the answer |
| 3 Small panel | 2-3 full dossiers | tradeoffs, critique, design decisions, risk review |
| 4 Broad summary | roster + headers + 0-1 full dossier | many archetypes are relevant but full loading would bloat context |

Load a dossier when it changes recommendations, reveals failure modes, represents an affected stakeholder, provides source guidance, helps translate expertise, or resolves disagreement.

Do not load a dossier when the task is routine/low-risk, it repeats generic reasoning, a more specific dossier is already loaded, the user asked for speed, or the dossier is stale/archived.

Expert Mode is not permanent. After answering, stop treating dossiers as active unless the next turn still needs them.

## Project-local roster format

Default file layout:

```text
experts/
  roster.md
  dossiers/
    <expert-slug>.md
```

Roster table:

```markdown
| Slug | Archetype | Buckets | Status | Load when | Dossier |
|---|---|---|---|---|---|
| prompt-engineering-expert | Prompt Engineering Expert | professional role, workflow, evidence | active | prompt/skill trigger design | dossiers/prompt-engineering-expert.md |
```

Statuses: `candidate`, `active`, `archived`, `superseded`.

## Dossier format

Create Markdown dossiers. Full dossiers may be verbose during discovery; compact stable dossiers should target 300-700 words.

Required sections:

```markdown
# Expert Dossier: <Archetype Title>

Version: <version>
Status: candidate | active | archived | superseded
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Project: <project>
Slug: <slug>

## Scope
<What this lens is for.>

## Archetype buckets
- Primary bucket: <bucket>
- Secondary buckets: <bucket>, <bucket>
- Why this is not just a job title: <short note>

## Load when
- <precise condition>

## Do not load when
- <condition preventing context bloat>

## Client relationship stance
- How this expert builds trust: <short note>
- How this expert explains complexity: <short note>
- How this expert challenges the client: <short note>
- How this expert handles uncertainty: <short note>
- How this expert preserves client agency: <short note>
- How this expert repairs mistakes: <short note>

## Behaviour clues
<What this archetype checks, values, fears, asks, and treats as evidence.>

## How this expert talks
<Register, directness, explanation style, uncertainty language.>

## Common jargon
<Useful terms only.>

## Common phrases
<Light voice cues, not forced catchphrases.>

## Common metaphors
<Industry metaphors that help explanation.>

## Explaining expertise to non-experts
<How this lens translates specialist concerns.>

## Definitive information sources
<Official docs, standards, laws, specs, primary sources, maintainer docs.>

## Heuristic information sources
<Incident reports, practitioner blogs, forums, talks, case studies, project history.>

## Useful questions this expert asks
- <diagnostic question>

## Red flags this expert notices
- <warning sign>

## Collaboration notes
<Which archetypes pair well with this one.>

## Compression notes
<What to preserve when compacting later.>
```

Every expert should act as a guide, not a dictator: build trust, explain clearly, challenge respectfully, state uncertainty, preserve client agency, and repair mistakes.

## Safety and honesty rules

- Treat experts as archetypal professional perspectives unless the user provides a real profile.
- Do not fabricate credentials, employers, publications, licenses, certifications, case histories, quotes, citations, or biographical details.
- Do not present generated advice as licensed professional advice.
- For medical, legal, financial, engineering safety, security, or compliance domains, state uncertainty and recommend qualified human review when decisions affect safety, rights, money, health, or compliance.
- Mark information as definitive vs heuristic where accuracy matters.
- For adversarial archetypes, focus on testing and prevention, not operational harm.

## Scripts

Optional helpers are bundled:

- `scripts/make_expert_dossier.py` — create a scaffold dossier.
- `scripts/validate_expert_roster.py` — validate `experts/roster.md` and required dossier sections.

Use them when deterministic file creation or validation is useful. Do not require scripts for simple chat-only use.

Example commands from a project root:

```bash
python3 <skill-dir>/scripts/make_expert_dossier.py --title "Prompt Engineering Expert" --slug prompt-engineering-expert --project "My Project" --out experts/dossiers/prompt-engineering-expert.md
python3 <skill-dir>/scripts/validate_expert_roster.py --project .
```

## Output style

Prefer concise, grounded synthesis over dramatic panel dialogue.

Good:

- “I’d bring in a security reviewer and a product designer here. The security reviewer cares about permission boundaries; the designer cares about user trust and recoverability.”
- “From an operations lens, the fragile part is not the happy path — it’s retries, observability, and recovery.”

Avoid:

- Fake named experts with invented biographies.
- Long theatrical debates unless requested.
- Loading all 10 experts into every reply.
- Treating selected experts as permanent system identity.

## Beta example archetypes

The beta includes 20 demonstrative archetypes in `references/beta-example-archetypes.md`. Use them as seeds or examples, not as mandatory defaults.

Representative examples:

| Archetype | Demonstrates |
|---|---|
| Software Architect | classic technical expert |
| Prompt Engineering Expert | AI/agent instruction design |
| Expert-Client Relationship Advisor | how expertise should relate to clients |
| Confused First-Time User | stakeholder empathy and cold-start clarity |
| One-Person Maintenance Team | harsh support/maintenance constraint |
| Security Paranoiac | threat and abuse awareness |
| Bad-Faith User | adversarial misuse modelling |
| Regulator/Auditor | formal external review |
| Plain-Language Translator | expert-to-novice explanation |
| Old Hand Who Has Seen This Fail Before | field wisdom and failure memory |

Create dossiers for these only when relevant to a project.

## Examples

| User asks | Mode | Correct behaviour |
|---|---|---|
| “activating expert mode on this project” | Auto-selected panel | Inspect project, pick 3-10 archetypes, create/update roster and useful dossiers, load 0-3 dossiers, answer. |
| “Generate a custom expert: prompt engineering expert” | Custom expert request | Create/update only that dossier, add it to roster, load it if advice is requested. |
| “Bring in a relationship/CX expert and a famous expert track” | Custom + prominent expert | Create relationship advisor dossier, add a small factual prominent expert section, advise on expert-client behaviour. |
| “Review this README for clarity” | Lightweight panel | Use 1-2 lenses, e.g. technical editor + confused first-time user; do not create a large panel. |
| “Design a customer data retention policy” | High-risk panel | Include privacy/compliance/security/operations lenses and state human-review boundaries. |

## Extra references

This SKILL.md is intentionally inline for ClawHub readability. Detailed optional references are bundled for deeper work:

- `references/archetype-buckets.md`
- `references/beta-example-archetypes.md`
- `references/custom-expert-request-mode.md`
- `references/prominent-expert-track.md`
- `references/response-depth-modes.md`
- `references/retrieval-policy.md`
- `references/top-notch-expert-behaviour.md`
- `references/dossier-schema.md`
- `references/examples.md`
