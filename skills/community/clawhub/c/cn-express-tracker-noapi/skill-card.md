## Description:

中国快递物流查询工具，用于查询顺丰、圆通、中通、申通、韵达、京东、EMS 等中国快递公司的物流状态和轨迹，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanyuai](https://clawhub.ai/user/huanyuai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Chinese courier package status, logistics history, and detail links from a tracking number, with optional manual carrier selection when auto-detection is unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package tracking numbers, and sometimes courier-specific helper details such as phone-number suffixes, are sent to kuaidi100.com for lookup.

Mitigation: Confirm user intent before lookup and avoid using the skill for requests outside Chinese courier tracking contexts.

Risk: Very frequent repeated lookups can lead to short-term blocking by the external tracking service.

Mitigation: Follow the skill guidance to avoid repeatedly querying the same tracking number within short intervals.

Risk: Carrier auto-detection can be wrong or unavailable for some tracking numbers.

Mitigation: Ask the user to confirm the courier company and rerun the query with an explicit carrier code when results are missing or inconsistent.

## Reference(s):

- [中国快递公司代码参考表](references/courier-codes.md)
- [ClawHub skill page](https://clawhub.ai/huanyuai/skills/cn-express-tracker-noapi)
- [kuaidi100 query endpoint](https://www.kuaidi100.com/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text tracking summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include carrier name, tracking number, current status, reverse-chronological logistics events, and a kuaidi100 detail link.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
