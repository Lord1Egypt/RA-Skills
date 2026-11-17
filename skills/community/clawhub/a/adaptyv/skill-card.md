## Description:

Guides agents in using the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzk1121](https://clawhub.ai/user/yzk1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioengineering teams use this skill to authenticate with the Adaptyv Foundry API, design protein assays, submit experiments, manage quotes and tokens, and retrieve lab results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Experiment submission, skip_draft, quote acceptance, and invoice creation can create cost or operational commitments.

Mitigation: Require explicit user approval before submitting experiments, accepting quotes, creating invoices, or enabling skip_draft or auto_accept_quote.

Risk: API tokens can authorize access to lab resources, and token revocation affects token descendants.

Mitigation: Use scoped or attenuated tokens where possible, protect .env credentials, and require approval before revoking tokens.

Risk: Unpinned SDK dependencies may change behavior in controlled environments.

Mitigation: Pin or lock the adaptyv SDK dependency for reproducible deployments.

## Reference(s):

- [Adaptyv Bio Foundry API endpoint reference](references/api-endpoints.md)
- [Adaptyv Foundry portal](https://foundry.adaptyvbio.com/)
- [Adaptyv Foundry API base URL](https://foundry-api-public.adaptyvbio.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/yzk1121/skills/adaptyv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated API calls and lab-submission workflows that require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
