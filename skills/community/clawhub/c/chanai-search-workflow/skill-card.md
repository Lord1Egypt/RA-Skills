## Description:

External web search workflow for Chinese and global public-web information. Use when searching news, flights, prices, products, docs, tutorials, community posts, websites, PDFs, research, or other external information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfyuanyi](https://clawhub.ai/user/cfyuanyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan public-web searches, choose Chinese domestic, global, or mixed routes, generate starter URLs, apply dynamic-information guardrails, and report reliability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer searches toward Chinese search services and public third-party search URLs.

Mitigation: Use it only for public-web discovery and avoid submitting secrets, private text, account data, or sensitive itinerary details to search services.

Risk: The fallback guidance includes shell-based curl fetching for public search pages.

Mitigation: Do not permit exec plus curl for ordinary searching unless the environment and query have been reviewed for data exposure risk.

Risk: Search results for flights, prices, inventory, bookings, tickets, finance, and news can be stale or incomplete.

Mitigation: Treat public search as preliminary discovery and rely on real-time, official, or transaction-adjacent pages before making final decisions.

## Reference(s):

- [Dynamic Information Boundary Rules](artifact/references/dynamic-info.md)
- [Source Priorities](artifact/references/priorities.md)
- [Intent Classification](artifact/references/intent-classification.md)
- [Direct Site URL Templates](artifact/references/direct-templates.md)
- [Reusable Search Patterns](artifact/references/use-cases.md)
- [Fallback Strategy](artifact/references/fallbacks.md)
- [Reliability Scoring](artifact/references/reliability-scoring.md)
- [Reporting Template](artifact/references/reporting-template.md)
- [Chinese-Site Search Guidance](artifact/references/domestic-search.md)
- [Global-Site Search Guidance](artifact/references/international-search.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [JSON search plans and Markdown report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes intent, route, dynamic subtype, starter URLs, source priority, reliability score, and reporting guidance.]

## Skill Version(s):

1.0.0 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
