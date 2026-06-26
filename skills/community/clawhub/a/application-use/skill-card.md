## Description: <br>
Automate macOS desktop tasks by opening apps, clicking elements, filling forms, typing, scrolling, taking screenshots, and controlling applications through CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qdore](https://clawhub.ai/user/qdore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate macOS desktop workflows such as opening applications, clicking hinted UI elements, filling forms, scrolling, taking screenshots, and controlling Finder or browser sessions through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over macOS applications, forms, browser sessions, and Finder. <br>
Mitigation: Use it only with active supervision and require explicit confirmation before submissions, file changes, messages, purchases, or account actions. <br>
Risk: Desktop automation may expose or type sensitive information through open windows or focused fields. <br>
Mitigation: Close sensitive windows before use and avoid delegating secrets, credentials, payment data, or private account actions to the agent. <br>
Risk: The workflow depends on installing and running an external npm package. <br>
Mitigation: Install only when the publisher and package source are trusted in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qdore/application-use) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands produce snapshot-based desktop feedback after supported actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
