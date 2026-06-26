## Description: <br>
Daily Workflow Manager helps English-speaking developers start work, check in before breaks, and end sessions by maintaining local project documentation for AI-to-AI handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to preserve local project state across work sessions by creating, reading, and updating handoff documentation and workflow configuration files at session boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project handoff notes may capture secrets, credentials, private personal data, or confidential project details if the user includes them. <br>
Mitigation: Review Docs/ and .workbuddy/ changes before sharing or committing them, and avoid storing tokens, credentials, private personal data, or confidential details in handoff notes. <br>
Risk: Generic trigger phrases can cause the agent to update workflow files at unintended times. <br>
Mitigation: Choose low-collision custom trigger phrases in .workbuddy/daily-workflow-config.json and review changed workflow files after each session boundary. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation updates, JSON configuration, and concise session summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local Docs/ handoff files and .workbuddy/daily-workflow-config.json; no network or credential use is evidenced.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
