# Custom Expert Request Mode v0.4.0-draft

Use this mode when the user asks for a specific expert/archetype instead of asking Expert Mode to auto-select a panel.

## Trigger patterns

Custom Expert Request Mode activates when the user says or implies:

- “generate a custom expert: <expert>”
- “add a <expert> expert”
- “use a <expert> to advise on this project”
- “create an archetype for <expert/lens>”
- “I want a custom expert who…”
- “bring in a <role/lens/stakeholder>”

Example:

> Can you generate a custom expert — a prompt engineering expert — to then advise on the project?

## Core behaviour

When the user requests a custom expert:

1. Treat the requested expert as the primary archetype.
2. Do not auto-generate a broad 10-expert panel unless the user also asks for one.
3. Check the roster for an existing matching archetype.
4. Create or update the dossier.
5. Add the dossier to the roster.
6. Load that dossier immediately if the user asked it to advise now.
7. Ask the custom expert to produce project-specific advice.
8. Add or update skill docs if the custom expert implies a reusable mode or pattern.

## Custom expert intake fields

Infer what you can. Ask only if the missing detail blocks useful creation.

Useful fields:

- Requested title.
- Project/task the expert should advise on.
- Why the expert is being requested.
- Primary archetype bucket.
- Secondary buckets.
- Whether to create a full dossier or compact dossier.
- Whether the expert should advise immediately.
- Any boundaries, e.g. “do not make this legal advice”.

## Naming

Use a clear lowercase slug:

```text
prompt-engineering-expert
retail-operations-specialist
hostile-user-red-teamer
plain-language-editor
```

Avoid fake personal names unless the user explicitly provides a real profile.

## Dossier depth

Default to a full dossier when:

- The expert will advise the project repeatedly.
- The expert affects skill mechanics or project direction.
- The user explicitly asks to generate a custom expert.

Use a compact dossier when:

- The request is one-off.
- The project is small.
- The expert is narrow and unlikely to recur.

## Immediate advice pattern

After creating or updating the custom expert, provide advice in this shape:

```markdown
Created custom expert:
- <Expert title>: <dossier path>

Loaded now:
- <Expert title>: <why>

<Expert title> advice:
1. <point>
2. <point>
3. <point>

Recommended project changes:
- <file/change>
```

Keep it concise unless the user asks for a full report.

## Safety rules

- Do not fabricate credentials or biographical details.
- Treat the custom expert as an archetype/lens.
- For high-stakes custom experts, include a human review boundary.
- For adversarial custom experts, focus on testing and prevention, not operational harm.

## Interaction with auto-selection

Custom Expert Request Mode short-circuits broad panel selection.

Good:

- User asks for Prompt Engineering Expert.
- Agent creates/loads Prompt Engineering Expert.
- Agent may mention 1-2 adjacent experts only if useful.

Bad:

- User asks for one expert.
- Agent creates 10 experts and buries the requested one.

## Completion criteria

A custom expert request is complete when:

- The roster has the expert entry.
- The dossier exists or was updated.
- The expert has advised if requested.
- Relevant reusable mode/pattern docs are updated if the request revealed a missing skill behaviour.
