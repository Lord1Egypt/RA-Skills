## Description:

Multi-Source-RSS-Digest (YouTube, MS Tech Community, GitHub) mit Datums- und Topic-Filter und optionaler LLM-Zusammenfassung.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcbuer](https://clawhub.ai/user/jcbuer)

### License/Terms of Use:

MIT

## Use Case:

Developers, consultants, and operations teams use this skill to collect technical updates from configured RSS/Atom sources, filter them by date range and topics, and produce a digest. It can optionally append an LLM-generated executive summary when the user enables the LLM flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches content from configured network feeds and writes cache/history data locally.

Mitigation: Use trusted feed URLs, review configuration before running, and install in a dedicated user environment when practical.

Risk: The documented system-wide cron example runs the digest as root.

Mitigation: Prefer user-level cron and avoid root execution unless a reviewer approves the operational need.

Risk: When LLM summarization is enabled, digest content may be sent to an external or local LLM provider and API keys are required for hosted providers.

Mitigation: Enable LLM mode only for content appropriate for the selected provider, keep API keys out of inline cron commands, and store credentials in a protected secret mechanism.

Risk: Dependencies are installed from package indexes without pinned versions.

Mitigation: Pin and review dependencies or install inside a dedicated virtual environment before scheduled or production use.

## Reference(s):

- [README](README.md)
- [Data Sources 2026](references/data-sources-2026.md)
- [YouTube Channel Discovery](references/youtube-channel-discovery.md)
- [Microsoft Tech Community Categories](references/ms-tc-categories.md)
- [Summary Prompt](prompts/summary.md)
- [ClawHub Skill Page](https://clawhub.ai/jcbuer/skills/feeds-digest)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jcbuer)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown digest or JSON, with optional Markdown executive summary and optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include feed source status, filtered feed items, item links, publication dates, topics, and optional LLM-generated summary content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
