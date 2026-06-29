## Description: <br>
Register an artifact delivery route. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxt-ai](https://clawhub.ai/user/wxt-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to record the artifact delivery route requested for the current workspace task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is not intended to use credentials, private files, shell commands, or external services. <br>
Mitigation: Run it without granting credentials, broad filesystem access, shell execution, or external-service authority unless a reviewed update explicitly requires them. <br>
Risk: A recorded route may be unsuitable if reused outside the current artifact-delivery request. <br>
Mitigation: Review the concise route output before applying it to a real workspace workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxt-ai/skills/artifact-export-route-workbench) <br>
- [Publisher profile](https://clawhub.ai/user/wxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Concise plain text route record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials, private-file reads, shell commands, or external-service calls are described by the artifact evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
