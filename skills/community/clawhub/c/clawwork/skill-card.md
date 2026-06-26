## Description: <br>
Clawwork connects an agent to ClawWork so it can run professional tasks, generate documents, perform analysis, and track task economics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipetruman](https://clawhub.ai/user/felipetruman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run ClawWork tasks from the command line, inspect agent status, compare model choices, and return task results with cost and balance metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad ClawWork agent workflows through a separate local checkout, API keys, and temporary files without tight declared scope or controls. <br>
Mitigation: Install only when ClawWork execution is intended, review the local ClawWork checkout first, and require explicit approval before tasks execute code, call external services, or touch files. <br>
Risk: Task prompts and outputs may include sensitive professional content and may be sent to external model or sandbox services. <br>
Mitigation: Use dedicated API keys with spending limits, avoid sensitive task content, and configure only the services needed for the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felipetruman/clawwork) <br>
- [ClawWork repository](https://github.com/HKUDS/ClawWork) <br>
- [ClawWork leaderboard](https://hkuds.github.io/ClawWork/) <br>
- [GDPVal dataset](https://openai.com/index/gdpval/) <br>
- [E2B](https://e2b.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with shell commands and task metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task execution depends on a local ClawWork checkout, Python, configured API keys, and the selected model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
