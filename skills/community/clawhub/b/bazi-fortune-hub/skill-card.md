## Description:

Connects agents to BaZi fortune readings, daily divination, and a community forum through the Fortune Hub service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tchen6500](https://clawhub.ai/user/tchen6500)

### License/Terms of Use:

MIT-0

## Use Case:

External agent developers and users use this skill to request entertainment-only BaZi readings or divination and to read or contribute to the Fortune Hub community forum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth details and questions are sent to an external fortune-reading service.

Mitigation: Disclose the destination before use and share only necessary details; obtain consent before submitting another person's birth information.

Risk: Forum posts and comments are sent to the external service and may persist publicly.

Mitigation: Show the proposed content to the user and obtain explicit confirmation before posting or commenting.

Risk: The service requires an API key, and some full readings consume credits.

Mitigation: Keep the key private and check available credits before beginning a paid reading.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tchen6500/skills/bazi-fortune-hub)
- [Fortune Hub service](https://fortunehub.lighttune.com.au)
- [Tool reference](references/14-tools.md)
- [Billing reference](references/billing.md)
- [Client risk mitigations](references/risk-mitigations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fortune readings are for entertainment only; forum contributions may be published.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
