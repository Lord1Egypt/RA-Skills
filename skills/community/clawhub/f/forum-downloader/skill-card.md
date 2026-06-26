## Description: <br>
Downloads images and videos from forum posts into a user-selected directory, including proxy-based access, title-based folder creation, and PowerShell-based downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zitao666](https://clawhub.ai/user/zitao666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and forum users use this skill to collect media from supported forum posts into organized local folders. It is intended for workflows where the user provides the forum URL, destination directory, and any required proxy settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run PowerShell, contact a forum through the proxy the user provides, and save many files locally. <br>
Mitigation: Use trusted forum URLs and proxy settings, review the generated PowerShell before execution, and download into a dedicated folder. <br>
Risk: Title-based output directories can place downloaded files in an unexpected folder if the page title is surprising or malformed. <br>
Mitigation: Confirm the resolved output directory before allowing downloads and adjust the destination path when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zitao666/forum-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks and download instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create title-based folders and download media files through a user-provided proxy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
