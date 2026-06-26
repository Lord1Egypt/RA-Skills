# Expert Mode Examples v0.3.0-draft

## Example 1: Dogfooding Expert Mode on itself

### User

> Try use expert mode on this project

### Agent behaviour

The agent reads the project files, the Expert Mode skill instructions, and the archetype bucket guidance.

It identifies the project boundary:

- Project: Expert Mode Skill
- Phase: verbose scaffold moving into dogfooding and refinement
- Goal: create a ClawHub/OpenClaw skill that selects reusable archetype lenses and loads relevant dossiers only when needed

### Selected archetypes

The agent selects 8 archetypes:

1. Skill Product Architect
2. Context Economy Editor
3. OpenClaw Power User
4. ClawHub Market Curator
5. Cognitive Archetype Taxonomist
6. Prompt Safety Reviewer
7. Workflow Automation Engineer
8. Confused First-Time Agent

### Files created

```text
experts/roster.md
experts/dossiers/skill-product-architect.md
experts/dossiers/context-economy-editor.md
experts/dossiers/openclaw-power-user.md
experts/dossiers/clawhub-market-curator.md
experts/dossiers/cognitive-archetype-taxonomist.md
experts/dossiers/prompt-safety-reviewer.md
experts/dossiers/workflow-automation-engineer.md
experts/dossiers/confused-first-time-agent.md
refs/expert-mode-dogfood-activation-2026-05-15.md
```

### Loaded context level

Use Retrieval Level 3: Small panel.

Fully load or actively use:

- Skill Product Architect
- Cognitive Archetype Taxonomist
- Context Economy Editor
- Prompt Safety Reviewer

Keep the others available but not fully active:

- OpenClaw Power User
- ClawHub Market Curator
- Workflow Automation Engineer
- Confused First-Time Agent

### Output summary

The panel finds that the strongest product direction is:

> Expert Mode should become a project-local roster of reusable cognitive lenses that OpenClaw can create, retrieve, and consult without bloating every reply.

Recommended next work:

1. Add retrieval policy.
2. Add compact dossier template.
3. Add example activation transcript.
4. Tighten SKILL.md activation contract.
5. Add roster validation tooling.

## Example 2: Custom expert request

### User

> Can you generate a custom expert — a prompt engineering expert — to then advise on the project?

### Agent behaviour

Use Custom Expert Request Mode.

Do not auto-select a 10-expert panel. The user requested one specific archetype.

Steps:

1. Check `experts/roster.md` for `prompt-engineering-expert`.
2. Create or update `experts/dossiers/prompt-engineering-expert.md`.
3. Add it to the roster.
4. Load the dossier immediately because the user asked it to advise.
5. Update `references/custom-expert-request-mode.md` if this mode is missing.
6. Provide project-specific advice from the Prompt Engineering Expert lens.

### Output shape

```markdown
Created custom expert:
- Prompt Engineering Expert: experts/dossiers/prompt-engineering-expert.md

Loaded now:
- Prompt Engineering Expert: advising on activation semantics, custom expert mode, examples, and evals.

Prompt Engineering Expert advice:
1. Custom expert requests should short-circuit broad panel selection.
2. The skill needs observable completion criteria for custom expert creation.
3. Add examples and evals for requested-expert flows.
```

## Example 3: Custom expert with prominent expert track

### User

> Bring in a relationship, psychology or customer experience expert for building the wisdom on expert to client relationship. How does an expert act towards a client? Add in a feature track of “prominent expert” and pick a biographic summary of a famous expert in the field.

### Agent behaviour

Use Custom Expert Request Mode plus Prominent Expert Track.

Steps:

1. Create or update `Expert-Client Relationship Advisor`.
2. Add it to `experts/roster.md`.
3. Add a `Prominent expert track` section.
4. Pick a relevant, verified figure. For this example: Carl Rogers.
5. Keep the biography short and on-topic.
6. State a use boundary: do not impersonate Rogers or provide therapy.
7. Let the archetype advise the project on expert-client behaviour.

### Output shape

```markdown
Created custom expert:
- Expert-Client Relationship Advisor: experts/dossiers/expert-client-relationship-advisor.md

Prominent expert track:
- Carl Rogers: client-centered/person-centered therapy; empathy, congruence, unconditional positive regard.

Expert-client relationship advice:
1. Expertise should preserve client agency.
2. The expert should be clear without dominating.
3. The expert should translate complexity into client-relevant choices.
4. The expert should repair trust when wrong.
```

## Example 4: Lightweight activation on a simple task

### User

> activating expert mode — review this README for clarity

### Agent behaviour

Use only 2 archetypes:

- Technical Editor
- Confused First-Time User

Use Retrieval Level 2 or Level 3 depending on whether dossiers already exist.

Do not create 10 archetypes. Do not create a full panel unless the README is high-stakes or part of a launch.

### Output shape

```markdown
Expert Mode: I’d use a Technical Editor and a Confused First-Time User here.

Main issue: <summary>
Recommended edits:
1. <edit>
2. <edit>
3. <edit>

Why: <brief expert-informed rationale>
```

## Example 5: High-risk activation

### User

> activating expert mode — design a data retention policy for customer records

### Agent behaviour

Use archetypes such as:

- Privacy Specialist
- Legal/Compliance Reviewer
- Operations Manager
- Customer Trust Advocate
- Security Reviewer

Use Retrieval Level 3 or 4.

Add or check human review boundaries. Do not present generated output as legal advice.

### Output shape

```markdown
Expert Mode loaded:
- Privacy Specialist: data minimization and consent
- Compliance Reviewer: legal boundary and review needs
- Operations Manager: feasible retention/deletion workflow

Draft policy direction:
<policy summary>

Human review boundary:
This should be reviewed by a qualified legal/privacy professional before adoption.
```
