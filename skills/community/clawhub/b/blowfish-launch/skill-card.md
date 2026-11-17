## Description:

Launch, check, list, and manage Solana token deployments and fee claims through the Blowfish Agent API for Meteora Dynamic Bonding Curve launches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[basedmereum](https://clawhub.ai/user/basedmereum)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to launch Solana tokens, monitor launch status, list launched tokens, and claim accrued trading fees through the Blowfish Agent API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Solana private key through WALLET_SECRET_KEY.

Mitigation: Use only a dedicated low-value wallet and avoid exposing WALLET_SECRET_KEY in shell history, logs, or shared command transcripts.

Risk: The skill can trigger real token launches or fee claims.

Mitigation: Require a manual confirmation step before any launch or fee claim and treat launches and claims as real blockchain operations, not simulations.

## Reference(s):

- [Blowfish Agent API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/basedmereum/skills/blowfish-launch)
- [Blowfish Agent API Base URL](https://api-blowfish.neuko.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript code paths, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated token launches, launch status polling, token listing, and fee claims.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
