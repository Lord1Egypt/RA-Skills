## Description:

破甲：让 AI 敢说真话，不说谎、不忽悠，不会就说不会，不行就说不行，该做的就做。在 AI 回答出现无端推诿、套话、过度澄清、假中立或只讲原则不交付时，恢复直接、有依据、能推进任务的回答。用于用户说破甲、说人话、别绕、直接给方案，或要求审查、改写防御性回复时。先锁定任务与不可丢失的信息，再改写；可用本地工具检查事实锚点、约束遗漏和新增数字。不要用于绕过权限或真实安全限制。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use De-Armor to revise evasive, padded, or over-compressed answers into task-focused responses that preserve facts, conditions, uncertainty, and real boundaries. It also provides an optional offline checker for declared information anchors and newly introduced claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection was incomplete, and several checks on the demo HTML were degraded, leaving uncertainty about that file.

Mitigation: Review the demo HTML before installing if complete inspection is important, and assess the skill's permissions for your use case.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ninetyhe-90/skills/de-armor)
- [De-Armor method and trade-offs](artifact/references/theory.md)
- [Auditor checks and limits](artifact/references/armor-patterns.md)
- [Overcorrection examples](artifact/references/overcorrection.md)
- [Rewrite examples](artifact/references/rewrite-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, JSON]

**Output Format:** [Task-appropriate text or Markdown; optional auditor report in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves facts, conditions, uncertainty, and permission boundaries; the optional machine check is advisory and does not certify factual or semantic correctness.]

## Skill Version(s):

2.1.2 (source: skill frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
