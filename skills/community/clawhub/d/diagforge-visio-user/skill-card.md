## Description: <br>
Bootstrap skill for DiagForge. Use this skill to onboard an agent into the DiagForge GitHub repository, understand the project structure, run the canonical cold-start smoke test, and begin working with the Visio-based drawing loop safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qweadzchn](https://clawhub.ai/user/qweadzchn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to enter the DiagForge repository with the correct read order, run the cold-start smoke test, and begin Visio-based figure reproduction work that can produce editable diagram assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to clone and run an external repository while using a sensitive VISIO_BRIDGE_TOKEN. <br>
Mitigation: Verify the repository before execution, review or pin the code being run, use an isolated workspace, and provide VISIO_BRIDGE_TOKEN with least privilege while keeping it out of logs, commits, screenshots, and prompts. <br>


## Reference(s): <br>
- [DiagForge GitHub repository](https://github.com/qweadzchn/DiagForge) <br>
- [ClawHub skill page](https://clawhub.ai/qweadzchn/diagforge-visio-user) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides repository onboarding, required tools, VISIO_BRIDGE_TOKEN handling, smoke-test execution, and expected Visio output files.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
