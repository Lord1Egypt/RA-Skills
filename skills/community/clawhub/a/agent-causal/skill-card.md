## Description: <br>
Agent Causal Decision Tool helps agents decide whether to ship, keep running, or roll back product experiments by returning structured decisions, statistics, and audit trails for A/B tests, Bayesian tests, Difference-in-Differences, cohort analysis, and sequential early stopping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhumorris](https://clawhub.ai/user/zhumorris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data scientists, and product teams use this skill to run defensible experiment analysis from local data or PostHog inputs and produce ship, continue, reject, or escalate recommendations with supporting statistics and audit details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PostHog connector use can expose experiment data or credentials if broad API tokens are used. <br>
Mitigation: Use a read-only PostHog token with minimal scopes and provide credentials through environment variables or a local config file. <br>
Risk: Saved analysis history can persist sensitive experiment data on shared machines. <br>
Mitigation: Avoid --save unless the audit trail is needed and periodically remove ~/.agent-causal/history.db in shared environments. <br>
Risk: Installing or running the wrong package version can undermine reproducibility. <br>
Mitigation: Install only from the intended GitHub release and confirm the release version before deployment. <br>
Risk: Automated experiment recommendations can be misleading when inputs have low traffic, weak assumptions, or inconclusive statistics. <br>
Mitigation: Review warnings, limitations, and audit trails before acting on ship, reject, or targeted rollout decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhumorris/agent-causal) <br>
- [Agent Causal source repository](https://github.com/ZhuMorris/agent-causal-decision-tool) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON decision outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include decision labels, statistical summaries, warnings, limitations, audit summaries, connector metadata, and optional local history records.] <br>

## Skill Version(s): <br>
0.10.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
