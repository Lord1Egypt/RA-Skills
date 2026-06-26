## Description: <br>
ClickSend API integration with managed authentication for sending SMS, MMS, and voice messages, managing contacts and lists, managing verified email addresses, and viewing account configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make user-approved ClickSend requests through Maton, including sending SMS, MMS, and voice messages and managing contacts, lists, verified email addresses, and account settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive credentials are required for ClickSend access through Maton. <br>
Mitigation: Keep MATON_API_KEY in trusted environment variables and avoid printing API keys in shared logs or screenshots. <br>
Risk: Messaging and voice operations can contact real recipients and may incur charges. <br>
Mitigation: Review recipient, content, timing, and cost impact before approving any send operation. <br>
Risk: Write operations can modify contacts, lists, verified email addresses, or other account data. <br>
Mitigation: Approve create, update, or delete requests only after confirming the target resource and intended effect. <br>
Risk: Accounts with multiple ClickSend connections can route a request to the wrong account. <br>
Mitigation: Specify the intended connection when multiple active connections exist. <br>


## Reference(s): <br>
- [ClickSend on ClawHub](https://clawhub.ai/byungkyu/clicksend) <br>
- [Maton](https://maton.ai) <br>
- [ClickSend Developer Portal](https://developers.clicksend.com/) <br>
- [ClickSend REST API v3 Documentation](https://developers.clicksend.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
