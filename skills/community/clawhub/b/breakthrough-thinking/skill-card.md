## Description: <br>
Breakthrough Thinking helps an AI recover from stalled work by switching to one mental model at a time, applying it directly, and continuing until the problem is solved or bounded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1204TMax](https://clawhub.ai/user/1204TMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an AI assistant break out of repeated failures or unproductive retry loops by selecting and applying a different reasoning framework. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on ordinary retry or frustration phrases because its trigger conditions are broad. <br>
Mitigation: Prefer explicit invocation or narrow the trigger phrases if the agent environment supports trigger customization. <br>
Risk: The skill can produce revised reasoning guidance that may still be incorrect or misleading. <br>
Mitigation: Require evidence for completion claims and review the proposed next action before relying on it. <br>


## Reference(s): <br>
- [107 Mental Models for Breaking Through](references/mental-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with a compact breakthrough status block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a dead-end summary, selected model, approach, result, and next step.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
