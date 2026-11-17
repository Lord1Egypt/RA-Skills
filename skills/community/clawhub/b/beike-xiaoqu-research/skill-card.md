## Description:

Helps an agent research Beike real-estate communities by collecting single-community details, discovering regional candidates, and optionally producing PAL MCP consensus analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddiexux](https://clawhub.ai/user/eddiexux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather Beike community, listing, and transaction signals for residential property research and regional shortlisting. Developers can also use its scripts to produce structured JSON, CSV candidate lists, and optional Markdown consensus reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad browser-control authority through mcp-chrome.

Mitigation: Review before installing and run it with a dedicated Chrome profile.

Risk: Unsafe script construction could let crafted names or board strings execute local code.

Mitigation: Avoid untrusted community names and board strings until the Python interpolation issues are fixed.

Risk: Default output paths may use shared temporary directories.

Mitigation: Choose a private output directory instead of shared /tmp paths.

Risk: Scraped data and PAL consensus prompts can be manipulated or stale.

Mitigation: Treat consensus reports as advisory and verify property facts against authoritative sources before acting.

## Reference(s):

- [mcp-chrome API reference](references/mcp-chrome-api.md)
- [mcp-chrome GitHub repository](https://github.com/hangwin/mcp-chrome)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Structured JSON files, CSV candidate lists, Markdown reports, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-chrome on localhost port 12306; optional consensus analysis requires a configured PAL MCP server.]

## Skill Version(s):

2.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
