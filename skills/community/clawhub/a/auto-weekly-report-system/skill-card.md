## Description:

Automates weekly report collection, Markdown report generation, and Enterprise WeChat document publishing for v3.5, InStreet, price monitoring, and system health data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to collect project metrics, generate weekly Markdown reports, and prepare Enterprise WeChat publication commands. It is suited for recurring team status reporting and data synchronization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated report content and publication commands may be published to Enterprise WeChat before review.

Mitigation: Review the generated report before publication and keep scheduled publishing disabled until the workflow has an explicit review gate.

Risk: Predictable temporary shell scripts and unescaped titles or data can make local execution unsafe with untrusted inputs.

Mitigation: Run only in a trusted local environment, validate titles and source data, use private output directories, and do not run generated temporary scripts from untrusted inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rf-ai-wh/skills/auto-weekly-report-system)
- [README](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON data files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated data, reports, and publication command scripts to local temporary paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
