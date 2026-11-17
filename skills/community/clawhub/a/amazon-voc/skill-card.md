## Description:

Amazon-VOC collects Amazon customer reviews and turns them into voice-of-customer insights, trend summaries, and listing recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and analysts use this skill to collect and review customer feedback, identify recurring product issues and buying motivations, compare products, and prepare evidence-based listing recommendations.

### Deployment Geography for Use:

Global (Amazon marketplaces: US, UK, DE, JP, CA, FR, ES, and IT)

## Known Risks and Mitigations:

Risk: ARI credit charges may occur without a prompt, including through a command described as a free preview.

Mitigation: Prefer a release that fixes preview execution, set and verify autoconfirm is off, use quote before analysis, choose manual scheduling for one-time collection, approve recurring costs separately, and protect the locally saved ARI key.

## Reference(s):

- [ARI API reference](references/reference.md)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [Amazon-VOC on ClawHub](https://clawhub.ai/funewa/skills/amazon-voc)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance, Shell commands]

**Output Format:** [Concise review summaries or structured Markdown VOC reports with findings, trends, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are based on collected review samples and available time ranges; recommendations should reflect those evidence limits.]

## Skill Version(s):

1.5.4 (source: server-resolved release metadata; artifact frontmatter: 1.5.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
