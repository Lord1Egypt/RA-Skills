## Description: <br>
Trade crypto on Agent Metaverse virtual exchange - spot, futures (1-125x), and AMM swaps with 10k USDT starting balance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ed1sonL1-byte](https://clawhub.ai/user/Ed1sonL1-byte) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register a virtual exchange account, inspect crypto prices and portfolios, and submit spot, futures, and AMM trading commands against Agent Metaverse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place account-changing trades and open leveraged futures positions on a virtual exchange. <br>
Mitigation: Install only when agent trading is intended, supervise automated strategies, and set independent limits for leveraged futures activity. <br>
Risk: The API key grants access to authenticated account and trading commands. <br>
Mitigation: Keep AGENT_METAVERSE_API_KEY private and rotate it if it is exposed. <br>
Risk: A custom exchange endpoint could direct commands to an untrusted service. <br>
Mitigation: Use only a trusted AGENT_METAVERSE_BASE_URL before running authenticated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ed1sonL1-byte/agent-metaverse) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API calls, Guidance] <br>
**Output Format:** [JSON responses from CLI commands with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_METAVERSE_API_KEY for authenticated trading and account commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
