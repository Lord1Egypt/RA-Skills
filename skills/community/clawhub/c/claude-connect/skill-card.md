## Description: <br>
Connects Claude CLI OAuth credentials to Clawdbot and refreshes them with a local scheduled job. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TunaIssaCoding](https://clawhub.ai/user/TunaIssaCoding) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this legacy Clawdbot helper to copy Claude CLI OAuth credentials from macOS Keychain into Clawdbot auth profiles and keep them refreshed. The release README says current Clawdbot handles Claude OAuth natively, so this skill is mainly for users who specifically need the older refresher behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies live Claude OAuth refresh tokens from Keychain into a local Clawdbot auth file. <br>
Mitigation: Install only when this legacy refresher is specifically needed; review the destination auth file and local file permissions before running installer or refresh scripts. <br>
Risk: The installer sets up a persistent launchd background job that refreshes tokens automatically. <br>
Mitigation: Review the launchd job before loading it, monitor the refresh log, and use the provided uninstall path to remove the job when native Clawdbot OAuth support is sufficient. <br>
Risk: Notification recipient auto-detection may use local Clawdbot data with insufficient scoping. <br>
Mitigation: Disable notifications or manually set the notification channel and target in the configuration before enabling automatic refresh. <br>


## Reference(s): <br>
- [Claude Connect on ClawHub](https://clawhub.ai/TunaIssaCoding/claude-connect) <br>
- [Clawdbot documentation](https://docs.clawd.bot) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup, refresh, verification, and uninstall guidance for a macOS credential refresher.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and CHANGELOG, released 2026-01-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
