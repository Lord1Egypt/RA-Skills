## Description:

Deep domain research for entity extraction, cross-article connections, and structured domain reports from a local knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dainash](https://clawhub.ai/user/dainash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to analyze harvested knowledge articles by domain, extract recurring entities, map cross-article relationships, and produce source-attributed research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local harvested knowledge markdown and may include private or unrelated material if the knowledge directory is too broad.

Mitigation: Run it only against the intended domain subset and review source lists before generating reports.

Risk: Entity extraction and connection mapping use shell-based text matching, so reports may contain missed entities, false positives, or weak relationships.

Mitigation: Review generated entity maps and connection claims against the cited source articles before using the report for decisions.

Risk: The skill writes source whitelist files and research reports under memory/.

Mitigation: Inspect generated files before sharing them and keep sensitive knowledge bases separate from publishable research outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dainash/skills/clawforage-research-agent)
- [Publisher Profile](https://clawhub.ai/user/dainash)
- [InspireHub.ai](https://inspireehub.ai)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown reports with source lists, entity maps, connection analysis, and validation output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads existing knowledge markdown and writes reports under memory/research/{domain}/ plus source whitelist files under memory/clawforage/sources/.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
