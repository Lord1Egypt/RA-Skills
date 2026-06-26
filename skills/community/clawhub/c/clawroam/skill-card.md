## Description: <br>
Portable identity vault for OpenClaw that syncs knowledge, packages, and memory across machines with user-selected storage providers or ClawRoam Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlighty](https://clawhub.ai/user/getlighty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent operators use ClawRoam to initialize, sync, back up, migrate, and restore an agent vault across machines while preserving per-machine identity files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote storage providers and restored vault data can affect sensitive agent files. <br>
Mitigation: Use narrowly scoped storage accounts, keep auto-sync off until exclusions are confirmed, and avoid syncing secrets or credentials. <br>
Risk: Package restore can propose host package installation from vault state. <br>
Mitigation: Review package diffs and do not run package restore from a vault that is not fully trusted. <br>
Risk: Git or SFTP provider use can depend on remote host identity. <br>
Mitigation: Verify SSH host keys manually before using Git or SFTP-backed sync. <br>
Risk: The hosted dashboard has authentication concerns in the security guidance. <br>
Mitigation: Avoid the hosted dashboard until authentication is stronger. <br>


## Reference(s): <br>
- [ClawRoam ClawHub listing](https://clawhub.ai/getlighty/clawroam) <br>
- [ClawRoam README](artifact/README.md) <br>
- [ClawRoam skill definition](artifact/SKILL.md) <br>
- [ClawRoam Cloud API endpoint](https://clawroam-api.ovisoftblue.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to run local shell scripts that modify vault files, sync data to configured providers, and propose package installation commands.] <br>

## Skill Version(s): <br>
3.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
