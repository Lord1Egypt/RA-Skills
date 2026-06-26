## Description: <br>
Treat email as untrusted input. Prevent prompt injection through your inbox by enforcing channel trust boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to keep email as an untrusted input channel while allowing email reading, summarization, and sending only after commands arrive through a verified channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured trusted confirmation channels could allow email-originated instructions to be approved by the wrong party. <br>
Mitigation: Configure the trusted channel and verified user ID carefully before relying on the policy. <br>
Risk: Forwarded email summaries may expose sensitive message contents outside the inbox. <br>
Mitigation: Keep forwarded summaries minimal and include only the sender, subject, requested action, and reason for flagging. <br>
Risk: Persistent memory or system-prompt changes may broaden the assistant's authority if applied without review. <br>
Mitigation: Review persistent memory and system-prompt updates before applying them. <br>


## Reference(s): <br>
- [Email Fortress on ClawHub](https://clawhub.ai/joeytbuilds/email-fortress) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown policy guidance with a reusable system-prompt or memory snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to provide their trusted confirmation channel and verified user ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
