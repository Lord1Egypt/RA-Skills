## Description: <br>
AIS Skill helps agents collaborate with users in a TorchV AIS knowledge base by reading structure, searching and reading documents, creating or updating documents and directories, publishing content, and returning document links through authenticated KB commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuchuan01](https://clawhub.ai/user/liuchuan01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base operators use this skill to let an agent inspect, search, edit, create, publish, upload, download, and link TorchV AIS knowledge-base content through authenticated KB commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AIS tokens copied from browser sessions may expose account or session access if pasted into chat or logs. <br>
Mitigation: Use short-lived, least-privilege AIS tokens when possible and avoid pasting browser session headers into chat or logs. <br>
Risk: Remote write, delete, move, or publish operations can alter or publish real knowledge-base content. <br>
Mitigation: Verify every remote write, delete, move, and publish action before execution, and reread the target content before modifying it. <br>
Risk: File upload, download, and link features can transfer real local or remote files. <br>
Mitigation: Use file transfer features only for files intentionally shared or saved, and confirm paths, document codes, and destinations before execution. <br>


## Reference(s): <br>
- [KB read operations guide](references/read.md) <br>
- [KB write and structure operations guide](references/write.md) <br>
- [KB patch update guide](references/update.md) <br>
- [AIS file transfer guide](references/file-transfer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown or plain text with inline KB commands, JSON command responses, document links, and file transfer results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify remote AIS knowledge-base content and may upload, download, or link files when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
