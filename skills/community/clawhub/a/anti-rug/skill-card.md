## Description:

Anti Rug is a Web3 token security scanner that checks token contracts for honeypots, rug-pull indicators, and contract risks across EVM chains and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Web3 analysts use this skill to run token contract risk checks, classify token scenarios, and review structured risk verdicts before deeper due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom API gateway can cause token queries to be sent to an untrusted endpoint.

Mitigation: Use the default GoPlus endpoint or a trusted HTTPS gateway, and do not allow untrusted prompts or users to choose the gateway.

Risk: A low-risk verdict can overstate token safety.

Mitigation: Treat the scanner result as one due-diligence input, not as investment advice or proof that a token is safe to buy.

## Reference(s):

- [ClawHub Anti Rug Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/anti-rug)
- [ClawHub deanpeng-dotcom Publisher Profile](https://clawhub.ai/user/deanpeng-dotcom)
- [GoPlus Labs API Endpoint](https://api.gopluslabs.io)
- [Repository listed in skill metadata](https://github.com/ZorroShao/anti-rug)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON output from a Python CLI, with explanatory text and command examples in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a chain identifier and token contract address; optional custom API gateway should only be a trusted HTTPS endpoint.]

## Skill Version(s):

3.1.0 (source: server release evidence, frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
