## Description: <br>
Agent observability — monitors tool invocations, LLM calls, token usage, costs, and anomalies with pluggable alerts and a real-time dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fiddyrod](https://clawhub.ai/user/fiddyrod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw agent health, tool reliability, token usage, cost trends, anomalies, and alert delivery during normal agent operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw session transcripts that may include sensitive tool arguments, errors, file paths, and usage data. <br>
Mitigation: Install only where local transcript monitoring is acceptable, and restrict access to the workspace and generated SQLite metrics database. <br>
Risk: Configured Discord or other webhook alerts can send sanitized alert text to an external destination. <br>
Mitigation: Use a dedicated trusted webhook, keep config.yaml out of source control and shared workspaces, and rotate the webhook if it may have been exposed. <br>
Risk: The dashboard frontend can load React and Babel from public CDNs, which may not fit air-gapped or high-security environments. <br>
Mitigation: Serve required frontend assets locally in restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fiddyrod/claw-reliability) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local dashboard/report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite-backed metrics, CLI summaries, anomaly reports, alert configuration, and localhost dashboard views.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
