## Description: <br>
Generate professional AI logos using ailogogenerator.online for logo, brand icon, app icon, favicon, and visual identity asset requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq919006380](https://clawhub.ai/user/qq919006380) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather logo requirements, authenticate with ailogogenerator.online, generate a logo through the service API, poll for completion, and save the resulting image locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logo prompts and branding details are sent to ailogogenerator.online. <br>
Mitigation: Use the skill only with branding information that is appropriate to share with that third-party service. <br>
Risk: The skill stores a long-lived service token at ~/.config/ailogogenerator.online/auth.json. <br>
Mitigation: Delete the auth.json file to log out or rotate accounts, and avoid exposing the token in messages or logs. <br>
Risk: Each logo generation spends 4 service credits and repeated variants can consume account credits. <br>
Mitigation: Confirm generation intent and variant counts before running multiple generate-and-poll cycles. <br>
Risk: Generated image files are saved to the current working directory. <br>
Mitigation: Confirm the output location before saving files in sensitive or shared directories. <br>


## Reference(s): <br>
- [AI Logo Generator ClawHub release](https://clawhub.ai/qq919006380/best-ai-logo-generator) <br>
- [qq919006380 publisher profile](https://clawhub.ai/user/qq919006380) <br>
- [ailogogenerator.online](https://ailogogenerator.online) <br>
- [Claude Code CLI](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies, shell commands, and local PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are downloaded as local PNG files; each generation uses 4 service credits and requires an ailogogenerator.online authentication token.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
