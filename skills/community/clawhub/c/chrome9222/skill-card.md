## Description: <br>
Launches Chrome with remote debugging enabled on port 9222 for local debugging and development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aizzaua](https://clawhub.ai/user/aizzaua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to start a local Windows Chrome instance with remote debugging on port 9222 for browser automation, inspection, and development tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill force-closes existing Chrome windows before launch, which can interrupt active browsing sessions or unsaved work. <br>
Mitigation: Save browser work and close Chrome intentionally before invoking the skill. <br>
Risk: Remote debugging on port 9222 can expose browser control in the debug-enabled profile. <br>
Mitigation: Use only in a trusted local development environment and avoid sensitive accounts in the debug profile. <br>
Risk: The launch behavior is tied to a Windows Chrome path and taskkill command. <br>
Mitigation: Confirm the local Chrome installation path and Windows execution context before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aizzaua/chrome9222) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Text status message after executing local Chrome launch commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts Chrome with --remote-debugging-port=9222 and a custom user data directory, after closing existing Chrome processes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
