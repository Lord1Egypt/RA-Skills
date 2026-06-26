## Description: <br>
Routes OpenClaw tasks across cheap, default, pro, and ultra model tiers, with optional manual overrides, sub-agent recommendations, and local briefing to reduce token use and cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarAtheris](https://clawhub.ai/user/StarAtheris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to choose a cost-appropriate model tier for each OpenClaw task, keep routine work on cheaper models, and escalate heavier work through sub-agents with a compact brief when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad router prompts or large private context may be analyzed for routing or summarized before being passed to another model or sub-agent. <br>
Mitigation: Use the router only on content intended for routing, review generated briefs before escalation, and disable auto routing or use manual overrides when sensitive context should stay on the main agent. <br>
Risk: Editable rules and local feedback state can change model thresholds, routing decisions, and cost behavior over time. <br>
Mitigation: Review rules.json and state.json before deployment and periodically after feedback commands are used, especially in cost-sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StarAtheris/arya-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, shell commands, json] <br>
**Output Format:** [JSON decisions and text guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits a routing level, model identifier, score, reasons, actions, response policy, and mode; the briefing helper emits compact plain text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
