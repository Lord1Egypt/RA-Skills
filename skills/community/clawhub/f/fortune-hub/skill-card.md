## Description:

Routes broad fortune-telling requests to an appropriate specialist skill, collects only the needed profile fields, and reuses a local MEMORY.md profile across supported domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill when they want fortune-telling guidance but have not chosen a specific domain. The agent presents domain options, gathers the minimum required birth or question details, and routes the user to the corresponding specialist skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update a local plaintext MEMORY.md profile containing birth details, location, gender, and name data.

Mitigation: Use it only when profile reuse is acceptable, avoid providing a legal or passport name unless necessary, request one-off use when appropriate, and inspect or delete MEMORY.md after use.

Risk: Fortune-telling outputs could be mistaken for professional advice.

Mitigation: Treat generated guidance as entertainment only and consult qualified professionals for medical, legal, financial, relationship, or other consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eamanc-lab/skills/fortune-hub)
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with menus, prompts, routing instructions, and local MEMORY.md profile updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions and may create or update a local plaintext MEMORY.md profile.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
