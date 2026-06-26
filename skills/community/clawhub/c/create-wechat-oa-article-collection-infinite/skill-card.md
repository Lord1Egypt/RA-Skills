## Description: <br>
Creates WeChat Official Account article collections in the WeChat public platform backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and agents use this skill to create article collections in an authenticated WeChat Official Account backend, including opening the collection form, filling collection details, publishing, and verifying the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a live WeChat Official Account backend. <br>
Mitigation: Use an isolated browser profile where possible, review collection name and description manually, and require manual confirmation before the final publish click. <br>
Risk: Token-bearing WeChat URLs may expose session-sensitive information in logs or screenshots. <br>
Mitigation: Avoid sharing logs or screenshots that include token-bearing WeChat URLs and refresh tokens from the current homepage session before navigation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/create-wechat-oa-article-collection-infinite) <br>
- [Publisher profile](https://clawhub.ai/user/infiniteask) <br>
- [WeChat Official Account backend](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown instructions with browser operation steps and URL patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated WeChat Official Account browser session and current session token handling.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
