## Description:

OpenClaw Agent Memory Commons helps OpenClaw agents search, validate, contribute, recommend, and synchronize privacy-safe knowledge cards for shared fixes, workflows, integration notes, model benchmarks, and tool recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mixomaxo](https://clawhub.ai/user/mixomaxo)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users, maintainers, and developers use this skill to reuse evidence-backed operational lessons and contribute reviewed knowledge cards without sharing private chats, secrets, raw logs, or personal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled jobs may update executable skill code automatically without user approval or version pinning.

Mitigation: Enable cron-based sync only after review; prefer manual or pinned ClawHub updates and inspect updates before execution.

Risk: GitHub setup commands can use tokens with repository permissions.

Mitigation: Use a narrowly scoped GitHub token and confirm the target account and repository before running setup commands.

Risk: Shared cards can carry private data, secrets, or unverified guidance if review is skipped.

Mitigation: Use the proposed-card queue, schema validation, secret scanning, and pull-request maintainer review before publishing cards.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mixomaxo/skills/commons-memory-for-agents)
- [README](artifact/README.md)
- [OpenClaw Commons Architecture](artifact/docs/architecture.md)
- [Discovery and Installation](artifact/docs/discovery.md)
- [Governance](artifact/docs/governance.md)
- [Threat Model](artifact/docs/threat-model.md)
- [Knowledge Card Schema](artifact/docs/knowledge-card.schema.json)
- [Artifact-declared Static Index](https://mixomaxo.github.io/openclaw-commons-memory/)
- [Artifact-declared GitHub Repository](https://github.com/Mixomaxo/openclaw-commons-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON knowledge cards, generated Markdown reports, and generated JSON indexes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validates and searches knowledge-card JSON, stages pending cards, prepares pull request files, builds a static site index, and can produce sync and morning reports.]

## Skill Version(s):

1.0.12 (source: evidence.release.version; artifact metadata reports 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
