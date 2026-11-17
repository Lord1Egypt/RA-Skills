## Description:

ByteRover provides `brv` CLI workflows for agents to query and curate project knowledge stored as Markdown in `.brv/context-tree` using a configured LLM provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qxbcn](https://clawhub.ai/user/qxbcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve project-specific memory before work and save durable implementation patterns or decisions after work. It supports local Markdown storage and optional authenticated cloud sync for team knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to query and persist project memory broadly, which can create or rely on context without an explicit consent boundary.

Mitigation: Use the skill only when project memory is intentionally needed, and confirm before saving new or sensitive project knowledge.

Risk: LLM-backed query and curate commands may send prompts, context, and attached file contents to the configured provider.

Mitigation: Avoid secrets, credentials, regulated data, and unnecessary file attachments; inspect selected files before running `brv curate`.

Risk: The documented installation command installs the latest global CLI package, which may change over time.

Mitigation: Prefer a pinned or otherwise verified `byterover-cli` installation before using the skill in sensitive repositories.

Risk: Optional cloud sync sends local knowledge to ByteRover cloud spaces when authenticated push or pull commands are used.

Mitigation: Use cloud sync only with approved accounts and spaces, and review `.brv/context-tree/` contents before syncing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qxbcn/skills/byterover-2-0-0)
- [Publisher profile](https://clawhub.ai/user/qxbcn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update human-readable Markdown knowledge files under `.brv/context-tree/`; file attachments are limited to five project-scoped files per curate command.]

## Skill Version(s):

2.0.0 (source: artifact/_meta.json); ClawHub release 1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
