## Description: <br>
Code calls functions, classes, or methods that don't exist — either on project types or on third-party library APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to help agents verify project and third-party API symbols before writing or modifying code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect repository code, library documentation, or type definitions while checking whether symbols exist. <br>
Mitigation: Review any repository reads, proposed commands, and resulting edits under the normal project review process. <br>
Risk: The skill may propose small code changes when a referenced helper or API does not exist. <br>
Mitigation: Confirm suggested replacements against project source, official documentation, and type-checking results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvogt99/fabricated-symbols) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with optional inline code or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend repository search, documentation checks, type checking, or small explicit code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
