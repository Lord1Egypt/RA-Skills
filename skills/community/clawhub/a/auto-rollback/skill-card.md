## Description: <br>
Timed rollback safety net for edits to ~/.openclaw/openclaw.json on macOS. Use when changing Gateway config, restarting Gateway after config edits, or needing backup + auto-restore protection via launchd and BOOT.md health-check cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill before changing OpenClaw Gateway configuration on macOS so an agent can create a backup, schedule a timed rollback, and cancel the rollback after a healthy restart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rollback helper creates a temporary macOS launchd job that can restore ~/.openclaw/openclaw.json and restart Gateway. <br>
Mitigation: Use it only when that behavior is intended, inspect status after configuration work, and cancel or remove the rollback plist and helper script if automatic cancellation does not run. <br>
Risk: Cleanup can trust a mutable state file when deleting a launchd plist. <br>
Mitigation: Before broad use, constrain cleanup to the fixed rollback plist label or validate the state file label strictly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/extraterrest/auto-rollback) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and generated local shell, plist, state, backup, and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS only; requires bash, launchctl, jq, curl, and plutil; creates a 10-minute rollback window for ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
1.2.0-alpha.2 (source: evidence release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
