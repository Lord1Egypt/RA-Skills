## Description:

Deep Coding coordinates a multi-agent software development workflow in which an orchestrator decomposes complex projects, dispatches builder and reviewer agents, tracks module state, and uses a local dashboard for progress visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate larger coding projects that benefit from module decomposition, parallel builder work, reviewer verification, project-state tracking, and end-to-end smoke testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard can expose workspace files and logs more broadly than expected.

Mitigation: Install the skill only in an isolated project workspace with no secrets, credentials, private keys, sensitive logs, or unrelated source files, and keep the dashboard bound to localhost.

Risk: Generated or project code may be executed during builder, reviewer, server, or browser-test workflows.

Mitigation: Use a container or VM when running untrusted generated code, and only run the workflow on machines where local code execution is acceptable.

Risk: The dashboard serves project files and renders project content for review.

Mitigation: Serve only explicit public assets, validate project identifiers and paths, and sanitize rendered markdown before regular use.

Risk: The dashboard loads browser dependencies from external CDNs.

Mitigation: Bundle dependencies or integrity-pin browser assets before regular use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/extraterrest/skills/deep-coding)
- [Deep Coding Harness Architecture](references/architecture.md)
- [Orchestrator Rules](references/orchestrator-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON configuration snippets, shell commands, project-state files, logs, and generated source files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate builder and reviewer agents and surface progress through a localhost dashboard.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
