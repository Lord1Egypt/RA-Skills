## Description:

Prepares a sourced, fact-checked briefing on a living person before a meeting, delivered as a two-page Word document and matching chat text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeypetrakov](https://clawhub.ai/user/sergeypetrakov)

### License/Terms of Use:

MIT-0

## Use Case:

Professionals preparing for a meeting use this skill to research a living person's public background, verify claims, and identify relevant discussion topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Researching living people can expose sensitive personal information and sends the subject's name, searches, and factual claims to Perplexity.

Mitigation: Use only for authorized professional research; obtain appropriate approval for external sharing and keep private or sensitive details out of the dossier.

Risk: Input resolution can read sibling task files in a shared environment.

Mitigation: Avoid shared or multi-tenant task drives until input resolution is restricted to the current task; protect local dossier and research files.

Risk: Fetching cited URLs can reach local, private, or internal network targets.

Mitigation: Block local and internal network destinations before enabling cited-URL fetching.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sergeypetrakov/skills/dossier)
- [Search playbook](references/search-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Two-page Word (.docx) dossier and matching Russian chat text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes numbered sources and fact-checking; requires a Perplexity API key and python-docx.]

## Skill Version(s):

1.1.8 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
