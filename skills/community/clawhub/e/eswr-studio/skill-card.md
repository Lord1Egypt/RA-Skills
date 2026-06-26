## Description: <br>
Elsewhere creator studio - register a new account with an invite code, publish articles, import WeChat articles, and manage an Elsewhere creator profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pitayak](https://clawhub.ai/user/pitayak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and their agents use this skill to register for Elsewhere, publish Markdown articles, import WeChat articles, upload images, and update profile metadata through Elsewhere APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a non-expiring Elsewhere API token to publish articles and update a creator profile. <br>
Mitigation: Provide the token through a user-controlled environment variable or secure secret manager, avoid storing it in long-term memory, and rotate it from the Elsewhere dashboard if exposure is suspected. <br>
Risk: The skill asks agents to refresh instructions from a remote file before use. <br>
Mitigation: Review any fetched update before following it and prefer a known, reviewed release when operating on a production account. <br>
Risk: Publishing and profile-update commands can change public Elsewhere content. <br>
Mitigation: Confirm article payloads, imported content, image replacements, and profile fields before executing authenticated API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pitayak/eswr-studio) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pitayak) <br>
- [Elsewhere creator dashboard](https://elsewhere.news/dashboard/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary JSON files and call Elsewhere APIs with a bearer token.] <br>

## Skill Version(s): <br>
2.9.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
