## Description:

Search, browse, and manage Audible audiobooks, including catalogue search, library viewing, book details, purchases after confirmation, and wishlist management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeathridge](https://clawhub.ai/user/ryandeathridge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Audible, inspect audiobook details, view an authenticated Audible library, manage a wishlist, and initiate purchases only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Audible login material at ~/.config/audible/auth.json.

Mitigation: Protect the auth file as a sensitive secret, keep owner-only permissions, exclude it from unsafe backups, and remove it when the skill is no longer used.

Risk: The skill auto-installs unpinned Python dependencies on first run.

Mitigation: Review or preinstall the audible and httpx dependencies in a controlled environment before running the scripts.

Risk: The skill can read an Audible library, modify a wishlist, and make purchases after confirmation.

Mitigation: Use the skill only with accounts where that access is acceptable, and require explicit user confirmation before any purchase command.

Risk: The skill relies on an unofficial Audible integration that may break if the service changes.

Mitigation: Verify search, library, wishlist, and purchase workflows in the target marketplace before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryandeathridge/skills/clawdible-audiobooks)
- [Publisher profile](https://clawhub.ai/user/ryandeathridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples; script output may also be JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against a local Audible auth file and a selected marketplace locale.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
