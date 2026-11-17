## Description:

Maps data retention periods, storage locations, cleanup ownership, expiry handling, and improvement suggestions for governance, privacy, and audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy teams, governance teams, and auditors use this skill to turn provided data asset, storage location, and retention requirement details into reviewable retention maps, risk notes, and cleanup recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may contain personal data, secrets, or sensitive storage-location details.

Mitigation: Redact unnecessary personal data and secrets before use, and limit inputs to the details needed for the retention review.

Risk: Retention guidance may be mistaken for formal compliance or legal advice.

Mitigation: Treat outputs as governance drafts and route them through qualified privacy, compliance, or legal review before adoption.

Risk: Incomplete source material can produce an incomplete or misleading retention map.

Mitigation: Review the generated pending-confirmation items and resolve missing data before using the map for decisions.

Risk: Generated cleanup checklists could be over-applied to external systems.

Mitigation: Use the skill in review or dry-run mode first, and require human approval before any deletion, publication, configuration, or external-system change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/data-retention-mapper)
- [README](artifact/README.md)
- [Structured Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Example Input](artifact/examples/example-input.md)
- [Example Output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report or JSON object, with optional inline shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local user-provided input and can print to stdout or write a chosen local output file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
