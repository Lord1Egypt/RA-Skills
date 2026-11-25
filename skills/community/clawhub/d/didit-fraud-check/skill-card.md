## Description:

Helps developers build integrations that plan, run, and retrieve Didit Fraud Check and IP Risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build server-side integrations that assess fraud and identity risk, estimate check costs, and retrieve results through Didit's Fraud Check and IP Risk APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fraud checks can send sensitive identifiers, claimed identity details, IP addresses, or a selfie to Didit.

Mitigation: Confirm that Didit is an approved recipient for this information, send only fields needed for the selected checks, and obtain the required consent before biometric checks.

Risk: Running selected paid checks can incur charges.

Mitigation: Call the plan endpoint first and review its estimated price before running the check.

## Reference(s):

- [Didit Fraud Check API](https://docs.didit.me/standalone-apis/fraud-check)
- [Didit Fraud Check Plan API](https://docs.didit.me/standalone-apis/fraud-check-plan)
- [Didit Fraud Check Results API](https://docs.didit.me/standalone-apis/fraud-check-result)
- [Didit IP Risk API](https://docs.didit.me/standalone-apis/ip-risk)
- [Didit Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Python and TypeScript examples, CLI commands, and JSON API request and response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and integration guidance for the Didit Fraud Check and IP Risk APIs]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
