## Description: <br>
Share code via GitHub Gist instead of inline chat blocks. Use when code output exceeds 10 lines, when the user asks for copy-friendly code sharing in Discord/chat, or when preserving formatting is important. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeromestein](https://clawhub.ai/user/Jeromestein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to share longer code outputs through GitHub Gist while keeping chat responses concise and copy-friendly. It supports creating secret gists by default and updating an existing gist URL when revising shared code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared files are uploaded to GitHub Gist and may expose secrets, personal data, or proprietary content. <br>
Mitigation: Review files before upload, remove sensitive values, and use placeholders for any required secrets. <br>
Risk: Secret Gists are external URLs and should not be treated as private local storage. <br>
Mitigation: Use secret Gists only for intended sharing, confirm the target GitHub account with gh auth status, and avoid uploading material that must remain private. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Jeromestein/code-share) <br>
- [Publisher Profile](https://clawhub.ai/user/Jeromestein) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with a gist URL and file metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed three-line response format with the shared file summary, Gist URL, filename, and line count.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
