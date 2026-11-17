## Description:

Manage linkding bookmarks - save URLs, search, tag, organize, and retrieve your personal bookmark collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveonkels](https://clawhub.ai/user/daveonkels)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage a personal linkding bookmark library from the terminal, including saving URLs, searching bookmarks, organizing tags and bundles, and retrieving unread items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run destructive bookmark operations such as delete, archive, and batch updates.

Mitigation: Review affected bookmark IDs and command intent before allowing delete, archive, asset deletion, or batch-update commands to run.

Risk: The clinkding CLI requires access to a linkding API token.

Mitigation: Use a revocable token, avoid exposing it in shared logs, and prefer environment or config storage appropriate for the host system.

Risk: The release provenance is unavailable in server evidence.

Mitigation: Verify the clinkding source and release before installation, and prefer a pinned version or checksum-verified binary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daveonkels/skills/clinkding)
- [clinkding GitHub repository](https://github.com/daveonkels/clinkding)
- [linkding GitHub repository](https://github.com/sissbruecker/linkding)
- [clinkding releases](https://github.com/daveonkels/clinkding/releases)
- [Homebrew formula](daveonkels/tap/clinkding)
- [Go module](github.com/daveonkels/clinkding@latest)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Text]

**Output Format:** [Markdown with inline bash code blocks and command-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bookmark data in human-readable tables, JSON, or plain text depending on selected clinkding flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
