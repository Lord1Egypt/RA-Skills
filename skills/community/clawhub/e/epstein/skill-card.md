## Description:

Search 44,886+ DOJ-released Jeffrey Epstein documents by name, topic, location, or keyword across the DugganUSA index and return document previews, entity metadata, source references, and direct DOJ PDF links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuxo](https://clawhub.ai/user/chuxo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search a public index of DOJ-released Epstein document records, inspect matching metadata, and retrieve direct DOJ PDF links for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the DugganUSA analytics API.

Mitigation: Avoid submitting sensitive or private search terms unless that third-party API exposure is acceptable.

Risk: Search and stats commands depend on a third-party endpoint being reachable.

Mitigation: Treat API downtime or failed requests as an availability limitation and retry after confirming network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chuxo/skills/epstein)
- [DOJ Epstein Records](https://www.justice.gov/epstein)
- [DugganUSA Analytics](https://analytics.dugganusa.com)
- [Project Einstein](https://emc2ai.io)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON search or stats results on stdout with human-readable status and Quick Links on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requires network access to the DugganUSA analytics API and accepts a query string plus an optional result limit from 1 to 500.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
