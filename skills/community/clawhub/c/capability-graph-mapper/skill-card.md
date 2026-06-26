## Description: <br>
Helps map the composite permission surface across AI agent skill dependency chains and identify emergent capabilities created by skill combinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to analyze installed agent skills, map permission combinations, and identify risky emergent capabilities before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input manifests or configuration files may contain secrets or other unnecessary sensitive data. <br>
Mitigation: Remove unnecessary secrets before providing manifests or configurations to the agent. <br>
Risk: Privilege surface scores and flagged chains are review guidance rather than a complete security guarantee. <br>
Mitigation: Validate findings against the actual skill manifests and manually review high-risk combinations before deployment. <br>


## Reference(s): <br>
- [Capability Graph Mapper release page](https://clawhub.ai/andyxinweiminicloud/capability-graph-mapper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with a permission matrix, risk flags, privilege surface score, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include delta analysis when evaluating a new skill addition.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
