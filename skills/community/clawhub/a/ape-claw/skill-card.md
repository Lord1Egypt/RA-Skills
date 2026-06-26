## Description: <br>
Use the ape-claw CLI to bridge to ApeChain and execute NFT quote, simulation, purchase, telemetry, and wallet-readiness workflows with policy gates and confirmation phrases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simplefarmer69](https://clawhub.ai/user/simplefarmer69) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw agents use this skill to discover ApeChain NFT listings, quote and simulate purchases, bridge APE, and execute transactions only after policy checks, confirmation phrases, and wallet readiness checks pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents toward real crypto wallet operations, including purchases and signed transactions. <br>
Mitigation: Use a dedicated low-balance wallet, keep strict spend limits and allowlists in place, and avoid autonomous execution unless those controls are configured. <br>
Risk: The skill instructs users to run unpinned remote ape-claw installer or CLI code. <br>
Mitigation: Review and pin the external ape-claw source before running installer or CLI commands. <br>
Risk: Credential-bearing clawbot chat flows can expose agent tokens if sent to an untrusted endpoint. <br>
Mitigation: Send clawbot tokens only to trusted HTTPS backends and avoid sharing them with unknown telemetry or chat servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simplefarmer69/ape-claw) <br>
- [ApeClaw website](https://apeclaw.ai) <br>
- [OpenClaw website](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands prefer --json output and may require wallet credentials, API keys, explicit --execute flags, simulation, and confirmation phrases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
