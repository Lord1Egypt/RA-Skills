## Description: <br>
Browser Auto Download helps agents use Playwright-driven browser automation to download files from dynamic pages that require platform detection, multi-step navigation, auto-download capture, or fallback button clicking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aaronxx](https://clawhub.ai/user/Aaronxx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to automate software downloads from dynamic web pages where simple HTTP tools are unreliable. It is especially suited for flows involving JavaScript-rendered download controls, platform-specific pages, and local file-saving workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads files from user-provided web pages, so a downloaded file may be unsafe or not the intended artifact. <br>
Mitigation: Use trusted URLs, review the saved filename and source, and verify or scan downloaded files before opening or executing them. <br>
Risk: Debug mode can save screenshots, HTML, and extracted text from pages to a local debug folder. <br>
Mitigation: Avoid using debug mode on logged-in or sensitive pages, and delete generated debug artifacts when they are no longer needed. <br>
Risk: Browser automation writes files to a local output directory and may select platform-specific download links automatically. <br>
Mitigation: Set an explicit output directory when needed and confirm the selected platform and saved file before using the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Aaronxx/browser-auto-download) <br>
- [Publisher profile](https://clawhub.ai/user/Aaronxx) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python snippets, and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress is reported on stderr; successful downloads return JSON with path, filename, size, and platform.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
