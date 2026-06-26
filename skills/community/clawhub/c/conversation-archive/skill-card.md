## Description: <br>
Automatically archives session conversations, preserves original records, and supports search, retrieval, and correction workflows that can feed a memory system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anfengxiaoguo](https://clawhub.ai/user/anfengxiaoguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep local conversation archives, search prior sessions, retrieve original records, and extract memory candidates for follow-up memory systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent conversation memory may capture private chat-derived data without clear consent or scope. <br>
Mitigation: Enable only when persistent local conversation memory is intentional, and define exactly which sessions are archived before use. <br>
Risk: Sensitive data could remain in stored archives if redaction, deletion, or automatic-capture controls are not verified. <br>
Mitigation: Confirm how to disable capture, delete stored archives, and test redaction before relying on the archive. <br>
Risk: Extracted memories may carry private or incorrect information into downstream memory systems. <br>
Mitigation: Review extracted memories before reuse or integration with other memory tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anfengxiaoguo/conversation-archive) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and local archive/index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local conversation-derived records when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
