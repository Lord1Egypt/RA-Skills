## Description:

Find, compare, and obtain datasets or data lakes across ML repositories, cloud public data registries, government portals, scientific archives, geospatial/climate catalogs, NLP corpora, and generic web dataset indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data scientists use this skill to turn dataset needs into a structured brief, search public catalogs and data lakes, compare candidates, and prepare guarded acquisition plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset queries and structured briefs may be sent to external catalog providers.

Mitigation: Use --offline or restrict searches with a narrow --source list for sensitive work.

Risk: Approved acquisition plans can download arbitrary URLs or run source CLI commands.

Mitigation: Avoid --url and untrusted --from-results files, inspect dry-run plans, and use --yes only after review.

## Reference(s):

- [ClawHub Dataset Search Skill](https://clawhub.ai/carlosdelfino/skills/dataset-search)
- [Publisher Profile](https://clawhub.ai/user/carlosdelfino)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON with dataset candidates, source links, caveats, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search can run offline for guided links; download commands default to dry-run plans unless explicitly approved with --yes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
