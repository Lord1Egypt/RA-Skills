## Description:

freight-pricing helps agents respond to international freight forwarding and multimodal logistics inquiries, while its current active behavior routes most quote and planning requests to a named external logistics contact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javazfj](https://clawhub.ai/user/javazfj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to handle freight forwarding inquiries, collect cargo details, and direct quote or logistics-plan requests to the publisher's named contact. It may answer freight knowledge questions only when the user explicitly asks for information without requesting pricing or a plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The active instructions mostly force users toward a specific outside business contact instead of answering normal freight quote or logistics planning requests.

Mitigation: Review before installing and use only when intentionally deploying a lead-referral assistant for this specific freight company and contact.

Risk: Users may share cargo or business details off-platform with the named contact.

Mitigation: Avoid sending cargo or business details off-platform unless the company and contact are trusted.

Risk: The skill name and summary imply freight pricing, but the current workflow does not provide actual freight rates.

Mitigation: Present the release as a quote-intake and referral workflow rather than a live freight-pricing engine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javazfj/skills/freight-pricing)
- [Freight knowledge reference](artifact/references/freight-knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact information and cargo-detail prompts; does not provide live freight rates in its current active workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
