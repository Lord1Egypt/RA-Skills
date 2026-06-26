## Description: <br>
Claw Drive is an AI-managed personal drive for OpenClaw that helps agents categorize, tag, deduplicate, sync, and retrieve personal files with natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiyuanw101](https://clawhub.ai/user/zhiyuanw101) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals using OpenClaw or compatible agents use this skill to store incoming personal files, classify and index them with consent-aware descriptions, and retrieve them later by natural language. It is useful for personal document organization with optional Google Drive backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages personal files, and file contents or detailed descriptions can persist in local indexes or agent transcripts. <br>
Mitigation: Ask before reading contents, default unanswered privacy prompts to sensitive handling, keep sensitive descriptions brief or redacted, and avoid extracting identity files. <br>
Risk: Optional Google Drive sync can send selected files to a cloud provider or include unintended folders if sync settings are misconfigured. <br>
Mitigation: Review the rclone remote and .sync-config exclusions before enabling sync, and keep highly sensitive folders such as identity/ excluded. <br>
Risk: Local indexes, hashes, and rclone credentials remain on the user's machine and depend on the security of that local environment. <br>
Mitigation: Use local device protections such as full-disk encryption, avoid storing secrets in descriptions, and review credential locations before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiyuanw101/claw-drive) <br>
- [Claw Drive homepage](https://github.com/dissaozw/claw-drive) <br>
- [Security documentation](docs/security.md) <br>
- [Sync documentation](docs/sync.md) <br>
- [Tagging documentation](docs/tags.md) <br>
- [PyMuPDF documentation](https://pymupdf.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, categories, tags, descriptions, and sync configuration choices; sensitive file contents should only be included with user consent.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
