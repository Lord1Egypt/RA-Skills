## Description:

Searches public medical literature across bibliographic sources, merges and verifies citations, and prepares evidence reports and open-access PDF downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Clinical-trial practitioners, clinicians, and medical students use this skill to find and organize published evidence about a drug, disease, or method. It helps build a deduplicated literature set, verify citations, and prepare reports for background research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags reported remote processing and logging of searches or imported bibliographic data, plus filesystem access beyond the stated literature-search scope.

Mitigation: Keep confidential or identifying material out of queries and imports; review the configured remote endpoints and filesystem permissions before running the skill.

## Reference(s):

- [Capabilities and data sources](artifact/references/capabilities.md)
- [Standard operating procedure](artifact/references/sop.md)
- [Citation styles and exports](artifact/references/citation_styles.md)
- [Clinical Trial Literature Search homepage](https://github.com/medstatstar/ct-literature)
- [Clinical Trial Literature Search workbench](https://ct-literature.app.workbuddy.host/)
- [ClawHub skill page](https://clawhub.ai/medstatstar/skills/ct-literature)

## Skill Output:

**Output Type(s):** [HTML reports, Excel workbooks, Citation files, PDF files, Markdown notes, Search and evidence guidance]

**Output Format:** [HTML, Excel (.xlsx), BibTeX/RIS/CSV, PDF, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports organize deduplicated records and source coverage; optional outputs include citation exports, open-access PDFs, Zotero files, and Obsidian notes.]

## Skill Version(s):

1.7.10 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
