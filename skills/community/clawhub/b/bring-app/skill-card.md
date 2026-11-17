## Description:

Manage Bring! shopping lists via CLI to add, remove, complete, and view items or lists using the Bring! API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joekravelli](https://clawhub.ai/user/joekravelli)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Bring! account use this skill to let an agent view and update Bring! shopping lists, including adding, removing, completing, and listing items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bring! credentials may be stored in a plaintext JSON file.

Mitigation: Prefer environment variables or an OS secret store; if the JSON file is used, restrict it to owner-only permissions.

Risk: The skill can mutate a third-party shopping-list account by adding, removing, or completing items.

Mitigation: Confirm the Bring! account, target list, and requested item before executing mutating actions.

Risk: The unpinned bring-api dependency receives the user's Bring! password.

Mitigation: Pin and review the bring-api dependency before deployment or routine use.

## Reference(s):

- [miaucl/bring-api](https://github.com/miaucl/bring-api)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Bring! credentials and an optional target list name to read or mutate shopping-list state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
