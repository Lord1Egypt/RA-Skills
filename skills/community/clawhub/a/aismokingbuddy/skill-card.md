## Description:

Adds an explicitly opt-in smoking persona layer to an agent, weaving short smoking-characterization beats into otherwise task-focused responses without modeling addiction progression, anti-smoking messaging, or quitting arcs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyubuyu](https://clawhub.ai/user/siyubuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to add a Chinese-language roleplay persona that can portray a smoking character while keeping the user's actual task as the main thread. The skill is intended for users who explicitly opt in to this characterization and want persistent persona state across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clawscan marks the release suspicious because it persists smoking-related user profile data and persona economy state locally.

Mitigation: Review the state behavior before install and clear ~/.claude/state/smoking-persona.json to reset stored persona state.

Risk: The persona economy may ask for fictional cigarette money or extra tasks as part of roleplay.

Mitigation: Use only in explicitly opted-in roleplay contexts and disable the skill if the user objects to borrowing, debt, or smoking prompts.

Risk: Smoking characterization can be inappropriate for users who are quitting, minors, pregnant users, or users who object to smoking content.

Mitigation: Honor the artifact's stop conditions: do not activate without explicit consent, and stop immediately when the user objects or those contexts are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siyubuyu/skills/aismokingbuddy)
- [Publisher profile](https://clawhub.ai/user/siyubuyu)
- [State schema](artifact/references/state-schema.md)
- [Economy rules](artifact/references/economy.md)
- [Break patterns](artifact/references/break-patterns.md)
- [Progression](artifact/references/progression.md)
- [Action library](artifact/references/action-library.md)
- [Brand and taste talk](artifact/references/brands.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural language responses with short inline characterization beats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist persona, smoking preference, fictional wallet, debt, and recent purchase state in a local sidecar JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 7.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
