## Description:

Helps estimate the blast radius when an AI agent skill turns malicious after widespread adoption by analyzing inheritance chains, dependency graphs, and adoption trends to project how many agents could be affected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

External developers, marketplace operators, and security reviewers use this skill to estimate potential exposure from a compromised agent skill. It helps prioritize monitoring and mitigation by reporting estimated direct and transitive impact, inheritance depth, adoption trend, version pinning posture, worst-case projection, urgency, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blast-radius estimates may be incomplete or imprecise when marketplace adoption, dependency, or update behavior data is unavailable.

Mitigation: Treat results as exposure estimates and corroborate them with platform telemetry, dependency manifests, and manual review before making incident decisions.

Risk: Real estimates may involve network lookups for marketplace or adoption data.

Mitigation: Run the skill only in environments where network access is expected and review outbound lookup behavior according to local policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with summary metrics, inheritance tree visualization, urgency rating, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on available adoption and dependency data and should be treated as potential exposure, not proof of compromise.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
