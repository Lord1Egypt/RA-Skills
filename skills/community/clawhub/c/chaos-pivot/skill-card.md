## Description: <br>
Prevents LLMs from sunk-cost pushing broken solutions. Triggers when an agent is stuck, looping, or failing repeatedly. Forces a Popperian falsification moment, then generates 3 constrained-chaotic alternative approaches and picks the best one. Loops like design thinking until solved or escalated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manecharo](https://clawhub.ai/user/Manecharo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent is repeating failed approaches, stuck in uncertainty, or taking more steps than expected. It guides the agent to declare the failed assumption, generate three divergent alternatives, test them for signal, and escalate with a clear diagnosis if repeated loops do not produce a viable path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: On high-stakes or irreversible tasks, the skill may prompt the agent to change strategy earlier than expected. <br>
Mitigation: Use additional human supervision and review the chosen pivot before executing actions with significant consequences. <br>
Risk: Structured alternatives can produce incorrect or misleading guidance if the agent treats weak signals as conclusive. <br>
Mitigation: Require the third-party audit step and verify that the selected approach still solves the original user goal. <br>


## Reference(s): <br>
- [Chaos Pivot ClawHub page](https://clawhub.ai/Manecharo/chaos-pivot) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Text] <br>
**Output Format:** [Markdown and structured text prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces internal reasoning checklists, alternative approach summaries, audit verdicts, and escalation guidance; it does not request credentials, persistence, or system access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
