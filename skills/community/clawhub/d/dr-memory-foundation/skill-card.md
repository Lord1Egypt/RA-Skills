## Description:

Provides an opinionated, file-based memory layout for OpenClaw-style agents, including dashboards, topic files, a glossary, and an always-on policy and topic catalog for setting up or reorganizing agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize or normalize a local file-based memory layout for OpenClaw-style workspaces while preserving existing notes and creating dashboards, topic files, a glossary, and daily logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated memory files can influence future agent context if inaccurate or stale information is placed in them.

Mitigation: Review MEMORY.md and memory/always_on.md before relying on the structure, and keep stable knowledge in auditable topic files.

Risk: Applying the skill changes the workspace by creating local memory folders, templates, and a daily log.

Mitigation: Install it only in workspaces where a persistent file-based memory structure is intended, and preserve existing notes during normalization.

## Reference(s):

- [Apply checklist](references/APPLY.md)
- [Activation prompt](references/configure_prompt.md)
- [MEMORY.md template](references/templates/MEMORY.md)
- [Always-on policy and topic catalog template](references/templates/memory/always_on.md)
- [Now dashboard template](references/templates/memory/now.md)
- [Open loops template](references/templates/memory/open-loops.md)
- [Automation registry template](references/templates/memory/automation.md)
- [Glossary template](references/templates/memory/topics/glossary.md)
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-memory-foundation)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated workspace memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or preserves local memory templates and an initial daily log when installed.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
