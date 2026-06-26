## Description: <br>
Restores readable filenames for Feishu-downloaded files by mapping hashed local names to original names and reporting batch rename results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Feishu users use this skill to restore meaningful names for locally downloaded Feishu files, including batch workflows for chat, document, and table-derived file mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rename local files in place from broad chat triggers without a preview or confirmation. <br>
Mitigation: Use it only on copied or backed-up Feishu downloads and require the agent to show the exact old and new filenames before allowing any rename. <br>
Risk: Broad natural-language triggers could cause unintended rename attempts. <br>
Mitigation: Prefer explicit slash commands such as /rename-file or /feishu-rename for operational use. <br>
Risk: The server security guidance warns not to rely on output-directory, Bitable/message-ID support, or the generated log as a full rollback mechanism unless implementation gaps are fixed. <br>
Mitigation: Treat the log as an audit aid, keep a separate backup, and validate those features in a test directory before using them on working files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/feishu-file-renamer) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown status messages, rename logs, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local rename log and rename files in place unless run against copied files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
