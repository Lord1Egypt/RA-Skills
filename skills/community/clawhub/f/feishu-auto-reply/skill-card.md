## Description: <br>
Feishu Auto Reply Bot - Automatic reply to Feishu messages based on rules <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[night556](https://clawhub.ai/user/night556) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Teams operating Feishu workspaces use this skill to configure rule-based automatic replies for common questions, holiday notices, after-hours responses, and department templates. Maintainers can generate a YAML configuration and test matching rules before running the reply service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu bot requires permission to read chats and send messages in the configured workspace scope. <br>
Mitigation: Grant only the intended workspace permissions, avoid sensitive channels unless approved, and stop the service when automatic replies are no longer needed. <br>
Risk: Broad keyword or regular expression rules can trigger unintended automatic replies. <br>
Mitigation: Keep matching rules narrow, use @mention-only rules where appropriate, and test the configuration in a non-production chat before broader use. <br>
Risk: The release documents automatic replies, while the bundled start command indicates live message event subscription is not complete. <br>
Mitigation: Confirm live Feishu event handling in the target environment before relying on the service for production auto-replies. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/night556/feishu-auto-reply) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, text, guidance] <br>
**Output Format:** [YAML configuration and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes rule matching modes, working-hours settings, and @mention-only reply options.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
