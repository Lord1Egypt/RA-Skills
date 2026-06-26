## Description: <br>
Agent-first service to register and manage Human Bitcoin Addresses (BIP-353) on clank.money with L402 bitcoin payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matbalez](https://clawhub.ai/user/matbalez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through registering a clank.money Human Bitcoin Address and updating the BIP-321 URI it resolves to after registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The management token controls future updates to the Human Bitcoin Address and can be exposed if stored in predictable temporary files. <br>
Mitigation: Store the token only in a private file with restrictive permissions, replace shared temporary paths with private temporary files, and delete temporary JSON files after registration. <br>
Risk: A user could pay an invoice or update an address using an unintended username, invoice, or BIP-321 URI. <br>
Mitigation: Verify the username, Lightning invoice, and BIP-321 URI before paying or submitting updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matbalez/get-hba) <br>
- [clank.money registrations API](https://clank.money/api/v1/registrations) <br>
- [clank.money service](https://clank.money) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash code blocks and API endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment-challenge handling and local management-token storage instructions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
