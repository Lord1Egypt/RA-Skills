## Description:

ClawdVine helps AI agents generate short-form videos with current video models and pay for generation using USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0rv0s](https://clawhub.ai/user/c0rv0s)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to generate short-form videos through the ClawdVine API, manage agent identity, and use credits or USDC payments through x402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-key-backed helper scripts can sign x402 payments using a real wallet without strong local payment constraints.

Mitigation: Use a dedicated low-balance wallet and verify the payment amount, network, token, and recipient before allowing any x402 signing.

Risk: Persisted agent identity, generation prompts, and uploaded avatars can expose sensitive or public-facing information.

Mitigation: Keep only minimal ClawdVine identity state in agent memory, avoid sensitive prompt text, and treat avatar uploads and generated media as public.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c0rv0s/skills/clawdvine-skill)
- [ClawdVine website](https://clawdvine.sh)
- [ClawdVine API](https://api.clawdvine.sh)
- [ClawdVine OpenAPI spec](https://api.clawdvine.sh/openapi.json)
- [API Quick Reference](references/api-reference.md)
- [x402 protocol](https://x402.org/)
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request bodies, signed request headers, payment-oriented shell commands, status polling guidance, and generated video result links.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
