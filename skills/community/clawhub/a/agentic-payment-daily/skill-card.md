## Description:

Generate and deliver a daily Agentic Payment news briefing covering Visa Greater China updates, market trends, competitor protocols, and regulatory signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juncaijames](https://clawhub.ai/user/juncaijames)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up, edit, debug, or run a scheduled daily Agentic Payment briefing for Visa Greater China VIC workflows. The skill curates news, deduplicates against recent reports, writes an Obsidian Markdown report, converts it to PDF, and delivers the report to WeChat.

### Deployment Geography for Use:

Global; report content is tailored to Visa Greater China and APAC signals.

## Known Risks and Mitigations:

Risk: The skill can run on a schedule and send generated PDFs to a hardcoded WeChat recipient.

Mitigation: Make the destination configurable, require confirmation before sends, and review the recipient before enabling cron delivery.

Risk: The skill writes business reports to a fixed local Obsidian path.

Mitigation: Restrict writable paths to approved report locations and confirm the destination before sharing generated reports.

Risk: The PDF converter uses shell-string execution and renders generated HTML.

Mitigation: Avoid shell-string execution, pass arguments safely, and escape or sanitize report content before rendering HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juncaijames/skills/agentic-payment-daily)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report text, Obsidian Markdown file, PDF file, inline shell commands, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local report files, generate a PDF, and deliver that PDF through a messaging channel when configured or scheduled.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
