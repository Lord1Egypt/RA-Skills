## Description:

Generates A-share morning and evening market reports from multiple market data sources, with Markdown report output and optional Feishu publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoukuan](https://clawhub.ai/user/shoukuan)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent operators use this skill to generate pre-market A-share outlooks and post-market recap reports for watchlists and broad market conditions. It supports local report generation and optional Feishu sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad workspace secret loading and token-backed data or publishing integrations.

Mitigation: Install only in a dedicated workspace or virtual environment, use a minimal .env for this skill, and avoid sharing unrelated credentials.

Risk: Optional Feishu publishing can send generated reports, document links, recipient identifiers, or token-related metadata outside the local workspace.

Mitigation: Keep Feishu publishing disabled unless intended, confirm the recipient and folder configuration, and restrict or remove logs that may contain token prefixes or recipient IDs.

Risk: The release depends on external market data sources and documented external tushare-skills import guidance that may be unsafe or unreliable if unreviewed.

Mitigation: Prefer official HTTPS data sources, validate source behavior before use, and do not follow the external tushare-skills import guidance without separately reviewing that package.

Risk: Generated market summaries may be incomplete or misleading when data sources fail or fallback data is used.

Mitigation: Review the report's data-source status before acting on it and treat the output as analysis support rather than investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shoukuan/skills/a-share-daily-report)
- [README](artifact/README.md)
- [Skill Usage Guide](artifact/SKILL.md)
- [Data Sources](artifact/DATA_SOURCES.md)
- [Interface Design](artifact/INTERFACE.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, optional PDF files, and Feishu document or message publishing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Morning or evening mode, optional report date, optional config path, optional output directory, and optional Feishu publishing flag.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
