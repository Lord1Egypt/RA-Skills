## Description:

Transfers files based on chat context with MIME validation, progress tracking, and a simulated Telegram transfer adapter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghostwritten](https://clawhub.ai/user/ghostwritten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add context-aware file validation, transfer routing, and transfer-status reporting to chat agents. The current Telegram behavior should be treated as simulated until a real integration is added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may expose local file paths or pass untrusted paths into file handling and cleanup helpers.

Mitigation: Restrict the paths the agent can access, use a dedicated temporary directory, and call cleanupTempFile only with trusted paths created by the skill.

Risk: The Telegram adapter reports simulated progress and completion, which can be mistaken for real file delivery.

Mitigation: Label Telegram transfers as simulation in deployments and require explicit user confirmation and privacy disclosure before adding a real Telegram integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ghostwritten/skills/file-transfer)
- [API Reference](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with JavaScript code snippets and JSON-like transfer result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns transfer status, context analysis, file validation details, and transfer statistics; transfer history is not persisted.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
