## Description:

Focus coach for AI agents that diagnoses focus blockers using BJ Fogg's B=MAP framework and returns one tiny action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daisuke134](https://clawhub.ai/user/daisuke134)

### License/Terms of Use:


## Use Case:

External users and agents use this skill when a user is distracted, procrastinating, or otherwise struggling to focus. It helps diagnose one focus blocker and returns a small next action with an environment adjustment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and authenticate a third-party payment CLI and pay per request.

Mitigation: Review the CLI and endpoint before use, run in a constrained environment, and use a low-limit payment identity.

Risk: Focus-related prompts may be sent to a paid external API.

Mitigation: Avoid sending private or sensitive situations unless the user trusts the endpoint and CLI, and minimize the personal detail included in requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daisuke134/skills/focus-coach)
- [Focus Coach x402 API endpoint](https://anicca-proxy-production.up.railway.app/api/x402/focus-coach)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [JSON response with focus diagnosis, tiny action, environment design, and safety flag]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a paid x402 request through the awal CLI; the artifact documents a price of $0.01 USDC per request on Base mainnet.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
