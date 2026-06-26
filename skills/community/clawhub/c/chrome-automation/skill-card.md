## Description: <br>
Chrome Automation helps agents run Chrome and Playwright automation on Linux servers for high-resolution screenshots, form filling, automated login flows, and stealth-style browsing behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanoha222](https://clawhub.ai/user/kanoha222) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to configure Linux server browser automation, capture screenshots, and run Playwright-based page interactions such as form filling or login workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports stealth anti-bot browsing and automated login or form submission. <br>
Mitigation: Use it only on systems and websites where automation is authorized, and require explicit approval before login, posting, or form submission. <br>
Risk: Headless browser execution and package installation can expand the runtime attack surface. <br>
Mitigation: Run the skill in an isolated, low-privilege environment rather than a shared or privileged host. <br>
Risk: Credential use in automated forms can expose sensitive account data. <br>
Mitigation: Avoid real credentials until logging is removed and credential handling has been reviewed. <br>


## Reference(s): <br>
- [Chrome Automation ClawHub page](https://clawhub.ai/kanoha222/chrome-automation) <br>
- [Google Chrome Linux package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) <br>
- [Playwright stealth script](scripts/playwright_stealth.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot files in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
