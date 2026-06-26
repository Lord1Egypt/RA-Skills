## Description: <br>
A multi-level conversation compaction skill that monitors context length and condenses conversation history into structured summaries while preserving key information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinnzen](https://clawhub.ai/user/sinnzen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to compact long conversations into structured summaries before the context window is exhausted. It supports automatic, manual, and focused compaction while preserving current work, important decisions, code details, and unresolved tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A vague request such as "summarize" could trigger compaction when the user did not intend to alter working context. <br>
Mitigation: Prefer explicit commands such as /compact and confirm intent before compacting important work. <br>
Risk: Conversation summaries can carry sensitive details into compressed context or long-term memory. <br>
Mitigation: Redact API keys, passwords, secrets, private keys, credentials, and full local file paths before retaining or storing summaries. <br>
Risk: Writing a compressed summary to long-term memory can preserve information beyond the current conversation. <br>
Mitigation: Require explicit user consent before writing any compressed summary to long-term memory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured summary and compaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted sensitive values and a compaction boundary marker.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
