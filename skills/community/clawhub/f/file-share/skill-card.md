## Description: <br>
Transfers files from the OpenClaw workspace to external file-sharing services using curl uploads, with support for transfer.whalebone.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakah2551](https://clawhub.ai/user/jakah2551) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload selected workspace files, such as logs, reports, or generated media, to a shareable external URL. It is intended for deliberate file transfer workflows where the operator has reviewed the file contents before upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive workspace files to a third-party transfer service and return a shareable download URL. <br>
Mitigation: Review file contents before upload, avoid secrets, credentials, private logs, memory files, and regulated data unless encrypted, and use a controlled transfer channel when stronger handling is required. <br>
Risk: Server security evidence reports weak path containment and no clear confirmation step. <br>
Mitigation: Confirm the exact file path and intended recipient before execution, and restrict uploads to files deliberately selected from the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jakah2551/file-share) <br>
- [Publisher profile](https://clawhub.ai/user/jakah2551) <br>
- [Transfer service reference](references/transfer_service.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples and returned download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute curl to upload a selected workspace file and return a shareable URL from the transfer service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
