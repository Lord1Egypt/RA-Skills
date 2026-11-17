## Description:

Helps map composite permission surfaces across AI agent skill dependency chains by tracing individual skill capabilities and identifying emergent combined capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to review installed skill sets, map permission combinations, and identify emergent capability chains that need manual review before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad inputs may expose unnecessary private skill or workspace context during review.

Mitigation: Provide scoped skill manifests or specific skill names instead of broad private directories.

Risk: Composite-risk scores may be misread as proof of a confirmed vulnerability.

Mitigation: Treat scores as review guidance and manually confirm risky combinations before making deployment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with permission matrices, risk summaries, scores, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3 according to ClawHub metadata; no credential environment variables are declared.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
