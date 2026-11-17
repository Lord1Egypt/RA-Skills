## Description:

BUDDY 宠物系统 is a virtual pet companion skill for generating, interacting with, displaying, muting, and unmuting an AI pet in an agent session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use BUDDY to add a Tamagotchi-style companion to an AI coding session, with commands to hatch a deterministic pet, view its ASCII card, show petting animations, mute or unmute interactions, and emit a short AI context prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared persistent state in /tmp can expose or mix pet state across users on shared machines or multi-user agent runtimes.

Mitigation: Use a private per-user state directory before deploying in shared environments.

Risk: Broad activation rules and AI-context prompt behavior may trigger BUDDY in conversations where the user did not explicitly request it.

Mitigation: Narrow activation to explicit /buddy commands and review the generated AI context prompt before enabling automatic injection.

Risk: Saved pet names and the save command need review before installation.

Mitigation: Validate saved pet names and document the save command behavior for users and reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/skills/buddy-pet)
- [BUDDY skill instructions](artifact/SKILL.md)
- [BUDDY CLI script](artifact/scripts/buddy.ts)
- [BUDDY companion generator](artifact/references/buddy/companion.ts)
- [BUDDY type definitions](artifact/references/buddy/types.ts)
- [BUDDY sprite definitions](artifact/references/buddy/sprites.ts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include ASCII pet sprites, pet cards, status messages, and an optional AI context prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
