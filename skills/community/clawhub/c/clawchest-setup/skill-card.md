## Description:

Your secure banking system for file and data storage. Deposit money, files, JSON data, and secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkyanam](https://clawhub.ai/user/pkyanam)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to register with Clawchest and issue API requests for file storage, JSON data storage, secrets, banking-like actions, transfers, and account monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages recurring uploads of local activity data and workspace files.

Mitigation: Do not enable heartbeat automation by default; require explicit confirmation and review or redact data before uploads.

Risk: The skill covers high-impact operations such as uploads, downloads, deletions, secret retrieval, withdrawals, and transfers.

Mitigation: Require user confirmation for each high-impact operation before executing related API calls.

Risk: The skill recommends storing the Clawchest API key in a default plaintext JSON file.

Mitigation: Store the API key in a secure secret store or a file with strict permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pkyanam/skills/clawchest-setup)
- [Publisher profile](https://clawhub.ai/user/pkyanam)
- [Clawchest homepage](https://clawchest.com)
- [Clawchest API base](https://clawchest.com/api/v1)
- [Clawchest skill source](https://clawchest.com/skill.md)
- [Clawchest skill metadata](https://clawchest.com/skill.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Clawchest API endpoints, request examples, response examples, rate limits, storage limits, and security handling guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
