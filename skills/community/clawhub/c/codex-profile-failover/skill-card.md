## Description: <br>
Provides automatic and manual failover between existing OpenClaw openai-codex OAuth profiles when usage remaining is low, usage or auth checks fail, or an operator requests a switch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugurinanc12](https://clawhub.ai/user/ugurinanc12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and run a Codex profile failover layer that monitors usage and auth health, recommends or applies session profile switches, and provides manual trigger commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with OAuth-backed Codex profiles and local OpenClaw auth/session state. <br>
Mitigation: Install only in workspaces where profile failover is intended, keep token and state files access-controlled, and verify that no personal identifiers are committed with published configs. <br>
Risk: Apply-mode commands can change session authProfileOverride values and create state backups or event logs. <br>
Mitigation: Run the threshold guard or watchdog in dry-run or once mode first, review the selected target sessions and candidate profiles, then use apply mode only after the result matches operator intent. <br>
Risk: A long-running watchdog may repeatedly switch profiles when thresholds, token expiry, or usage errors are detected. <br>
Mitigation: Use conservative thresholds, review watchdog and event-log paths, and monitor generated JSON status output after enabling the background process. <br>


## Reference(s): <br>
- [Setup](references/setup.md) <br>
- [Threshold config example](references/threshold-config.example.json) <br>
- [Watchdog config example](references/watchdog-config.example.json) <br>
- [ClawHub release page](https://clawhub.ai/ugurinanc12/codex-profile-failover) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python scripts that emit JSON status payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write workspace-local configuration, event logs, backups, and session profile override updates when run with apply options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
