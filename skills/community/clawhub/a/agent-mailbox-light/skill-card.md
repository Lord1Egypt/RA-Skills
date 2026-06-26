## Description: <br>
Lightweight cross-agent mailbox using per-workspace file inboxes with best-effort fanout and local read/archive flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmeng6666](https://clawhub.ai/user/yangmeng6666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to share short, local coordination notes across OpenClaw workspaces without chat fanout, cloud sync, or guaranteed delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox fanout can write notes into unintended local workspaces if MAILBOX_GLOB is broad. <br>
Mitigation: Keep MAILBOX_GLOB narrow and use this only in trusted local workspaces. <br>
Risk: Mailbox messages may contain sensitive or untrusted content. <br>
Mitigation: Do not put secrets in mailbox messages, and treat mailbox contents as hints that require agent judgment. <br>
Risk: Users may mistake mailbox delivery for reliable task dispatch. <br>
Mitigation: Use the mailbox for advisory context only; do not rely on it for guaranteed delivery, retries, or automatic execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangmeng6666/agent-mailbox-light) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and local mailbox files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mailbox messages are local advisory Markdown files under .agent-mailbox; delivery is best-effort and should not trigger automatic execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
