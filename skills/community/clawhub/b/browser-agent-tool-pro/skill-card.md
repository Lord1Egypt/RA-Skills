## Description:

Guides agents in using a pro browser automation CLI for network interception, request mocking, cookies and storage management, batch scheduling, proxy pools, monitoring, multi-tenant workspaces, and team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and operations teams use this skill to run authorized browser automation workflows for data collection, competitive monitoring, end-to-end testing, and multi-account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad command and file authority for browser automation workflows.

Mitigation: Use it only for explicitly authorized browser automation tasks and avoid unrelated local file or shell operations.

Risk: Browser session state, cookies, saved authentication files, proxy settings, webhooks, and multi-account workflows can expose sensitive data.

Mitigation: Treat those assets as sensitive, restrict sharing or export of session state, and confirm where state is stored and who can access it.

Risk: The underlying browser automation package source affects execution trust.

Mitigation: Prefer a pinned and trusted agent-browser package source before installation or execution.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/thcjp/skills/browser-agent-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, YAML, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences, configuration snippets, structured JSON output examples, and operational cautions for browser session state.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
