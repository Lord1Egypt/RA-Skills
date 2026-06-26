## Description: <br>
Cex provides shell commands for adding, listing, searching, deleting, exporting, and configuring local entries under a user-controlled data directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill as a simple local entry tracker for notes or records, with commands to add, inspect, search, remove, export, and configure entries. It should not be treated as CEX or protocol-security analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as CEX and blockchain security analysis, but the security review says it functions as a persistent local entry tracker. <br>
Mitigation: Install it only for local entry tracking, and do not rely on it for CEX or protocol-security analysis. <br>
Risk: Entries, configuration, and exported files may contain sensitive notes if users store them there. <br>
Mitigation: Avoid storing secrets, account details, trading records, or sensitive investigation notes, and review ~/.cex plus cex-export files when using or removing the skill. <br>


## Reference(s): <br>
- [Cex on ClawHub](https://clawhub.ai/xueyetianya/cex) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text command output, JSONL or CSV exports, and config key-value text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local data under CEX_DIR, defaulting to ~/.cex, and can export cex-export files in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
