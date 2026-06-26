## Description: <br>
Automatically create a new OpenClaw agent, translate its name, and initialize its persona/system prompt based on user requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freesaber](https://clawhub.ai/user/freesaber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn a natural-language role request into an independent peer agent with a generated ID, display name, persona prompt, and initialized workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent OpenClaw agents and changes local OpenClaw state. <br>
Mitigation: Review the generated agent ID, display name, workspace path, and full persona prompt before execution, and back up ~/.openclaw/openclaw.json. <br>
Risk: Persona text may place sensitive or inappropriate instructions into the new agent's memory. <br>
Mitigation: Do not include secrets in persona text and review the prompt before it is injected. <br>
Risk: The documented Windows PowerShell path references a script that is not included in the artifact. <br>
Mitigation: Do not use the Windows PowerShell path unless the missing script is supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freesaber/agent-creator-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style guidance with inline shell commands and generated persona text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent OpenClaw agents, updates local OpenClaw configuration, and injects the generated persona prompt into the new agent.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
