## Description: <br>
Automatically generates optimized Dockerfile templates for Node.js, Python, Go, and Java applications with multi-stage build and container best-practice guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to draft Dockerfiles for common application stacks, including Node.js, Python, Go, and Java. It helps produce starting templates with multi-stage build patterns and configurable image versions or ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Dockerfiles may include image versions, ports, or commands that do not match the target application. <br>
Mitigation: Review the generated Dockerfile before building or deploying it. <br>
Risk: Untrusted values for image versions or ports can change the resulting Dockerfile text. <br>
Mitigation: Use trusted configuration values and pin image versions before building containers. <br>


## Reference(s): <br>
- [Dockerfile Generator ClawHub release](https://clawhub.ai/HonestQiao/dockerfile-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Dockerfile code blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Dockerfile templates should be reviewed before building or deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
