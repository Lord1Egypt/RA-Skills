## Description:

零售与门店经营专家 routes pasted retail and store-operation tables to one of 17 reconciliation checks and returns line-referenced, reproducible conclusions or states which required columns are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Retail, store-operations, finance, and audit users can use this skill to check pasted tabular materials for settlement, rebate, margin, inventory-transfer, night-audit, prepaid-card, and membership-liability issues. It is designed to avoid conclusions when required headers or data are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive retail, finance, or store-operation tables.

Mitigation: Use only approved business data, remove unnecessary sensitive fields, and run it in an environment appropriate for local processing of those tables.

Risk: The release under-discloses a persistent five-use counter and subscription gate.

Mitigation: Review the five-use limit, local usage-counter behavior, and subscription terms before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-retail-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON reconciliation results, including selected sub-skill, sub-skill name, findings, missing-field notices, and line-referenced conclusions when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through Node.js commands; JSON mode returns {subSkill, subSkillName, result}.]

## Skill Version(s):

1.0.10 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
