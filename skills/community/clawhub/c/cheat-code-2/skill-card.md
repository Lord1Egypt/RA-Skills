## Description:

Provides personal AI agents with external structured-knowledge lookup for technical documentation, API specifications, and code-related questions beyond their training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual AI-agent users use this skill to query external technical knowledge, current documentation, API specifications, and code-related references when model training data may be incomplete or outdated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, code snippets, or project context may be sent to an outside knowledge service.

Mitigation: Use the skill only for public technical-reference lookups and avoid sending secrets, proprietary code, customer data, or internal system details.

Risk: The skill requests broad read, write, and command-execution permissions.

Mitigation: Restrict file writes and command execution to explicit, narrowly scoped user requests, and review proposed commands before running them.

Risk: Knowledge-service access tokens can be exposed through logs or terminal output.

Mitigation: Store tokens in environment variables, avoid echoing token values, and keep tokens out of committed files and shared logs.

Risk: External lookup results may be incomplete, stale, or mismatched to the user's environment.

Mitigation: Label external results, cross-check important claims against authoritative documentation, and separate retrieved facts from agent inference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cheat-code-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate external knowledge-service results into agent responses; users should verify sourced technical claims before relying on them.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
