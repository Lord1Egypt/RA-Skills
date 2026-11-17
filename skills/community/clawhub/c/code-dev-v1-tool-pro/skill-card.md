## Description:

结构化开发工具专业版 helps engineering teams plan versioned development work, coordinate releases, define team standards, and produce delivery audit guidance in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure multi-task software delivery, release management, quality gates, changelog generation, and audit reporting for versioned projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide file writes, shell commands, API calls, callbacks, tags, changelog changes, and release or deployment actions without clear user gating.

Mitigation: Require explicit confirmation before writes, shell commands, network or API calls, callback configuration, version tagging, changelog edits, and any staging or production release action.

Risk: Broad development and release guidance could expose credentials or apply changes to the wrong environment.

Mitigation: Use least-privilege credentials from environment variables, redact secrets from outputs, prefer dry runs or staging first, and review generated commands and configuration before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-dev-v1-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed file changes, release checklists, audit records, and commands for review before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
