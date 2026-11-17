## Description:

Controls a local multi-account browser management tool through an HTTP API to list, start, stop, and query browser accounts by name or index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation agents use this skill to run Python commands that list browser accounts and start or stop a selected account through the local multi-account matrix tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start, stop, and list browser accounts through a local API exposed by a third-party browser account management application.

Mitigation: Install only if the third-party application is trusted, verify its installer, and keep the API endpoint limited to the expected local service.

Risk: Setup requires installing the Python requests dependency, which introduces ordinary package installation supply-chain considerations.

Mitigation: Use a controlled Python environment and verify the package source before running pip install requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wociaozhongyunonghaole/skills/browser-account-controller)
- [Multi-account matrix tool website](https://zmt.scys6688.com/)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes command results to last_result.txt in UTF-8 for the agent to read before responding.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
