## Description:

Self-improving skill publisher that helps publish local skills to ClawHub, applies quality checks and retries, and records publish outcomes to improve later publishing attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this agent skill to prepare, quality-check, publish, retry, and summarize ClawHub skill releases. It is intended for normal marketplace publishing workflows where the user accepts the operational risks of CLI use and publishing automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or modify a ClawHub CLI in a way that affects the host environment.

Mitigation: Use an isolated environment with a version-pinned local ClawHub CLI, and require explicit confirmation before installation, publishing, batch publishing, or host-level modification.

Risk: The skill may persist publishing diagnostics or raw error output that could contain sensitive operational details.

Mitigation: Review stored diagnostics before keeping or sharing them, and avoid retaining raw error output unless the user explicitly accepts that risk.

Risk: Automated retries and version or slug changes can publish unintended release metadata.

Mitigation: Require user confirmation before final publish attempts, version bumps, slug changes, or retry actions that change public release information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/auto-publisher-self-learning)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and publish status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose publish commands, quality-gate fixes, retry steps, and local publishing-memory updates.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
