## Description:

Archives referenced ebook originals, including ebooks inside supported archives, in Calibre with source URLs and useful tags while excluding Web clips and unused search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers use this skill to add the original ebook files they actually reference to an existing Calibre library, with source URLs and useful tags. It is intended for use under a standing auto-save instruction or an explicit archival request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mistaken selection could add irrelevant or duplicate books to the configured Calibre library.

Mitigation: Save only a finite set of original ebooks actually referenced in research, check candidates before import, and repeat duplicate lookup during plan application.

Risk: Archive contents may include unsupported or unsafe entries.

Mitigation: Inventory archives first and import only selected ebook members; reject unsupported, encrypted, linked, special, or path-unsafe entries.

## Reference(s):

- [Calibre Reference Ingest on ClawHub](https://clawhub.ai/nextaltair/skills/calibre-reference-ingest)
- [Calibre Catalog Read](https://clawhub.ai/nextaltair/skills/calibre-catalog-read)
- [Calibre Metadata Apply](https://clawhub.ai/nextaltair/skills/calibre-metadata-apply)
- [calibredb Command-Line Interface](https://manual.calibre-ebook.com/generated/en/calibredb.html)
- [Calibre Supported Formats](https://manual.calibre-ebook.com/faq.html#what-formats-does-calibre-support-conversion-to-from)
- [libarchive](https://github.com/libarchive/libarchive)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [JSON import manifests and plans, shell commands, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves ebook originals during staging and records source and archive identity; imports target the configured Calibre library.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
