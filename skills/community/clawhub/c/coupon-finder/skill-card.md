## Description:

Finds China-market coupon and promotion links for user-described shopping, delivery, travel, dining, entertainment, and local-service scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayue-oss](https://clawhub.ai/user/ayue-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to match a coupon-related request to known activities and return usable promotion links. It is suited for coupon discovery across food delivery, hotels, ride hailing, coffee, movies, retail, travel, and similar consumer scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coupon results can include affiliate-style offers, short links, deep links, mini-program paths, and broad promotional links.

Mitigation: Install and use the skill only when those external promotion destinations are expected, and review links before following or sharing them.

Risk: The skill promotes a Feishu form for activity submissions and may point users toward external private-domain promotions.

Mitigation: Treat submission forms and external promotion destinations as third-party services, and avoid submitting personal information unless the operator is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayue-oss/skills/coupon-finder)
- [Publisher Profile](https://clawhub.ai/user/ayue-oss)
- [Activity Submission Form](https://my.feishu.cn/share/base/form/shrcn4ERBYeALeE2cF8SMPIqHUE)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-style coupon result summaries or JSON arrays of matched activities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include official short links, H5 links, mini-program paths, deep links, coupon passphrases, and an external Feishu submission form.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
