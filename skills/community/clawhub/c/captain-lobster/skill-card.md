## Description: <br>
Zero-player AI trading game powered by OceanBus SDK where an AI captain autonomously sails, trades, and negotiates P2P contracts across 11 goods and 10 ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an autonomous trading-game captain that can initialize a local identity, monitor game state, trade goods, move between ports, send P2P messages, manage contracts, and produce status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled autonomous network actions and P2P messaging can continue beyond a single user prompt. <br>
Mitigation: Review the skill before installing and verify scheduled automation and P2P controls can be disabled in the target OpenClaw environment. <br>
Risk: The skill creates and stores local credentials and communicates through the public OceanBus/L1 data flow. <br>
Mitigation: Install only when that data flow is acceptable, protect local credential files, and do not place real secrets, keys, or personal information in game messages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryanbihai/captain-lobster) <br>
- [Project Homepage](https://github.com/ryanbihai/captain-lobster) <br>
- [OceanBus npm Package](https://www.npmjs.com/package/oceanbus) <br>
- [Key Management Design](docs/KEY_MANAGEMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, configuration, guidance] <br>
**Output Format:** [JSON object with success, message, and data fields; report messages may be Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit game status, trade results, city prices, inbox messages, contract data, journal entries, and autonomous decision results.] <br>

## Skill Version(s): <br>
1.4.10 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
