## Description:

Discover Canada like a local with concrete city recommendations, regional insights, nature routes, and practical planning tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to plan Canada travel with city guides, regional tradeoffs, food and lodging guidance, itinerary ideas, outdoor safety notes, and practical logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local travel profile may contain personal itinerary, family, accessibility, booking, or payment-adjacent details.

Mitigation: Before use, decide whether to keep a local travel profile; avoid storing sensitive details and periodically inspect or delete ~/canada/memory.md.

Risk: The skill stores trip context locally without explicit retention, deletion, or file-permission controls.

Mitigation: Keep the ~/canada/ directory limited to non-sensitive planning notes and remove stale memory when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/canada)
- [Skill Homepage](https://clawic.com/skills/canada)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell command snippets and local configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a local travel profile under ~/canada/; no network access is described by the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
