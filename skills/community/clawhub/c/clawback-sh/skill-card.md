## Description: <br>
Clawback helps agents use Gmail through a security proxy with policy enforcement, approval workflows, and audit logging for reading, searching, sending, and managing mail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rotemtam](https://clawhub.ai/user/rotemtam) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Employees and developers use this skill when they want an agent to work with Gmail through Clawback guardrails, including search, message retrieval, send and draft workflows, labels, history, settings, and approval-aware actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox-changing actions such as deletes, draft deletes, label changes, and batch modifications can alter user Gmail data. <br>
Mitigation: Require explicit user confirmation before any delete, draft delete, label change, batch modification, or other mailbox-changing action. <br>
Risk: The skill depends on a locally installed Clawback CLI and the configured Clawback server. <br>
Mitigation: Install only when the user trusts Honeybadge Labs, the clawback binary on PATH, and the configured CB_SERVER value. <br>


## Reference(s): <br>
- [Clawback skill listing](https://clawhub.ai/rotemtam/clawback-sh) <br>
- [Clawback homepage](https://clawback.sh) <br>
- [Clawback releases](https://github.com/honeybadge-labs/clawback/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the clawback CLI and favors JSON, no-input, and fail-empty flags for reliable parsing.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
