## Description: <br>
Feishu Group Memory records structured information from Feishu group messages, stores it for keyword search, and helps generate summaries or advice for sales, customer service, legal, and project workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinzeny](https://clawhub.ai/user/vinzeny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external teams that use Feishu group chats can use this skill to capture important chat context, search prior records, and ask for activity summaries or next-step advice. It is aimed at workflows such as sales tracking, customer support, legal matters, and project management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Feishu group chat content and may store extracted records locally. <br>
Mitigation: Use only with Feishu groups the user is authorized to process, restrict access to the workspace, and define retention and deletion rules before use. <br>
Risk: Paid analysis, advice, and summary flows may charge through SkillPay without sufficiently clear user consent. <br>
Mitigation: Require explicit confirmation before each billed action and show the amount, label, and payment result before continuing. <br>
Risk: The release evidence reports weak secret handling for the SkillPay key. <br>
Mitigation: Remove the hard-coded key, rotate the exposed credential, and load billing credentials from a protected secret source. <br>
Risk: Advice and summaries are generated from chat history and may be incomplete or misleading. <br>
Mitigation: Present generated advice as assistance for review, cite the relevant stored records when possible, and ask the user to verify important decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vinzeny/feishu-group-memory) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store extracted Feishu group records and industry context in the configured local workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
