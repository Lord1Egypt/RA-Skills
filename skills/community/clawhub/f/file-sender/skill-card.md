## Description: <br>
File Sender packages workspace files into ZIP archives, stores a human-readable description, and notifies a Manager service for user delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to package completed workspace deliverables and send them to users with a short description. It is intended for local workspace files, not remote web content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can proactively package workspace files without explicit per-send user confirmation. <br>
Mitigation: Require the agent to show the exact path being packaged and obtain confirmation before running the send script. <br>
Risk: Broad directories may include secrets or unintended files. <br>
Mitigation: Package only narrow, reviewed paths and avoid directories that may contain credentials, private data, or unrelated project files. <br>
Risk: Delivered files and descriptions are persisted in .file-outbox. <br>
Mitigation: Periodically clean .file-outbox when deliveries contain sensitive material. <br>
Risk: Delivery depends on a trusted Manager service and injected file-push token. <br>
Mitigation: Use the skill only in environments where the Manager URL and injected token are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyhit2005/file-sender) <br>
- [Publisher profile](https://clawhub.ai/user/whyhit2005) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands] <br>
**Output Format:** [ZIP archive with companion plain-text description and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, zip, and Manager-injected OpenClaw environment variables; enforces /home/node/workspace scope and a 500MB ZIP size limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
