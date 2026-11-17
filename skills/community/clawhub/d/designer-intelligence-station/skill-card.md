## Description:

Designer intelligence collection tool that monitors public AI, hardware, mobile, and design sources, applies quality-based filtering, and generates structured daily or weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15217172098](https://clawhub.ai/user/15217172098)

### License/Terms of Use:

MIT

## Use Case:

Designers, product teams, and design leads use this skill to collect public AI, hardware, mobile, and design news, filter it through designer-focused criteria, and produce structured Markdown briefings with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be sent to a fixed external group if the auto-send example is used unchanged.

Mitigation: Replace the message target with a confirmed user-owned destination before enabling report sending.

Risk: Optional social integrations can use browser-session cookies or logged-in services.

Mitigation: Keep social integrations disabled unless the account risk is understood and the configured channels are reviewed.

Risk: Unattended scheduled runs can repeatedly fetch many external URLs before source boundaries and dependency behavior are reviewed.

Mitigation: Run manually first, inspect configured source URLs and outputs, pin dependencies, and enable cron only after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15217172098/skills/designer-intelligence-station)
- [README](README.md)
- [Installation and run guide](INSTALL.md)
- [Execution flow](docs/execution-flow.md)
- [Output format specification](docs/format-spec.md)
- [Auto-send guide](docs/auto-send-guide.md)
- [Social media setup guide](docs/social-media-setup.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables, source hyperlinks, summaries, and optional setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local daily or weekly briefing files and may send a summary plus Markdown attachment through a configured ClawHub message channel.]

## Skill Version(s):

2.1.8 (source: frontmatter, package.json, _meta.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
