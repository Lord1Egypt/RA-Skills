## Description: <br>
Provides WeChat Official Account article writing, Markdown formatting, theme selection, image handling, draft creation, and publishing guidance for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongdinghuan](https://clawhub.ai/user/gongdinghuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, operators, and agents use this skill to plan, write, format, preview, and prepare WeChat Official Account articles, including optional draft creation and publishing workflows. It is most useful when an agent needs platform-specific Markdown guidance, layout theme selection, image handling, and WeChat publishing checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat App ID, App Secret, or access tokens could be exposed during publishing setup. <br>
Mitigation: Store credentials in environment variables or a managed secret store, avoid committing them, and rotate them if exposure is suspected. <br>
Risk: An agent could publish public WeChat content before a human has reviewed the article, images, and target account. <br>
Mitigation: Use draft creation and preview as the default workflow, and require explicit human approval before any publish_draft, publish_now, or full_auto_publish action. <br>
Risk: Generated article content may violate platform policy, include sensitive material, or contain inaccurate claims. <br>
Mitigation: Review the final article against WeChat policies and the account's editorial standards before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongdinghuan/clawhub-wechat-writing-pro) <br>
- [WeChat publishing guide](knowledge/wechat-publishing-guide.md) <br>
- [WeChat Official Account developer documentation](https://developers.weixin.qq.com/doc/offiaccount) <br>
- [Markdown syntax reference](https://blog.axiaoxin.com/post/markdown-guide/) <br>
- [Theme catalog source](https://md.axiaoxin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with article drafts, checklists, command examples, API examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include formatted WeChat article content, publishing action plans, WeChat API request examples, and human-review checkpoints.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, artifact package.json, and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
