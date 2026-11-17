## Description: <br>
Cloud Manager Free helps individual users choose, organize, sync, back up, and safely share files with consumer cloud storage services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual users use this skill for practical guidance on consumer cloud-storage selection, cleanup, synchronization, backup planning, and safe sharing. It is aimed at personal file and photo workflows rather than infrastructure cloud storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud sync, upload, copy, and deletion commands may overwrite, remove, or expose real files if executed against live accounts. <br>
Mitigation: Review every path, remote name, filter, and sync direction before execution; test on disposable data first and keep a separate backup. <br>
Risk: The skill requests broad read, write, and exec capabilities for guidance that is mostly Markdown-based. <br>
Mitigation: Install with the least privileges needed and avoid granting command execution unless a reviewed command must be run. <br>
Risk: Examples include cloud API tokens and account-backed command-line tools. <br>
Mitigation: Use short-lived credentials where possible, avoid pasting secrets into shared logs, and revoke tokens after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-manager-free) <br>
- [Skill artifact](artifact/SKILL.md) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with tables and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rclone, PowerShell, 7z, and VeraCrypt examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
