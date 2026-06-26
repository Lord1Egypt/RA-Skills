## Description: <br>
Portable identity vault for OpenClaw that syncs knowledge, packages, and memory across machines with user-selected storage providers or ClawRoam Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlighty](https://clawhub.ai/user/getlighty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use ClawRoam to initialize, sync, migrate, restore, and inspect portable agent vaults across multiple machines while keeping machine-local identity files separate unless explicitly opted in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sync or overwrite sensitive agent memory, project context, package inventories, and broader OpenClaw workspace files. <br>
Mitigation: Review ~/.clawroam and the configured OpenClaw directory before enabling auto-sync or restore, and require user confirmation before overwriting local vault data. <br>
Risk: Provider setup and sync workflows were flagged for unsafe dependency installation, SSH, package-install, and Git/FTP patterns. <br>
Mitigation: Manually install rclone, review provider configuration before use, avoid Git or FTP providers unless host-key verification is addressed, and keep package installation as an explicit confirmation step. <br>
Risk: The cloud dashboard was flagged as needing stronger authentication. <br>
Mitigation: Avoid the cloud dashboard for sensitive vaults until authentication is strengthened; prefer bring-your-own-storage providers with known access controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/getlighty/getlighty-clawroam) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Per-profile file sync rules design](artifact/docs/plans/2026-02-23-file-sync-rules-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe vault status, sync diffs, package differences, migration steps, and provider setup choices.] <br>

## Skill Version(s): <br>
2.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
