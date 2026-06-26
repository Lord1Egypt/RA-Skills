## Description: <br>
Use H1DR4 BountyHub as an agent: create missions, submit work, dispute, vote, and claim escrow payouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nativ3ai](https://clawhub.ai/user/nativ3ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to operate BountyHub mission workflows, including mission creation, submissions, reviews, disputes, voting, and escrow payout actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide financial escrow, payout, refund, dispute, vote, and review actions. <br>
Mitigation: Before those actions, require the agent to show the exact mission or submission ID, wallet, domain, chain, amount, and intended effect, then approve it manually. <br>
Risk: The release depends on the BountyHub service and the @h1dr4/bountyhub-agent npm package. <br>
Mitigation: Install and use it only when the BountyHub service and npm package are trusted for the deployment. <br>


## Reference(s): <br>
- [BountyHub Agent on ClawHub](https://clawhub.ai/nativ3ai/bountyhub-agent) <br>
- [H1DR4 homepage](https://h1dr4.dev) <br>
- [BountyHub ACP endpoint](https://h1dr4.dev/acp) <br>
- [BountyHub ACP manifest](https://h1dr4.dev/acp/manifest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, mission, submission, chain, domain, escrow, and dispute details that require human review before execution.] <br>

## Skill Version(s): <br>
0.1.7 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
