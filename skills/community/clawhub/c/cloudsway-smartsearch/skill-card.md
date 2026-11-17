## Description:

Smartsearch helps agents search the web through Cloudsway SmartSearch to retrieve up-to-date online information, news, research data, and fact-checking results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prismheart](https://clawhub.ai/user/prismheart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use this skill to search the web, retrieve current news and research, verify facts, and optionally fetch webpage text through the Cloudsway API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, filters, and optionally extracted web content are sent to the Cloudsway service.

Mitigation: Do not include secrets, proprietary context, or personal data in searches.

Risk: Troubleshooting commands that print the API key can expose credentials.

Mitigation: Use a presence check instead of printing the CLOUDSWAYS_AK value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prismheart/skills/cloudsway-smartsearch)
- [Cloudsway homepage](https://cloudsway.ai)
- [Cloudsway SmartSearch API endpoint](https://aisearchapi.cloudsway.net/api/search/smart)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON search results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLOUDSWAYS_AK; optional response fields can include snippets, extracted content, main text, URLs, and publication dates.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
