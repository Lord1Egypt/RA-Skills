## Description:

Use Chanjing text-to-digital-person APIs for AI portraits, talking videos, optional LoRA training, polling, and explicit downloads when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Chanjing text-to-digital-person image tasks, turn generated portraits into talking videos, poll asynchronous task status, optionally run LoRA training, and download completed outputs only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API secrets and persists an access token on disk.

Mitigation: Store credentials only in the configured Chanjing credentials directory, protect credentials.json with restrictive permissions, and do not commit it to version control.

Risk: Changing the API base URL can redirect credentialed requests outside the expected Chanjing service.

Mitigation: Use CHANJING_OPENAPI_BASE_URL or legacy CHANJING_API_BASE only in controlled testing and keep production use on trusted, allowlisted Chanjing hosts.

Risk: Downloaded result URLs write files to the local workspace or an explicit output path.

Mitigation: Download only trusted result URLs and use a dedicated output directory for generated media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binkes/skills/chanjing-text-to-digital-person)
- [Chanjing OpenAPI Documentation](https://doc.chanjing.cc)
- [Artifact Reference](artifact/reference.md)
- [Artifact Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Files, Configuration guidance]

**Output Format:** [Plain text task identifiers, URLs, JSON task details, and local file paths from CLI scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on asynchronous Chanjing API task state; downloads are explicit and write to a local output path.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
