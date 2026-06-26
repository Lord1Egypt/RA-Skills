## Description: <br>
智能邮件草稿生成和模板管理工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users can use this skill to generate email drafts from keywords, adjust tone, manage reusable templates, and draft messages in multiple languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email drafts and templates may be saved locally as drafts.json and templates.json, which can expose sensitive content if local persistence is not acceptable for the environment. <br>
Mitigation: Confirm local persistence is acceptable before use, and avoid saving passwords, secrets, or highly confidential email content. <br>
Risk: Generated email drafts may contain inaccurate, incomplete, or tone-inappropriate wording. <br>
Mitigation: Review and edit generated drafts before sending them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/email-draft-oc) <br>
- [Publisher profile](https://clawhub.ai/user/huangjingzhi07) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown email drafts, with optional local JSON files for saved drafts and templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save drafts.json and templates.json locally when draft or template persistence is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
