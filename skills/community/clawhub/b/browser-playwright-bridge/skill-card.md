## Description: <br>
Run Playwright scripts that share OpenClaw browser's login state via CDP, with automatic conflict avoidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert OpenClaw browser workflows into reusable Playwright scripts that can run with the same Chrome profile, login state, and lock-based CDP conflict prevention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playwright scripts can access the user's existing OpenClaw browser login state. <br>
Mitigation: Review every script before running it, avoid sensitive or production accounts, and prefer a dedicated browser profile or test account. <br>
Risk: Scheduled browser automation can continue acting without fresh user confirmation. <br>
Mitigation: Use cron only for reviewed workflows and keep timeouts, lock status checks, and account scope constrained. <br>


## Reference(s): <br>
- [Browser Playwright Bridge release page](https://clawhub.ai/swaylq/browser-playwright-bridge) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Playwright](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript code templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scripts and commands that operate on a shared browser profile and may use existing login state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
