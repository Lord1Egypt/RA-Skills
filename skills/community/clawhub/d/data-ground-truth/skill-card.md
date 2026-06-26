## Description: <br>
Before presenting numbers in reports or recommendations, verify facts and check values against industry baselines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, analysts, and developers use this skill to check factual claims and benchmark business or performance metrics before including numbers in reports, recommendations, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends claims and metric values to AgentUtil external services. <br>
Mitigation: Use it only when sharing the specific claims, category identifiers, and metric values with those services is acceptable. <br>
Risk: Confidential, personal, regulated, or highly sensitive business data could be exposed if included in claims or metric values. <br>
Mitigation: Avoid submitting sensitive data unless that disclosure has been approved for the use case. <br>
Risk: Queries may incur costs after the free tiers described by the artifact. <br>
Mitigation: Review expected query volume and pricing before using the skill in recurring workflows. <br>


## Reference(s): <br>
- [AgentUtil](https://agentutil.net) <br>
- [Verify API](https://verify.agentutil.net/v1/verify) <br>
- [Norm check API](https://norm.agentutil.net/v1/check) <br>
- [Norm batch API](https://norm.agentutil.net/v1/batch) <br>
- [Norm categories API](https://norm.agentutil.net/v1/categories) <br>
- [ClawHub release page](https://clawhub.ai/CutTheMustard/data-ground-truth) <br>
- [Publisher profile](https://clawhub.ai/user/CutTheMustard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, analysis, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown guidance with optional inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verdicts, freshness notes, percentiles, assessment labels, and baseline ranges returned by external services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
