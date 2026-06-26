## Description: <br>
Track OpenClaw agent costs. Check daily/weekly spending and model breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShallIfy](https://clawhub.ai/user/ShallIfy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use ClawCost to summarize local agent spending, daily budgets, balance status, and model cost breakdowns from their own OpenClaw session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs, which may contain usage and spending details. <br>
Mitigation: Install only if local cost summarization is desired, and avoid sharing generated summaries when they expose sensitive usage details. <br>
Risk: Setting a balance writes local state at ~/.clawcost/config.json. <br>
Mitigation: Review or remove the local configuration file if balance tracking is no longer needed. <br>


## Reference(s): <br>
- [Model Pricing Reference](references/pricing.md) <br>
- [ClawCost on ClawHub](https://clawhub.ai/ShallIfy/clawcost) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the local script, rendered by the agent as concise text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; reads local OpenClaw session logs and can write a local balance configuration file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
