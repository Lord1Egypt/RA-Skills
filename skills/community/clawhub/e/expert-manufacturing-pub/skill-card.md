## Description:

制造与生产管理专家 routes pasted manufacturing or operations tables to one of seven local checkers and returns line-referenced, recalculable findings or missing-column guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, operations, finance, maintenance, and compliance users can paste table data to check settlement, maintenance cost, monthly self-check, outsourced processing, safety-production-fee, and related records. The skill is best used for narrow table consistency checks, not as audit, legal, or compliance assurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a suspicious verdict because the package writes an under-disclosed persistent local trial-use counter in the user's home directory.

Mitigation: Install only if a local usage counter is acceptable, and disclose that trial counting is stored locally before users run the command.

Risk: The security scan notes that results are narrow table consistency checks, not compliance or audit assurance.

Mitigation: Use the findings as review aids only; require qualified human review and source-document verification before operational, audit, or compliance decisions.

Risk: The security scan notes that the manufacturing-branded package includes an unrelated water-supply hygiene checker.

Mitigation: Review the sub-skill list before deployment and instruct users to force the intended sub-skill when mixed-scope routing would be confusing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-manufacturing-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact expert manifest](artifact/scripts/engine/expert-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Plain text or JSON findings with source line references, recalculation details, and insufficient-input messages when required fields are missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes by table headers; command-line execution can list sub-skills, run a sample, accept pasted text, or force a sub-skill.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
