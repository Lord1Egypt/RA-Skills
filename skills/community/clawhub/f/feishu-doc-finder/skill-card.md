## Description: <br>
Find and download files from Feishu chat history by filename. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to locate a named file in Feishu chat history and download it when automatic retrieval misses a file or when older shared files need to be recovered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded file names can influence the local save path. <br>
Mitigation: Use least-privilege Feishu app credentials, run only against trusted chats, choose a dedicated empty output directory, and review path handling before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/feishu-doc-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Command-line text output and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET environment variables, plus chat ID, filename, optional output directory, and optional search time window.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
