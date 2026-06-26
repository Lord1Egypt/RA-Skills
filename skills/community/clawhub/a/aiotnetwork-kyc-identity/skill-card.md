## Description: <br>
Know-Your-Customer verification via MasterPay Global. Submit personal data, upload identity documents, and track approval status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to complete KYC setup, submit profile and identity document data, upload verification documents, and check MasterPay Global review status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles identity documents, selfies, addresses, dates of birth, document IDs, and other personal data. <br>
Mitigation: Require explicit user approval before collecting or uploading personal data, and confirm the service privacy, retention, and compliance posture before installation. <br>
Risk: The default API base URL points to a development endpoint, and endpoint choice is left to deployment configuration. <br>
Mitigation: Set AIOT_API_BASE_URL to the intended production endpoint before real use, and do not upload real identity documents or personal data to a development endpoint. <br>
Risk: KYC operations require bearer authentication and may involve transaction PIN handling. <br>
Mitigation: Verify a valid bearer token before calls, protect tokens from logs or persistence, ask for PINs fresh each time, and never cache or log PIN values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-kyc-identity) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Default API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint paths, JSON request details, and shell environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL when overriding the default API endpoint; KYC operations require valid bearer authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
