## Description:

Error pattern tracking for AI agents. Detects corrections, escalates recurring mistakes, learns mitigations. The 'something's off' detector from the AI Brain series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to detect user corrections or frustration in transcripts, record recurring error patterns, and load concise guidance that helps future sessions avoid repeated mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private transcripts and can send excerpts to configured model CLIs.

Mitigation: Review whether transcript analysis fits your privacy needs and prefer local-only ACC_MODELS where possible.

Risk: The skill stores untrusted error text in persistent memory that future agents may load as guidance.

Mitigation: Review ACC_STATE.md and stored ACC state before loading them into future sessions.

Risk: Scheduled analysis can run automatically when cron setup is enabled.

Mitigation: Avoid --with-cron until you understand the analysis cadence and workspace impact.

Risk: The security guidance identifies a timestamp interpolation issue in update-watermark.sh.

Mitigation: Fix the update-watermark.sh timestamp interpolation issue before using the skill in a shared or untrusted workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/impkind/skills/acc-error-memory)
- [Source repository metadata](https://github.com/ImpKind/acc-error-memory)
- [AI Brain series](https://clawhub.ai/skills?tag=ai-brain)
- [Hippocampus memory skill](https://clawhub.ai/skills/hippocampus)
- [Amygdala memory skill](https://clawhub.ai/skills/amygdala-memory)
- [VTA memory skill](https://clawhub.ai/skills/vta-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, JSON state files, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent memory files in the OpenClaw workspace and may use configured model CLIs for transcript screening.]

## Skill Version(s):

1.0.0 (source: release evidence, OpenClaw metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
