## Description:

Export a bounded structured dataset (TikTok, Instagram, Amazon, YouTube and other EveryInfra platforms) with capability discovery, cost controls, pagination, deduplication and CSV or JSON verification. Use when the user asks for many records, all available pages, a dataset, or a CSV/JSON export rather than a single response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxihexiaoyu](https://clawhub.ai/user/xiaoxihexiaoyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to retrieve bounded datasets from EveryInfra-supported platforms for analysis or reporting. It guides capability discovery, controlled pagination, deduplication, and delivery as verified CSV or JSON, with explicit approval for material paid pulls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated paid export calls can incur charges.

Mitigation: Agree on row, call, and spending limits before a material pull, then stop when any limit is reached.

Risk: The service receives the API credential and export parameters.

Mitigation: Keep the key in secret settings and restrict it to the data capabilities needed for the export.

## Reference(s):

- [EveryInfra documentation and quickstart](https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everyinfra-bulk-data-export#quickstart)
- [EveryInfra API key restrictions](https://everyinfra.com/en/docs#authentication)
- [ClawHub skill release](https://clawhub.ai/xiaoxihexiaoyu/skills/everyinfra-bulk-data-export)

## Skill Output:

**Output Type(s):** [Files, CSV, JSON, Guidance, Shell commands, Configuration instructions]

**Output Format:** [CSV or JSON data files, with Markdown guidance and shell commands for setup and reporting]

**Output Parameters:** [Structured records with selected fields, bounded by requested row, call, and spending limits]

**Other Properties Related to Output:** [Deduplicated records; output files are checked for existence, non-empty content, and parseability.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
