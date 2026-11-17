## Description:

Recommends popular and highly-rated skills from ClawHub based on user intent and conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandon-zhanghaodong](https://clawhub.ai/user/brandon-zhanghaodong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover ClawHub skills that match their current task, such as development, productivity, communication, search, or automation needs. It helps compare options and returns concise recommendations with links and install commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recommended skill could be treated as trusted solely because this recommender surfaced it.

Mitigation: Before installing, review the recommended skill's publisher, permissions, install hooks, persistence behavior, communication access, and agent-behavior changes.

Risk: Recommendation data can become stale as skill popularity, ratings, publishers, or security posture change.

Mitigation: Confirm current ClawHub metadata and security status before relying on a recommendation for production use.

## Reference(s):

- [ClawHub Recommender release page](https://clawhub.ai/brandon-zhanghaodong/skills/clawhub-recommender)
- [Popular ClawHub Skills](references/popular_skills.md)
- [Recommendation Logic for ClawHub Skills](references/recommendation_logic.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline install commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are generated from user intent, conversation context, and bundled ClawHub skill reference material.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
