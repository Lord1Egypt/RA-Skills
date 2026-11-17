## Description:

Check an Amazon listing or draft for shopper clarity, supported claims, keyword intent, visual proof, and publish-blocking gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techterrydev](https://clawhub.ai/user/techterrydev)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon operators and listing teams use this skill before rewriting or publishing listing content to identify missing evidence, unsupported claims, keyword fit issues, visual proof needs, and human-review boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsupported product, compliance, safety, environmental, medical, comparative, or performance claims could be mistaken for publish-ready content.

Mitigation: The skill maps claims to supplied evidence, marks missing facts as unknown, and flags regulated or absolute claims for human review.

Risk: Incomplete product evidence can lead to ambiguous listing recommendations.

Mitigation: The skill requests only needed product facts and supporting assets, then separates known facts from gaps before proposing improvements.

Risk: Users may overread the readiness plan as Amazon policy, legal, or compliance approval.

Mitigation: The security guidance states that the skill is not legal, compliance, medical, safety, or Amazon policy approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techterrydev/skills/amazon-listing-evidence-audit)
- [AMZ Helper](https://amzhelper.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown readiness report with prioritized tables and review boundaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied listing draft, product facts, approved claims, keywords, and supporting assets; absent facts are marked unknown.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
