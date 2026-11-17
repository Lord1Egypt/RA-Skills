## Description:

Auto Router routes each message to a suitable, cost-aware AI model based on question type, choosing between local free models and paid APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thibautnext](https://clawhub.ai/user/thibautnext)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to classify prompts and route them to a local or API-backed model based on expected complexity and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled wrapper delegates execution to an unbundled local script at /Users/thibaut/clawd/auto-router.js.

Mitigation: Audit the local router script before installation and confirm it matches the documented routing behavior.

Risk: Whole prompts may be routed to external API-backed models.

Mitigation: Require user or operator consent for external routing and block or redact sensitive data before prompts leave the local environment.

Risk: The router may select paid API models.

Mitigation: Configure provider allowlists, spending limits, and logging so paid model use is intentional and reviewable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes prompts through an unbundled local Node.js router and may select paid API models.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
