## Description:

Find recent arXiv papers, skip what is already in Zotero, and save new imports with parent-item tagging and PDF attachments into a dedicated collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnicpyx](https://clawhub.ai/user/cnicpyx)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and Zotero users use this skill to search recent arXiv papers by topic and time range, deduplicate against their Zotero library, and import new papers with PDF attachments into a dedicated collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads ~/.openclaw/.env and may over-read unrelated secrets stored in that shared file.

Mitigation: Use a dedicated Zotero API key with the minimum required permissions and avoid storing unrelated secrets in ~/.openclaw/.env.

Risk: PDF downloads have insufficient host, redirect, and size restrictions before upload attempts.

Mitigation: Review before installation and restrict PDF downloads to expected arXiv HTTPS hosts with redirect and size limits, or disable PDF attachment behavior if that risk is unacceptable.

Risk: Runs can create Zotero items, attachments, and a collection in the configured library.

Mitigation: Confirm the target Zotero library and collection settings before use, and use a narrowly scoped Zotero API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnicpyx/skills/arxiv-to-zotero)
- [Publisher profile](https://clawhub.ai/user/cnicpyx)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown text with a direct Python command invocation and final run summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Zotero parent items, attachments, and a target collection through the Zotero Web API; can optionally write a JSON run summary when configured.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
