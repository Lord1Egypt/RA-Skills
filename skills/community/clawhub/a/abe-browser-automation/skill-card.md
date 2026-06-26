## Description: <br>
Automate web browser interactions using natural language via CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to navigate websites, interact with web applications, extract structured page data, capture screenshots, fill forms, and manage browser sessions through a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser tasks may be routed through SkillBoss API Hub when SKILLBOSS_API_KEY is configured. <br>
Mitigation: Use the remote mode only for sites and data approved for that service, and avoid submitting sensitive information unless explicitly required. <br>
Risk: The skill can reuse persistent logged-in browser state through .chrome-profile. <br>
Mitigation: Use an isolated or disposable browser profile for sensitive work and regularly clear .chrome-profile after use. <br>
Risk: The browser can submit forms and download files locally. <br>
Mitigation: Confirm before submitting forms or downloading files, and review downloaded files in ./agent/downloads before opening or using them. <br>
Risk: The reviewed artifact does not include the CLI implementation that users are asked to install. <br>
Mitigation: Verify the implementation source before installing dependencies or linking the browser command. <br>


## Reference(s): <br>
- [Browser Automation Skill](https://clawhub.ai/abeltennyson/abe-browser-automation) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [REFERENCE.md](artifact/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON command results, screenshots, and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create browser screenshots, downloads, and persistent Chrome profile state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
