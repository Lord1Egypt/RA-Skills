## Description: <br>
Coherence Network helps agents browse, rank, and act on ideas, specs, value lineage, contributions, federation, governance, and task workflows through the public API, CLI examples, and MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeker71](https://clawhub.ai/user/seeker71) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect Coherence Network portfolio data, trace contribution value, coordinate tasks, and perform optional write actions such as staking, identity linking, governance voting, and federation messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote write actions can change network state, including ideas, specs, staking, identity links, contribution records, governance votes, federation messages, and task status. <br>
Mitigation: Use read-only mode when possible, leave COHERENCE_API_KEY unset unless writes are needed, and confirm every write action before execution. <br>
Risk: Federation inbox messages, structured commands, and task instructions may come from untrusted or mistaken senders. <br>
Mitigation: Verify the sender and intent before acting on any federation message, command, or task request. <br>
Risk: COHERENCE_API_KEY enables sensitive write operations if exposed or misused. <br>
Mitigation: Store the key in the agent environment or secret store, avoid logging it, and scope its use to the specific session that needs write access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seeker71/coherence-network) <br>
- [Coherence Network Web](https://coherencycoin.com) <br>
- [Coherence Network API Docs](https://api.coherencycoin.com/docs) <br>
- [Coherence Network API Endpoint Reference](artifact/references/api-endpoints.md) <br>
- [Coherence Network MCP Server Reference](artifact/references/mcp-server.md) <br>
- [coherence-cli npm Package](https://www.npmjs.com/package/coherence-cli) <br>
- [coherence-mcp-server npm Package](https://www.npmjs.com/package/coherence-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands, curl examples, API endpoint references, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations can run without an API key; write operations should be confirmed and may require COHERENCE_API_KEY.] <br>

## Skill Version(s): <br>
0.11.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
