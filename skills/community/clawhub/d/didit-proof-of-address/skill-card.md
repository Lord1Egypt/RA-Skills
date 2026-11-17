## Description:

Integrate Didit Proof of Address standalone API to verify address documents, including utility bills, bank statements, and government documents, with OCR extraction, geocoding, name matching, and multi-page document support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to integrate Didit proof-of-address checks into onboarding, KYC, compliance, or account verification workflows. It helps submit address documents, interpret verification statuses and warnings, and run a command-line verification helper with a DIDIT_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proof-of-address files and extracted address data are highly sensitive and are sent to Didit's third-party API.

Mitigation: Use the skill only with explicit user consent, confirm privacy and retention requirements before deployment, and restrict access to documents and API results.

Risk: The default API parameter described by the artifact saves requests in the Business Console unless disabled.

Mitigation: Prefer setting save_api_request to false when retention is not required, and document any retention choice for compliance review.

Risk: The utility script prints full JSON responses that may include names, addresses, document URLs, and warning details.

Mitigation: Avoid running it in logged automation environments and redact or suppress personal data in console output before sharing logs.

Risk: The DIDIT_API_KEY grants access to the Didit API and is required by the helper script.

Mitigation: Store the key in a secret manager or protected environment variable, rotate it if exposed, and avoid hardcoding it in prompts, scripts, or logs.

## Reference(s):

- [Didit Documentation Homepage](https://docs.didit.me)
- [Didit Proof of Address API Reference](https://docs.didit.me/standalone-apis/proof-of-address)
- [Didit Proof of Address Feature Guide](https://docs.didit.me/core-technology/proof-of-address/overview)
- [Didit Business Console](https://business.didit.me)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload proof-of-address documents to Didit's API and print structured verification responses containing personal data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
