## Description:

Provides paid, web-grounded answers through an OpenAI-compatible chat completions endpoint with single-search and streaming research modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a paid Answers proxy for fast cited answers or deeper multi-search research through OpenAI-compatible request and streaming response formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt content is sent to a paid external Answers service.

Mitigation: Use only with prompt content appropriate for that provider and avoid sensitive data unless the use is approved.

Risk: Automatic x402 payment flow can incur paid requests without per-request review.

Mitigation: Set explicit payment limits or confirmation steps and monitor usage and cost data returned by the service.

Risk: The recommended payment helper is unpinned and can run third-party code.

Mitigation: Pin and review the payment helper package before use, and run it with minimal local access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-answers)
- [sprintmint publisher profile](https://clawhub.ai/user/sprintmint)
- [CPBox API provider](https://www.cpbox.io)
- [CPPay facilitator](https://www.cppay.finance)
- [Answers API endpoint](https://www.cpbox.io/api/x402/answers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [OpenAI-compatible JSON or SSE streaming text, with optional citation, answer, progress, and usage tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an x402 payment flow; research mode requires streaming and emits progress, blindspots, answer, and usage tags.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
