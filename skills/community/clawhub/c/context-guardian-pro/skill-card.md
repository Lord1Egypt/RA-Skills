## Description: <br>
Automates context monitoring by summarizing history, saving to long-term memory, and sending QQ alerts when session message or token limits approach a configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artwebs](https://clawhub.ai/user/artwebs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor context pressure during long sessions and trigger backup, memory persistence, and notification actions before the session exceeds its context limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to run automatically, write to long-term memory, and may claim a backup was made even when only a placeholder summary was written. <br>
Mitigation: Install only after reviewing automatic scheduling, memory-write behavior, and backup claims; require review-before-save behavior before relying on it for context backup. <br>
Risk: Notification behavior may involve QQ transmission in future versions. <br>
Mitigation: Require clear disclosure and opt-in controls before enabling any external notification channel. <br>
Risk: Persisted session summaries may need retention, deletion, or disable controls. <br>
Mitigation: Ask the publisher to document a disable path and retention or deletion controls before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/artwebs/context-guardian-pro) <br>
- [Publisher profile](https://clawhub.ai/user/artwebs) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Status text and memory notes, with command execution through scheduled taskflow or cron workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports task status and whether summarization and notification actions were taken.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
