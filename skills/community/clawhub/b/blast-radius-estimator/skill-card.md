## Description: <br>
Helps estimate the blast radius when an AI agent skill turns malicious after widespread adoption by analyzing inheritance chains, dependency graphs, and adoption trends to project how many agents could be affected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to estimate downstream exposure if an AI agent skill becomes compromised. It helps prioritize monitoring and response by tracing direct adopters, inherited dependents, adoption velocity, version pinning, and capability composition risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blast-radius estimates may be incomplete or approximate when marketplace adoption data, dependency relationships, or update behavior are missing. <br>
Mitigation: Verify marketplace and adoption data before using the report for prioritization or incident response decisions. <br>
Risk: The skill does not need credentials, but users might provide unnecessary sensitive information while investigating a marketplace asset. <br>
Mitigation: Avoid providing credentials or secrets; use public identifiers, asset URLs, hashes, slugs, or non-sensitive marketplace metadata. <br>


## Reference(s): <br>
- [Blast Radius Estimator on ClawHub](https://clawhub.ai/andyxinweiminicloud/blast-radius-estimator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown report with counts, an inheritance tree, adoption trend, worst-case projection, urgency rating, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates are approximate and depend on available adoption, dependency, and update behavior data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
