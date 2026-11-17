## Description:

Injects long-term user memory from LanceDB into OpenClaw agent sessions and provides CLI/API workflows for semantic memory search, storage, profile generation, and automatic memory extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asbinbin](https://clawhub.ai/user/asbinbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to persist user preferences, facts, tasks, and general notes in LanceDB, retrieve them semantically, and inject summarized memory into agent bootstrap context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories and search text can contain sensitive personal or business information and may be sent to Zhipu AI for embedding.

Mitigation: Review the privacy model before installation, avoid private content in automatic extraction, and configure approved embedding services and data-handling controls.

Risk: Automatic extraction can persist information from conversations without enough user review.

Mitigation: Require explicit user consent, narrow what can be saved, and provide routine review and deletion procedures for stored memories.

Risk: A hard-coded default user identity can mix memories across users or sessions.

Mitigation: Remove the hard-coded identity and require an explicit OPENCLAW_USER_ID or equivalent authenticated user mapping.

Risk: Shell command construction in the hook can expose execution-safety issues.

Mitigation: Use argument arrays or validated escaping for subprocess calls before production deployment.

Risk: The setup flow can write API keys to ~/.bashrc.

Mitigation: Store credentials in an approved secret manager or scoped environment configuration instead of persistent shell startup files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asbinbin/skills/clawlancememory)
- [Install Guide](docs/INSTALL.md)
- [Usage Guide](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Hook Integration Guide](docs/HOOK.md)
- [Zhipu AI API](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown bootstrap memory content, JSON CLI/API responses, and setup or usage commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local LanceDB storage and a ZHIPU_API_KEY-backed embedding service for memory indexing and retrieval.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
