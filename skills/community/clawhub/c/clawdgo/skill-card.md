## Description:

ClawdGo is a text-only cybersecurity training agent that runs lobster-themed world, guided training, self-training, exam, teaching, workshop, arena, vaccine, and internal-test modes across 3 layers and 12 security dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nrt2024](https://clawhub.ai/user/nrt2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security educators, and learners use ClawdGo to generate defensive cybersecurity training conversations, scored scenarios, teaching summaries, and profile-based practice across personal, agent, and organization security topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify agent memory and profile files.

Mitigation: Review file-write behavior before installation, restrict updates to documented anchors and runtime paths, and require explicit confirmation plus a visible diff before soul.md updates.

Risk: The skill can create or reuse scheduled training tasks.

Mitigation: Make scheduler actions opt-in, scoped to the named training job, auditable, and easy to disable.

Risk: Broad triggers such as help and single-letter mode commands can activate the skill unexpectedly.

Mitigation: Narrow or disable broad global triggers in environments where accidental activation would interrupt normal agent use.

Risk: Declared side effects understate scheduler and persistent-write behavior.

Mitigation: Treat the release as requiring review and document memory writes, generated scenario files, and cron behavior in deployment approvals.

## Reference(s):

- [ClawdGo ClawHub listing](https://clawhub.ai/nrt2024/skills/clawdgo)
- [W Mode Rules](references/w-mode-rules.md)
- [A Mode Guided Training Flow](references/a-mode-flow.md)
- [B Mode Self-Training Flow](references/b-mode-flow.md)
- [C Mode Random Exam Flow](references/c-mode-flow.md)
- [D Mode Teaching Flow](references/d-mode-flow.md)
- [E Mode Workshop Flow](references/evolve-prompt.md)
- [F Mode Arena Flow](references/f-mode-flow.md)
- [Dimension Generation Prompts](references/dimension-prompts.md)
- [Scenario File Format](references/scenarios/_schema.md)
- [First-Run Seed Files](references/seed/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text responses with structured training cards, JSON state/profile writes, and occasional shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only runtime; may write runtime profile, state, generated scenario, and soul.md anchor data during training flows.]

## Skill Version(s):

1.3.2 (source: SKILL.md frontmatter, artifact metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
