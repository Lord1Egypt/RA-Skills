## Description: <br>
Starts Chrome with a local remote debugging port and supports either reused login state or an independent browser profile for automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1232023](https://clawhub.ai/user/luis1232023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to launch a Chrome instance on port 9222 for Chrome DevTools or Playwright workflows. It is intended for browser automation that may need either a clean profile or reused cookie/session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reuse mode can expose logged-in browser sessions through the local Chrome debugging port. <br>
Mitigation: Prefer independent mode when possible, avoid personal or production accounts, and close the debug browser when finished. <br>
Risk: Local tools that can connect to port 9222 may control pages in the launched browser. <br>
Mitigation: Use the skill only in trusted local environments and keep the debugging session open only as long as needed. <br>
Risk: Reuse mode may close existing Chrome windows or replace active browser state. <br>
Mitigation: Save browser work before reuse mode, or choose independent mode when preserving existing windows matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1232023/brower-opener) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch Chrome in the background and expose Chrome DevTools on http://127.0.0.1:9222.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
