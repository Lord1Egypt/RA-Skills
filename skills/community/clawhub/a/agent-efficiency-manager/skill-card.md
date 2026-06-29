## Description: <br>
Agent Efficiency Manager analyzes OpenClaw agent configurations to estimate token overhead, identify redundant skills, recommend SkillHub additions, track efficiency trends, and prepare optimization reports or notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw agent skill configurations, reduce prompt-token overhead, and generate recommendation reports for ongoing agent optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw agent configuration, which may expose agent names, installed skills, and optimization context. <br>
Mitigation: Run it only against intended local configuration files and keep generated reports local unless sharing is explicitly approved. <br>
Risk: Optional webhook or document-report delivery may publish recommendations outside the local environment. <br>
Mitigation: Use only trusted webhook destinations and review report contents before enabling push notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/perrykono-debug/agent-efficiency-manager) <br>
- [Metrics Definitions](references/metrics_definitions.md) <br>
- [Optimization Patterns](references/optimization_patterns.md) <br>
- [Recommendation Logic](references/recommendation_logic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON reports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are advisory by default; configuration changes require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
