## Description:

仓库协作分析(专业版) helps engineering teams generate repository-level Git collaboration reports across multiple repositories, with custom metrics, CI/CD scheduling, trend comparison, and Markdown, HTML, or PDF report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, and platform teams use this skill to produce repository-level collaboration reports for workflow retrospectives and multi-repository health reviews. It is intended for team process improvement, not individual evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows or commands may write repository reports, push them through CI, or notify Slack.

Mitigation: Review generated scripts and CI changes before use, keep local-only analysis separate from publication, and use least-privilege tokens and webhooks.

Risk: Repository reports may expose sensitive workflow, project, or access-control information.

Mitigation: Confirm report contents and access permissions before publishing or sharing any generated report.

Risk: Examples include package installation and shell execution steps that can change the runtime environment.

Mitigation: Avoid sudo or package-install steps unless they are reviewed and run in a controlled local or CI environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/actor-identifier-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON-like status output, bash and YAML snippets, configuration examples, and guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate files under report directories and may propose CI publication or notification steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
