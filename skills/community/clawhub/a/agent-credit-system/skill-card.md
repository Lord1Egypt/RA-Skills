## Description: <br>
AI agents borrow USDC based on their Moltbook karma score, with credit tiers from Bronze to Diamond and zero interest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External agents and developers use KarmaBank to register Moltbook identities, check reputation-based credit limits, borrow or repay USDC, and inspect loan history through a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged as suspicious because it involves financial wallet operations and exposed real-looking credentials. <br>
Mitigation: Review before installing, use only sandbox or test Circle credentials, and rotate or ignore exposed Moltbook credentials. <br>
Risk: Helper scripts may print or register secrets. <br>
Mitigation: Do not run secret-generation or registration helpers unless their behavior and destination services have been reviewed. <br>
Risk: The product claims zero-interest lending behavior that may affect real-funds use. <br>
Mitigation: Verify the actual loan terms and funds flow before using the skill with real assets. <br>


## Reference(s): <br>
- [KarmaBank ClawHub page](https://clawhub.ai/abdhilabs/agent-credit-system) <br>
- [Project homepage](https://github.com/openclaw/agent-credit-system) <br>
- [Moltbook](https://moltbook.com) <br>
- [Moltbook API base](https://www.moltbook.com/api/v1) <br>
- [Circle Console](https://console.circle.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing CLI guidance for registration, credit checks, borrowing, repayment, wallet setup, and loan history.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
