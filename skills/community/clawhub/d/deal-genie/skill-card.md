## Description:

Deal Genie Enhanced turns a product screenshot or description into a Chinese-language commerce operations plan spanning product scoring, positioning, compliance review, platform copy, creative prompts, influencer matching, launch execution, follow-up conversion, data review, and optional Feishu push summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[user-zyj](https://clawhub.ai/user/user-zyj)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and influencer-marketing teams use this skill to decide whether to promote a product, prepare Chinese campaign content, coordinate creator outreach and sampling, manage launch-day actions, and review post-campaign performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign metrics, influencer details, product screenshots, and sales results may be posted to Feishu when webhook integration is enabled.

Mitigation: Use a dedicated webhook for the intended group, confirm recipient access before sending, and disconnect or rotate the webhook when it is no longer needed.

Risk: The skill implies ongoing preference learning from campaign results without clear retention or reset controls.

Mitigation: Avoid entering sensitive profile data unless storage, deletion, and reset behavior is known and acceptable.

## Reference(s):

- [Conversion Playbook](references/conversion_playbook.md)
- [Data Review Model](references/data_review.md)
- [Feishu Integration Guide](references/feishu_integration.md)
- [Influencer Matching Rules](references/influencer_matching.md)
- [Launch Execution Playbook](references/launch_execution.md)
- [Material Workshop Templates](references/material_workshop.md)
- [Tracking Management Templates](references/tracking_management.md)
- [ClawHub Skill Page](https://clawhub.ai/user-zyj/skills/deal-genie)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Chinese Markdown with optional HTML reports, tables, templates, and Feishu webhook configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core workflow does not require external APIs; optional Feishu integration can send summaries and reminders to configured groups or documents.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
