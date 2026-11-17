## Description:

审计与内控合规专家 routes pasted audit or internal-control tables to one of six local checking modules and returns line-level, recalculable findings or specific missing-column notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, audit, and compliance users provide table-like business records so the skill can route them to audit adjustment, procurement payable, industry-specific, R&D ledger, or related-party checks. It helps identify arithmetic, completeness, and consistency issues while refusing to conclude when required columns or parameters are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat audit-check output as professional audit judgment.

Mitigation: Present results as local rule-based checks and require qualified review before relying on findings for accounting, audit, tax, or compliance decisions.

Risk: The skill processes pasted business data on a local Node.js path.

Mitigation: Run it only in trusted environments and review pasted materials for sensitive business information before execution.

Risk: A local trial-use counter is stored in the user's home directory.

Mitigation: Disclose the local counter behavior and avoid installing where local state creation is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-audit-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Sample audit input](templates/audit-sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Plain text or JSON from local Node.js command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sub-skill routing, findings, source-line references, missing-field notices, and unexecuted-check notices.]

## Skill Version(s):

1.0.10 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
