## Description: <br>
Transfers files based on chat context with MIME validation, progress tracking, and an extensible channel adapter design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghostwritten](https://clawhub.ai/user/ghostwritten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add context-aware file transfer flows that validate local file paths, infer transfer intent, and route files through channel adapters such as Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Telegram adapter simulates transfer behavior and does not perform a real Telegram API upload in this version. <br>
Mitigation: Treat transfer results as non-production until a real adapter is configured and verified with explicit user confirmation. <br>
Risk: The agent receives explicit local file paths and destination chat identifiers, which can expose sensitive files or send data to the wrong destination. <br>
Mitigation: Require confirmation of the file path and destination before transfer, avoid sensitive files unless the destination is verified, and redact logs. <br>
Risk: The security evidence notes that readFileInChunks does not read actual file bytes reliably enough for production use. <br>
Mitigation: Do not rely on chunked file reads for real sharing until the implementation is fixed and tested with real file contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ghostwritten/file-transfer) <br>
- [API Reference](docs/API.md) <br>
- [Development Guide](docs/DEVELOPMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JavaScript examples with configuration objects and transfer result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transfer status, context analysis, validation results, and transfer metadata; Telegram transfer behavior is simulated in this version.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
