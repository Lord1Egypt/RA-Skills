## Description: <br>
Backup or restore a complete OpenClaw installation, including configuration, agents, skills, credentials, memory, workspace, and Telegram bots, as a portable .tar.gz archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create, list, verify, encrypt, and restore full OpenClaw home-directory backups for migration or recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain credentials, identity tokens, secrets, and other sensitive OpenClaw state. <br>
Mitigation: Treat archives as highly sensitive, store them in trusted locations, and use GPG encryption before moving backups through cloud storage, shared drives, or removable media. <br>
Risk: Restore handling is broad for full-environment archives. <br>
Mitigation: Restore only archives that the operator created or explicitly trusts, and verify archive integrity before restoring. <br>


## Reference(s): <br>
- [OpenClaw Backup Path Policy](references/paths.md) <br>
- [GnuPG Downloads](https://gnupg.org/download/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include archive paths, backup sizes, verification status, restore summaries, and security handling guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
