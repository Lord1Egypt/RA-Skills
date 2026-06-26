## Description: <br>
Captures learnings, errors, corrections, and feature requests so coding agents can review and promote reusable project knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockcloud](https://clawhub.ai/user/blockcloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture non-obvious failures, user corrections, missing capabilities, and reusable workflow learnings in markdown logs, then promote durable guidance into project or agent memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can store raw errors, user corrections, agent behavior rules, secrets, personal data, customer details, proprietary content, environment details, or full command output. <br>
Mitigation: Require review before writing or promoting learnings, and redact secrets, tokens, personal data, customer details, proprietary content, raw environment data, and full command output before saving or sharing entries. <br>
Risk: Broad or global hook setups can cause the skill to inject reminders across more contexts than intended. <br>
Mitigation: Keep hooks project-scoped and opt-in; avoid global empty-matcher configurations unless the deployment owner has explicitly approved that behavior. <br>
Risk: Unreviewed promoted learnings can introduce incorrect or misleading guidance into project or agent memory files. <br>
Mitigation: Confirm that a learning is accurate, reusable, and appropriate for the target memory file before promotion, and resolve stale or incorrect entries during periodic review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blockcloud/cpppselfimprovingagent123123) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, hook configuration snippets, and optional generated skill files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of .learnings markdown logs, agent memory files, hook settings, and relative-path skill scaffolds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
