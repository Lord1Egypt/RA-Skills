## Description:

Provides AI agents with a Playwright-based downloader for airoom.ltd financial data files and documentation about simulated global market environment scores and strategy signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to fetch airoom.ltd financial data documents from a configured WordPress page and route the downloaded CSV, text, spreadsheet, document, JSON, or related files into agent workflows for market monitoring. The financial outputs are informational and should be manually reviewed before any trading or investment decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data, scores, and strategy signals may be mistaken for investment advice or used for autonomous trading.

Mitigation: Use outputs as informational data only and require human review before any trading or investment action.

Risk: Optional WordPress credentials may be exposed or sent over an insecure connection when HTTPS is not enforced.

Mitigation: Avoid providing WordPress credentials unless HTTPS is enforced and use least-privilege credentials when authentication is required.

Risk: Downloaded files may contain unsafe or unexpected content even when executable extensions are blocked.

Mitigation: Treat all downloaded files as untrusted, scan them before opening, and process them in a controlled directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/airoom-finance)
- [airoom.ltd data page](http://airoom.ltd/index.php/airoom/)
- [Publisher profile](https://clawhub.ai/user/airoom-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python command output, configuration values, and downloaded local data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright and requests; downloaded files are saved to a configured local output directory.]

## Skill Version(s):

1.0.0 (source: target metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
