## Description: <br>
Guides agents through incremental synchronization of local content into Feishu documents, including table replacement, positioned inserts, header-row creation, column widths, and diff-based updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read, create, update, and synchronize Feishu documents and Docx tables while preserving structure and formatting where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to make persistent edits to Feishu documents. <br>
Mitigation: Confirm the target document, requested operation, and permissions before allowing write, append, insert, delete, or table operations. <br>
Risk: The artifact describes reading local Feishu app credentials and using raw API calls outside the declared tool workflow. <br>
Mitigation: Do not use the raw API/header-row workflow unless explicitly approved, and keep credential access behind a vetted user-approved tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deadblue22/feishu-doc-sync) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples, shell command examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe Feishu document actions that create persistent document changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
