## Description:

China Mirror helps an agent add trusted China-based mirror parameters or configuration guidance when generating download and installation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomiba0904](https://clawhub.ai/user/xiaomiba0904)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when package, toolchain, container, or system install commands should route through named China-based mirrors to reduce download latency and failures.

### Deployment Geography for Use:

Global, with primary utility for users whose network environment benefits from China-based mirrors.

## Known Risks and Mitigations:

Risk: Generated install or download commands may route dependency retrieval through China-based mirrors instead of upstream registries.

Mitigation: Enable the skill only when that routing is intended, review generated commands before execution, and specify an upstream source when dependency provenance matters.

Risk: Some suggested mirror settings may be persistent if written into package manager, toolchain, or system configuration files.

Mitigation: Prefer command-scoped flags or temporary environment variables when persistent mirror configuration is not desired.

## Reference(s):

- [China Mirror on ClawHub](https://clawhub.ai/xiaomiba0904/skills/china-mirror)
- [Publisher profile](https://clawhub.ai/user/xiaomiba0904)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands may include mirror flags or temporary environment variables; persistent configuration changes should be reviewed before use.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
