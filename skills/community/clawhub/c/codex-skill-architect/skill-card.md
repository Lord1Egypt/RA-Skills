## Description:

Audits and restructures large SKILL.md files into routed skill packs, and turns long conversations into reusable snapshots for later handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit and modularize oversized agent skills with backups and validation, or to capture long conversations as snapshots and skill packs for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local skill files may be modified or overwritten.

Mitigation: Use only on trusted repositories, approve the change scope, retain a backup, and review the result before relying on it.

Risk: Conversation snapshots or handoff archives may expose private material.

Mitigation: Use explicit snapshot and output paths, and inspect the generated handoff zip before sharing it.

Risk: Broad tests or commands supplied by untrusted text may execute locally.

Mitigation: Do not pass untrusted text into --test-command; review commands before running them.

Risk: Generic continuation requests may cause the skill to read an unintended snapshot.

Mitigation: Avoid generic continuation triggers and specify the intended snapshot path.

Risk: The release license conflicts with the bundled non-commercial license.

Mitigation: Confirm applicable license terms with the publisher before commercial use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lisong2003-lgtm/skills/codex-skill-architect)
- [Skill restructuring best practices](artifact/references/瘦身最佳实践.md)
- [Conversation summarization best practices](artifact/references/长对话归纳最佳实践.md)
- [Cross-user handoff best practices](artifact/references/跨用户传输最佳实践.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reports, skill packs, routing indexes, conversation snapshots, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May package a conversation snapshot and skill packs as a handoff zip; review contents before sharing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled files say 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
