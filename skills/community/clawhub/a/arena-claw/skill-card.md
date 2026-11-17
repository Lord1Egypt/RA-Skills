## Description:

are.na claw is a simple CLI wrapper for the are.na API that lists channels, adds blocks, watches feeds, and makes explicit API calls without AI automation or external integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koellins](https://clawhub.ai/user/koellins)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to manage are.na channels and blocks through the `arena` CLI, including listing channel contents, adding image or link blocks, watching channel changes, and switching accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents and installs an `arena` executable, but the actual executable source is not present in the artifact and the install guidance points to a mutable placeholder GitHub source.

Mitigation: Do not provide an are.na API token until the executable source is included or replaced by a verified, pinned release with checksum or signature validation.

Risk: The CLI stores are.na API tokens in local token files.

Mitigation: Inspect the executable before use, restrict token-file permissions, and revoke the are.na token if the install source cannot be trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koellins/skills/arena-claw)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include are.na CLI command examples and API-oriented guidance; no AI-generated curation is claimed.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
