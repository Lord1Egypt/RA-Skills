## Description: <br>
Full-featured headless browser for OpenClaw agents that navigates pages, reads accessibility-tree snapshots with @ref targets, manages tabs, runs JavaScript, and imports cookies without a vision model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashish797](https://clawhub.ai/user/ashish797) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Gbrow to give OpenClaw agents browser navigation, page reading, form interaction, tab management, JavaScript execution, screenshots, and PDF capture through Playwright and a local HTTP command interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with real browser sessions, cookies, local files, repository state, and persistent session storage. <br>
Mitigation: Run it in an isolated workspace and browser profile, and avoid importing cookies for sensitive accounts. <br>
Risk: The documented one-line installer executes a remote shell script. <br>
Mitigation: Prefer a pinned clone or reviewed release artifact before running setup commands. <br>
Risk: Headed and sidebar features can expand local agent execution and repository-write exposure. <br>
Mitigation: Enable those features only when that access is intended and has been reviewed. <br>


## Reference(s): <br>
- [Playwright](https://playwright.dev/) <br>
- [Bun](https://bun.sh/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [gstack](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, JSON, HTML] <br>
**Output Format:** [Plain text, Markdown command guidance, JSON command responses, HTML snippets, screenshots, and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser outputs may include page content, accessibility-tree refs, local browser/session state, screenshots, PDFs, and command activity logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
