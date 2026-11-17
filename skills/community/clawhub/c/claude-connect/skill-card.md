## Description:

Connect Claude to Clawdbot instantly and keep it connected 24/7 by linking a Claude subscription and refreshing OAuth tokens automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunaissacoding](https://clawhub.ai/user/tunaissacoding)

### License/Terms of Use:

MIT

## Use Case:

External developers and Clawdbot users maintaining a legacy Claude CLI OAuth setup use this skill to install and manage a macOS token refresher, update Clawdbot auth profiles, and configure refresh notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent process that can read and update Claude OAuth credentials.

Mitigation: Install only when intentionally maintaining a legacy Clawdbot setup, review the installed launchd job, and uninstall it when native Clawdbot onboarding is sufficient.

Risk: The release is for a deprecated use case and may duplicate Clawdbot's native OAuth onboarding.

Mitigation: Prefer Clawdbot's native onboarding path before installing this skill.

Risk: Configuration and skill files affect credential refresh behavior, including the OAuth token endpoint.

Mitigation: Review claude-oauth-refresh-config.json, especially token_url, and treat the skill directory and config as credential-sensitive.

Risk: An existing installation may leave a background token refresher running.

Mitigation: Use uninstall.sh and verify launchctl no longer lists com.clawdbot.claude-oauth-refresher.

## Reference(s):

- [Claude Connect Skill Page](https://clawhub.ai/tunaissacoding/skills/claude-connect)
- [Publisher Profile](https://clawhub.ai/user/tunaissacoding)
- [Clawdbot Docs](https://docs.clawd.bot)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [UPGRADE.md](artifact/UPGRADE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installer, verifier, token refresh, detection, validation, and uninstall shell scripts for a macOS Clawdbot environment.]

## Skill Version(s):

1.1.0 (source: server release metadata, changelog, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
