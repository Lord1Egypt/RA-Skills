## Description:

Brand Sentinel searches public web results for brand-related reputation signals, deduplicates URLs, filters by recency, and returns structured results for agent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbniao100](https://clawhub.ai/user/bbniao100)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to monitor recent public brand or product mentions, gather potentially negative reputation signals, and prepare structured search results for separate LLM-based risk review or alerting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships an embedded API application key and depends on a local token service.

Mitigation: Rotate the embedded key, move credentials out of source, and run the token service only in a trusted local environment.

Risk: The brand argument may not be included in searches unless each keyword already contains the brand name.

Mitigation: Validate configuration and include the brand in every keyword before relying on monitoring results.

Risk: Public web search results and date parsing may retain undated or stale items.

Mitigation: Review returned items before escalation, especially results with unknown dates or incomplete snippets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbniao100/skills/brand-sentinel)
- [Publisher profile](https://clawhub.ai/user/bbniao100)
- [Example configuration](references/config-example.json)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [Plain text summary or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output includes brand, run time, time window, keywords, result counts, and items with title, URL, snippet, date status, and parsed date when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
