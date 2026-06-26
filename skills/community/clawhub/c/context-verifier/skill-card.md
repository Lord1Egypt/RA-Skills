## Description: <br>
Know the file you're editing is the file you think it is — verify integrity before you act. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to compute SHA-256 hashes, verify that files have not changed unexpectedly, classify file-change severity, and create context packets for review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read any user-specified path for hashing or packet creation. <br>
Mitigation: Use precise file paths and narrow globs instead of broad workspace-wide patterns. <br>
Risk: Using --include-content can store sensitive file contents in context packets. <br>
Mitigation: Do not use --include-content with .env files, credentials, secrets, or other private data. <br>
Risk: Context packets are written under output/context-packets/ and may remain on disk. <br>
Mitigation: Keep output/context-packets/ out of git and delete old packets when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leegitw/context-verifier) <br>
- [Publisher profile](https://clawhub.ai/user/leegitw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style command responses and JSON context packet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes context packets to output/context-packets/ when packet creation is requested.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
