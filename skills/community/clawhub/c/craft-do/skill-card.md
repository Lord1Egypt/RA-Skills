## Description:

Integrate with Craft.do to automate tasks, create and manage documents and folders, edit markdown content, and migrate Obsidian vaults using the Craft REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomtanstudio](https://clawhub.ai/user/atomtanstudio)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate Craft.do documents, folders, tasks, and markdown content. It also supports one-time migration of Obsidian vaults into Craft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful Craft API token for bulk uploads and destructive changes.

Mitigation: Use a narrowly scoped, revocable Craft API key, back up or export important Craft and Obsidian data before running scripts, and avoid unattended migration or cleanup runs.

Risk: The scripts trust the configured CRAFT_ENDPOINT.

Mitigation: Verify CRAFT_ENDPOINT is the official HTTPS Craft endpoint before every run.

Risk: The cleanup script can move documents to trash and delete user-created folders.

Mitigation: Run cleanup only after reviewing the target Craft space and confirming the interactive prompt intentionally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atomtanstudio/skills/craft-do)
- [Craft API Documentation](https://craft.do/api)
- [Craft Blog - Collections](https://www.craft.do/blog/introducing-collections)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Bash scripts, curl examples, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Craft API key, a Craft endpoint, curl, jq, and an Obsidian vault path when running migration scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-01-31T18:55:20Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
