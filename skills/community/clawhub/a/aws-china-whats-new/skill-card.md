## Description:

Provides AWS China Region service launch announcements and availability details for Beijing and Ningxia from 2016 to present, including dates and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jowhee327](https://clawhub.ai/user/jowhee327)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud teams use this skill to answer AWS China availability and launch timeline questions for the Beijing and Ningxia regions using indexed AWS China What's New announcements. The skill helps summarize matching services, launch dates, regions, and source announcement links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local announcements cache can be stale or contain internally mismatched records.

Mitigation: Run the incremental update before time-sensitive answers and verify important availability or launch-date decisions against the linked AWS announcement.

Risk: Refreshing data makes outbound requests to www.amazonaws.cn.

Mitigation: Install and run the skill only in environments where that outbound network access is acceptable.

Risk: No indexed announcement does not prove that a service is unavailable in AWS China.

Mitigation: State this limitation in answers and corroborate important availability conclusions with official AWS regional service documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jowhee327/skills/aws-china-whats-new)
- [AWS China What's New](https://www.amazonaws.cn/en/new/)
- [AWS China Regional Product Services](https://www.amazonaws.cn/en/about-aws/regional-product-services/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summaries supported by JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries a local JSON cache and may refresh it from www.amazonaws.cn when data is stale.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
