## Description: <br>
Decision recording + result tracking skill <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to record important decisions, rationale, alternatives, expected outcomes, and later result reviews in a local decision journal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision notes and metadata are saved locally, which can persist sensitive decision content beyond the immediate session. <br>
Mitigation: Avoid recording secrets or highly confidential decisions, and review the generated local files before keeping or sharing them. <br>
Risk: Decision titles and file paths may be emitted as local event records. <br>
Mitigation: Use non-sensitive titles and confirm that local event records are appropriate for the workspace. <br>
Risk: The 30-day review behavior depends on scheduling support in the agent environment. <br>
Mitigation: Confirm that the review mechanism is actually scheduled, and verify how to remove or update scheduled reviews. <br>
Risk: Broad trigger phrases may cause the skill to record decisions when the user did not intend persistent logging. <br>
Mitigation: Confirm intent before persisting a decision log entry when the trigger context is ambiguous. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown decision log files with JSON local event records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local decision notes under memory/decisions and local decision event records under events when the agent environment supports those paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
