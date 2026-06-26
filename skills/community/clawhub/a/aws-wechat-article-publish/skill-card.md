## Description: <br>
Publishes prepared WeChat Official Account articles to drafts or submits them for release through the WeChat API, with credential checks, cover and image uploads, and pre-publish review steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operations teams, developers, and agents use this skill to move a prepared article directory into a WeChat Official Account draft or publishing workflow. It is intended for controlled release workflows where credentials, article assets, and publication mode are checked before the API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live WeChat credentials and sends article files to an API endpoint. <br>
Mitigation: Use a dedicated WeChat account, keep aws.env out of version control, and confirm the destination API base before running publishing commands. <br>
Risk: A configurable API base or proxy could route credentials and content to an untrusted endpoint. <br>
Mitigation: Allow only the official WeChat API endpoint or a trusted approved proxy, and review any configured API base before execution. <br>
Risk: Publishing commands can create drafts or submit live content. <br>
Mitigation: Run draft mode or an explicit dry run first, require confirmation before live publishing, and review the pre-publish checklist before marking the article complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-publish) <br>
- [Usage guide](references/usage.md) <br>
- [Submit guide](references/submit-guide.md) <br>
- [WeChat API reference](references/api-reference.md) <br>
- [Pre-publish checklist](references/pre-publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration checks, and status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create WeChat drafts or submit live publishing requests when credentials, article assets, and publish mode are confirmed.] <br>

## Skill Version(s): <br>
1.0.22 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
