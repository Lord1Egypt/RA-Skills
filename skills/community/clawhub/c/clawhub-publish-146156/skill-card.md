## Description: <br>
Automate web navigation, interaction, and data extraction using a fast Rust-based headless browser CLI with Node.js fallback and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxw975](https://clawhub.ai/user/gxw975) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser workflows such as navigation, form filling, UI testing, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a browser session and may access page contents, logged-in sessions, form inputs, screenshots, and saved files when directed. <br>
Mitigation: Use least-privilege Ziniao/API key access and avoid assigning tasks involving sensitive accounts unless that browser access is intended. <br>
Risk: Browser automation can submit forms, run page JavaScript, and change web application state. <br>
Mitigation: Review the target site, commands, and session context before allowing actions that submit data or perform account changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gxw975/clawhub-publish-146156) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser actions, page snapshots, screenshots, PDF export, video recording, and JSON output when the underlying CLI is used.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
