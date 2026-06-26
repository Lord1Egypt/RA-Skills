## Description: <br>
在东方热线论坛（东论）发帖、回帖、浏览热帖、查看帖子和回复。支持从环境变量或配置文件读取 token，无需登录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnoolteam](https://clawhub.ai/user/cnoolteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Donglun forum activity and to post or reply through a user-provided Donglun token. It is suited for account-authorized forum workflows where the user reviews write actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Donglun token can authorize account actions and may be exposed if saved in config.json or shared command history. <br>
Mitigation: Prefer an environment variable or command-line token, keep any saved config private, and avoid committing config.json. <br>
Risk: Posting and replying can publish user-visible content through the configured Donglun account. <br>
Mitigation: Review post and reply content before running write commands. <br>
Risk: The @file content option can submit unintended local file contents if the path is wrong. <br>
Mitigation: Confirm @file paths and file contents before using them in post or reply commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnoolteam/donglun-cli) <br>
- [Donglun forum](https://bbs.cnool.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Console text and JSON responses from Donglun API operations, with command-line usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations may read content from @file paths and may use a command-line, environment-variable, or config-file token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
