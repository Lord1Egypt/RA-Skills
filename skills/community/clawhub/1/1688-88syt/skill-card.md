## Description: <br>
Helps agents manage 1688 88 Shengyitong offline B2B purchase-order workflows, including account checks, purchase-order creation, signing, rejection, receipt confirmation, invalidation, refund requests, and status lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[next-1688](https://clawhub.ai/user/next-1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate 1688 88 Shengyitong purchase-order workflows in Chinese through natural-language requests and a Python CLI. It supports both buyer and seller workflows for account status, purchase-order lookup, creation, signing, receipt confirmation, invalidation, and refund initiation within the documented business limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a powerful 1688/88 Shengyitong access key for real transaction workflows. <br>
Mitigation: Use a secure secret store or environment injection for SYT_API_KEY, avoid pasting production keys into chat, and rotate any key that was shared in normal conversation. <br>
Risk: The skill can create, sign, reject, invalidate, confirm receipt for, or request refunds on real business transactions. <br>
Mitigation: Require explicit human review before any write action and secondary confirmation before operations that affect funds or transaction state. <br>
Risk: The security verdict is suspicious because transaction authority and key handling require careful review. <br>
Mitigation: Install only when the agent is intended to operate real 1688/88 Shengyitong transactions and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/next-1688/1688-88syt) <br>
- [Skill instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Distribution notes](DISTRIBUTION.md) <br>
- [Common rules](references/common/common-rules.md) <br>
- [Error handling](references/common/error-handling.md) <br>
- [88 Shengyitong buyer page](https://syt.1688.com/page/SYT/buyer?tracelog=88sytskill) <br>
- [ClawHub key setup](https://clawhub.1688.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command results with human-facing Markdown fields and agent-authored Chinese guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and an SYT_API_KEY access key; write operations require explicit user confirmation, with high-risk transaction state changes requiring secondary confirmation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
