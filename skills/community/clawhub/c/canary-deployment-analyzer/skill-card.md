## Description: <br>
Analyze canary deployments by comparing metrics between canary and baseline. Provide data-driven promotion/rollback recommendations based on error rates, latency percentiles, and custom business metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill during progressive delivery decisions to compare canary and baseline health signals and decide whether to promote, hold, or roll back a release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require monitoring, cloud, or Kubernetes credentials to collect deployment metrics and logs. <br>
Mitigation: Use least-privilege, preferably read-only credentials and verify the target account, cluster, namespace, and deployment labels before running commands. <br>
Risk: Promotion or rollback recommendations could affect production availability if applied automatically. <br>
Mitigation: Treat recommendations as human-reviewed decision support rather than automatic deployment actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/canary-deployment-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendation-oriented canary analysis for human review before promotion or rollback.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
