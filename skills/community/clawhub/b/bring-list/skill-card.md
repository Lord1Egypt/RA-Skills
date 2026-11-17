## Description:

Manage Bring! shopping lists (Einkaufsliste / grocery list) by adding, catalog-matching, previewing, removing, checking off, batch-importing, and showing items while keeping setup passwords in the user's own terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikimolto](https://clawhub.ai/user/maikimolto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to manage Bring! shopping lists from conversation or shell workflows, including setup guidance, list viewing, item additions, completion, restoration, removal, batch operations, dry-run previews, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change Bring! shopping lists.

Mitigation: Use it only for lists the user authorizes, preview modifying commands with --dry-run when uncertain, and confirm permanent removals before execution.

Risk: The cached Bring! access and refresh token is sensitive.

Mitigation: Run setup in the user's own terminal, never paste the Bring! password into chat, and keep the token cache owner-only.

Risk: Changes to shared Bring! lists sync immediately to other people.

Mitigation: Tell the user when a shared list may be affected and confirm destructive actions before changing shared lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maikimolto/skills/bring-list)
- [Bring! service](https://getbring.com)
- [Bring! REST API endpoint used by the skill](https://api.getbring.com/rest)
- [Bring! catalog endpoint used by the skill](https://web.getbring.com/locale)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; modifying operations support dry-run previews.]

## Skill Version(s):

1.3.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
