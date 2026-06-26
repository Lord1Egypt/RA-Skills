## Description: <br>
Helps diagnose and repair OpenClaw CLI device scope issues that cause subagent, spawn, or cron operations to fail with pairing-required errors while the gateway is running. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whhh1994](https://clawhub.ai/user/whhh1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an OpenClaw CLI device is paired but lacks the admin-level scopes needed for subagent, spawn, or cron workflows. It guides diagnosis, dry-run review, repair, gateway restart, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair script rewrites local OpenClaw pairing and device-auth files to grant persistent admin-level device scopes. <br>
Mitigation: Run the diagnostic and dry-run modes first, confirm the target device ID and requested scopes, keep generated backups, and avoid force mode unless automation requires it. <br>
Risk: Verification output includes token prefixes that could expose sensitive authentication context if shared. <br>
Mitigation: Do not paste or publish raw verification output; redact token prefixes and device identifiers before sharing logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whhh1994/fix-cli-device-scope) <br>
- [Publisher profile](https://clawhub.ai/user/whhh1994) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration file changes performed by bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The repair workflow writes backups before changing local OpenClaw pairing and device-auth files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
