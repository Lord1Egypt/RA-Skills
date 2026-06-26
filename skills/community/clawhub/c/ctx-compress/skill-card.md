## Description: <br>
Intelligently compress context - conversations, code, logs - while preserving key information and reducing token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compress long conversations, code, logs, and text into smaller summaries that preserve decisions, issues, key code, changes, and statistics for memory-efficient workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compression is lossy, so summaries can omit context that later becomes important. <br>
Mitigation: Keep source files or conversation history available for review, and use light compression when fidelity matters. <br>
Risk: Code compression can remove comments or imports that carry important intent or setup details. <br>
Mitigation: Review compressed code before using it for implementation decisions, and avoid aggressive mode for unfamiliar code. <br>
Risk: Chat and log compression rely on pattern matching and can miss non-standard formats. <br>
Mitigation: Set the content type explicitly when auto-detection is uncertain and verify extracted decisions, errors, and fixes. <br>


## Reference(s): <br>
- [Context Compressor on ClawHub](https://clawhub.ai/besty0121/ctx-compress) <br>
- [Publisher profile](https://clawhub.ai/user/besty0121) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown sections, JSON extraction output, and CLI-oriented shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports light, medium, and aggressive compression levels; content type can be auto-detected or set to chat, code, log, or text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
