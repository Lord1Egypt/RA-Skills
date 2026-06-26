## Description: <br>
AndonQ 腾讯云智能客服"领域虾" — 不切窗口、不排队，即刻获得腾讯云全产品线专业解答。支持工单查询（列表/详情/流水）、集团/MC 工单与需求单管理、腾讯云全产品线智能问答、云产品资源查询等。当用户查询工单、查看工单详情、咨询腾讯云产品问题、查询集团(360)工单/需求单、或查询腾讯云资源信息时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyuxlif](https://clawhub.ai/user/cyuxlif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Tencent Cloud users use this skill to authorize AndonQ and ask account-specific support questions, including ticket lookup, demand-order management, product Q&A, and cloud resource queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow uses an account-linked OAuth temporary code, and the security verdict flags this as needing careful review. <br>
Mitigation: Install only when intending to authorize AndonQ for Tencent Cloud support, ticket, demand-order, and resource access; prefer terminal binding flows instead of pasting the temporary code into chat. <br>
Risk: The local OAuth token file grants continued access while the authorization remains valid. <br>
Mitigation: Protect ~/.andonq/auth.json on shared machines, verify it is readable only by the local user, and revoke or reauthorize if the code may have been exposed. <br>


## Reference(s): <br>
- [AndonQ ClawHub Release Page](https://clawhub.ai/cyuxlif/andonq) <br>
- [ChatCompletionsAndonQ API Reference](references/api/ChatCompletionsAndonQ.md) <br>
- [AndonQ Gateway](https://andon.cloud.tencent.com) <br>
- [Tencent Cloud Authorization](https://cloud.tencent.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON setup output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams AndonQ gateway responses through SSE and may write local OAuth token configuration during setup.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
