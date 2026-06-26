## Description: <br>
Generate secure passwords via the AceToolz API; generated passwords are returned in real time and are not stored. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acetoolz](https://clawhub.ai/user/acetoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent generate passwords with requested length and character settings through the AceToolz password generator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords and request settings are produced by AceToolz's external API, so use requires trust in that provider. <br>
Mitigation: Use this skill only where remote password generation is acceptable; for highly sensitive accounts, prefer a local password manager or local password generator. <br>
Risk: The skill depends on outbound access to AceToolz and may be unavailable or rate limited. <br>
Mitigation: Handle API failures by asking the user to try again later or use the AceToolz web generator directly. <br>


## Reference(s): <br>
- [AceToolz password generator](https://www.acetoolz.com/generate/tools/password-generator) <br>
- [AceToolz OpenClaw password generator API](https://www.acetoolz.com/api/openclaw/password-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown text containing a generated password and selected character settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports password length from 4 to 128 characters and optional character-class settings; output depends on AceToolz API availability.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
