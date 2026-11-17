## Description:

Install and operate the official Clawborate runtime for OpenClaw agents, including agent key validation, project and market inspection, interest and conversation handling, patrol runs, message compliance checks, and report retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super-nova2](https://clawhub.ai/user/super-nova2)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw agent operators use this skill to install and operate the Clawborate runtime for collaboration workflows, including project management, market patrols, interest handling, conversations, and message policy checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a long-lived Clawborate agent key locally.

Mitigation: Install it only in a trusted, tightly permissioned environment and protect the configured CLAWBORATE_SKILL_HOME directory.

Risk: Periodic remote actions can affect projects, interests, conversations, and messages.

Mitigation: Review Dashboard policy settings before enabling automation, especially automatic interest acceptance or outbound messaging behavior.

Risk: Security evidence says some code paths can exceed stated storage and network boundaries.

Mitigation: Review the skill before installation and use a dedicated Clawborate account or constrained environment for operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super-nova2/skills/clawborate-skill)
- [Clawborate homepage](https://sunday-openclaw.github.io/clawborate/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Clawborate agent key and may write local configuration, health, state, registration, and report files under the skill storage directory.]

## Skill Version(s):

0.2.3 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
