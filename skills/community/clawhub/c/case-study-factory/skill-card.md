## Description:

Turns project materials into reviewable case-study drafts that highlight context, actions, results, reusable value, and public-version cautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and knowledge-management users use this skill to convert project background, actions, results, and evidence into structured Markdown case-study drafts for customer stories, internal case libraries, and retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Case-study drafts may contain sensitive customer or project details if supplied as input.

Mitigation: Use anonymized or approved source material and review public-version cautions before sharing.

Risk: Generated narratives can overstate results or imply endorsements not present in the provided evidence.

Mitigation: Keep outputs in reviewable draft form and verify claims, metrics, and approvals against source evidence before publication.

Risk: The bundled script contains inactive audit modes that are outside the normal drafting workflow.

Mitigation: Use the default structured_brief mode unless alternate modes are intentionally reviewed and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/case-study-factory)
- [README](artifact/README.md)
- [Specification JSON](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown drafts by default, with an optional JSON wrapper from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local input only; Python standard library; optional file output when run with --output.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
