## Description: <br>
Tired of being on hold? Polly calls customer service for you - navigates phone menus, waits on hold, explains your issue, and fights for a resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yox](https://clawhub.ai/user/hi-yox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have PollyReach place customer service calls, navigate phone menus, wait on hold, and pursue outcomes such as refunds, cancellations, billing corrections, bookings, and complaint escalation. The skill can also configure and poll incoming call handling so users can receive summaries, transcripts, and follow-up details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a persistent local PollyReach account token. <br>
Mitigation: Protect the credential file, avoid use on shared or compromised machines, and revoke or rotate the token if exposure is suspected. <br>
Risk: The skill can make outbound calls, answer calls to its assigned number, and retrieve inbound call or message content. <br>
Mitigation: Install and use it only when the user is comfortable delegating those actions to PollyReach, and confirm call goals and authorization before execution. <br>
Risk: Call summaries, transcripts, and recording or detail links can expose private communications. <br>
Mitigation: Share returned call details only with the appropriate user and avoid including sensitive personal, financial, or account information unless necessary for the task. <br>
Risk: Periodic inbound polling creates ongoing checks for new call information. <br>
Mitigation: Enable scheduled polling only after explicit user consent and disable it when ongoing monitoring is no longer needed. <br>


## Reference(s): <br>
- [Customer Service Caller on ClawHub](https://clawhub.ai/hi-yox/customer-service-caller) <br>
- [PollyReach homepage](https://pollyreach.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include activation URLs, call task status, call summaries, transcripts, recording or detail links, balance status, and local credential setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
