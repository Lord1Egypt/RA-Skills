## Description:

Make a static site answer-engine-citable by adding JSON-LD, clean Markdown siblings, llms.txt, and sitemap.xml so answer engines can parse and cite it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and web teams use this skill to audit static HTML sites and apply machine-readable citation improvements. It helps prepare pages for answer-engine citation by adding structured data, clean text surfaces, llms.txt, and sitemap.xml.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write commands can edit HTML in place or create new Markdown, llms.txt, and sitemap.xml files.

Mitigation: Run audit and dry-run first, use version control or backups, and target the specific static-site directory.

Risk: Generated structured data or FAQ content can misrepresent a page if supplied values are inaccurate.

Mitigation: Review generated JSON-LD, FAQ answers, and metadata before publishing or requesting recrawl.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workloftai/skills/aeo-citability)
- [Publisher profile](https://clawhub.ai/user/workloftai)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Workloft Ships](https://workloft.ai/ships)
- [Workloft Labs](https://workloft.ai/labs/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local static-site file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify static-site files; dry-run is available for write commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and clawhub.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
