## Description: <br>
Bridge is an Agent-to-Human (A2H) verification and escrow platform where agents request physical-world tasks, define proof criteria, and escrow is released only when all criteria pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use Bridge to run a local FastAPI service for creating human-work tasks, collecting GPS, photo, timestamp, or signature proofs, and holding or releasing escrow state based on those checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API models escrow and payments but the security evidence says it is not suitable for real payments or production escrow. <br>
Mitigation: Limit use to local experimentation or review until real authentication, authorization, HTTPS deployment guidance, and stricter escrow state handling are added. <br>
Risk: The workflow can involve sensitive human-location and photo proof data. <br>
Mitigation: Avoid sensitive location or photo workflows until privacy controls and deployment guidance are defined. <br>
Risk: Signature proof is represented as presence of a non-empty signature rather than cryptographic verification. <br>
Mitigation: Require real cryptographic signature verification before relying on signature proofs for payment or task completion decisions. <br>


## Reference(s): <br>
- [Bridge ClawHub release](https://clawhub.ai/mirni/gh-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with shell commands and JSON HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a local FastAPI service, REST endpoints, proof submission payloads, and escrow status behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
