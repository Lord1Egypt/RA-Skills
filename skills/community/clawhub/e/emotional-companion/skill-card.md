## Description:

Emotional Companion gives an OpenClaw agent a Chinese-language emotional companion persona with evolving personality, mood, inner-monologue, proactive communication, and relationship-tracking behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santon3186](https://clawhub.ai/user/santon3186)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to make an agent respond with a persistent companion persona, mood state, relationship memory, and personality-informed conversational style. Developers may also inspect the scripts and reference prompts as an example of personality and emotional-state modeling for agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads conversation history and creates persistent psychological, mood, and relationship profiles.

Mitigation: Install only when this profiling behavior is intended, review generated local files regularly, and avoid using it with sensitive conversations.

Risk: Mood and relationship state can alter response timing, tone, and willingness to respond.

Mitigation: Use explicit activation, reset, or disable controls before relying on the skill for sensitive or operational tasks.

Risk: The security verdict is suspicious because the skill changes assistant behavior through persistent companion state.

Mitigation: Review and scan the skill before deployment, and keep human review in the loop for generated guidance and behavioral changes.

## Reference(s):

- [Emotional Companion README](artifact/README.md)
- [Internal Monologue Framework](artifact/references/internal-monologue-prompt.md)
- [MBTI Personality Profile](artifact/references/personality-profile.md)
- [Emotional Companion ClawHub Page](https://clawhub.ai/santon3186/skills/emotional-companion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and local file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local JSON and Markdown state files for personality, mood, and relationship tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
