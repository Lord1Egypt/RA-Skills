## Description: <br>
Send SMS messages through Alibaba Cloud Short Message Service, including verification codes, notifications, marketing messages, batch sends, delivery queries, statistics, and signature or template checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send and monitor Alibaba Cloud SMS messages from an agent workflow, including collecting required phone, signature, template, and template-parameter inputs before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime Alibaba CLI plugin installation may change the execution environment without prior review. <br>
Mitigation: Preinstall and pin the Alibaba CLI and dysmsapi plugin before use when runtime installation is not acceptable. <br>
Risk: Qualification-detail APIs can expose sensitive account or identity records. <br>
Mitigation: Grant qualification-detail permissions only for admin workflows that require them, and redact qualification details before displaying or sharing them. <br>
Risk: Bulk or marketing SMS can create consent, compliance, and recipient-impact risk. <br>
Mitigation: Confirm recipient consent and applicable SMS compliance requirements before sending bulk or marketing messages. <br>
Risk: Overbroad RAM permissions increase blast radius for SMS operations. <br>
Mitigation: Use least-privilege RAM policies and add optional query or batch-send permissions only when the workflow requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-sms-send-short-message) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [SMS Send-Status Error Codes](references/sms-error-codes.md) <br>
- [SMS Qualification Query Reference](references/sms-qualification.md) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [SendSms API documentation](https://help.aliyun.com/document_detail/419273.html) <br>
- [Domestic SMS delivery-receipt error codes](https://help.aliyun.com/document_detail/101347.html) <br>
- [SMS service error codes](https://help.aliyun.com/document_detail/101346.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, parameter confirmation prompts, status summaries, and error-handling guidance.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
