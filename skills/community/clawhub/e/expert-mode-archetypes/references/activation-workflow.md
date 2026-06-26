# Expert Mode Activation Workflow v0.1.0-scaffold

## Trigger

The main trigger phrase is:

> activating expert mode

Also use this workflow when the user clearly asks to gather expert perspectives, build a panel of experts, consult a professional lens, or create expert dossiers for a project.

## Step A: Understand the current project/task

Read available project files when working inside a managed project:

1. `PROJECT.md`
2. `PLAN.md`
3. `LOG.md` if recent history matters
4. relevant `refs/` or `work/` files

Then produce an internal brief:

- Project name.
- Current goal.
- Current phase.
- Immediate decision or task.
- Known constraints.
- Known risks.
- Desired output.

## Step B: Decide whether expert mode should be light or full

Use light mode when:

- The task is narrow.
- A single expert lens is enough.
- The user wants speed.
- The project is low-risk.

Use full mode when:

- The task spans multiple domains.
- The project is in early design.
- Mistakes could be expensive.
- There are legal, safety, medical, financial, security, privacy, accessibility, or operational risks.
- The user explicitly asks for up to 10 experts.

## Step C: Select experts

Choose up to 10 expert archetypes.

For each candidate, write:

- Expert title.
- Why relevant now.
- What they would inspect.
- Whether they are lead, supporting, or reviewer.
- Whether a dossier already exists.

Prefer a balanced panel:

- 1 lead domain expert.
- 1 implementation expert.
- 1 user/customer expert if people interact with the output.
- 1 risk/compliance/security expert if high-stakes.
- 1 operations/maintenance expert if the thing will run over time.
- 1 communication/documentation expert if adoption matters.

## Step D: Consult or create roster

Suggested `experts/roster.md` format:

```markdown
# Expert Roster

Project: <project>
Updated: <date>

| Slug | Expert | Status | Load when | Dossier |
|---|---|---|---|---|
| software-architect | Software Architect | active | architecture and boundaries | dossiers/software-architect.md |
```

If no roster exists and writing files is appropriate, create it. If writing files would be surprising, ask first.

## Step E: Open dossiers

For each expert needed now or likely to recur:

1. Create a slug.
2. Create a dossier from the schema.
3. Fill it with project-specific expert behaviour.
4. Add retrieval rules.
5. Add source guidance.
6. Update the roster.

## Step F: Load minimal context

Before answering, decide which dossier(s) are truly needed.

Patterns:

- One expert: focused implementation or review.
- Two experts: decision with tradeoff, e.g. product + engineering.
- Three experts: lead + user lens + risk lens.
- More than three: planning/review summary only, not all details.

If many experts are relevant, summarize the panel instead of loading every dossier fully.

## Step G: Answer using expert synthesis

Structure options:

### Fast synthesis

```markdown
Expert mode: I’d use <expert A>, <expert B>, and <expert C> here.

Recommendation: <short answer>
Why: <expert-informed reasons>
Watchouts: <risks>
Next step: <action>
```

### Review panel

```markdown
Expert mode panel:
- <Expert A>: <main concern>
- <Expert B>: <main concern>
- <Expert C>: <main concern>

Consensus:
<shared recommendation>

Disagreement:
<important tradeoff, if any>
```

### Dossier creation report

```markdown
Created/updated expert dossiers:
- <expert>: <path>
- <expert>: <path>

Loaded now:
- <expert>: <reason>

Not loaded:
- <expert>: <reason>
```

## Step H: Maintain over time

When a dossier becomes stale:

- Update it instead of creating a duplicate.
- Mark superseded dossiers.
- Move unused experts to archived.
- Compress verbose sections after repeated use.
