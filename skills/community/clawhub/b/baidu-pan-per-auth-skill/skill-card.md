## Description: <br>
Guides Baidu Pan personal-app OAuth2 authorization, token exchange, token refresh, and scheduled refresh setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authorize a Baidu Pan personal application, write access and refresh tokens to a local .env file, and refresh tokens before expiry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local .env file stores Baidu Pan app credentials and OAuth access and refresh tokens. <br>
Mitigation: Keep the .env file out of version control and backups, restrict local file permissions where possible, and rotate or revoke Baidu credentials if the file is exposed. <br>
Risk: Refreshing a token writes a new refresh token and invalidates the previous one. <br>
Mitigation: Run refresh commands against the intended .env file and preserve the updated file after each refresh; re-authorize if the stored refresh token becomes invalid. <br>


## Reference(s): <br>
- [Baidu Pan Open Platform Documentation](https://pan.baidu.com/union/doc/al0rwqzzl) <br>
- [Baidu Pan App Console](https://pan.baidu.com/union/console/applist) <br>
- [ClawHub Skill Page](https://clawhub.ai/ugpoor/baidu-pan-per-auth-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local .env file with OAuth access token, refresh token, scope, expiry, and authorization date fields when the bundled Python script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
