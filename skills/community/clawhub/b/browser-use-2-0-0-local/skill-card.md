## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wings229](https://clawhub.ai/user/wings229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate browser navigation, form entry, screenshots, web state inspection, data extraction, and local or cloud browser session control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser automation and real Chrome profile access can expose authenticated sessions, cookies, or sensitive browsing data. <br>
Mitigation: Use a dedicated test browser profile when possible, avoid exporting cookies, and use real profiles only when the task explicitly requires them. <br>
Risk: Python mode and cloud REST passthrough can run powerful actions beyond ordinary page interaction. <br>
Mitigation: Avoid Python mode and cloud REST passthrough unless explicitly needed, review commands before execution, and treat API keys as secrets. <br>
Risk: Tunnel support can make a local service reachable from the internet. <br>
Mitigation: Start tunnels only for ports intentionally meant to be reachable and stop tunnels promptly after use. <br>


## Reference(s): <br>
- [Browser Use 2.0.0 Local on ClawHub](https://clawhub.ai/wings229/browser-use-2-0-0-local) <br>
- [browser-use CLI setup documentation](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON, Files] <br>
**Output Format:** [Markdown guidance with browser-use CLI command examples; command output may include text, JSON, screenshots, cookies, or extracted page data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses persistent browser sessions and may invoke headed or headless browsers, real Chrome profiles, cloud browser APIs, tunnels, cookie import/export, and Python execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
