## Description:

Structures ambiguous business process requests into a workflow handoff, packages the result as a ClawHub skill asset, and guides publication to the ClawHub resource center.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow owners use this skill to turn unclear business-process requirements into structured steps, then package and publish the resulting handoff as a searchable ClawHub resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow handoffs may contain confidential business details, credentials, customer data, or internal-only procedures before publication.

Mitigation: Review and redact the handoff before packaging or publishing it to ClawHub.

Risk: Publishing an under-specified workflow can create a low-value or misleading reusable asset.

Mitigation: Complete the clarification, step extraction, risk review, rule generation, and user confirmation stages before packaging.

Risk: A malformed skill folder or conflicting slug can cause publication failure.

Mitigation: Run the documented dry run, verify the folder layout, and confirm slug uniqueness before publishing.

## Reference(s):

- [Workflow handoff description](artifact/references/DESCRIPTION.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/collab-workflow-ingest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a workflow handoff, a skill-shaped folder layout, ClawHub publish commands, and validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
