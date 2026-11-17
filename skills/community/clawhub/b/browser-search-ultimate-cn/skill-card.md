## Description:

A Chinese web-search helper that retrieves Bing China search results and returns concise answer snippets plus a deduplicated result list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chn012cjus](https://clawhub.ai/user/chn012cjus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run Chinese-language web searches for domestic information, news, hot topics, and general queries, with output formatted for quick summarization and source review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to external providers such as Bing China.

Mitigation: Do not use the skill for secrets, credentials, private internal project names, or other sensitive queries.

Risk: Search summaries may be noisy or incomplete because they are extracted from search result HTML and only Bing is described as stable.

Mitigation: Review source URLs and verify important claims before relying on the summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chn012cjus/skills/browser-search-ultimate-cn)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text search summary and result list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries are sent to external search providers; the freshness parameter is reserved but not implemented.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
