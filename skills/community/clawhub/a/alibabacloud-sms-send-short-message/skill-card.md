## Description:

Send and manage Alibaba Cloud SMS messages through the Aliyun CLI, including test verification messages and delivery queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers use this skill to send verification, notification, or marketing SMS through Alibaba Cloud and to check signature, template, delivery, and send statistics. It also supports a built-in test verification SMS for accounts without approved signatures or templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags credential-handling concerns, cloud access beyond the stated SMS purpose, and partially inspected CLI guide and script content.

Mitigation: Clarify credential examples and unrelated cloud access and complete review of the CLI guide and script before installation. If proceeding, keep reusable access keys out of command-line arguments, use a protected credential method, and review the permissions and data the skill can access.

Risk: Sending an SMS contacts the specified phone number and may deliver a message the user did not intend.

Mitigation: Confirm all user-customizable parameters and restate the recipient and full send plan; send only after the user explicitly confirms.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-sms-send-short-message)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [RAM policies](references/ram-policies.md)
- [SMS qualification guide](references/sms-qualification.md)
- [SMS error codes](references/sms-error-codes.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Alibaba Cloud SMS console](https://dysms.console.aliyun.com/)
- [SendSms API documentation](https://help.aliyun.com/document_detail/419273.html)
- [SendTestVerification API documentation](https://api.aliyun.com/api/Dysmsapi/2017-05-25/SendTestVerification)
- [SMS delivery receipt error codes](https://help.aliyun.com/document_detail/101347.html)
- [SMS service error codes](https://help.aliyun.com/document_detail/101346.html)
- [QuerySmsQualificationRecord API documentation](https://help.aliyun.com/zh/sms/developer-reference/api-dysmsapi-2017-05-25-querysmsqualificationrecord)
- [QuerySingleSmsQualification API documentation](https://help.aliyun.com/zh/sms/developer-reference/api-dysmsapi-2017-05-25-querysinglesmsqualification)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Shell commands, API responses, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate SMS delivery when the user confirms a send plan.]

## Skill Version(s):

0.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
