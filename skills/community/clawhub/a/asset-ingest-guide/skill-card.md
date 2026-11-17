## Description:

Reference skill demonstrating TaskFlow + ClawHub tooling for publishing digital content to the resource hub.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and new contributors use this reference skill to understand the smallest viable skill folder shape and a sample TaskFlow plus ClawHub prepare, validate, publish, and verify workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the referenced publishing workflow may upload or register content outside the local workspace.

Mitigation: Review actual TaskFlow and ClawHub commands before running them, especially publish or registration steps.

Risk: The artifact is a minimal reference guide, so it may omit environment-specific validation details needed for a real release.

Mitigation: Run the prepare, validate, publish, and verify steps against the target workspace and inspect their results before relying on the release.

## Reference(s):

- [Asset Ingest Workflow Reference](references/ASSET-INGEST-WORKFLOW.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/asset-ingest-guide)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-only skill; no executable scripts are included in the artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
