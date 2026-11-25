## Description:

通过用户已登录的 Easy WebBridge 浏览器整理闲鱼商品资料、检查发布草稿，并在用户明确确认后执行一次上架。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External sellers can use this skill to turn existing product details and images into an Xianyu listing draft, check required fields, and optionally review a limited set of public comparable listings. The skill pauses before publication unless the user explicitly confirms a single listing action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a benign verdict but notes that one script was only partially inspected and the skill's environment and network permissions are unclear.

Mitigation: Before installation, review the uninspected script and confirm the browser and network permissions available to Easy WebBridge. Use the specified account and keep the task in draft mode until ready to approve publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/easy-xianyu-publish-free)
- [Easy WebBridge setup and source](https://github.com/xxjrq/easy-webbridge)
- [EasyBR download page](https://www.ebrower.com/down.html)
- [Easy WebBridge operation contract](references/操作契约.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON or Markdown listing report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports listing status, checked and missing fields, optional public comparable-item summaries, and next steps.]

## Skill Version(s):

1.1.1 (source: package.json, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
