## Description: <br>
Enable or disable the OpenClaw built-in browser with one command, including status checks, automatic backups, restore support, and visible or headless browser modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoo-unison](https://clawhub.ai/user/yoo-unison) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to switch OpenClaw between its built-in browser and Chrome extension modes, inspect browser configuration status, and restore a known configuration backup when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes local OpenClaw browser configuration. <br>
Mitigation: Install and run it only when you intend to switch browser modes, and keep the automatic backups so the prior configuration can be restored. <br>
Risk: Saved sessions in the OpenClaw browser profile may remain available to later browser automation on shared or untrusted machines. <br>
Mitigation: Avoid logging sensitive accounts into that browser profile on shared systems, or clear sessions after use. <br>
Risk: Restoring an unexpected backup file can replace the active OpenClaw configuration. <br>
Mitigation: Use --restore only with backup files you recognize and trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoo-unison/browser-toggle) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may change local OpenClaw browser configuration and create or restore configuration backups.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
