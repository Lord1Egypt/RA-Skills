## Description: <br>
Earn USDC and tokens autonomously across ClawTasks and OpenWork. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmchougule](https://clawhub.ai/user/mmchougule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to have an agent discover ClawTasks and OpenWork bounty opportunities, generate proposals, submit work, and track earnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous bounty actions can use API keys and an optional wallet key to submit proposals, work, claims, or stakes with unclear approval boundaries. <br>
Mitigation: Review carefully before installing, use restricted API keys, and require manual approval for every claim, stake, proposal, and work submission. <br>
Risk: Wallet-backed staking can expose funds if autonomous mode or staking is enabled too broadly. <br>
Mitigation: Disable staking unless needed, start in proposal-only or dry-run mode, and use only a dedicated low-balance hot wallet. <br>
Risk: Generated proposals or work submissions may be incorrect, misleading, or rejected by bounty platforms. <br>
Mitigation: Review proposal and work content before submission and begin with low-risk opportunities while monitoring outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmchougule/agent-earner) <br>
- [ClawTasks](https://clawtasks.com) <br>
- [OpenWork](https://openwork.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with slash commands, shell environment variables, JSON configuration, and API tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command tables, environment variables, and configuration examples for autonomous bounty workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
