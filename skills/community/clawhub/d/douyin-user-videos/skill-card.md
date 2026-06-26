## Description: <br>
获取抖音博主的视频列表 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanshiyang](https://clawhub.ai/user/tanshiyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch a Douyin creator's public profile video list from a Douyin user homepage URL, including descriptions and publish times. It is intended for workflows that need structured video-list retrieval after the user configures the required API key and Douyin cookie. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured Douyin login cookie and API key to xueai.szzy.top. <br>
Mitigation: Install only if the user trusts the publisher and xueai.szzy.top with those credentials; use a separate low-risk Douyin session where possible. <br>
Risk: A Douyin logged-in cookie can expose account session access if mishandled. <br>
Mitigation: Rotate or remove the cookie after use and avoid using a high-value account session. <br>
Risk: The API key is used for identity and billing with the third-party service. <br>
Mitigation: Scope the key to this skill configuration, monitor usage, and remove it when the skill is no longer needed. <br>
Risk: The security evidence recommends review before installing and warns against broad automatic activation. <br>
Mitigation: Review the skill and keep activation narrow until credential handling and protection are clear enough for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanshiyang/douyin-user-videos) <br>
- [Publisher profile](https://clawhub.ai/user/tanshiyang) <br>
- [Credential setup notes](https://my.feishu.cn/wiki/HbTpwSDMMiu4mUkCsjwcXgCWn7Z) <br>
- [Third-party Douyin video API endpoint](https://xueai.szzy.top/api/agi/douyin/user-home-videos) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON tool response with fields for success, message, data, and count; agents may format the returned video list as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns video descriptions and publish times when the upstream service succeeds; errors report invalid URLs, missing API keys, invalid cookies, insufficient balance, or network/API failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
