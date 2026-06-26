## Description: <br>
内容创业凭证管理器追踪并管理内容创作技能的 API 凭证配置状态，提供状态扫描、配置引导和本地凭证写入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amazinglittlefish](https://clawhub.ai/user/amazinglittlefish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to check whether content-production skills have the credentials they need, identify missing API keys or cookies, and write supported credentials into a local configuration file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful API keys and a Xiaohongshu session cookie, and artifact guidance may lead users to provide secrets in chat or command arguments. <br>
Mitigation: Use only on a trusted local machine; avoid pasting full API keys or cookies into chat; prefer a secure local prompt or manually editing a protected credentials file. <br>
Risk: A leaked Xiaohongshu cookie can act like a password for the related account session. <br>
Mitigation: Treat the cookie as a secret, store it only in the protected local credentials file, and rotate or revoke any credential that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amazinglittlefish/content-credential-manager) <br>
- [Tavily API key portal](https://app.tavily.com) <br>
- [StepFun developer platform](https://platform.stepfun.com) <br>
- [Meitu Open-Claw platform](https://www.miraclevision.com/open-claw) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON credential configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes supported credential values to ~/.openclaw/credentials.json with owner-only file permissions when the set_credential.py helper is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
