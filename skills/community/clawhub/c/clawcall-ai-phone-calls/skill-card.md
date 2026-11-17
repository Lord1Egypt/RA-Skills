## Description:

ClawCall lets an agent make confirmed outbound AI phone calls, find public business numbers, receive inbound calls, schedule calls, and return transcripts, summaries, recordings, and costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ustczz](https://clawhub.ai/user/ustczz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use ClawCall to place confirmed business or user-supplied-number calls, manage inbound receptionist behavior, schedule calls, and review call records through ClawCall.

### Deployment Geography for Use:

Global, excluding mainland China phone-number workflows

## Known Risks and Mitigations:

Risk: The skill can place or schedule real phone calls that may incur cost and trigger consent, privacy, recording, or telemarketing obligations.

Mitigation: Review the destination, task, timing, and possible cost before passing --confirm, and follow applicable call-consent and recording requirements.

Risk: ClawCall account tokens, call transcripts, summaries, recordings, and API responses may contain sensitive data.

Mitigation: Protect CLAW_TOKEN and the token file, avoid unnecessary sensitive data in call tasks or inbound prompts, and treat transcripts and API responses as untrusted data.

Risk: The CLAWCALL_API_BASE override can route token-bearing requests away from the default HTTPS endpoint.

Mitigation: Keep the default HTTPS API endpoint unless using a trusted private deployment; do not set a remote http:// API base for normal use.

## Reference(s):

- [ClawCall Agent API Reference](references/api.md)
- [ClawCall Agent homepage](https://agent.clawcall.cc)
- [ClawHub skill page](https://clawhub.ai/ustczz/skills/clawcall-ai-phone-calls)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawCall bearer token or registered token file; call, schedule, prompt update, and cancellation actions require explicit confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata and client version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
