## Description:

谷歌搜索(专业版) helps agents run batch and specialized Google searches, summarize results with an LLM, monitor keywords, search across languages, and cache or export search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, market researchers, product teams, and communications teams can use this skill to collect Google search results in bulk, summarize findings, monitor keyword changes, and prepare structured reports. It is not suitable for decisions that require fully deterministic or independently verified results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad execution permissions and setup commands can run tooling or installation steps outside the narrow search workflow.

Mitigation: Review commands before execution, prefer package-manager or manual installation steps, and run the skill in a sandboxed workspace with least-privilege access.

Risk: Search queries, result snippets, proxy traffic, LLM summaries, and webhook alerts may expose sensitive or confidential information to third-party services.

Mitigation: Use non-sensitive queries, avoid confidential inputs, control proxy and webhook destinations, and confirm that downstream services are approved for the data being sent.

Risk: Caching and scheduled monitoring can retain or repeatedly transmit search results and keyword data.

Mitigation: Choose non-sensitive monitored keywords, set short cache retention where possible, periodically purge cached results, and disable monitoring when it is no longer needed.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/free-google-search-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [JSON responses, Markdown reports, code snippets, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include search result data, execution logs, summaries, cached results, monitoring alerts, and exports in JSON, Markdown, or CSV.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
