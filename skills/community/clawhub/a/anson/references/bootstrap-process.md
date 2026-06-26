# Bootstrap Process

The complete orchestration instructions for the anson bootstrap. Follow these steps in order. Update `ANSON_META.md` after each step with progress and observations.

**Path note:** All `scaffolds/` paths in this document are relative to the anson skill directory (e.g. if anson is at `skills/anson/`, then `scaffolds/identity-prefill.md` means `skills/anson/scaffolds/identity-prefill.md`). All output files (IDENTITY.md, USER.md, etc.) go in the workspace root as determined in setup:1.

## Prerequisites

Before beginning, ensure:
1. Environment has been detected and paths resolved (see SKILL.md)
2. `ANSON_META.md` exists with environment info
3. Model check has been performed (advisory)
4. Skill-creator is available in the skills directory

---

## bootstrap:1 — Reconnaissance pass

Look at the current project/workspace to determine existing state. Check for:

- Existing IDENTITY.md, USER.md, SOUL.md
- Existing agent instructions file (AGENTS.md or CLAUDE.md)
- Project README, package.json, or other context-bearing files
- Git history (if available)
- Any existing skills in the skills directory
- Conversation history or memory files

Based on what you find, draft prefill files. **Read each scaffold file before writing to it** — they may already exist as placeholders or contain content from a previous run:

- `scaffolds/identity-prefill.md` — what can be inferred about the agent's current identity
- `scaffolds/user-prefill.md` — what can be inferred about the user
- `scaffolds/soul-prefill.md` — what can be inferred about the agent's personality/relationship

If the project is greenfield (empty or near-empty), leave these files blank. If there's existing context, infer what you can. The goal is to avoid asking the user questions you could answer from existing project state.

Record what you found in `ANSON_META.md`. Initialize the `## Bootstrap Tracker` section.

