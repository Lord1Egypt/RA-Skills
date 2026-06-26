## Description: <br>
Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabrielsubtil](https://clawhub.ai/user/gabrielsubtil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to apply concise, pragmatic coding standards, avoid over-engineering, and verify code changes before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to edit related files beyond the initially requested file. <br>
Mitigation: Keep work under version control and set explicit file or scope limits when narrow changes are required. <br>
Risk: The skill references validation scripts from other local skill folders that are not bundled with this release. <br>
Mitigation: Review any referenced local validation scripts before allowing an agent to run them. <br>


## Reference(s): <br>
- [Clean Code on ClawHub](https://clawhub.ai/gabrielsubtil/clean-code) <br>
- [Publisher profile: gabrielsubtil](https://clawhub.ai/user/gabrielsubtil) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt agents to inspect related files, summarize validation output, and ask before fixing validation findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
