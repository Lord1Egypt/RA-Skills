## Description: <br>
Set up OpenClaw multi-provider authentication with OpenAI Codex OAuth fallback profiles, profile import, fallback ordering, and optional cooldown-based model switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Markeljan](https://clawhub.ai/user/Markeljan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure multiple Codex OAuth profiles for rate-limit failover, add profile tokens through the Codex device-flow login, and optionally enable local cooldown-based model switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles OAuth access and refresh tokens and writes imported profiles to local OpenClaw auth configuration. <br>
Mitigation: Install only when OpenClaw should reuse Codex OAuth sessions; keep auth-profiles.json and backup files private, out of git and logs, and remove stale backups when no longer needed. <br>
Risk: The optional cron job can switch the active model without manual intervention. <br>
Mitigation: Enable the cron job only when unattended model switching is desired, and review the configured profile order and cooldown behavior before enabling it. <br>


## Reference(s): <br>
- [Config Templates](references/config-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Markeljan/codex-multi-subscription-auth-fallbacks) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local auth-profile setup and optional cron configuration; generated commands and configuration should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
