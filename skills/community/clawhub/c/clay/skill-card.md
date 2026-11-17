## Description:

Search, manage, and organize your contact network via the Clay CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khrrsn](https://clawhub.ai/user/khrrsn)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help Clay users search, create, update, and organize contacts, notes, groups, events, emails, and reminders through the Clay CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clay CLI output can include sensitive personal and third-party contact data.

Mitigation: Treat command output as sensitive and avoid exposing contacts, emails, notes, events, locations, birthdays, or interaction history in shared logs or transcripts.

Risk: Commands that update, archive, restore, merge, or change groups can affect contact records.

Mitigation: Confirm contact IDs and intended changes before running mutating Clay CLI commands.

Risk: Installing the CLI grants local workflows access to a Clay account after authentication.

Mitigation: Install only when Clay account access is intended, authenticate with `clay login`, and consider pinning or otherwise verifying the `@clayhq/clay-cli` package before installation.

## Reference(s):

- [Clay](https://clay.earth)
- [ClawHub Clay skill page](https://clawhub.ai/khrrsn/skills/clay)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Clay CLI session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
