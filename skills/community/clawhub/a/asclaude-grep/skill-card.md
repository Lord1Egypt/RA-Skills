## Description: <br>
asclaude-grep searches a local OpenClaw workspace for matching file contents and filenames using grep and find. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miaoxingjun](https://clawhub.ai/user/miaoxingjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace users use this skill to locate code, documentation, JSON, and other text matches across local OpenClaw workspaces. It helps with code review, troubleshooting, refactoring, and quick file discovery without uploading workspace data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad searches can surface matching lines or paths from secrets or sensitive documents in the agent conversation. <br>
Mitigation: Use targeted patterns and avoid broad searches in folders that contain secrets or sensitive documents. <br>
Risk: Search results may be incomplete because the script searches selected text file extensions and truncates output to the first 20 matches. <br>
Mitigation: Run narrower follow-up searches or inspect files directly when completeness matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miaoxingjun/asclaude-grep) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/miaoxingjun) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is local to the workspace and may be truncated to the first 20 matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
