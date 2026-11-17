## Description:

Autowriter helps an agent draft technical articles, paper explainers, and AI/ML content through a closed loop of source-grounded research, writing, de-AI rewriting, self-evaluation, and iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use Autowriter to turn user-provided papers, project files, notes, or references into technical articles with iterative self-evaluation and draft logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies an opinionated first-person, anti-AI writing style that may not fit every publication voice.

Mitigation: Review the final draft against the target publication style before use.

Risk: Generated writing quality depends on the completeness and accuracy of user-provided or workspace source material.

Mitigation: Provide authoritative sources and verify claims, code, and data before publishing.

Risk: The skill can read and write workspace files.

Mitigation: Run it only in workspaces that contain material appropriate for the writing task.

## Reference(s):

- [autoresearch Design Philosophy Deep Dive](references/autoresearch-philosophy.md)
- [Karpathy Code Style to Writing Style](references/karpathy-code-style.md)
- [Autowriter on ClawHub](https://clawhub.ai/lifei68801/skills/autowriter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown articles, research fact checklists, self-evaluation tables, and draft log summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided or workspace source material; the declared behavior has no network, telemetry, or credential use.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
