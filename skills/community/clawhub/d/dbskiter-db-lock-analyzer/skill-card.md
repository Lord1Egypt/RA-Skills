## Description: <br>
数据库锁分析与死锁检测帮助代理分析当前数据库锁、检测死锁并追踪锁等待链。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database developers and operators use this skill to ask an agent for database lock analysis, deadlock checks, wait-chain tracing, reports, and transaction termination guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live database lock operations and includes a transaction-kill workflow without enough clear scoping or confirmation in the artifact. <br>
Mitigation: Before any transaction-kill action, require the agent to show the exact database, session or transaction ID, expected impact, and a separate explicit confirmation from an authorized operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-db-lock-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/magicczc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live database lock summaries, deadlock details, wait-chain analysis, reports, and transaction-kill command proposals that require operator confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
