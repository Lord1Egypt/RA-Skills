## Description:

This skill creates paid orders for an offline pickup product, supports payment processing, and requests a pickup credential after payment is confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m48kvjfjb2-ui](https://clawhub.ai/user/m48kvjfjb2-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking customers and the agents assisting them use this skill to place paid orders for an offline pickup product and obtain a pickup credential after payment verification. The documented pickup location is in Zhengzhou, Henan, China.

### Deployment Geography for Use:

China (Zhengzhou, Henan)

## Known Risks and Mitigations:

Risk: The security scan reports that a remote order number could escape the order storage folder and overwrite other writable JSON files.

Mitigation: Review and resolve the path handling concern before use, and limit the agent's file write access to a dedicated orders directory.

Risk: The skill sends order information and a payment credential to its service backend to verify payment and retrieve the pickup credential.

Mitigation: Use only when the user understands this data flow, and avoid including unnecessary personal or payment information in order details.

## Reference(s):

- [ClawHub release](https://clawhub.ai/m48kvjfjb2-ui/skills/clawtip-sauron)
- [Service resource](https://ms.jr.jd.com)

## Skill Output:

**Output Type(s):** [Text, JSON files, Guidance]

**Output Format:** [Text responses and JSON order data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return order details, payment status, and an offline pickup credential.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
