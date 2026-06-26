## Description: <br>
ClawVault is a portable identity vault for OpenClaw that syncs agent knowledge, memory, package lists, and profiles across machines using user-selected storage providers or ClawVault Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlighty](https://clawhub.ai/user/getlighty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to back up, sync, migrate, and restore agent environment state across multiple machines while keeping each machine on its own profile unless the user explicitly pulls another profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synced vault contents can include sensitive agent knowledge, memory, package manifests, and migration state. <br>
Mitigation: Treat vault contents as sensitive, review the skill before installation, keep backups before pull or profile restore, and avoid storing secrets unless separate trusted protection is in place. <br>
Risk: Security evidence warns not to rely on the skill's encryption claims without real payload encryption from the publisher. <br>
Mitigation: Use trusted storage, avoid depending on ClawVault as the sole confidentiality control, and require publisher-provided payload encryption before syncing highly sensitive data. <br>
Risk: Provider setup and transport choices include external tooling and Git/SFTP host key concerns. <br>
Mitigation: Install rclone from a trusted source yourself and avoid Git or SFTP providers until host key verification is fixed. <br>
Risk: Package restore can propose install commands that affect the local system. <br>
Mitigation: Inspect every package install command and approve only commands that match the intended migration plan. <br>


## Reference(s): <br>
- [ClawVault ClawHub Release](https://clawhub.ai/getlighty/getlighty-clawvault) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup, provider selection, sync operations, profile restore, package diff review, and key management.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and clawvault.sh; SKILL.md frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
