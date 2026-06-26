## Description: <br>
Automates browser tasks with the agent-browser CLI using local headless Chrome or Browserbase cloud mode for protected sites, form interaction, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maikimolto](https://clawhub.ai/user/maikimolto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive browser sessions for navigation, form filling, screenshots, data extraction, and setup of local or Browserbase-backed automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can access logged-in sessions, cookies, saved auth state, screenshots, clipboard contents, and network logs. <br>
Mitigation: Prefer isolated browser sessions, avoid real Chrome profiles unless intentionally needed, close sessions after use, and do not commit state files. <br>
Risk: The Browserbase API key grants access to cloud browser sessions. <br>
Mitigation: Store the key in a protected environment file or secret store, restrict file permissions, and avoid logging, sharing, or committing it. <br>
Risk: Stealth and CAPTCHA-solving automation can create policy or terms-of-service risk on protected sites. <br>
Mitigation: Use Browserbase and CAPTCHA-related features only on sites where automation is authorized. <br>


## Reference(s): <br>
- [agent-browser Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maikimolto/browser-agent-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation commands that operate on live websites and optional Browserbase cloud configuration.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
