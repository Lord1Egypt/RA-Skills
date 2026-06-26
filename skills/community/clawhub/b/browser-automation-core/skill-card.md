## Description: <br>
Core browser automation library for OpenClaw agents. Provides reusable navigation, interaction, and capture capabilities for both Facet (Onshape learning) and Ace (competition entry). Use when any agent needs to automate web browser interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a reusable browser automation core for navigating websites, interacting with elements and forms, capturing screenshots or page content, and extending those capabilities into agent-specific workflows such as Onshape learning or competition-entry automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can operate a browser with broad powers, including navigation, form submission, screenshots, and in-page script execution. <br>
Mitigation: Use a dedicated browser profile, restrict allowed domains and workflows, and require explicit approval before form submission, custom script execution, or captures of sensitive pages. <br>
Risk: Screenshots and captured page data can include personal, account, or business-sensitive information. <br>
Mitigation: Store captures only in reviewed locations, avoid personal logged-in sessions, and delete screenshots or session data that are no longer needed. <br>
Risk: The sample competition and Onshape workflows include realistic domains and form-filling patterns that may be adapted to high-impact actions. <br>
Mitigation: Replace sample data, review target-site rules, and keep a human approval gate before submitting entries or changing authenticated account state. <br>


## Reference(s): <br>
- [Browser Automation Core on ClawHub](https://clawhub.ai/stefanferreira/browser-automation-core) <br>
- [Publisher profile](https://clawhub.ai/user/stefanferreira) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [Puppeteer documentation](https://pptr.dev/) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [Selenium documentation](https://www.selenium.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and generated browser artifacts such as screenshots when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an available OpenClaw browser or Chrome DevTools Protocol endpoint for live browser operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
