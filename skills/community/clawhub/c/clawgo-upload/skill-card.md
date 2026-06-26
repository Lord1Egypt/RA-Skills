## Description: <br>
Zips selected local files or folders, uploads the archive to clawgo.me, and returns a shareable clone link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjunyeee](https://clawhub.ai/user/chenjunyeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to package selected workspace files, upload them to clawgo.me, and share or move the resulting clone link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files may include secrets, personal data, or workspace profile files that should not be uploaded. <br>
Mitigation: Require the agent to list the exact files and archive size before upload, then remove or redact sensitive content before proceeding. <br>
Risk: A clone link can expose the uploaded archive to anyone who has the key. <br>
Mitigation: Treat the clone key and link as sensitive, share them only with intended recipients, and avoid uploading files that should not leave the local workspace. <br>
Risk: Workspace context files such as USER.md, TOOLS.md, AGENTS.md, or SOUL.md can contain profile, policy, or access details. <br>
Mitigation: Review and redact these files before upload, or exclude them unless the user explicitly confirms they should be shared. <br>


## Reference(s): <br>
- [Published ClawHub skill page](https://clawhub.ai/chenjunyeee/clawgo-upload) <br>
- [ClawGo upload service](https://clawgo.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus upload result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a zip archive and reports the clone link, key, file name, size, and upload time after a successful upload.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
