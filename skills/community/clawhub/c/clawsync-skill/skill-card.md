## Description: <br>
Backs up and restores an OpenClaw configuration, including skills, memory, settings, credentials, history, and optional workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zaosusu](https://clawhub.ai/user/Zaosusu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create, list, verify, and restore configuration backups for migration, disaster recovery, daily backups, or controlled sharing of skills and settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain sensitive OpenClaw data such as credentials, memory, history, and workspace files. <br>
Mitigation: Use quick or selective backups when possible, avoid including credentials/history/workspace data unless needed, and store backup ZIP files only in trusted protected locations. <br>
Risk: The security review says encryption is claimed but should not be relied on for protecting backup archives. <br>
Mitigation: Apply separate, reviewed encryption or storage controls before moving or sharing backup ZIP files. <br>
Risk: Restore behavior may write outside the intended OpenClaw folder. <br>
Mitigation: Restore only archives you created and inspected, use dry-run or manual inspection first, and run restore in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zaosusu/clawsync-skill) <br>
- [OpenClaw website](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ZIP backup files and restore configuration files when the bundled script is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
