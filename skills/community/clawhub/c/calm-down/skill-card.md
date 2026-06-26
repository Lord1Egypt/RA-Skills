## Description: <br>
Detects frustration signals during AI conversations and appends a brief grounding reminder after addressing the user's request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kencan666-ai](https://clawhub.ai/user/kencan666-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to have an agent notice repeated frustration directed at the AI and add one short grounding reminder after the task response. It is intended to reduce escalation without replacing the concrete answer or fix the user requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The grounding reminder can be unwanted or distracting during frustrated conversations. <br>
Mitigation: Use the skill only where this behavior is acceptable, keep the reminder brief, and allow users to disable or ignore it. <br>
Risk: Reference examples could encourage triggering from project stress or late-night timing without enough AI-directed frustration. <br>
Mitigation: Apply the artifact's stated trigger boundary: require frustration signals directed at the AI and do not trigger on external situations alone. <br>
Risk: A calming reminder could interfere with the user's actual task if it appears too early. <br>
Mitigation: Follow the skill's response order by solving the request first, then acknowledging briefly, then appending one grounding line at the end. <br>


## Reference(s): <br>
- [Signal Examples](references/signal-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/kencan666-ai/calm-down) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text appended to the agent response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One brief reminder after the requested task is addressed; no code execution, credentials, persistence, or external transmission requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
