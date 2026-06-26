## Description: <br>
Autonomous agent guidance for managing Adam's side-income workflows across AI services, packaged skill publishing, automated trading, and personal finance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamwgp](https://clawhub.ai/user/adamwgp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to coordinate a side-business operating system for service sales, ClawHub skill publishing, trading workflows, and personal finance reminders. It is intended as operational guidance rather than a standalone executable tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact exposes live-looking secrets, wallet details, and wallet backup paths. <br>
Mitigation: Rotate or revoke exposed keys, remove secrets and wallet paths from the skill text, and avoid granting the skill access to secret stores by default. <br>
Risk: The skill asks an agent to make autonomous trading, publishing, marketplace, and personal finance decisions. <br>
Mitigation: Require explicit approval gates before trading, publishing, marketplace actions, spending, or access to personal financial data. <br>
Risk: Financial and trading guidance may cause monetary loss if executed without review. <br>
Mitigation: Treat outputs as proposals, review them manually, and enforce conservative limits before any financial action is taken. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adamwgp/adam-bounty-hunter) <br>
- [Soul.Markets service page](https://soul.mds.markets/gellycat-adam-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with command tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose operational, publishing, trading, and finance actions that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
