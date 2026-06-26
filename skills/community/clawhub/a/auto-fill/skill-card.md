## Description: <br>
Uses Chrome Debug Protocol (CDP) to read the current page's form structure and fill fields from user-provided data after explicit invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLiu007](https://clawhub.ai/user/ScottLiu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assist with browser form completion in a real Chrome session while retaining responsibility for navigation, submission, CAPTCHAs, and ambiguous fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real Chrome session through CDP and may enter user data into unintended pages. <br>
Mitigation: Use a separate Chrome profile, confirm the destination URL before filling, and only run it on pages you trust. <br>
Risk: Form filling can expose sensitive information if used on private, financial, password, or identity forms without close supervision. <br>
Mitigation: Avoid sensitive forms unless watching closely, require confirmation before password or file-upload fields, and leave submission to the user by default. <br>
Risk: Starting Chrome with a remote debugging port broadens local browser-control authority while it remains open. <br>
Mitigation: Close the debug Chrome process when finished and keep the CDP endpoint bound to the local machine. <br>
Risk: Installing browser automation tooling with a floating package version can change behavior over time. <br>
Mitigation: Pin the MCP package version before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ScottLiu007/auto-fill) <br>
- [Publisher profile](https://clawhub.ai/user/ScottLiu007) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate browser tooling through Chrome CDP and may produce screenshot-based confirmation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
