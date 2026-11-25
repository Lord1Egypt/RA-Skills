## Description:

Guides agents through diagnosing recurring failures and choosing reusable mechanism-level fixes instead of accumulating isolated patches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longfellow1](https://clawhub.ai/user/longfellow1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use it to diagnose recurring failures in prompts, routing, or system boundaries, choose an appropriate abstraction level for a durable fix, and define an evaluation loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may retrieve changed CLI or skill content when versions are not pinned.

Mitigation: Pin the CLI and skill to reviewed versions, and inspect release changes before installation.

Risk: Security scan coverage was partial; SKILL.md was partly inspected and the binary image was outside the analyzer's scope.

Mitigation: Review the skill files and binary assets for each release before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/longfellow1/skills/deep-fix-principled-simplicity)
- [Source repository (server-resolved provenance)](https://github.com/Longfellow1/Principled-Simplicity-skill)
- [Failure pattern taxonomy](references/patterns.md)
- [Architecture review procedure](references/procedure.md)
- [Abstraction readiness guide](references/abstraction-readiness.md)
- [Prompt decomposition guide](references/prompt-decompose.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text or a structured Markdown repair plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversational diagnosis by default; can provide a structured plan and evaluation checks when requested.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
