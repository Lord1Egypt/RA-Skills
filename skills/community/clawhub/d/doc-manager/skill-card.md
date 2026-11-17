## Description:

Manages document generation, storage, tracking, and URL access for professional documents, reports, analyses, and guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[171622474](https://clawhub.ai/user/171622474)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and content-producing agents use this skill to create, store, list, update, and archive Markdown documents with metadata, timestamped folders, and direct access URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documents can be written persistently and exposed through public HTTP URLs and index pages.

Mitigation: Do not use the skill for confidential, personal, credential-bearing, or internal-only content unless access controls and HTTPS are added.

Risk: Unsafe slug handling may allow writes outside the intended documents directory when slug input is untrusted.

Mitigation: Validate slugs against an allowlist, reject path separators and traversal sequences, and verify resolved paths stay under the documents root before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/171622474/skills/doc-manager)
- [Document index URL](http://45.197.148.41:18792/docs/INDEX.md)
- [Document URL pattern](http://45.197.148.41:18792/docs/doc-{YYYYMMDD}-{slug}/content.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON metadata, shell commands, configuration]

**Output Format:** [Markdown documents, JSON metadata, index listings, and direct URL strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent document folders and index entries; generated documents may be reachable through configured HTTP URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
