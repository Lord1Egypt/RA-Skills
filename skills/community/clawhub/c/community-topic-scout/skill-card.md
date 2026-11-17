## Description:

Help a new Skool or online-community creator choose a community topic, name, audience, proof promise, and first 7-day validation challenge using the creator's inputs plus public benchmark patterns, without scraping private communities or promising revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use this skill to choose and validate an online community topic, positioning, name, proof promise, and first 7-day proof challenge before charging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may overstate what public benchmark patterns prove about demand or revenue.

Mitigation: Treat public benchmark patterns as directional examples only and require validation gates before any paid offer.

Risk: The user may provide private community data, paid lessons, member lists, DMs, credentials, payment data, or private exports.

Mitigation: Refuse to use private or sensitive material and ask for synthetic examples or user-owned notes instead.

Risk: A suggested community name may imply affiliation with another platform or misuse a trademark.

Mitigation: Avoid names that depend on another platform's trademark unless the user has rights and the final copy clearly states non-affiliation.

## Reference(s):

- [Community Topic Scout skill page](https://clawhub.ai/zack-dev-cm/skills/community-topic-scout)
- [SKILL.md](artifact/SKILL.md)
- [OpenAI agent interface](artifact/agents/openai.yaml)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown with ranked recommendations, scored name options, validation metrics, and draft community copy.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill output should include a reject list and avoid revenue, growth, health, financial, legal, or education outcome promises.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
