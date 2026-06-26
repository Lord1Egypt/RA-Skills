## Description: <br>
Auto Memory helps OpenClaw agents extract session conversations into persistent memory, summarize recent work, and refresh searchable memory indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dtldhjh](https://clawhub.ai/user/dtldhjh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to preserve important session context, maintain long-term memory notes, and make prior work retrievable in later agent runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived content is stored long term and may be reused across agents. <br>
Mitigation: Use the skill only where persistent memory is intended, and inspect or delete stored memory files before using it with sensitive or compartmentalized work. <br>
Risk: Memory content may be sent to a remote model without clear opt-in or remote-summarization disclosure. <br>
Mitigation: Avoid secrets, customer data, regulated data, and proprietary material unless the publisher adds clear opt-in controls, redaction, retention limits, and deletion controls. <br>
Risk: Shared learning files can broaden access to conversation-derived errors or best practices across agents. <br>
Mitigation: Enable shared memory only for agents that are allowed to exchange that context, and review shared learning files regularly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dtldhjh/dtldhjh-auto-memory) <br>
- [Artifact README](README.md) <br>
- [Artifact SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown memory files, console status text, and OpenClaw memory index updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists conversation-derived content under OpenClaw workspace memory and learning paths.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
