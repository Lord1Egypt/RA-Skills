## Description:

Run a self-contained Chinese and international AI news workflow inside the current workspace. Use when the user wants either high-frequency RSS capture only or scheduled report delivery only, with cumulative Excel outputs and a merged Word brief, without relying on an external local repository path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nighmat1220](https://clawhub.ai/user/nighmat1220)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to collect Chinese and international AI news from configured RSS feeds, generate AI-assisted titles, summaries, and impact scores, and produce cumulative Excel reports plus a daily Word brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External API credentials and RSS credentials are used at runtime.

Mitigation: Run the skill in a dedicated workspace, provide credentials only through trusted configuration or environment variables, avoid feed credentials on plaintext URLs, and set ARK_API_BASE only to a trusted model provider.

Risk: Untrusted RSS content is collected and later summarized or written into reports.

Mitigation: Use trusted HTTPS RSS sources, review generated summaries before sharing, and use --disable-ai when processing sensitive content.

Risk: Generated XLSX reports may contain untrusted spreadsheet content.

Mitigation: Treat generated XLSX files as untrusted until formula escaping is added, and review them before opening or distributing in higher-trust environments.

## Reference(s):

- [Commands reference](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/nighmat1220/skills/ai-news-pipeline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated workspace files include JSONL data, XLSX reports, DOCX briefs, logs, snapshots, and state JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports capture-only, report-only, full workflow, explicit reporting windows, and a disable-AI mode.]

## Skill Version(s):

1.0.4 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
