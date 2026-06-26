## Description: <br>
Automates browser tasks with OpenClaw's Playwright browser control, including navigation, form filling, screenshots, PDFs, data extraction, multi-step flows, monitoring, and attended logins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to direct an agent through Chromium browser workflows such as scraping dynamic pages, filling forms, capturing screenshots or PDFs, and monitoring changing web content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over browser pages, including real logged-in sessions. <br>
Mitigation: Prefer the sandbox target and use profile="user" only for attended tasks where the user is present. <br>
Risk: Browser automation may submit forms, perform purchases, delete content, change accounts, or act on private sites. <br>
Mitigation: Require explicit confirmation before login, form submission, purchase, deletion, account changes, or actions on private sites. <br>
Risk: Credentials or one-time codes could be exposed during browser automation. <br>
Mitigation: Do not give the agent passwords or one-time codes. <br>


## Reference(s): <br>
- [Browser Automation ClawHub listing](https://clawhub.ai/fuzzyb33s/fuzzy-browser-automation) <br>
- [Fuzzyb33s publisher profile](https://clawhub.ai/user/fuzzyb33s) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Files] <br>
**Output Format:** [Markdown with JSON-style browser action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, PDFs, structured DOM snapshots, console logs, or extracted page data through browser actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
