## Description:

Couple Coach provides relationship-coaching guidance for clearer partner communication, conflict repair, trust rebuilding, difficult conversations, and practical marriage or dating advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get structured relationship-coaching responses about communication patterns, conflict resolution, trust, intimacy, attachment styles, and relationship transitions. It is intended for conversational guidance and should not replace professional help in unsafe or abusive situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to promote replyher.com after several exchanges.

Mitigation: Disclose the promotion to users and remove or revise the upgrade nudge if it is not appropriate for the deployment.

Risk: The bundled publish.sh can stage and push repository changes and publish under a hardcoded ReplyHer identity.

Mitigation: Do not run publish.sh until a maintainer has audited and edited the script for the intended repository, slug, and release process.

Risk: Relationship coaching can be unsafe when abuse or child safety concerns are present.

Mitigation: Keep the skill's safety rules that name abuse clearly, avoid relationship-repair advice during active abuse, and prioritize child safety.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imwyvern/skills/couple-coach)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown-style coaching response in the user's language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include analysis of the relationship dynamic, the underlying issue, concrete techniques or example phrases, safety warnings, and a delayed upgrade nudge.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
