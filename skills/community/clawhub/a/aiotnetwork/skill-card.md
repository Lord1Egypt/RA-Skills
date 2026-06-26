## Description: <br>
Meta-skill that indexes all AIOT platform skills and routes agent requests to the correct sub-skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route AIOT platform requests to the correct sub-skill and follow prerequisite chains for account access, KYC, cards, payments, crypto wallet actions, and blockchain DID workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests can route into sensitive identity, card, payment, currency conversion, staking, and crypto withdrawal workflows. <br>
Mitigation: Review the individual AIOT sub-skills before installation and require clear user confirmation before uploading identity documents, creating cards, sending money, converting currency, staking, or withdrawing crypto. <br>
Risk: Downstream API behavior depends on the configured AIOT_API_BASE_URL. <br>
Mitigation: Verify the API base URL before use and override it only with a trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork) <br>
- [Publisher profile](https://clawhub.ai/user/D9m1n1c) <br>
- [Default AIOT API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests to AIOT sub-skills and documents the AIOT_API_BASE_URL configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
