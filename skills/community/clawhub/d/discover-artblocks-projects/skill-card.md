## Description: <br>
Browse, search, and explore Art Blocks projects, collections, and collector portfolios using artblocks-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryley-o](https://clawhub.ai/user/ryley-o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and collectors use this skill to discover Art Blocks projects, inspect minting status and upcoming releases, explore artist project lists, and summarize collector wallets or token holdings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead agents from discovery into purchase-transaction follow-up tools that are outside the core browsing use case. <br>
Mitigation: Keep transaction-building or purchase actions out of scope unless the user explicitly requests them and independently reviews all transaction details before execution. <br>
Risk: Collector wallet and profile lookups may expose or aggregate public wallet holdings through the external artblocks-mcp server. <br>
Mitigation: Use wallet/profile queries only when the user requests them and is comfortable sending those identifiers to the external MCP server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryley-o/discover-artblocks-projects) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ryley-o) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown or text responses summarizing Art Blocks project, mint, artist, tag, and wallet data returned by MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project metadata, floor prices, mint progress, token traits, wallet summaries, media links, and Art Blocks links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
