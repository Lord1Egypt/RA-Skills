## Description: <br>
Automates browser-based collection of article and video result data from Douyin keyword search pages with configurable output format, result limit, browser mode, and output file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urhd528](https://clawhub.ai/user/urhd528) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and analysts use this skill to run keyword searches on Douyin and export structured search-result records for review, reporting, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may interact with an authenticated Douyin session or expose account-linked content in a failed-run screenshot. <br>
Mitigation: Run in a virtual environment or disposable workspace, use a dedicated Douyin account or isolated browser session, and delete debug_screenshot.png after failed runs if it contains private content. <br>
Risk: The skill requires installing Playwright and Chromium before use. <br>
Mitigation: Review the Playwright and Chromium installation steps before approval and install dependencies in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urhd528/douyin-keyword-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON, CSV, or text data output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print results to the console or write them to a user-specified output file; may create a debug screenshot when search-result parsing fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
