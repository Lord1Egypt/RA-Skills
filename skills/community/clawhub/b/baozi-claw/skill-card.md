## Description: <br>
Complete Solana prediction markets skill for Baozi: list markets, get odds, place bets, and claim winnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Baozi Solana prediction markets, review odds and portfolio positions, and prepare betting or claim actions through an agent interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises Solana betting and claiming actions while the shipped code, documentation, and tool list are inconsistent. <br>
Mitigation: Install only for review or testing until the publisher aligns the shipped code, documentation, and tool list. <br>
Risk: Transaction-related tools use a shell-backed execution path and may receive untrusted free-form inputs. <br>
Mitigation: Verify the exact Baozi MCP version being executed and avoid passing untrusted free-form inputs to shell-backed tools. <br>
Risk: Betting and claiming can affect wallet funds. <br>
Mitigation: Do not allow autonomous betting or claiming; require manual wallet review and signature for every transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcusfranca12/baozi-claw) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Shell commands] <br>
**Output Format:** [JSON tool results returned to the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transaction-related outputs should be reviewed manually before any wallet signature or on-chain action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
