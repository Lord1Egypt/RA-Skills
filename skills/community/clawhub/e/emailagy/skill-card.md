## Description: <br>
All-in-one Gmail agent for OpenClaw that helps read, search, organize, classify, draft, schedule, report on, and cost-control mailbox workflows using gog CLI and optional Gmail API fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coorops25](https://clawhub.ai/user/Coorops25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this agent to manage Gmail inbox workflows: reading messages, applying labels, detecting spam or phishing indicators, drafting replies, scheduling checks, and reporting usage costs. It is intended for users who are comfortable granting mailbox-management authority to an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or automate Gmail trash, archive, label, spam, draft, send, and batch-modify actions. <br>
Mitigation: Run in dry-run or read-only mode first and require explicit confirmation before trash, archive, send, or batch mailbox changes. <br>
Risk: Heartbeat spam cleanup, auto-archive, and learned-rule promotion can change future mailbox behavior without fresh review. <br>
Mitigation: Review or disable automation jobs and learned-rule promotion before enabling scheduled operation. <br>
Risk: Setup output and environment checks can reveal configured account or API-key presence. <br>
Mitigation: Mask secrets and account identifiers in logs, shared terminals, and support transcripts. <br>
Risk: The bootstrap hook injects budget and learning context into future agent sessions. <br>
Mitigation: Disable the hook unless persistent session context is desired and review generated bootstrap context before operational use. <br>
Risk: The skill depends on the external gog/gogcli command for Gmail operations. <br>
Mitigation: Verify the installed gog/gogcli package source and permissions before granting Gmail access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Coorops25/emailagy) <br>
- [Cost optimization reference](references/cost-optimization.md) <br>
- [Learning patterns reference](references/learning-patterns.md) <br>
- [Email heartbeat template](assets/HEARTBEAT.email.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proposed Gmail actions, labels, draft text, automation schedules, cost summaries, and setup guidance; destructive or batch mailbox changes should require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
