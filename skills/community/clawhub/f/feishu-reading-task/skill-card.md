## Description: <br>
Creates Feishu read-later tasks from chat trigger phrases, assigns saved content to the conversation sender, and records the item in local memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[partigle](https://clawhub.ai/user/partigle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and automation users use this skill to save links, documents, or other chat content into Feishu as assigned read-later tasks for the conversation sender. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read-later trigger phrases can create tasks from sensitive or unintended chat content. <br>
Mitigation: Use care in sensitive conversations and confirm the content and assignee before creating a Feishu task when intent is ambiguous. <br>
Risk: Saved links, titles, descriptions, sender IDs, and timestamps are used for Feishu task creation and recorded in local memory. <br>
Mitigation: Install only where this data handling is acceptable, and avoid saving confidential content unless the workspace retention policy allows it. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/partigle/feishu-reading-task) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Files] <br>
**Output Format:** [JSON task payload plus concise chat confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include saved links, titles, descriptions, sender IDs, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
