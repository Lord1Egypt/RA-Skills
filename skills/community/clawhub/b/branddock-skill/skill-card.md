## Description:

Work on-brand with Branddock, the brand memory and brand check for AI, by fetching real brand context first, writing with it, scoring outputs with the F-VAL brand check, and leaving publishing to the human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erikjager55](https://clawhub.ai/user/erikjager55)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to connect an agent to Branddock, fetch brand context before drafting, create or rewrite brand-aware content, score outputs with F-VAL, and keep final publishing approval with a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand context and text submitted for scoring or generation may be sent to Branddock.

Mitigation: Use the skill only when Branddock processing is intended, avoid submitting secrets or unrelated sensitive text, and rely on Branddock context rather than inventing brand facts.

Risk: Paid generation actions can consume credits, especially high-credit SEO, campaign, image, or video work.

Mitigation: Confirm the cost and user intent before paid generation, and keep final publishing, scheduling, or sending approval with the human.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/erikjager55/skills/branddock-skill)
- [Branddock MCP Connector](https://branddock.app/mcp)
- [Branddock REST API](https://branddock.app/api/v1)
- [Brand Context Endpoint](https://branddock.app/api/v1/brand-context)
- [Brand Scoring Endpoint](https://branddock.app/api/v1/score)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call instructions, optional inline REST examples, F-VAL scores, findings, and human approval next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Branddock score thresholds, revision findings, and credit-cost notices for paid generation actions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
