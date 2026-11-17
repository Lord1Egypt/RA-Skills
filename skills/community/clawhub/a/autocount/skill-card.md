## Description:

Create and validate AutoCount business documents through AutoCount Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teckyuen](https://clawhub.ai/user/teckyuen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business automation teams use this skill to create, validate, inspect, and test AutoCount sales, purchase, transfer, and master-data workflows through the AutoCount Web API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents API-key access over plain HTTP in the observed AutoCount environment.

Mitigation: Use only trusted AutoCount environments protected by HTTPS, VPN, or another secure tunnel, and prefer a dedicated least-privilege API key.

Risk: The skill supports live financial record posting, update, cancel, and delete workflows.

Mitigation: Test in drafts or a sandbox first, and require explicit confirmation before final posting, update, cancel, or delete operations.

## Reference(s):

- [AutoCount Invoice Test Notes](references/test-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload examples and HTTP request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft-first workflow recommendations, request payloads, endpoint choices, and post-create verification steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
