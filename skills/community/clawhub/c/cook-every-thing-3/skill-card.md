## Description: <br>
Captures learnings, errors, feature requests, and corrections in structured Markdown files so agents can reuse and promote durable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, feature requests, and reusable patterns during coding sessions. It helps convert recurring lessons into project memory, hook reminders, or new agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs may preserve secrets, credentials, personal data, proprietary code, or raw conversation details. <br>
Mitigation: Redact sensitive material before logging and keep learning files project-local unless they have been reviewed for sharing. <br>
Risk: Global hooks can inject reminders or prompts across sessions where this behavior is not expected. <br>
Mitigation: Prefer project-level setup, avoid global hooks unless needed, and review hook scripts before enabling them. <br>
Risk: Promoted guidance can become durable agent behavior even when a learning was incomplete or context-specific. <br>
Mitigation: Review recurring learnings before promotion and keep promoted rules concise, scoped, and reversible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yequanzheng/cook-every-thing-3) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Entry Examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, hook reminders, and skill scaffold content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning logs, hook configuration, and skill scaffold files when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
