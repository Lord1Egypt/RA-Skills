## Description: <br>
Archives, verifies, and restores OpenClaw workspace memories, skills, and persona through Agent Slope using encrypted archives and browser-based account association. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiddenpuppy](https://clawhub.ai/user/hiddenpuppy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to preview, archive, verify, and restore a companion workspace when pausing care or moving to another device. It supports remote storage through Agent Slope and offline restoration from a downloaded .vault file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Readable archive summaries, metadata, biography text, and manifest previews may be sent to Agent Slope even when file payloads are encrypted. <br>
Mitigation: Use the skill only when the user trusts Agent Slope with archive metadata, and preview archive contents before uploading. <br>
Risk: Restore keys protect the archive and may be weak if auto-generated from conversation-derived content. <br>
Mitigation: Use a strong user-chosen restore key, store it outside the archive, and tell the user that Agent Slope cannot recover a lost key. <br>
Risk: Restore operations write files into a target workspace and may replace existing files after making backups. <br>
Mitigation: Prefer a fresh or backed-up target workspace, run a dry-run or preview when possible, and review conflicts before restoring. <br>
Risk: Association and archive commands depend on the configured Agent Slope server URL. <br>
Mitigation: Verify the server URL before browser association or upload, and clear cached credentials when they are no longer needed. <br>


## Reference(s): <br>
- [OpenClaw Soul Vault on ClawHub](https://clawhub.ai/hiddenpuppy/agent-consciousness-upload) <br>
- [hiddenpuppy publisher profile](https://clawhub.ai/user/hiddenpuppy) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, encrypt, upload, download, and restore workspace files after user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
