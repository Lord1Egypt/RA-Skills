## Description:

Formats CRediT author contribution statements from supplied author-role input for research manuscripts and collaborative projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, research administrators, and publication support teams use this skill to prepare contribution statements, document CRediT roles, and identify authorship inputs that need human review before manuscript submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated authorship order, fairness, or compliance language may be mistaken for an authoritative decision.

Mitigation: Use the output as a draft only and have the research team, institutional policy owner, or journal submission owner confirm author order, CRediT roles, and ICMJE compliance.

Risk: XML or structured contribution output may be accepted into journal or metadata systems without enough review.

Mitigation: Validate XML and structured fields against the target journal or metadata system before submission.

Risk: Incomplete author-role input can lead to incomplete or misleading contribution statements.

Mitigation: Collect missing author names, affiliations, corresponding-author flags, equal-contribution flags, and role codes before treating the output as final.

## Reference(s):

- [Authorship CRediT Gen on ClawHub](https://clawhub.ai/aipoch-ai/skills/authorship-credit-gen-1)
- [Audit Reference](artifact/references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, xml, shell commands, guidance]

**Output Format:** [Markdown guidance plus optional plain text, JSON, or XML contribution statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated statements to a user-specified output file; output should be reviewed before journal or metadata submission.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md lists 1.0 and tile.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
