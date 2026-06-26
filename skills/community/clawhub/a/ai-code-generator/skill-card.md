## Description: <br>
AI code generator using Plan-and-Solve + ReAct for generating complete, runnable code from requirements and specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banxian87](https://clawhub.ai/user/banxian87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn natural language requirements into generated project files, tests, documentation, and setup guidance for application development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code may contain incorrect logic, unsafe dependencies, or insecure defaults. <br>
Mitigation: Review generated files, dependencies, and setup commands before saving, installing, or running them. <br>
Risk: Requirements prompts may expose secrets, private keys, or sensitive proprietary details to the configured LLM backend. <br>
Mitigation: Do not include secrets or sensitive proprietary information in requirements unless the model backend is trusted and approved for that data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JavaScript object containing generated file contents, analysis, architecture, and Markdown next-step instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code and dependency instructions should be reviewed before saving, installing, or running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
