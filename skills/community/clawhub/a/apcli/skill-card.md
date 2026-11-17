## Description:

Search, read and edit Apple Contacts from the command line on macOS: find people by name, nickname or company, show a card, create, update and delete contacts, with JSON output for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopaljigaur](https://clawhub.ai/user/gopaljigaur)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent on macOS can find and inspect contacts, or create, update, and delete contact records through a command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact updates or deletion can affect records in synchronized accounts.

Mitigation: Search first and verify the selected contact and requested changes; keep deletion confirmation enabled and use --yes only with explicit authorization.

Risk: The JXA scripts that perform contact access and changes were absent from the supplied files, and macOS behavior was not tested.

Mitigation: Review the npm release and its JXA scripts before granting Contacts access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gopaljigaur/skills/apcli)
- [Source repository listed in package metadata](https://github.com/gopaljigaur/apcli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON contact records or errors; human-readable text; shell commands for operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited to 50 by default and can be adjusted with --limit.]

## Skill Version(s):

0.1.2 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
