## Description: <br>
Agent Phone Call gives agents a phone number and PollyReach-backed workflows for outbound calls, incoming-call handling, call summaries, recordings, and balance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsz](https://clawhub.ai/user/mrsz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register or activate a PollyReach phone identity, make task-oriented outbound calls, retrieve results, answer incoming calls, update answering behavior, and check account balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make and receive real calls through PollyReach. <br>
Mitigation: Require explicit user approval before every outbound call, booking, retry, target switch, purchase-like action, or scheduled polling setup. <br>
Risk: Call instructions, caller data, transcripts, recordings, and message notifications may be processed by PollyReach. <br>
Mitigation: Avoid sharing secrets or sensitive account details during calls, and show users the relevant transcript, summary, and recording links for review. <br>
Risk: The skill stores a persistent PollyReach phone-account token. <br>
Mitigation: Protect the token file, limit access to the configured credential path, and remove or rotate the token when the integration is no longer needed. <br>
Risk: A persistent inbound answering prompt can continue affecting how calls are handled. <br>
Mitigation: Review, update, or disable the inbound answering prompt when the user's intended call-handling behavior changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrsz/agent-phone-call) <br>
- [PollyReach homepage](https://pollyreach.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PollyReach account activation, persistent token storage, API polling, and user approval before call-related actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
