## Description:

Manage Apple Calendar events from the command line on macOS — create, update, delete, search, export, and check availability with full JSON output for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopaljigaur](https://clawhub.ai/user/gopaljigaur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill on macOS to inspect, create, update, delete, search, export, and check availability for Apple Calendar events through the accli command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install an unpinned third-party npm package.

Mitigation: Review the npm package provenance before installing and prefer a pinned, reviewed version with integrity verification.

Risk: The CLI requires Full Calendar access and can read, export, create, update, and delete events.

Mitigation: Grant Calendar access only when that authority is acceptable, use --json for auditable responses, and use --dry-run before destructive update or delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gopaljigaur/skills/accli-plus)
- [npm package @gopaljigaur/accli](https://www.npmjs.com/package/@gopaljigaur/accli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline bash code blocks and JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; accli commands should use --json for programmatic parsing and --dry-run before destructive update or delete operations.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
