## Description: <br>
Query historical and real-time crypto market data from 0xArchive across Hyperliquid, Lighter.xyz, HIP-3 builder perps, HIP-4 outcome markets, and Hyperliquid Spot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xfantommenace](https://clawhub.ai/user/0xfantommenace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to have an agent query 0xArchive market-data endpoints, generate curl commands, inspect historical and real-time crypto data, and reason about venue-specific coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or WebSocket URLs containing API keys could be exposed in logs or shared transcripts. <br>
Mitigation: Use a scoped, rotatable OXARCHIVE_API_KEY and avoid pasting real API-key URLs into logs, tickets, or chat transcripts. <br>
Risk: Web3 signup and subscription flows can involve wallet signing or paid USDC subscription steps. <br>
Mitigation: Require explicit user confirmation before any wallet-signing action or paid subscription flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xfantommenace/0xarchive) <br>
- [0xArchive API base](https://api.0xarchive.io/v1/...) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Markdown with curl examples, API endpoint guidance, and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the OXARCHIVE_API_KEY environment variable and may require wallet signing or paid subscription confirmation for Web3 and tiered access flows.] <br>

## Skill Version(s): <br>
1.10.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
