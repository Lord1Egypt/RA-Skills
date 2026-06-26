## Description: <br>
Plan and execute dark launches with feature flags, performance monitoring, and gradual exposure rollouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and SREs use this skill to plan dark launches, inspect feature flag integration points, monitor hidden production code paths, and prepare controlled promotion or rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated kubectl, rollout, or rollback snippets could affect production traffic if applied to the wrong cluster, namespace, or feature key. <br>
Mitigation: Treat commands as drafts and confirm cluster context, namespace, feature key, rollback behavior, and release-owner approval before applying them. <br>
Risk: Promotion decisions can be misleading if feature-specific monitoring is missing or not comparable to a baseline. <br>
Mitigation: Confirm the required dashboards, alerts, feature labels, and success gates before promoting a dark-launched feature. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Kubernetes YAML, JSON, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are drafts for human review before any production rollout, promotion, or rollback action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
