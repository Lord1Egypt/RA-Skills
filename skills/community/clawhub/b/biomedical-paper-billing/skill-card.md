## Description:

AI-powered biomedical manuscript generation with DOCX output for biomedical research papers and Chinese theses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baronshang-blip](https://clawhub.ai/user/baronshang-blip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and biomedical researchers use this skill to turn Chinese drafts or outlines into English biomedical manuscripts or Chinese thesis sections with structured sections, Vancouver references, and DOCX formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscript citation details may be sent to external search services during reference verification.

Mitigation: Require user approval before external lookups and avoid including unpublished, patient-adjacent, or confidential details in search queries.

Risk: Automatic reference addition or replacement can introduce citation errors or unintended source changes.

Mitigation: Present proposed replacements and a citation mapping table for review before finalizing manuscripts or DOCX files.

Risk: Biomedical manuscript outputs can affect publication, thesis, or research decisions if unchecked.

Mitigation: Review factual claims, statistics, references, and formatting against source data and journal or institution requirements before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baronshang-blip/skills/biomedical-paper-billing)
- [GBD Results Tool](http://ghdx.healthdata.org/gbd-results-tool)
- [Journal Style Guide](references/style-guide.md)
- [Section Templates](references/section-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown manuscript drafts, Python DOCX generation code, and DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vancouver-style references, citation mapping tables, and journal or thesis formatting guidance.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
