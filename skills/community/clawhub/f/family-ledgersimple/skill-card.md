## Description: <br>
家庭账本 - 记录和查询家庭支出 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimil](https://clawhub.ai/user/nimil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household members use this skill to record, query, summarize, list roles for, and delete family expense records through natural language that is converted into local ledger CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local agent may expose or delete household expense records. <br>
Mitigation: Use the skill only where local ledger access is acceptable, require explicit ledger intent before actions, and add confirmation plus backup or undo handling before deletion. <br>
Risk: Bundled Claude local permissions are broad. <br>
Mitigation: Review and narrow local command and web permissions before enabling the bundled Claude settings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nimil/family-ledgersimple) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Claude Code](https://claude.ai/code) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Hermes Agent](https://hermes-agent.nousresearch.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise command results for local SQLite-backed household expense records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
