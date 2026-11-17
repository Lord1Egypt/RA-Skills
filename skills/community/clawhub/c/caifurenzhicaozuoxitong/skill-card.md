## Description:

A Chinese-language business and wealth cognition skill pack that routes agent responses through mental models, business frameworks, compliance checks, and reusable templates for strategy, marketing, pricing, investment, management, and personal brand questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate structured Chinese-language guidance, checklists, tables, and templates for business strategy, revenue models, marketing copy, pricing, customer profiling, logistics, organization design, financial controls, personal branding, speeches, networking, and time management. Legal, tax, investment, and policy outputs should be treated as decision-support frameworks rather than professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a Claude local settings file that pre-approves broad reads of Windows drives and user files.

Mitigation: Review or remove artifact/.claude/settings.local.json before installation, and grant file-read permissions only for the specific workspace needed.

Risk: Legal, tax, investment, and China-specific policy outputs may be mistaken for professional advice.

Mitigation: Use the output as a general framework, verify primary sources, and consult licensed professionals before making regulated or high-impact decisions.

Risk: Policy and platform-rule guidance can become outdated.

Mitigation: Require current source checks and record the retrieval date when using this skill for policy, regulatory, or platform-rule analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhc2026/skills/caifurenzhicaozuoxitong)
- [Artifact README](artifact/README.md)
- [Skill entrypoint](artifact/SKILL.md)
- [Mental model quick reference](artifact/参考/思维模型速查表.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or structured Chinese text, often with checklists, tables, and reusable templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output; policy and platform-rule guidance is expected to include a retrieval date.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, release metadata, README version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
