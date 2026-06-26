## Description: <br>
Monitor token usage and estimated costs across OpenClaw agents with budget alerts and optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neal-collab](https://clawhub.ai/user/neal-collab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to produce cost reports, budget warnings, and optimization guidance for OpenClaw agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose usage and cost metadata across multiple agents. <br>
Mitigation: Install it only where the monitoring agent is allowed to access that metadata, and review alert channels and budget thresholds before enabling automated reports. <br>
Risk: Cost estimates can be inaccurate when model pricing, caching behavior, or custom rates differ from the reference values. <br>
Mitigation: Confirm current provider pricing and update custom rates before relying on reports or budget projections. <br>
Risk: Optimization recommendations may change model choice, caching, heartbeat intervals, pruning, or session reset behavior. <br>
Mitigation: Review each recommendation before applying it, especially in workflows where quality, latency, or retention requirements matter. <br>


## Reference(s): <br>
- [Agent Cost Monitor on ClawHub](https://clawhub.ai/neal-collab/agent-cost-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables, budget alerts, recommendations, and optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates depend on available usage metadata, current model pricing, caching behavior, and user-defined budget thresholds.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
