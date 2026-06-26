## Description: <br>
Real-time AI agent safety monitoring, anomaly detection, and constraint enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect agent event logs, configure safety rules, and surface alerts for rate limits, tool allowlists, budget caps, scope checks, and behavioral anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact describes real-time enforcement, dashboard, webhook, and pause or kill behavior that is not fully present in the reviewed files. <br>
Mitigation: Use it only as an offline log analyzer unless those enforcement and dashboard components are added and reviewed. <br>
Risk: The release is tagged as requiring wallet and sensitive credential capabilities. <br>
Mitigation: Do not provide wallets, secrets, or production credentials unless a separate review confirms the artifact needs and protects them. <br>
Risk: Security evidence marks the release as suspicious because capability claims exceed the implemented behavior. <br>
Mitigation: Run it in a constrained environment with test logs and manually review alerts before relying on operational decisions. <br>


## Reference(s): <br>
- [Safety Rules Reference](references/rules-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/evezart/agent-safety-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and Python command examples; monitor execution emits JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires reviewed local event logs and YAML rule configuration; security evidence says this release should be treated as a prototype offline log analyzer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
