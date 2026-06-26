## Description: <br>
Automates a daily ClawHub skill update routine with before-and-after version comparison and Feishu or Telegram update reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dillardarchie](https://clawhub.ai/user/dillardarchie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage ClawHub installations use this skill to configure a scheduled Gateway Cron job that updates installed skills and reports version changes. It is intended for environments that intentionally allow unattended daily skill updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change installed skills without a manual review step. <br>
Mitigation: Use this only where automatic updates are intended; prefer pinning or allowlisting trusted skills, review updates before wider rollout when possible, and keep rollback instructions available. <br>
Risk: Update summaries may be sent to external Feishu or Telegram recipients. <br>
Mitigation: Send reports only to private, approved recipients and avoid routing operational update details to public or untrusted channels. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command snippets and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron schedule, timezone, notification channel, manual test commands, and update-report examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
