## Description: <br>
Bridge is an Agent-to-Human (A2H) verification and escrow platform for requesting physical-world tasks, defining verification criteria, splitting work into milestones, tracking worker reputation, and handling disputes. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Bridge to create local A2H task workflows that track requested physical work, verification criteria, escrow state, milestones, disputes, and worker reputation through an HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill describes escrow, payments, proof, worker reputation, and privacy-sensitive workflows without controls strong enough for real funds or public marketplaces. <br>
Mitigation: Treat the release as an unsecured local demo until authentication, authorization, real payment controls, stronger proof validation, privacy disclosures, and safer milestone accounting are added. <br>
Risk: The artifact uses local in-memory state for tasks, escrow status, disputes, and worker reputation, so data is not durable and should not be treated as an auditable financial ledger. <br>
Mitigation: Use it only for local evaluation or prototyping unless durable storage, audit trails, reconciliation, and operational controls are implemented. <br>


## Reference(s): <br>
- [Bridge on ClawHub](https://clawhub.ai/mirni/a2h-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP API examples, shell commands, and JSON request or response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local API usage patterns for tasks, verification proofs, milestone releases, disputes, worker reputation, and platform statistics.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
