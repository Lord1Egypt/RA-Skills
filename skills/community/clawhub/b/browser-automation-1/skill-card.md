## Description: <br>
Automates browser navigation, data extraction, screenshots, form filling, clicking, and web application interaction through a local browser CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuradil](https://clawhub.ai/user/nuradil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to control a local browser for web research, page navigation, structured extraction, screenshots, form filling, and other interactive web tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect web accounts and local files through browser actions, downloads, screenshots, cookies, and cached browser data. <br>
Mitigation: Use an isolated browser profile, confirm before submissions or account-changing clicks, and clear screenshots, downloads, cookies, and cached data after sensitive use. <br>
Risk: The security review reports incomplete install provenance and weak guardrails. <br>
Mitigation: Install only after independently verifying the CLI or source package and trusting the publisher. <br>
Risk: Natural-language browser commands can expose credentials or perform unintended interactions. <br>
Mitigation: Avoid real credentials in natural-language commands and review each action before execution on sensitive sites. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nuradil/browser-automation-1) <br>
- [Browser Automation CLI Reference](artifact/REFERENCE.md) <br>
- [Browser Automation Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with browser CLI commands, JSON command results, and screenshot or download paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on a persistent local browser profile and may create screenshots or downloaded files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
