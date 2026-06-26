## Description: <br>
ClawdCall helps OpenClaw agents place outbound AI voice calls, manage signup and authentication, wire optional completion webhooks, retrieve transcripts, and track billing-aware call execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chitrang89](https://clawhub.ai/user/chitrang89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use ClawdCall to orchestrate paid outbound voice-agent calls from OpenClaw, including call setup, webhook-based completion handling, transcript retrieval, and safe storage of non-secret call identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls that may consume call credits and contact real people. <br>
Mitigation: Confirm the user's intent, target phone number, call objective, caller identity, and paid-call readiness before placing any outbound call. <br>
Risk: API tokens, webhook tokens, OTPs, and transcripts may contain sensitive information. <br>
Mitigation: Use secure environment or runtime storage, avoid persistent memory for secrets, and retain transcripts only when the user explicitly requests it. <br>
Risk: Asynchronous callback wiring can send call results to an OpenClaw endpoint. <br>
Mitigation: Enable webhook callbacks only when the endpoint is controlled and trusted, and omit callback wiring when required routing values or tokens are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chitrang89/clawdcall) <br>
- [ClawdCall homepage](https://clawdcall.com) <br>
- [ClawdCall API base](https://api.clawdcall.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP request shapes and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawdCall credentials for calls and optional OpenClaw webhook credentials for asynchronous results.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
