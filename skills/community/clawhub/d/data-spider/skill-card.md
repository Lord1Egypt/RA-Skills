## Description: <br>
Scrape any webpage and extract structured data as JSON, table, or list. Supports schema-guided extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users can use this skill to extract product data, pricing, statistics, article facts, or dataset rows from webpages into structured JSON, table, or list output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs, extraction instructions, schemas, and resulting page content are sent to AIProx and its downstream model provider. <br>
Mitigation: Use only on pages and data you are authorized to share with those services; avoid private dashboards, authenticated pages, intranet hosts, localhost, cloud metadata endpoints, and sensitive regulated content unless approved. <br>
Risk: The AIPROX_SPEND_TOKEN may authorize paid API usage. <br>
Mitigation: Store the token as a protected environment secret, restrict access to trusted agents, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Data Spider ClawHub page](https://clawhub.ai/unixlamadev-spec/data-spider) <br>
- [AIProx homepage](https://aiprox.dev) <br>
- [AIProx orchestration endpoint](https://aiprox.dev/api/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured extraction results as JSON object, table columns and rows, or flat list with summary, source URL, and format.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
