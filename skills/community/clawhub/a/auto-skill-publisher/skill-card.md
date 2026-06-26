## Description: <br>
自动整理、审核、打包并通过CLI或网页上传技能至ClawHub平台，实现技能快速发布与变现管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[155143783](https://clawhub.ai/user/155143783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to prepare, review, package, publish, and operate ClawHub skills for marketplace release and monetization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable credentials and account tokens may be exposed or mishandled. <br>
Mitigation: Remove bundled secrets, rotate the affected GitHub and BotStreet credentials, and use user-driven scoped authentication before installation or execution. <br>
Risk: Automated publishing, task application, or delivery submission can create unintended marketplace actions. <br>
Mitigation: Require explicit user confirmation and enforced approval before publishing, applying for tasks, or submitting deliveries. <br>
Risk: The security verdict is suspicious for this release. <br>
Mitigation: Do not install this version as-is; review and remediate the security guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/155143783/auto-skill-publisher) <br>
- [ClawHub skill review standards](artifact/references/审核标准.md) <br>
- [ClawHub skill sales workflow test report](artifact/测试报告.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated packaging artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate ZIP packages, upload guides, review checklists, and publishing records for ClawHub skill releases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
