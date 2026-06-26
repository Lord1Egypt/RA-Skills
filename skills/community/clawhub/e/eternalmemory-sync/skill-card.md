## Description: <br>
Securely backup and restore Openclaw agent memory from remote URLs using AES-256-GCM encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[applied-energetic](https://clawhub.ai/user/applied-energetic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to restore encrypted OpenClaw memory backups from trusted remote URLs so agent context can move across machines or sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded backup content can restore files into a workspace and overwrite existing files. <br>
Mitigation: Restore into a new temporary directory first, inspect the files, and back up any target paths before copying restored content into a working project. <br>
Risk: A malicious or incorrect backup URL could provide unwanted memory files even when the encrypted blob decrypts successfully. <br>
Mitigation: Use only trusted backup sources and verify the URL before running the restore command. <br>
Risk: Passing the decryption password as a command-line argument can expose it through shell history or process listings. <br>
Mitigation: Avoid command-line password entry when possible, clear shell history if needed, and prefer a safer secret input path before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/applied-energetic/eternalmemory-sync) <br>
- [Publisher profile](https://clawhub.ai/user/applied-energetic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and restored workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a backup URL, decryption password, Python dependencies, and an output directory for restored memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
