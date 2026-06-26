## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlshiny](https://clawhub.ai/user/zlshiny) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to drive the browser-use CLI for website navigation, page interaction, authenticated browsing, screenshots, data extraction, remote browser tasks, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cookie exports, synced profiles, and real Chrome profiles may expose authenticated sessions or other sensitive browser data. <br>
Mitigation: Ask before using profiles or syncing cookies, prefer domain-scoped sync, and avoid full-profile sync unless the user explicitly requires it. <br>
Risk: Remote or cloud browser mode may move page activity outside the local machine. <br>
Mitigation: Use remote mode for sensitive sites only with explicit user awareness, and stop cloud sessions after use. <br>
Risk: Tunnels can expose local development services beyond the local machine. <br>
Mitigation: Expose only the needed port and stop tunnels when the browsing task is complete. <br>


## Reference(s): <br>
- [Browser Use CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md) <br>
- [ClawHub release page](https://clawhub.ai/zlshiny/browser-use-1-0-2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline bash command examples and optional JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser state text, screenshots saved to files or emitted as base64, cookie JSON, and remote task or session identifiers from the CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
