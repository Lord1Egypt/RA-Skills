## Description: <br>
Operate Electron desktop applications on macOS via Puppeteer CDP. Open an app, find a UI element by text, click it, and take a screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate local macOS Electron apps by launching an installed application, selecting a visible text target, and returning a screenshot for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture the whole desktop, which may include sensitive windows outside the target application. <br>
Mitigation: Install only when local Electron desktop automation is needed, close sensitive windows before use, and prefer a revised version that captures only the target app and asks before saving screenshots. <br>
Risk: The skill may close processes more broadly than users expect after automation finishes. <br>
Mitigation: Run it only against trusted, non-production or non-account-sensitive apps unless the risk is accepted, and prefer a revision that terminates only the process it launched. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/bondli/desktop-operator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON object containing a screenshot file path; screenshot saved as a PNG file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, a local Electron app installed under /Applications, and accessibility permission for Terminal or Node.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
