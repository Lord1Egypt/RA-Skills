## Description: <br>
A Clawdbot skill that gives an agent native access to DWLF, a market analysis platform for crypto and stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andywilliams](https://clawhub.ai/user/andywilliams) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to DWLF for market analysis, trade signals, backtesting, portfolio tracking, watchlists, trade journaling, chart annotations, strategy building, and academy content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad authenticated DWLF API calls that read or modify account data. <br>
Mitigation: Install only for trusted DWLF accounts and require explicit user approval before write, delete, purge, bulk activation, settings, trade, strategy, watchlist, or API-key operations. <br>
Risk: The helper script may look for a locally stored API key if DWLF_API_KEY is not set. <br>
Mitigation: Prefer the DWLF_API_KEY environment variable and avoid storing plaintext credentials in workspace files. <br>


## Reference(s): <br>
- [DWLF Skill on ClawHub](https://clawhub.ai/andywilliams/dwlf) <br>
- [DWLF Website](https://dwlf.co.uk) <br>
- [DWLF API Base](https://api.dwlf.co.uk/v2) <br>
- [DWLF API Endpoints Reference](references/api-endpoints.md) <br>
- [DWLF Strategy Builder Reference](references/strategy-builder.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq helper commands with DWLF API key authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
