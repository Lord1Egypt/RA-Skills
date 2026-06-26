## Description: <br>
Initializes Chrome in Chrome DevTools Protocol (CDP) mode for Playwright or browser-use Agent automation, including profile-copy setup for Chrome 145+ App-Bound Encryption and non-default user-data-dir requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyzmeat](https://clawhub.ai/user/xyzmeat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to start and inspect a real Chrome CDP session for deterministic Playwright workflows or natural-language browser-use Agent tasks such as data extraction, screenshots, and form filling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies a logged-in Chrome profile and can expose cookies, history, and active web sessions to browser automation. <br>
Mitigation: Use a separate automation-only Chrome profile or test accounts, avoid copying a main personal profile, and protect or delete the copied profile after use. <br>
Risk: A CDP-enabled Chrome session can be controlled by Playwright or an LLM-driven browser-use Agent while the session is running. <br>
Mitigation: Install and run the skill only when this level of browser control is intended, close the CDP browser when finished, and review tasks before agent execution. <br>
Risk: The startup script can terminate existing Chrome processes and preserve logged-in sessions in the copied profile. <br>
Mitigation: Save browser work before running start_chrome.py and review the script before execution, especially the profile path, port, and process termination behavior. <br>


## Reference(s): <br>
- [Chrome CDP solution reference](references/chrome-cdp-solution.md) <br>
- [ClawHub skill page](https://clawhub.ai/xyzmeat/browser-use-init) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [Playwright connect to an existing browser](https://playwright.dev/python/docs/browsers#connect-to-an-existing-browser-instance) <br>
- [browser-use documentation](https://docs.browser-use.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and helper scripts for local Chrome CDP startup, CDP inspection, Playwright connection, and browser-use Agent execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
