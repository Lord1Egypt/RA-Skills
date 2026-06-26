## Description: <br>
Soul-Bound Keys and Soulchain for persistent agent identity, reputation, and messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gonzih](https://clawhub.ai/user/Gonzih) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to integrate agents with AMAI's identity service for key-based registration, signed API requests, identity lookup, reputation anchoring, and public-key messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived private identity keys can bind an agent identity to AMAI's service and may be exposed if examples are used unchanged. <br>
Mitigation: Avoid printing private keys, store generated keys in a protected secret store or with strict file permissions, and review identity-binding implications before installation. <br>
Risk: Soulchain and reputation records are described as persistent and append-only. <br>
Mitigation: Avoid recording sensitive or reversible-test data unless permanent retention is acceptable. <br>


## Reference(s): <br>
- [AMAI ID ClawHub Release](https://clawhub.ai/Gonzih/amai-id) <br>
- [AMAI Identity Service](https://id.amai.net) <br>
- [AMAI Website](https://amai.net) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, API calls, configuration] <br>
**Output Format:** [Markdown with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides Ed25519 identity registration and signed request examples; no files are generated automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
