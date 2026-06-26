## Description: <br>
AI debugging assistant that combines a 7-step debugging method, root-cause analysis, automated test-case generation, error pattern recognition, and cross-language debugging guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when debugging code errors, crashes, failed tests, API issues, memory leaks, or performance problems. It guides the agent through reproduction, error capture, root-cause analysis, fixes, validation, and prevention steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested debug or test commands may run project scripts that modify data, call external services, or touch credentials. <br>
Mitigation: Review each command and run it in a safe development environment before allowing an agent to execute it. <br>
Risk: Automated fix suggestions and generated tests may be incomplete or incorrect for the target codebase. <br>
Mitigation: Inspect proposed code changes and verify them with the project's test suite before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and debugging report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Suggested debug and test commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
