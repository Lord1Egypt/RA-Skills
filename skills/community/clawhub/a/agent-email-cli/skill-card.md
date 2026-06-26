## Description: <br>
Operate the agent-email CLI to create disposable inboxes, poll for new mail, retrieve full message details, and manage local mailbox profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaddy6](https://clawhub.ai/user/zaddy6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create disposable or agent-specific inboxes, poll for incoming email, retrieve message details, and manage local mailbox profiles from a terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email privacy exposure from routing sensitive personal or business messages through disposable or agent-managed inboxes. <br>
Mitigation: Use the skill for disposable or agent-specific inboxes, avoid sensitive mail unless storage and credential handling are understood, and do not print or summarize secret values. <br>
Risk: Supply-chain exposure from installing and running a globally installed npm or bun CLI. <br>
Mitigation: Install only when the publisher is trusted, review the package before use, and verify CLI availability and behavior before relying on it in automation. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zaddy6/agent-email-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON field summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON-native CLI output and avoids repeating secret fields such as passwords or tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
