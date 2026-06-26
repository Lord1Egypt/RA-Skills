## Description: <br>
Control browser automation through HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhg5](https://clawhub.ai/user/chenhg5) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to drive browser navigation, element interaction, page analysis, screenshots, JavaScript execution, and data extraction through a BrowserWing Executor HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control browser sessions and perform sensitive actions through the configured executor. <br>
Mitigation: Require explicit user approval before logins, uploads, purchases, posts, account changes, screenshots, page dumps, network inspection, or JavaScript execution. <br>
Risk: A remote or untrusted BrowserWing Executor could expose browser data or execute unintended actions. <br>
Mitigation: Install only when the executor is trusted, and prefer a local or otherwise secured executor endpoint. <br>
Risk: Using automation on sensitive logged-in sites can expose credentials, page content, or account state. <br>
Mitigation: Avoid sensitive logged-in sites unless necessary and review planned actions before execution. <br>


## Reference(s): <br>
- [browserwing ClawHub release](https://clawhub.ai/chenhg5/browserwing) <br>
- [BrowserWing project homepage](https://github.com/browserwing/browserwing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BROWSERWING_EXECUTOR_URL to choose the BrowserWing Executor endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
