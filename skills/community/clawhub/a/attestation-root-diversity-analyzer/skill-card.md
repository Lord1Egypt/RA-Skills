## Description:

Helps measure the concentration of trust roots in a skill's attestation graph, identifying monoculture risk where a single compromised root can invalidate a chain that appears to have multiple validators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and marketplace operators use this skill to assess whether a skill's attestation trust graph depends too heavily on one root, publisher, or organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis can be incomplete or misleading when attestation graph data or organizational relationship data is missing.

Mitigation: Use the report as advisory guidance and verify conclusions against complete attestation records and independent organizational ownership data.

Risk: The release declares curl and python3 requirements even though the inspected Markdown artifact does not exercise them.

Mitigation: Review future releases before installation if executable helpers are added or those requirements become active.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/attestation-root-diversity-analyzer)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown root diversity report with text-based trust graph analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report depends on the completeness and accuracy of the provided attestation graph and organizational relationship data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
