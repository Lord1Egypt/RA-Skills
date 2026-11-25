## Description:

Helps agents write backend integrations with Didit's standalone APIs for identity document verification and digital ID wallet sign-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build integrations that submit identity document images or PDFs to Didit's verification APIs, handle verification results, or start supported digital ID wallet sign-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification requests involve identity document images and an API key, and saved API requests may retain verification sessions and images.

Mitigation: Share document data only when approved for the use case, keep DIDIT_API_KEY in a secret store, and set save_api_request to false when session storage is unnecessary.

Risk: The security review reports incomplete reference-resolution coverage, so its benign verdict does not establish that the artifact is risk-free.

Mitigation: Review the skill and its referenced components before deployment, and confirm that the required data sharing and credential scope fit the application.

## Reference(s):

- [Didit ID Verification API Reference](https://docs.didit.me/standalone-apis/id-verification)
- [Didit Digital ID Wallets API Reference](https://docs.didit.me/standalone-apis/digital-id-wallets)
- [ID Verification Feature Guide](https://docs.didit.me/core-technology/id-verification/overview)
- [ID Verification Warnings](https://docs.didit.me/core-technology/id-verification/warnings-id-verification)
- [Supported Documents](https://docs.didit.me/core-technology/id-verification/supported-documents-id-verification)
- [Didit Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes request setup, response handling, and operational guidance for identity verification integrations.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
