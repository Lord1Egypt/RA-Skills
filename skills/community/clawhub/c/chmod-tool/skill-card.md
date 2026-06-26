## Description: <br>
Change file permissions using symbolic or numeric modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent propose or run local file-permission changes with chmod-style modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing permissions on sensitive system, credential, or account files can weaken access controls. <br>
Mitigation: Use explicit paths and review each proposed permission change before execution. <br>
Risk: The documentation describes symbolic and recursive chmod examples, but the bundled helper appears to accept only octal modes for one file. <br>
Mitigation: Prefer octal modes with a single explicit file path unless the implementation is updated and retested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/chmod-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper accepts an octal mode and one file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
