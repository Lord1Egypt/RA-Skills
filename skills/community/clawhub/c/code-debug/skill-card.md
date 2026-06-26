## Description: <br>
Diagnose failures in the current local codebase and produce the smallest defensible fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose reported errors, crashes, failed tests, bad output, flaky behavior, and other local code failures, then identify the root cause and smallest defensible repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging may expose source files, logs, test output, and local error details to the agent. <br>
Mitigation: Use the skill in trusted repositories, avoid placing secrets in debug logs or files, and review any proposed patch before applying it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with root-cause analysis, repair guidance or patches, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a minimal reproduction, impact scope, and validation method when supported by the debugging evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
