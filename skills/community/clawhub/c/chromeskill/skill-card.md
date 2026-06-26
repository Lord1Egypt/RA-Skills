## Description: <br>
Browser automation via the Chrome AI Action bridge for navigating pages, clicking, typing, capturing screenshots, extracting content, and managing browser state through Puppeteer CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jami-lin](https://clawhub.ai/user/jami-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to control a local Chrome or Chromium browser for web navigation, form interaction, screenshots, content extraction, cookie and storage management, PDF export, and network inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad local control over Chrome through a localhost bridge. <br>
Mitigation: Review requested browser actions before execution and keep the bridge bound to localhost rather than exposing it beyond the local machine. <br>
Risk: First use may install and run the third-party chrome-ai-action npm package with local user privileges. <br>
Mitigation: Review the package before installation and run the skill in an environment appropriate for third-party local code. <br>
Risk: Browser automation can interact with logged-in accounts, cookies, storage, downloads, and page content. <br>
Mitigation: Use a dedicated Chrome profile and avoid sensitive logged-in sessions unless each action is intentional. <br>


## Reference(s): <br>
- [Bridge API Reference](references/bridge-api.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/jami-lin/chromeskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON action examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger local browser actions through a localhost bridge and return browser-derived text, screenshots, page metadata, cookies, storage values, PDFs, network data, and status JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
