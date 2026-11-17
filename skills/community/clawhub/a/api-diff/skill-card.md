## Description:

Compares two OpenAPI 3.x or Swagger 2.0 specifications and generates a changelog of breaking and non-breaking API changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API platform teams use this skill to compare API versions, identify breaking changes, and produce changelogs for release review or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted API specification content may affect how Markdown reports render when published.

Mitigation: Prefer JSON output for automated pipelines or sanitize generated Markdown before sharing it externally.

Risk: Diff classifications may influence API release decisions.

Mitigation: Review generated changelogs before using them to approve or block a release.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Text, JSON, or Markdown changelog output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can show only breaking changes or return a nonzero CI exit status when breaking changes are found.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
