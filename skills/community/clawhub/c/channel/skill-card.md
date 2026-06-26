## Description: <br>
WeChat Official Account Draft Box management tool. Create and manage graphic draft articles via WeChat API, supporting text and images. Automatically extracts the first paragraph as summary. Supports draft creation, listing, publishing, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to prepare and manage WeChat Official Account draft articles, upload associated images, list drafts, and submit or delete drafts through the WeChat API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or delete WeChat Official Account drafts when run with valid credentials. <br>
Mitigation: Review media IDs and intended actions before running publish or delete commands. <br>
Risk: WECHAT_APPSECRET and the cached access token can grant access to account draft-management APIs. <br>
Mitigation: Protect WECHAT_APPSECRET and ~/.config/channel/access_token.json, and rotate credentials if they are exposed. <br>
Risk: Article and image files passed to the tool may be uploaded to WeChat services. <br>
Mitigation: Use only article text and media files that are approved for upload to the connected WeChat Official Account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manifoldor/channel) <br>
- [WeChat Official Account documentation](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html) <br>
- [WeChat Official Account API reference](references/wechat_api.md) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, Python CLI commands, and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WECHAT_APPID and WECHAT_APPSECRET environment variables and may cache an access token under ~/.config/channel.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
