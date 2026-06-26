## Description: <br>
Sends workspace files such as images, audio, and documents through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tazio7](https://clawhub.ai/user/Tazio7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill when they need to share a selected workspace file through Feishu with an optional caption. It is suited to user-approved sends of known workspace files, not unattended sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send workspace files to Feishu, which may expose sensitive content externally. <br>
Mitigation: Before each send, verify the file path, file contents, caption, and recipient or channel; avoid sending sensitive files unless external sharing is acceptable. <br>
Risk: Using a non-workspace path or the wrong message parameter can cause failed delivery or unintended behavior. <br>
Mitigation: Use workspace paths and the documented media, file_path, or path parameter for file sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tazio7/feishu-file-send) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown instructions with Python tool-call examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes workspace file paths, Feishu channel selection, optional captions, and recipient or channel review before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
