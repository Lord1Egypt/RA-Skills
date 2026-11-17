## Description:

Documentation extraction and indexing. Extracts information from markdown files and syncs to workspace-db. Works alongside workspace-db which handles synchronization and organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use Doc Scraper to extract structured metadata from Markdown documentation, index it in docs.db, and keep extracted records updated as files change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad indexing or watch-mode targets can store metadata from private Markdown documents in docs.db.

Mitigation: Use narrow --dir or --file targets first, review what will be indexed, and enable watch mode only for documentation folders intended for indexing.

## Reference(s):

- [workspace-db Skill](https://clawhub.com/skills/workspace-db)
- [DATABASE_AND_TREE_TRACKING.md](../docs/reference/DATABASE_AND_TREE_TRACKING.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript, YAML, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include indexing, search, watch-mode, extraction-template, and workspace-db integration examples.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
