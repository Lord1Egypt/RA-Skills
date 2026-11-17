## Description:

Demo skill for practicing Cashu HTTP 402 payment flow end-to-end: detect 402, review x-cashu challenge, request permission when needed, settle payment, and retry with X-Cashu.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[robwoodgate](https://clawhub.ai/user/robwoodgate)

### License/Terms of Use:


## Use Case:

External developers and agent builders use Clawtar to practice a controlled Cashu-gated HTTP 402 payment flow: inspect the x-cashu challenge, request approval when payment is needed, settle the challenge, and retry with X-Cashu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend a small Cashu amount and send a Cashu payment token to a specific demo service.

Mitigation: Proceed only with explicit user approval for spending or cocod installation, and send payment tokens only in the X-Cashu retry header.

Risk: An agent could confuse the x-cashu challenge with a payment token or report completion before the endpoint confirms success.

Mitigation: Treat x-cashu as a challenge, not a token, and report success only when the response includes ok: true.

## Reference(s):

- [Clawtar endpoint](https://clawtar.cashutools.dev/v1/clawtar/ask)
- [Minibits Mint](https://mint.minibits.cash/Bitcoin)
- [cocod ClawHub skill](https://clawhub.ai/Egge21M/cocod)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline HTTP, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before spending Cashu tokens or installing payment tooling.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
