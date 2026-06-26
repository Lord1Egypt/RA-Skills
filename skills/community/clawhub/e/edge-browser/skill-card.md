## Description: <br>
Control Microsoft Edge browser to fetch web pages and extract content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Meikowo](https://clawhub.ai/user/Meikowo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch a specified URL through Microsoft Edge or Chromium when normal fetch tools fail, JavaScript rendering is needed, or a site has basic bot-detection friction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses Playwright/Chromium to access arbitrary URLs, which can expose an agent to untrusted web content. <br>
Mitigation: Use it only for intended URLs and avoid sensitive internal or authenticated pages unless that access is explicitly required. <br>
Risk: Shell invocation with an unquoted URL can behave unexpectedly when the URL contains special characters. <br>
Mitigation: Quote URLs when running the fetch command from a shell. <br>
Risk: The optional output path can overwrite existing writable files. <br>
Mitigation: Choose output paths deliberately and avoid pointing the option at important existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Meikowo/edge-browser) <br>
- [Publisher profile](https://clawhub.ai/user/Meikowo) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the fetch script, plus Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script returns the URL, page title, HTML content, extracted body text, and success or error status; optional output files can overwrite writable paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
