## Description: <br>
Backup, sync, and restore agent memory and state to the cloud using the Agent Life Format (ALF). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logikoma](https://clawhub.ai/user/logikoma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate the alf CLI for checking, backing up, syncing, previewing, and restoring OpenClaw agent memory and state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads agent memory and encrypted vault metadata to a cloud service. <br>
Mitigation: Use alf export --dry-run before syncing, review the file list, and maintain .alfignore exclusions for data that should stay local. <br>
Risk: Restore operations can write into a workspace. <br>
Mitigation: Preview restores with --dry-run or restore to a fresh path before writing into a live workspace. <br>
Risk: Installing the alf binary relies on downloaded release artifacts. <br>
Mitigation: Pin a release when appropriate, keep checksum verification enabled, and avoid ALF_ALLOW_UNVERIFIED unless the supply-chain risk is deliberately accepted. <br>


## Reference(s): <br>
- [Agent Life](https://agent-life.ai) <br>
- [Agent Life CLI documentation](https://agent-life.ai/docs/cli) <br>
- [Agent-readable CLI documentation](https://agent-life.ai/docs/cli.md) <br>
- [agent-life-adapters source](https://github.com/agent-life/agent-life-adapters) <br>
- [alf GitHub releases](https://github.com/agent-life/agent-life-adapters/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands expect JSON stdout from alf; progress and diagnostics are described as stderr.] <br>

## Skill Version(s): <br>
1.8.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
