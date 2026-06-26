## Description: <br>
Manages long-term memory and files for multiple AI agents using vector search and timeline filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janussilence](https://clawhub.ai/user/janussilence) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, index, search, and delete per-agent files and context for long-running projects. It supports semantic and timeline-filtered retrieval, with optional LLM analysis when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads context-manager code from a separate local workspace path that is not bundled in the artifact. <br>
Mitigation: Review and pin the separate context-manager code and dependencies before installation or use. <br>
Risk: The skill can retain long-term local memory, embeddings, caches, and logs. <br>
Mitigation: Avoid storing secrets or regulated data unless retention, storage, and deletion behavior have been reviewed. <br>
Risk: Natural-language deletion requests can remove agent or file context. <br>
Mitigation: Review deletion requests before execution and maintain backups for important context stores. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/janussilence/autoglm-context-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like text responses with status messages, search result summaries, and inline configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, index, retrieve, or delete local context data when the external context-manager workspace is installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