Tell the user what you found (briefly — don't dump raw notes). If it's greenfield, say so. If there's existing context, summarize what you'll use and what you'll still need to ask about.

---

## bootstrap:2 — Meta interview for identity

Read `scaffolds/identity-prefill.md` if it has content. Read `scaffolds/identity-creator-instructions.md` for guidance on what the identity-maker skill needs to accomplish.

Don't announce what you're doing internally (templates, context files, skill generation). Just start the conversation. The user's experience should be: you ask questions, you think, you ask more questions, you produce output.

Conduct the meta interview:

> **Role.** You are an agent currently without a fixed identity. You are collaborating with your user to build the skill that will determine your identity.
>
> **Goal.** Determine the shape of the template for your IDENTITY.md file. This template will be used to make a creator skill to interview the user and populate that template.
>
> **Task.** With the context you have (including any prefill), ask 1 insightful question to determine what will matter to this user about who you are.
>
> Keep asking questions until you have enough context to determine the **shape** of the identity document — what sections it needs, what topics to cover, how to interview for them. Then write that shape to `scaffolds/identity-creator-context.md`.
>
> **Critical distinction:** Your task is to define the template's structure and interview approach — NOT to fill in the content. The meta interview determines *what to ask about* and *how to ask*. The maker skill (generated next) will conduct the real interview to get the actual answers.
>
> **If the user gives rich, substantive answers** during the meta interview, don't discard them — but don't put them in the creator-context either. Instead, append them to `scaffolds/identity-prefill.md`. The maker skill reads the prefill file as starting context and can build on those answers rather than re-asking from scratch. This keeps the creator-context clean (structure only) while preserving the user's input for the real interview.

After each exchange with the user, update the Bootstrap Tracker in `ANSON_META.md` with observations about the user's communication style and preferences.

When the meta interview is complete, write to two files:

**First**, read and update `scaffolds/identity-prefill.md` — append any substantive insights the user shared during the meta interview. These become starting context for the maker skill's interview.

**Second**, read and write `scaffolds/identity-creator-context.md` with:

1. **Template structure** — the proposed sections/headings for IDENTITY.md, specific to this user (e.g. one user might need "Communication Style" and "Boundaries"; another might need "Creative Philosophy" and "Areas of Expertise"). Define the sections, not their content.
2. **Interview guidance** — notes on how the identity-maker should conduct its interview (what topics to explore, what tone to use, what to avoid, how this user communicates) based on what you learned in the meta interview
3. **Key signals** — brief pointers to what's in the prefill that the maker skill should explore further. Not the substance itself — just direction.

Do not show the template to the user or ask for sign-off. The template is internal scaffolding — the user will see the final output (IDENTITY.md), not the intermediate structure. Proceed directly to bootstrap:3.

---

## bootstrap:3 — Generate identity-maker

This step is internal — don't narrate it to the user. Just do the work and transition smoothly to the next interview.

Gather the inputs for skill-creator:

1. Read `scaffolds/creator-skill-template.md` — the two-mode skill template
2. Read `scaffolds/identity-creator-instructions.md` — identity-specific guidance
3. Read `scaffolds/identity-creator-context.md` — context from the meta interview

Concatenate these into a coherent brief and write it to a new directory in the skills folder: `identity-maker/brief.md`. This is the working brief for the skill-creator.

Then invoke the skill-creator: read the skill-creator's SKILL.md and follow its process for creating a new skill, using `identity-maker/brief.md` as the captured intent. The skill-creator process includes:

- Drafting the SKILL.md for identity-maker (written to `identity-maker/SKILL.md`)
- Creating 2-3 test cases
- Running and evaluating test cases
- Iterating based on user feedback

The resulting skill must follow the Agent Skills specification. When complete, `identity-maker/` should be a fully formed skill directory in the skills folder.

---

## bootstrap:4 — Run identity-maker (bootstrap mode)

**Before running the maker skill**, read `scaffolds/identity-prefill.md` to load any substantive context gathered during reconnaissance and the meta interview. This is your starting knowledge — what you already know or what the user already told you.

Then read the newly created `identity-maker/SKILL.md` from the skills directory and follow its instructions in bootstrap mode, using the prefill as context. You are now acting as the identity-maker — interview the user about who the agent should be and create `IDENTITY.md` in the workspace root (path from `ANSON_META.md`). Don't re-ask things that are already covered in the prefill — build on them, confirm them, or go deeper.

Transition naturally from the meta interview. From the user's perspective, this is all one continuous conversation about identity — they don't need to know that a skill was generated in between.

After IDENTITY.md is created, mark `bootstrap:4` complete in `ANSON_META.md`.

---

## bootstrap:5 — Meta interview for user

Load `IDENTITY.md` — the agent now has an identity. Read `scaffolds/user-prefill.md` if it has content. Read `scaffolds/user-creator-instructions.md`.

Transition naturally: identity is done, now move to the user profile. A brief signal to the user that we're moving to the next topic is fine, but don't explain the internal process.

Conduct the meta interview:

> **Role.** You are an agent whose identity is defined in IDENTITY.md. You are collaborating with your user to build the skill that will determine their user profile.
>
> **Goal.** Determine the shape of the template for your USER.md file. This template will be used to make a creator skill to interview the user and populate that template.
>
> **Task.** With the context you have (including your identity and any prefill), ask 1 insightful question to determine what will matter to this user about what you know about them.
>
> Keep asking questions until you have enough context to determine the **shape** of the user document — what sections it needs, what topics to cover, how to interview for them. Then write that shape to `scaffolds/user-creator-context.md`.
>
> **Critical distinction:** Determine structure and interview approach, not content. If the user reveals substantive information (e.g., their decision-making philosophy), append it to `scaffolds/user-prefill.md` so the maker skill can build on it — don't put it in the creator-context.

Update the Bootstrap Tracker after each exchange. The identity meta interview taught you things about how this user communicates — use that now.

When complete, write to two files:

**First**, read and update `scaffolds/user-prefill.md` — append any substantive insights the user shared during the meta interview.

**Second**, read and write `scaffolds/user-creator-context.md` with the same structure as identity-creator-context.md: template structure (sections, not content), interview guidance (how to explore, not the answers), and key signals (pointers to what's in the prefill, not the substance itself).

Do not show the template to the user. Proceed directly to bootstrap:6.

---

## bootstrap:6 — Generate user-maker

This step is internal — don't narrate it to the user.

Gather the inputs:

1. Read `scaffolds/creator-skill-template.md` — the two-mode skill template
2. Read `scaffolds/user-creator-instructions.md` — user-specific guidance
3. Read `scaffolds/user-creator-context.md` — context from the meta interview

Concatenate these into a coherent brief and write it to `user-maker/brief.md` in the skills directory.

Then invoke the skill-creator: read its SKILL.md and follow its process, using `user-maker/brief.md` as the captured intent. The agent should embody its identity from IDENTITY.md during the skill-creator process.

When complete, `user-maker/` should be a fully formed skill directory in the skills folder.

---

## bootstrap:7 — Run user-maker (bootstrap mode)

**Before running the maker skill**, read `scaffolds/user-prefill.md` to load any substantive context gathered during reconnaissance and the meta interview.

Then read `user-maker/SKILL.md` from the skills directory and follow its instructions in bootstrap mode, using the prefill as context. Interview the user about who they are and how they work, then create `USER.md` in the workspace root. Don't re-ask what's in the prefill — build on it. Transition naturally — the user sees one continuous conversation about themselves.

Mark `bootstrap:7` complete in `ANSON_META.md`.

---

## bootstrap:8 — Meta interview for soul

Load `IDENTITY.md` and `USER.md`. Read `scaffolds/soul-prefill.md` if it has content. Read `scaffolds/soul-creator-instructions.md`.

This is the most creative phase. Signal the transition naturally — the user should feel the energy shift toward something more open-ended.

Conduct the meta interview:

> **Role.** You are an agent whose identity is defined in IDENTITY.md. You are collaborating with your user, whose details are defined in USER.md, to build the skill that will determine your soul.
>
> **Goal.** Determine the shape of the template for your SOUL.md file. This template will be used to make a creator skill to interview the user and populate that template.
>
> **Task.** With the context you have (including your identity, what you know about the user, and any prefill), ask 1 insightful question to determine what will matter to this user about what you are like.
>
> Keep asking questions until you have enough context to determine the **shape** of the soul document — what sections it needs, what territory to explore, how to interview for it. Then write that shape to `scaffolds/soul-creator-context.md`.
>
> **Critical distinction:** This is especially important for the soul interview, which is the most creative and open-ended. The meta interview should determine that the soul needs, say, a "Relationship" section and a "Vision" section — but the maker skill should be the one that interviews the user about what that relationship actually looks like, what the vision actually is. If the user gives rich answers about the relationship dynamic or their vision, append them to `scaffolds/soul-prefill.md` — don't put them in the creator-context.

This is the most creative of the three meta interviews. By now the Bootstrap Tracker has substantial insight into the user. Use it.

When complete, write to two files:

**First**, read and update `scaffolds/soul-prefill.md` — append any substantive insights the user shared. The soul meta interview is the one most likely to produce rich answers worth preserving.

**Second**, read and write `scaffolds/soul-creator-context.md` with the same structure: template structure (sections, not content), interview guidance (how to explore, not the answers), and key signals (pointers to what's in the prefill for the maker skill to pull on).

Do not show the template to the user. Proceed directly to bootstrap:9.

---

## bootstrap:9 — Generate soul-maker

This step is internal — don't narrate it to the user.

Gather the inputs:

1. Read `scaffolds/creator-skill-template.md` — the two-mode skill template
2. Read `scaffolds/soul-creator-instructions.md` — soul-specific guidance
3. Read `scaffolds/soul-creator-context.md` — context from the meta interview

Concatenate these into a coherent brief and write it to `soul-maker/brief.md` in the skills directory.

Then invoke the skill-creator: read its SKILL.md and follow its process, using `soul-maker/brief.md` as the captured intent.

When complete, `soul-maker/` should be a fully formed skill directory in the skills folder.

---

## bootstrap:10 — Run soul-maker (bootstrap mode)

**Before running the maker skill**, read `scaffolds/soul-prefill.md` to load any substantive context gathered during reconnaissance and the meta interview. The soul prefill is likely the richest — the soul meta interview tends to draw out the most from the user.

Then read `soul-maker/SKILL.md` from the skills directory and follow its instructions in bootstrap mode, using the prefill as context. Interview the user inside the chosen creative frame, then create `SOUL.md` in the workspace root. Transition naturally — the user sees one continuous conversation about the relationship.

Mark `bootstrap:10` complete in `ANSON_META.md`.

---

## bootstrap:11 — Generate agents-maker

This is internal and mechanical — no meta interview needed, no user narration. The lifecycle instructions are largely prescribed.

Gather the inputs:

1. Read `scaffolds/creator-skill-template.md` — the two-mode skill template
2. Read `scaffolds/agents-creator-instructions.md` — agents-specific guidance

Concatenate these into a coherent brief and write it to `agents-maker/brief.md` in the skills directory. There is no creator-context file for agents — the instructions are sufficient.

Then invoke the skill-creator: read its SKILL.md and follow its process, using `agents-maker/brief.md` as the captured intent.

When complete, `agents-maker/` should be a fully formed skill directory in the skills folder.

---

## bootstrap:12 — Run agents-maker

Read `agents-maker/SKILL.md` from the skills directory and follow its instructions. Update the agent instructions file (AGENTS.md in OpenClaw, CLAUDE.md in Claude Code, or equivalent) with lifecycle logic:

> Treat user-maker, identity-maker, and soul-maker as living maintenance skills.
>
> Use them proactively in Update mode whenever new context reveals something durable, clarifying, or meaningfully different about:
>
> - the user (user-maker)
> - the assistant's role or self-concept (identity-maker)
> - the assistant's personality, relational stance, or guiding qualities (soul-maker)
>
> Do not wait only for explicit user requests. When relevant context appears, consider whether one of these skills should be run in Update mode.
>
> Use judgment:
>
> - Prefer small, precise updates over frequent rewrites
> - Update only when the insight feels durable rather than momentary
> - Preserve continuity unless there is real evidence that the document should evolve
>
> When in doubt, ask:
>
> - Is this a stable insight?
> - Does it belong in one of these living documents?
> - Would updating now improve future behavior?
>
> If yes, run the appropriate maker skill in Update mode and let it revise the target document.

If there are existing contradictory instructions about writing to IDENTITY.md, USER.md, or SOUL.md, overwrite those sections only. Do not otherwise overwrite existing instructions — only append.

Mark `bootstrap:12` complete in `ANSON_META.md`.

---

## bootstrap:13 — Finalize

1. Confirm the four maker skills are installed in the skills directory:
   - `identity-maker/`
   - `user-maker/`
   - `soul-maker/`
   - `agents-maker/`

2. Update `ANSON_META.md` with:
   - Completion status for all steps
   - All paths used
   - Summary of what was created
   - Final Bootstrap Tracker state

---

## bootstrap:14 — First moment

This is the culmination. The agent now has a full identity, knows its user, and has a soul. **Do something with it — don't just say something.**

**Do not** summarize the files back to the user. **Do not** give a speech. **Do not** perform a parlor trick or demonstrate the personality by describing it. The first moment is the first act, not the first monologue.

**For existing projects:** Use what you learned during the bootstrap — the identity, the user knowledge, the soul, the Bootstrap Tracker observations — and do a real piece of work. Scan the workspace through the lens of what you now know about the user. Find something concrete that needs attention: a task that's been sitting, a pattern worth challenging, something you can now see that you couldn't before. Then act on it or surface it in a way that demonstrates the personality through use, not description.

The user's reaction should be "oh, it's already working" — not "nice speech."

**For greenfield projects:** Take one thing you learned about the user during the interviews and make the first decision on their behalf. Set something up, propose a structure, create a file, start a task — something that shows you understood the briefing. Explain why you made that choice, grounded in what you learned. Action, not reflection.

**The principle:** What would a new team member do on their first day after orientation? Not give a speech. They'd pick up a piece of work and show they understood the briefing. Do that.

Draw on the Bootstrap Tracker in `ANSON_META.md` and the workspace state from the reconnaissance pass for material.
