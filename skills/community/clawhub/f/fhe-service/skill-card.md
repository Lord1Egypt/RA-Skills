## Description: <br>
Enables agents to call the RheumaScore API for homomorphic-encryption-based clinical score computations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to register for RheumaScore API access, list available clinical scores, retrieve schemas, and request single or batch score computations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release makes strong encrypted-health-data privacy claims while examples show clinical values sent to a third-party API as ordinary JSON. <br>
Mitigation: Review the provider, privacy terms, compliance posture, and end-to-end encryption design before using real clinical information. <br>
Risk: Protected health information or patient-derived values could be exposed if the service or data flow is not approved for the organization. <br>
Mitigation: Use test or de-identified data unless organizational approval covers the service and workflow. <br>
Risk: API keys obtained from the service can authorize requests to a third-party clinical scoring API. <br>
Mitigation: Protect API keys, rotate them when needed, and avoid embedding keys in shared prompts, logs, or repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CryptoReuMD/fhe-service) <br>
- [CryptoReuMD publisher profile](https://clawhub.ai/user/CryptoReuMD) <br>
- [RheumaScore website](https://rheumascore.xyz) <br>
- [RheumaScore FHE API](https://rheumascore.xyz/fhe/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and API endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API-key registration, score schema lookup, single and batch computation requests, pricing, error codes, and support details.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
