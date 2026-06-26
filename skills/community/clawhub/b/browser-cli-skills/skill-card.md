## Description: <br>
Control Chrome browsers from the terminal via the AIPex extension. Use this skill when the agent needs to manage browser tabs, search page elements, click buttons, fill forms, capture screenshots, or download content - all through shell commands without an MCP client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buttercannfly](https://clawhub.ai/user/buttercannfly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to control Chrome from shell commands, including tab management, page inspection, element interaction, screenshots, downloads, and scripted browser workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad command-line control over a connected Chrome browser, including page interaction, screenshots, downloads, uploads, and skill script execution. <br>
Mitigation: Use it only with browser sessions and pages where that level of control is acceptable, and require explicit confirmation before sensitive actions such as uploads, form submissions, purchases, deletions, screenshots, downloads, LLM analysis, skill script execution, or self-updates. <br>
Risk: Automation may interact with sensitive logged-in pages or expose private page contents through screenshots, downloads, or analysis. <br>
Mitigation: Avoid using it on banking, work, admin, or other sensitive logged-in pages unless each action is intentionally approved and the resulting files or outputs are reviewed. <br>
Risk: The security verdict is suspicious because of broad, under-scoped authority, even though the static scan was clean and VirusTotal was pending. <br>
Mitigation: Review the generated commands and the browser state before execution, keep the Chrome extension connection scoped to the intended task, and treat the pending scan status as a reason for extra caution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buttercannfly/browser-cli-skills) <br>
- [browser-cli homepage](https://github.com/AIPexStudio/browser-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for browser automation through browser-cli; the commands may operate on live browser tabs and local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
