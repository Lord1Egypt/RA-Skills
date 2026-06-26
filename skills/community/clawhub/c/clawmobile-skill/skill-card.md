## Description: <br>
ClawMobile is an Android automation toolkit that integrates with AutoX.js to help agents manage workflows, record mobile interactions, handle AI-assisted recovery, and communicate with an HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyan1221](https://clawhub.ai/user/miyan1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and RPA operators use this skill to automate Android device workflows, record mobile UI actions into reusable automation, and operate AutoX.js through a local or protected HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control an Android device and its visible app contents through an API. <br>
Mitigation: Install only when controlled device access is acceptable, and require explicit confirmation before recording, deletion, batch execution, text entry, AI recovery, or remote access. <br>
Risk: Weak default scoping or unchanged default tokens could expose the automation API. <br>
Mitigation: Keep the API bound to localhost or a protected network and replace default tokens before use. <br>
Risk: Screen recording and UI capture may collect secrets or personal data displayed on the device. <br>
Mitigation: Avoid recording screens that contain secrets or personal data, and disable or limit capture options unless needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miyan1221/clawmobile-skill) <br>
- [Publisher profile](https://clawhub.ai/user/miyan1221) <br>
- [ClawMobile documentation](https://docs.clawmobile.com) <br>
- [AutoX.js](https://autoxjs.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline Python, shell, cURL, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow identifiers, Android package names, API URLs, bearer tokens, membership actions, recording options, and AutoX.js task parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
