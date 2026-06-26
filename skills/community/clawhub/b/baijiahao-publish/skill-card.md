## Description: <br>
使用 auth 登录态打开百家号发布页，可填入标题与正文（支持 .md 转富文本）、选封面、存草稿或发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilisidu1210-ui](https://clawhub.ai/user/lilisidu1210-ui) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to open a Baijiahao publishing session with an existing auth or cookie file, fill an article title and body, and save a draft or publish through browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Baidu/Baijiahao auth or cookie file to operate the user's account. <br>
Mitigation: Use only auth files intended for this workflow, protect those files as credentials, and verify the active account before taking draft or publish actions. <br>
Risk: Draft and publish actions create real account changes, including public posting when --publish is used. <br>
Mitigation: Test with open-only, --draft, or --keep-open flows first, and use --publish only after reviewing the account, title, content, and cover selection. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lilisidu1210-ui/baijiahao-publish) <br>
- [Baijiahao editor page](https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [CLI status text and browser automation actions using optional Markdown article input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits [RESULT] success or [RESULT] failed for agent parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
