## Description: <br>
Codex Switcher helps OpenClaw users manage multiple local Codex accounts through OAuth auth snapshots for adding accounts, switching profiles, checking quota, and refreshing tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppaibb](https://clawhub.ai/user/ppaibb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw with multiple Codex accounts use this skill to add OAuth snapshots, switch the active Codex profile, inspect the current account and quota, and refresh expiring snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores refreshable OAuth tokens and can modify the active Codex auth profile. <br>
Mitigation: Install only when this credential-management behavior is expected; restrict snapshot files to owner-only permissions, confirm the target profile before switching, keep backups for rollback, and revoke tokens if a snapshot directory may have been exposed. <br>
Risk: Credential values may be exposed if snapshot files or command output are copied into chat or logs. <br>
Mitigation: Treat all snapshot files as secrets and never display full access tokens or refresh tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppaibb/codex-switcher) <br>
- [Security Notes](references/security-notes.md) <br>
- [Local Flow Sketch](scripts/README-local-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and local configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths and command invocations; full access tokens and refresh tokens should not be displayed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
