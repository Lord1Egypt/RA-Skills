## Description: <br>
Security engineer skill for backend ACL structure, menu visibility control, and administrative access safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, and repair backend ACL paths, admin menu visibility, and controller permission wiring for WelineFramework admin features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ACL or menu changes can affect who can see or access administrative features. <br>
Mitigation: Review generated code and configuration changes and verify both permitted-role and denied-role behavior before deployment. <br>
Risk: Menu visibility alone may hide an admin surface without enforcing controller-level permission checks. <br>
Mitigation: Align menu source identifiers with controller permission annotations and validate denied access through the real admin path. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with code and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation evidence for allowed and denied admin access behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
