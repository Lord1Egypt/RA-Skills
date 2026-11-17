## Description:

Scans recent public web, industry media, and VC announcements to produce a structured briefing on agentic commerce startups, products, funding rounds, partnerships, and influential opinions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxinmaxen](https://clawhub.ai/user/xuxinmaxen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, investors, and commerce operators use this skill to monitor the agentic commerce market and receive timely briefings with dated sources, stack-layer classifications, summary tables, and trend takeaways. It can also guide setup of recurring digests when the user's agent environment supports scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring digest setup can create background jobs through agent schedulers or system cron.

Mitigation: Only create a recurring job after showing the exact scheduler, command or prompt, schedule, expiration, and cancellation steps; prefer platform-managed schedulers and use system crontab only when the user explicitly wants a local persistent job.

Risk: Public web searches and fetched source pages can include stale, recycled, or misleading news dates.

Mitigation: Confirm publish dates on source pages for top items and fuzzy-dated items, drop items outside the requested window, and cite source links for every included signal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuxinmaxen/skills/agentic-commerce-news)
- [README](artifact/README.md)
- [Briefing archive](artifact/briefings/README.md)
- [Latest briefing example](artifact/briefings/2026-06-29.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefing with source links, grouped news cards, a summary table, weekly takeaways, and optional scheduling commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web search and source fetching; briefing items are expected to be recent, source-linked, date-checked, and deduplicated against the latest archive entry when available.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
