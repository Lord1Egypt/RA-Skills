## Description: <br>
Easy Mining helps agents monitor and manage BTC mining farms through natural-language requests, including farm overviews, miner status, abnormal miner detection, revenue history, and confirmed batch operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External BTC mining farm operators and their agents use this skill to inspect farm health, hashrate, revenue, miner status, and task progress, then prepare operational actions such as reboots, power-mode changes, firmware updates, network scans, pool configuration, and locator-light flashes. Write operations should be executed only after the affected miners and task parameters are confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a live Nonce API key in chat. <br>
Mitigation: Use a tightly scoped and revocable API key where possible, avoid sharing long-lived credentials, and rotate the key if it may have been exposed. <br>
Risk: The skill can create sensitive miner task batches, including pool configuration, firmware updates, network scans, and reboots. <br>
Mitigation: Review the exact farm ID, miner IDs, task type, and parameters before approval, and require explicit confirmation before any write operation. <br>


## Reference(s): <br>
- [ClawHub Easy Mining release](https://clawhub.ai/deanpeng-dotcom/easy-mining) <br>
- [Nonce MCP Tools Reference](references/nonce-tools.md) <br>
- [Nonce App](https://app.nonce.app) <br>
- [Antalpha](https://www.antalpha.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries, JSON-style tool results, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can perform read-only mining farm queries and user-confirmed write operations using a user-provided Nonce API key.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
