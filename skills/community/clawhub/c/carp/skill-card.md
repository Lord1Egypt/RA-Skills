## Description: <br>
Manage a local CARP interface for secure, verified agent-to-agent commerce workflows over CARP endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitsanity](https://clawhub.ai/user/bitsanity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure IF_URL and run CARP curl workflows for registration, polling, request submission, result posting, answer retrieval, and menu lookup through a trusted local or LAN interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CARP curl commands may send request bodies, cookies, keys, and results to the configured IF_URL endpoint. <br>
Mitigation: Set IF_URL only to a localhost or trusted LAN CARP interface and treat request bodies, cookies, and keys as sensitive. <br>
Risk: Queue polling or request automation can repeat operations unintentionally if loops are too aggressive. <br>
Mitigation: Use idempotent polling loops with backoff when automating CARP queue reads. <br>


## Reference(s): <br>
- [CARP reference implementation](https://github.com/bitsanity/agent-crvp) <br>
- [CARP on ClawHub](https://clawhub.ai/bitsanity/carp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and IF_URL; commands target a user-configured local or LAN CARP interface.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
