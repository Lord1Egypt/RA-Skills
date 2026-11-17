## Description:

Generates a ten-item AI vendor due-diligence checklist and scores responses against a configurable threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and legal teams use this skill to request evidence on ten AI vendor governance topics and screen responses before contract review. A person reviews any gaps and makes the final decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described JSON-input workflow is not implemented in the local CLI.

Mitigation: Use the --template or --score CLI arguments instead of relying on JSON input.

Risk: The skill declares WebFetch access that its local checklist does not use.

Mitigation: Limit tool permissions to the access needed for local execution where supported.

Risk: A checklist score alone cannot establish vendor compliance.

Mitigation: Have procurement and legal reviewers check supporting evidence and contract terms before approval.

## Reference(s):

- [AI Vendor Checklist release on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-vendor-checklist)
- [Skill README](README.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON]

**Output Format:** [Markdown checklist or text/JSON score report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional checklist file; scores below the threshold return exit code 1. CLI output is primarily Chinese.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
