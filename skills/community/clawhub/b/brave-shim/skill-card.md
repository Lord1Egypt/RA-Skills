## Description: <br>
Set up brave_shim as a free local proxy for OpenClaw web_search, routing Brave API requests to DuckDuckGo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weare20202020](https://clawhub.ai/user/weare20202020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure no-api-key web search by routing OpenClaw Brave Search requests through a local DuckDuckGo-backed proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes OpenClaw search behavior by patching installed provider files. <br>
Mitigation: Back up OpenClaw provider files before patching and confirm how to revert the endpoint changes. <br>
Risk: The setup path runs unpinned external code and Python dependencies for the local proxy. <br>
Mitigation: Review or pin the external brave_shim repository and dependencies before installation. <br>
Risk: Search queries are routed through a locally cloned proxy service that uses DuckDuckGo/DDGS. <br>
Mitigation: Install only when that routing is acceptable and verify how to stop the local service. <br>


## Reference(s): <br>
- [brave_shim repository](https://github.com/asoraruf/brave_shim) <br>
- [ClawHub skill page](https://clawhub.ai/weare20202020/brave-shim) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell and Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local service setup, dependency installation, and edits to OpenClaw provider files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
