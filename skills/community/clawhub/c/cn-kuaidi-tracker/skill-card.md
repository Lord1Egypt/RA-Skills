## Description:

快递追踪助手。输入快递单号查询物流状态，自动识别快递公司。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query China courier tracking status by tracking number, auto-detect supported couriers, and maintain a local list of shipments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Courier tracking numbers are sent to Kuaidi100 during lookups.

Mitigation: Use the skill only when sharing the tracking number with Kuaidi100 is acceptable.

Risk: The local tracking list is stored as plaintext JSON.

Mitigation: Avoid sensitive deliveries on shared systems and remove stored entries when they are no longer needed.

Risk: Clear and delete commands can erase the local tracking list without an additional confirmation step.

Mitigation: Review the command text before running deletion or clear operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-kuaidi-tracker)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [Kuaidi100](https://www.kuaidi100.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query Kuaidi100 and may save a plaintext local tracking list.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
