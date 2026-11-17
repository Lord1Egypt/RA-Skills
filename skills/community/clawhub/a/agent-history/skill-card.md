## Description:

Searches local AI coding-agent conversation history with the `ochist` CLI so agents can recover prior research, commands, errors, and decisions before repeating work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adlternative](https://clawhub.ai/user/adlternative)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to search and inspect previous local agent sessions before repeating research, debugging, or codebase exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local conversation histories across agents and projects, which may expose secrets, credentials, personal data, or unrelated project content.

Mitigation: Start with project-scoped searches, require explicit approval for global or cross-agent searches, and avoid reprinting sensitive or unrelated content found in past sessions.

Risk: Large session histories can add unnecessary context or reveal more prior conversation detail than needed.

Mitigation: Narrow results first with `sessions`, `grep`, `meta`, and `show`, then read only specific parts and page command output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adlternative/skills/agent-history)
- [Server-Resolved GitHub Provenance](https://github.com/adlternative/agent-historian/tree/main/skills/agent-history)
- [Publisher Profile](https://clawhub.ai/user/adlternative)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local history queries should be scoped and paged to minimize sensitive output and context bloat.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
