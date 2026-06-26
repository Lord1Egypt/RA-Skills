## Description: <br>
Publish Instagram images, Reels, and carousels, check Instagram publishing status, fetch recent Instagram direct messages, and send Instagram direct messages through a preconfigured MyBrandMetrics API connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish Instagram images, Reels, and carousels through a configured MyBrandMetrics connection, check publishing status, and fetch or send Instagram direct messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive MyBrandMetrics credentials and Instagram account identifiers. <br>
Mitigation: Keep credentials out of committed files, prefer runtime arguments or environment variables in shared workspaces, and install only when the user trusts the skill and MyBrandMetrics with the connected account. <br>
Risk: Publishing posts or sending direct messages can create external actions on the connected Instagram account. <br>
Mitigation: Verify the exact account, caption, media, conversation ID, and message text before allowing posts or direct messages. <br>


## Reference(s): <br>
- [Configuration](references/configuration.md) <br>
- [Publishing Examples](references/publishing-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clawbus/clawbus-instagram-publish) <br>
- [Clawbus](https://www.clawbus.com/) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts print the real MyBrandMetrics JSON response and stderr errors; no token caps or post-processing constraints are specified.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
