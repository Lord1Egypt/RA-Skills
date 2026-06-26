## Description: <br>
A text-based calendar and scheduling application. Use strictly for CLI-based calendar management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CLI users use this skill to have an agent query a local calcurse calendar and propose commands for adding appointments or todos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar queries can reveal personal schedule details to the agent. <br>
Mitigation: Only use the skill when calendar access is intended and review queried date ranges before execution. <br>
Risk: Add commands can create local appointments or todos. <br>
Mitigation: Review date, time, duration, description, and todo priority before allowing updates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local calcurse binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
