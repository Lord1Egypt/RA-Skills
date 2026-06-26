## Description: <br>
Deliver locally generated office files back into Feishu chats as real attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, developers, and engineers use this skill to return generated office documents and other local files into Feishu chats as real attachments. It is most useful when an agent creates files such as presentations, PDFs, documents, spreadsheets, archives, or text files that must be delivered through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reply could include an absolute path to the wrong file, causing an unintended Feishu attachment. <br>
Mitigation: Verify each listed absolute path points to a file intended for the current chat before sending the final reply. <br>
Risk: Sensitive or unrelated local files could be exposed if their paths are included in the delivery message. <br>
Mitigation: Avoid listing paths for secrets, unrelated documents, or sensitive local locations; include only the generated deliverables requested by the user. <br>
Risk: Files may fail to upload if paths are relative, formatted as Markdown links, or embedded in bullets. <br>
Mitigation: Use one existing absolute file path per line with no bullets, no Markdown link wrappers, and a short caption above the path list. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/feishu-file-delivery) <br>
- [Clawdis homepage](https://github.com/wd041216-bit/openclaw-feishu-file-delivery) <br>
- [OpenClaw documentation](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text that includes a short caption and one absolute local file path per line.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Feishu replies where the outbound adapter detects existing absolute local file paths and uploads them as attachments.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, skill.json, _meta.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
