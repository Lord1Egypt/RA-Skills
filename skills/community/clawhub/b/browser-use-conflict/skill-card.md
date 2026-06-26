## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang2606](https://clawhub.ai/user/tang2606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control a browser from the command line for navigation, page inspection, form interactions, screenshots, and data extraction. It is suited to testing or web workflows that need persistent sessions, authenticated profiles, cloud browsers, or browser automation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the skill as suspicious because it exposes broad browser automation, Python execution, authenticated session, cloud API, and public tunnel capabilities. <br>
Mitigation: Install only when the full browser-use CLI surface is needed, review commands before use, and run browser-use Python only on trusted code. <br>
Risk: Browser profiles, cookies, cloud API keys, and tunnels can expose accounts, secrets, or local services if used carelessly. <br>
Mitigation: Prefer isolated browser profiles, avoid cookie export/import and profile sync unless explicitly needed, treat cloud API keys as secrets, and stop public tunnels promptly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tang2606/browser-use-conflict) <br>
- [browser-use CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser state text, screenshots, HTML, cookies, or JSON output through the browser-use CLI depending on the command.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
