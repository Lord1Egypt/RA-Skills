## Description:

Orchestrate outbound AI voice calls and asynchronous call results through ClawdCall from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chitrang89](https://clawhub.ai/user/chitrang89)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to place user-confirmed outbound voice-agent calls, configure optional OpenClaw callbacks, retrieve completed call transcripts, and manage non-secret call identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real outbound calls that may consume paid calling minutes.

Mitigation: Require explicit user confirmation, a verified phone number, and a clear call objective before each outbound call.

Risk: ClawdCall and OpenClaw tokens could expose account access if stored or logged.

Mitigation: Keep tokens in secure runtime storage or ephemeral session state, and never write them to persistent memory, logs, transcripts, or task text.

Risk: Call transcripts and spoken context may contain sensitive personal information.

Mitigation: Retrieve transcripts only for completed calls and retain transcripts or sensitive call details only when the user explicitly asks for retention.

Risk: Incorrect callback routing or fabricated identifiers could misattribute call results.

Mitigation: Use only available webhook URLs, tokens, conversation IDs, call IDs, and campaign IDs; omit callback wiring or defer lookup when required values are missing.

## Reference(s):

- [ClawdCall skill page](https://clawhub.ai/chitrang89/skills/clawdcall)
- [Publisher profile](https://clawhub.ai/user/chitrang89)
- [ClawdCall homepage](https://clawdcall.com)
- [ClawdCall API base](https://api.clawdcall.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payload shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include outbound-call instructions, callback configuration, call-result summaries, transcript retrieval guidance, and safe memory-handling rules.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
