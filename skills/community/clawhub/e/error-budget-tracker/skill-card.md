## Description: <br>
Track SLO error budgets across services. Calculate remaining budget from SLI metrics, alert on budget burn rate, recommend development vs reliability investment, and generate error budget reports for stakeholder review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and service owners use this skill to calculate SLO error budget status, evaluate burn rates, draft Prometheus-based reporting steps, and decide when to ship features or invest in reliability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prometheus queries or generated SLO calculations may be incorrect for a specific service or metric schema. <br>
Mitigation: Review queries and calculations before running them, and use read-only monitoring credentials. <br>
Risk: Generated slo.yaml or policy changes may affect reliability governance decisions. <br>
Mitigation: Protect SLO configuration and policy updates through normal code review and stakeholder approval. <br>
Risk: The skill has catalog tags for crypto and purchases, but the security evidence says it should not receive financial authority. <br>
Mitigation: Do not grant wallet, payment, purchase, or unrelated financial authority based on this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/error-budget-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, bash, Python, and report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed SLO reporting guidance and policy drafts; no automatic monitoring changes are performed by the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
