## Description:

Provides guidance and code for integrating Didit's standalone AML screening API to screen people or companies, review potential matches, and configure ongoing monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Didit AML screening into backend services and API-key workflows. It guides request setup, scoring configuration, hit review, safe retries, and optional ongoing monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening data and API credentials are sent to an external service.

Mitigation: Before use, confirm you trust Didit and are comfortable sending the screening data and credentials to it.

Risk: The security scan was partial, so its evidence is incomplete.

Mitigation: Treat the benign verdict as limited evidence and review the skill and its use before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosasalberto/skills/didit-aml-screening)
- [Didit AML Screening API](https://docs.didit.me/standalone-apis/aml-screening)
- [AML Screening feature guide](https://docs.didit.me/core-technology/aml-screening/overview)
- [AML Match Score](https://docs.didit.me/core-technology/aml-screening/aml-match-score)
- [AML Risk Score](https://docs.didit.me/core-technology/aml-screening/aml-risk-score)
- [Didit pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples, JSON request and response examples, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Python command-line helper script.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
