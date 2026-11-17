## Description:

Helps detect when AI agent skills silently mutate across inheritance chains before audit scope becomes stale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to assess skill lineage, measure capability drift between versions, classify mutations, and decide whether a re-audit is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to use curl or Python against user-specified skill versions or marketplace lineage data.

Mitigation: Review proposed commands and target URLs before execution, and scan any retrieved skill artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/evolution-drift-detector)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown drift analysis report with lineage, per-generation diff summary, capability score, mutation classification, and re-audit recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3 when an agent inspects user-specified skill versions or marketplace lineage data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
