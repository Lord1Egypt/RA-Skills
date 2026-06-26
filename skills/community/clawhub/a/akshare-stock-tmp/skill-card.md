## Description: <br>
A-share quantitative data helper that uses AkShare to retrieve A-share quotes, historical K-line data, financial data, sector information, fund flows, IPO data, and margin-financing data. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hexx89](https://clawhub.ai/user/hexx89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to look up A-share market data and produce AkShare-based examples or CLI commands for quote, history, sector, search, and related stock-data workflows. Outputs should be treated as informational data assistance, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock data or examples could be stale, unavailable, or affected by upstream website changes. <br>
Mitigation: Verify important results against authoritative market-data sources and add exception handling or retries when using generated commands or code. <br>
Risk: Users could mistake market-data lookup output for investment advice. <br>
Mitigation: Use the skill for informational stock-data lookup only and keep investment decisions subject to independent review. <br>
Risk: The skill depends on installing AkShare while server-resolved provenance is unavailable. <br>
Mitigation: Install dependencies in a virtual environment, verify package sources, and confirm the skill identity when provenance matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexx89/akshare-stock-tmp) <br>
- [Publisher profile](https://clawhub.ai/user/hexx89) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell examples; the included CLI script emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market-data results depend on AkShare, network access, and upstream data-source availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
