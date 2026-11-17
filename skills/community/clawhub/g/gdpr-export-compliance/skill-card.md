## Description:

A practical GDPR compliance playbook for Chinese companies expanding into Europe, with guidance and a zero-dependency local toolkit for scope checks, lawful-basis selection, data-subject rights, DPIA, cross-border transfer mechanisms, breach notification, fines, and GDPR/PIPL comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Legal, compliance, and data leaders use this skill to assess GDPR obligations for China-to-Europe business workflows, including applicability, lawful processing bases, data-subject rights, DPIA, transfer mechanisms, breach response, and penalty exposure. Developers and operators can use the bundled local CLI for structured first-pass checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance guidance may become outdated or may not fit a specific regulatory fact pattern.

Mitigation: Treat outputs as an initial aid, verify current GDPR guidance before relying on them, and consult qualified legal counsel or a DPO for real regulatory decisions.

Risk: Verification scripts may read package-local files and regenerate local verification outputs.

Mitigation: Run verification scripts only in a controlled copy of the package when those local file reads and output regeneration are acceptable.

## Reference(s):

- [GDPR 全景与适用范围](references/01-GDPR全景与适用范围.md)
- [合法处理基础](references/02-合法处理基础.md)
- [数据主体权利](references/03-数据主体权利.md)
- [DPIA 评估](references/04-DPIA评估.md)
- [跨境传输机制](references/05-跨境传输机制.md)
- [违规罚款与泄露通报](references/06-违规罚款与泄露通报.md)
- [GDPR 与个保法对照](references/07-GDPR与个保法对照.md)
- [FAQ](references/08-FAQ.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Text]

**Output Format:** [Markdown guidance with optional local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language GDPR compliance guidance; the local CLI uses Python standard library functionality and does not require network access.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
