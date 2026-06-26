## Description: <br>
Automates 12306 train-ticket workflows, including browser-based login, ticket search, and booking-oriented actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Feiyang2007](https://clawhub.ai/user/Feiyang2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with China Railway 12306 can use this skill to automate login and ticket-search workflows. Booking or payment-related actions should remain supervised and require explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global, for workflows involving the China Railway 12306 service. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate against a real 12306 travel account and may reach booking-related workflows. <br>
Mitigation: Require explicit user confirmation before booking, purchase, or payment actions, and keep browser automation supervised. <br>
Risk: Reusable login cookies may be saved in 12306_cookies.json. <br>
Mitigation: Store the workspace securely, do not share generated session files, and delete 12306_cookies.json when the session should no longer be retained. <br>
Risk: Credentials are supplied through RAILWAY_12306_USERNAME and RAILWAY_12306_PASSWORD environment variables. <br>
Mitigation: Avoid logging or exposing these values in prompts, command output, screenshots, or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Feiyang2007/12306-conflict) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve Playwright browser automation, 12306 account credentials from environment variables, and a reusable cookie file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
