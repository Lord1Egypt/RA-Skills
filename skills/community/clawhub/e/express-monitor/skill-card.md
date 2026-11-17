## Description:

快递监控Skill - 查询快递物流、绑定手机号自动获取快递、同步到飞书

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators can use this skill to query courier tracking numbers, bind a phone number for delivery monitoring, view local shipment history, and summarize package statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers are sent to Kuaidi100, and phone numbers plus shipment history are stored locally under the OpenClaw workspace.

Mitigation: Install only when users accept this data flow; disclose the Kuaidi100 lookup and local storage behavior before use.

Risk: The artifact claims phone data is encrypted, but the security evidence says phone numbers are stored in plaintext.

Mitigation: Remove the encryption claim until encryption is implemented, or add real protection and data minimization for stored phone numbers.

Risk: Automatic sync and Feishu-related release claims are not fully supported by the artifact behavior described in the security guidance.

Mitigation: Revise the skill before broad use to remove unsupported claims or implement the missing behavior.

Risk: There is no delete or unbind workflow for locally stored phone data.

Mitigation: Add a delete or unbind command so users can remove stored phone numbers and shipment history.

## Reference(s):

- [express-monitor ClawHub page](https://clawhub.ai/hongjiahao371-pixel/skills/express-monitor)
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel)
- [Kuaidi100 mobile query service](https://m.kuaidi100.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs courier company, shipment status, recent tracking events, bound phone list, and local history summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
