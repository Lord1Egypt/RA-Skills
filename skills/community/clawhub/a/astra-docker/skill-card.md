## Description: <br>
Interact with Astra's Docker container workspace by executing commands and reading or writing files at /workspace inside the astra-env container. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walniek](https://clawhub.ai/user/walniek) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to operate inside an Astra Docker workspace, run commands in the astra-env container, and write files under /workspace when the container is trusted and available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent powerful sudo Docker command access to the astra-env container. <br>
Mitigation: Install only when the Astra Docker container is trusted and Docker command authority is acceptable for the environment. <br>
Risk: The security summary warns that Docker commands are built unsafely and should be reviewed before use. <br>
Mitigation: Prefer a revised version that uses argument-based execution, validates paths under /workspace, avoids host shell interpolation, and confirms state-changing commands or file writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/walniek/astra-docker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Structured tool results with success status, stdout, stderr, errors, or file-write confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and file writes target the astra-env Docker container workspace at /workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
