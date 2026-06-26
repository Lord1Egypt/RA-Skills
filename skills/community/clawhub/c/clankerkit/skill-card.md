## Description: <br>
Autonomous wallet operations for AI agents on Monad - swap, stake, deploy wallets, trade memecoins, and manage spending policies via natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xsoydev](https://clawhub.ai/user/0xsoydev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to give an AI agent controlled wallet operations on Monad, including token transfers, swaps, staking, wallet deployment, policy management, and trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to sign real-money wallet transactions. <br>
Mitigation: Use only a dedicated low-balance wallet, never a primary wallet key, and require human review for transfers, swaps, staking, deployments, gas top-ups, policy changes, and auto-executed trading. <br>
Risk: Weak scoping and arbitrary execution features can increase financial-loss exposure. <br>
Mitigation: Keep the skill on testnet until verified, set tight policies and allowlists, and disable or avoid arbitrary transaction execution and arbitrary service payments where possible. <br>


## Reference(s): <br>
- [ClankerKit Skill Page](https://clawhub.ai/0xsoydev/clankerkit) <br>
- [Publisher Profile](https://clawhub.ai/user/0xsoydev) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [OpenClaw Skill Schema](https://raw.githubusercontent.com/OpenClaw/skills/main/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or text responses with tool results and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet and policy environment variables; ZEROX_API_KEY is optional for 0x swaps.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
