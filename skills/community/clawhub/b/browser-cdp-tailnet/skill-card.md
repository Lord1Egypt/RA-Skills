## Description: <br>
Uses a shared Chromium browser exposed over a tailnet Chrome DevTools Protocol endpoint for remote browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need a shared remote Chromium session over a tailnet instead of a local browser. It provides connection guidance and checks for using the remote CDP target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents receive broad control of a shared remote browser, which can expose pages, sessions, or browser state to others who can access the tailnet endpoint. <br>
Mitigation: Connect only to trusted tailnet endpoints and use a dedicated non-sensitive browser profile for agent activity. <br>
Risk: Actions performed through the shared browser can submit forms, change account data, or use authenticated sessions. <br>
Mitigation: Require explicit user approval before submitting forms, changing account data, or using authenticated sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lotfinity/browser-cdp-tailnet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline endpoint and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CDP HTTP and WebSocket endpoint guidance plus a probe requirement before claiming the browser works.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
