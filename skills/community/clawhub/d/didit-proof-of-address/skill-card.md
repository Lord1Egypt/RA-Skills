## Description:

Helps developers integrate Didit’s Proof of Address API to verify address documents and return extracted details, checks, and warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Didit’s standalone Proof of Address API into backend applications, submitting address documents and optionally checking extracted details against expected identity or address data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proof-of-address documents and related fields are sent to Didit, and an API key is required.

Mitigation: Submit only documents and fields you are authorized to share, and keep DIDIT_API_KEY in a secure environment variable.

Risk: The security scan has partial coverage because some referenced materials could not be resolved.

Mitigation: Review the complete skill and its referenced materials before deployment.

## Reference(s):

- [Didit Proof of Address API](https://docs.didit.me/standalone-apis/proof-of-address)
- [Proof of Address feature guide](https://docs.didit.me/core-technology/proof-of-address/overview)
- [Proof of Address warnings](https://docs.didit.me/core-technology/proof-of-address/warnings-proof-of-address)
- [Didit pricing](https://didit.me/pricing)

## Skill Output:

**Output Type(s):** [Code, Shell commands, JSON, Guidance]

**Output Format:** [Python integration code, JSON verification results, and a short text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY and an address document; API requests may be billed.]

## Skill Version(s):

1.4.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
