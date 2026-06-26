## Description: <br>
Helps configure an agent to act proactively through persistent memory, write-ahead logging, onboarding, heartbeat checks, security hardening, and guarded autonomous workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up proactive agent behavior, including onboarding users, preserving memory across context loss, running periodic heartbeat checks, and proposing useful work while gating external actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent proactive behavior can broaden agent authority over memory, cleanup, account checks, and background work. <br>
Mitigation: Require explicit opt-in before enabling persistence or background jobs, keep stop controls visible, and review memory and rule-file edits. <br>
Risk: Sensitive credentials or personal data may be exposed through account integrations or workspace memory. <br>
Mitigation: Limit accessible folders and tools, keep credentials out of memory files and logs, and approve email, calendar, or account access case by case. <br>
Risk: Heartbeat cleanup or autonomous cron actions can alter local state without adequate user control. <br>
Mitigation: Disable or require confirmation for cleanup, deletion, sending, posting, and other external or irreversible actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chaoliuzhu/delonix-proactive-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/chaoliuzhu) <br>
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md) <br>
- [Security Patterns Reference](artifact/references/security-patterns.md) <br>
- [Creator Profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and starter configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes starter files and a security audit script; outputs should be reviewed before enabling persistent memory, background jobs, or external account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
