## Description: <br>
Helps audit Agent Card signing practices in A2A protocol implementations by identifying missing signatures, weak signing schemes, and revocation gaps that allow impersonation in agent-to-agent trust handshakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit Agent Card signing practices for A2A protocol implementations. It helps assess signature presence, signing scheme strength, key transparency, revocation support, and key rotation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL input can cause the agent to contact an endpoint while fetching an Agent Card. <br>
Mitigation: Provide only endpoints intentionally selected for audit, or use direct JSON input or snapshots when outbound fetching is not desired. <br>
Risk: The audit evaluates publicly observable Agent Card signing metadata and cannot prove private key custody, key storage security, or undisclosed key compromise. <br>
Mitigation: Use signing audit results alongside behavioral analysis and broader trust-chain review before relying on capability or identity claims. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/agent-card-signing-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes signing posture checks, a STRONG / ADEQUATE / WEAK / UNSIGNED risk rating, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
