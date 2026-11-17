## Description:

Website Audit mit 230+ Rules fuer SEO, Performance, Security, Technical und Content Issues. LLM-optimierte Reports mit Health Scores und Handlungsempfehlungen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO teams use this skill to audit websites for SEO, performance, security, technical, and content issues and receive health scores with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced squirrel audit tool is not included in the skill artifact.

Mitigation: Confirm that the installed audit tool is expected and trusted before using the skill.

Risk: Website audits crawl user-provided URLs and can generate reports about third-party or sensitive sites.

Mitigation: Run audits only for authorized sites and review generated reports before sharing them.

## Reference(s):

- [LLM Format Output Reference](artifact/references/OUTPUT-FORMAT.md)
- [ClawHub skill page](https://clawhub.ai/akkualle/skills/akkualle-audit-website)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and references to text, JSON, and compact XML audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit reports may include health scores, issue lists, affected pages, metrics, and recommended fixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
