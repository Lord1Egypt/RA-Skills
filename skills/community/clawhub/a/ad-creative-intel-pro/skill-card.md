## Description:

广告情报专业版 helps media-buying, campaign optimization, and market research teams use a paid ad intelligence API for bulk creative export, historical trend review, multi-market comparison, creative attribution, and estimated download or revenue analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to prepare API calls and analysis workflows for paid advertising intelligence research. It supports bulk ad creative export, historical campaign review, market comparison, attribution-oriented reporting, and estimated app download or revenue analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if copied into prompts, command history, logs, or generated files.

Mitigation: Store ADC_INTEL_API_KEY in an environment variable or credential store, avoid echoing it, and review generated commands before execution.

Risk: Search terms, product identifiers, market filters, and API responses are sent to a third-party ad intelligence service.

Mitigation: Submit only data that is approved for third-party processing and avoid sending confidential campaign or customer information unless the service terms permit it.

Risk: Bulk export and scheduled dashboard workflows can create high-volume external API usage.

Mitigation: Scope exports deliberately, monitor quota and rate limits, and review scheduled jobs before enabling automated runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ad-creative-intel-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Ad Creative Intel quota status API](https://api.ad-creative-intel.com/api/quota/status)
- [Ad Creative Intel search API](https://api.ad-creative-intel.com/api/data/search)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide synchronous HTTP API calls and produce raw JSON, comparison matrices, and human-readable analysis notes.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
